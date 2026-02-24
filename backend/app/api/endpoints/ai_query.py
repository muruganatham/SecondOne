from datetime import datetime
from typing import Optional, Dict, Any
import uuid
import time
import asyncio
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.services.ai_service import ai_service
from app.services.schema_context import schema_context
from app.models.profile_models import Users, UserAcademics
from app.core.security import get_current_user, RoleChecker
from app.core.db import get_db, SessionLocal
from app.core.logging_config import get_logger
from app.core.rate_limiter import rate_limiter, query_cache
from app.prompts import (
    get_admin_prompt,
    get_student_prompt,
    get_staff_prompt,
    get_college_admin_prompt,
    get_trainer_prompt,
    get_content_creator_prompt,
)

from app.services import sql_executor
from app.services.query_classifier import query_classifier

router = APIRouter()
logger = get_logger("ai_query")

# In-memory Job Store for Async Queries
JOB_STORE: Dict[str, Any] = {}


from app.models.saved_queries import SavedQuery

class AIQueryRequest(BaseModel):
    question: str
    model: str = "deepseek-chat"
    user_id: Optional[int] = None
    user_role: Optional[int] = None


class SaveQueryRequest(BaseModel):
    job_id: str
    name: str
    description: Optional[str] = None
    slug: str


class AIQueryResponse(BaseModel):
    answer: str
    follow_ups: list = []
    job_id: Optional[str] = None
    execution_time_ms: Optional[int] = None
    cached: Optional[bool] = None
    confidence: Optional[float] = None      # 1.0 = first-attempt success, degrades on retries
    data_quality: Optional[str] = None     # "complete" | "partial" | "empty" | "estimated"
    row_count: Optional[int] = None        # number of rows returned
    attempt_count: Optional[int] = None    # how many SQL attempts were needed


# --- CORE LOGIC ---


