# backend/models/rule.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.config.database import Base
import enum


class RuleType(str, enum.Enum):
    EMAIL = "email"
    DRIVE = "drive"


class RuleAction(str, enum.Enum):
    ARCHIVE = "archive"
    DELETE = "delete"
    LABEL = "label"
    MOVE = "move"
    ORGANIZE = "organize"


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Rule definition
    name = Column(String, nullable=False)
    rule_type = Column(Enum(RuleType), nullable=False)
    action = Column(Enum(RuleAction), nullable=False)

    # Rule conditions (JSON)
    conditions = Column(JSON, nullable=False)
    # Example: {
    #   "subject_contains": ["Sale", "Discount"],
    #   "older_than_days": 14,
    #   "from_domain": "newsletter.com"
    # }

    # Rule parameters
    parameters = Column(JSON, default={})
    # Example: {"destination_folder": "Archive/Old Newsletters"}

    # Status
    is_active = Column(Boolean, default=True)

    # Usage stats
    times_applied = Column(Integer, default=0)
    last_applied = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="rules")