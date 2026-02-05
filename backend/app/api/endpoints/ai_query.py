"""
AI API Endpoint
Exposes the Text-to-SQL functionality.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.ai_service import ai_service
from app.services.schema_context import schema_context
from app.services.sql_executor import sql_executor
from app.models.profile_models import Users
from app.api.endpoints.auth import get_current_user
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

class AIQueryRequest(BaseModel):
    question: str
    model: str = "deepseek-chat"  # Default to DeepSeek

class AIQueryResponse(BaseModel):
    answer: str
    sql: str
    data: list
    follow_ups: list = []
    requires_confirmation: bool = False
    affected_rows: int = 0

@router.post("/ask", response_model=AIQueryResponse)
async def ask_database(
    request: AIQueryRequest, 
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process natural language question -> SQL -> Answer
    """
    question = request.question
    model = request.model
    
    # 1. Get Schema Context (The Prompt)
    system_prompt = schema_context.get_system_prompt()
    
    # 1.5 Role-Based Search Control (Student Focus)
    from app.models.profile_models import UserAcademics
    
    # Defaults
    role_instruction = ""
    is_access_denied = False
    
    # SUPER ADMIN (1) & ADMIN (2)
    current_role_id = current_user.role
    if current_role_id in [1, 2]:
        role_instruction = get_admin_prompt()

    # STUDENT ROLE (ID: 7)
    elif current_role_id == 7:
        # Fetch Student's Department
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        college_id = academics.college_id if academics else "Unknown"
        
        # Safe access to college short name
        college_short_name = "admin" # default
        if academics and academics.college:
             # explicit string conversion to avoid potential Enum issues if SQLAlchemy maps it weirdly
             # Also handling attribute error just in case
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
    
    # 2. Get SQL from AI
    generated_sql = ai_service.generate_sql(system_prompt_with_context, question, model)
    
    # 2.4 Intercept Knowledge Queries (General Q&A)
    if "Knowledge Query" in generated_sql or "SELECT 'Knowledge Query'" in generated_sql:
        human_answer = ai_service.answer_general_question(question, model)
        return {
            "answer": human_answer,
            "sql": "-- General Knowledge Query (No DB Access)",
            "data": [],
            "follow_ups": [],
            "requires_confirmation": False,
            "affected_rows": 0
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
            "sql": "-- Blocked by Security Protocol",
            "data": [],
            "follow_ups": [],
            "requires_confirmation": False,
            "affected_rows": 0
        }
    
    # 3. Execute SQL
    execution_result = sql_executor.execute_query(generated_sql)
    
    if "error" in execution_result:
        return {
            "answer": f"I couldn't run that query. Error: {execution_result['error']}",
            "sql": generated_sql,
            "data": [],
            "follow_ups": []
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
            ai_service.generate_follow_ups, question, generated_sql, data
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

    # 7. Update User Stats
    try:
        current_user.stats_chat_count = (current_user.stats_chat_count or 0) + 1
        
        # Estimate word count
        words = len(human_answer.split())
        current_user.stats_words_generated = (current_user.stats_words_generated or 0) + words
        
        db.commit()
    except Exception as e:
        print(f"Failed to update stats: {e}")

    return {
        "answer": human_answer,
        "sql": generated_sql,
        "data": data,
        "follow_ups": follow_ups,
        "requires_confirmation": is_destructive,
        "affected_rows": affected_rows
    }
