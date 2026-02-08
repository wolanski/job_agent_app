"""
app/models.py
SQLModel ORM models for the job mirror database.
Maps to product/contracts/schemas.py Pydantic models.
"""

import hashlib
import json
from datetime import datetime

from sqlmodel import Field, SQLModel


class JobPostingDB(SQLModel, table=True):
    """
    Database model for job postings.
    Primary key: job_id (server-generated UUID).
    Unique constraint: (source, external_id) for upsert.
    """

    __tablename__ = "job_postings"

    # Primary key
    job_id: str = Field(primary_key=True)

    # Source identification
    source: str = Field(index=True)
    external_id: str | None = Field(default=None, index=True)

    # Core fields
    title: str = Field(index=True)
    description: str | None = None

    # Company
    company_name: str | None = Field(default=None, index=True)
    company_id: str | None = None

    # Location (flattened from nested object)
    location_country_code: str = Field(index=True)
    location_region: str | None = None
    location_city: str | None = Field(default=None, index=True)
    location_postal_code: str | None = None
    location_raw: str | None = None

    # Employment details
    employment_type: str | None = None
    remote_type: str | None = None
    seniority: str | None = None

    # Salary (flattened)
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str | None = None
    salary_period: str | None = None

    # Application
    apply_url: str | None = None
    apply_urls_json: str | None = None  # JSON array stored as string

    # Timestamps
    posted_at_utc: datetime | None = None
    expires_at_utc: datetime | None = None
    ingested_at_utc: datetime = Field(default_factory=datetime.utcnow)
    updated_at_utc: datetime = Field(default_factory=datetime.utcnow)

    # Status
    status: str = Field(default="active", index=True)

    # Taxonomy (stored as JSON strings for MVP simplicity)
    occupations_json: str | None = None
    skills_json: str | None = None

    # Deduplication
    dedupe_key: str | None = Field(default=None, index=True)

    def compute_dedupe_key(self) -> str:
        """
        Compute dedupe key from (company_name, title, location_city, apply_url).
        Used when external_id is not available.
        """
        components = [
            (self.company_name or "").strip().lower(),
            (self.title or "").strip().lower(),
            (self.location_city or "").strip().lower(),
            (self.apply_url or "").strip().lower(),
        ]
        combined = "|".join(components)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:32]

    @property
    def apply_urls(self) -> list[str]:
        """Parse apply_urls from JSON string."""
        if self.apply_urls_json:
            result: list[str] = json.loads(self.apply_urls_json)
            return result
        return []

    @apply_urls.setter
    def apply_urls(self, urls: list[str]) -> None:
        """Store apply_urls as JSON string."""
        self.apply_urls_json = json.dumps(urls) if urls else None
