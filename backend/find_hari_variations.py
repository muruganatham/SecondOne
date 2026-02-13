import mysql.connector

def find_hari_variations():
    conn = mysql.connector.connect(host="localhost", port=3306, user="root", password="root", database="coderv4")
    cursor = conn.cursor(dictionary=True)
    
    variations = ["%hariharan%", "%hariharn%", "%hariha%", "%hari_haran%"]
    
    print("Searching for Hariharn variations...")
    for var in variations:
        cursor.execute("SELECT id, name, roll_no FROM users WHERE name LIKE %s", (var,))
        results = cursor.fetchall()
        if results:
            print(f"\nMatches for {var}:")
            for r in results:
                print(f"  ID: {r['id']} | Name: {r['name']} | Roll: {r['roll_no']}")
        else:
            print(f"\nNo matches for {var}")
            
    cursor.close()
    conn.close()

if __name__ == "__main__":
    find_hari_variations()
