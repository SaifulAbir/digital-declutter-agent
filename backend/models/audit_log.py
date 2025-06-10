from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.config.database import Base
import enum


class ActionType(str, enum.Enum):
    EMAIL_ARCHIVE = "email_archive"
    EMAIL_DELETE = "email_delete"
    EMAIL_LABEL = "email_label"
    FILE_MOVE = "file_move"
    FILE_DELETE = "file_delete"
    FILE_ORGANIZE = "file_organize"
    RULE_APPLIED = "rule_applied"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Action details
    action_type = Column(Enum(ActionType), nullable=False)
    resource_id = Column(String, nullable=False)  # Email ID, File ID, etc.
    resource_type = Column(String, nullable=False)  # "email", "file"

    # Action description
    description = Column(String)

    # Original state (for undo functionality)
    original_state = Column(JSON)

    # New state
    new_state = Column(JSON)

    # Metadata
    metadata = Column(JSON, default={})

    # Undo capability
    can_undo = Column(String, default=True)  # Boolean, but using String for SQLite
    undone_at = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="audit_logs")