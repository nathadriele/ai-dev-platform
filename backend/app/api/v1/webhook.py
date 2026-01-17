"""
GitHub Webhook Endpoints

Handle GitHub webhook events for CI/CD integration.
"""
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import hmac
import hashlib
from app.core.database import get_db
from app.core.config import settings
from app.services.github_service import GitHubService
from app.models.pipeline import PipelineExecution, PipelineStatus
from app.models.project import Project
from sqlalchemy import select
import uuid

router = APIRouter()


async def verify_github_signature(payload: bytes, signature: str) -> bool:
    """Verify GitHub webhook signature."""
    if not settings.github_webhook_secret:
        return False

    hash_algorithm, github_signature = signature.split('=', 1)
    algorithm = hashlib.sha256

    mac = hmac.new(
        settings.github_webhook_secret.encode(),
        msg=payload,
        digestmod=algorithm
    )

    return hmac.compare_digest(mac.hexdigest(), github_signature)


@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Handle GitHub webhook events."""
    # Get raw payload
    payload = await request.body()

    # Verify signature if secret is configured
    signature = request.headers.get("x-hub-signature-256")
    if signature and settings.github_webhook_secret:
        if not await verify_github_signature(payload, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse event data
    event_data = await request.json()
    event_type = request.headers.get("x-github-event")

    # Handle different event types
    if event_type == "push":
        background_tasks.add_task(handle_push_event, event_data, db)
    elif event_type == "pull_request":
        background_tasks.add_task(handle_pull_request_event, event_data, db)
    elif event_type == "ping":
        return {"message": "pong"}

    return {"message": "Webhook received"}


async def handle_push_event(event_data: Dict[str, Any], db: AsyncSession):
    """Handle push event (trigger CI/CD pipeline)."""
    try:
        repo_full_name = event_data["repository"]["full_name"]
        ref = event_data["ref"]
        branch = ref.split("/")[-1] if "/" in ref else ref
        commit_sha = event_data["after"]
        pusher = event_data["pusher"]["name"]

        # Find project by repository URL
        result = await db.execute(
            select(Project).where(
                Project.repository_url.contains(repo_full_name)
            )
        )
        project = result.scalar_one_or_none()

        if not project:
            return

        # Create pipeline execution
        pipeline = PipelineExecution(
            id=uuid.uuid4(),
            project_id=str(project.id),
            pipeline_name="ci-pipeline",
            status=PipelineStatus.RUNNING,
            commit_sha=commit_sha,
            branch=branch,
            triggered_by=pusher,
        )

        db.add(pipeline)
        await db.commit()

        # TODO: Trigger actual CI/CD pipeline
        # This would involve calling the CI/CD system

    except Exception as e:
        print(f"Error handling push event: {e}")


async def handle_pull_request_event(event_data: Dict[str, Any], db: AsyncSession):
    """Handle pull request event."""
    try:
        action = event_data["action"]
        pr = event_data["pull_request"]
        repo_full_name = event_data["repository"]["full_name"]

        # Only handle opened and synchronize events
        if action not in ["opened", "synchronize"]:
            return

        # TODO: Trigger PR analysis with AI
        # This could involve:
        # 1. Fetching PR diff
        # 2. Analyzing changes
        # 3. Generating PR summary
        # 4. Posting comment on PR

    except Exception as e:
        print(f"Error handling PR event: {e}")


@router.post("/webhook/github/test")
async def test_webhook():
    """Test endpoint to verify webhook is accessible."""
    return {
        "status": "active",
        "message": "GitHub webhook endpoint is ready"
    }


@router.get("/webhook/github/config")
async def get_webhook_config():
    """Get webhook configuration details."""
    return {
        "url": "/api/v1/webhook/github",
        "events": ["push", "pull_request", "ping"],
        "content_type": "json",
        "secret_configured": bool(settings.github_webhook_secret)
    }
