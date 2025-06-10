from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    google_id = Column(String, unique=True, index=True)

    # OAuth tokens (encrypted in production)
    access_token = Column(String)
    refresh_token = Column(String)
    token_expires_at = Column(DateTime)

    # User preferences
    preferences = Column(JSON, default={})
    is_active = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    cleanup_sessions = relationship("CleanupSession", back_populates="user")
    rules = relationship("Rule", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")