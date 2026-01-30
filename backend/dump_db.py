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
    
    # Get all conversations
    cursor.execute("SELECT id, user_id, title FROM conversations")
    conversations = cursor.fetchall()
    
    # Get all users
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    
    print("--- CONVERSATIONS ---")
    for c in conversations:
        print(f"ID: {c[0]}, UserID: {c[1]}, Title: {c[2]}")
        
    print("\n--- USERS ---")
    for u in users:
        print(f"ID: {u[0]}, Username: {u[1]}, Email: {u[2]}")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
