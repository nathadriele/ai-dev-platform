"""
Filesystem MCP Server Implementation

This server provides filesystem operations for AI agents.
Run with: python mcp_server.py
"""
from typing import Dict, List, Optional
import os
import re
from pathlib import Path
from mcp import Server, types

server = Server("filesystem-mcp-server", version="1.0.0")

ALLOWED_BASE_PATHS = [
    "/home/nathadriele/Imagens/ai-dev",
    "/tmp/ai-dev-workspace"
]
MAX_FILE_SIZE = 1024 * 1024 


def validate_path(path: str) -> bool:
    """Validate that path is within allowed directories."""
    real_path = os.path.realpath(path)

    for base in ALLOWED_BASE_PATHS:
        real_base = os.path.realpath(base)
        if real_path.startswith(real_base):
            return True

    return False


@server.tool("filesystem.list_directory")
async def list_directory(params: Dict) -> Dict:
    """List contents of a directory."""
    path = params.get("path", ".")
    recursive = params.get("recursive", False)
    include_hidden = params.get("include_hidden", False)

    # Validate path
    if not validate_path(path):
        raise ValueError(f"Access denied: {path}")

    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")

    if not os.path.isdir(path):
        raise ValueError(f"Not a directory: {path}")

    files = []

    try:
        for item in Path(path).iterdir():
            if not include_hidden and item.name.startswith('.'):
                continue

            file_info = {
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "path": str(item),
            }

            if item.is_file():
                file_info["size"] = item.stat().st_size
                file_info["modified"] = item.stat().st_mtime

            files.append(file_info)

            if recursive and item.is_dir():
                sub_files = await list_directory({
                    "path": str(item),
                    "recursive": True,
                    "include_hidden": include_hidden
                })
                files.extend(sub_files["files"])

        return {"files": files}

    except PermissionError:
        raise ValueError(f"Permission denied: {path}")


