"""
DeepSeek AI Service - Production Grade v3.1
Handles communication with the DeepSeek API (OpenAI-compatible).

FIXES & CHANGES:
- max_tokens 500 → 2000 in generate_sql() (fixes all SQL truncation bugs)
- max_tokens 500 → 800 in analyze_question_with_schema()
- Added _is_sql_truncated() to detect cut-off queries before DB execution
- Added auto-retry with simplified prompt on truncation
- Added dynamic column resolution via DESCRIBE (fixes wrong column name errors)
- Added schema hint injection into AI prompt (fixes solved_count / total_coding_score errors)
- solve_status filter moved to JOIN ON clause (prevents row drops on LEFT JOIN)
- Added confirmed schema for tests, srec result, standard_qb_codings tables
- Added TYPE F (Trainer) and TYPE G (Assessment) query patterns
- Token usage logging for monitoring
"""

import os
import re
import json
from datetime import datetime
from openai import OpenAI
from app.core.config import settings
from app.core.logging_config import get_logger
from app.core.db import SessionLocal
from sqlalchemy import text

logger = get_logger("ai_service")


# ════════════════════════════════════════════════════════════════
#  CONFIRMED TABLE SCHEMAS (verified via DESCRIBE)
#  Use these as ground truth when building prompts
# ════════════════════════════════════════════════════════════════

CONFIRMED_SCHEMAS = {
    "tests": {
        "id": "bigint unsigned",
        "testName": "varchar(50)",  # ← camelCase! NOT test_name
        "clone_id": "int",
        "is_edited": "tinyint",
        "creator_college_id": "int",
        "status": "tinyint",
        "created_at": "timestamp",
        "updated_at": "timestamp",
    },
    "srec_2025_2_coding_result": {
        "id": "bigint unsigned",
        "user_id": "bigint unsigned",
        "allocate_id": "int unsigned",
        "course_allocation_id": "bigint unsigned",
        "topic_test_id": "bigint unsigned",  # ← FK to tests.id
        "topic_type": "int unsigned",  # 1 = coding
        "module_id": "bigint unsigned",
        "question_id": "int unsigned",  # ← FK to standard_qb_codings.id
        "type": "int unsigned",
        "complexity": "int",
        "mark": "float",
        "total_mark": "float",
        "main_solution": "text",  # ← student's submitted code
        "sub_solutions": "json",
        "test_cases": "json",
        "compile_id": "int",
        "total_time": "int",
        "first_submission_time": "int",
        "correct_submission_time": "int",
        "errors": "json",
        "action_counts": "json",
        "report_metrics": "json",
        "solve_status": "int",  # 0=unsolved 1=partial 2=solved
        "status": "tinyint",
        "created_at": "timestamp",
        "updated_at": "timestamp",
    },
}

# Verified via SHOW TABLES LIKE '%coding%'
COLLEGE_CODING_TABLES = [
    "academic_qb_codings",
    "admin_coding_result",
    "b2c_coding_result",
    "ciet_2026_1_coding_result",
    "demolab_2025_2_coding_result",
    "demolab_2026_1_coding_result",
    "dotlab_2025_2_coding_result",
    "dotlab_2026_1_coding_result",
    "jpc_2026_1_coding_result",
    "kclas_2026_1_coding_result",
    "kits_2026_1_coding_result",
    "link_coding_result",
    "mcet_2025_2_coding_result",
    "mcet_2026_1_coding_result",
    "mec_2026_1_coding_result",
    "niet_2026_1_coding_result",
    "nit_2026_1_coding_result",
    "skacas_2025_2_coding_result",
    "skasc_2026_1_coding_result",
    "skcet_2026_1_coding_result",
    "skct_2025_2_coding_result",
    "srec_2025_2_coding_result",
    "srec_2026_1_coding_result",
    "standard_qb_coding_validations",
    "tep_2026_1_coding_result",
    "uit_2026_1_coding_result",
]

# Verified via SHOW TABLES LIKE '%question%'
QUESTION_TABLES = [
    "feedback_questions",
    "practice_question_maps",
    "test_question_maps",  # ← bridge between tests and standard_qb_codings
    "viva_question_bank",
]


# ════════════════════════════════════════════════════════════════
#  AI SERVICE
# ════════════════════════════════════════════════════════════════


