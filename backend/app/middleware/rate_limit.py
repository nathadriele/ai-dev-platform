"""
Rate Limiting Middleware

Simple in-memory rate limiting implementation.
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Dict
from datetime import datetime, timedelta
import time


class RateLimiter:
    """In-memory rate limiter."""

    def __init__(self):
        self.requests: Dict[str, list] = {}

    def is_allowed(
        self,
        key: str,
        max_requests: int,
        window_seconds: int
    ) -> bool:
        """Check if request is allowed within rate limit."""
        now = time.time()

        # Clean old entries
        if key in self.requests:
            # Remove requests outside the time window
            window_start = now - window_seconds
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > window_start
            ]

        # Initialize if not exists
        if key not in self.requests:
            self.requests[key] = []

        # Check if under limit
        if len(self.requests[key]) < max_requests:
            self.requests[key].append(now)
            return True

        return False


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware."""

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.rate_limiter = RateLimiter()
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def dispatch(self, request: Request, call_next):
        """Process request with rate limiting."""
        # Skip rate limiting for health checks
        if request.url.path in ["/api/v1/health", "/api/v1/health/ready"]:
            return await call_next(request)

        # Get client identifier (IP or user ID)
        if request.state.user_id:
            # Use user ID if authenticated
            key = f"user:{request.state.user_id}"
        else:
            # Use IP address
            key = f"ip:{request.client.host}"

        # Check rate limit
        if not self.rate_limiter.is_allowed(key, self.max_requests, self.window_seconds):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": {
                        "message": "Rate limit exceeded",
                        "code": "RATE_LIMIT_EXCEEDED",
                        "limit": self.max_requests,
                        "window": self.window_seconds
                    }
                },
                headers={
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + self.window_seconds),
                }
            )

        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, self.max_requests - len(self.rate_limiter.requests.get(key, [])))
        )

        return response
