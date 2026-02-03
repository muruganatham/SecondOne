import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.profile_models import Users
from app.models.enums import UsersRole

def promote_user(email):
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        user = db.query(Users).filter(Users.email == email).first()
        if not user:
            print(f"Error: User with email '{email}' not found.")
            return

        print(f"Current Role for {email}: {user.role}")
        user.role = 1  # Super Admin ID
        db.commit()
        print(f"Success! {email} is now a Super Admin (Role 1).")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python promote_user.py <email>")
    else:
        promote_user(sys.argv[1])
