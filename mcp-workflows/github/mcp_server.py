"""
GitHub MCP Server Implementation

This server provides GitHub API operations for AI agents.
"""
from typing import Dict, List, Optional
import httpx
from mcp import Server

server = Server("github-mcp-server", version="1.0.0")

# Configuration
GITHUB_API_BASE = "https://api.github.com"


@server.tool("github.get_repo")
async def get_repo(params: Dict) -> Dict:
    """Get repository information."""
    owner = params["owner"]
    repo = params["repo"]
    token = params.get("token")

    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()


@server.tool("github.get_commits")
async def get_commits(params: Dict) -> List[Dict]:
    """Get recent commits."""
    owner = params["owner"]
    repo = params["repo"]
    per_page = params.get("per_page", 10)
    token = params.get("token")

    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits",
            headers=headers,
            params={"per_page": per_page}
        )
        response.raise_for_status()
        return response.json()


@server.tool("github.get_diff")
async def get_diff(params: Dict) -> Dict:
    """Get commit diff."""
    owner = params["owner"]
    repo = params["repo"]
    sha = params["sha"]
    token = params.get("token")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Accept": "application/vnd.github.diff",  # Get diff format
    }
    if token:
        headers["Authorization"] = f"token {token}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits/{sha}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()


@server.tool("github.get_pulls")
async def get_pulls(params: Dict) -> List[Dict]:
    """Get pull requests."""
    owner = params["owner"]
    repo = params["repo"]
    state = params.get("state", "open")
    token = params.get("token")

    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls",
            headers=headers,
            params={"state": state}
        )
        response.raise_for_status()
        return response.json()


@server.tool("github.get_pr_files")
async def get_pr_files(params: Dict) -> List[Dict]:
    """Get files changed in a pull request."""
    owner = params["owner"]
    repo = params["repo"]
    pull_number = params["pull_number"]
    token = params.get("token")

    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls/{pull_number}/files",
            headers=headers
        )
        response.raise_for_status()
        return response.json()


@server.tool("github.create_issue")
async def create_issue(params: Dict) -> Dict:
    """Create a new issue."""
    owner = params["owner"]
    repo = params["repo"]
    title = params["title"]
    body = params.get("body", "")
    labels = params.get("labels", [])
    token = params.get("token")

    if not token:
        raise ValueError("Token required for creating issues")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }

    data = {
        "title": title,
        "body": body,
    }
    if labels:
        data["labels"] = labels

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()


@server.tool("github.create_comment")
async def create_comment(params: Dict) -> Dict:
    """Create a comment on an issue or PR."""
    owner = params["owner"]
    repo = params["repo"]
    issue_number = params["issue_number"]
    body = params["body"]
    token = params.get("token")

    if not token:
        raise ValueError("Token required for creating comments")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }

    data = {"body": body}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues/{issue_number}/comments",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()


@server.tool("github.get_languages")
async def get_languages(params: Dict) -> Dict[str, int]:
    """Get repository languages."""
    owner = params["owner"]
    repo = params["repo"]
    token = params.get("token")

    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/languages",
            headers=headers
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    import uvicorn

    print("Starting GitHub MCP Server...")
    print("GitHub API Base:", GITHUB_API_BASE)

    uvicorn.run(
        server,
        host="0.0.0.0",
        port=3002,
        log_level="info"
    )
