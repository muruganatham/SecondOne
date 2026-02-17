"""
AI API Endpoint
Exposes the Text-to-SQL functionality.
Role-based access control enabled.
Supports both Synchronous (Blocking) and Asynchronous (Non-Blocking) modes.
"""
from typing import Optional, Dict, Any
import uuid
import time
import asyncio
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.services.ai_service import ai_service
from app.services.schema_context import schema_context
from app.services.sql_executor import sql_executor
from app.models.profile_models import Users, UserAcademics
from app.core.security import get_current_user, RoleChecker
from app.core.db import get_db, SessionLocal
from app.prompts import (
    get_admin_prompt, 
    get_student_prompt, 
    get_staff_prompt, 
    get_college_admin_prompt, 
    get_trainer_prompt, 
    get_content_creator_prompt
)

router = APIRouter()

# In-memory Job Store for Async Queries
# { "job_id": { "status": "processing" | "completed" | "failed", "result": ..., "created_at": ... } }
JOB_STORE: Dict[str, Any] = {}

class AIQueryRequest(BaseModel):
    question: str
    model: str = "deepseek-chat"  # Default to DeepSeek
    user_id: Optional[int] = None
    user_role: Optional[int] = None

class AIQueryResponse(BaseModel):
    answer: str
    sql: str | None = None
    data: list | None = None
    follow_ups: list = []

# --- CORE LOGIC ---