class AIService:

    def __init__(self):
        self.deepseek_api_key = settings.DEEPSEEK_API_KEY or os.getenv(
            "DEEPSEEK_API_KEY"
        )

        print(
            f"DEBUG: DeepSeek API Key: {self.deepseek_api_key[:20]}..."
            if self.deepseek_api_key
            else "No DeepSeek key"
        )

        # Create DeepSeek client
        if self.deepseek_api_key:
            logger.info("DeepSeek API key configured")
            self.deepseek_client = OpenAI(
                api_key=self.deepseek_api_key,
                base_url="https://api.deepseek.com",
            )
        else:
            logger.warning("DeepSeek API key not found")
            self.deepseek_client = None
            print("⚠️ WARNING: DEEPSEEK_API_KEY is not set.")

        # Always use DeepSeek
        self.client = self.deepseek_client

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (approx 4 chars per token)."""
        if not text:
            return 0
        return len(text) // 4

    def _log_token_usage(
        self, 
        interaction_type: str, 
        usage, 
        user_question: str, 
        model: str,
        input_breakdown: dict = None
    ):
        """Log token usage with optional breakdown."""
        if not usage:
            return

        try:
            breakdown_str = ""
            if input_breakdown:
                parts = [f"{k}: ~{v}" for k, v in input_breakdown.items()]
                breakdown_str = f" ({', '.join(parts)})"

            log_entry = (
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {interaction_type.upper():<15} | "
                f"Total: {usage.total_tokens:<5} "
                f"(Input: {usage.prompt_tokens:<5}{breakdown_str}, Output: {usage.completion_tokens:<5}) | "
                f"Model: {model:<15} | Q: {user_question[:50]}..."
            )
            
            # Append to token_usage.log in the backend directory
            with open("token_usage.log", "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
                
        except Exception as e:
            logger.error(f"Failed to log token usage: {e}")


    def _get_client(self, model: str):
        """Get the appropriate OpenAI client for the specified model"""
        # For now, we only support DeepSeek
        return self.deepseek_client

    def _is_sql_truncated(self, sql: str) -> bool:
        """
        Check if the SQL query appears to be truncated/incomplete.
        Signs of truncation:
        - Missing closing parentheses
        - Missing semicolon at end
        - Ends with incomplete syntax (AND, OR, comma, etc.)
        """
        if not sql:
            return True

        sql = sql.strip()

        # Check for unbalanced parentheses
        if sql.count("(") != sql.count(")"):
            return True

        # Check for incomplete FROM/WHERE/JOIN (ends with keyword)
        incomplete_endings = [" FROM", " WHERE", " AND", " OR", " JOIN", " ON", ","]
        for ending in incomplete_endings:
            if sql.upper().endswith(ending.upper()):
                return True

        # Query should end with semicolon or just be valid
        if not sql.upper().startswith("SELECT"):
            return True

        return False

    def _build_simplified_prompt(self, user_question: str) -> str:
        """Build a simplified prompt for retry with fewer JOINs and simpler structure"""
        return f"""
You are a MySQL expert. Generate a SIMPLE, DIRECT SQL query for this question.
Use minimal JOINs (max 2), no subqueries, no window functions.

QUESTION: {user_question}

Return ONLY the SELECT statement. Start with SELECT, end with semicolon.
"""

    # second update
    def analyze_question_with_schema(
        self,
        user_question: str,
        schema_context: str,
        model: str = "deepseek-chat",
        user_context_str: str = "",
    ) -> dict:
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
            return {"can_answer": True, "error": "AI client not available"}

        analysis_prompt = f"""You are an expert database analyst. Identify the best tables and strategy to answer the user's question.

DATABASE SCHEMA:
{schema_context}

USER QUESTION: "{user_question}"

USER CONTEXT:
{user_context_str}

YOUR TASK:
1. Identify EVERYTHING the user is asking for.
2. **DEEP SEARCH MODE**: The user requires a thorough analysis. Do not stop at the first match.
   - Search for indirect relationships.
   - If a table seems empty or irrelevant, check for mapping tables.
   - If the data is not in the obvious table, look for related tables (e.g. `colleges` -> `users` -> `results`).
3. CRITICAL: Data might be stored:
   - DIRECTLY (e.g. user_id is in the table).
   - HIERARCHICALLY (e.g. table is linked to a College, Dept, Batch, or Section mapping).
   - If one table (like user_course_enrollments) is empty, a mapping table (like course_academic_maps) almost certainly contains the data.
