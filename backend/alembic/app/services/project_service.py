from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.project import Project, ProjectStatus
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.base import BaseService


class ProjectService(BaseService[Project, ProjectCreate, ProjectUpdate]):
    """Service for project operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Project, db)

    async def get_user_projects(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ProjectStatus] = None
    ) -> List[Project]:
        """Get projects for a specific user."""
        query = select(Project).where(Project.created_by == user_id)

        if status:
            query = query.where(Project.status == status)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def search(
        self,
        user_id: str,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """Search projects by name or description."""
        result = await self.db.execute(
            select(Project)
            .where(Project.created_by == user_id)
            .where(
                or_(
                    Project.name.ilike(f"%{search_term}%"),
                    Project.description.ilike(f"%{search_term}%")
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_active_count(self, user_id: str) -> int:
        """Get count of active projects for user."""
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count(Project.id))
            .where(Project.created_by == user_id)
            .where(Project.status == ProjectStatus.ACTIVE)
        )
        return result.scalar()
