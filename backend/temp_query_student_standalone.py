import mysql.connector
import os

def query_student(name):
    try:
        # DB connection using details from .env (found earlier)
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="coderv4"
        )
        cursor = conn.cursor(dictionary=True)

        # 1. Find User
        query = "SELECT id, full_name, roll_no FROM users WHERE full_name LIKE %s OR name LIKE %s"
        cursor.execute(query, (f"%{name}%", f"%{name}%"))
        users = cursor.fetchall()

        if not users:
            print(f"No student found matching: {name}")
            return

        for u in users:
            uid = u['id']
            print(f"Found: {u['full_name']} (ID: {uid}, Roll: {u['roll_no']})")
            print("-" * 50)

            # 2. Coding Results
            cursor.execute("""
                SELECT c.course_name, r.mark, r.solve_status 
                FROM admin_coding_result r 
                JOIN courses c ON r.course_id = c.id 
                WHERE r.user_id = %s
            """, (uid,))
            coding_res = cursor.fetchall()
            
            print("  [Coding Results]")
            if not coding_res:
                print("    - None found")
            else:
                for r in coding_res:
                    status = "Solved" if r['solve_status'] == 2 else ("Partial" if r['solve_status'] == 1 else "Unsolved")
                    print(f"    - {r['course_name']}: {r['mark']} Marks | Status: {status}")

            # 3. MCQ Results
            cursor.execute("""
                SELECT c.course_name, r.mark, r.solve_status 
                FROM admin_mcq_result r 
                JOIN courses c ON r.course_id = c.id 
                WHERE r.user_id = %s
            """, (uid,))
            mcq_res = cursor.fetchall()
            
            print("\n  [MCQ Results]")
            if not mcq_res:
                print("    - None found")
            else:
                for r in mcq_res:
                    status = "Solved" if r['solve_status'] == 2 else ("Partial" if r['solve_status'] == 1 else "Unsolved")
                    print(f"    - {r['course_name']}: {r['mark']} Marks | Status: {status}")
            print("=" * 60)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    query_student("hariharn")