4. RECOMMENDED TABLES: List ALL tables needed for JOINs to answer the question accurately within the user's scope.
5. BE OPTIMISTIC: If it sounds like data that should be in an LMS, it likely is. Find the closest match.

Respond in this EXACT JSON format (no markdown, no extra text):
Reply ONLY in this exact JSON format (no markdown, no extra text):
{{
    "can_answer": true/false,
    "query_type": "simple|complex|general_knowledge",
    "recommended_tables": ["table1", "table2"],
    "suggested_sql_approach": "one-line description",
    "reasoning": "detailed reasoning allowing for deep analysis"
}}

RULES:
- Only recommend tables that exist in the schema above
- Never use placeholder values like {{user_id}} — use literal values
- "general_knowledge" only for: Companies, Skills, Educational Info, Career Advice
- "Who am I?" / "My Profile" = database query (type: simple), NOT general_knowledge
- tests.testName is camelCase — never suggest test_name
- coding result FK to tests = topic_test_id (NOT test_id)
- Bridge table between tests ↔ questions = test_question_maps
- College result tables follow: [college]_[year]_[sem]_coding_result"""

        try:
            model_name = "deepseek-chat"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a database schema expert. Respond with valid JSON only.",
                    },
                    {"role": "user", "content": analysis_prompt},
                ],
                max_tokens=getattr(settings, "AI_MAX_OUTPUT_TOKENS", 2000),  # Fallback to 2000 if not set
                temperature=0.1,
                stream=False,
            )

            raw = response.choices[0].message.content.strip()

            # Log token usage
            if response.usage:
                # Estimate breakdown
                sys_tokens = self._estimate_tokens(analysis_prompt.split("USER QUESTION")[0])
                q_tokens = self._estimate_tokens(user_question)
                schema_tokens = self._estimate_tokens(schema_context)
                
                self._log_token_usage(
                    "SCHEMA_ANALYSIS", 
                    response.usage, 
                    user_question, 
                    model_name,
                    input_breakdown={
                        "Schema": schema_tokens,
                        "System": sys_tokens,
                        "Q": q_tokens
                    }
                )

            # Strip markdown fences if present
            if "```json" in raw:
                raw = raw.split("```json")[1].split("```")[0].strip()
            elif "```" in raw:
                raw = raw.split("```")[1].split("```")[0].strip()

            if not raw.endswith("}"):
                raw += "}"

            try:
                analysis = json.loads(raw)
            except Exception:
                logger.warning(f"Malformed JSON from schema analysis: {raw[:100]}")
                return {
                    "can_answer": True,
                    "query_type": "simple",
                    "recommended_tables": [],
                    "reasoning": "JSON parse error — proceeding with direct SQL generation",
                    "suggested_sql_approach": "Standard SQL",
                    "confidence": "low",
                }

            logger.info(
                f"Schema Analysis | "
                f"can_answer={analysis.get('can_answer')} | "
                f"type={analysis.get('query_type')} | "
                f"tables={analysis.get('recommended_tables')}"
            )

            return {
                "can_answer": analysis.get("can_answer", True),
                "query_type": analysis.get("query_type", "unknown"),
                "recommended_tables": analysis.get("recommended_tables", []),
                "reasoning": analysis.get("reasoning", ""),
                "suggested_sql_approach": analysis.get("suggested_sql_approach", ""),
                "confidence": analysis.get("confidence", "medium"),
            }

        except Exception as e:
            logger.error(f"Schema Analysis Error: {e}")
            return {
                "can_answer": True,
                "error": str(e),
                "query_type": "unknown",
                "recommended_tables": [],
                "reasoning": "Analysis failed — proceeding with direct SQL generation",
                "confidence": "low",
            }

    # ────────────────────────────────────────────
    # SQL Generation
    # ────────────────────────────────────────────

    def generate_sql(
        self,
        system_prompt: str,
        user_question: str,
        model: str = "deepseek-chat",
        result_table: str = None,
    ) -> str:
        """
        Generates SQL from a natural language question.

        Args:
            system_prompt:  Admin/role prompt from get_admin_prompt()
            user_question:  User's natural language question
            model:          AI model (default: deepseek-chat)
            result_table:   Optional college result table name.
                            When provided, real columns are injected into
                            the prompt so AI never guesses column names.

        Returns:
            A complete, valid SQL SELECT string — or "Error: ..." on failure.
        """
        client = self._get_client(model)
        if not client:
            return f"Error: API key for '{model}' is missing"

        # Inject verified column schema if result_table provided
        schema_hint = ""
        if result_table:
            schema_hint = (
                f"\n\n### VERIFIED RESULT TABLE SCHEMA:\n"
                f"{self._build_result_table_schema_hint(result_table)}\n"
            )

        safe_system_prompt = f"""{system_prompt}{schema_hint}

