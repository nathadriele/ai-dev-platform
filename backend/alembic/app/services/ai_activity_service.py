from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from app.models.ai_activity import AIActivity, AITool, ActivityCategory
from app.schemas.ai_activity import AIActivityCreate
from app.services.base import BaseService


class AIActivityService(BaseService[AIActivity, AIActivityCreate, dict]):
    """Service for AI activity operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(AIActivity, db)

    async def get_project_activities(
        self,
        project_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[AIActivity]:
        """Get activities for a specific project."""
        result = await self.db.execute(
            select(AIActivity)
            .where(AIActivity.project_id == project_id)
            .order_by(desc(AIActivity.timestamp))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_user_activities(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[AIActivity]:
        """Get activities for a specific user."""
        result = await self.db.execute(
            select(AIActivity)
            .where(AIActivity.user_id == user_id)
            .order_by(desc(AIActivity.timestamp))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_tool(
        self,
        tool: AITool,
        skip: int = 0,
        limit: int = 100
    ) -> List[AIActivity]:
        """Get activities by AI tool used."""
        result = await self.db.execute(
            select(AIActivity)
            .where(AIActivity.tool_used == tool)
            .order_by(desc(AIActivity.timestamp))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_category(
        self,
        category: ActivityCategory,
        skip: int = 0,
        limit: int = 100
    ) -> List[AIActivity]:
        """Get activities by category."""
        result = await self.db.execute(
            select(AIActivity)
            .where(AIActivity.category == category)
            .order_by(desc(AIActivity.timestamp))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        project_id: Optional[str] = None
    ) -> List[AIActivity]:
        """Get activities within a date range."""
        query = select(AIActivity).where(
            and_(
                AIActivity.timestamp >= start_date,
                AIActivity.timestamp <= end_date
            )
        )

        if project_id:
            query = query.where(AIActivity.project_id == project_id)

        result = await self.db.execute(
            query.order_by(desc(AIActivity.timestamp))
        )
        return list(result.scalars().all())

    async def get_statistics(
        self,
        project_id: Optional[str] = None,
        days: int = 30
    ) -> dict:
        """Get activity statistics for the past N days."""
        start_date = datetime.utcnow() - timedelta(days=days)

        query = select(AIActivity).where(AIActivity.timestamp >= start_date)
        if project_id:
            query = query.where(AIActivity.project_id == project_id)

        result = await self.db.execute(query)
        activities = list(result.scalars().all())

        # Calculate statistics
        total = len(activities)
        by_tool = {}
        by_category = {}
        total_cost = 0.0

        for activity in activities:
            tool = activity.tool_used.value
            category = activity.category.value

            by_tool[tool] = by_tool.get(tool, 0) + 1
            by_category[category] = by_category.get(category, 0) + 1

            # Rough cost estimation (adjust based on actual pricing)
            total_cost += 0.002

        return {
            "total_prompts": total,
            "prompts_by_tool": by_tool,
            "prompts_by_category": by_category,
            "total_cost_estimate": round(total_cost, 4),
            "avg_tokens_per_prompt": 150.0,  # Placeholder
            "time_saved_hours": round(total * 0.25, 2)
        }
