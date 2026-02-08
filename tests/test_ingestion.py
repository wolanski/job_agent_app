"""
tests/test_ingestion.py
Unit tests for ingestion service and deduplication logic.
"""

from datetime import datetime

from app.adapters.base import RawJobPosting
from app.services.ingestion import _compute_dedupe_key, _create_job_from_raw


class TestDeduplication:
    """Tests for deduplication logic."""

    def test_compute_dedupe_key_consistent(self) -> None:
        """Test that dedupe key is consistent for same inputs."""
        raw1 = RawJobPosting(
            source="test",
            external_id=None,
            title="Software Developer",
            description="A job",
            company_name="Acme Corp",
            country_code="SE",
            city="Stockholm",
            apply_url="https://example.com/apply",
        )
        raw2 = RawJobPosting(
            source="test",
            external_id=None,
            title="Software Developer",
            description="Different description",  # Different
            company_name="Acme Corp",
            country_code="SE",
            city="Stockholm",
            apply_url="https://example.com/apply",
        )

        key1 = _compute_dedupe_key(raw1)
        key2 = _compute_dedupe_key(raw2)

        # Description is not part of dedupe key, so keys should match
        assert key1 == key2

    def test_compute_dedupe_key_case_insensitive(self) -> None:
        """Test that dedupe key is case-insensitive."""
        raw1 = RawJobPosting(
            source="test",
            external_id=None,
            title="SOFTWARE DEVELOPER",
            description=None,
            company_name="ACME CORP",
            country_code="SE",
            city="STOCKHOLM",
            apply_url="https://EXAMPLE.COM/apply",
        )
        raw2 = RawJobPosting(
            source="test",
            external_id=None,
            title="software developer",
            description=None,
            company_name="acme corp",
            country_code="SE",
            city="stockholm",
            apply_url="https://example.com/apply",
        )

        key1 = _compute_dedupe_key(raw1)
        key2 = _compute_dedupe_key(raw2)

        assert key1 == key2

    def test_compute_dedupe_key_different_for_different_jobs(self) -> None:
        """Test that different jobs get different dedupe keys."""
        raw1 = RawJobPosting(
            source="test",
            external_id=None,
            title="Software Developer",
            description=None,
            company_name="Acme Corp",
            country_code="SE",
            city="Stockholm",
            apply_url="https://example.com/apply",
        )
        raw2 = RawJobPosting(
            source="test",
            external_id=None,
            title="Data Engineer",  # Different title
            description=None,
            company_name="Acme Corp",
            country_code="SE",
            city="Stockholm",
            apply_url="https://example.com/apply",
        )

        key1 = _compute_dedupe_key(raw1)
        key2 = _compute_dedupe_key(raw2)

        assert key1 != key2


class TestJobCreation:
    """Tests for job creation from raw data."""

    def test_create_job_with_external_id(self) -> None:
        """Test creating a job with external_id (no dedupe_key needed)."""
        raw = RawJobPosting(
            source="arbetsformedlingen",
            external_id="12345",
            title="Developer",
            description="A job",
            company_name="Corp",
            country_code="SE",
        )

        job = _create_job_from_raw(raw, datetime.utcnow())

        assert job.source == "arbetsformedlingen"
        assert job.external_id == "12345"
        assert job.title == "Developer"
        assert job.dedupe_key is None  # Not needed when external_id present

    def test_create_job_without_external_id(self) -> None:
        """Test creating a job without external_id (dedupe_key computed)."""
        raw = RawJobPosting(
            source="test",
            external_id=None,
            title="Developer",
            description="A job",
            company_name="Corp",
            country_code="SE",
            city="Stockholm",
            apply_url="https://example.com",
        )

        job = _create_job_from_raw(raw, datetime.utcnow())

        assert job.external_id is None
        assert job.dedupe_key is not None
        assert len(job.dedupe_key) == 32  # SHA256 truncated to 32 chars

    def test_create_job_preserves_all_fields(self) -> None:
        """Test that all fields are preserved during creation."""
        now = datetime.utcnow()
        posted = datetime(2026, 1, 15)
        expires = datetime(2026, 2, 15)

        raw = RawJobPosting(
            source="test",
            external_id="xyz",
            title="Senior Developer",
            description="We need help",
            company_name="Tech Inc",
            country_code="SE",
            region="Stockholm",
            city="Stockholm",
            postal_code="111 22",
            employment_type="full_time",
            remote_type="hybrid",
            seniority="senior",
            salary_min=50000.0,
            salary_max=70000.0,
            salary_currency="SEK",
            salary_period="month",
            apply_url="https://apply.example.com",
            apply_urls=["https://apply.example.com", "https://backup.example.com"],
            posted_at_utc=posted,
            expires_at_utc=expires,
            occupations=[{"taxonomy": "SSYK", "code": "1234"}],
        )

        job = _create_job_from_raw(raw, now)

        assert job.title == "Senior Developer"
        assert job.location_country_code == "SE"
        assert job.location_city == "Stockholm"
        assert job.salary_min == 50000.0
        assert job.salary_currency == "SEK"
        assert job.posted_at_utc == posted
        assert job.ingested_at_utc == now
