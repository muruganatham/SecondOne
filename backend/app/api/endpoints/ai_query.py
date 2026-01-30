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
    
    # Add current user context to the prompt
    user_context = f"\n\nIMPORTANT: The current logged-in user has ID = {current_user.id}. When the user asks about 'me', 'my', 'I', or 'current user', use this ID in WHERE clauses like: WHERE user_id = {current_user.id} or WHERE u.id = {current_user.id}"
    system_prompt_with_context = system_prompt + user_context
    
    # 2. Get SQL from AI
    generated_sql = ai_service.generate_sql(system_prompt_with_context, question, model)
    
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
    
    # 4. Synthesize Human Answer
    human_answer = ai_service.synthesize_answer(question, generated_sql, data, model)

    # 5. Generate Follow-up Questions
    follow_ups = ai_service.generate_follow_ups(question, human_answer, generated_sql)

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
