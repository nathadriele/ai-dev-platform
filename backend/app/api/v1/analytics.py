from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from app.core.database import get_db
from app.models.ai_activity import AIActivity
from app.schemas.analytics import UsageAnalytics, ProductivityMetrics

router = APIRouter()


@router.get("/usage", response_model=dict)
async def get_usage_analytics(
    project_id: Optional[UUID] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get AI tool usage analytics."""
    query = select(AIActivity)

    if project_id:
        query = query.where(AIActivity.project_id == project_id)
    if start_date:
        query = query.where(AIActivity.timestamp >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.where(AIActivity.timestamp <= datetime.combine(end_date, datetime.max.time()))

    result = await db.execute(query)
    activities = result.scalars().all()

    # Calculate analytics
    total_prompts = len(activities)
    prompts_by_tool = {}
    prompts_by_category = {}

    for activity in activities:
        tool = activity.tool_used.value
        category = activity.category.value

        prompts_by_tool[tool] = prompts_by_tool.get(tool, 0) + 1
        prompts_by_category[category] = prompts_by_category.get(category, 0) + 1

    # Estimate costs (very rough estimates)
    total_cost_estimate = total_prompts * 0.002  # $0.002 per prompt
    avg_tokens_per_prompt = 150.0  # Estimate
    time_saved_hours = total_prompts * 0.25  # 15 minutes saved per prompt

    analytics = UsageAnalytics(
        total_prompts=total_prompts,
        prompts_by_tool=prompts_by_tool,
        prompts_by_category=prompts_by_category,
        total_cost_estimate=round(total_cost_estimate, 2),
        avg_tokens_per_prompt=avg_tokens_per_prompt,
        time_saved_hours=round(time_saved_hours, 2),
    )

    return {"data": analytics}


@router.get("/productivity", response_model=dict)
async def get_productivity_metrics(
    project_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get developer productivity metrics."""
    # For MVP, return placeholder data
    # In production, this would integrate with Git, CI/CD, and test coverage tools

    metrics = ProductivityMetrics(
        total_commits=150,
        lines_of_code_changed=12500,
        ai_assisted_commits=95,
        ai_contribution_percentage=63.3,
        test_coverage=78.5,
        avg_build_time_minutes=4.2,
    )

    return {"data": metrics}
