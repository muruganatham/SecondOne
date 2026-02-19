import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from app.core.db import SessionLocal
from sqlalchemy import text

def check_enrollments():
    user_id = 35
    print(f"--- Checking enrollments for User ID: {user_id} ---")
    db = SessionLocal()
    
    # 1. Check user_academics
    academics = db.execute(text("SELECT college_id, department_id, batch_id, section_id FROM user_academics WHERE user_id = :user_id"), {"user_id": user_id}).fetchone()
    if academics:
        college_id, dept_id, batch_id, section_id = academics
        print(f"Hierarchy IDs: College={college_id}, Dept={dept_id}, Batch={batch_id}, Section={section_id}")
    else:
        print("No academic record found for User 35")
        db.close()
        return

    # 2. Check user_course_enrollments (Direct)
    direct_enrollments = db.execute(text("SELECT COUNT(*) FROM user_course_enrollments WHERE user_id = :user_id"), {"user_id": user_id}).scalar()
    print(f"Count in user_course_enrollments: {direct_enrollments}")

    # 3. Check course_academic_maps (Allocated via Hierarchy)
    allocated_count = db.execute(text("""
        SELECT COUNT(*) 
        FROM course_academic_maps 
        WHERE college_id = :college_id 
        AND department_id = :dept_id 
        AND batch_id = :batch_id 
        AND section_id = :section_id
    """), {
        "college_id": college_id,
        "dept_id": dept_id,
        "batch_id": batch_id,
        "section_id": section_id
    }).scalar()
    print(f"Count in course_academic_maps: {allocated_count}")
    
    # 5. Inspect course_academic_maps schema
    print("\n--- Schema for course_academic_maps ---")
    columns = db.execute(text("DESCRIBE course_academic_maps")).fetchall()
    for col in columns:
        print(f"Col: {col[0]}, Type: {col[1]}")

    db.close()

if __name__ == "__main__":
    check_enrollments()
