"""
Verify AI Agent
Tests the text-to-sql pipeline.
"""
import os
import sys
from app.services.schema_context import schema_context
from app.services.ai_service import ai_service
from app.services.sql_executor import sql_executor

print("="*60)
print("🤖 VERIFYING DEEPSEEK AI AGENT")
print("="*60)

# 1. Verify Schema Context
print("\n[1] Checking Schema Context...")
context = schema_context.get_system_prompt()
if "2025_submission_tracks" in context and "Student" in context:
    print(f"✅ Schema Context Loaded ({len(context)} chars)")
    print("   (Includes Verified Enums: 'Student' found)")
else:
    print("❌ Schema Context Missing or Incomplete")

# 2. Check API Key
print("\n[2] Checking API Key...")
if ai_service.api_key:
    print("✅ DeepSeek API Key Detected")
    
    # 3. Dry Run Test (End-to-End)
    question = "How many students are there?"
    print(f"\n[3] Testing Question: '{question}'")
    
    try:
        # A. Prompt
        print("   -> Generating SQL...")
        sql = ai_service.generate_sql(context, question)
        print(f"   Generated SQL: {sql}")
        
        # B. Execute
        if "SELECT" in sql.upper():
            print("   -> Executing SQL...")
            result = sql_executor.execute_query(sql)
            
            if "error" in result:
                 print(f"❌ Execution Error: {result['error']}")
            else:
                 print(f"✅ Execution Success: {result['count']} rows found")
                 print(f"   Data: {result['data']}")
                 
                 # C. Human Answer
                 print("   -> Synthesizing Answer...")
                 human = ai_service.synthesize_answer(question, sql, result['data'])
                 print(f"🗣️  AI Answer: {human}")
        else:
            print("⚠️  AI didn't return a valid SELECT query (might normally happen if API quota is low or prompt needs tweaking).")
            
    except Exception as e:
        print(f"❌ Error during test: {e}")

else:
    print("⚠️  DeepSeek API Key NOT FOUND.")
    print("    Please set DEEPSEEK_API_KEY in .env or config if you want to run the real test.")

print("\nDONE.")
