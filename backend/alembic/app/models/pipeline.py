from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.core.database import Base


class PipelineStatus(str, enum.Enum):
    """Pipeline execution status enumeration."""
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class PipelineExecution(Base):
    """Pipeline execution model."""

    __tablename__ = "pipeline_executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    pipeline_name = Column(String, nullable=False)
    status = Column(SQLEnum(PipelineStatus), default=PipelineStatus.RUNNING)
    commit_sha = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    triggered_by = Column(String, nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    test_results = Column(JSON)
    deployment_url = Column(String, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="pipeline_executions")
