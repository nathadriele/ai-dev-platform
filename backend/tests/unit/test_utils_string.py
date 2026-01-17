import pytest
from app.utils.string import (
    generate_random_string,
    generate_token,
    truncate_text,
    slugify,
    extract_hashtags,
    extract_mentions,
    mask_email,
    is_valid_url,
    normalize_whitespace,
)


class TestStringUtils:
    """Unit tests for string utilities."""

    def test_generate_random_string(self):
        """Test random string generation."""
        s = generate_random_string(16)
        assert len(s) == 16
        assert s.isalnum()

    def test_generate_token(self):
        """Test token generation."""
        token = generate_token()
        assert len(token) > 0
        assert isinstance(token, str)

    def test_truncate_text_no_truncation(self):
        """Test text truncation when not needed."""
        text = "Short text"
        result = truncate_text(text, 20)
        assert result == text

    def test_truncate_text_with_truncation(self):
        """Test text truncation."""
        text = "This is a very long text that should be truncated"
        result = truncate_text(text, 20)
        assert len(result) <= 23  # 20 + "..."
        assert result.endswith("...")

    def test_slugify(self):
        """Test slugify function."""
        text = "Hello World! This is a Test"
        slug = slugify(text)
        assert slug == "hello-world-this-is-a-test"

    def test_slugify_special_chars(self):
        """Test slugify with special characters."""
        text = "Hello @#$ World"
        slug = slugify(text)
        assert slug == "hello-world"

    def test_extract_hashtags(self):
        """Test hashtag extraction."""
        text = "This is #awesome and #great #coding"
        tags = extract_hashtags(text)
        assert "awesome" in tags
        assert "great" in tags
        assert "coding" in tags

    def test_extract_mentions(self):
        """Test mention extraction."""
        text = "Hey @user1 and @user2 check this"
        mentions = extract_mentions(text)
        assert "user1" in mentions
        assert "user2" in mentions

    def test_mask_email(self):
        """Test email masking."""
        email = "testuser@example.com"
        masked = mask_email(email)
        assert "@" in masked
        assert "testuser" not in masked

    def test_is_valid_url_http(self):
        """Test valid HTTP URL."""
        assert is_valid_url("http://example.com") is True

    def test_is_valid_url_https(self):
        """Test valid HTTPS URL."""
        assert is_valid_url("https://example.com") is True

    def test_is_valid_url_invalid(self):
        """Test invalid URL."""
        assert is_valid_url("not-a-url") is False

    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        text = "This   has    weird   whitespace"
        normalized = normalize_whitespace(text)
        assert normalized == "This has weird whitespace"
