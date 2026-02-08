"""
tests/test_export.py
Tests for the export API endpoints.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestExportJobs:
    """Tests for GET /export/jobs endpoint."""

    def test_export_json_format(self) -> None:
        """Test JSON export format."""
        response = client.get("/export/jobs?format=json")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert "attachment" in response.headers.get("content-disposition", "")

    def test_export_csv_format(self) -> None:
        """Test CSV export format."""
        response = client.get("/export/jobs?format=csv")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers.get("content-disposition", "")

    def test_export_invalid_format(self) -> None:
        """Test that invalid format returns error."""
        response = client.get("/export/jobs?format=xml")
        assert response.status_code == 422  # Validation error

    def test_export_with_filters(self) -> None:
        """Test that export accepts filter parameters."""
        response = client.get("/export/jobs?format=json&country_code=SE&source=arbetsformedlingen")
        assert response.status_code == 200
