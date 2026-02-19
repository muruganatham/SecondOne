import sys
import os
sys.path.append(os.getcwd())
from app.core.db import SessionLocal
from sqlalchemy import text

def inspect_uce():
    db = SessionLocal()
    with open("uce_columns.txt", "w") as f:
        columns = db.execute(text("DESCRIBE user_course_enrollments")).fetchall()
        for col in columns:
            f.write(f"Col: {col[0]}, Type: {col[1]}\n")
    db.close()

if __name__ == "__main__":
    inspect_uce()
