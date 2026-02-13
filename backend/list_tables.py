import mysql.connector

def list_tables():
    conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    for row in cursor.fetchall():
        print(row[0])
    cursor.close()
    conn.close()

if __name__ == "__main__":
    list_tables()
