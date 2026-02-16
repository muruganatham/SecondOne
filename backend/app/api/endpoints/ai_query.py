"""
AI API Endpoint
Exposes the Text-to-SQL functionality.
Role-based access control enabled.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.ai_service import ai_service
from app.services.schema_context import schema_context
from app.services.sql_executor import sql_executor
from app.models.profile_models import Users
from app.core.security import get_current_user, RoleChecker
from app.core.db import get_db
from app.prompts import (
    get_admin_prompt, 
    get_student_prompt, 
    get_staff_prompt, 
    get_college_admin_prompt, 
    get_trainer_prompt, 
    get_content_creator_prompt
)

router = APIRouter()

# Example: Protect specific endpoints with RoleChecker
# router = APIRouter(dependencies=[Depends(RoleChecker([1, 2]))]) # This would protect the whole router

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

@router.get("/tables")
async def get_available_tables(current_user: Users = Depends(get_current_user)):
    """
    Get list of available tables in the database.
    Useful for debugging and understanding what data is available.
    """
    tables = sql_executor.get_available_tables()
    return {
        "tables": tables,
        "count": len(tables),
        "message": f"Found {len(tables)} tables in the database"
    }

@router.post("/ask", response_model=AIQueryResponse, response_model_exclude_none=True)
async def ask_database(
    request: AIQueryRequest, 
    db: Session = Depends(get_db)
):
    """
    Process natural language question -> SQL -> Answer
    AUTHENTICATION BYPASS: Uses user_id and user_role from payload.
    """
    question = request.question
    model = request.model
    
    # 0. Identifying the user context from payload (Frontend-only mode)
    # We trust the frontend to provide valid user_id and user_role
    current_user = None
    
    if request.user_id:
        current_user = db.query(Users).filter(Users.id == str(request.user_id)).first()
        if current_user and request.user_role:
            current_user.role = request.user_role
            
    # Fallback/Mock if user doesn't exist or isn't provided
    if not current_user:
        current_user = Users(
            id=str(request.user_id or "0"),
            email="static-frontend@app.local",
            name="Static Frontend App",
            role=request.user_role or 1, # Default to Admin if none provided
        )
    
    # 1. Get Schema Context (The Prompt)
    system_prompt = schema_context.get_system_prompt()
    
    # 1.5 Role-Based Search Control
    from app.models.profile_models import UserAcademics
    
    # Defaults
    role_instruction = ""
    
    # SUPER ADMIN (1) & ADMIN (2)
    current_role_id = current_user.role
    if current_role_id in [1, 2]:
        role_instruction = get_admin_prompt(current_user.id)
    
    # STUDENT ROLE (ID: 7)
    elif current_role_id == 7:
        # Fetch Student's Department
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        college_id = academics.college_id if academics else "Unknown"
        
        # Safe access to college short name
        college_short_name = "admin" # default
        if academics and academics.college:
             try:
                 college_short_name = str(academics.college.college_short_name).lower()
             except:
                 college_short_name = "admin"

        role_instruction = get_student_prompt(dept_id, college_id, college_short_name, current_user.id)

    # STAFF / FACULTY ROLE (ID: 4)
    elif current_user.role == 4:
        # Fetch Staff's Department
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        role_instruction = get_staff_prompt(dept_id, current_user.id)

    # COLLEGE ADMIN ROLE (ID: 3)
    elif current_user.role == 3:
        # Fetch Admin's College
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        college_id = academics.college_id if academics else "Unknown"
        role_instruction = get_college_admin_prompt(college_id, current_user.id)

    # CONTENT ROLE (ID: 6)
    elif current_user.role == 6:
        role_instruction = get_content_creator_prompt(current_user.id)

    # TRAINER ROLE (ID: 5)
    elif current_user.role == 5:
        # Fetch Trainer's Department
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        role_instruction = get_trainer_prompt(dept_id, current_user.id)
    
    # Construct the Prompt
    system_prompt_with_context = f"{system_prompt}\n\n{'='*20}{role_instruction}\n{'='*20}\n\nTask: Generate SQL for: \"{question}\""
    
    # 1.8 DEEP SCHEMA ANALYSIS: Analyze question with FULL schema context
    # This is INFORMATIONAL ONLY - we use it to log insights but don't block SQL generation
    # WE NOW PASS system_prompt_with_context SO THE ANALYST SEES THE ROLE RESTRICTIONS
    analysis = ai_service.analyze_question_with_schema(
        user_question=question,
        schema_context=system_prompt_with_context,  # Includes Schema + Role Rules
        model=model
    )
    
    print(f"📊 Question Analysis (Informational):")
    print(f"   - Can Answer: {analysis.get('can_answer', True)}")
    print(f"   - Query Type: {analysis.get('query_type', 'unknown')}")
    print(f"   - Recommended Tables: {analysis.get('recommended_tables', [])}")
    print(f"   - Confidence: {analysis.get('confidence', 'unknown')}")
    print(f"   - SQL Approach: {analysis.get('suggested_sql_approach', 'N/A')[:80]}...")
    
    # NOTE: We don't block based on analysis - let the AI attempt to generate SQL
    # The analysis provides insights but we trust the SQL generation phase
    
    # 1.9 INTEGRATE ANALYSIS INTO GENERATION PROMPT (CRITICAL FIX)
    # We now explicitly force the SQL generator to use the analysis results
    # Safe extraction of tables
    rec_tables = analysis.get('recommended_tables', [])
    if isinstance(rec_tables, list):
        rec_tables_str = ", ".join(rec_tables)
    else:
        rec_tables_str = str(rec_tables)

    analysis_guidance = f"""
    \n{'='*20}
    [PRE-COMPUTED SCHEMA ANALYSIS]
    Use the following expert analysis to guide your SQL generation:
    1. **Recommended Tables**: {rec_tables_str}
    2. **Strategy**: {analysis.get('suggested_sql_approach', 'Standard SQL')}
    3. **Reasoning**: {analysis.get('reasoning', 'Follow standard protocols')}
    
    IMPORTANT: If the analysis suggests specific tables (especially college-specific ones), YOU MUST USE THEM.
    {'='*20}
    """
    
    final_system_prompt = f"{system_prompt_with_context}\n{analysis_guidance}"

    # 2. Get SQL from AI (with schema analysis insights)
    generated_sql = ai_service.generate_sql(final_system_prompt, question, model)
    
    # 2.4 Intercept Knowledge Queries (General Q&A)
    if "Knowledge Query" in generated_sql or "SELECT 'Knowledge Query'" in generated_sql:
        human_answer = ai_service.answer_general_question(question, model)
        return {
            "answer": human_answer,
            #"sql": "-- General Knowledge Query (No DB Access)", # HIDDEN
            #"data": [], # HIDDEN
            "follow_ups": []
        }

    # 2.5 Intercept Access Denied
    if "ACCESS_DENIED_VIOLATION" in generated_sql:
        denial_reason = "Access Denied: You do not have permission to view this data."
        if current_user.role == 7:
            denial_reason = "Access Denied: You are restricted to your own data and Departmental Analytics."
        elif current_user.role == 4:
            denial_reason = "Access Denied: You are restricted to data within your Department."
        elif current_user.role == 3:
            denial_reason = "Access Denied: You are restricted to data within your College."
        elif current_user.role == 6:
            denial_reason = "Access Denied: You are restricted to Content and Assets only."
        elif current_user.role == 5:
            denial_reason = "Access Denied: You are restricted to Student Performance data within your Department."
        return {
            "answer": denial_reason,
            #"sql": "-- Blocked by Security Protocol", # HIDDEN
            #"data": [], # HIDDEN
            "follow_ups": []
        }

    # 3. Execute SQL
    execution_result = sql_executor.execute_query(generated_sql)
    
    if "error" in execution_result:
        # Production-ready error message
        # We don't burden the user with debug details unless it's a critical system error
        # The AI should have used available tables. If this fails, it's a data availability issue.
        
        answer = "I couldn't retrieve that information from the database. This might be because the specific data hasn't been recorded yet or is structured differently."
        
        # Optional: Add specific note if table is missing
        if "doesn't exist" in execution_result.get('error', '').lower():
             answer = "I couldn't find the specific table or data you requested in the current database. I tried looking for relevant information but couldn't locate it."

        return {
            "answer": answer,
            #"sql": generated_sql, # Keep SQL for transparency/admins # HIDDEN
            #"data": [], # HIDDEN
            "follow_ups": ["List available tables", "Show courses", "Show student performance"]
        }
        
    data = execution_result["data"]
    
    # 4 & 5. Parallelize Synthesize Answer and Follow-up Generation (Optimized Latency)
    import asyncio
    
    async def run_parallel_tasks():
        # Task A: Generate Human Answer
        task_answer = asyncio.to_thread(
            ai_service.synthesize_answer, question, generated_sql, data, model
        )
        
        # Task B: Generate Follow-ups (Now independent of answer)
        task_followups = asyncio.to_thread(
            ai_service.generate_follow_ups, question, generated_sql, data, None, current_role_id
        )
        
        return await asyncio.gather(task_answer, task_followups)

    try:
        human_answer, follow_ups = await run_parallel_tasks()
    except Exception as e:
        print(f"Parallel Execution Error: {e}")
        # Fallback to serial or basic
        human_answer = "Here is the data."
        follow_ups = []

    # 6. Check if query is destructive
    is_destructive = ai_service.is_destructive_query(generated_sql)
    affected_rows = len(data) if is_destructive else 0

    # 7. Update User Stats (Skip for mock/static user ID "0")
    if str(current_user.id) != "0":
        try:
            current_user.stats_chat_count = (current_user.stats_chat_count or 0) + 1
            
            # Estimate word count
            words = len(human_answer.split())
            current_user.stats_words_generated = (current_user.stats_words_generated or 0) + words
            
            db.commit()
        except Exception as e:
            print(f"Failed to update stats: {e}")
            db.rollback()

    return {
        "answer": human_answer,
        #"sql": generated_sql, # HIDDEN
        #"data": data, # HIDDEN
        "follow_ups": follow_ups
    }
