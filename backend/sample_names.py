import mysql.connector

def sample_names():
    conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE role = 7 LIMIT 20")
    for row in cursor.fetchall():
        print(row[0])
    cursor.close()
    conn.close()

if __name__ == "__main__":
    sample_names()
