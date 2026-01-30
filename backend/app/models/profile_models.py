from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, Numeric, ForeignKey, Float, JSON, Enum, BigInteger, SmallInteger
from sqlalchemy.orm import relationship
from app.core.db import Base
import app.models.enums as Enums
from datetime import datetime

# Final Stable Models
# Using Integer for potential Enums that are missing in the Enums file to prevent crashes.

class Users(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(255), nullable=True)
    roll_no = Column(String(20), nullable=True)
    # UsersRole is confirmed to exist in Enums.py logic but causing LookupError. Using Integer.
    role = Column(Integer, nullable=False)
    
    # Analytics Stats
    stats_chat_count = Column(Integer, default=0)
    stats_words_generated = Column(BigInteger, default=0)
    active_streak = Column(Integer, default=0)
    last_active_date = Column(DateTime, nullable=True)
    
    # Relationships
    conversations = relationship('Conversations', back_populates='user', cascade='all, delete-orphan')

class Conversations(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    messages = Column(JSON, nullable=False)  # Store messages as JSON array
    message_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship
    user = relationship('Users', back_populates='conversations')

class Colleges(Base):
    __tablename__ = 'colleges'

    # Fallback to Integer for missing Enums
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) 
    college_name = Column(Integer, nullable=False) # Maps to an Enum value
    # Removed other columns

class Departments(Base):
    __tablename__ = 'departments'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    department_name = Column(String(80), nullable=False)

class UserAcademics(Base):
    __tablename__ = 'user_academics'

    id = Column(String, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    college_id = Column(Integer, ForeignKey('colleges.id'), nullable=True)
    department_id = Column(String, ForeignKey('departments.id'), nullable=True)
    
    # Relationships
    college = relationship('Colleges', foreign_keys=[college_id])
    department = relationship('Departments', foreign_keys=[department_id])
    user = relationship('Users', foreign_keys=[user_id])