async def _process_ai_query(request: AIQueryRequest, db: Session) -> dict:
    """
    Core Logic for processing AI queries.
    Refactored for reuse in Sync and Async modes.
    Ensures high-precision role-based prompts (Batch/Section scoping).
    """
    question = request.question
    model = request.model

    # 0. User Context Identification
    current_user = None
    if request.user_id:
        current_user = db.query(Users).filter(Users.id == str(request.user_id)).first()
        if current_user and request.user_role:
            current_user.role = request.user_role

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
    role_instruction = ""
    user_context_str = ""
    current_role_id = int(str(current_user.role or 7))
    
    if current_role_id in [1, 2]: # Admin
        role_instruction = get_admin_prompt(current_user.id)

    elif current_role_id == 7:  # Student
        academics = (
            db.query(UserAcademics)
            .filter(UserAcademics.user_id == current_user.id)
            .first()
        )
        dept_id = academics.department_id if academics else "Unknown"
        college_id = academics.college_id if academics else "Unknown"
        batch_id = academics.batch_id if academics else "Unknown"
        section_id = academics.section_id if academics else "Unknown"

        college_short_name = "admin"
        college_name = "Your Institution"
        dept_name = "Your Department"
        batch_name = "Your Batch"
        section_name = "Your Section"

        if academics:
            user_context_str += f"""
            - College ID: {college_id}
            - Department ID: {dept_id}
            - Batch ID: {batch_id}
            - Section ID: {section_id}
            """
            if academics.college:
                try:
                    college_short_name = str(
                        academics.college.college_short_name
                    ).lower()
                    college_name = str(academics.college.college_name)
                except:
                    pass
            if academics.department:
                try:
                    dept_name = str(academics.department.department_name)
                except:
                    pass
            if academics.batch:
                try:
                    batch_name = str(academics.batch.batch_name)
                except:
                    pass
            if academics.section:
                try:
                    section_name = str(academics.section.section_name)
                except:
                    pass

        role_instruction = get_student_prompt(
            dept_id,
            dept_name,
            college_id,
            college_name,
            college_short_name,
            current_user.id,
            batch_id=batch_id,
            batch_name=batch_name,
            section_id=section_id,
            section_name=section_name,
        )

    elif current_role_id == 4:  # Staff
        academics = (
            db.query(UserAcademics)
            .filter(UserAcademics.user_id == current_user.id)
            .first()
        )
        dept_id = academics.department_id if academics else "Unknown"
        dept_name = "Your Department"
        if academics:
            user_context_str += f"\n- Department ID: {dept_id}"
            if academics.department:
                dept_name = str(academics.department.department_name)
        role_instruction = get_staff_prompt(dept_id, dept_name, current_user.id)

    elif current_role_id == 3:  # College Admin
        academics = (
            db.query(UserAcademics)
            .filter(UserAcademics.user_id == current_user.id)
            .first()
        )
        college_id = academics.college_id if academics else "Unknown"
        college_short_name = "admin"
        college_name = "Your Institution"
        if academics and academics.college:
             try:
                 college_short_name = str(academics.college.college_short_name).lower()
                 college_name = str(academics.college.college_name)
             except: pass
        role_instruction = get_college_admin_prompt(college_id, college_name, college_short_name, current_user.id)

    elif current_role_id == 6:  # Content
        role_instruction = get_content_creator_prompt(current_user.id)

    elif current_role_id == 5:  # Trainer
        academics = (
            db.query(UserAcademics)
            .filter(UserAcademics.user_id == current_user.id)
            .first()
        )
        dept_id = academics.department_id if academics else "Unknown"
        dept_name = "Your Department"
        if academics:
            user_context_str += f"\n- Department ID: {dept_id}"
            if academics.department:
                dept_name = str(academics.department.department_name)
        role_instruction = get_trainer_prompt(dept_id, dept_name, current_user.id)

    else:
        role_instruction = f"Unauthorized role: {current_role_id}. Access Denied."

    # 1.6 Security Interceptor
    if current_role_id not in [1, 2]:
        lower_q = question.lower()
        hard_bans = [
            "database schema",
            "db schema",
            "system structure",
            "show databases",
            "show tables",
        ]
        if any(ban in lower_q for ban in hard_bans):
            return {
                "answer": "Access Denied: You do not have permission to view system architecture details.",
                "follow_ups": [],
            }

        if "table" in lower_q or "database" in lower_q:
            if any(
                trigger in lower_q for trigger in ["list", "show", "what", "structure"]
            ):
                if "time table" not in lower_q and "timetable" not in lower_q:
                    return {
                        "answer": "Access Denied: Direct table queries are restricted.",
                        "follow_ups": [],
                    }

    # STEP 1.5: Query Intent Classification (zero API cost)
    intent = query_classifier.classify(question)
    logger.info(f"🎯 Intent: {intent.intent} (conf={intent.confidence}) | {intent.metadata.get('reason', '')}")

    # Short-circuit: answer general knowledge directly without touching DB
    if query_classifier.should_skip_db(intent):
        follow_ups = ["Show my performance", "List available courses", "Top performers in my batch"]
        return {
            "answer": (
                "That's a general knowledge question — I can answer it without the database.\n\n"
                "Please re-ask me and I'll answer using my AI knowledge directly!"
            ),
            "follow_ups": follow_ups,
            "confidence": 1.0,
            "data_quality": "complete",
            "row_count": 0,
            "attempt_count": 0,
        }

    intent_hint = query_classifier.get_intent_hint_for_prompt(intent)

    # STEP 1.6: Deep Schema Analysis (only for complex queries)
    if query_classifier.should_skip_schema_analysis(intent):
        # Fast path: skip the DeepSeek schema analysis API call
        logger.info(f"⚡ Skipping schema analysis for intent: {intent.intent}")
        table_hint = intent.table_hint or ""
        detailed_schema = schema_context.get_detailed_schema(
            [t for t in schema_context.get_all_table_names() if table_hint in t]
        ) if table_hint else ""
        analysis_summary = f"Intent: {intent.intent} | Table hint: {table_hint}"
    else:
        # Full path: schema analysis via DeepSeek
        all_table_names = schema_context.get_all_table_names()
        analysis_result = await run_in_threadpool(
            ai_service.analyze_question_with_schema,
            question,
            all_table_names,
            model
        )
        recommended_tables = analysis_result.get("recommended_tables", [])
        detailed_schema = schema_context.get_detailed_schema(recommended_tables)
        analysis_summary = (
            f"Query Type: {analysis_result.get('query_type')} | "
            f"Tables: {recommended_tables} | "
            f"Strategy: {analysis_result.get('suggested_sql_approach')}"
        )

    # Construct Final Prompt
    final_system_prompt = f"""{detailed_schema}

{'='*20}
{role_instruction}
{'='*20}

### QUERY ANALYSIS
{analysis_summary}

{intent_hint}

### USER TASK
Generate SQL for: "{question}"
"""
    print('final_system_prompt', final_system_prompt)
    # STEP 2 & 3: Generate and Execute SQL (with Self-Correction Loop)
    max_retries = 3
    generated_sql = ""
    execution_result = {}
    error_message = None
    attempt_count = 0

    for attempt in range(max_retries):
        generated_sql = await run_in_threadpool(
            ai_service.generate_sql, 
            final_system_prompt, 
            question, 
            model,
            None, # result_table
            error_message
        )

        import re
        # Extract only the SQL block
        sql_match = re.search(
            r"SELECT\s+.*?(?:;|$)", generated_sql, re.IGNORECASE | re.DOTALL
        )
        if sql_match:
            generated_sql = sql_match.group(0).strip()

        # Clean markdown
        generated_sql = generated_sql.replace("```sql", "").replace("```", "").strip()

        # STEP 3: Execute SQL
        execution_result = await run_in_threadpool(
            sql_executor.execute_query, generated_sql
        )

        attempt_count += 1

        # If success, break loop
        if "error" not in execution_result:
            logger.info(f"✅ SQL execution succeeded on attempt {attempt + 1}")
            break
        
        # If error, log and prepare for correction
        error_message = execution_result.get("error")
        logger.warning(f"⚠️ SQL Attempt {attempt + 1} failed: {error_message}. Retrying with correction...")

    # Final Failure Handling
    if "error" in execution_result:
        # Debug logging for persistent failures
        with open("debug_ai.log", "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now()}] PERSISTENT FAILURE | QUESTION: {question}\n")
            f.write(f"LAST SQL: {generated_sql}\n")
            f.write(f"LAST ERROR: {error_message}\n")

        debug_data = (
            [{"error": error_message}]
            if current_role_id in [1, 2]
            else None
        )
        debug_sql = generated_sql if current_role_id in [1, 2] else None

        if current_role_id in [1, 2]:
            # Admins get the actual error for debugging
            answer = f"Query failed after {max_retries} attempts. Last error: {error_message}"
        elif "doesn't exist" in (error_message or "").lower():
            answer = "I couldn't find the specific data requested. The information may not be recorded yet."
        else:
            answer = "I couldn't retrieve that information right now. Try rephrasing your question or asking about a specific college or student."

        return {
            "answer": answer,
            "sql": debug_sql,
            "data": debug_data,
            "follow_ups": ["Show my performance"],
            "confidence": 0.0,
            "data_quality": "failed",
            "row_count": 0,
            "attempt_count": attempt_count,
        }

    data = execution_result["data"]
    row_count = len(data) if isinstance(data, list) else 0

    # Compute confidence based on attempts needed
    confidence_map = {1: 1.0, 2: 0.8, 3: 0.6}
    confidence = confidence_map.get(attempt_count, 0.5)

    # Compute data quality
    if row_count == 0:
        data_quality = "empty"
        confidence = round(confidence * 0.8, 2)  # penalise empty result
    elif attempt_count > 1:
        data_quality = "partial"   # succeeded but needed retries
    else:
        data_quality = "complete"

    # STEP 4: Synthesize Answer
    async def run_parallel_tasks():
        task_answer = asyncio.to_thread(
            ai_service.synthesize_answer,
            question,
            generated_sql,
            data,
            model,
            current_role_id,
        )
        task_followups = asyncio.to_thread(
            ai_service.generate_follow_ups,
            question,
            generated_sql,
            data,
            None,
            current_role_id,
        )
        return await asyncio.gather(task_answer, task_followups)

    try:
        human_answer, follow_ups = await run_parallel_tasks()
    except Exception as e:
        human_answer = "Here is the data."
        follow_ups = []

    # 7. Update User Stats
    if str(current_user.id) != "0":
        try:
            current_user.stats_chat_count = (current_user.stats_chat_count or 0) + 1
            words = len(human_answer.split())
            current_user.stats_words_generated = (
                current_user.stats_words_generated or 0
            ) + words
            db.commit()
        except:
            db.rollback()

    # Final Job Storage for persistence (Saved Queries)
    job_id = str(uuid.uuid4())
    JOB_STORE[job_id] = {
        "status": "completed",
        "sql": generated_sql,
        "question": question,
        "data_count": len(data) if isinstance(data, list) else 0,
        "created_at": time.time(),
    }

    return {
        "answer": human_answer,
        "follow_ups": follow_ups,
        "job_id": job_id,
        "confidence": round(confidence, 2),
        "data_quality": data_quality,
        "row_count": row_count,
        "attempt_count": attempt_count,
    }


