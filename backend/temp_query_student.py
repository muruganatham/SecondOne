from app.core.db import engine
from sqlalchemy import text

def query_student(name):
    with engine.connect() as connection:
        user_res = connection.execute(text("SELECT id, full_name, roll_no FROM users WHERE full_name LIKE :name OR name LIKE :name"), {"name": f"%{name}%"})
        users = user_res.fetchall()
        
        if not users:
            print(f"No student found matching: {name}")
            return

        for u in users:
            uid, fname, roll = u
            print(f"Found: {fname} (ID: {uid}, Roll: {roll})")
            print("-" * 50)
            
            # Coding Results
            coding_res = connection.execute(text("""
                SELECT c.course_name, r.mark, r.solve_status 
                FROM admin_coding_result r 
                JOIN courses c ON r.course_id = c.id 
                WHERE r.user_id = :uid
            """), {"uid": uid}).fetchall()
            
            print("  [Coding Results]")
            if not coding_res:
                print("    - None found")
            else:
                for r in coding_res:
                    status = "Solved" if r[2] == 2 else ("Partial" if r[2] == 1 else "Unsolved")
                    print(f"    - {r[0]}: {r[1]} Marks | Status: {status}")
            
            # MCQ Results
            mcq_res = connection.execute(text("""
                SELECT c.course_name, r.mark, r.solve_status 
                FROM admin_mcq_result r 
                JOIN courses c ON r.course_id = c.id 
                WHERE r.user_id = :uid
            """), {"uid": uid}).fetchall()
            
            print("\n  [MCQ Results]")
            if not mcq_res:
                print("    - None found")
            else:
                for r in mcq_res:
                    status = "Solved" if r[2] == 2 else ("Partial" if r[2] == 1 else "Unsolved")
                    print(f"    - {r[0]}: {r[1]} Marks | Status: {status}")
            print("=" * 60)

if __name__ == "__main__":
    query_student("hariharn")
