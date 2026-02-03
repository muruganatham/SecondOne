from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.profile_models import Users

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

print("\n--- SUPER ADMINS (Role=1) ---")
admins = db.query(Users).filter(Users.role == 1).all()
if not admins:
    print("NO Super Admins found!")
else:
    for u in admins:
        print(f"Email: {u.email} | Name: {u.name}")

print("\n--- ALL USERS SAMPLE ---")
users = db.query(Users).limit(5).all()
for u in users:
    print(f"Email: {u.email} | Role: {u.role}")
