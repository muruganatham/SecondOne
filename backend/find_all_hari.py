import mysql.connector

def find_all_hari():
    try:
        conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, roll_no FROM users WHERE name LIKE '%hari%'")
        results = cursor.fetchall()
        print(f"Found {len(results)} matches:")
        for row in results:
            print(f"ID: {row['id']} | Name: {row['name']} | Roll: {row['roll_no']}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_all_hari()
