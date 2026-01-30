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
        # Initialize DeepSeek client
        self.deepseek_api_key = settings.DEEPSEEK_API_KEY or os.getenv("DEEPSEEK_API_KEY")
        self.deepseek_base_url = "https://api.deepseek.com"
        
        # Initialize OpenAI client
        self.openai_api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        
        print(f"DEBUG: DeepSeek API Key: {self.deepseek_api_key[:20]}..." if self.deepseek_api_key else "No DeepSeek key")
        print(f"DEBUG: OpenAI API Key: {self.openai_api_key[:20]}..." if self.openai_api_key else "No OpenAI key")

        # Create DeepSeek client
        if self.deepseek_api_key:
            self.deepseek_client = OpenAI(
                api_key=self.deepseek_api_key,
                base_url=self.deepseek_base_url
            )
        else:
            self.deepseek_client = None
            print("⚠️ WARNING: DEEPSEEK_API_KEY is not set.")
        
        # Create OpenAI client
        if self.openai_api_key:
            self.openai_client = OpenAI(
                api_key=self.openai_api_key
            )
        else:
            self.openai_client = None
            print("⚠️ WARNING: OPENAI_API_KEY is not set.")
        
        # For backward compatibility
        self.client = self.deepseek_client
        
    def generate_sql(self, system_prompt: str, user_question: str, model: str = "deepseek-chat") -> str:
        """
        Generates SQL from natural language using specified model
        """
        client = self._get_client(model)
        if not client:
            return f"Error: API Key for {model} is missing."

        try:
            model_name = "deepseek-coder" if "deepseek" in model else "gpt-4"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question},
                ],
                max_tokens=1024,
                temperature=0.0,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return f"Error: {str(e)}"

    def synthesize_answer(self, user_question: str, sql_result: str, row_data: list, model: str = "deepseek-chat") -> str:
        """
        Converts detailed data into a human-readable summary
        """
        client = self._get_client(model)
        if not client:
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
            model_name = "deepseek-chat" if "deepseek" in model else "gpt-4"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful data assistant. Answer the user based on the provided data."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
             return f"Here is the data: {row_data}"

    def generate_follow_ups(self, user_question: str, answer: str, sql_query: str) -> list:
        """
        Generates 3 contextual follow-up questions based on the conversation
        """
        if not self.client:
            return [
                "Can you show me more details?",
                "How does this compare to other records?",
                "What are the trends over time?"
            ]

        prompt = f"""
        User asked: "{user_question}"
        
        We answered: "{answer}"
        
        SQL used: {sql_query}
        
        Task: Generate 3 smart follow-up questions the user might want to ask next.
        Make them specific to the data and context.
        Return ONLY the 3 questions, one per line, no numbering or extra text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that suggests relevant follow-up questions."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            # Parse response into list
            follow_ups_text = response.choices[0].message.content.strip()
            follow_ups = [q.strip() for q in follow_ups_text.split('\n') if q.strip()]
            
            # Return first 3 questions
            return follow_ups[:3] if len(follow_ups) >= 3 else follow_ups + [
                "Can you show me more details?",
                "How does this compare to others?"
            ][:3-len(follow_ups)]
            
        except Exception as e:
            print(f"❌ Follow-up generation error: {e}")
            return [
                "Can you show me more details about this?",
                "How does this compare to other records?",
                "What are the trends over time?"
            ]

    def _get_client(self, model: str):
        """Get the appropriate client based on model name"""
        if "gpt" in model.lower():
            return self.openai_client
        else:
            return self.deepseek_client

    def is_destructive_query(self, sql: str) -> bool:
        """
        Detects if a SQL query is destructive (modifies data)
        Returns True for UPDATE, DELETE, DROP, TRUNCATE, ALTER queries
        """
        if not sql:
            return False
        
        sql_upper = sql.strip().upper()
        destructive_keywords = ['UPDATE', 'DELETE', 'DROP', 'TRUNCATE', 'ALTER', 'INSERT']
        
        # Check if query starts with destructive keyword
        for keyword in destructive_keywords:
            if sql_upper.startswith(keyword):
                return True
        
        return False

ai_service = AIService()
