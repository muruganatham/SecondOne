"""
DB Inspector - Production Grade
Introspects table schemas to prevent runtime column-not-found errors.
Used before SQL execution to validate column references.
"""

from sqlalchemy import text
from app.core.db import SessionLocal
from app.core.logging_config import get_logger
import functools
import time

logger = get_logger("db_inspector")


class DBInspector:
    """
    Caches table column metadata so we can validate SQL before execution
    and build accurate prompts for the AI.
    """

    def __init__(self):
        self._column_cache: dict = {}   # { table_name: {col_name: col_type} }
        self._cache_ttl: int = 300      # 5 minutes
        self._cache_ts: dict = {}       # { table_name: timestamp }

    # ─────────────────────────────────────────────
    # Column Fetching
    # ─────────────────────────────────────────────

    def get_columns(self, table_name: str, force_refresh: bool = False) -> dict:
        """
        Returns { column_name: data_type } for the given table.
        Uses cache with TTL. Returns empty dict if table doesn't exist.
        """
        now = time.time()
        cached_ts = self._cache_ts.get(table_name, 0)

        if not force_refresh and table_name in self._column_cache:
            if (now - cached_ts) < self._cache_ttl:
                return self._column_cache[table_name]

        db = SessionLocal()
        try:
            result = db.execute(
                text("DESCRIBE `{}`".format(table_name))
            )
            columns = {}
            for row in result.fetchall():
                col_name = row[0]
                col_type = row[1]
                columns[col_name] = col_type

            self._column_cache[table_name] = columns
            self._cache_ts[table_name] = now

            logger.debug(f"Loaded {len(columns)} columns for table '{table_name}'")
            return columns

        except Exception as e:
            logger.warning(f"Could not describe table '{table_name}': {str(e)}")
            return {}
        finally:
            db.close()

    def table_has_column(self, table_name: str, column_name: str) -> bool:
        """Check if a specific column exists in a table."""
        cols = self.get_columns(table_name)
        return column_name in cols

    def get_available_columns(self, table_name: str) -> list:
        """Return sorted list of column names for a table."""
        return sorted(self.get_columns(table_name).keys())

    # ─────────────────────────────────────────────
    # Multi-table column resolver
    # ─────────────────────────────────────────────

    def resolve_score_columns(self, table_name: str) -> dict:
        """
        Inspects a college result table and returns the best available
        columns for: solved_count, total_score, and solve_status.

        Different tables use different column names across the codebase:
          - solved_count / solve_count / solved
          - total_coding_score / total_score / score / mark
          - solve_status / status

        Returns:
          {
            "solved_count": "solved_count" | "solve_count" | None,
            "total_score":  "total_coding_score" | "total_score" | "mark" | None,
            "solve_status": "solve_status" | "status" | None,
            "user_id":      "user_id" | "uid" | None,
          }
        """
        cols = self.get_columns(table_name)
        if not cols:
            return {
                "solved_count": None,
                "total_score": None,
                "solve_status": None,
                "user_id": None,
                "available_columns": [],
            }

        col_names = set(cols.keys())

        def pick(candidates):
            for c in candidates:
                if c in col_names:
                    return c
            return None

        result = {
            "solved_count": pick(["solved_count", "solve_count", "solved", "total_solved"]),
            "total_score":  pick(["total_coding_score", "total_score", "score", "mark", "total_mark"]),
            "solve_status": pick(["solve_status", "status", "submission_status"]),
            "user_id":      pick(["user_id", "uid", "student_id"]),
            "available_columns": sorted(col_names),
        }

        logger.info(
            f"Resolved columns for '{table_name}': "
            f"solved_count={result['solved_count']}, "
            f"total_score={result['total_score']}, "
            f"solve_status={result['solve_status']}"
        )
        return result

    # ─────────────────────────────────────────────
    # SQL Column Validator
    # ─────────────────────────────────────────────

    def validate_sql_columns(self, sql: str, table_column_map: dict) -> dict:
        """
        Cross-checks SQL column references against known table schemas.

        Args:
            sql: The SQL query string
            table_column_map: { "table_alias_or_name": ["col1", "col2", ...] }

        Returns:
            {
                "valid": bool,
                "missing_columns": [ {"table": ..., "column": ...} ],
                "message": str
            }
        """
        import re
        missing = []

        for alias, columns in table_column_map.items():
            for col in columns:
                # Check if alias.col appears in SQL
                pattern = rf'\b{re.escape(alias)}\.{re.escape(col)}\b'
                if re.search(pattern, sql, re.IGNORECASE):
                    if not any(col in c for c in self.get_columns(alias).keys()):
                        missing.append({"table": alias, "column": col})

        return {
            "valid": len(missing) == 0,
            "missing_columns": missing,
            "message": (
                "All columns valid"
                if not missing
                else f"Missing columns: {missing}"
            ),
        }

    def get_table_summary(self, table_name: str) -> str:
        """
        Returns a human-readable summary of a table's columns.
        Useful for injecting into AI prompts.
        """
        cols = self.get_columns(table_name)
        if not cols:
            return f"Table '{table_name}' not found or has no columns."

        lines = [f"Table: {table_name}"]
        for col, dtype in sorted(cols.items()):
            lines.append(f"  - {col} ({dtype})")
        return "\n".join(lines)


# Singleton
db_inspector = DBInspector()