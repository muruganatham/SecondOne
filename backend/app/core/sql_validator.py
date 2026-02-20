"""
SQL Validator - Production Grade
Validates and sanitizes SQL queries before execution
"""

import re
from typing import Dict, List, Tuple
from enum import Enum


class SQLQueryType(Enum):
    SELECT = "SELECT"
    SHOW = "SHOW"
    DESCRIBE = "DESCRIBE"
    INVALID = "INVALID"


class SQLValidator:
    """
    Validates SQL queries for syntax, safety, and correctness
    """

    # Forbidden keywords for read-only mode
    DESTRUCTIVE_KEYWORDS = {
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "RENAME",
        "REPLACE",
        "EXEC",
        "EXECUTE",
        "CALL",
    }

    # Patterns that indicate syntax issues
    COMMON_SYNTAX_ERRORS = {
        r"(?i)near\s+['\"]": "Syntax error near quoted string",
        r"(?i)line\s+\d+": "Syntax error at specific line",
        r"(?i)unexpected\s+EOF": "Unexpected end of query",
        r"(?i)missing\s+(?:FROM|WHERE|SELECT)": "Missing required clause",
    }

    @staticmethod
    def get_query_type(sql: str) -> SQLQueryType:
        """Determine the type of SQL query"""
        clean_sql = sql.strip().upper()

        if clean_sql.startswith("SELECT"):
            return SQLQueryType.SELECT
        elif clean_sql.startswith("SHOW"):
            return SQLQueryType.SHOW
        elif clean_sql.startswith("DESCRIBE") or clean_sql.startswith("DESC"):
            return SQLQueryType.DESCRIBE
        else:
            return SQLQueryType.INVALID

    @staticmethod
    def is_read_only(sql: str) -> bool:
        """Check if query is read-only (safe)"""
        sql_upper = sql.strip().upper()

        # Check for destructive keywords
        for keyword in SQLValidator.DESTRUCTIVE_KEYWORDS:
            if f" {keyword} " in f" {sql_upper} ":
                return False

        # Check if starts with allowed keywords
        for allowed in ["SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN", "WITH"]:
            if sql_upper.startswith(allowed):
                return True

        return False

    @staticmethod
    def extract_tables(sql: str) -> List[str]:
        """Extract table names from SQL query"""
        # Remove comments
        sql_clean = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
        sql_clean = re.sub(r"/\*.*?\*/", "", sql_clean, flags=re.DOTALL)

        tables = []

        # Pattern 1: FROM tablename
        from_matches = re.findall(
            r"\bFROM\s+`?([a-zA-Z0-9_]+)`?", sql_clean, re.IGNORECASE
        )
        tables.extend(from_matches)

        # Pattern 2: JOIN tablename
        join_matches = re.findall(
            r"\bJOIN\s+`?([a-zA-Z0-9_]+)`?", sql_clean, re.IGNORECASE
        )
        tables.extend(join_matches)

        # Return unique tables
        return list(set(tables))

    @staticmethod
    def detect_common_errors(sql: str) -> List[str]:
        """Detect common SQL syntax issues"""
        errors = []
        sql_upper = sql.upper()

        # Check for incomplete JSON functions
        if "JSON_EXTRACT" in sql_upper or "JSON_UNQUOTE" in sql_upper:
            json_pattern = (
                r'JSON_(?:EXTRACT|UNQUOTE)\s*\(\s*([^,]+),\s*[\'"]([^\'"]+)[\'"]\s*\)'
            )
            if not re.search(json_pattern, sql):
                errors.append("Potentially malformed JSON function syntax")

        # Check for missing closing parentheses
        if sql.count("(") != sql.count(")"):
            errors.append(
                f"Mismatched parentheses: {sql.count('(')} opening, {sql.count(')')} closing"
            )

        # Check for missing commas in SELECT list
        if "SELECT" in sql_upper:
            # This is a basic check - may have false positives
            select_part = re.search(r"SELECT\s+(.+?)\s+FROM", sql, re.IGNORECASE)
            if select_part:
                select_list = select_part.group(1)
                # Count keywords that should have commas between them
                if re.search(
                    r"\b(?:CASE|WHEN|THEN|ELSE|END)\b.*\b(?:CASE|WHEN|THEN)\b",
                    select_list,
                    re.IGNORECASE,
                ):
                    # This is likely complex CASE statement, harder to validate
                    pass

        # Check for NULL/NOT NULL in WHERE without comparison
        if re.search(r"\bWHERE\s+.*\w+\s+(?!IS|<|>|=|!)", sql, re.IGNORECASE):
            pass  # Complex validation, skip

        # Check for incomplete CAST
        # FIXED: handles DECIMAL(3,2), UNSIGNED, CHAR(10), etc.
        # FIND this (line ~85 in detect_common_errors):

