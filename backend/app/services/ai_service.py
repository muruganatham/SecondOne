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
    "suggested_sql_approach": "brief description of how to construct the query",
    "reasoning": "very brief explanation (max 1 sentence)"
}}

IMPORTANT GUIDELINES:
- If the question is about general knowledge (not database-related), set query_type to "general_knowledge" and can_answer to true.
- CATEGORIZATION: General knowledge is ONLY allowed if it relates to: Companies, Skills, Educational Info, or Recruitment/Interviews. Everything else is out-of-scope.
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
                max_tokens=500, # Reduced for speed
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
            
            # Additional cleanup for robust parsing
            analysis_text = analysis_text.strip()
            if not analysis_text.endswith("}"):
                # Try to fix truncated JSON
                analysis_text += "}" 
            
            try:
                analysis = json.loads(analysis_text)
            except:
                # Fallback if AI returns malformed JSON
                print(f"⚠️ Warning: AI returned malformed JSON: {analysis_text[:100]}...")
                return {
                    "can_answer": True,
                    "query_type": "simple", 
                    "recommended_tables": [],
                    "reasoning": "JSON parse error, proceeding anyway",
                    "suggested_sql_approach": "Standard SQL"
                }
            
            print(f"🔍 Deep Schema Analysis:")
            print(f"   - Can Answer: {analysis.get('can_answer', 'unknown')}")
            print(f"   - Query Type: {analysis.get('query_type', 'unknown')}")
            print(f"   - Recommended Tables: {analysis.get('recommended_tables', [])}")
            print(f"   - SQL Approach: {analysis.get('suggested_sql_approach', 'N/A')[:100]}...")
            
            return {
                "can_answer": analysis.get("can_answer", True),
                "query_type": analysis.get("query_type", "unknown"),
                "recommended_tables": analysis.get("recommended_tables", []),
                "reasoning": analysis.get("reasoning", ""),
                "suggested_sql_approach": analysis.get("suggested_sql_approach", ""),
                "confidence": analysis.get("confidence", "medium") # Optional now
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
                    {"role": "system", "content": f"{system_prompt}"},
                    {"role": "user", "content": user_question},
                ],
                max_tokens=2048,
                temperature=0.0,
                seed=42,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return f"Error: {str(e)}"

    def synthesize_answer(self, user_question: str, sql_result: str, row_data: list, model: str = "deepseek-chat", role_id: int = None) -> str:
        """
        Converts detailed data into a human-readable summary.
        Now supports Role-Based Personas (e.g. Admin gets Executive Summaries).
        """
        client = self._get_client(model)
        if not client:
            return f"Data found: {row_data} (AI explanation unavailable: Missing API Key)"

        # Default Persona
        persona = "You are an Executive Assistant. Summarize the data for a non-technical user."
        guidance = ""
        
        # Admin Persona (Production Level)
        if role_id in [1, 2]:
            persona = "You are a Senior Data Analyst & Placement Director."
            guidance = """
            [ADMIN SPECIFIC INSTRUCTIONS]:
            1. **Strategic Tone**: Be direct, professional, and insight-driven.
            2. **Recruitment Focus**: If the question is about "Cracking Interviews" or "Eligibility", provide a clear ASSESSMENT (High/Medium/Low chance) based on the data.
            3. **Actionable Insights**: Don't just list data; suggest next steps (e.g., "Recommend focused training on DSA").
            4. **Risk Flags**: Highlight low attendance or poor performance as "Risk Factors".
            """

        prompt = f"""
        User Question: "{user_question}"
        User Role ID: {role_id}
        
        Data Retrieved: 
        {str(row_data)}
        
        Task: {persona}
        
        PRODUCTION GUIDELINES:
        1. **Professional & Informative**: Start with the direct answer.
        2. **Insightful**: Use the data to provide context and trends.
        3. **Formatting**:
           - **MARKDOWN**: Use Markdown Tables for datasets to ensure high readability.
           - **BOLDING**: Use bold text for key metrics and numbers.
           - **LISTS**: Use standard bullet points.
        4. **No Technical Jargon**: Do NOT mention "columns", "rows", or "table names".
        5. **Confidence**: Provide a complete summary of all retrieved data.
        6. **ANTI-HALLUCINATION**: ONLY answer based on the 'Data Retrieved'. If the data is empty or insufficient, explicitly state: 'I couldn't find sufficient data to answer this part of your question.' Do NOT make up numbers, names, or performance facts.
        
        {guidance}

        EXAMPLE OUTPUT:
        "**Assessment for Sanjay**:
        Sanjay has a **High Probability** of clearing Zoho based on:
        - **CGPA**: 8.5 (Strong)
        - **Coding Score**: 92% (Excellent)
        
        **Recommendation**: Encourage him to focus on System Design."
        """
        
        try:
            model_name = "deepseek-chat" if "deepseek" in model else "gpt-4"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a professional assistant. Output clean, formatted text only."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                seed=42
            )
            return response.choices[0].message.content
        except Exception as e:
             return f"Here is the data: {row_data}"

    def generate_follow_ups(self, user_question: str, sql_query: str, data: list = None, answer: str = None, role_id: int = None) -> list:
        """
        Generates 3 contextual follow-up questions independent of the final answer text.
        Injects role-specific security constraints to prevent unauthorized pivots.
        """
        if not self.client:
            return ["Show more details", "Visualization", "Export data"]

        # Optimize Context
        data_preview = "No Data"
        if data:
            try:
                preview_items = data[:3]
                data_preview = str(preview_items)
            except:
                data_preview = str(data)[:500]
        
        # Role-based Security Constraints
        security_guidance = ""
        if role_id == 7: # Student
            security_guidance = """
            [SECURITY: STUDENT ROLE]
            - DO NOT suggest querying marks, grades, or performance for ANY individual OTHER than the user.
            - DO NOT suggest "drilling down" into peer data found in the findings.
            - Focus suggestions on personal growth, department rankings, or course materials.
            """
        elif role_id == 5: # Trainer
            security_guidance = "[SECURITY: TRAINER] Focus on department-level performance and student tracking."
        elif role_id == 3: # College Admin
            security_guidance = "[SECURITY: COLLEGE ADMIN] Focus on institutional metrics and recruitment."

        prompt = f"""
        [SCENARIO]
        User Query: "{user_question}"
        Data Findings: {data_preview}
        
        {security_guidance}

        [TASK]
        Suggest 3 "Next Logical Questions" that are safe and relevant for this user's role.
        
        [STRATEGY]
        1. **Deepen**: Ask for more detail about the *current* dataset (e.g., "Top performers" if looking at marks).
        2. **Personal**: Focus on user's own path (if Student).
        3. **Safe Pivots**: Comparisons to averages or exploring related courses/materials.
        
        [CONSTRAINTS]
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
1. Companies (e.g., tech companies like Zoho, recurring firms, industry leaders, hiring trends, company culture).
2. Professional Skills (e.g., programming languages, soft skills, technical concepts, career development).
3. Educational Information (e.g., academic advice, study topics, university/degree info, learning paths).
4. Recruitment & Interviews (e.g., interview process, common questions, aptitude tests, technical rounds, preparation tips).

[STRICT ENFORCEMENT]:
If the user asks about ANYTHING unrelated to the above (e.g., sports, movies, politics, entertainment, general history, biology), you MUST refuse to answer.
Refusal message: "I am only authorized to provide general knowledge on Companies, Professional Skills, Educational Information, and Recruitment."
Do not answer the prohibited question or provide any context for it."""},
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
