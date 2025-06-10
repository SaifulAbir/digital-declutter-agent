# backend/config/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config.settings import settings

# DATABASE ENGINE CONFIGURATION
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite specific configuration
)

# SESSION FACTORY CONFIGURATION
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# BASE MODEL CLASS
Base = declarative_base() # Base class for all SQLAlchemy ORM models

# DATABASE DEPENDENCY
def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal() # Create a new database session
    try:
        yield db # Provide the session to the FastAPI endpoint
    finally:
        db.close() # Ensure session is closed after request completion