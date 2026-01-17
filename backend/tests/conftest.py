import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.database import Base, get_db
from app.models import (
    User, Project, AIActivity, AgentExecution,
    PipelineExecution, MCPServer
)


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database override."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "Test1234!",
        "full_name": "Test User"
    }


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        "name": "Test Project",
        "description": "A test project for AI development",
        "repository_url": "https://github.com/nathadriele/test-project",
        "tech_stack": ["React", "FastAPI", "PostgreSQL"]
    }


@pytest.fixture
def sample_ai_activity_data():
    """Sample AI activity data for testing."""
    return {
        "tool_used": "claude",
        "prompt": "Generate a REST API for user management",
        "response": "Here is a FastAPI implementation...",
        "category": "feature"
    }


@pytest.fixture
async def test_user(db_session: AsyncSession, sample_user_data):
    """Create a test user in database."""
    from app.core.security import get_password_hash

    user = User(
        email=sample_user_data["email"],
        username=sample_user_data["username"],
        full_name=sample_user_data["full_name"],
        hashed_password=get_password_hash(sample_user_data["password"])
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_project(db_session: AsyncSession, test_user, sample_project_data):
    """Create a test project in database."""
    project = Project(
        name=sample_project_data["name"],
        description=sample_project_data["description"],
        repository_url=sample_project_data["repository_url"],
        tech_stack=sample_project_data["tech_stack"],
        created_by=str(test_user.id)
    )
    db_session.add(project)
    await db_session.commit()
    await db_session.refresh(project)
    return project


@pytest.fixture
async def auth_headers(client: AsyncClient, sample_user_data):
    """Get authentication headers for test user."""
    # Register and login
    await client.post("/api/v1/auth/register", json=sample_user_data)

    response = await client.post("/api/v1/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })

    tokens = response.json()["tokens"]
    return {"Authorization": f"Bearer {tokens['access_token']}"}
