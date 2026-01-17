import os
import mimetypes
from typing import Optional, List
from pathlib import Path


def ensure_directory(path: str) -> None:
    """Ensure directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()


def get_mime_type(filename: str) -> str:
    """Get MIME type of file."""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"


def is_allowed_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """Check if file extension is in allowed list."""
    ext = get_file_extension(filename)
    return ext in [e.lower() if e.startswith('.') else f'.{e.lower()}' for e in allowed_extensions]


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing dangerous characters."""
    # Remove directory paths
    filename = os.path.basename(filename)

    # Replace dangerous characters
    dangerous_chars = ['..', '/', '\\', '\0', ' ', '\n', '\r', '\t']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')

    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')

    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file"

    return filename


def get_file_size(filepath: str) -> int:
    """Get file size in bytes."""
    return os.path.getsize(filepath)


def file_exists(filepath: str) -> bool:
    """Check if file exists."""
    return os.path.isfile(filepath)


def delete_file(filepath: str) -> bool:
    """Delete file if exists."""
    try:
        if file_exists(filepath):
            os.remove(filepath)
        return True
    except Exception:
        return False


def read_file(filepath: str, encoding: str = "utf-8") -> Optional[str]:
    """Read file content."""
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except Exception:
        return None


def write_file(filepath: str, content: str, encoding: str = "utf-8") -> bool:
    """Write content to file."""
    try:
        ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception:
        return False
