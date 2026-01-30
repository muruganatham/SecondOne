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
    
    print("🚀 Creating conversations table with correct schema...")
    
    # Drop table if exists (to recreate with correct schema)
    cursor.execute("DROP TABLE IF EXISTS conversations")
    
    # Create table with BIGINT UNSIGNED to match users.id
    create_sql = """
    CREATE TABLE conversations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id BIGINT UNSIGNED NOT NULL,
        title VARCHAR(255) NOT NULL,
        messages JSON NOT NULL,
        message_count INT DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        INDEX idx_user_id (user_id),
        INDEX idx_updated_at (updated_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    
    cursor.execute(create_sql)
    conn.commit()
    print("✅ Table created successfully!")
    
    # Verify
    cursor.execute("DESCRIBE conversations")
    columns = cursor.fetchall()
    print("\n📋 Table Structure:")
    for col in columns:
        print(f"   {col[0]}: {col[1]}")
    
    conn.close()
    print("\n🎉 Migration completed!")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