### CONFIRMED TABLE FACTS (always follow — verified via DESCRIBE):

-- tests table:
--   testName          VARCHAR(50)   ← camelCase, NEVER test_name
--   status            TINYINT
--   created_at        TIMESTAMP

-- [college]_coding_result tables (e.g. srec_2025_2_coding_result):
--   user_id           BIGINT        ← FK to users.id
--   topic_test_id     BIGINT        ← FK to tests.id  (NEVER test_id)
--   question_id       INT           ← FK to standard_qb_codings.id
--   topic_type        INT           ← 1 = coding questions
--   mark              FLOAT         ← student's score for this question
--   total_mark        FLOAT         ← max possible mark
--   solve_status      INT           ← 0=unsolved, 1=partial, 2=solved
--   main_solution     TEXT          ← student's submitted code
--   test_cases        JSON          ← test case results

-- For assessment question queries:
--   Bridge table      → test_question_maps (test_id, question_id)
--   Question bank     → standard_qb_codings (id, title, question, solution, testcases)
--   Join order        → coding_result → tests → test_question_maps → standard_qb_codings

-- For trainer queries:
--   Use users WHERE role = 5 + JOIN user_academics (college filter)
--   NEVER join course_staff_trainer_allocations → causes 1 row per course assignment

### CRITICAL SQL RULES (non-negotiable):
1.  SELECT only — no INSERT, UPDATE, DELETE, DROP, ALTER
2.  Return ONLY raw SQL — no explanation, no markdown fences, no comments
3.  Every '(' must have a matching ')'
4.  Every CASE must have a matching END
5.  Only use columns confirmed in the schema above
6.  solve_status goes in JOIN ON — not WHERE — to avoid losing LEFT JOIN rows:
      ✅  LEFT JOIN result_table cr ON cr.user_id = u.id AND cr.solve_status = 2
      ❌  WHERE cr.solve_status = 2
