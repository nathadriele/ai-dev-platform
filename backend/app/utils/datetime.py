from datetime import datetime, timedelta
from typing import Optional


def now_utc() -> datetime:
    """Get current UTC datetime."""
    return datetime.utcnow()


def add_days(dt: datetime, days: int) -> datetime:
    """Add days to datetime."""
    return dt + timedelta(days=days)


def add_hours(dt: datetime, hours: int) -> datetime:
    """Add hours to datetime."""
    return dt + timedelta(hours=hours)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string."""
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """Parse string to datetime."""
    try:
        return datetime.strptime(dt_str, format_str)
    except (ValueError, TypeError):
        return None


def get_age_in_days(dt: datetime) -> int:
    """Get age of datetime in days."""
    return (datetime.utcnow() - dt).days


def is_recent(dt: datetime, days: int = 7) -> bool:
    """Check if datetime is within recent N days."""
    return (datetime.utcnow() - dt).days <= days


def get_date_range_days(days: int) -> tuple[datetime, datetime]:
    """Get start and end datetime for past N days."""
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    return start, end
