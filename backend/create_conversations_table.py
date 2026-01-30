"""
Database Migration Script - Create Conversations Table
Run this script to create the conversations table in your database
"""

from app.core.db import Base, engine
from app.models.profile_models import Conversations, Users

def create_conversations_table():
    """Create the conversations table"""
    try:
        # Create only the conversations table
        Conversations.__table__.create(bind=engine, checkfirst=True)
        print("✅ Conversations table created successfully!")
        print("   - Table: conversations")
        print("   - Columns: id, user_id, title, messages (JSON), message_count, created_at, updated_at")
        print("   - Foreign Key: user_id -> users.id")
        return True
    except Exception as e:
        print(f"❌ Error creating conversations table: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting database migration...")
    print("=" * 60)
    success = create_conversations_table()
    print("=" * 60)
    if success:
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed!")
