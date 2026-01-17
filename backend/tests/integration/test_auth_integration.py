import pytest
from httpx import AsyncClient


class TestAuthIntegration:
    """Integration tests for authentication endpoints."""

    async def test_register_user(self, client: AsyncClient, sample_user_data):
        """Test user registration."""
        response = await client.post("/api/v1/auth/register", json=sample_user_data)

        assert response.status_code == 201
        data = response.json()
        assert "data" in data
        assert "tokens" in data
        assert data["data"]["email"] == sample_user_data["email"]
        assert data["data"]["username"] == sample_user_data["username"]
        assert "access_token" in data["tokens"]
        assert "refresh_token" in data["tokens"]

    async def test_register_duplicate_email(self, client: AsyncClient, sample_user_data):
        """Test registration with duplicate email."""
        await client.post("/api/v1/auth/register", json=sample_user_data)

        response = await client.post("/api/v1/auth/register", json=sample_user_data)

        assert response.status_code == 409
        assert "error" in response.json()

    async def test_login_success(self, client: AsyncClient, sample_user_data):
        """Test successful login."""
        await client.post("/api/v1/auth/register", json=sample_user_data)

        response = await client.post("/api/v1/auth/login", json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        })

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "tokens" in data
        assert "access_token" in data["tokens"]

    async def test_login_invalid_credentials(self, client: AsyncClient, sample_user_data):
        """Test login with invalid credentials."""
        response = await client.post("/api/v1/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        })

        assert response.status_code == 401
        assert "error" in response.json()

    async def test_refresh_token(self, client: AsyncClient, sample_user_data):
        """Test token refresh."""
        await client.post("/api/v1/auth/register", json=sample_user_data)

        login_response = await client.post("/api/v1/auth/login", json={
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        })
        refresh_token = login_response.json()["tokens"]["refresh_token"]

        response = await client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh_token
        })

        assert response.status_code == 200
        assert "access_token" in response.json()
