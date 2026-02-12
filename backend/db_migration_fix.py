import os
import sys
# Add current directory to path
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, text
from app.core.config import settings

# Setup DB
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

def migrate():
    print("Starting migration to add missing columns to users table...")
    with engine.connect() as conn:
        # Check if columns exist first to avoid duplicate column error?
        # Or just use try-except for each ALTER command.
        
        commands = [
            "ALTER TABLE users ADD COLUMN stats_chat_count INT DEFAULT 0",
            "ALTER TABLE users ADD COLUMN stats_words_generated BIGINT DEFAULT 0",
            "ALTER TABLE users ADD COLUMN active_streak INT DEFAULT 0",
            "ALTER TABLE users ADD COLUMN last_active_date DATETIME NULL"
        ]
        
        for cmd in commands:
            try:
                print(f"Executing: {cmd}")
                conn.execute(text(cmd))
                print("Success.")
            except Exception as e:
                # 1060 = Duplicate column name
                if "Duplicate column name" in str(e) or "1060" in str(e):
                    print("Column already exists. Skipping.")
                else:
                    print(f"Error executing {cmd}: {e}")
                    
        conn.commit() # Commit changes
        print("Migration complete.")

if __name__ == "__main__":
    migrate()
