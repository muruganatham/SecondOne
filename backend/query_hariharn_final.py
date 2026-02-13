import mysql.connector

def query_hariharn():
    try:
        conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
        cursor = conn.cursor(dictionary=True)
        
        # 1. Find user (Using 'name' instead of 'full_name')
        cursor.execute("SELECT id, name, roll_no FROM users WHERE name LIKE '%hariharn%'")
        users = cursor.fetchall()
        
        if not users:
            print("No student found with name 'hariharn'")
            return

        for u in users:
            uid = u['id']
            print(f"Found User: {u['name']} (ID: {uid}, Roll: {u['roll_no']})")
            print("-" * 50)
            
            # 2. Get Coding Results
            # Based on previous DESC, columns were: id, user_id, allocate_id, course_allocation_id, topic_test_id, topic_type, module_id, question_id, solve_status, status, created_at, etc.
            cursor.execute("""
                SELECT c.course_name, r.mark, r.solve_status, r.created_at
                FROM admin_coding_result r
                JOIN course_academic_maps cam ON r.course_allocation_id = cam.id
                JOIN courses c ON cam.course_id = c.id
                WHERE r.user_id = %s
            """, (uid,))
            coding = cursor.fetchall()
            
            print("  [Coding Results]")
            if not coding:
                print("    - No records found")
            else:
                for row in coding:
                    print(f"    - {row['course_name']}: {row['mark']} Marks | Status: {row['solve_status']} | Date: {row['created_at']}")
            
            # 3. Get MCQ Results
            cursor.execute("""
                SELECT c.course_name, r.mark, r.solve_status, r.created_at
                FROM admin_mcq_result r
                JOIN course_academic_maps cam ON r.course_allocation_id = cam.id
                JOIN courses c ON cam.course_id = c.id
                WHERE r.user_id = %s
            """, (uid,))
            mcq = cursor.fetchall()
            
            print("\n  [MCQ Results]")
            if not mcq:
                print("    - No records found")
            else:
                for row in mcq:
                    print(f"    - {row['course_name']}: {row['mark']} Marks | Status: {row['solve_status']} | Date: {row['created_at']}")
            print("=" * 60)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query_hariharn()
