"""
SQL Executor
Safely executes AI-generated SQL queries.
"""
from sqlalchemy import text
from app.core.db import SessionLocal
import re

class SQLExecutor:
    def __init__(self):
        pass
        
    def is_safe(self, sql: str) -> bool:
        """
        Basic safety check to prevent destructive queries.
        """
        sql_upper = sql.upper()
        forbidden = ["DROP ", "DELETE ", "UPDATE ", "INSERT ", "ALTER ", "TRUNCATE ", "CREATE "]
        for word in forbidden:
            if word in sql_upper:
                return False
        return True

    def execute_query(self, sql: str):
        """
        Executes raw SQL and returns dict results.
        """
        # Remove any markdown wrapping if present
        clean_sql = sql.replace("```sql", "").replace("```", "").strip()
        
        if not self.is_safe(clean_sql):
             return {"error": "Unsafe query detected. Only SELECT allowed."}

        db = SessionLocal()
        try:
            result = db.execute(text(clean_sql))
            
            # Fetch all rows
            rows = result.fetchall()
            
            # Get column names
            keys = result.keys()
            
            # Form list of dicts
            data = [dict(zip(keys, row)) for row in rows]
            
            return {"data": data, "count": len(data), "sql": clean_sql}
            
        except Exception as e:
            return {"error": str(e), "sql": clean_sql}
        finally:
            db.close()

# Singleton
sql_executor = SQLExecutor()
