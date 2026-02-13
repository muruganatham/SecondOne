import mysql.connector

def find_hari():
    conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, roll_no FROM users WHERE name LIKE '%hari%'")
    for row in cursor.fetchall():
        print(f"ID: {row['id']} | Name: {row['name']} | Roll: {row['roll_no']}")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    find_hari()
