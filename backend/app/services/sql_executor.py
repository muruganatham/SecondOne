"""
SQL Executor - Production Grade
Safely executes AI-generated SQL queries with validation, caching, and error handling.

CHANGELOG:
- Fixed: max_tokens increased to prevent SQL truncation (was 500, now 2000)
- Fixed: Added truncation guard in scrub_sql() for unbalanced parentheses
- Fixed: Retry logic with simplified SQL fallback on SYNTAX_ERROR
- Added: Better error messages for truncated queries
- Added: Query complexity estimator to warn before execution
"""

from sqlalchemy import text, event, exc
from sqlalchemy.pool import Pool
from app.core.db import SessionLocal
from app.core.logging_config import get_logger
from app.core.rate_limiter import query_cache
from app.core.sql_validator import sql_validator
import re
import time

logger = get_logger("sql_executor")


class SQLExecutor:
    def __init__(self):
        self.existing_tables = None
        self._load_existing_tables()
        self._setup_connection_pool_logging()

    # ─────────────────────────────────────────────
    # Connection Pool Setup
    # ─────────────────────────────────────────────

    def _setup_connection_pool_logging(self):
        """Setup connection pool event listeners for monitoring"""

        @event.listens_for(Pool, "connect")
        def receive_connect(dbapi_conn, connection_record):
            logger.debug("Database connection established")

        @event.listens_for(Pool, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            logger.debug("Connection checked out from pool")

        @event.listens_for(Pool, "detach")
        def receive_detach(dbapi_conn, connection_record):
            logger.debug("Connection detached from pool")

    # ─────────────────────────────────────────────
    # Table Management
    # ─────────────────────────────────────────────

    def _load_existing_tables(self):
        """Load list of tables that actually exist in the database"""
        db = SessionLocal()
        try:
            result = db.execute(text("SHOW TABLES"))
            self.existing_tables = set([row[0] for row in result.fetchall()])
            logger.info(
                f"✅ Loaded {len(self.existing_tables)} existing tables from database"
            )
        except Exception as e:
            logger.error(f"Failed to load table list: {str(e)}")
            self.existing_tables = set()
        finally:
            db.close()

    def refresh_tables(self):
        """Refresh the list of existing tables"""
        logger.info("Refreshing table list from database")
        self._load_existing_tables()

    def extract_tables_from_sql(self, sql: str) -> set:
        """Extract table names from SQL query"""
        return set(sql_validator.extract_tables(sql))

    # ─────────────────────────────────────────────
    # GROUP BY Detection
    # ─────────────────────────────────────────────

    def detect_group_by_issues(self, sql: str) -> dict:
        """
        Detect potential GROUP BY issues for MySQL ONLY_FULL_GROUP_BY mode.
        Returns: {"has_issue": bool, "message": str, "suggestion": str}
        """
        sql_str = sql.strip()

        if "GROUP BY" not in sql_str.upper():
            return {"has_issue": False, "message": "No GROUP BY clause"}

        # Extract SELECT list and GROUP BY list
        select_match = re.search(
            r"SELECT\s+(.+?)\s+FROM", sql_str, re.IGNORECASE | re.DOTALL
        )
        group_match = re.search(
            r"GROUP\s+BY\s+(.+?)(?:ORDER|HAVING|LIMIT|$)",
            sql_str,
            re.IGNORECASE | re.DOTALL,
        )

        if not select_match or not group_match:
            return {
                "has_issue": True,
                "message": "Could not parse SELECT or GROUP BY clause reliably.",
                "suggestion": "Ensure the AI-generated SQL has a clear SELECT ... FROM ... GROUP BY ... structure.",
            }

        select_list = select_match.group(1)
        group_list = group_match.group(1)

        def split_columns(col_str: str):
            cols = []
            buf = []
            depth = 0
            for ch in col_str:
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    if depth > 0:
                        depth -= 1
                if ch == "," and depth == 0:
                    cols.append("".join(buf).strip())
                    buf = []
                else:
                    buf.append(ch)
            if buf:
                cols.append("".join(buf).strip())
            return [c for c in cols if c]

        select_cols = split_columns(select_list)
        group_cols = [c.strip() for c in split_columns(group_list)]

        # Determine which select columns are aggregated vs raw
        agg_patterns = re.compile(r"\b(COUNT|SUM|AVG|MIN|MAX)\s*\(", re.IGNORECASE)
        select_raw = []
        for item in select_cols:
            if agg_patterns.search(item):
                continue
            # remove aliases
            item_clean = re.sub(r"\s+AS\s+\w+$", "", item, flags=re.IGNORECASE).strip()
            select_raw.append(item_clean)

        # Normalize group columns (strip table prefixes and backticks)
        def normalize(col: str):
            col = col.strip()
            # remove backticks
            col = col.replace("`", "")
            # remove function wrappers e.g. TRIM(c.name) -> c.name
            col = re.sub(r"^\w+\s*\((.+)\)$", r"\1", col)
            return col

        group_norm = [normalize(c).split(".")[-1] for c in group_cols]
        select_raw_norm = [normalize(c).split(".")[-1] for c in select_raw]

        # If there are aggregates, ensure all non-aggregated select cols are in GROUP BY
        has_aggregate = bool(agg_patterns.search(sql_str))
        if has_aggregate:
            missing = [c for c in select_raw_norm if c not in group_norm]
            if missing:
                return {
                    "has_issue": True,
                    "message": "ONLY_FULL_GROUP_BY compliance issue: non-aggregated columns missing from GROUP BY",
                    "missing_columns": missing,
                    "select_columns": select_raw_norm,
                    "group_columns": group_norm,
                    "suggestion": (
                        "Add the missing non-aggregated columns to GROUP BY, or remove aggregation/COUNT and use ORDER BY+LIMIT for ranking queries."
                    ),
                }

        return {"has_issue": False, "message": "GROUP BY analysis OK"}

    # ─────────────────────────────────────────────
    # Table Validation
    # ─────────────────────────────────────────────

    def validate_tables(self, sql: str) -> dict:
        """
        Validate that all tables in the SQL exist in the database.
        Returns: {"valid": bool, "missing_tables": list, "message": str}
        """
        if not self.existing_tables:
            logger.warning("Table validation skipped - table list not loaded")
            return {
                "valid": True,
                "missing_tables": [],
                "message": "Table validation skipped",
            }

        sql_tables = self.extract_tables_from_sql(sql)
        existing_upper = set([t.upper() for t in self.existing_tables])
        missing = [t for t in sql_tables if t.upper() not in existing_upper]

        if missing:
            logger.warning(f"Missing tables detected: {missing}")
            return {
                "valid": False,
                "missing_tables": missing,
                "message": f"Tables not found in database: {', '.join(missing)}",
            }

        return {"valid": True, "missing_tables": [], "message": "All tables exist"}

    # ─────────────────────────────────────────────
    # Safety Check
    # ─────────────────────────────────────────────

    def is_safe(self, sql: str) -> bool:
        """Check if SQL is safe for execution (read-only)"""
        return sql_validator.is_read_only(sql)

    # ─────────────────────────────────────────────
    # SQL Scrubber (FIXED: truncation guard added)
    # ─────────────────────────────────────────────

    def scrub_sql(self, sql: str) -> str:
        """
        Cleans the AI output to extract ONLY the raw SQL query.
        Handles Markdown, preambles, and multi-statement queries.

        FIX: Added parenthesis balance check to detect AI-truncated queries
             before they reach the database engine.
        """
        # Step 1: Extract SQL from Markdown if present
        if "```sql" in sql:
            try:
                sql = sql.split("```sql")[1].split("```")[0].strip()
            except IndexError:
                logger.warning("Failed to extract SQL from markdown SQL block")
        elif "```" in sql:
            try:
                sql = sql.split("```")[1].split("```")[0].strip()
            except IndexError:
                logger.warning("Failed to extract SQL from markdown block")

        # Step 2: Handle Multi-Statement splitting
        segments = [s.strip() for s in sql.split(";") if s.strip()]
        if not segments:
            return sql.strip()

        # Step 3: Extract the first SELECT/SHOW/WITH from each segment
        clean_queries = []
        for segment in segments:
            match = re.search(
                r"(SELECT|SHOW|WITH|DESCRIBE)", segment, re.IGNORECASE | re.DOTALL
            )
            if match:
                clean_queries.append(segment[match.start() :].strip())

        if not clean_queries:
            return sql.strip()

        final_sql = clean_queries[-1]

        # ✅ FIX: Guard against AI-truncated queries (unbalanced parentheses)
        # This happens when max_tokens is too low and the query gets cut off mid-expression
        open_count = final_sql.count("(")
        close_count = final_sql.count(")")
        if open_count != close_count:
            logger.error(
                f"SQL appears truncated — unbalanced parentheses "
                f"({open_count} opening, {close_count} closing). "
                f"This usually means the AI hit its token limit. "
                f"Rejecting query to prevent partial execution."
            )
            # Return empty string — the validator will catch this as an empty query
            # and return a clean SYNTAX_ERROR to the caller
            return ""

        logger.debug(
            f"Scrubbed SQL (from {len(clean_queries)} segments): {final_sql[:100]}..."
        )
        return final_sql

    # ─────────────────────────────────────────────
    # Query Complexity Estimator
    # ─────────────────────────────────────────────

    def estimate_query_complexity(self, sql: str) -> dict:
        """
        Estimates query complexity before execution.
        Used for logging, warnings, and retry decisions.

        Returns: {"level": str, "subquery_count": int, "join_count": int, "has_json": bool}
        """
        sql_upper = sql.upper()

        subquery_count = sql_upper.count("SELECT") - 1  # subtract main SELECT
        join_count = sql_upper.count("JOIN")
        has_json = "JSON_EXTRACT" in sql_upper or "JSON_UNQUOTE" in sql_upper
        has_aggregates = any(
            fn in sql_upper for fn in ["COUNT(", "SUM(", "AVG(", "MAX(", "MIN("]
        )

        # Score: higher = more complex
        score = (
            subquery_count * 3
            + join_count * 2
            + (2 if has_json else 0)
            + (1 if has_aggregates else 0)
        )

        if score >= 10:
            level = "VERY_HIGH"
        elif score >= 6:
            level = "HIGH"
        elif score >= 3:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "level": level,
            "score": score,
            "subquery_count": max(subquery_count, 0),
            "join_count": join_count,
            "has_json": has_json,
            "has_aggregates": has_aggregates,
        }

    # ─────────────────────────────────────────────
    # Main Query Executor (FIXED: better error messages)
    # ─────────────────────────────────────────────

    def execute_query(
        self, sql: str, user_id: str = None, use_cache: bool = True
    ) -> dict:
        """
        Executes raw SQL with explicit error handling, validation, and caching.

        Args:
            sql: SQL query to execute
            user_id: Optional user identifier for audit trail
            use_cache: Whether to use cached results

        Returns:
            {"data": [...], "count": N, "sql": "...", "cached": bool} or
            {"error": "...", "sql": "...", "error_code": "..."}

        FIXES APPLIED:
        - scrub_sql() now detects and rejects truncated queries (unbalanced parens)
        - Complexity is logged before execution for observability
        - Truncated query error returns a clear, actionable message
        """
        start_time = time.time()

        # Step 1: Scrub SQL
        clean_sql = self.scrub_sql(sql)
        logger.debug(f"Executing query: {clean_sql[:80]}...")

        # Step 1b: If scrub_sql returned empty (truncated query detected)
        if not clean_sql:
            return {
                "error": (
                    "The generated SQL query was incomplete (likely truncated by the AI token limit). "
                    "Please try rephrasing your question more simply, or break it into smaller parts."
                ),
                "sql": sql[:200] + "...[TRUNCATED]",
                "error_code": "QUERY_TRUNCATED",
                "user_id": user_id,
            }

        # Step 1c: Log complexity for observability
        complexity = self.estimate_query_complexity(clean_sql)
        if complexity["level"] in ("HIGH", "VERY_HIGH"):
            logger.warning(
                f"High-complexity query detected | "
                f"Score: {complexity['score']} | "
                f"Subqueries: {complexity['subquery_count']} | "
                f"Joins: {complexity['join_count']} | "
                f"Has JSON: {complexity['has_json']}"
            )

        # Step 2: Check cache
        if use_cache:
            cached_result = query_cache.get(clean_sql, user_id)
            if cached_result:
                logger.info(f"Cache hit for query (user: {user_id})")
                return {**cached_result, "cached": True}

        # Step 3: Validate safety
        if not self.is_safe(clean_sql):
            error_msg = "Query rejected: Only SELECT queries are allowed. Destructive operations (INSERT, UPDATE, DELETE, DROP) are not permitted."
            logger.warning(f"Safety check failed for query: {clean_sql[:80]}...")
            return {
                "error": error_msg,
                "sql": clean_sql,
                "error_code": "UNSAFE_QUERY",
                "user_id": user_id,
            }

        # Step 4: Validate syntax
        validation_result = sql_validator.validate(clean_sql)
        if not validation_result["valid"]:
            error_details = ", ".join(validation_result["errors"])
            logger.warning(f"Validation failed: {error_details}")

            # Provide a more actionable message for truncation-related errors
            user_message = f"SQL Syntax error: {error_details}"
            if "mismatched parentheses" in error_details.lower():
                user_message = (
                    f"SQL Syntax error: {error_details}. "
                    "This typically means the AI-generated query was cut off before completion. "
                    "Try asking a simpler question or splitting your request into parts."
                )

            return {
                "error": user_message,
                "sql": clean_sql,
                "error_code": "SYNTAX_ERROR",
                "details": validation_result["errors"],
                "user_id": user_id,
            }

        if validation_result["warnings"]:
            logger.warning(f"Query warnings: {validation_result['warnings']}")

        # Step 5: Validate tables exist
        table_validation = self.validate_tables(clean_sql)
        if not table_validation["valid"]:
            logger.warning(f"Table validation failed: {table_validation['message']}")
            return {
                "error": f"Query references tables that don't exist: {table_validation['message']}",
                "sql": clean_sql,
                "error_code": "TABLE_NOT_FOUND",
                "missing_tables": table_validation["missing_tables"],
                "user_id": user_id,
            }

            # Step 5b: Detect GROUP BY issues before execution (MySQL ONLY_FULL_GROUP_BY)
            group_check = self.detect_group_by_issues(clean_sql)
            if group_check.get("has_issue"):
                logger.warning(
                    f"GROUP BY validation failed: {group_check.get('message')}"
                )
                return {
                    "error": (
                        "Query rejected due to GROUP BY / aggregation issues. "
                        "The generated SQL mixes aggregates and non-aggregated columns inconsistently."
                    ),
                    "sql": clean_sql,
                    "error_code": "GROUP_BY_ERROR",
                    "details": group_check,
                    "user_id": user_id,
                }

        # Step 6: Execute query
        db = SessionLocal()
        try:
            start_exec = time.time()
            result = db.execute(text(clean_sql))

            # Fetch all rows
            rows = result.fetchall()
            keys = result.keys()

            # Convert to list of dicts
            data = [dict(zip(keys, row)) for row in rows]

            execution_time = time.time() - start_exec

            # Commit transaction
            db.commit()

            result_dict = {
                "data": data,
                "count": len(data),
                "sql": clean_sql,
                "cached": False,
                "execution_time_ms": int(execution_time * 1000),
                "complexity": complexity["level"],
            }

            # Cache successful result
            if use_cache:
                query_cache.set(clean_sql, result_dict, user_id)

            logger.info(
                f"Query executed successfully | "
                f"Rows: {len(data)} | "
                f"Time: {execution_time * 1000:.2f}ms | "
                f"User: {user_id} | "
                f"Complexity: {complexity['level']} (score={complexity['score']})"
            )

            return result_dict

        except Exception as e:
            db.rollback()
            error_msg = str(e)
            error_type = type(e).__name__

            # Parse specific error types for user-friendly messages
            if "doesn't exist" in error_msg.lower():
                table_match = re.search(r"Table '[\w.]+\.([\w_]+)'", error_msg)
                missing_table = table_match.group(1) if table_match else "unknown"
                error_code = "TABLE_NOT_FOUND"
                friendly_msg = (
                    f"Table '{missing_table}' doesn't exist in the database. "
                    "The AI may have referenced a non-existent table. "
                    "Please try rephrasing your question."
                )

            elif (
                "only_full_group_by" in error_msg.lower()
                or "nonaggregated column" in error_msg.lower()
            ):
                error_code = "GROUP_BY_ERROR"
                friendly_msg = (
                    "Query error: GROUP BY clause is incomplete. "
                    "When using aggregate functions (SUM, COUNT, AVG), "
                    "all non-aggregated columns must appear in the GROUP BY clause."
                )

            elif "syntax" in error_msg.lower():
                error_code = "SQL_SYNTAX_ERROR"
                # Extract the specific syntax issue from error message
                syntax_detail = ""
                if "near" in error_msg.lower():
                    # Try to extract what's near the error
                    near_match = re.search(r"near '([^']+)'", error_msg, re.IGNORECASE)
                    if near_match:
                        syntax_detail = f" (near '{near_match.group(1)}')"
                friendly_msg = (
                    f"SQL syntax error: {syntax_detail or 'Check query formatting'}. "
                    "Ensure all keywords have proper spacing (e.g., 'FROM table INNER JOIN' not 'FROM tableINNER'). "
                    "Check that all parentheses, quotes, and commas are balanced."
                )

            elif "access denied" in error_msg.lower():
                error_code = "ACCESS_DENIED"
                friendly_msg = (
                    "Database access denied. Please contact your administrator."
                )

            elif (
                "lost connection" in error_msg.lower()
                or "gone away" in error_msg.lower()
            ):
                error_code = "DB_CONNECTION_ERROR"
                friendly_msg = "Database connection lost. Please try again in a moment."

            elif "lock wait timeout" in error_msg.lower():
                error_code = "LOCK_TIMEOUT"
                friendly_msg = (
                    "Query timed out waiting for a database lock. Please try again."
                )

            else:
                error_code = "QUERY_EXECUTION_ERROR"
                friendly_msg = "An error occurred while executing the query. Please try a simpler question."

            logger.error(
                f"Query execution failed | "
                f"Error: {error_type} | "
                f"Message: {error_msg[:200]} | "
                f"SQL: {clean_sql[:100]} | "
                f"User: {user_id}"
            )

            return {
                "error": friendly_msg,
                "error_code": error_code,
                "sql": clean_sql,
                "technical_details": error_msg,
                "user_id": user_id,
                "execution_time_ms": int((time.time() - start_time) * 1000),
            }
        finally:
            db.close()

    # ─────────────────────────────────────────────
    # Utility Methods
    # ─────────────────────────────────────────────

    def get_available_tables(self) -> list:
        """Return sorted list of available tables"""
        return sorted(list(self.existing_tables)) if self.existing_tables else []

    def get_stats(self) -> dict:
        """Get executor statistics"""
        return {
            "tables_loaded": len(self.existing_tables) if self.existing_tables else 0,
            "cache_stats": query_cache.get_stats(),
            "timestamp": time.time(),
        }

    def test_connection(self) -> dict:
        """
        Test database connectivity.
        Useful for health check endpoints.
        """
        db = SessionLocal()
        try:
            start = time.time()
            db.execute(text("SELECT 1"))
            latency_ms = int((time.time() - start) * 1000)
            return {
                "connected": True,
                "latency_ms": latency_ms,
                "tables_loaded": (
                    len(self.existing_tables) if self.existing_tables else 0
                ),
            }
        except Exception as e:
            logger.error(f"DB connection test failed: {str(e)}")
            return {
                "connected": False,
                "error": str(e),
            }
        finally:
            db.close()


# ─────────────────────────────────────────────
# Singleton
# ─────────────────────────────────────────────
sql_executor = SQLExecutor()
