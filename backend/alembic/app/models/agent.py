from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.core.database import Base


class AgentStatus(str, enum.Enum):
    """Agent execution status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentExecution(Base):
    """Agent execution model."""

    __tablename__ = "agent_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    agent_type = Column(String, nullable=False)
    task_description = Column(Text, nullable=False)
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.PENDING)
    input_data = Column(JSON)
    output_data = Column(JSON)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="agent_executions")
