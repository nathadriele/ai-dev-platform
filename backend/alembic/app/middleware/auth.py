"""
Authentication Middleware

Provides JWT authentication for protected routes.
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.security import decode_token
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to handle JWT authentication."""

    async def dispatch(self, request: Request, call_next):
        """Process request and validate JWT token."""
        # Skip authentication for public endpoints
        if request.url.path in [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/health",
            "/api/v1/health/ready",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
        ]:
            return await call_next(request)

        # Get token from Authorization header
        authorization = request.headers.get("Authorization")

        if not authorization:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": {"message": "Missing authorization header", "code": "NO_AUTH_HEADER"}}
            )

        if not authorization.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": {"message": "Invalid authorization format", "code": "INVALID_AUTH_FORMAT"}}
            )

        token = authorization.split(" ")[1]

        # Decode and validate token
        payload = decode_token(token)

        if not payload:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": {"message": "Invalid or expired token", "code": "INVALID_TOKEN"}}
            )

        # Check token type
        if payload.get("type") != "access":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": {"message": "Invalid token type", "code": "INVALID_TOKEN_TYPE"}}
            )

        # Add user info to request state
        request.state.user_id = payload.get("sub")
        request.state.token_payload = payload

        return await call_next(request)


async def get_current_user(request: Request, db: AsyncSession) -> User:
    """Get current authenticated user from request."""
    user_id = request.state.user_id

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# Optional dependency for routes that can work without auth
async def get_optional_user(request: Request, db: AsyncSession) -> User | None:
    """Get current user if authenticated, otherwise return None."""
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None
