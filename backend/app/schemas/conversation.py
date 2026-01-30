from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    sender: str
    text: str
    sql: Optional[str] = None
    data: Optional[List] = None

class ConversationCreate(BaseModel):
    title: str
    messages: List[Message]

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    messages: Optional[List[Message]] = None

class ConversationResponse(BaseModel):
    id: int
    user_id: int  # Changed from str to int to match BigInteger
    title: str
    messages: List[dict]  # JSON messages
    message_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
