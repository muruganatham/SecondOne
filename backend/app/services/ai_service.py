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
        
    def analyze_question_with_schema(self, user_question: str, schema_context: str, model: str = "deepseek-chat") -> dict:
        """
        Deep analysis of the question with FULL schema context.
        The AI analyzes:
        1. Question intent and what data is needed
        2. Which tables and relationships can provide that data
        3. Whether the query is answerable with available schema
        4. Recommended query strategy
        
        Returns: {
            "can_answer": bool,
            "query_type": str,
            "recommended_tables": [...],
            "reasoning": str,
            "confidence": str,
            "suggested_sql_approach": str
        }
        """
        client = self._get_client(model)
        if not client:
            return {"can_answer": True, "error": "AI client not available, proceeding anyway"}
        
        # Enhanced analysis prompt with FULL schema context
        analysis_prompt = f"""You are an expert database analyst. Your job is to help answer the user's question by identifying relevant tables and query strategies.

COMPLETE DATABASE SCHEMA:
{schema_context}

USER QUESTION: "{user_question}"

Your task:
1. Understand what data the user is asking for
2. Identify which tables and relationships can provide this data
3. Suggest the best query approach
4. Be OPTIMISTIC - if there's any way to answer the question with available data, identify it

Respond in this EXACT JSON format (no markdown, no extra text):
{{
    "can_answer": true/false,
    "query_type": "simple|complex|general_knowledge",
    "recommended_tables": ["table1", "table2"],
    "reasoning": "brief explanation of your analysis and recommended approach",
    "confidence": "high|medium|low",
    "suggested_sql_approach": "brief description of how to construct the query",
    "alternative_interpretation": "if the question could mean multiple things, suggest the most likely interpretation"
}}

IMPORTANT GUIDELINES:
- If the question is about general knowledge (not database-related), set query_type to "general_knowledge" and can_answer to true
- If data exists but in different table names, identify the correct tables (e.g., "assessments" might be in "user_assessments" or "assessment_results")
- Consider table relationships and foreign keys to find indirect data
- Look for enum mappings to understand status/role fields
- Be creative in finding solutions - don't say "unanswerable" unless truly impossible
- For user-specific questions (like "my assessments"), assume we can filter by user_id
- College-specific tables are prefixed with college codes (e.g., srec_2025_2_coding_result)"""

        try:
            model_name = "deepseek-chat" if "deepseek" in model else "gpt-4"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a database schema expert. Analyze questions deeply and respond with valid JSON only."},
                    {"role": "user", "content": analysis_prompt},
                ],
                max_tokens=800,
                temperature=0.1,
                stream=False
            )
            
            import json
            analysis_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if "```json" in analysis_text:
                analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
            elif "```" in analysis_text:
                analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(analysis_text)
            
            print(f"🔍 Deep Schema Analysis:")
            print(f"   - Can Answer: {analysis.get('can_answer', 'unknown')}")
            print(f"   - Query Type: {analysis.get('query_type', 'unknown')}")
            print(f"   - Recommended Tables: {analysis.get('recommended_tables', [])}")
            print(f"   - Confidence: {analysis.get('confidence', 'unknown')}")
            print(f"   - Reasoning: {analysis.get('reasoning', 'N/A')[:100]}...")
            
            return {
                "can_answer": analysis.get("can_answer", True),
                "query_type": analysis.get("query_type", "unknown"),
                "recommended_tables": analysis.get("recommended_tables", []),
                "reasoning": analysis.get("reasoning", ""),
                "confidence": analysis.get("confidence", "medium"),
                "suggested_sql_approach": analysis.get("suggested_sql_approach", ""),
                "alternative_interpretation": analysis.get("alternative_interpretation", "")
            }
            
        except Exception as e:
            print(f"❌ Schema Analysis Error: {e}")
            # If analysis fails, allow to proceed (fallback to original behavior)
            return {
                "can_answer": True,
                "error": str(e),
                "query_type": "unknown",
                "recommended_tables": [],
                "reasoning": "Analysis failed, proceeding with direct SQL generation",
                "confidence": "low"
            }

    def generate_sql(self, system_prompt: str, user_question: str, model: str = "deepseek-chat") -> str:
        """
        Generates SQL from natural language using specified model
        """
        client = self._get_client(model)
        if not client:
            return f"Error: API Key for {model} is missing."

        try:
            model_name = "deepseek-chat" if "deepseek" in model else "gpt-4"
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
        
        Data Retrieved: 
        {str(row_data)}
        
        Task: You are an Executive Assistant. Summarize the data for a non-technical user.
        
        PRODUCTION GUIDELINES:
        1. **Clean & Direct**: Start with the answer immediately. No "Based on the data..." preambles.
        2. **No Technical Terms**: Do NOT mention "columns", "rows", "status codes", "table names", or "role IDs".
        3. **Formatting**:
           - **NO MARKDOWN**: Plain text only. No asterisks (**), underscores (_), or backticks (`).
           - **LISTS**: Use standard bullet points ("- ") for items. 
           - **SPACING**: Use **SINGLE SPACING** only. Do NOT use double newlines (blank lines) between list items.
           - **LAYOUT**: Keep the output compact.
        4. **Tone**: Professional, confident, and concise. 
        5. **Context**: If the count includes specific filters (like "Active Only"), mention it naturally.

        EXAMPLE OUTPUT:
        "There are 4,021 active students across these departments:
        - CSE: 1,200 students
        - ECE: 800 students
        - MECH: 600 students"
        """
        
        try:
            model_name = "deepseek-chat" if "deepseek" in model else "gpt-4"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a professional assistant. Output clean, formatted text only."},
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
                    {"role": "system", "content": """You are a specialized IT and Educational Consultant. 
You are strictly limited to answering questions related to:
1. Companies (e.g., tech companies, recruiting firms, industry leaders).
2. Professional Skills (e.g., programming languages, soft skills, technical concepts).
3. Educational Information (e.g., courses, degrees, study topics, academic concepts).

If the user asks about ANYTHING else (e.g., movies, sports, politics, general history, biology, entertainment, personal advice), you MUST refuse to answer.
Refusal message: "I can only answer general knowledge questions related to Companies, Skills, and Educational Information."
Do not answer the prohibited question."""},
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
