"""
AI API Endpoint
Exposes the Text-to-SQL functionality.
Role-based access control enabled.
"""
from datetime import datetime
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
    
    current_user = None
    
    if request.user_id:
        current_user = db.query(Users).filter(Users.id == str(request.user_id)).first()
        if current_user and request.user_role:
            current_user.role = request.user_role
            
    # Fallback/Mock if user doesn't exist or isn't provided    if not current_user:
        current_user = Users(
            id=str(request.user_id or "0"),
            email="static-frontend@app.local",
            name="Static Frontend App",
            role=request.user_role if request.user_role is not None else 0, # Default to 0 (No Role)
        )
    
    # 1. Get Schema Context (The Prompt)
    system_prompt = schema_context.get_system_prompt()
    
    # 1.5 Role-Based Search Control
    from app.models.profile_models import UserAcademics
    
    # Defaults
    role_instruction = ""
    current_role_id = request.user_role if request.user_role is not None else current_user.role
    
    # SUPER ADMIN (1) & ADMIN (2)
    if current_role_id in [1, 2]:
        role_instruction = get_admin_prompt(current_user.id)
    
    # STUDENT ROLE (ID: 7)
    elif current_role_id == 7:
        # Fetch Student's Department, College, Batch, and Section Details
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        college_id = academics.college_id if academics else "Unknown"
        batch_id = academics.batch_id if academics else "Unknown"
        section_id = academics.section_id if academics else "Unknown"
        
        # Safe access to Names and Short Names
        college_short_name = "admin" 
        college_name = "Your Institution"
        dept_name = "Your Department"
        batch_name = "Your Batch"
        section_name = "Your Section"
        
        if academics:
            if academics.college:
                try:
                    college_short_name = str(academics.college.college_short_name).lower()
                    college_name = str(academics.college.college_name)
                except: pass
            if academics.department:
                try:
                    dept_name = str(academics.department.department_name)
                except: pass
            if academics.batch:
                try:
                    batch_name = str(academics.batch.batch_name)
                except: pass
            if academics.section:
                try:
                    section_name = str(academics.section.section_name)
                except: pass

        role_instruction = get_student_prompt(
            dept_id, dept_name, college_id, college_name, college_short_name, current_user.id,
            batch_id=batch_id, batch_name=batch_name, section_id=section_id, section_name=section_name
        )

    # STAFF / FACULTY ROLE (ID: 4)
    elif current_role_id == 4:
        # Fetch Staff's Department
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        dept_name = "Your Department"
        if academics and academics.department:
            dept_name = str(academics.department.department_name)
        role_instruction = get_staff_prompt(dept_id, dept_name, current_user.id)

    # COLLEGE ADMIN ROLE (ID: 3)
    elif current_role_id == 3:
        # Fetch Admin's College
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        college_id = academics.college_id if academics else "Unknown"
        
        # Safe access to college names and IDs
        college_short_name = "admin" # default
        college_name = "Your Institution" # default
        if academics and academics.college:
             try:
                 college_short_name = str(academics.college.college_short_name).lower()
                 college_name = str(academics.college.college_name)
             except: pass

        role_instruction = get_college_admin_prompt(college_id, college_name, college_short_name, current_user.id)

    # CONTENT ROLE (ID: 6)
    elif current_role_id == 6:
        role_instruction = get_content_creator_prompt(current_user.id)

    # TRAINER ROLE (ID: 5)
    elif current_role_id == 5:
        # Fetch Trainer's Department
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        dept_name = "Your Department"
        if academics and academics.department:
            dept_name = str(academics.department.department_name)
        role_instruction = get_trainer_prompt(dept_id, dept_name, current_user.id)
    
    # DEFAULT / UNAUTHORIZED (e.g. Role 0)
    else:
        role_instruction = "[SECURITY VIOLATION] Unauthorized role: {current_role_id}. Access Denied."
    
    # --- SECURITY INTERCEPTOR (CRITICAL) ---
    if current_role_id not in [1, 2]:
        lower_q = question.lower()
        hard_bans = ["database schema", "db schema", "system structure", "backend config", "metadata", "show databases", "show tables", "list tables"]
        if any(ban in lower_q for ban in hard_bans):
            return {"answer": "Access Denied: You do not have permission to view system architecture details.", "follow_ups": []}
            
        if "table" in lower_q or "database" in lower_q:
             trigger_words = ["list", "available", "all", "what", "show", "structure"]
             if any(trigger in lower_q for trigger in trigger_words):
                 if "time table" not in lower_q and "timetable" not in lower_q:
                     return {"answer": "Access Denied: Direct table queries are restricted.", "follow_ups": []}

    # Construct and Execute
    final_system_prompt = f"{system_prompt}\n\n{'='*20}{role_instruction}\n{'='*20}\n\nTask: Generate SQL for: \"{question}\""
    generated_sql = ai_service.generate_sql(final_system_prompt, question, model)
    
    # 2.4 Intercept Knowledge Queries
    if "Knowledge Query" in generated_sql or "SELECT 'Knowledge Query'" in generated_sql:
        human_answer = ai_service.answer_general_question(question, model)
        return {"answer": human_answer, "sql": None, "data": [], "follow_ups": []}

    # 2.5 Intercept Access Denied
    if "ACCESS_DENIED_VIOLATION" in generated_sql:
        return {"answer": "Access Denied: Restricted data boundary.", "sql": None, "data": [], "follow_ups": []}

    # 3. Execute SQL
    execution_result = sql_executor.execute_query(generated_sql)
    
    if "error" in execution_result:
        answer = "I couldn't retrieve that information from the database. It might be missing or structured differently."
        return {"answer": answer, "sql": None, "data": None, "follow_ups": ["Check courses", "Show student rank"]}
        
    data = execution_result["data"]
    
    # 4 & 5. Parallelize Synthesize Answer and Follow-up Generation
    import asyncio
    async def run_parallel_tasks():
        task_answer = asyncio.to_thread(ai_service.synthesize_answer, question, generated_sql, data, model)
        task_followups = asyncio.to_thread(ai_service.generate_follow_ups, question, generated_sql, data, None, current_role_id)
        return await asyncio.gather(task_answer, task_followups)

    try:
        human_answer, follow_ups = await run_parallel_tasks()
    except Exception as e:
        print(f"Parallel Execution Error: {e}")
        human_answer = "Here is the data."
        follow_ups = []

    # 7. Update User Stats
    if str(current_user.id) != "0":
        try:
            current_user.stats_chat_count = (current_user.stats_chat_count or 0) + 1
            words = len(human_answer.split())
            current_user.stats_words_generated = (current_user.stats_words_generated or 0) + words
            db.commit()
        except: db.rollback()

    return {
        "answer": human_answer,
        "sql": None,
        "data": None,
        "follow_ups": follow_ups
    }
