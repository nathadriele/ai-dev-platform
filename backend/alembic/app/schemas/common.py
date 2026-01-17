from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    page: int
    per_page: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    data: List[T]
    meta: PaginationMeta


class Error(BaseModel):
    """Error response schema."""
    error: dict


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str


class ReadinessResponse(BaseModel):
    """Readiness check response."""
    ready: bool
    dependencies: dict[str, str]
