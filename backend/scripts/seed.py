"""
Database seeding script.
Run with: python scripts/seed.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, init_db
from app.models.user import User
from app.models.project import Project, ProjectStatus
from app.models.ai_activity import AIActivity, AITool, ActivityCategory
from app.core.security import get_password_hash


async def seed_users(db: AsyncSession):
    """Seed default users."""
    users = [
        User(
            email="admin@example.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("Admin123!"),
        ),
        User(
            email="nathadriele@example.com",
            username="nathadriele",
            full_name="Natha Driele",
            hashed_password=get_password_hash("User123!"),
        ),
    ]

    for user in users:
        db.add(user)

    await db.commit()
    print(f"Seeded {len(users)} users")


async def seed_projects(db: AsyncSession):
    """Seed sample projects."""
    # Get admin user
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.username == "admin"))
    admin = result.scalar_one()

    projects = [
        Project(
            name="AI Dev Platform",
            description="Platform for tracking AI-assisted development",
            repository_url="https://github.com/nathadriele/ai-dev-platform",
            tech_stack=["React", "TypeScript", "FastAPI", "PostgreSQL"],
            status=ProjectStatus.ACTIVE,
            created_by=str(admin.id),
        ),
        Project(
            name="ML Model Training",
            description="Machine learning model training pipeline",
            repository_url="https://github.com/nathadriele/ml-training",
            tech_stack=["Python", "TensorFlow", "Docker"],
            status=ProjectStatus.ACTIVE,
            created_by=str(admin.id),
        ),
    ]

    for project in projects:
        db.add(project)

    await db.commit()
    print(f"Seeded {len(projects)} projects")


async def seed_ai_activities(db: AsyncSession):
    """Seed sample AI activities."""
    from sqlalchemy import select
    import uuid

    # Get user and project
    result_user = await db.execute(select(User).where(User.username == "admin"))
    user = result_user.scalar_one()

    result_project = await db.execute(select(Project).where(Project.name == "AI Dev Platform"))
    project = result_project.scalar_one()

    activities = [
        AIActivity(
            id=uuid.uuid4(),
            project_id=str(project.id),
            tool_used=AITool.CLAUDE,
            prompt="Generate a FastAPI backend structure with authentication",
            response="Here is a complete FastAPI implementation with JWT authentication...",
            code_changes=["app/main.py", "app/api/v1/auth.py"],
            user_id=str(user.id),
            category=ActivityCategory.FEATURE,
        ),
        AIActivity(
            id=uuid.uuid4(),
            project_id=str(project.id),
            tool_used=AITool.CHATGPT,
            prompt="Create a React login form with Material UI",
            response="Here is a React login form component using Material UI...",
            code_changes=["frontend/src/pages/LoginPage.tsx"],
            user_id=str(user.id),
            category=ActivityCategory.FEATURE,
        ),
        AIActivity(
            id=uuid.uuid4(),
            project_id=str(project.id),
            tool_used=AITool.CLAUDE,
            prompt="Review this code for security issues",
            response="I found several potential security issues:\n1. SQL injection risk...",
            code_changes=["app/api/v1/projects.py"],
            user_id=str(user.id),
            category=ActivityCategory.BUGFIX,
        ),
    ]

    for activity in activities:
        db.add(activity)

    await db.commit()
    print(f"Seeded {len(activities)} AI activities")


async def main():
    """Main seeding function."""
    print("Starting database seeding...")

    # Initialize database
    await init_db()
    print("Database initialized")

    async with AsyncSessionLocal() as db:
        try:
            await seed_users(db)
            await seed_projects(db)
            await seed_ai_activities(db)

            print("Seeding completed successfully!")
        except Exception as e:
            print(f"Error during seeding: {e}")
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
