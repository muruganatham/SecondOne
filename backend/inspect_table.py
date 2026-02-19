import sys
import os
sys.path.append(os.getcwd())
from app.core.db import SessionLocal
from sqlalchemy import text

def inspect_table():
    db = SessionLocal()
    print("--- course_academic_maps Table ---")
    columns = db.execute(text("DESCRIBE course_academic_maps")).fetchall()
    column_names = [col[0] for col in columns]
    print(f"Columns: {', '.join(column_names)}")
    
    print("\n--- Sample Data (Hierarchical Match for User 35) ---")
    # User 35: College=4, Dept=3, Batch=4, Section=3
    data = db.execute(text("""
        SELECT * FROM course_academic_maps 
        WHERE college_id = 4 AND department_id = 3 AND batch_id = 4 AND section_id = 3 
        LIMIT 2
    """)).fetchall()
    for row in data:
        print(row)
    
    db.close()

if __name__ == "__main__":
    inspect_table()
