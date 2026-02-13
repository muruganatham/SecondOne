import mysql.connector

def list_students_with_results():
    try:
        conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
        cursor = conn.cursor(dictionary=True)
        
        print("Students with Coding Results:")
        cursor.execute("""
            SELECT DISTINCT u.id, u.name, u.roll_no 
            FROM admin_coding_result r 
            JOIN users u ON r.user_id = u.id
        """)
        for row in cursor.fetchall():
            print(f"ID: {row['id']} | Name: {row['name']} | Roll: {row['roll_no']}")
            
        print("\nStudents with MCQ Results:")
        cursor.execute("""
            SELECT DISTINCT u.id, u.name, u.roll_no 
            FROM admin_mcq_result r 
            JOIN users u ON r.user_id = u.id
        """)
        for row in cursor.fetchall():
            print(f"ID: {row['id']} | Name: {row['name']} | Roll: {row['roll_no']}")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_students_with_results()
