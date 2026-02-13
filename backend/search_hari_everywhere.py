import mysql.connector

def search_everywhere():
    conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
    cursor = conn.cursor(dictionary=True)
    
    # 1. Get all Hari-like IDs
    cursor.execute("SELECT id, name FROM users WHERE name LIKE '%Harihara%' OR name LIKE '%Hariha%'")
    users = cursor.fetchall()
    user_ids = [u['id'] for u in users]
    user_map = {u['id']: u['name'] for u in users}
    
    if not user_ids:
        print("No users found matching Harihara/Hariha")
        return

    # 2. Get all result tables
    cursor.execute("SHOW TABLES LIKE '%result%'")
    tables = [row['Tables_in_coderv4 (%result%)'] for row in cursor.fetchall()]
    
    print(f"Searching across {len(tables)} tables for {len(user_ids)} users...")
    
    found_any = False
    for table in tables:
        # Check if user_id column exists
        cursor.execute(f"SHOW COLUMNS FROM {table} LIKE 'user_id'")
        if not cursor.fetchone(): continue
        
        # Search in this table
        query = f"SELECT user_id, COUNT(*) as count FROM {table} WHERE user_id IN ({','.join(map(str, user_ids))}) GROUP BY user_id"
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            found_any = True
            print(f"\n[Table: {table}]")
            for r in results:
                uid = r['user_id']
                print(f"  User: {user_map[uid]} (ID: {uid}) | Records: {r['count']}")

    if not found_any:
        print("\nNo results found for any variation of Hariharn in any result table.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    search_everywhere()
