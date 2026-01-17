from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from uuid import UUID
from app.core.database import get_db
from app.models.project import Project, ProjectStatus
from app.schemas.project import ProjectCreate, ProjectUpdate, Project

router = APIRouter()


@router.get("", response_model=dict)
async def list_projects(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status_filter: Optional[ProjectStatus] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all projects with pagination."""
    query = select(Project)

    if status_filter:
        query = query.where(Project.status == status_filter)

    if search:
        query = query.where(Project.name.ilike(f"%{search}%"))

    # Count total
    count_query = select(Project)
    if status_filter:
        count_query = count_query.where(Project.status == status_filter)
    if search:
        count_query = count_query.where(Project.name.ilike(f"%{search}%"))

    # Get paginated results
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    projects = result.scalars().all()

    # Get total count
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    total_pages = (total + per_page - 1) // per_page

    return {
        "data": [Project.model_validate(p) for p in projects],
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        },
    }


@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new project."""
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        repository_url=str(project_data.repository_url),
        tech_stack=project_data.tech_stack,
        created_by=UUID("00000000-0000-0000-0000-000000000000"),  # TODO: Get from auth
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)

    return {"data": Project.model_validate(new_project)}


@router.get("/{project_id}", response_model=dict)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific project by ID."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "Project not found", "code": "PROJECT_NOT_FOUND"}},
        )

    return {"data": Project.model_validate(project)}


@router.put("/{project_id}", response_model=dict)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a project."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "Project not found", "code": "PROJECT_NOT_FOUND"}},
        )

    # Update fields
    if project_data.name is not None:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description
    if project_data.repository_url is not None:
        project.repository_url = str(project_data.repository_url)
    if project_data.tech_stack is not None:
        project.tech_stack = project_data.tech_stack
    if project_data.status is not None:
        project.status = project_data.status

    await db.commit()
    await db.refresh(project)

    return {"data": Project.model_validate(project)}


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a project."""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"message": "Project not found", "code": "PROJECT_NOT_FOUND"}},
        )

    await db.delete(project)
    await db.commit()
