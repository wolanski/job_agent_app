"""
app/adapters/base.py
Base adapter interface for job source connectors.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RawJobPosting:
    """
    Raw job posting data from a source.
    Adapters transform source-specific data into this common format.
    """

    source: str
    external_id: str | None

    title: str
    description: str | None

    company_name: str | None

    # Location
    country_code: str
    region: str | None = None
    city: str | None = None
    postal_code: str | None = None
    location_raw: str | None = None

    # Employment
    employment_type: str | None = None
    remote_type: str | None = None
    seniority: str | None = None

    # Salary
    salary_min: float | None = None
    salary_max: float | None = None
    salary_currency: str | None = None
    salary_period: str | None = None

    # Application
    apply_url: str | None = None
    apply_urls: list[str] | None = None

    # Timestamps
    posted_at_utc: datetime | None = None
    expires_at_utc: datetime | None = None

    # Taxonomy
    occupations: list[dict] | None = None
    skills: list[dict] | None = None


class BaseAdapter(ABC):
    """Abstract base class for job source adapters."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the canonical source identifier (e.g., 'arbetsformedlingen')."""
        ...

    @abstractmethod
    def fetch_jobs(self, since: datetime | None = None) -> Iterator[RawJobPosting]:
        """
        Fetch job postings from the source.

        Args:
            since: If provided, only fetch jobs updated after this timestamp.
                   If None, fetch all available jobs (initial load).

        Yields:
            RawJobPosting objects for each job found.
        """
        ...

    @abstractmethod
    def fetch_snapshot(self) -> Iterator[RawJobPosting]:
        """
        Fetch a complete snapshot of all active jobs.
        Used for initial load or full refresh.

        Yields:
            RawJobPosting objects for each active job.
        """
        ...
