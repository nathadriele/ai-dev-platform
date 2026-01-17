from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
from app.core.database import get_db
from app.models.ai_activity import AIActivity, AITool, ActivityCategory
from app.schemas.ai_activity import AIActivityCreate, AIActivity

router = APIRouter()


@router.get("", response_model=dict)
async def list_ai_activities(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    project_id: Optional[UUID] = None,
    tool_used: Optional[AITool] = None,
    category: Optional[ActivityCategory] = None,
    db: AsyncSession = Depends(get_db),
):
    """List AI activities with pagination."""
    query = select(AIActivity)

    if project_id:
        query = query.where(AIActivity.project_id == project_id)
    if tool_used:
        query = query.where(AIActivity.tool_used == tool_used)
    if category:
        query = query.where(AIActivity.category == category)

    query = query.order_by(AIActivity.timestamp.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    activities = result.scalars().all()

    # Get total count
    count_query = select(AIActivity)
    if project_id:
        count_query = count_query.where(AIActivity.project_id == project_id)
    if tool_used:
        count_query = count_query.where(AIActivity.tool_used == tool_used)
    if category:
        count_query = count_query.where(AIActivity.category == category)

    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    total_pages = (total + per_page - 1) // per_page

    return {
        "data": [AIActivity.model_validate(a) for a in activities],
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        },
    }


@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def log_ai_activity(
    activity_data: AIActivityCreate,
    db: AsyncSession = Depends(get_db),
):
    """Log an AI activity."""
    new_activity = AIActivity(
        project_id=activity_data.project_id,
        tool_used=activity_data.tool_used,
        prompt=activity_data.prompt,
        response=activity_data.response,
        code_changes=activity_data.code_changes,
        category=activity_data.category,
        user_id=UUID("00000000-0000-0000-0000-000000000000"),  # TODO: Get from auth
    )
    db.add(new_activity)
    await db.commit()
    await db.refresh(new_activity)

    return {"data": AIActivity.model_validate(new_activity)}


@router.get("/{activity_id}", response_model=dict)
async def get_ai_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific AI activity."""
    result = await db.execute(select(AIActivity).where(AIActivity.id == activity_id))
    activity = result.scalar_one_or_none()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "AI activity not found", "code": "ACTIVITY_NOT_FOUND"}},
        )

    return {"data": AIActivity.model_validate(activity)}
