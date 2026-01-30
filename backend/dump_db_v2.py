import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='coderv4'
    )
    cursor = conn.cursor()
    
    # Get specific conversation
    print("--- CHECKING ID 3 ---")
    cursor.execute("SELECT id, user_id, title FROM conversations WHERE id=3")
    conv3 = cursor.fetchone()
    if conv3:
        print(f"Conversation 3 FOUND: ID={conv3[0]}, UserID={conv3[1]}, Title={conv3[2]}")
    else:
        print("Conversation 3 NOT FOUND")

    # Get all conversations (limit 10)
    print("\n--- ALL CONVERSATIONS (Top 10) ---")
    cursor.execute("SELECT id, user_id, title FROM conversations ORDER BY id DESC LIMIT 10")
    conversations = cursor.fetchall()
    for c in conversations:
        print(f"ID: {c[0]}, UserID: {c[1]}, Title: {c[2]}")
        
    # Get all users
    cursor.execute("SELECT id, full_name, email FROM users")
    users = cursor.fetchall()
    
    print("\n--- USERS ---")
    for u in users:
        print(f"ID: {u[0]}, Name: {u[1]}, Email: {u[2]}")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
