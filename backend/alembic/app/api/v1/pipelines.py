from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
from app.core.database import get_db
from app.models.pipeline import PipelineExecution, PipelineStatus
from app.schemas.pipeline import PipelineTrigger, PipelineExecution

router = APIRouter()


@router.get("", response_model=dict)
async def list_pipeline_executions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    project_id: Optional[UUID] = None,
    status_filter: Optional[PipelineStatus] = None,
    db: AsyncSession = Depends(get_db),
):
    """List pipeline executions."""
    query = select(PipelineExecution)

    if project_id:
        query = query.where(PipelineExecution.project_id == project_id)
    if status_filter:
        query = query.where(PipelineExecution.status == status_filter)

    query = query.order_by(PipelineExecution.started_at.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    executions = result.scalars().all()

    # Get total count
    count_query = select(PipelineExecution)
    if project_id:
        count_query = count_query.where(PipelineExecution.project_id == project_id)
    if status_filter:
        count_query = count_query.where(PipelineExecution.status == status_filter)

    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    total_pages = (total + per_page - 1) // per_page

    return {
        "data": [PipelineExecution.model_validate(e) for e in executions],
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        },
    }


@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def trigger_pipeline(
    pipeline_data: PipelineTrigger,
    db: AsyncSession = Depends(get_db),
):
    """Trigger a CI/CD pipeline."""
    new_execution = PipelineExecution(
        project_id=pipeline_data.project_id,
        pipeline_name="ci-pipeline",  # TODO: Configure per project
        commit_sha=pipeline_data.commit_sha,
        branch=pipeline_data.branch,
        triggered_by="user",  # TODO: Get from auth
    )
    db.add(new_execution)
    await db.commit()
    await db.refresh(new_execution)

    # TODO: Trigger actual CI/CD pipeline via GitHub Actions or similar

    return {"data": PipelineExecution.model_validate(new_execution)}


@router.get("/{execution_id}", response_model=dict)
async def get_pipeline_execution(
    execution_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get pipeline execution details."""
    result = await db.execute(select(PipelineExecution).where(PipelineExecution.id == execution_id))
    execution = result.scalar_one_or_none()

    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "Pipeline execution not found", "code": "PIPELINE_NOT_FOUND"}},
        )

    return {"data": PipelineExecution.model_validate(execution)}
