from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List, Any
from app.models.agent import AgentStatus


class AgentType(BaseModel):
    """Agent type schema."""
    id: str
    name: str
    description: str
    capabilities: List[str]
    requires_mcp_server: bool


class AgentExecutionCreate(BaseModel):
    """Agent execution creation schema."""
    project_id: UUID
    agent_type: str = Field(..., description="Type of agent to execute")
    task_description: str = Field(..., description="Description of the task to perform")
    input_data: dict[str, Any] | None = None


class AgentExecution(BaseModel):
    """Agent execution response schema."""
    id: UUID
    project_id: UUID
    agent_type: str
    task_description: str
    status: AgentStatus
    input_data: dict[str, Any] | None = None
    output_data: dict[str, Any] | None = None
    started_at: datetime
    completed_at: datetime | None = None
    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)
