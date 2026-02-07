
import sys
import os
sys.path.append(os.getcwd())

from app.core.db import SessionLocal
from app.core.config import settings
from app.models.profile_models import Colleges, Batches, Departments, CollegeDepartmentMaps, CourseAcademicMaps, CollegeSectionMaps, Courses, UserAcademics, Users
from sqlalchemy import text


db = SessionLocal()

def check_college_data(name_part):
    print(f"--- Searching for college: {name_part} ---")
    college = db.query(Colleges).filter(Colleges.college_name.ilike(f"%{name_part}%")).first()
    if not college:
        print("College not found.")
        return

    print(f"Found College: {college.college_name} (ID: {college.id})")
    
    cid = college.id
    
    # Check Batches
    batches = db.query(Batches).filter(Batches.college_id == cid).all()
    print(f"Batches count: {len(batches)}")
    for b in batches[:5]:
        print(f" - {b.batch_name} (Status: {b.status})")

    # Check CollegeDepartmentMaps
    dept_maps = db.query(CollegeDepartmentMaps).filter(CollegeDepartmentMaps.college_id == cid).all()
    print(f"CollegeDepartmentMaps count: {len(dept_maps)}")
    
    # Check CourseAcademicMaps
    cam_query = db.query(CourseAcademicMaps).filter(CourseAcademicMaps.college_id == cid)
    cam_count = cam_query.count()
    print(f"CourseAcademicMaps count matching college_id: {cam_count}")
    
    if cam_count > 0:
        print("First 5 CourseAcademicMaps rows:")
        rows = cam_query.limit(5).all()
        for r in rows:
            print(f" - ID: {r.id}, DeptID: {r.department_id}, BatchID: {r.batch_id}, SectionID: {r.section_id}")
            
    if cam_count == 0:
        print("!! No CourseAcademicMaps found for this college via college_id column !!")
        
    # Check specific IDs found in CAM
    print("Checking specific IDs found in CAM (Dept: 50, Batch: 10)...")
    d50 = db.query(Departments).filter(Departments.id == "50").first()
    if d50:
        print(f"Found Dept 50: {d50.department_name}")
    else:
        print("!! Dept 50 NOT FOUND in Departments table !!")

    b10 = db.query(Batches).filter(Batches.id == "10").first()
    if b10:
        print(f"Found Batch 10: {b10.batch_name} (College: {b10.college_id})")
    # Introspect Batches
    print("Introspecting Batches Table...")
    try:
        res = db.execute(text("SELECT * FROM batches LIMIT 1"))
        print(f"Batches Columns: {res.keys()}")
    except Exception as e:
        print(f"Batches SELECT failed: {e}")

    # Introspect Sections 
    print("Introspecting Sections Table...")
    try:
        res = db.execute(text("SELECT * FROM sections LIMIT 1"))
        print(f"Sections Columns: {res.keys()}")
    except Exception as e:
        print(f"Sections SELECT failed: {e}")

    # Raw SQL Batches
    print("Checking Raw SQL Batches...")
    batches_query = text("""
        SELECT DISTINCT b.id, b.batch_name 
        FROM batches b
        JOIN course_academic_maps cam ON b.id = cam.batch_id
        WHERE cam.college_id = :college_id
    """)
    batches = db.execute(batches_query, {"college_id": cid}).fetchall()
    print(f"Raw SQL Batches count: {len(batches)}")
    for b in batches:
        print(f" - {b.batch_name} (ID: {b.id})")

    # Raw SQL Sections
    print("Checking Raw SQL Sections...")
    sections_query = text("""
        SELECT DISTINCT s.id, s.section 
        FROM sections s
        JOIN course_academic_maps cam ON s.id = cam.section_id
        WHERE cam.college_id = :college_id
    """)
    sections = db.execute(sections_query, {"college_id": cid}).fetchall()
    print(f"Raw SQL Sections count: {len(sections)}")
    for s in sections:
        print(f" - {s.section} (ID: {s.id})")

    # Check Courses Join
    print("Checking Courses JOIN...")
    courses = db.query(Courses).join(CourseAcademicMaps, Courses.id == CourseAcademicMaps.course_id)\
                .filter(CourseAcademicMaps.college_id == cid)\
                .distinct().all()
    print(f"Courses JOIN count: {len(courses)}")
    for c in courses[:5]:
        print(f" - {c.course_name} (ID: {c.id})")

if __name__ == "__main__":
    with open("debug_output_fixed.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        
        # Test the actual leaderboard query for MCET + Batch 8
        c_name = "Dr Mahalingam College of Engineering and Technology"
        print(f"Testing Leaderboard Query for {c_name} + Batch 8...")
        c = db.query(Colleges).filter(Colleges.college_name == c_name).first()
        
        if c:
            print(f"College ID: {c.id}, Code: {c.college_short_name}")
            
            # Simulate the leaderboard query
            college_id = c.id
            batch_id = "8"  # As string
            
            # Test the filter condition
            test_query = text("""
                SELECT COUNT(DISTINCT u.id) as user_count
                FROM users u
                JOIN user_academics ua ON u.id = ua.user_id
                WHERE ua.college_id = :college_id
                AND ua.batch_id = :batch_id
            """)
            result = db.execute(test_query, {"college_id": college_id, "batch_id": batch_id}).scalar()
            print(f"Users matching College {college_id} + Batch {batch_id}: {result}")
            
            # Check with results
            test_with_results = text("""
                SELECT COUNT(DISTINCT u.id)
                FROM mcet_2025_2_coding_result r
                JOIN users u ON r.user_id = u.id
                JOIN user_academics ua ON u.id = ua.user_id
                WHERE ua.college_id = :college_id
                AND ua.batch_id = :batch_id
            """)
            result2 = db.execute(test_with_results, {"college_id": college_id, "batch_id": batch_id}).scalar()
            print(f"Users with results for College {college_id} + Batch {batch_id}: {result2}")
            
            # Try as integer
            batch_id_int = 8
            result3 = db.execute(test_with_results, {"college_id": college_id, "batch_id": batch_id_int}).scalar()
            print(f"Users with results (batch as int): {result3}")
            
            # Check what type batch_id is in user_academics
            type_check = db.execute(text("SELECT batch_id FROM user_academics WHERE college_id = 8 LIMIT 1")).fetchone()
            print(f"Sample batch_id from DB: {type_check[0] if type_check else 'N/A'}, Type: {type(type_check[0]) if type_check else 'N/A'}")
        else:
            print("MCET not found")
