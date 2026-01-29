"""
AI API Endpoint
Exposes the Text-to-SQL functionality.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ai_service
from app.services.schema_context import schema_context
from app.services.sql_executor import sql_executor

router = APIRouter()

class AIQueryRequest(BaseModel):
    question: str

class AIQueryResponse(BaseModel):
    answer: str
    sql: str
    data: list

@router.post("/ask", response_model=AIQueryResponse)
async def ask_database(request: AIQueryRequest):
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
    # We pass the question and the data back to the AI for a summary
    human_answer = ai_service.synthesize_answer(question, generated_sql, data)

    return {
        "answer": human_answer,
        "sql": generated_sql,
        "data": data
    }
