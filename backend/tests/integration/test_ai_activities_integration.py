import pytest
from httpx import AsyncClient


class TestAIActivitiesIntegration:
    """Integration tests for AI activities endpoints."""

    async def test_log_ai_activity(
        self,
        client: AsyncClient,
        auth_headers,
        test_project,
        sample_ai_activity_data
    ):
        """Test logging AI activity."""
        activity_data = {
            **sample_ai_activity_data,
            "project_id": str(test_project.id)
        }

        response = await client.post(
            "/api/v1/ai-activities",
            json=activity_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert "data" in data
        assert data["data"]["tool_used"] == sample_ai_activity_data["tool_used"]
        assert data["data"]["category"] == sample_ai_activity_data["category"]

    async def test_list_ai_activities(
        self,
        client: AsyncClient,
        auth_headers,
        test_project
    ):
        """Test listing AI activities."""
        response = await client.get(
            "/api/v1/ai-activities",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data

    async def test_get_ai_activity(
        self,
        client: AsyncClient,
        auth_headers,
        test_project,
        sample_ai_activity_data
    ):
        """Test getting specific AI activity."""
        activity_data = {
            **sample_ai_activity_data,
            "project_id": str(test_project.id)
        }
        create_response = await client.post(
            "/api/v1/ai-activities",
            json=activity_data,
            headers=auth_headers
        )
        activity_id = create_response.json()["data"]["id"]

        response = await client.get(
            f"/api/v1/ai-activities/{activity_id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "data" in data

    async def test_filter_by_tool(
        self,
        client: AsyncClient,
        auth_headers,
        test_project
    ):
        """Test filtering activities by tool."""
        response = await client.get(
            "/api/v1/ai-activities?tool_used=claude",
            headers=auth_headers
        )

        assert response.status_code == 200
