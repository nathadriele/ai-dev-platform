from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List
from app.models.project import ProjectStatus


class ProjectBase(BaseModel):
    """Base project schema."""
    name: str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(None, max_length=500)
    repository_url: HttpUrl
    tech_stack: List[str] = Field(default_factory=list, max_length=20)


class ProjectCreate(ProjectBase):
    """Project creation schema."""
    pass


class ProjectUpdate(BaseModel):
    """Project update schema."""
    name: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, max_length=500)
    repository_url: HttpUrl | None = None
    tech_stack: List[str] | None = Field(None, max_length=20)
    status: ProjectStatus | None = None


class Project(ProjectBase):
    """Project response schema."""
    id: UUID
    status: ProjectStatus
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
