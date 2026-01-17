import pytest
from httpx import AsyncClient


class TestProjectsIntegration:
    """Integration tests for projects endpoints."""

    async def test_create_project(self, client: AsyncClient, auth_headers, sample_project_data):
        """Test project creation."""
        response = await client.post(
            "/api/v1/projects",
            json=sample_project_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert "data" in data
        assert data["data"]["name"] == sample_project_data["name"]
        assert data["data"]["repository_url"] == sample_project_data["repository_url"]

    async def test_list_projects(self, client: AsyncClient, auth_headers, test_project):
        """Test listing projects."""
        response = await client.get("/api/v1/projects", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert isinstance(data["data"], list)

    async def test_get_project(self, client: AsyncClient, auth_headers, test_project):
        """Test getting a specific project."""
        response = await client.get(
            f"/api/v1/projects/{test_project.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert data["data"]["id"] == str(test_project.id)

    async def test_update_project(self, client: AsyncClient, auth_headers, test_project):
        """Test updating a project."""
        update_data = {"name": "Updated Project Name"}
        response = await client.put(
            f"/api/v1/projects/{test_project.id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["data"]["name"] == update_data["name"]

    async def test_delete_project(self, client: AsyncClient, auth_headers, test_project):
        """Test deleting a project."""
        response = await client.delete(
            f"/api/v1/projects/{test_project.id}",
            headers=auth_headers
        )

        assert response.status_code == 204

    async def test_search_projects(self, client: AsyncClient, auth_headers, test_project):
        """Test searching projects."""
        response = await client.get(
            "/api/v1/projects?search=Test",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
