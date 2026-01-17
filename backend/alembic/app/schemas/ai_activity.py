from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List
from app.models.ai_activity import AITool, ActivityCategory


class AIActivityBase(BaseModel):
    """Base AI activity schema."""
    project_id: UUID
    tool_used: AITool
    prompt: str
    response: str | None = None
    code_changes: List[str] = Field(default_factory=list)
    category: ActivityCategory


class AIActivityCreate(AIActivityBase):
    """AI activity creation schema."""
    pass


class AIActivity(AIActivityBase):
    """AI activity response schema."""
    id: UUID
    user_id: UUID
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