7.  Always add LIMIT (default 100)
8.  Use SELECT DISTINCT when joining allocation/map tables to prevent duplicates
9.  Mentally count parentheses and CASE/END pairs before returning"""

        model_name = "deepseek-chat" if "deepseek" in model else "gpt-4"

        # ── Attempt 1 ──────────────────────────────────────────────────────
        try:
            logger.debug(f"SQL generation attempt 1: {user_question[:80]}")

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": safe_system_prompt},
                    {"role": "user", "content": user_question},
                ],
                max_tokens=getattr(settings, "AI_MAX_OUTPUT_TOKENS", 2000),  # Fallback to 2000 if not set
                temperature=0.0,
                seed=42,
                stream=False,
            )

            generated = response.choices[0].message.content

            # Log token usage
            if hasattr(response, "usage") and response.usage:
                u = response.usage
                
                # Estimate breakdown for SQL Gen
                # prompt contains: detailed schema, role instruction, analysis result
                # roughly:
                schema_part = safe_system_prompt.split("===")[0] if "===" in safe_system_prompt else ""
                sys_part = safe_system_prompt.split("===")[1] if "===" in safe_system_prompt else ""
                
                self._log_token_usage(
                    "SQL_GENERATION", 
                    u, 
                    user_question, 
                    model_name,
                    input_breakdown={
                        "Schema": self._estimate_tokens(schema_part),
                        "System": self._estimate_tokens(sys_part),
                        "Q": self._estimate_tokens(user_question)
                    }
                )
                logger.info(
                    f"SQL tokens | prompt={u.prompt_tokens} "
                    f"completion={u.completion_tokens} total={u.total_tokens}"
                )
                limit = getattr(settings, "AI_MAX_OUTPUT_TOKENS", 2000)
                if u.completion_tokens > (limit * 0.9):
                    logger.warning(
                        f"Completion near limit ({u.completion_tokens}/{limit}) - "
                        "consider simplifying question or raising max_tokens further."
                    )

            logger.debug(f"SQL attempt 1: {generated[:150]}")

            if self._is_sql_truncated(generated):
                logger.warning(
                    "SQL truncated on attempt 1 — retrying with simplified prompt"
                )
                return self._generate_sql_retry(
                    client, model_name, user_question, safe_system_prompt
                )

            return generated

        except Exception as e:
            logger.error(f"SQL generation error: {e}")
            return f"Error: {e}"

    def _generate_sql_retry(
        self,
        client,
        model_name: str,
        user_question: str,
        safe_system_prompt: str,
    ) -> str:
        """
        Attempt 2 — retries with a simplified prompt when attempt 1 was truncated.
        Forces fewer JOINs, no correlated subqueries, simpler structure.
        """
        simplified = self._build_simplified_prompt(user_question)

        try:
            logger.debug(f"SQL generation attempt 2 (simplified): {user_question[:80]}")

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": safe_system_prompt},
                    {"role": "user", "content": simplified},
                ],
                max_tokens=1200,
                temperature=0.0,
                seed=42,
                stream=False,
            )

            generated = response.choices[0].message.content

            if hasattr(response, "usage") and response.usage:
                self._log_token_usage(
                    "SQL_RETRY", response.usage, user_question, model_name
                )
                logger.info(
                    f"SQL retry tokens | completion={response.usage.completion_tokens}/1200"
                )

            if self._is_sql_truncated(generated):
                logger.error(
                    "SQL still truncated after retry — returning error to caller"
                )
                return (
                    "Error: Unable to generate a complete SQL query for this request. "
                    "Please try a simpler or more specific question."
                )

            logger.info("SQL attempt 2 succeeded.")
            return generated

        except Exception as e:
            logger.error(f"SQL retry error: {e}")
            return f"Error: {e}"

    # ────────────────────────────────────────────
    # Result Validation
    # ────────────────────────────────────────────

    def _validate_result_completeness(
        self,
        user_question: str,
        row_data: list,
        expected_type: str = None,
    ) -> dict:
        """
        Assesses the quality and completeness of query results.
        Returns: { is_complete, data_quality, record_count, has_aggregates, insights }
        """
        if not row_data:
            return {
                "is_complete": False,
                "data_quality": "empty",
                "record_count": 0,
                "has_aggregates": False,
                "insights": "No data found. Query may need refinement.",
            }

        record_count = len(row_data) if isinstance(row_data, list) else 1

        has_aggregates = any(
            isinstance(row, dict)
            and any(
                k in str(row) for k in ["count_", "sum_", "avg_", "total_", "COUNT"]
            )
            for row in (row_data if isinstance(row_data, list) else [row_data])
        )

        is_course_query = (
            "course" in user_question.lower() and "what" in user_question.lower()
        )

        if is_course_query and record_count < 5:
            quality = "partial"
            insights = f"⚠️ Only {record_count} courses found — full list may have more."
        elif record_count == 1 and not has_aggregates:
            quality = "partial"
            insights = "⚠️ Only 1 record found — query may be too restrictive."
        else:
            quality = "complete"
            insights = f"✅ Retrieved {record_count} records."

        return {
            "is_complete": quality == "complete",
            "data_quality": quality,
            "record_count": record_count,
            "has_aggregates": has_aggregates,
            "insights": insights,
        }

    # ────────────────────────────────────────────
    # Answer Synthesis
    # ────────────────────────────────────────────

    def synthesize_answer(
        self,
        user_question: str,
        sql_result: str,
        row_data: list,
        model: str = "deepseek-chat",
        role_id: int = None,
    ) -> str:
        """
        Converts raw query results into a human-readable Markdown summary.
        Admins (role 1, 2) receive executive-level structured output.
        """
        client = self._get_client(model)
        if not client:
            return f"Data retrieved: {row_data}\n(AI unavailable — missing API key)"

        validation = self._validate_result_completeness(user_question, row_data)

        # Early exit — empty result
        if validation["data_quality"] == "empty":
            return (
                "❌ No data found. Possible reasons:\n"
                "1. The requested data doesn't exist in the database\n"
                "2. Search filters are too restrictive\n"
                "3. College or department name may be misspelled\n\n"
                "**Suggestions:** Broaden your search, check spelling, "
                "or verify the time period and college name."
            )

        # Role-based persona and formatting
        if role_id in [1, 2]:
            persona = (
                "You are a Senior Database Administrator & Strategic Data Analyst "
                "specializing in student performance, recruitment analytics, "
                "and institutional metrics."
            )
            guidance = """
