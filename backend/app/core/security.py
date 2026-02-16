import bcrypt
from datetime import datetime, timedelta
from typing import Optional, List, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.db import get_db
from app.models.profile_models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token") # Removed
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Handle PHP/Laravel $2y$ bcrypt format by converting to $2b$
        if hashed_password and hashed_password.startswith('$2y$'):
            hashed_password = hashed_password.replace('$2y$', '$2b$', 1)
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback for plain text passwords in dev/legacy
        return plain_password == str(hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(api_key_header), db: Session = Depends(get_db)) -> Users:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
            headers={"WWW-Authenticate": "x-api-key"},
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "x-api-key"},
    )
    
    # Support Master API Key for internal access
    master_key = getattr(settings, "MASTER_BEARER_TOKEN", None)
    static_token = getattr(settings, "FRONTEND_BEARER_TOKEN", None)
    
    if master_key and token == master_key:
        # Fetch the first admin user as a mock for master key access
        user = db.query(Users).filter(Users.role == 1).first()
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Master key active but no admin user found",
        )
    
    # Support Frontend Static Token
    if static_token and token == static_token:
        # Return a mock user object representing the static app
        # This user is "trusted" and will have its persona overridden in the endpoint
        return Users(
            id="0",
            email="static-frontend@app.local",
            name="Static Frontend App",
            role=1, # Default to Admin role for the app itself
            # Note: other fields like 'status' are omitted if not in model or not needed
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

class RoleChecker:
    def __init__(self, allowed_roles: List[int]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: Users = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough permissions to perform this action"
            )
        return current_user
