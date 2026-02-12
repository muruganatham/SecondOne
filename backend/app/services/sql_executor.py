"""
SQL Executor
Safely executes AI-generated SQL queries with table validation.
"""
from sqlalchemy import text
from app.core.db import SessionLocal
import re

class SQLExecutor:
    def __init__(self):
        self.existing_tables = None
        self._load_existing_tables()
        
    def _load_existing_tables(self):
        """Load list of tables that actually exist in the database"""
        db = SessionLocal()
        try:
            result = db.execute(text("SHOW TABLES"))
            self.existing_tables = set([row[0] for row in result.fetchall()])
            print(f"✅ Loaded {len(self.existing_tables)} existing tables from database")
        except Exception as e:
            print(f"⚠️ Warning: Could not load table list: {e}")
            self.existing_tables = set()
        finally:
            db.close()
    
    def refresh_tables(self):
        """Refresh the list of existing tables"""
        self._load_existing_tables()
        
    def extract_tables_from_sql(self, sql: str) -> set:
        """Extract table names from SQL query"""
        # Remove comments and normalize
        sql_clean = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
        sql_clean = re.sub(r'/\*.*?\*/', '', sql_clean, flags=re.DOTALL)
        sql_upper = sql_clean.upper()
        
        tables = set()
        
        # Pattern to match table names after FROM and JOIN
        patterns = [
            r'FROM\s+`?(\w+)`?',
            r'JOIN\s+`?(\w+)`?',
            r'INTO\s+`?(\w+)`?',
            r'UPDATE\s+`?(\w+)`?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, sql_upper)
            tables.update(matches)
        
        return tables
    
    def validate_tables(self, sql: str) -> dict:
        """
        Validate that all tables in the SQL exist in the database.
        Returns: {"valid": bool, "missing_tables": list, "message": str}
        """
        if not self.existing_tables:
            # If we couldn't load tables, skip validation
            return {"valid": True, "missing_tables": [], "message": "Table validation skipped"}
        
        sql_tables = self.extract_tables_from_sql(sql)
        
        # Convert existing tables to uppercase for comparison
        existing_upper = set([t.upper() for t in self.existing_tables])
        
        # Find missing tables
        missing = [t for t in sql_tables if t not in existing_upper]
        
        if missing:
            return {
                "valid": False,
                "missing_tables": missing,
                "message": f"Tables not found in database: {', '.join(missing)}"
            }
        
        return {"valid": True, "missing_tables": [], "message": "All tables exist"}
        
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
        Table validation is disabled - AI will always attempt to generate and execute SQL.
        """
        # Remove any markdown wrapping if present
        clean_sql = sql.replace("```sql", "").replace("```", "").strip()
        
        if not self.is_safe(clean_sql):
             return {"error": "Unsafe query detected. Only SELECT allowed."}
        
        # NOTE: Table validation is DISABLED per user request
        # The AI should always attempt to generate SQL, even if tables don't exist
        # This allows for better error messages and learning from failures
        
        # COMMENTED OUT: Pre-execution table validation
        # validation = self.validate_tables(clean_sql)
        # if not validation["valid"]:
        #     return {
        #         "error": f"Table validation failed: {validation['message']}",
        #         "missing_tables": validation["missing_tables"],
        #         "sql": clean_sql,
        #         "suggestion": "Please ask about tables that exist in the database, or ask 'What tables are available?'"
        #     }

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
            error_msg = str(e)
            
            # Enhanced error message with suggestions
            if "doesn't exist" in error_msg.lower():
                # Extract table name from error if possible
                import re
                table_match = re.search(r"Table '[\w.]+\.([\w_]+)' doesn't exist", error_msg)
                missing_table = table_match.group(1) if table_match else "unknown"
                
                return {
                    "error": f"Table '{missing_table}' doesn't exist in the database.",
                    "sql": clean_sql,
                    "suggestion": f"The AI generated SQL for a table that doesn't exist. This might be because:\n1. The table was removed or renamed\n2. The schema analysis is outdated\n3. The question refers to data not in this database\n\nTry asking: 'What tables are available?' or rephrase your question.",
                    "missing_table": missing_table
                }
            
            return {"error": error_msg, "sql": clean_sql}
        finally:
            db.close()
    
    def get_available_tables(self) -> list:
        """Return list of available tables"""
        return sorted(list(self.existing_tables)) if self.existing_tables else []

# Singleton
sql_executor = SQLExecutor()

