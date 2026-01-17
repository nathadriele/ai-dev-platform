from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.models.agent import AgentExecution
from app.schemas.agent import AgentType, AgentExecutionCreate, AgentExecution
from app.services.agent_executor import AgentExecutor
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
    AgentType(
        id="github-analyzer",
        name="GitHub Analyzer",
        description="Analyzes GitHub repository and recent commits",
        capabilities=["github", "analysis", "commits"],
        requires_mcp_server=True,
    ),
]


def run_agent_task(
    execution_id: UUID,
    agent_type: str,
    project_id: str,
    task_description: str,
    input_data: dict
):
    """Background task to run agent."""
    import asyncio
    from app.core.database import AsyncSessionLocal

    async def run():
        async with AsyncSessionLocal() as db:
            executor = AgentExecutor(db)
            try:
                await executor.run_agent(
                    agent_type=agent_type,
                    project_id=project_id,
                    task_description=task_description,
                    input_data=input_data
                )
            except Exception as e:
                print(f"Agent execution failed: {e}")

    asyncio.run(run())


@router.post("", status_code=status.HTTP_202_ACCEPTED, response_model=dict)
async def execute_agent(
    execution_data: AgentExecutionCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Execute an agent task (runs in background)."""
    # Verify agent type exists
    agent_types = {agent.id for agent in AVAILABLE_AGENTS}
    if execution_data.agent_type not in agent_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"message": f"Unknown agent type: {execution_data.agent_type}", "code": "INVALID_AGENT_TYPE"}},
        )

    # Create execution record
    execution = AgentExecution(
        id=UUID(__import__('uuid').uuid4().hex),
        project_id=execution_data.project_id,
        agent_type=execution_data.agent_type,
        task_description=execution_data.task_description,
        status="pending",
        input_data=execution_data.input_data,
        started_at=datetime.utcnow(),
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)

    # Run agent in background
    background_tasks.add_task(
        run_agent_task,
        str(execution.id),
        execution_data.agent_type,
        str(execution_data.project_id),
        execution_data.task_description,
        execution_data.input_data or {}
    )

    return {
        "data": AgentExecution.model_validate(execution),
        "message": "Agent execution started. Check status using the execution ID."
    }


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
    result = await db.execute(
        select(AgentExecution).where(AgentExecution.id == execution_id)
    )
    execution = result.scalar_one_or_none()

    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "Agent execution not found", "code": "EXECUTION_NOT_FOUND"}},
        )

    return {"data": AgentExecution.model_validate(execution)}
