from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.core.database import Base


class AITool(str, enum.Enum):
    """AI tool enumeration."""
    CHATGPT = "chatgpt"
    CLAUDE = "claude"
    COPILOT = "copilot"
    CURSOR = "cursor"


class ActivityCategory(str, enum.Enum):
    """Activity category enumeration."""
    FEATURE = "feature"
    BUGFIX = "bugfix"
    REFACTOR = "refactor"
    DOCS = "docs"
    TEST = "test"


class AIActivity(Base):
    """AI Activity tracking model."""

    __tablename__ = "ai_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    tool_used = Column(SQLEnum(AITool), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text)
    code_changes = Column(ARRAY(String))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category = Column(SQLEnum(ActivityCategory), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="ai_activities")
    user = relationship("User", back_populates="ai_activities")