@server.tool("filesystem.read_file")
async def read_file(params: Dict) -> Dict:
    """Read content of a file."""
    path = params["path"]
    encoding = params.get("encoding", "utf-8")
    max_lines = params.get("max_lines", None)

    if not validate_path(path):
        raise ValueError(f"Access denied: {path}")

    if not os.path.exists(path):
        raise ValueError(f"File does not exist: {path}")

    if not os.path.isfile(path):
        raise ValueError(f"Not a file: {path}")

    file_size = os.path.getsize(path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {file_size} bytes")

    try:
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()

        if max_lines:
            lines = content.split('\n')[:max_lines]
            content = '\n'.join(lines)

        return {
            "content": content,
            "lines": len(content.split('\n')),
            "size": file_size,
            "encoding": encoding
        }

    except UnicodeDecodeError:
        raise ValueError(f"Cannot decode file with {encoding}")
    except PermissionError:
        raise ValueError(f"Permission denied: {path}")


@server.tool("filesystem.search_files")
async def search_files(params: Dict) -> Dict:
    """Search for files matching pattern."""
    path = params.get("path", ".")
    pattern = params.get("pattern", "*")
    search_content = params.get("search_content", None)
    exclude_dirs = params.get("exclude_dirs", [])

    # Validate path
    if not validate_path(path):
        raise ValueError(f"Access denied: {path}")

    matches = []

    try:
        for root, dirs, files in os.walk(path):
            # Filter excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            # Match files by pattern
            for filename in files:
                if re.match(pattern.replace("*", ".*"), filename):
                    file_path = os.path.join(root, filename)

                    if search_content:
                        # Search within file
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                for line_num, line in enumerate(f, 1):
                                    if search_content in line:
                                        matches.append({
                                            "file": file_path,
                                            "line": line_num,
                                            "content": line.strip()
                                        })
                        except (UnicodeDecodeError, PermissionError):
                            continue
                    else:
                        matches.append({
                            "file": file_path
                        })

        return {"matches": matches}

    except PermissionError:
        raise ValueError(f"Permission denied: {path}")


@server.tool("filesystem.analyze_code")
async def analyze_code(params: Dict) -> Dict:
    """Analyze code structure in directory."""
    path = params.get("path", ".")
    language = params.get("language", "python")

    # Validate path
    if not validate_path(path):
        raise ValueError(f"Access denied: {path}")

    # Language-specific patterns
    patterns = {
        "python": {
            "classes": r"^class\s+(\w+)",
            "functions": r"^def\s+(\w+)",
            "imports": r"^from\s+(\S+)\s+import|^import\s+(\S+)"
        },
        "typescript": {
            "classes": r"class\s+(\w+)",
            "functions": r"function\s+(\w+)|(?:const|let)\s+(\w+)\s*=\s*\([^)]*\)\s*=>",
            "imports": r"import.*from\s+['\"]([^'\"]+)['\"]"
        }
    }

    lang_patterns = patterns.get(language, patterns["python"])

    modules = set()
    classes = []
    functions = []
    imports = set()

    # Find all relevant files
    extensions = {
        "python": ".py",
        "typescript": ".ts,.tsx"
    }

    ext = extensions.get(language, ".py")

    try:
        for root, dirs, files in os.walk(path):
            # Skip common exclusions
            dirs[:] = [d for d in dirs if d not in [
                "__pycache__", "node_modules", ".git", "venv", "dist"
            ]]

            for filename in files:
                if filename.endswith(ext.split(",")):
                    file_path = os.path.join(root, filename)
                    module = file_path.replace(path, "").replace("/", ".").replace(ext, "")
                    modules.add(module)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                # Match classes
                                if class_match := re.match(lang_patterns["classes"], line):
                                    classes.append(class_match.group(1))

                                # Match functions
                                if func_match := re.match(lang_patterns["functions"], line):
                                    func_name = func_match.group(1) or func_match.group(2)
                                    if func_name:
                                        functions.append(func_name)

                                # Match imports
                                if import_match := re.match(lang_patterns["imports"], line):
                                    import_name = import_match.group(1) or import_match.group(2)
                                    if import_name:
                                        imports.add(import_name.split(".")[0])

                    except (UnicodeDecodeError, PermissionError):
                        continue

        return {
            "modules": sorted(list(modules)),
            "classes": sorted(set(classes)),
            "functions": sorted(set(functions)),
            "imports": sorted(list(imports))
        }

    except PermissionError:
        raise ValueError(f"Permission denied: {path}")


@server.tool("filesystem.get_stats")
async def get_stats(params: Dict) -> Dict:
    """Get statistics about a directory."""
    path = params.get("path", ".")

    # Validate path
    if not validate_path(path):
        raise ValueError(f"Access denied: {path}")

    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")

    total_files = 0
    total_dirs = 0
    total_size = 0
    file_types = {}

    try:
        for root, dirs, files in os.walk(path):
            # Skip common exclusions
            dirs[:] = [d for d in dirs if d not in [
                "__pycache__", "node_modules", ".git", "venv", "dist"
            ]]

            total_dirs += len(dirs)

            for filename in files:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):
                    total_files += 1
                    size = os.path.getsize(file_path)
                    total_size += size

                    # Count file types
                    ext = os.path.splitext(filename)[1].lower()
                    file_types[ext] = file_types.get(ext, 0) + 1

        return {
            "total_files": total_files,
            "total_dirs": total_dirs,
            "total_size": total_size,
            "file_types": file_types
        }

    except PermissionError:
        raise ValueError(f"Permission denied: {path}")


if __name__ == "__main__":
    import uvicorn

    print("Starting Filesystem MCP Server...")
    print(f"Allowed paths: {ALLOWED_BASE_PATHS}")
    print(f"Max file size: {MAX_FILE_SIZE} bytes")

    # Run server
    uvicorn.run(
        server,
        host="0.0.0.0",
        port=3001,
        log_level="info"
    )
