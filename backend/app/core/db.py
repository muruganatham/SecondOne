from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

import os
import certifi

# Create database engine
connect_args = {}
# TiDB Cloud requires SSL. 
# On Render (Linux), we typically use the system CA certs.
# On Windows/other, we use certifi to provide a valid CA bundle.
ca_path = "/etc/ssl/certs/ca-certificates.crt"
if os.path.exists(ca_path):
    connect_args["ssl"] = {"ca": ca_path}
else:
    # Fallback to certifi for cross-platform support (especially Windows)
    connect_args["ssl"] = {"ca": certifi.where()}

# Add connection timeout
connect_args["connect_timeout"] = 10

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
