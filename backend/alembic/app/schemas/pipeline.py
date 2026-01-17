from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Any
from app.models.pipeline import PipelineStatus


class PipelineTrigger(BaseModel):
    """Pipeline trigger schema."""
    project_id: UUID
    branch: str = Field(..., description="Git branch to build")
    commit_sha: str = Field(..., description="Git commit SHA")


class PipelineExecution(BaseModel):
    """Pipeline execution response schema."""
    id: UUID
    project_id: UUID
    pipeline_name: str
    status: PipelineStatus
    commit_sha: str
    branch: str
    triggered_by: str
    started_at: datetime
    completed_at: datetime | None = None
    test_results: dict[str, Any] | None = None
    deployment_url: HttpUrl | None = None

    model_config = ConfigDict(from_attributes=True)
