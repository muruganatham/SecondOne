from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.profile_models import Users
import sys

# Setup DB connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Role ID':<10}")
    print("-" * 70)
    users = db.query(Users).all()
    for user in users:
        print(f"{str(user.id):<5} {user.name[:18]:<20} {user.email[:28]:<30} {user.role:<10}")
        
    print("\nReminder: SUPER_ADMIN Role ID is 1")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