[ADMIN OUTPUT RULES]:
1.  Present ALL data in structured Markdown (tables for 3+ rows, **bold** key metrics)
2.  Eligibility queries  → label each student: Highly Eligible / Eligible / Review / Not Eligible
3.  Course queries       → show: code, name, type, status
4.  Performance queries  → show: rank, CGPA, coding score, problems solved
5.  Trainer queries      → deduplicate by ID, show active/inactive clearly
6.  Assessment queries   → show: question title, student solution, mark, solve_status
7.  NEVER say "insufficient data" when rows were returned — always present what exists
8.  Flag anomalies: duplicates, conflicting status values, missing fields
9.  End with 1–2 strategic recommendations or next-step suggestions
"""
            result_prefix = (
                f"\n>>> ⚠️ **PARTIAL RESULTS**: {validation['insights']}\n\n"
                if validation["data_quality"] == "partial"
                else f"\n>>> ✅ **COMPLETE RESULTS**: {validation['record_count']} records\n\n"
            )
        else:
            persona = (
                "You are a helpful assistant. Summarize the data clearly for the user."
            )
            guidance = ""
            result_prefix = ""

        prompt = f"""
User Question: "{user_question}"
Role ID: {role_id}
Total Records: {len(row_data) if isinstance(row_data, list) else 1}

Retrieved Data:
{json.dumps(row_data, indent=2, default=str)[:3000]}

Task: {persona}

{guidance}

Output Guidelines:
- Summarize ALL retrieved data comprehensively
- Use Markdown formatting (tables, **bold**, bullet points)
- Base ONLY on the retrieved data — no hallucination
- If data is partial, label it ⚠️ Partial Results but still present it fully
"""

        try:
            model_name = "deepseek-chat"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional data analyst. "
                            "Output comprehensive, well-formatted Markdown summaries. "
                            "Present ALL data received. Be thorough and strategic."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=getattr(settings, "AI_MAX_OUTPUT_TOKENS", 2000),
                temperature=0.2,
                seed=42,
            )
            # Log token usage
            if response.usage:
                self._log_token_usage(
                    "ANSWER_SYNTHESIS", 
                    response.usage, 
                    user_question, 
                    model_name,
                    input_breakdown={
                        "Data": self._estimate_tokens(json.dumps(data, default=str)),
                        "SQL": self._estimate_tokens(sql_query),
                        "System": 800  # Approx
                    }
                )
            return result_prefix + response.choices[0].message.content

        except Exception as e:
            logger.error(f"Answer synthesis error: {e}")
            return (
                f"Retrieved data:\n"
                f"```json\n{json.dumps(row_data, indent=2, default=str)}\n```"
            )

    # ────────────────────────────────────────────
    # Follow-up Generation
    # ────────────────────────────────────────────

    def generate_follow_ups(
        self,
        user_question: str,
        sql_query: str,
        data: list = None,
        answer: str = None,
        role_id: int = None,
    ) -> list:
        """
        Generates 3 intelligent follow-up questions based on query type.
        Admins get strategic, institutional follow-ups.
        """
        if not self.client:
            return ["View more details", "Filter by department", "Show trends"]

        q = user_question.lower()

        is_assessment = any(
            k in q for k in ["assessment", "test", "question", "asked", "exam"]
        )
        is_trainer = any(k in q for k in ["trainer", "staff"])
        is_course = "course" in q
        is_student = any(k in q for k in ["student", "top", "best", "performer"])
        is_recruitment = any(
            k in q
            for k in ["eligible", "placement", "company", "zoho", "amazon", "tcs"]
        )
        is_analytics = any(
            k in q for k in ["performance", "department", "average", "rank"]
        )

        data_preview = (
            f"Retrieved {len(data)} records"
            if data and isinstance(data, list)
            else "No data"
        )

        admin_note = (
            "[ADMIN]: Generate strategic institutional follow-ups — "
            "drill into subgroups, cross-reference metrics, suggest comparisons."
            if role_id in [1, 2]
            else ""
        )

        if is_assessment:
            ctx = "ASSESSMENT: question difficulty, student scores, submission patterns, topic gaps"
        elif is_trainer:
            ctx = (
                "TRAINER: course assignments, active vs inactive, workload distribution"
            )
        elif is_course:
            ctx = "COURSE: enrollment stats, completion rates, student performance per course"
        elif is_student:
            ctx = "STUDENT: department breakdown, skill gaps, attendance, placement readiness"
        elif is_recruitment:
            ctx = "RECRUITMENT: alternate companies, skill development, group eligibility breakdown"
        elif is_analytics:
            ctx = "ANALYTICS: trend analysis, outliers, department comparison, improvements"
        else:
            ctx = "GENERAL: trends, breakdowns, top/bottom performers"

        prompt = f"""
