"""
Request Logging Middleware

Logs all requests and responses.
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests with timing information."""

    async def dispatch(self, request: Request, call_next):
        """Process request and log details."""
        start_time = time.time()

        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_host": request.client.host if request.client else None,
            }
        )

        # Process request
        try:
            response = await call_next(request)
            duration = time.time() - start_time

            # Log response
            logger.info(
                f"Response: {response.status_code} - {duration:.3f}s",
                extra={
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                    "method": request.method,
                    "path": request.url.path,
                }
            )

            response.headers["X-Process-Time"] = f"{duration:.3f}"
            return response

        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Request failed: {str(e)} - {duration:.3f}s",
                extra={
                    "error": str(e),
                    "duration_ms": round(duration * 1000, 2),
                    "method": request.method,
                    "path": request.url.path,
                }
            )
            raise
