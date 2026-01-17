# Filesystem MCP Server Integration

This document describes the Filesystem MCP (Model-Context Protocol) server integration for the AI-Assisted Developer Productivity Platform.

## Overview

The Filesystem MCP server allows the platform to:
- Read and analyze project files
- Traverse directory structures
- Search for specific patterns in code
- Generate file statistics
- Analyze code dependencies

## Configuration

### Register Filesystem MCP Server

```bash
curl -X POST http://localhost:8000/api/v1/mcp/servers \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "filesystem-local",
    "server_type": "filesystem",
    "endpoint": "http://localhost:3001",
    "capabilities": ["read", "list", "search", "analyze"]
  }'
```

## Available Operations

### 1. List Directory Contents

**Tool**: `filesystem.list_directory`

**Parameters**:
```json
{
  "path": "/home/nathadriele/Imagens/ai-dev/backend",
  "recursive": false,
  "include_hidden": false
}
```

**Response**:
```json
{
  "files": [
    {
      "name": "app",
      "type": "directory",
      "path": "/home/nathadriele/Imagens/ai-dev/backend/app"
    },
    {
      "name": "main.py",
      "type": "file",
      "path": "/home/nathadriele/Imagens/ai-dev/backend/main.py",
      "size": 1024
    }
  ]
}
```

### 2. Read File Content

**Tool**: `filesystem.read_file`

**Parameters**:
```json
{
  "path": "/home/nathadriele/Imagens/ai-dev/backend/app/main.py",
  "encoding": "utf-8"
}
```

**Response**:
```json
{
  "content": "from fastapi import FastAPI...",
  "lines": 50,
  "encoding": "utf-8"
}
```

### 3. Search Files

**Tool**: `filesystem.search_files`

**Parameters**:
```json
{
  "path": "/home/nathadriele/Imagens/ai-dev/backend",
  "pattern": "*.py",
  "search_content": "def test_",
  "exclude_dirs": ["__pycache__", "venv"]
}
```

**Response**:
```json
{
  "matches": [
    {
      "file": "tests/test_main.py",
      "line": 10,
      "content": "def test_health_endpoint():"
    }
  ]
}
```

### 4. Analyze Code Structure

**Tool**: `filesystem.analyze_code`

**Parameters**:
```json
{
  "path": "/home/nathadriele/Imagens/ai-dev/backend",
  "language": "python"
}
```

**Response**:
```json
{
  "modules": ["app", "app.api", "app.models"],
  "classes": ["User", "Project"],
  "functions": ["get_db", "create_access_token"],
  "imports": ["fastapi", "sqlalchemy"]
}
```

## MCP Server Implementation

The MCP server can be implemented as a separate service. Here's a basic implementation:

```python
from mcp import Server, types
from pathlib import Path
import os

server = Server("filesystem-server")

@server.tool("filesystem.list_directory")
async def list_directory(params: dict) -> dict:
    """List directory contents."""
    path = params.get("path", ".")
    recursive = params.get("recursive", False)

    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")

    files = []
    for item in Path(path).iterdir():
        files.append({
            "name": item.name,
            "type": "directory" if item.is_dir() else "file",
            "path": str(item),
            "size": item.stat().st_size if item.is_file() else None
        })

    return {"files": files}

@server.tool("filesystem.read_file")
async def read_file(params: dict) -> dict:
    """Read file content."""
    path = params["path"]
    encoding = params.get("encoding", "utf-8")

    if not os.path.isfile(path):
        raise ValueError(f"Not a file: {path}")

    with open(path, 'r', encoding=encoding) as f:
        content = f.read()

    return {
        "content": content,
        "lines": len(content.split('\n')),
        "encoding": encoding
    }

if __name__ == "__main__":
    server.run()
```

## Usage Examples

### Example 1: Analyze Project Structure

```python
from app.services.mcp_service import MCPService

mcp_service = MCPService()

result = await mcp_service.execute_tool(
    server_id="filesystem-local",
    tool_name="filesystem.analyze_code",
    parameters={
        "path": "/home/nathadriele/Imagens/ai-dev/backend",
        "language": "python"
    }
)

print(f"Found {len(result['modules'])} modules")
print(f"Found {len(result['classes'])} classes")
```

### Example 2: Search for Usage Pattern

```python
result = await mcp_service.execute_tool(
    server_id="filesystem-local",
    tool_name="filesystem.search_files",
    parameters={
        "path": "/home/nathadriele/Imagens/ai-dev/backend",
        "pattern": "*.py",
        "search_content": "from sqlalchemy import"
    }
)

for match in result["matches"]:
    print(f"{match['file']}: {match['line']}")
```

## Security Considerations

1. **Path Validation**: Always validate and sanitize file paths
2. **Access Control**: Restrict access to specific directories
3. **File Size Limits**: Implement limits on file reading
4. **Hidden Files**: Control access to hidden files (.env, etc.)
5. **Symbolic Links**: Handle symbolic links carefully to prevent path traversal

## Best Practices

1. **Caching**: Cache file contents to avoid repeated reads
2. **Async Operations**: Use async I/O for better performance
3. **Error Handling**: Handle file permission errors gracefully
4. **Logging**: Log all file system operations for auditing
5. **Rate Limiting**: Implement rate limiting to prevent abuse

