import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

output_file = "debug_db_info.txt"

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='coderv4'
    )
    cursor = conn.cursor()
    
    with open(output_file, "w") as f:
        f.write("--- DEBUG INFO ---\n\n")
        
        # Check specific conversation 3
        f.write("Checking Conversation ID 3:\n")
        cursor.execute("SELECT id, user_id, title FROM conversations WHERE id=3")
        conv3 = cursor.fetchone()
        if conv3:
            f.write(f"FOUND: ID={conv3[0]}, UserID={conv3[1]}, Title={conv3[2]}\n")
            
            # Check owner details
            cursor.execute(f"SELECT id, email FROM users WHERE id={conv3[1]}")
            owner = cursor.fetchone()
            if owner:
                f.write(f"OWNER: ID={owner[0]}, Email={owner[1]}\n")
            else:
                f.write(f"OWNER NOT FOUND for UserID {conv3[1]}\n")
        else:
            f.write("Conversation 3 NOT FOUND\n")
            
        # List all conversations
        f.write("\nAll Conversations:\n")
        cursor.execute("SELECT id, user_id, title FROM conversations")
        conversations = cursor.fetchall()
        for c in conversations:
            f.write(f"ID: {c[0]}, UserID: {c[1]}, Title: {c[2]}\n")
            
        # List all users
        f.write("\nAll Users:\n")
        cursor.execute("SELECT id, email FROM users")
        users = cursor.fetchall()
        for u in users:
            f.write(f"ID: {u[0]}, Email: {u[1]}\n")
            
    conn.close()
    print(f"Debug info written to {output_file}")
    
except Exception as e:
    print(f"Error: {e}")
