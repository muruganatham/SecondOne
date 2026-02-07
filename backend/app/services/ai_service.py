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
        
        SQL Query Context: "{sql_result}"
        
        Data Retrieved: 
        {str(row_data)}
        
        Task: You are a Data Analyst. Analyze the data above and provide a clear, accurate response.
        
        Guidelines:
        1. **Direct Answer**: Start with the direct answer (number, list, or fact).
        2. **Insight (If applicable)**: If the data allows, briefly explain *why* or provide a percentage/trend (e.g. "This represents 80% of active users").
        3. **No Data Handling**: If the data is empty `[]` or None, say "No active records found matching that criteria." Do NOT make up data.
        4. **Tone**: Professional, precise, yet conversational.
        5. **Formatting**: Use bullet points for lists. Use bold for key numbers.
        6. **Context**: If the SQL used `status=1`, you can mention "active students" to be precise.

        Reference Cheat Sheet (Translate these codes to text if seen):
        - Status: 0=Inactive, 1=Active
        - Role: 1=SuperAdmin, 2=Admin, 3=CollegeAdmin, 4=Staff, 5=Trainer, 7=Student
        - Gender: 1=Male, 2=Female
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

    def generate_follow_ups(self, user_question: str, sql_query: str, data: list = None, answer: str = None) -> list:
        """
        Generates 3 contextual follow-up questions independent of the final answer text
        """
        if not self.client:
            return ["Show more details", "Visualization", "Export data"]

        # Optimize Context
        data_preview = "No Data"
        if data:
            # Create a structured preview of the first few items to help AI pick names/values
            try:
                # If data is list of objects/dicts
                preview_items = data[:3]
                data_preview = str(preview_items)
            except:
                data_preview = str(data)[:500]
        
        prompt = f"""
        [SCENARIO]
        User Query: "{user_question}"
        Data Findings: {data_preview}
        
        [TASK]
        As an expert Data Analyst, suggest 3 "Next Logical Questions" the user should ask to dig deeper.
        
        [STRATEGY]
        1. **Drill Down**: specific detail query (e.g., "Show [Student Name]'s marks" if a name appears).
        2. **Pivot/Compare**: comparative insight (e.g., "How does this compare to class average?").
        3. **Actionable**: a decision-support query (e.g., "Who needs improvement?").
        
        [CONSTRAINTS]
        - If specific names/roles appear in Data Findings, USE THEM in the questions (e.g. "What about [Name]?").
        - Keep questions short, natural, and useful.
        - Output strictly 3 lines. No numbering.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful data analyst assistant. Generate only the questions, one per line."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            # Parse response into list
            follow_ups_text = response.choices[0].message.content.strip()
            follow_ups = [q.strip() for q in follow_ups_text.split('\n') if q.strip()]
            
            # Clean up numbering if present (1. , - , etc)
            cleaned_follow_ups = []
            for q in follow_ups:
                # Remove leading numbers or dashes
                import re
                clean_q = re.sub(r'^[\d\-\.\)\s]+', '', q)
                cleaned_follow_ups.append(clean_q)
            
            return cleaned_follow_ups[:3] if len(cleaned_follow_ups) >= 3 else cleaned_follow_ups
            
        except Exception as e:
            print(f"❌ Follow-up generation error: {e}")
            return ["Analyze further", "Show details", "Visualize result"]
            


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

    def answer_general_question(self, user_question: str, model: str = "deepseek-chat") -> str:
        """
        Answers general knowledge questions using the LLM directly, skipping database context.
        """
        client = self._get_client(model)
        if not client:
            return "I cannot answer this question as the AI service is unavailable."

        try:
            model_name = "deepseek-chat" if "deepseek" in model else "gpt-4"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful IT and Educational Consultant. Answer the user's question accurately based on general knowledge. Do not mention that you cannot access the database. Be helpful, professional, and concise."},
                    {"role": "user", "content": user_question},
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ General Answer Error: {e}")
            return "I encountered an error while processing your request."

ai_service = AIService()
