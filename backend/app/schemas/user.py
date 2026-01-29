from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: str  # Users.id is String in models.py
    name: str
    email: EmailStr
    roll_no: Optional[str] = None
    role: str
    college: str
    department: str
    
    # Analytics
    stats_chat_count: int = 0
    stats_words_generated: int = 0
    active_streak: int = 0
    
    class Config:
        from_attributes = True
