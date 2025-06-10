from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.config.database import Base
import enum


class SessionStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SessionType(str, enum.Enum):
    EMAIL = "email"
    DRIVE = "drive"
    COMBINED = "combined"


class CleanupSession(Base):
    __tablename__ = "cleanup_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Session details
    session_type = Column(Enum(SessionType), nullable=False)
    status = Column(Enum(SessionStatus), default=SessionStatus.PENDING)

    # Results summary
    total_items_processed = Column(Integer, default=0)
    items_archived = Column(Integer, default=0)
    items_deleted = Column(Integer, default=0)
    items_organized = Column(Integer, default=0)

    # Detailed results (JSON)
    summary = Column(JSON, default={})
    actions_taken = Column(JSON, default=[])

    # Error handling
    error_message = Column(String)

    # Timestamps
    started_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="cleanup_sessions")