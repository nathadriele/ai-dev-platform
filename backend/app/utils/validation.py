import re
from typing import Optional, List
from pydantic import EmailStr, ValidationError


def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """
    Validate username format.
    Returns (is_valid, error_message).
    """
    if not username:
        return False, "Username is required"

    if len(username) < 3:
        return False, "Username must be at least 3 characters long"

    if len(username) > 50:
        return False, "Username must be less than 50 characters"

    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"

    return True, None


def validate_password(password: str) -> tuple[bool, Optional[List[str]]]:
    """
    Validate password strength.
    Returns (is_valid, list_of_errors).
    """
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if len(password) > 100:
        errors.append("Password must be less than 100 characters")

    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")

    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")

    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one digit")

    return len(errors) == 0, errors if errors else None


def validate_repository_url(url: str) -> tuple[bool, Optional[str]]:
    """
    Validate GitHub/GitLab repository URL.
    Returns (is_valid, error_message).
    """
    if not url:
        return False, "Repository URL is required"

    # Common git repository patterns
    patterns = [
        r'^https?://github\.com/[\w-]+/[\w-]+/?$',
        r'^https?://gitlab\.com/[\w-]+/[\w-]+/?$',
        r'^https?://bitbucket\.org/[\w-]+/[\w-]+/?$',
        r'^git@github\.com:[\w-]+/[\w-]+\.git$',
    ]

    for pattern in patterns:
        if re.match(pattern, url):
            return True, None

    return False, "Invalid repository URL. Must be a valid GitHub, GitLab, or Bitbucket URL"


def sanitize_html(text: str) -> str:
    """Remove potentially dangerous HTML tags."""
    # Basic sanitization - in production, use a proper library like bleach
    dangerous_tags = ['<script', '</script', '<iframe', '</iframe', '<object', '</object']
    for tag in dangerous_tags:
        text = text.replace(tag, '')
    return text


def validate_pagination_params(
    page: int = 1,
    per_page: int = 20
) -> tuple[int, int]:
    """
    Validate and normalize pagination parameters.
    Returns (page, per_page).
    """
    page = max(1, min(page, 1000))  # Limit max page
    per_page = max(1, min(per_page, 100))  # Limit per page
    return page, per_page
