# GitHub MCP Server Integration

## Overview

The GitHub MCP server integrates with GitHub API to provide:
- Repository information and metadata
- Commit history and diffs
- Issue and PR tracking
- File content access
- Webhook management

## Configuration

### Environment Variables

```bash
GITHUB_TOKEN=ghp_your_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret
```

### Register GitHub MCP Server

```bash
curl -X POST http://localhost:8000/api/v1/mcp/servers \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "github-api",
    "server_type": "github",
    "endpoint": "https://api.github.com",
    "capabilities": ["read:repo", "read:commits", "read:issues"]
  }'
```

## Available Operations

### 1. Get Repository Info

**Tool**: `github.get_repo`

**Parameters**:
```json
{
  "owner": "nathadriele",
  "repo": "ai-dev-platform"
}
```

**Response**:
```json
{
  "name": "ai-dev-platform",
  "full_name": "nathadriele/ai-dev-platform",
  "description": "AI-Assisted Developer Productivity Platform",
  "private": false,
  "language": "TypeScript",
  "stars": 42,
  "forks": 8
}
```

### 2. Get Recent Commits

**Tool**: `github.get_commits`

**Parameters**:
```json
{
  "owner": "nathadriele",
  "repo": "ai-dev-platform",
  "per_page": 10
}
```

### 3. Get Commit Diff

**Tool**: `github.get_diff`

**Parameters**:
```json
{
  "owner": "nathadriele",
  "repo": "ai-dev-platform",
  "sha": "abc123"
}
```

### 4. Get Pull Requests

**Tool**: `github.get_pulls`

**Parameters**:
```json
{
  "owner": "nathadriele",
  "repo": "ai-dev-platform",
  "state": "open"
}
```

### 5. Get PR Files

**Tool**: `github.get_pr_files`

**Parameters**:
```json
{
  "owner": "nathadriele",
  "repo": "ai-dev-platform",
  "pull_number": 42
}
```

### 6. Create Issue

**Tool**: `github.create_issue`

**Parameters**:
```json
{
  "owner": "nathadriele",
  "repo": "ai-dev-platform",
  "title": "Feature: Add dark mode",
  "body": "It would be great to have dark mode support...",
  "labels": ["enhancement", "good first issue"]
}
```

### 7. Create PR Comment

**Tool**: `github.create_comment`

**Parameters**:
```json
{
  "owner": "nathadriele",
  "repo": "ai-dev-platform",
  "issue_number": 42,
  "body": "Great work on this PR! Just a few suggestions..."
}
```

## Webhook Integration

### Setting Up Webhook

1. Go to your GitHub repository settings
2. Navigate to Webhooks → Add webhook
3. Configure:
   - **Payload URL**: `https://your-domain.com/api/v1/webhook/github`
   - **Content type**: `application/json`
   - **Secret**: Your webhook secret
   - **Events**: Pushes, Pull requests

### Webhook Events

#### Push Event

Triggered when code is pushed to repository.

**Use Case**: Trigger CI/CD pipeline

```python
{
  "ref": "refs/heads/main",
  "repository": {
    "full_name": "nathadriele/ai-dev-platform"
  },
  "pusher": {
    "name": "nathadriele"
  },
  "after": "abc123..."
}
```

#### Pull Request Event

Triggered when PR is opened or updated.

**Use Case**: Generate AI PR summary

```python
{
  "action": "opened",
  "pull_request": {
    "number": 42,
    "title": "Add new feature",
    "body": "Description..."
  }
}
```

## Implementation Examples

### Example 1: Get Project Repository Info

```python
from app.services.github_service import GitHubService

github_service = GitHubService()

# Parse repository URL
owner, repo = await github_service.parse_repository_url(
    "https://github.com/nathadriele/ai-dev-platform"
)

# Get repository info
repo_info = await github_service.get_repo(owner, repo)
print(f"Repository: {repo_info['full_name']}")
print(f"Stars: {repo_info['stargazers_count']}")
```

### Example 2: Get Recent Commits

```python
# Get last 10 commits
commits = await github_service.get_repo_commits(owner, repo, per_page=10)

for commit in commits:
    print(f"{commit['sha'][:7]}: {commit['commit']['message']}")
```

### Example 3: Analyze PR with AI

```python
# Get PR files
files = await github_service.get_pull_files(owner, repo, pr_number)

# Analyze changes
for file in files:
    print(f"File: {file['filename']}")
    print(f"Changes: +{file['additions']} -{file['deletions']}")
    print(f"Status: {file['status']}")

# TODO: Send to AI for analysis
```

### Example 4: Create Automated PR Comment

```python
# Generate PR summary with AI
summary = await ai_service.generate_pr_summary(pr_data)

# Post comment on PR
await github_service.create_comment(
    owner=owner,
    repo=repo,
    issue_number=pr_number,
    body=summary
)
```

## Integration with AI Agents

### Code Review Agent

```python
async def review_pr(owner: str, repo: str, pr_number: int):
    """Review a pull request using AI."""
    # Get PR diff
    pr_files = await github_service.get_pull_files(owner, repo, pr_number)

    # Analyze with AI
    for file in pr_files:
        patch = file['patch']

        review = await ai_code_reviewer.execute(
            task_description=f"Review this code change:\n{patch}",
            input_data={"filename": file['filename']}
        )

        # Post review comments
        if review.get("issues"):
            await github_service.create_comment(
                owner, repo, pr_number,
                body=format_review_comment(review)
            )
```

### Documentation Generator Agent

```python
async def generate_docs_from_repo(owner: str, repo: str):
    """Generate documentation from repository."""
    # Get repository structure
    tree = await github_service.get_repo_tree(owner, repo)

    # Analyze code structure
    for item in tree['tree']:
        if item['type'] == 'blob' and item['path'].endswith('.py'):
            # Get file content
            content = await github_service.get_raw_file(
                owner, repo, item['path']
            )

            # Generate documentation
            docs = await doc_generator.execute(
                task_description=f"Generate docs for:\n{content}",
                input_data={"filename": item['path']}
            )
```

## Security Considerations

1. **Token Storage**: Never expose GitHub tokens in logs
2. **Rate Limiting**: Respect GitHub API rate limits (5000/hour authenticated)
3. **Webhook Secrets**: Always verify webhook signatures
4. **Permissions**: Use minimum required permissions (read-only preferably)
5. **IP Whitelisting**: Restrict webhook IPs if possible

## Rate Limiting

GitHub API has rate limits:
- **Authenticated**: 5000 requests/hour
- **Unauthenticated**: 60 requests/hour

Monitor usage:
```python
response = await github_service._request(...)
remaining = response.headers.get("x-ratelimit-remaining")
reset = response.headers.get("x-ratelimit-reset")
```

## Troubleshooting

### 401 Unauthorized

**Error**: "Bad credentials"

**Solution**: Verify GitHub token is valid and not expired

### 403 Forbidden

**Error**: "API rate limit exceeded"

**Solution**: Implement rate limiting or use authenticated requests

### 404 Not Found

**Error**: "Repository not found"

**Solution**: Verify owner/repo name and token has access permissions

### Webhook Not Triggering

**Error**: Webhooks not being received

**Solutions**:
- Verify webhook URL is accessible
- Check webhook secret matches
- Ensure correct events are selected
- Check GitHub webhook delivery logs