async def _process_ai_query(request: AIQueryRequest, db: Session) -> dict:
    """
    Core Logic for processing AI queries.
    Refactored for reuse in Sync and Async modes.
    Contains all AI interaction, security checks, and DB Execution.
    """
    question = request.question
    model = request.model
    
    # 0. User Context Identification
    current_user = None
    
    if request.user_id:
        current_user = db.query(Users).filter(Users.id == str(request.user_id)).first()
        if current_user and request.user_role:
            current_user.role = request.user_role
            
    # Fallback/Mock if user doesn't exist
    if not current_user:
        current_user = Users(
            id=str(request.user_id or "0"),
            email="static-frontend@app.local",
            name="Static Frontend App",
            role=request.user_role if request.user_role is not None else 0,
        )
    
    # 1. Get Schema Context
    system_prompt = schema_context.get_system_prompt()
    
    # 1.5 Role-Based Search Control
    # Initialize variables to prevent Scope Errors
    role_instruction = ""
    college_short_name = "admin"
    current_role_id = current_user.role
    
    # Ensure current_role_id is int for reliable comparison
    try:
        current_role_id = int(str(current_role_id))
    except:
        current_role_id = 7
    
    if current_role_id in [1, 2]: # Admin
        role_instruction = get_admin_prompt(current_user.id)
    
    elif current_role_id == 7: # Student
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        college_id = academics.college_id if academics else "Unknown"
        # college_short_name already initialized
        college_name = "Your Institution"
        dept_name = "Your Department"
        if academics:
            if academics.college:
                try:
                    college_short_name = str(academics.college.college_short_name).lower()
                    college_name = str(academics.college.college_name)
                except: pass
            if academics.department:
                try: dept_name = str(academics.department.department_name)
                except: pass
        role_instruction = get_student_prompt(dept_id, dept_name, college_id, college_name, college_short_name, current_user.id)
        
    elif current_role_id == 4: # Staff
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        dept_name = "Your Department"
        if academics and academics.department:
            dept_name = str(academics.department.department_name)
        role_instruction = get_staff_prompt(dept_id, dept_name, current_user.id)

    elif current_role_id == 3: # College Admin
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        college_id = academics.college_id if academics else "Unknown"
        # college_short_name already initialized
        college_name = "Your Institution"
        if academics and academics.college:
             try:
                 college_short_name = str(academics.college.college_short_name).lower()
                 college_name = str(academics.college.college_name)
             except: pass
        role_instruction = get_college_admin_prompt(college_id, college_name, college_short_name, current_user.id)

    elif current_role_id == 6: # Content
        role_instruction = get_content_creator_prompt(current_user.id)

    elif current_role_id == 5: # Trainer
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        dept_name = "Your Department"
        if academics and academics.department:
            dept_name = str(academics.department.department_name)
        role_instruction = get_trainer_prompt(dept_id, dept_name, current_user.id)
    
    else:
        role_instruction = "Your role is UNAUTHORIZED. ACCESS DENIED."
    
    # Security Interceptor
    effective_role = request.user_role if request.user_role is not None else current_user.role
    try: current_role_id = int(effective_role)
    except: current_role_id = 7
        
    print(f"SECURITY DEBUG: User={request.user_id}, Role={current_role_id}, Question='{question}'")

    if current_role_id not in [1, 2]:
        lower_q = question.lower()
        hard_bans = ["database schema", "list distinct data", "db schema", "system structure", "show databases", "show tables"]
        if any(ban in lower_q for ban in hard_bans):
            return {"answer": "Access Denied: You do not have permission to view system architecture.", "follow_ups": []}
            
        if "table" in lower_q or "database" in lower_q:
             if any(trigger in lower_q for trigger in ["list", "show", "what", "structure"]):
                 if "time table" not in lower_q and "timetable" not in lower_q:
                     return {"answer": "Access Denied: You cannot query database tables directly.", "follow_ups": []}

    # Construct Prompt
    system_prompt_with_context = f"{system_prompt}\n\n{'='*20}{role_instruction}\n{'='*20}\n\nTask: Generate SQL for: \"{question}\""
    
    # STEP 1: Analyze Schema (Non-blocking)
    analysis_guidance = ""
    try:
        print(f"🔍 Analyzing question with database schema...")
        analysis = await run_in_threadpool(
            ai_service.analyze_question_with_schema,
            user_question=question,
            schema_context=system_prompt_with_context,
            model=model
        )
        
        rec_tables = analysis.get('recommended_tables', [])
        rec_tables_str = ", ".join(rec_tables) if isinstance(rec_tables, list) else str(rec_tables)

        analysis_guidance = f"""
\n{'='*20}
[PRE-COMPUTED SCHEMA ANALYSIS]
Use the following expert analysis to guide your SQL generation:
1. **Recommended Tables**: {rec_tables_str}
2. **Query Type**: {analysis.get('query_type', 'unknown')}
3. **Strategy**: {analysis.get('suggested_sql_approach', 'Standard SQL')}
4. **Reasoning**: {analysis.get('reasoning', 'Follow standard protocols')}

CRITICAL INSTRUCTIONS:
- If recommended tables are provided, YOU MUST USE THEM (especially college-specific tables)
- Follow the suggested SQL approach exactly
{'='*20}
"""
    except Exception as e:
        print(f"⚠️ Schema analysis failure (handled): {str(e)}")
        analysis_guidance = ""
    
    final_system_prompt = system_prompt_with_context + analysis_guidance

    # STEP 3: Generate SQL (Non-blocking)
    generated_sql = await run_in_threadpool(
        ai_service.generate_sql,
        final_system_prompt,
        question,
        model
    )
    
    print(f"🔍 DEBUG - Generated SQL: {generated_sql[:200]}...")
    
    # Intercept Knowledge/Security
    if "Knowledge Query" in generated_sql or "SELECT 'Knowledge Query'" in generated_sql:
        human_answer = await run_in_threadpool(ai_service.answer_general_question, question, model)
        return {"answer": human_answer, "follow_ups": []}

    if "ACCESS_DENIED_VIOLATION" in generated_sql:
        return {"answer": "Access Denied: You do not have permission to view this data.", "follow_ups": []}

    # Execute SQL (Non-blocking)
    execution_result = await run_in_threadpool(sql_executor.execute_query, generated_sql)
    
    if "error" in execution_result:
        answer = "I couldn't retrieve that information. The data might not be recorded yet."
        if "doesn't exist" in execution_result.get('error', '').lower():
             answer = "I couldn't find the specific table or data requested."
        return {"answer": answer, "follow_ups": ["Show my courses", "Show my performance"]}
        
    data = execution_result["data"]
    
    # Synthesize Answer (Non-blocking)
    async def run_parallel_tasks():
        task_answer = asyncio.to_thread(ai_service.synthesize_answer, question, generated_sql, data, model)
        task_followups = asyncio.to_thread(ai_service.generate_follow_ups, question, generated_sql, data, None, current_role_id)
        return await asyncio.gather(task_answer, task_followups)

    try:
        human_answer, follow_ups = await run_parallel_tasks()
    except Exception as e:
        human_answer = "Here is the data."
        follow_ups = []

    # Check destructive
    is_destructive = ai_service.is_destructive_query(generated_sql)

    # Update stats
    if str(current_user.id) != "0":
        try:
            current_user.stats_chat_count = (current_user.stats_chat_count or 0) + 1
            if not is_destructive:
                 words = len(human_answer.split())
                 current_user.stats_words_generated = (current_user.stats_words_generated or 0) + words
            db.commit()
        except:
            db.rollback()

    return {
        "answer": human_answer,
        "sql": generated_sql if current_role_id in [1, 2] else None, # Show SQL only to admins
        "data": data[:50] if current_role_id in [1, 2] else None, # Clean output (admins get debug data)
        "follow_ups": follow_ups
    }


@router.get("/tables")
async def get_available_tables(current_user: Users = Depends(get_current_user)):
    """Get list of available tables."""
    tables = sql_executor.get_available_tables()
    return {"tables": tables, "count": len(tables)}

@router.post("/ask", response_model=AIQueryResponse, response_model_exclude_none=True)
async def ask_database(
    request: AIQueryRequest, 
    db: Session = Depends(get_db)
):
    """
    Process natural language question -> SQL -> Answer
    """
    try:
        print(f"\n🚀 [DEBUG] STARTING REQUEST: '{request.question[:50]}...'")
        print(f"   User: {request.user_id}, Role: {request.user_role}")
        
        result = await _process_ai_query(request, db)
        
        print(f"✅ [DEBUG] REQUEST COMPLETED SUCCESSFULLY")
        return result
        
    except Exception as e:
        print(f"🔥 [CRITICAL ERROR] in ask_database: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