@router.get("/tables")
async def get_available_tables(current_user: Users = Depends(get_current_user)):
    """Get list of available tables."""
    tables = sql_executor.get_available_tables()
    return {"tables": tables, "count": len(tables)}


@router.post("/ask", response_model=AIQueryResponse, response_model_exclude_none=True)
async def ask_database(request: AIQueryRequest, db: Session = Depends(get_db)):
    """
    Synchronous entry point.
    """
    try:
        return await _process_ai_query(request, db)
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")



@router.post("/ask/async")
async def ask_database_async(
    request: AIQueryRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Asynchronous entry point. Returns a job ID immediately.
    """
    job_id = str(uuid.uuid4())
    JOB_STORE[job_id] = {"status": "processing", "created_at": time.time()}

    async def task_wrapper():
        try:
            result = await _process_ai_query(request, db)
            JOB_STORE[job_id] = {
                "status": "completed",
                "result": result,
                "updated_at": time.time(),
            }
        except Exception as e:
            JOB_STORE[job_id] = {
                "status": "failed",
                "error": str(e),
                "updated_at": time.time(),
            }

    background_tasks.add_task(task_wrapper)
    return {"job_id": job_id, "status": "processing"}


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Check status of an async job."""
    if job_id not in JOB_STORE:
        raise HTTPException(status_code=404, detail="Job not found")
    return JOB_STORE[job_id]


@router.post("/save-query")
async def save_verified_query(
    request: SaveQueryRequest,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    """Save a successful query from the Job Store to the permanent database."""
    if request.job_id not in JOB_STORE:
        raise HTTPException(
            status_code=404, detail="Original query job not found or expired"
        )

    job_data = JOB_STORE[request.job_id]

    # Create saved query entry
    new_saved = SavedQuery(
        name=request.name,
        slug=request.slug,
        description=request.description,
        sql_query=job_data["sql"],
        creator_id=current_user.id,
    )

    try:
        db.add(new_saved)
        db.commit()
        db.refresh(new_saved)
        return {
            "status": "success",
            "slug": new_saved.slug,
            "message": "Query saved as API endpoint",
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to save query: {str(e)}")


@router.get("/query/{slug}")
async def execute_saved_query(
    slug: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user),
):
    """Execute a previously saved query by its slug."""
    saved = db.query(SavedQuery).filter(SavedQuery.slug == slug).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved query not found")

    # Execute the saved SQL
    execution_result = await run_in_threadpool(
        sql_executor.execute_query, saved.sql_query
    )

    if "error" in execution_result:
        raise HTTPException(
            status_code=500, detail=f"Execution error: {execution_result['error']}"
        )

    return {
        "name": saved.name,
        "data": execution_result["data"],
        "count": len(execution_result["data"]),
    }
