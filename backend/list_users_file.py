from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.profile_models import Users

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

with open("users_list.txt", "w") as f:
    admins = db.query(Users).filter(Users.role == 1).all()
    if not admins:
        f.write("NO_SUPER_ADMINS\n")
    else:
        for u in admins:
            f.write(f"SUPER_ADMIN: {u.email}\n")
    
    f.write("\nALL_USERS:\n")
    users = db.query(Users).all()
    for u in users:
        f.write(f"{u.email} (Role: {u.role})\n")
