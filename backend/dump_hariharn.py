import mysql.connector

def dump_hariharn():
    conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
    cursor = conn.cursor(dictionary=True)
    
    # Find user
    cursor.execute("SELECT id, full_name FROM users WHERE full_name LIKE '%hariharn%'")
    users = cursor.fetchall()
    
    if not users:
        print("No student found")
        return

    for u in users:
        uid = u['id']
        print(f"User: {u['full_name']} (ID: {uid})")
        
        # Check first record in coding results
        cursor.execute("SELECT * FROM admin_coding_result WHERE user_id = %s LIMIT 1", (uid,))
        res = cursor.fetchone()
        if res:
            print(f"Sample Coding Record: {res}")
            # Get course name via simple direct query if possible
            if 'course_id' in res:
                cursor.execute("SELECT course_name FROM courses WHERE id = %s", (res['course_id'],))
                cname = cursor.fetchone()
                print(f"Course Name: {cname}")
        else:
            print("No coding records.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    dump_hariharn()
