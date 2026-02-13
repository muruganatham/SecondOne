
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.db import get_db, engine
from app.core.config import settings

from fastapi.middleware.cors import CORSMiddleware

print("🚀 Starting AI Application Backend...")

app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.PROJECT_VERSION,
    swagger_ui_parameters={"persistAuthorization": True}
)

print("✅ FastAPI App initialized.")

# CORS Configuration
origins = [
    "http://192.168.0.125:3000",
    "*", # Allow All Origins for Debugging as requested
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Application Backend"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Try to execute a simple query
        result = db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "result": result.scalar()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Include Routers - Full Role-Based System
from app.api.endpoints import ai_query
from app.api.endpoints import auth
from app.api.endpoints import conversations

app.include_router(ai_query.router, prefix="/api/v1/ai", tags=["AI Chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["Conversations"])

