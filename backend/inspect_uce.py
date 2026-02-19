import sys
import os
sys.path.append(os.getcwd())
from app.core.db import SessionLocal
from sqlalchemy import text

def inspect_uce():
    db = SessionLocal()
    print("--- user_course_enrollments Table ---")
    columns = db.execute(text("DESCRIBE user_course_enrollments")).fetchall()
    for col in columns:
        print(f"Col: {col[0]}, Type: {col[1]}")
    db.close()

if __name__ == "__main__":
    inspect_uce()