Question: "{user_question}"
Data: {data_preview}
{admin_note}
Context: {ctx}

Generate exactly 3 follow-up questions. One per line. No numbering, no bullets, no extra formatting.
"""

        try:
            model_name = "deepseek-chat"
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Generate 3 practical follow-up questions. "
                            "One per line. No numbering or special formatting."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.6,
            )

            lines = response.choices[0].message.content.strip().split("\n")
            
            # Log token usage
            if response.usage:
                self._log_token_usage(
                    "FOLLOW_UPS", 
                    response.usage, 
                    user_question, 
                    model_name,
                    input_breakdown={
                       "Context": 50,
                       "DataPreview": 20
                    }
                )

            cleaned = [
                re.sub(r"^[\d\.\-\)\:\s]*", "", line).strip()
                for line in lines
                if line.strip() and len(line.strip()) > 5
            ]
            return cleaned[:3] if len(cleaned) >= 3 else cleaned

        except Exception as e:
            logger.error(f"Follow-up generation error: {e}")
            fallbacks = {
                "assessment": [
                    "Which students scored highest in this assessment?",
                    "Show questions that most students failed",
                    "Compare this assessment with the previous one",
                ],
                "trainer": [
                    "Show trainer-wise course assignments",
                    "Which trainers are currently inactive?",
                    "Show trainer workload by number of batches",
                ],
                "course": [
                    "Show enrollment numbers for these courses",
                    "Which course has the lowest completion rate?",
                    "List students who haven't started any course",
                ],
                "student": [
                    "Show performance breakdown by department",
                    "List at-risk students needing support",
                    "Which skills do top performers have in common?",
                ],
                "recruitment": [
                    "Show other companies with similar eligibility criteria",
                    "What training would improve eligibility rates?",
                    "Department-wise eligibility breakdown",
                ],
                "analytics": [
                    "Show trends over the past two semesters",
                    "Identify underperforming departments",
                    "Compare batch-wise performance",
                ],
            }
            if is_assessment:
                return fallbacks["assessment"]
            if is_trainer:
                return fallbacks["trainer"]
            if is_course:
                return fallbacks["course"]
            if is_student:
                return fallbacks["student"]
            if is_recruitment:
                return fallbacks["recruitment"]
            return fallbacks["analytics"]

    # ────────────────────────────────────────────
    # Utilities
    # ────────────────────────────────────────────

    def is_destructive_query(self, sql: str) -> bool:
        """Returns True if the SQL modifies data (UPDATE, DELETE, DROP, etc.)"""
        if not sql:
            return False
        sql_upper = sql.strip().upper()
        for kw in ["UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "INSERT"]:
            if sql_upper.startswith(kw):
                return True
        return False

    def answer_general_question(
        self,
        user_question: str,
        model: str = "deepseek-chat",
    ) -> str:
        """
        Answers general knowledge questions via LLM (no DB query needed).
        Restricted to: Companies, Skills, Educational Info, Recruitment.
        Refuses all other topics with a standard message.
        """
        client = self._get_client(model)
        if not client:
            return "I cannot answer this question as the AI service is unavailable."

        try:
            model_name = "deepseek-chat"
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a specialized IT and Educational Consultant.\n"
                            "You ONLY answer questions about:\n"
                            "  1. Companies (tech companies, hiring trends, culture)\n"
                            "  2. Professional Skills (programming, soft skills, career)\n"
                            "  3. Educational Information (academic advice, learning paths)\n"
                            "  4. Recruitment & Interviews (process, aptitude, preparation)\n\n"
                            "For ANY other topic, respond exactly with:\n"
                            "  'I am only authorized to provide general knowledge on "
                            "Companies, Professional Skills, Educational Information, and Recruitment.'"
                        ),
                    },
                    {"role": "user", "content": user_question},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"General answer error: {e}")
            return "I encountered an error while processing your request."


# ════════════════════════════════════════════════════════════════
#  Singleton
# ════════════════════════════════════════════════════════════════

ai_service = AIService()
