"""
Production-Grade Logging Configuration
Provides structured logging with rotation, error tracking, and audit trails
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)


# Configure main application logger
def setup_logging():
    """Initialize production-grade logging"""
    app_logger = logging.getLogger("ai_app")
    app_logger.setLevel(logging.DEBUG)

    # Format for all handlers
    detailed_format = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1. INFO + WARNINGS -> application.log (rotating, 10MB)
    info_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "application.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(detailed_format)
    app_logger.addHandler(info_handler)

    # 2. ERRORS -> error.log (rotating, 10MB)
    error_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "error.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_format)
    app_logger.addHandler(error_handler)

    # 3. SQL QUERIES -> sql.log (rotating, 20MB) - For audit trail
    sql_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "sql.log", maxBytes=20 * 1024 * 1024, backupCount=10
    )
    sql_handler.setLevel(logging.DEBUG)
    sql_handler.setFormatter(detailed_format)
    sql_logger = logging.getLogger("sql_queries")
    sql_logger.addHandler(sql_handler)

    # 4. AI INTERACTIONS -> ai.log (rotating, 20MB)
    ai_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "ai.log", maxBytes=20 * 1024 * 1024, backupCount=10
    )
    ai_handler.setLevel(logging.DEBUG)
    ai_handler.setFormatter(detailed_format)
    ai_logger = logging.getLogger("ai_service")
    ai_logger.addHandler(ai_handler)

    # 5. CONSOLE (INFO level only - avoid spam in production)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(levelname)s | %(name)s | %(message)s")
    console_handler.setFormatter(console_formatter)
    app_logger.addHandler(console_handler)

    return app_logger


# Initialize on import
logger = setup_logging()


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module"""
    return logging.getLogger(name)