# REPLACE WITH:
        if "CAST" in sql_upper:
            cast_pattern = r"CAST\s*\(.+?\s+AS\s+\w+"
            if not re.search(cast_pattern, sql, re.IGNORECASE):
                errors.append("Potentially malformed CAST() syntax")
        return errors

    @staticmethod
    def validate(sql: str) -> Dict:
        """
        Comprehensive SQL validation
        Returns: {
            "valid": bool,
            "query_type": str,
            "is_safe": bool,
            "errors": [],
            "warnings": [],
            "tables": [],
            "estimated_complexity": str
        }
        """
        sql_stripped = sql.strip()

        if not sql_stripped:
            return {
                "valid": False,
                "query_type": "INVALID",
                "is_safe": False,
                "errors": ["Empty query"],
                "warnings": [],
                "tables": [],
                "estimated_complexity": "N/A",
            }

        query_type = SQLValidator.get_query_type(sql_stripped)
        is_safe = SQLValidator.is_read_only(sql_stripped)
        tables = SQLValidator.extract_tables(sql_stripped)
        syntax_errors = SQLValidator.detect_common_errors(sql_stripped)

        warnings = []

        # Estimate complexity
        if len(tables) > 5:
            warnings.append("High table join count - may impact performance")
            complexity = "HIGH"
        elif len(tables) > 2:
            complexity = "MEDIUM"
        else:
            complexity = "LOW"

        # Check for large LIMIT values
        if re.search(r"\bLIMIT\s+(\d+)", sql_stripped, re.IGNORECASE):
            limit_match = re.search(r"\bLIMIT\s+(\d+)", sql_stripped, re.IGNORECASE)
            limit_val = int(limit_match.group(1))
            if limit_val > 10000:
                warnings.append(
                    f"Large LIMIT value ({limit_val}) - consider pagination"
                )

        return {
            "valid": query_type != SQLQueryType.INVALID
            and not syntax_errors
            and is_safe,
            "query_type": query_type.value,
            "is_safe": is_safe,
            "errors": syntax_errors if syntax_errors else [],
            "warnings": warnings,
            "tables": tables,
            "estimated_complexity": complexity,
        }
def _check_distinct_orderby(self, sql: str) -> list:
    """
    Detects SELECT DISTINCT queries where ORDER BY references
    expressions not in the SELECT list — causes MySQL error 3065.
    """
    errors = []
    sql_upper = sql.upper()

    if "SELECT DISTINCT" not in sql_upper:
        return errors

    # Find ORDER BY section
    order_idx = sql_upper.rfind("ORDER BY")
    if order_idx == -1:
        return errors

    order_clause = sql_upper[order_idx:]

    # These patterns in ORDER BY are dangerous after SELECT DISTINCT
    dangerous = [
        r"ORDER BY\s+CASE\s+WHEN",          # CASE block in ORDER BY
        r"ORDER BY.*JSON_EXTRACT",            # JSON call in ORDER BY
        r"ORDER BY.*JSON_UNQUOTE",            # JSON call in ORDER BY
        r"ORDER BY.*CAST\s*\(",               # CAST in ORDER BY
    ]

    for pattern in dangerous:
        if re.search(pattern, order_clause):
            errors.append(
                "SELECT DISTINCT with complex ORDER BY expression — "
                "move the expression into SELECT as a named alias, "
                "then ORDER BY that alias instead."
            )
            break

    return errors

# Global instance
sql_validator = SQLValidator()
