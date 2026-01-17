import pytest
from app.utils.validation import (
    validate_username,
    validate_password,
    validate_repository_url,
    validate_pagination_params,
    sanitize_html,
)


class TestValidationUtils:
    """Unit tests for validation utilities."""

    def test_validate_username_success(self):
        """Test valid username."""
        is_valid, error = validate_username("testuser123")
        assert is_valid is True
        assert error is None

    def test_validate_username_too_short(self):
        """Test username too short."""
        is_valid, error = validate_username("ab")
        assert is_valid is False
        assert "at least 3 characters" in error

    def test_validate_username_invalid_chars(self):
        """Test username with invalid characters."""
        is_valid, error = validate_username("test user!")
        assert is_valid is False
        assert "letters, numbers" in error

    def test_validate_password_success(self):
        """Test valid password."""
        is_valid, errors = validate_password("Test1234!")
        assert is_valid is True
        assert errors is None

    def test_validate_password_too_short(self):
        """Test password too short."""
        is_valid, errors = validate_password("Short1!")
        assert is_valid is False
        assert any("at least 8 characters" in e for e in errors)

    def test_validate_password_missing_uppercase(self):
        """Test password without uppercase."""
        is_valid, errors = validate_password("test1234!")
        assert is_valid is False
        assert any("uppercase" in e for e in errors)

    def test_validate_repository_url_github(self):
        """Test valid GitHub URL."""
        is_valid, error = validate_repository_url("https://github.com/nathadriele/test-project")
        assert is_valid is True
        assert error is None

    def test_validate_repository_url_invalid(self):
        """Test invalid repository URL."""
        is_valid, error = validate_repository_url("https://example.com/not-a-repo")
        assert is_valid is False
        assert error is not None

    def test_sanitize_html(self):
        """Test HTML sanitization."""
        dangerous = "<script>alert('xss')</script><p>Safe content</p>"
        safe = sanitize_html(dangerous)
        assert "<script" not in safe
        assert "<p>Safe content</p>" in safe

    def test_validate_pagination_params(self):
        """Test pagination parameter validation."""
        page, per_page = validate_pagination_params(page=0, per_page=150)
        assert page == 1  # Minimum
        assert per_page == 100  # Maximum

    def test_validate_pagination_params_normal(self):
        """Test normal pagination parameters."""
        page, per_page = validate_pagination_params(page=5, per_page=20)
        assert page == 5
        assert per_page == 20
