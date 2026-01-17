"""
GitHub Integration Service

This service handles GitHub API interactions for the platform.
"""
import os
from typing import Dict, List, Optional
import httpx
from app.core.config import settings


class GitHubService:
    """Service for GitHub API operations."""

    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub service."""
        self.token = token or settings.github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict:
        """Make authenticated request to GitHub API."""
        url = f"{self.base_url}/{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()

    async def get_user(self, username: str) -> Dict:
        """Get user information."""
        return await self._request("GET", f"users/{username}")

    async def get_user_repos(
        self,
        username: str,
        repo_type: str = "all"
    ) -> List[Dict]:
        """Get user repositories."""
        params = {"type": repo_type}
        return await self._request(
            "GET",
            f"users/{username}/repos",
            params=params
        )

    async def get_repo(self, owner: str, repo: str) -> Dict:
        """Get repository information."""
        return await self._request("GET", f"repos/{owner}/{repo}")

    async def get_repo_commits(
        self,
        owner: str,
        repo: str,
        per_page: int = 10
    ) -> List[Dict]:
        """Get recent commits."""
        params = {"per_page": per_page}
        return await self._request(
            "GET",
            f"repos/{owner}/{repo}/commits",
            params=params
        )

    async def get_commit_diff(
        self,
        owner: str,
        repo: str,
        sha: str
    ) -> Dict:
        """Get commit diff."""
        return await self._request(
            "GET",
            f"repos/{owner}/{repo}/commits/{sha}"
        )

    async def get_repo_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open"
    ) -> List[Dict]:
        """Get repository issues."""
        params = {"state": state}
        return await self._request(
            "GET",
            f"repos/{owner}/{repo}/issues",
            params=params
        )

    async def get_repo_pulls(
        self,
        owner: str,
        repo: str,
        state: str = "open"
    ) -> List[Dict]:
        """Get repository pull requests."""
        params = {"state": state}
        return await self._request(
            "GET",
            f"repos/{owner}/{repo}/pulls",
            params=params
        )

    async def get_pull_files(
        self,
        owner: str,
        repo: str,
        pull_number: int
    ) -> List[Dict]:
        """Get files changed in a pull request."""
        return await self._request(
            "GET",
            f"repos/{owner}/{repo}/pulls/{pull_number}/files"
        )

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None
    ) -> Dict:
        """Create a new issue."""
        data = {
            "title": title,
            "body": body,
        }
        if labels:
            data["labels"] = labels

        return await self._request(
            "POST",
            f"repos/{owner}/{repo}/issues",
            json=data
        )

    async def create_comment(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        body: str
    ) -> Dict:
        """Create a comment on an issue or PR."""
        data = {"body": body}
        return await self._request(
            "POST",
            f"repos/{owner}/{repo}/issues/{issue_number}/comments",
            json=data
        )

    async def get_repo_languages(
        self,
        owner: str,
        repo: str
    ) -> Dict[str, int]:
        """Get repository languages."""
        return await self._request("GET", f"repos/{owner}/{repo}/languages")

    async def get_webhook(
        self,
        owner: str,
        repo: str,
        hook_id: int
    ) -> Dict:
        """Get webhook configuration."""
        return await self._request(
            "GET",
            f"repos/{owner}/{repo}/hooks/{hook_id}"
        )

    async def create_webhook(
        self,
        owner: str,
        repo: str,
        webhook_url: str,
        events: List[str],
        secret: Optional[str] = None
    ) -> Dict:
        """Create a webhook."""
        data = {
            "name": "web",
            "active": True,
            "events": events,
            "config": {
                "url": webhook_url,
                "content_type": "json",
            }
        }

        if secret:
            data["config"]["secret"] = secret

        return await self._request(
            "POST",
            f"repos/{owner}/{repo}/hooks",
            json=data
        )

    async def parse_repository_url(self, repo_url: str) -> tuple[str, str]:
        """Parse GitHub URL to get owner and repo."""
        # Remove .git suffix if present
        repo_url = repo_url.rstrip('.git')

        # Parse URL
        if "github.com/" in repo_url:
            parts = repo_url.split("github.com/")[-1].split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]

        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")

    async def get_repo_tree(
        self,
        owner: str,
        repo: str,
        branch: str = "main"
    ) -> List[Dict]:
        """Get repository tree structure."""
        # First get the default branch commit
        repo_info = await self.get_repo(owner, repo)
        default_branch = repo_info.get("default_branch", "main")

        # Get the tree
        return await self._request(
            "GET",
            f"repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
        )
