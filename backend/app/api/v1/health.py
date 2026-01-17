from fastapi import APIRouter, Depends
from datetime import datetime
from app.core.config import settings
from app.core.database import get_db
from app.schemas.common import HealthResponse, ReadinessResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def check_health():
    """Check API health status."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version=settings.app_version,
    )


@router.get("/health/ready", response_model=ReadinessResponse)
async def check_readiness(db: AsyncSession = Depends(get_db)):
    """Check API readiness (database connection)."""
    dependencies = {}
    ready = True

    # Check database connection
    try:
        await db.execute("SELECT 1")
        dependencies["database"] = "connected"
    except Exception as e:
        dependencies["database"] = f"error: {str(e)}"
        ready = False

    return ReadinessResponse(ready=ready, dependencies=dependencies)
