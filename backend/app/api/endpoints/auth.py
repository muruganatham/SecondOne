from datetime import timedelta, datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.db import get_db
# Import core models from the comprehensive models file
from app.models.profile_models import Users, UserAcademics, Colleges, Departments
import app.models.enums as Enums
from app.core.config import settings
from app.schemas.user import Token, UserLogin, UserResponse

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def verify_password(plain_password, hashed_password):
    # In a real scenario, use verify. For now assuming bcrypt.
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback if hash format is different or plain
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Users).filter(Users.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Query using the Users model
    user = db.query(Users).filter(Users.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Streak Logic
    now = datetime.utcnow()
    today = now.date()
    
    if user.last_active_date:
        last_date = user.last_active_date.date()
        diff = (today - last_date).days
        
        if diff == 1:
            # Consecutive day, increment streak
            user.active_streak = (user.active_streak or 0) + 1
        elif diff > 1:
            # Broken streak, reset to 1
            user.active_streak = 1
        # If diff == 0, same day, do nothing (keep current streak)
    else:
        # First time login or no history
        user.active_streak = 1
        
    user.last_active_date = now
    db.commit()
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    # 1. Fetch UserAcademics to get IDs
    user_academic = db.query(UserAcademics).filter(UserAcademics.user_id == current_user.id).first()
    
    college_name = "N/A"
    department_name = "N/A"
    
    if user_academic:
        # 2. Fetch College Name
        if user_academic.college_id:
            college = db.query(Colleges).filter(Colleges.id == user_academic.college_id).first()
            if college:
                college_name = college.college_name
                # Handle Enum if it comes back as one, but usually String column
        
        # 3. Fetch Department Name
        if user_academic.department_id:
            dept = db.query(Departments).filter(Departments.id == user_academic.department_id).first()
            if dept:
                department_name = dept.department_name
    
    # 4. Map Role
    # role is an Enum in DB. get_label returns string like "student"
    role_str = "Unknown"
    try:
        role_enum_val = current_user.role
        # Check if it's already an int or Enum object
        if hasattr(role_enum_val, 'value'):
             role_label = Enums.UsersRole.get_label(role_enum_val.value)
        else:
             role_label = Enums.UsersRole.get_label(role_enum_val)
        
        role_str = role_label.title() # "Student"
    except Exception as e:
        print(f"Role mapping error: {e}")
        role_str = str(current_user.role)

    return UserResponse(
        id=str(current_user.id),
        name=current_user.name,
        email=current_user.email,
        roll_no=current_user.roll_no,
        role=role_str,
        college=college_name,
        department=department_name,
        stats_chat_count=current_user.stats_chat_count,
        stats_words_generated=current_user.stats_words_generated,
        active_streak=current_user.active_streak
    )
