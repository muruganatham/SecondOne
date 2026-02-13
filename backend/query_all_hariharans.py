import mysql.connector

def query_all_hariharans():
    try:
        conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
        cursor = conn.cursor(dictionary=True)
        
        hari_ids = [164, 541, 754, 895, 1560, 1561, 1935, 2368, 2420, 3011, 3645, 3728, 4096, 4536, 5038, 5341, 5342, 5679, 5992, 6125, 6405, 1813, 1560, 1561]
        
        # Remove duplicates
        hari_ids = list(set(hari_ids))
        
        print(f"Checking {len(hari_ids)} students for results...")
        
        for uid in hari_ids:
            # Check User details
            cursor.execute("SELECT name, roll_no FROM users WHERE id = %s", (uid,))
            u = cursor.fetchone()
            if not u: continue
            
            # Check if has results in coding
            cursor.execute("SELECT COUNT(*) as count FROM admin_coding_result WHERE user_id = %s", (uid,))
            coding_count = cursor.fetchone()['count']
            
            # Check if has results in mcq
            cursor.execute("SELECT COUNT(*) as count FROM admin_mcq_result WHERE user_id = %s", (uid,))
            mcq_count = cursor.fetchone()['count']
            
            if coding_count > 0 or mcq_count > 0:
                print(f"Found Results for {u['name']} (ID: {uid}, Roll: {u['roll_no']})")
                print(f"  - Coding Records: {coding_count}")
                print(f"  - MCQ Records: {mcq_count}")
                
                # Fetch detailed coding results
                cursor.execute("""
                    SELECT c.course_name, r.mark, r.solve_status 
                    FROM admin_coding_result r 
                    JOIN course_academic_maps cam ON r.course_allocation_id = cam.id
                    JOIN courses c ON cam.course_id = c.id
                    WHERE r.user_id = %s
                """, (uid,))
                for row in cursor.fetchall():
                    status = "Solved" if row['solve_status'] == 2 else ("Partial" if row['solve_status'] == 1 else "Unsolved")
                    print(f"    - [Coding] {row['course_name']}: {row['mark']} Marks ({status})")

                # Fetch detailed mcq results
                cursor.execute("""
                    SELECT c.course_name, r.mark, r.solve_status 
                    FROM admin_mcq_result r 
                    JOIN course_academic_maps cam ON r.course_allocation_id = cam.id
                    JOIN courses c ON cam.course_id = c.id
                    WHERE r.user_id = %s
                """, (uid,))
                for row in cursor.fetchall():
                    status = "Solved" if row['solve_status'] == 2 else ("Partial" if row['solve_status'] == 1 else "Unsolved")
                    print(f"    - [MCQ] {row['course_name']}: {row['mark']} Marks ({status})")
                print("-" * 50)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query_all_hariharans()
