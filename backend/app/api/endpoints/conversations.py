from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.db import get_db
from app.models.profile_models import Users, Conversations
from app.schemas.conversation import ConversationCreate, ConversationUpdate, ConversationResponse
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for the current user"""
    conversations = db.query(Conversations).filter(
        Conversations.user_id == current_user.id
    ).order_by(Conversations.updated_at.desc()).all()
    return conversations

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific conversation"""
    conversation = db.query(Conversations).filter(
        Conversations.id == conversation_id,
        Conversations.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation

@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation: ConversationCreate,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new conversation"""
    # Convert Pydantic models to dicts for JSON storage
    messages_data = [msg.dict() for msg in conversation.messages]
    
    db_conversation = Conversations(
        user_id=current_user.id,
        title=conversation.title,
        messages=messages_data,
        message_count=len(messages_data)
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    
    # Update user's chat count
    current_user.stats_chat_count = db.query(Conversations).filter(
        Conversations.user_id == current_user.id
    ).count()
    db.commit()
    
    return db_conversation

@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: int,
    conversation: ConversationUpdate,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing conversation"""
    db_conversation = db.query(Conversations).filter(
        Conversations.id == conversation_id,
        Conversations.user_id == current_user.id
    ).first()
    
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if conversation.title is not None:
        db_conversation.title = conversation.title
    
    if conversation.messages is not None:
        messages_data = [msg.dict() for msg in conversation.messages]
        db_conversation.messages = messages_data
        db_conversation.message_count = len(messages_data)
    
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a conversation"""
    db_conversation = db.query(Conversations).filter(
        Conversations.id == conversation_id,
        Conversations.user_id == current_user.id
    ).first()
    
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(db_conversation)
    db.commit()
    
    # Update user's chat count
    current_user.stats_chat_count = db.query(Conversations).filter(
        Conversations.user_id == current_user.id
    ).count()
    db.commit()
    
    return None
