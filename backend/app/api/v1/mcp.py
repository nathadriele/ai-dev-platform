from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.core.database import get_db
from app.models.mcp import MCPServer
from app.schemas.mcp import MCPServerCreate, MCPServer, MCPToolExecute
from typing import List

router = APIRouter()


@router.get("/servers", response_model=dict)
async def list_mcp_servers(
    db: AsyncSession = Depends(get_db),
):
    """List all configured MCP servers."""
    result = await db.execute(select(MCPServer))
    servers = result.scalars().all()

    return {"data": [MCPServer.model_validate(s) for s in servers]}


@router.post("/servers", status_code=status.HTTP_201_CREATED, response_model=dict)
async def register_mcp_server(
    server_data: MCPServerCreate,
    db: AsyncSession = Depends(get_db),
):
    """Register a new MCP server."""
    new_server = MCPServer(
        name=server_data.name,
        server_type=server_data.server_type,
        endpoint=str(server_data.endpoint),
        capabilities=server_data.capabilities,
    )
    db.add(new_server)
    await db.commit()
    await db.refresh(new_server)

    return {"data": MCPServer.model_validate(new_server)}


@router.post("/servers/{server_id}/execute", response_model=dict)
async def execute_mcp_tool(
    server_id: UUID,
    tool_data: MCPToolExecute,
    db: AsyncSession = Depends(get_db),
):
    """Execute a tool on an MCP server."""
    # Get server
    result = await db.execute(select(MCPServer).where(MCPServer.id == server_id))
    server = result.scalar_one_or_none()

    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "MCP server not found", "code": "SERVER_NOT_FOUND"}},
        )

    # TODO: Implement actual MCP server communication
    # This would involve:
    # 1. Establishing connection to MCP server
    # 2. Calling the specified tool with parameters
    # 3. Returning the result

    result_data = {
        "tool_name": tool_data.tool_name,
        "parameters": tool_data.parameters,
        "result": "Tool execution result (placeholder)",
    }

    return {"data": result_data}
