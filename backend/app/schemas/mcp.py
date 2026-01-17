from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List
from app.models.mcp import MCPServerType, MCPServerStatus


class MCPServerBase(BaseModel):
    """Base MCP server schema."""
    name: str
    server_type: MCPServerType
    endpoint: HttpUrl
    capabilities: List[str] = Field(default_factory=list)


class MCPServerCreate(MCPServerBase):
    """MCP server creation schema."""
    pass


class MCPServer(MCPServerBase):
    """MCP server response schema."""
    id: UUID
    status: MCPServerStatus
    last_health_check: datetime

    model_config = ConfigDict(from_attributes=True)


class MCPToolExecute(BaseModel):
    """MCP tool execution schema."""
    tool_name: str = Field(..., description="Name of the tool to execute")
    parameters: dict[str, object] = Field(default_factory=dict, description="Parameters for the tool")
