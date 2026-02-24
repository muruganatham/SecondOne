from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.db import get_db, engine
from app.core.config import settings
from app.core.logging_config import setup_logging, get_logger
# Add at the very top of app/main.py, before any logger calls
import sys
import os

# Fix Windows terminal Unicode encoding
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
# Initialize logging FIRST
logger = setup_logging()

print("\n" + "=" * 60)
logger.info("🚀 Starting AI Application Backend...")
print("=" * 60 + "\n")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    swagger_ui_parameters={"persistAuthorization": True},
)

print("✅ FastAPI App initialized.")

# CORS Configuration (Production-Safe)
allowed_origins = list(settings.ALLOWED_CORS_ORIGINS)

# CORS Configuration
# We apply this LAST so it is the FIRST to execute
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://demolab.amypo.ai",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ],
    allow_origin_regex=r"https?://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


from fastapi.responses import FileResponse as _FileResponse
import os as _os

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to AI Application Backend",
        "version": settings.PROJECT_VERSION,
        "status": "running",
    }


@app.get("/test")
def stream_test_page():
    """Serve the local AI stream tester page (dev only)."""
    html_path = _os.path.join(_os.path.dirname(__file__), "..", "test_stream.html")
    html_path = _os.path.abspath(html_path)
    if _os.path.exists(html_path):
        return _FileResponse(html_path, media_type="text/html")
    return {"error": "test_stream.html not found"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Comprehensive health check"""
    try:
        # Database connectivity
        result = db.execute(text("SELECT 1"))
        db_status = "connected" if result.scalar() == 1 else "error"

        # AI Service check
        from app.services.ai_service import ai_service

        ai_status = "configured" if ai_service.client else "unconfigured"

        # SQL Executor check
        from app.services.sql_executor import sql_executor

        tables_loaded = (
            len(sql_executor.existing_tables) if sql_executor.existing_tables else 0
        )

        # Cache stats
        from app.core.rate_limiter import query_cache

        cache_stats = query_cache.get_stats()

        health_data = {
            "status": "healthy" if db_status == "connected" else "degraded",
            "timestamp": datetime.now().isoformat(),
            "database": {"status": db_status, "tables_loaded": tables_loaded},
            "ai_service": {"status": ai_status},
            "cache": cache_stats,
            "version": settings.PROJECT_VERSION,
        }

        logger.info(f"Health check: {health_data['status']}")
        return health_data

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


@app.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """Get performance metrics and statistics"""
    try:
        from app.services.sql_executor import sql_executor

        metrics = {
            "timestamp": datetime.now().isoformat(),
            "executor": sql_executor.get_stats(),
            "cache": query_cache.get_stats(),
        }

        logger.debug(f"Metrics requested: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Metrics error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error retrieving metrics: {str(e)}"
        )


# Include Routers - Full Role-Based System
from app.api.endpoints import ai_query
from app.api.endpoints import auth
from app.api.endpoints import conversations

app.include_router(ai_query.router, prefix="/api/v1/ai", tags=["AI Chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(
    conversations.router, prefix="/api/v1/conversations", tags=["Conversations"]
)
