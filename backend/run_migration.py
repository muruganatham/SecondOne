"""
Run SQL Migration to Create Conversations Table
"""
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection details from .env
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME = os.getenv('DB_NAME', 'coderv4')

# SQL to create conversations table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    messages JSON NOT NULL,
    message_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

def run_migration():
    """Run the migration to create conversations table"""
    try:
        # Connect to MySQL
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        print(f"✅ Connected to database: {DB_NAME}")
        
        with connection.cursor() as cursor:
            # Execute the CREATE TABLE statement
            cursor.execute(CREATE_TABLE_SQL)
            connection.commit()
            print("✅ Conversations table created successfully!")
            
            # Verify table was created
            cursor.execute("SHOW TABLES LIKE 'conversations'")
            result = cursor.fetchone()
            if result:
                print(f"✅ Verified: Table 'conversations' exists in database '{DB_NAME}'")
                
                # Show table structure
                cursor.execute("DESCRIBE conversations")
                columns = cursor.fetchall()
                print("\n📋 Table Structure:")
                for col in columns:
                    print(f"   - {col[0]}: {col[1]}")
            else:
                print("❌ Table verification failed")
        
        connection.close()
        print("\n🎉 Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting SQL Migration...")
    print("=" * 60)
    run_migration()
    print("=" * 60)
