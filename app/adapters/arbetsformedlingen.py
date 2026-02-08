"""
app/adapters/arbetsformedlingen.py
Adapter for Arbetsförmedlingen (Swedish Public Employment Service) JobStream API.

API Documentation: https://gitlab.com/arbetsformedlingen/api-docs/jobtechdev-open-api
Base URL: https://jobstream.api.jobtechdev.se
"""

import logging
from collections.abc import Iterator
from datetime import datetime

import httpx

from app.adapters.base import BaseAdapter, RawJobPosting
from app.config import get_settings

logger = logging.getLogger(__name__)


class ArbetsformedlingenAdapter(BaseAdapter):
    """
    Adapter for fetching job postings from Arbetsförmedlingen JobStream API.

    The JobStream API provides:
    - /stream: Get updates since a timestamp (delta updates)
    - /snapshot: Get all currently active ads
    """

    SOURCE_NAME = "arbetsformedlingen"

    # API endpoints
    SNAPSHOT_PATH = "/snapshot"
    STREAM_PATH = "/stream"

    def __init__(self, base_url: str | None = None):
        settings = get_settings()
        self.base_url = base_url or settings.af_jobstream_base_url
        self.client = httpx.Client(timeout=60.0)

    @property
    def source_name(self) -> str:
        return self.SOURCE_NAME

    def fetch_jobs(self, since: datetime | None = None) -> Iterator[RawJobPosting]:
        """
        Fetch job updates from the stream endpoint.

        Args:
            since: Fetch jobs updated after this timestamp. If None, fetches snapshot.
        """
        if since is None:
            yield from self.fetch_snapshot()
            return

        # Use stream endpoint for delta updates
        url = f"{self.base_url}{self.STREAM_PATH}"
        params = {"date": since.strftime("%Y-%m-%dT%H:%M:%S")}

        logger.info(f"Fetching jobs from {url} since {since}")

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            for ad in data:
                try:
                    yield self._transform_ad(ad)
                except Exception as e:
                    logger.warning(f"Failed to transform ad {ad.get('id')}: {e}")

        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching stream: {e}")
            raise

    def fetch_snapshot(self) -> Iterator[RawJobPosting]:
        """
        Fetch all active jobs from the snapshot endpoint.
        The snapshot is paginated, so we iterate through all pages.
        """
        url = f"{self.base_url}{self.SNAPSHOT_PATH}"
        offset = 0
        limit = 100

        logger.info(f"Fetching snapshot from {url}")

        while True:
            try:
                response = self.client.get(url, params={"offset": offset, "limit": limit})
                response.raise_for_status()
                data = response.json()

                if not data:
                    break

                for ad in data:
                    try:
                        yield self._transform_ad(ad)
                    except Exception as e:
                        logger.warning(f"Failed to transform ad {ad.get('id')}: {e}")

                if len(data) < limit:
                    break

                offset += limit
                logger.debug(f"Fetched {offset} jobs so far...")

            except httpx.HTTPError as e:
                logger.error(f"HTTP error fetching snapshot at offset {offset}: {e}")
                raise

    def _transform_ad(self, ad: dict) -> RawJobPosting:
        """Transform a raw Arbetsförmedlingen ad into RawJobPosting."""
        # Extract workplace address
        workplace = ad.get("workplace_address", {}) or {}
        city = workplace.get("city")
        region = workplace.get("region")
        postal_code = workplace.get("postcode")

        # Extract employer
        employer = ad.get("employer", {}) or {}
        company_name = employer.get("name")

        # Extract application info
        application = ad.get("application_details", {}) or {}
        apply_url = application.get("url")

        # Parse timestamps
        posted_at = self._parse_timestamp(ad.get("publication_date"))
        expires_at = self._parse_timestamp(ad.get("last_publication_date"))

        # Extract employment type
        employment_type = None
        if ad.get("employment_type"):
            employment_type = ad["employment_type"].get("label")

        return RawJobPosting(
            source=self.SOURCE_NAME,
            external_id=str(ad.get("id")),
            title=ad.get("headline", "Untitled"),
            description=ad.get("description", {}).get("text"),
            company_name=company_name,
            country_code="SE",
            region=region,
            city=city,
            postal_code=postal_code,
            location_raw=workplace.get("street_address"),
            employment_type=employment_type,
            remote_type=None,  # Not directly available in API
            seniority=None,  # Not directly available
            apply_url=apply_url,
            apply_urls=[apply_url] if apply_url else None,
            posted_at_utc=posted_at,
            expires_at_utc=expires_at,
            occupations=self._extract_occupations(ad),
            skills=None,  # Would need enrichment API
        )

    def _parse_timestamp(self, ts_str: str | None) -> datetime | None:
        """Parse ISO timestamp string to datetime."""
        if not ts_str:
            return None
        try:
            # Handle various ISO formats
            if ts_str.endswith("Z"):
                ts_str = ts_str[:-1] + "+00:00"
            return datetime.fromisoformat(ts_str)
        except ValueError:
            logger.warning(f"Failed to parse timestamp: {ts_str}")
            return None

    def _extract_occupations(self, ad: dict) -> list[dict] | None:
        """Extract occupation taxonomy tags from ad."""
        occupations = []

        # Occupation group
        occupation = ad.get("occupation_group", {}) or {}
        if occupation.get("legacy_ams_taxonomy_id"):
            occupations.append(
                {
                    "taxonomy": "SSYK",
                    "code": occupation.get("legacy_ams_taxonomy_id"),
                    "label": occupation.get("label"),
                }
            )

        # Occupation field
        field = ad.get("occupation_field", {}) or {}
        if field.get("legacy_ams_taxonomy_id"):
            occupations.append(
                {
                    "taxonomy": "SSYK_FIELD",
                    "code": field.get("legacy_ams_taxonomy_id"),
                    "label": field.get("label"),
                }
            )

        return occupations if occupations else None

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
