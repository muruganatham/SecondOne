"""
DeepSeek AI Service
Handles communication with the DeepSeek API (OpenAI-compatible).
"""
import os
from openai import OpenAI
from app.core.config import settings
from typing import Optional

class AIService:
    def __init__(self):
        # Use DeepSeek base URL
        self.api_key = settings.DEEPSEEK_API_KEY or settings.GROQ_API_KEY
        self.base_url = "https://api.deepseek.com"
        
        # Fallback to env var if not in settings yet
        if not self.api_key:
             self.api_key = os.getenv("DEEPSEEK_API_KEY")

        if not self.api_key:
            print("⚠️ WARNING: DEEPSEEK_API_KEY is not set. AI features will be disabled.")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        
    def generate_sql(self, system_prompt: str, user_question: str) -> str:
        """
        Generates SQL from natural language using DeepSeek-Coder-V2
        """
        if not self.client:
            return "Error: DeepSeek API Key is missing. Please configure DEEPSEEK_API_KEY."

        try:
            response = self.client.chat.completions.create(
                model="deepseek-coder",  # or deepseek-chat
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question},
                ],
                max_tokens=1024,
                temperature=0.0, # Deterministic for SQL
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return f"Error: {str(e)}"

    def synthesize_answer(self, user_question: str, sql_result: str, row_data: list) -> str:
        """
        Converts detailed data into a human-readable summary
        """
        if not self.client:
            return f"Data found: {row_data} (AI explanation unavailable: Missing API Key)"

        prompt = f"""
        User Question: "{user_question}"
        
        SQL Query Run: {sql_result}
        
        Data Returned: {str(row_data)}
        
        Task: Explain the answer to the user in simple, friendly human language. 
        Do not show the SQL or raw JSON unless specifically asked.
        Just give the insight.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful data assistant. Answer the user based on the provided data."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
             return f"Here is the data: {row_data}"

# Singleton instance
ai_service = AIService()
