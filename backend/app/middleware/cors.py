"""
CORS Middleware Configuration

Configure Cross-Origin Resource Sharing policies.
"""
from fastapi import Request
from starlette.middleware.cors import CORSMiddleware
from typing import List


def configure_cors_middleware(
    app,
    allow_origins: List[str] = None,
    allow_methods: List[str] = None,
    allow_headers: List[str] = None,
):
    """Configure CORS middleware for application."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins or ["*"],
        allow_credentials=True,
        allow_methods=allow_methods or ["*"],
        allow_headers=allow_headers or ["*"],
        expose_headers=["X-Process-Time", "X-RateLimit-*"],
    )

    return app
