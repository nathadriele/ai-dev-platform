from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid
import enum
from app.core.database import Base


class MCPServerType(str, enum.Enum):
    """MCP server type enumeration."""
    GITHUB = "github"
    FILESYSTEM = "filesystem"
    DATABASE = "database"
    HTTP_API = "http_api"


class MCPServerStatus(str, enum.Enum):
    """MCP server status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class MCPServer(Base):
    """MCP Server model."""

    __tablename__ = "mcp_servers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    server_type = Column(SQLEnum(MCPServerType), nullable=False)
    endpoint = Column(String, nullable=False)
    status = Column(SQLEnum(MCPServerStatus), default=MCPServerStatus.ACTIVE)
    capabilities = Column(ARRAY(String))
    last_health_check = Column(DateTime(timezone=True), server_default=func.now())
