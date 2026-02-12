from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.db import get_db
from app.core.security import get_current_user, RoleChecker
from app.models.profile_models import Users, UserAcademics, Colleges, Departments
from app.core.config import settings

router = APIRouter()

@router.post("/analytics/leaderboard")
async def get_leaderboard(
    filter_data: dict,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get Leaderboard Data with weighted scoring.
    Filters: college_id (mandatory), department_id, batch_id, section_id, course_id.
    Logic: Aggregate marks from college-specific result tables.
    """
    college_id = filter_data.get("college_id")
    department_id = filter_data.get("department_id")
    batch_id = filter_data.get("batch_id") 
    section_id = filter_data.get("section_id")
    course_id = filter_data.get("course_id")
    category = filter_data.get("category", "all") # 'mcq', 'coding', or 'all'
    
    # DEBUG: Log incoming filter data
    with open("leaderboard_request_log.txt", "a", encoding="utf-8") as f:
        import json
        f.write(f"\n=== New Request ===\n")
        f.write(f"User: {current_user.id}, Role: {current_user.role}\n")
        f.write(f"Filters: {json.dumps(filter_data, indent=2)}\n")
    
    # Role-based limit: Students see top 10 + their rank, Admins see all
    if current_user.role == 7:  # Student
        limit = 10
    else:  # Admin (Role 2) or Super Admin (Role 1)
        limit = 999999  # Effectively show all results

    if not college_id:
        # Default to current user's college
        user_academic = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        if user_academic and user_academic.college_id:
            college_id = user_academic.college_id
        else:
             raise HTTPException(status_code=400, detail="College ID is required")

    # 1. Get College Short Name for Table Lookup
    college = db.query(Colleges).filter(Colleges.id == college_id).first()
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    
    college_code = str(college.college_short_name).lower()

    # Security: Ensure Student can only view their own college
    if current_user.role == 7:
        user_acad = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        if user_acad and user_acad.college_id != int(college_id):
            raise HTTPException(status_code=403, detail="Access denied to other college leaderboard")

    # 2. Identify Result Tables
    # We look for tables starting with college_code and ending with _coding_result or _mcq_result
    semesters = ["2025_1", "2025_2", "2026_1", "2026_2"]
    
    tables_to_query = []
    
    for sem in semesters:
        current_tables = []
        if category in ["all", "coding"]:
            current_tables.append(f"{college_code}_{sem}_coding_result")
        if category in ["all", "mcq"]:
            current_tables.append(f"{college_code}_{sem}_mcq_result")
        
        tables_to_query.extend(current_tables)

    # 3. Build the Big Aggregation Query
    # We need to UNION ALL these tables, then join with users and user_academics for filtering.
    
    union_parts = []
    for table in tables_to_query:
        # We check if table exists by trying to select from it. 
        # In SQL, we can't easily check existence inside a query without dynamic SQL or stored procs.
        # Better: Query information_schema.tables
        check_sql = text(f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '{settings.DB_NAME}' AND table_name = '{table}'")
        result = db.execute(check_sql).scalar()
        if result > 0:
            # Check for course_allocation_id column to enable course-specific filtering
            check_col_sql = text(f"SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = '{settings.DB_NAME}' AND table_name = '{table}' AND column_name = 'course_allocation_id'")
            has_course_col = db.execute(check_col_sql).scalar() > 0
            
            # Pre-aggregate in the UNION to reduce rows for the main sort
            col_select = "course_allocation_id" if has_course_col else "NULL"
            group_by = "GROUP BY user_id, course_allocation_id" if has_course_col else "GROUP BY user_id"
            
            union_parts.append(f"""
                SELECT 
                    user_id, 
                    SUM(mark) as sub_mark, 
                    COUNT(*) as sub_attempts,
                    SUM(CASE WHEN solve_status = 2 THEN 1 ELSE 0 END) as sub_solved,
                    {col_select} as course_allocation_id
                FROM {table}
                WHERE status = 1
                {group_by}
            """)

    if not union_parts:
         return [] # No data found for this college

    union_query = " UNION ALL ".join(union_parts)

    # Main Query using Window Functions for Ranking
    # 1. user_stats: Aggregate raw data from pre-aggregated subqueries
    # 2. scored_stats: Calculate WPI Score
    
    filters = []
    params = {"college_id": college_id, "limit": limit}
    
    # Base College Filter
    filters.append("ua.college_id = :college_id")
    
    if department_id:
        filters.append("ua.department_id = :department_id")
        params["department_id"] = department_id
        
    if current_user.role != 7:
        if batch_id:
            filters.append("ua.batch_id = :batch_id")
            params["batch_id"] = batch_id
            
        if section_id:
            filters.append("ua.section_id = :section_id")
            params["section_id"] = section_id

    # Course Filtering Logic
    # Note: course_allocation_id in result tables may be unreliable/corrupted
    # Instead, we filter by ensuring users are enrolled in the selected course
    if course_id:
        if current_user.role == 7:
            # Verify student is enrolled
            student_segment = db.execute(
                text("SELECT batch_id FROM course_wise_segregations WHERE user_id = :uid AND course_id = :cid LIMIT 1"), 
                {"uid": current_user.id, "cid": course_id}
            ).fetchone()
            
            if not student_segment:
                raise HTTPException(status_code=403, detail="You are not enrolled in this course")

        # Filter to only show users enrolled in this specific course
        # We do this by checking if user_id exists in course_wise_segregations for this course
        params["course_id"] = course_id
        filters.append("u.id IN (SELECT user_id FROM course_wise_segregations WHERE course_id = :course_id)")

    where_clause = " AND ".join(filters)
    
    params["current_user_id"] = current_user.id

    final_sql = f"""
    WITH combined_results AS (
        {union_query}
    ),
    user_stats AS (
        SELECT 
            u.id as user_id,
            u.name as student_name,
            SUM(sub_mark) as total_marks,
            SUM(sub_attempts) as total_attempts,
            SUM(sub_solved) as solved_count,
            (SUM(sub_solved) * 100.0 / NULLIF(SUM(sub_attempts), 0)) as accuracy
        FROM combined_results
        JOIN users u ON combined_results.user_id = u.id
        JOIN user_academics ua ON u.id = ua.user_id
        WHERE {where_clause}
        GROUP BY u.id, u.name
    ),
    scored_stats AS (
        SELECT 
            *,
            (total_marks * 0.7) + (COALESCE(accuracy, 0) * 0.2) + (total_attempts * 0.1) as wpi_score
        FROM user_stats
    ),
    ranked_stats AS (
        SELECT 
            *,
            ROW_NUMBER() OVER (ORDER BY wpi_score DESC, total_marks DESC) as student_rank
        FROM scored_stats
    )
    SELECT * FROM ranked_stats
    WHERE student_rank <= :limit OR user_id = :current_user_id
    ORDER BY student_rank ASC
    """
    
    try:
        result = db.execute(text(final_sql), params).fetchall()
        
        leaderboard = []
        for row in result:
            leaderboard.append({
                "rank": row.student_rank,
                "student_name": row.student_name,
                "is_current_user": row.user_id == current_user.id,
                "avatar_seed": row.student_name,
                "metrics": {
                    "score": round(row.wpi_score, 2),
                    "total_marks": row.total_marks,
                    "questions_attended": row.total_attempts,
                    "accuracy": f"{round(row.accuracy or 0, 1)}%"
                }
            })
            
        return leaderboard
        
    except Exception as e:
        print(f"Leaderboard Query Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/leaderboard/courses")
async def get_college_courses(
    college_id: int = None,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    """
    Get list of courses available in a college.
    """
    
    if not college_id:
         # Default to current user's college
        user_academic = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        if user_academic and user_academic.college_id:
            college_id = user_academic.college_id
        else:
             raise HTTPException(status_code=400, detail="College ID is required and could not be determined from user profile")

    # Enforce same college for students and filter by enrolled courses
    if current_user.role == 7: # Student
        user_academic = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        if not user_academic or user_academic.college_id != college_id:
             raise HTTPException(status_code=403, detail="Access denied to other college data")

        # Students only see courses they are enrolled in
        query = text("""
            SELECT DISTINCT c.id, c.course_name AS title 
            FROM courses c
            JOIN course_wise_segregations cws ON c.id = cws.course_id 
            WHERE cws.college_id = :college_id
            AND cws.user_id = :user_id
            ORDER BY c.course_name ASC
        """)
        params = {"college_id": college_id, "user_id": current_user.id}

    else:
        # Admins see all courses in the college (via Course Academic Maps)
        query = text("""
            SELECT DISTINCT c.id, c.course_name AS title 
            FROM courses c
            JOIN course_academic_maps cam ON c.id = cam.course_id 
            WHERE cam.college_id = :college_id
            ORDER BY c.course_name ASC
        """)
        # Ensure college_id is int
        params = {"college_id": int(college_id)}

    try:
        result = db.execute(query, params).fetchall()
        
        courses = []
        for row in result:
            courses.append({
                "id": row.id,
                "title": row.title
            })
            
        return courses
        
    except Exception as e:
        print(f"Error fetching courses: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/leaderboard/colleges")
def get_leaderboard_colleges(
    db: Session = Depends(get_db),
    current_user: Users = Depends(RoleChecker([1, 2]))
):
         
    # Exclude dummy/test colleges
    colleges = db.query(Colleges).filter(Colleges.college_name.notin_(['skcet', 'skct'])).all()
    return [{"id": c.id, "name": c.college_name} for c in colleges]

from app.models.profile_models import Batches, Sections, CourseAcademicMaps, CollegeSectionMaps, Courses, CollegeDepartmentMaps

@router.get("/analytics/leaderboard/metadata")
def get_leaderboard_metadata(
    college_id: int = None,
    db: Session = Depends(get_db),
    current_user: Users = Depends(RoleChecker([1, 2]))
):
    with open("debug_log.txt", "a") as f:
        f.write(f"Metadata Request: college_id={college_id}, Role={current_user.role}\n")
    if not college_id:
        user_acad = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        if user_acad and user_acad.college_id:
            college_id = user_acad.college_id
        else:
             if current_user.role == 1:
                 return {"departments": [], "batches": [], "sections": []}
             raise HTTPException(status_code=400, detail="College ID required")

    # Verify access
    if current_user.role == 2:
        user_acad = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        # Ensure college_id is int for comparison
        if user_acad and user_acad.college_id != int(college_id):
             raise HTTPException(status_code=403, detail="Access denied to other college")

    # Filter metadata using Raw SQL to bypass ORM mapping ambiguities
    # Departments
    deps_query = text("""
        SELECT DISTINCT d.id, d.department_name 
        FROM departments d
        JOIN course_academic_maps cam ON d.id = cam.department_id
        WHERE cam.college_id = :college_id
    """)
    deps = db.execute(deps_query, {"college_id": college_id}).fetchall()
             
    # Batches - Only show batches that have actual students enrolled
    batches_query = text("""
        SELECT DISTINCT b.id, b.batch_name 
        FROM batches b
        JOIN user_academics ua ON b.id = ua.batch_id
        WHERE ua.college_id = :college_id
        ORDER BY b.batch_name DESC
    """)
    batches = db.execute(batches_query, {"college_id": college_id}).fetchall()
    
    # Sections
    sections_query = text("""
        SELECT DISTINCT s.id, s.section_name 
        FROM sections s
        JOIN course_academic_maps cam ON s.id = cam.section_id
        WHERE cam.college_id = :college_id
    """)
    sections = db.execute(sections_query, {"college_id": college_id}).fetchall()
    
    return {
        "departments": [{"id": row.id, "name": row.department_name} for row in deps], 
        "batches": [{"id": row.id, "name": row.batch_name} for row in batches],
        "sections": [{"id": row.id, "name": row.section_name} for row in sections]
    }

@router.get("/analytics/leaderboard/courses")
def get_leaderboard_courses(
    college_id: int = None,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    if not college_id:
        if current_user.role == 1:
            return [] # SuperAdmin needs to select college first
            
        user_acad = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
        if user_acad and user_acad.college_id:
            college_id = user_acad.college_id
        else:
            raise HTTPException(status_code=400, detail="College ID required")

    # Fetch courses for this college
    courses = db.query(Courses).join(CourseAcademicMaps, Courses.id == CourseAcademicMaps.course_id)\
                .filter(CourseAcademicMaps.college_id == college_id)\
                .distinct().all()
    
    return [{"id": c.id, "title": c.course_name} for c in courses]
