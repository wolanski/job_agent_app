"""
tests/test_api_jobs.py
Integration tests for the jobs API endpoints.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestListJobs:
    """Tests for GET /jobs endpoint."""

    def test_list_jobs_empty(self) -> None:
        """Test listing jobs when database is empty."""
        # Mock the database to return empty
        with patch("app.api.jobs.get_session") as mock_session:
            mock_session.return_value.__enter__ = lambda s: s
            mock_session.return_value.__exit__ = lambda s, *args: None
            mock_session.return_value.exec.return_value = iter([])

            response = client.get("/jobs")

        # Should return empty list with page_info
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["page_info"]["has_more"] is False

    def test_list_jobs_with_country_filter(self) -> None:
        """Test that country_code filter is applied."""
        response = client.get("/jobs?country_code=SE")
        # Will return empty but filter should be accepted
        assert response.status_code == 200

    def test_list_jobs_with_source_filter(self) -> None:
        """Test that source filter is applied."""
        response = client.get("/jobs?source=arbetsformedlingen")
        assert response.status_code == 200

    def test_list_jobs_with_search_query(self) -> None:
        """Test that search query is accepted."""
        response = client.get("/jobs?q=developer")
        assert response.status_code == 200

    def test_list_jobs_with_limit(self) -> None:
        """Test that limit parameter is accepted."""
        response = client.get("/jobs?limit=10")
        assert response.status_code == 200

    def test_list_jobs_limit_max(self) -> None:
        """Test that limit cannot exceed 200."""
        response = client.get("/jobs?limit=500")
        assert response.status_code == 422  # Validation error


class TestGetJobById:
    """Tests for GET /jobs/{job_id} endpoint."""

    def test_get_job_not_found(self) -> None:
        """Test getting a non-existent job returns 404."""
        response = client.get("/jobs/non-existent-id")
        assert response.status_code == 404


class TestHealthEndpoint:
    """Tests for health check."""

    def test_health_includes_time(self) -> None:
        """Test that health endpoint returns time_utc."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "time_utc" in data


class TestVersionEndpoint:
    """Tests for version endpoint."""

    def test_version_endpoint(self) -> None:
        """Test version metadata endpoint."""
        response = client.get("/meta/version")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
