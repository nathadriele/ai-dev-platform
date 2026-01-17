from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import structlog
from app.core.config import settings
from app.core.database import init_db
from app.middleware import (
    AuthMiddleware,
    RateLimitMiddleware,
    RequestLoggingMiddleware,
    configure_cors_middleware,
)
from app.api.v1 import (
    health,
    auth,
    projects,
    ai_activities,
    agents,
    pipelines,
    analytics,
    mcp,
    webhook,
)

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer() if settings.log_format == "json" else structlog.dev.ConsoleRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    logger.info("Starting up application")
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for managing AI-assisted development workflows",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# Configure CORS
configure_cors_middleware(
    app,
    allow_origins=settings.cors_origins,
)

# Add rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    max_requests=settings.rate_limit_per_minute,
    window_seconds=60,
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Add authentication middleware
app.add_middleware(AuthMiddleware)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}},
    )


# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(ai_activities.router, prefix="/api/v1/ai-activities", tags=["AI Activities"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(pipelines.router, prefix="/api/v1/pipelines", tags=["Pipelines"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(mcp.router, prefix="/api/v1/mcp", tags=["MCP"])
app.include_router(webhook.router, prefix="/api/v1/webhook", tags=["Webhooks"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI-Assisted Developer Productivity Platform API",
        "version": settings.app_version,
        "docs": "/docs" if settings.debug else "disabled in production",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
