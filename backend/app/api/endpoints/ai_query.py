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
        role_instruction = """
        \n\n[SECURITY PROTOCOL: SUPER ADMIN / ADMIN LEVEL]
        USER CONTEXT: System Administrator with UNRESTRICTED ACCESS.
        
        PERMISSIONS:
        1. ALLOWED: **GLOBAL VIEW**.
           - Can access ALL tables, ALL users, and ALL data across Colleges.
           - Example: "Show overall user data", "List all staff in the system".
           
        RESTRICTIONS:
        - NONE.
        """

    # STUDENT ROLE (ID: 7)
    elif current_role_id == 7:
        # Fetch Student's Department
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"
        
        role_instruction = f"""
        \n\n[SECURITY PROTOCOL: STUDENT LEVEL]
        USER CONTEXT: Student in Department '{dept_id}'.
        
        PERMISSIONS:
        1. ALLOWED: **Personal Data** ("Me", "My", "I").
           - Example: "My marks", "My attendance", "My skills", "Tell me about myself".
           - Interpretation: Treat "Skills" as "Coding Results", "Badges", or "Marks".
           - Note: Tables like `admin_coding_result` ARE ALLOWED if filtered by `user_id`.
           - SQL Rule: MUST include "WHERE user_id = '{current_user.id}'" (or "WHERE id = '{current_user.id}'" for `users` table).
        2. ALLOWED: **Department & Class Analytics** (Aggregates Only) for '{dept_id}'.
           - You MAY calculate metrics for specific Classes, Years, Semesters, or Batches WITHIN '{dept_id}'.
           - SQL Rule: MUST include "WHERE department_id = '{dept_id}'".
        3. ALLOWED: **General Conversation & Knowledge** (Non-Data).
           - Example: "Hi", "Hello", "How does this work?", "What skills do I need for project X?", "Explain Python".
           - SQL Rule: Generate "SELECT 'Knowledge Query'".
           
        RESTRICTIONS (STRICT):
        1. FORBIDDEN: Do NOT retrieve details of **individual students** OTHER THAN YOURSELF.
           - Violation: "Who is the topper?", "Marks of John", "List data of Student X".
        2. FORBIDDEN: Do NOT access **Staff, Faculty, HOD, or Admin** data.
           - Violation: "How many staff?", "HOD name?".
        3. FORBIDDEN: Do NOT access **Global/Overall User Counts**.
           - Violation: "Total users count", "How many students in the system?".
           - You MUST NOT implicitly scope "Total Users" to Department. If user asks "Total Users", DENY IT.
        4. FORBIDDEN: Do NOT access other Departments.

        ENFORCEMENT:
        If the user asks a Forbidden question, DO NOT generate SQL. 
        Instead, output EXACTLY the single string: "ACCESS_DENIED_VIOLATION"
        """

    # STAFF / FACULTY ROLE (ID: 4)
    elif current_user.role == 4:
        # Fetch Staff's Department
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"

        role_instruction = f"""
        \n\n[SECURITY PROTOCOL: STAFF/FACULTY LEVEL]
        USER CONTEXT: Faculty Member in Department '{dept_id}'.
        
        PERMISSIONS:
        1. ALLOWED: **Student Data** (Within Department '{dept_id}' ONLY).
           - Can view individual student marks, attendance, and details.
           - SQL Rule: MUST include "WHERE department_id = '{dept_id}'" (for tables with dept_id) OR join through users.
        2. ALLOWED: **Department Analytics**.
           - Performance of classes, subjects, pass rates WITHIN '{dept_id}'.
        3. ALLOWED: **Personal Data**.
           - "My class stats", "My profile".
        4. ALLOWED: **General Conversation**.
           - SQL Rule: Generate "SELECT 'Knowledge Query'".

        RESTRICTIONS (STRICT):
        1. FORBIDDEN: Do NOT access data of **Other Departments**.
           - Violation: "Show me CSE students" (if user is ECE).
        2. FORBIDDEN: Do NOT access **Other Staff/Admin** personal details.
           - Violation: "Salary of Staff X", "Admin passwords".
        3. FORBIDDEN: Do NOT access **Global/Overall User Counts**.
           - Violation: "Total users count". If user asks "Total Users", DENY IT.
        
        ENFORCEMENT:
        Scope ALL queries to College ID '{dept_id}'.
        """

    # COLLEGE ADMIN ROLE (ID: 3)
    elif current_user.role == 3:
        # Fetch Admin's College
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        college_id = academics.college_id if academics else "Unknown"
        
        role_instruction = f"""
        \n\n[SECURITY PROTOCOL: COLLEGE ADMIN LEVEL]
        USER CONTEXT: YOU ARE THE ADMINISTRATOR FOR COLLEGE ID '{college_id}'.
        
        PRIMARY DIRECTIVE:
        You have jurisdiction OVER AND ONLY OVER data related to College ID '{college_id}'.
        Every single SQL query (except purely personal or knowledge queries) MUST strictly filter by `college_id = '{college_id}'`.
        
        PERMISSIONS & IMPLEMENTATION RULES:
        
        1. **MANAGING PEOPLE (Staff, Trainers, Students)**
           - ALLOWED: View details of users properly associated with College '{college_id}'.
           - STRATEGY: To verify a user belongs to your college, you MUST JOIN `user_academics`.
           - SQL PATTERN: 
             `SELECT ... FROM users u JOIN user_academics ua ON u.id = ua.user_id WHERE ua.college_id = '{college_id}'`
        
        2. **ACADEMIC ASSETS (Courses, Question Banks)**
           - ALLOWED: View content explicitly mapped to your college.
           - STRATEGY: Use `course_academic_maps` as the gatekeeper.
           - SQL PATTERN:
             `SELECT ... FROM courses c JOIN course_academic_maps cam ON c.id = cam.course_id WHERE cam.college_id = '{college_id}'`
        
        3. **ANALYTICS & REPORTS**
           - ALLOWED: Aggregates (pass rates, attendance) solely for YOUR college.
           - RESTRICTION: Do not generate global system stats.
           - SQL RULE: Any `COUNT`, `AVG`, `SUM` must have `WHERE college_id = '{college_id}'` (or equivalent JOIN).
           
        4. **PERSONAL DATA**
           - ALLOWED: "Me", "My Profile".
           - SQL: `SELECT * FROM users WHERE id = '{current_user.id}'`

        NON-NEGOTIABLE RESTRICTIONS:
        
        1. **NO GLOBAL VIEW**: You can NEVER answer "How many students are in the system?" or "List all users".
           - REACTION: If asked for global data without "in my college", IMPLICITLY APPLY the filter `WHERE college_id = '{college_id}'`.
           - IF IMPLICIT FILTERING FAILS (e.g. "Show me data for College ID 999"): DENY ACCESS.
           
        2. **NO COLLEGE LISTINGS**: You are forbidden from listing other colleges.
           - VIOLATION: "What other colleges are there?", "List all colleges", "Who else uses Amypo?".
           - REACTION: You must strictly return ONLY your own college details.
           - FORBIDDEN SQL: `SELECT * FROM colleges`, `SELECT name FROM colleges`.
           - ALLOWED SQL: `SELECT * FROM colleges WHERE id = '{college_id}'`.

        3. **NO CROSS-COLLEGE ACCESS**: You cannot see data for other colleges. 
           - TRIGGER: If `college_id` in request != '{college_id}', return "ACCESS_DENIED_VIOLATION".

        4. **NO SYSTEM CONFIG ACCESS**: Super Admin tables are off-limits.
        
        FINAL INSTRUCTION:
        Your generated SQL must act as a logical firewall. If a query does not contain logic to isolate College '{college_id}', it is MALFORMED and INVALID.
        """

    # CONTENT ROLE (ID: 6)
    elif current_user.role == 6:
        role_instruction = f"""
        \n\n[SECURITY PROTOCOL: CONTENT CREATOR LEVEL]
        USER CONTEXT: Content Team Member.
        
        PERMISSIONS:
        1. ALLOWED: **Content & Assets**.
           - Can view Question Banks (`academic_qb_...`), Courses, Study Materials, Assets.
           - Example: "Show me active MCQs", "List all Java courses".
        2. ALLOWED: **General Conversation**.
           - SQL Rule: Generate "SELECT 'Knowledge Query'".
        3. ALLOWED: **Personal Data** ("Me", "My").
           - "Tell me about myself", "My details".
           - SQL Rule: "SELECT * FROM users WHERE id = '{current_user.id}'".
           
        RESTRICTIONS:
        1. FORBIDDEN: Do NOT access **Student Data** (Marks, Attendance, Personal Info).
           - Violation: "Show me user marks", "Student details".
        2. FORBIDDEN: Do NOT access **Other Staff/User Data** (Exception: SELF is ALWAYS allowed).
        3. FORBIDDEN: Do NOT access **Global/Overall User Counts**.
        
        ENFORCEMENT:
        If request seeks Student/User PII, output: "ACCESS_DENIED_VIOLATION"
        """

    # TRAINER ROLE (ID: 5)
    elif current_user.role == 5:
        # Fetch Trainer's Department
        academics = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        dept_id = academics.department_id if academics else "Unknown"

        role_instruction = f"""
        \n\n[SECURITY PROTOCOL: TRAINER LEVEL]
        USER CONTEXT: Technical Trainer in Department '{dept_id}'.
        
        PERMISSIONS:
        1. ALLOWED: **Student & Staff Details**.
           - Can view basic inputs (Name, Email) and Performance of Students AND Staff within '{dept_id}'.
        2. ALLOWED: **Educational Content**.
           - Question Banks, Courses, Modules, Assessments, Assets.
           - Schema Hint: To filter Courses by Trainer, JOIN `course_staff_trainer_allocations` -> `course_academic_maps` (on `allocation_id`) -> `courses`.
        3. ALLOWED: **Colleges & Work History**.
           - Can view list of Colleges, Departments, Batches.
           - "Colleges I worked at": JOIN `course_staff_trainer_allocations` (user_id) -> `course_academic_maps` (allocation_id) -> `colleges` (college_id).
        4. ALLOWED: **Personal Data** ("Me", "My").
           - "Tell me about myself".
           - SQL Rule: "SELECT * FROM users WHERE id = '{current_user.id}'".
        5. ALLOWED: **Feedback**.
           - "My feedback", "What students say about me".
           - SQL Rule: Query `staff_trainer_feedback` WHERE `staff_trainer_id` = '{current_user.id}'.
        6. ALLOWED: **General Conversation**.
           - SQL Rule: Generate "SELECT 'Knowledge Query'".

        RESTRICTIONS:
        1. FORBIDDEN: Do NOT access **Other Departments' Student/Staff data** (except for cross-college work history).
        2. FORBIDDEN: Do NOT access **Salary/Admin/Super Admin** sensitive info.
        3. FORBIDDEN: Do NOT access **Global/Overall User Counts**.
           - Violation: "Total users count". If user asks "Total Users", DENY IT.
        
        ENFORCEMENT:
        Scope User/Performance queries to Department '{dept_id}' unless requesting College/Work History or Feedback.
        """
    
    # Construct the Prompt
    system_prompt_with_context = f"{system_prompt}\n\n{'='*20}{role_instruction}\n{'='*20}\n\nTask: Generate SQL for: \"{question}\""
    
    # 2. Get SQL from AI
    generated_sql = ai_service.generate_sql(system_prompt_with_context, question, model)
    
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
