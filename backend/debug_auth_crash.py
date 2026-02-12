import os
import sys
# Add current directory to path
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.profile_models import Users 

# Setup DB
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def debug():
    db = SessionLocal()
    email = "hariharan.2305032@srec.ac.in"
    
    # print(f"Checking user: {email}") # Commented out to reduce noise
    try:
        # Step 1: Raw SQL check for user columns
        print("Checking Users table columns via RAW SQL...")
        result = db.execute(text("SHOW COLUMNS FROM users"))
        columns = [row[0] for row in result]
        print(f"Columns in users table: {columns}")
        
        # Check required columns for auth model
        required = ['id', 'name', 'email', 'password', 'role', 'active_streak', 'last_active_date']
        missing = [col for col in required if col not in columns]
        if missing:
            print(f"CRITICAL: Missing columns in users table: {missing}")
        else:
            print("All required columns present in users table.")
            
        # Step 2: ORM Query
        print("Attempting ORM query for user...")
        # Catch ORM query exception specifically
        try:
            user = db.query(Users).filter(Users.email == email).first()
            
            if not user:
                print("User not found via ORM.")
            else:
                print(f"User found: ID={user.id}, Role={user.role}")
                print(f"Streak: {user.active_streak}")
                print(f"Last Active: {user.last_active_date}")
        except Exception as query_exc:
            print(f"Query Exception: {query_exc}")
            raise query_exc
            
    except Exception as e:
        print(f"Overall Exception: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    with open('debug_output_utf8.txt', 'w', encoding='utf-8') as f:
        sys.stdout = f
        sys.stderr = f
        debug()
