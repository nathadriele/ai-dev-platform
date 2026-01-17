from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.core.database import get_db
from app.models.agent import AgentExecution
from app.schemas.agent import AgentType, AgentExecutionCreate, AgentExecution
from typing import List

router = APIRouter()

# Available agent types
AVAILABLE_AGENTS: List[AgentType] = [
    AgentType(
        id="code-scaffolder",
        name="Code Scaffolder",
        description="Generates project structure and boilerplate code",
        capabilities=["scaffold", "boilerplate", "structure"],
        requires_mcp_server=False,
    ),
    AgentType(
        id="code-reviewer",
        name="Code Reviewer",
        description="Reviews code for bugs, security issues, and best practices",
        capabilities=["review", "analyze", "security"],
        requires_mcp_server=True,
    ),
    AgentType(
        id="test-generator",
        name="Test Generator",
        description="Generates unit and integration tests",
        capabilities=["testing", "unit-tests", "integration-tests"],
        requires_mcp_server=True,
    ),
    AgentType(
        id="doc-generator",
        name="Documentation Generator",
        description="Generates technical documentation",
        capabilities=["docs", "documentation", "markdown"],
        requires_mcp_server=True,
    ),
]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def execute_agent(
    execution_data: AgentExecutionCreate,
    db: AsyncSession = Depends(get_db),
):
    """Execute an agent task."""
    # Verify agent type exists
    agent_types = {agent.id for agent in AVAILABLE_AGENTS}
    if execution_data.agent_type not in agent_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"message": f"Unknown agent type: {execution_data.agent_type}", "code": "INVALID_AGENT_TYPE"}},
        )

    # Create agent execution record
    new_execution = AgentExecution(
        project_id=execution_data.project_id,
        agent_type=execution_data.agent_type,
        task_description=execution_data.task_description,
        input_data=execution_data.input_data,
    )
    db.add(new_execution)
    await db.commit()
    await db.refresh(new_execution)

    # TODO: Queue actual agent execution in background

    return {"data": AgentExecution.model_validate(new_execution)}


@router.get("/types", response_model=dict)
async def list_agent_types():
    """List available agent types."""
    return {"data": AVAILABLE_AGENTS}


@router.get("/{execution_id}", response_model=dict)
async def get_agent_execution(
    execution_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get agent execution status and results."""
    result = await db.execute(select(AgentExecution).where(AgentExecution.id == execution_id))
    execution = result.scalar_one_or_none()

    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "Agent execution not found", "code": "EXECUTION_NOT_FOUND"}},
        )

    return {"data": AgentExecution.model_validate(execution)}
