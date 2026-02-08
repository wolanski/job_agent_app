"""
tests/test_adapters.py
Unit tests for source adapters with mocked HTTP responses.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.adapters.arbetsformedlingen import ArbetsformedlingenAdapter
from app.adapters.base import RawJobPosting


class TestArbetsformedlingenAdapter:
    """Tests for Arbetsförmedlingen adapter."""

    @pytest.fixture
    def sample_ad(self) -> dict:
        """Sample ad from Arbetsförmedlingen API."""
        return {
            "id": "12345678",
            "headline": "Software Developer",
            "description": {"text": "We are looking for a developer..."},
            "employer": {"name": "Tech Corp AB"},
            "workplace_address": {
                "city": "Stockholm",
                "region": "Stockholms län",
                "postcode": "111 22",
            },
            "application_details": {"url": "https://example.com/apply"},
            "publication_date": "2026-02-01T10:00:00Z",
            "last_publication_date": "2026-03-01T23:59:59Z",
            "employment_type": {"label": "full_time"},
            "occupation_group": {
                "legacy_ams_taxonomy_id": "1234",
                "label": "Mjukvaruutvecklare",
            },
        }

    def test_source_name(self) -> None:
        """Test that source name is correct."""
        adapter = ArbetsformedlingenAdapter()
        assert adapter.source_name == "arbetsformedlingen"

    def test_transform_ad(self, sample_ad: dict) -> None:
        """Test transforming a raw ad to RawJobPosting."""
        adapter = ArbetsformedlingenAdapter()
        result = adapter._transform_ad(sample_ad)

        assert isinstance(result, RawJobPosting)
        assert result.source == "arbetsformedlingen"
        assert result.external_id == "12345678"
        assert result.title == "Software Developer"
        assert result.company_name == "Tech Corp AB"
        assert result.country_code == "SE"
        assert result.city == "Stockholm"
        assert result.apply_url == "https://example.com/apply"

    def test_transform_ad_minimal(self) -> None:
        """Test transforming an ad with minimal fields."""
        adapter = ArbetsformedlingenAdapter()
        minimal_ad = {
            "id": "99999",
            "headline": "Job Title",
        }
        result = adapter._transform_ad(minimal_ad)

        assert result.external_id == "99999"
        assert result.title == "Job Title"
        assert result.description is None
        assert result.company_name is None

    @patch("httpx.Client.get")
    def test_fetch_snapshot_single_page(self, mock_get: MagicMock, sample_ad: dict) -> None:
        """Test fetching snapshot with single page of results."""
        mock_response = MagicMock()
        mock_response.json.return_value = [sample_ad]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        adapter = ArbetsformedlingenAdapter()
        jobs = list(adapter.fetch_snapshot())

        assert len(jobs) == 1
        assert jobs[0].external_id == "12345678"

    @patch("httpx.Client.get")
    def test_fetch_snapshot_empty(self, mock_get: MagicMock) -> None:
        """Test fetching snapshot with no results."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        adapter = ArbetsformedlingenAdapter()
        jobs = list(adapter.fetch_snapshot())

        assert len(jobs) == 0

    def test_parse_timestamp_valid(self) -> None:
        """Test parsing valid ISO timestamp."""
        adapter = ArbetsformedlingenAdapter()
        result = adapter._parse_timestamp("2026-02-08T12:00:00Z")
        assert result is not None
        assert result.year == 2026
        assert result.month == 2
        assert result.day == 8

    def test_parse_timestamp_none(self) -> None:
        """Test parsing None timestamp."""
        adapter = ArbetsformedlingenAdapter()
        result = adapter._parse_timestamp(None)
        assert result is None

    def test_extract_occupations(self, sample_ad: dict) -> None:
        """Test occupation extraction."""
        adapter = ArbetsformedlingenAdapter()
        occupations = adapter._extract_occupations(sample_ad)

        assert occupations is not None
        assert len(occupations) >= 1
        assert occupations[0]["taxonomy"] == "SSYK"
        assert occupations[0]["code"] == "1234"
