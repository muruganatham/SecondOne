from sqlalchemy import text
from app.core.db import engine

def add_columns():
    try:
        with engine.connect() as conn:
            # Using basic SQL that works on Postgres and SQLite for safety
            print("Adding stats_chat_count...")
            try:
                conn.execute(text("ALTER TABLE users ADD COLUMN stats_chat_count INTEGER DEFAULT 0"))
            except Exception as e:
                print(f"stats_chat_count might already exist: {e}")

            print("Adding stats_words_generated...")
            try:
                conn.execute(text("ALTER TABLE users ADD COLUMN stats_words_generated BIGINT DEFAULT 0"))
            except Exception as e:
                print(f"stats_words_generated might already exist: {e}")

            print("Adding active_streak...")
            try:
                conn.execute(text("ALTER TABLE users ADD COLUMN active_streak INTEGER DEFAULT 0"))
            except Exception as e:
                print(f"active_streak might already exist: {e}")
            
            print("Adding last_active_date...")
            try:
                conn.execute(text("ALTER TABLE users ADD COLUMN last_active_date TIMESTAMP"))
            except Exception as e:
                print(f"last_active_date might already exist: {e}")

            conn.commit()
            print("Schema update completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    add_columns()
