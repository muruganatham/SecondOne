import asyncio
import json
import time
import uuid
import logging
from app.services.ai_service import AIService
from app.core.db import SessionLocal
from app.api.endpoints.ai_query import JOB_STORE

# Custom run_in_threadpool helper to avoid starlette dependency in test
async def run_in_threadpool(func, *args, **kwargs):
    return await asyncio.to_thread(func, *args, **kwargs)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verify")

async def verify():
    print("🚀 Starting Mako Upgrade Verification...")
    
    ai_service = AIService()
    
    # 1. Test Self-Correction Prompt Injection
    print("\n📝 Testing Self-Correction Prompt Logic...")
    system_prompt = "You are a professional SQL analyst."
    question = "List top performers in skcet"
    error = "1055 (42000): Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'u.name'..."
    
    # Generate SQL with error message
    corrected_sql = await run_in_threadpool(
        ai_service.generate_sql, 
        system_prompt, 
        question, 
        "deepseek-chat",
        None,
        error
    )
    
    print(f"\n✅ AI Response with Error Feedback:\n{corrected_sql[:200]}...")
    
    if "SELECT" in corrected_sql.upper():
        print("✅ Self-correction loop successfully generated SQL.")
    else:
        print("❌ Self-correction failed to generate selective SQL.")

    # 2. Verify Semantic Schema Hints
    print("\n🧠 Verifying Semantic Schema Hints...")
    from app.services.schema_context import schema_context
    hints = schema_context.get_all_table_names()
    
    if "institutional ranks" in hints and "university-level" in hints:
        print("✅ Semantic hints are enriched and active.")
    else:
        print("❌ Semantic hints are missing or not updated.")

    print("\n✨ Mako Upgrade Verification Complete!")

if __name__ == "__main__":
    asyncio.run(verify())
