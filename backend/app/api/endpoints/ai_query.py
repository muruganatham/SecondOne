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
from app.api.endpoints.auth import get_current_user
from app.core.db import get_db
from app.models.profile_models import Users

router = APIRouter()

class AIQueryRequest(BaseModel):
    question: str

class AIQueryResponse(BaseModel):
    answer: str
    sql: str
    data: list

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
    
    # 1. Get Schema Context (The Prompt)
    system_prompt = schema_context.get_system_prompt()
    
    # 2. Get SQL from AI
    generated_sql = ai_service.generate_sql(system_prompt, question)
    
    # 3. Execute SQL
    execution_result = sql_executor.execute_query(generated_sql)
    
    if "error" in execution_result:
        return {
            "answer": f"I couldn't run that query. Error: {execution_result['error']}",
            "sql": generated_sql,
            "data": []
        }
        
    data = execution_result["data"]
    
    # 4. Synthesize Human Answer
    human_answer = ai_service.synthesize_answer(question, generated_sql, data)

    # 5. Update User Stats
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
        "data": data
    }
