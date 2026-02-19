import sys
import os
sys.path.append(os.getcwd())
from app.core.db import SessionLocal
from sqlalchemy import text

def extract_fks():
    db = SessionLocal()
    query = """
    SELECT 
        TABLE_NAME, 
        COLUMN_NAME, 
        REFERENCED_TABLE_NAME, 
        REFERENCED_COLUMN_NAME 
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE REFERENCED_TABLE_NAME IS NOT NULL
    AND TABLE_SCHEMA = 'coderv4'
    """
    res = db.execute(text(query)).fetchall()
    with open("db_relations_audit.txt", "w") as f:
        f.write("DATABASE RELATIONSHIPS (FOREIGN KEYS):\n")
        f.write("="*40 + "\n")
        for r in res:
            f.write(f"{r[0]}.{r[1]} -> {r[2]}.{r[3]}\n")
    db.close()
    print("Success: Relations written to db_relations_audit.txt")

if __name__ == "__main__":
    extract_fks()
