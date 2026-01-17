import re
import secrets
import string
from typing import Optional


def generate_random_string(length: int = 32) -> str:
    """Generate cryptographically secure random string."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_token(length: int = 32) -> str:
    """Generate secure random token."""
    return secrets.token_urlsafe(length)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    # Convert to lowercase
    text = text.lower()

    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)

    # Remove special characters except hyphens
    text = re.sub(r'[^\w\-]', '', text)

    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    return text


def extract_hashtags(text: str) -> list[str]:
    """Extract hashtags from text."""
    return re.findall(r'#(\w+)', text)


def extract_mentions(text: str) -> list[str]:
    """Extract mentions from text."""
    return re.findall(r'@(\w+)', text)


def mask_email(email: str) -> str:
    """Mask email for privacy."""
    if '@' not in email:
        return email

    username, domain = email.split('@', 1)
    if len(username) <= 2:
        masked_username = '*' * len(username)
    else:
        masked_username = username[0] + '*' * (len(username) - 2) + username[-1]

    return f"{masked_username}@{domain}"


def mask_string(s: str, visible_chars: int = 4) -> str:
    """Mask string showing only first and last few characters."""
    if len(s) <= visible_chars * 2:
        return '*' * len(s)
    return s[:visible_chars] + '*' * (len(s) - visible_chars * 2) + s[-visible_chars:]


def is_valid_url(url: str) -> bool:
    """Check if string is a valid URL."""
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(url) is not None


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text."""
    return ' '.join(text.split())
