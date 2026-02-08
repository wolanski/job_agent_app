"""
app/services/ingestion.py
Ingestion service: orchestrates fetching from adapters, deduplication, and DB upsert.
"""

import json
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlmodel import Session, select

from app.adapters.base import BaseAdapter, RawJobPosting
from app.db import get_engine
from app.models import JobPostingDB

logger = logging.getLogger(__name__)


@dataclass
class IngestionResult:
    """Result of an ingestion run."""

    source: str
    fetched_at_utc: datetime
    received_count: int
    created_count: int
    updated_count: int
    skipped_count: int
    errors: list[str]


def ingest_from_adapter(
    adapter: BaseAdapter,
    since: datetime | None = None,
) -> IngestionResult:
    """
    Ingest job postings from an adapter into the database.

    Args:
        adapter: The source adapter to fetch from.
        since: If provided, only fetch jobs updated after this timestamp.

    Returns:
        IngestionResult with counts and any errors.
    """
    fetched_at = datetime.utcnow()
    result = IngestionResult(
        source=adapter.source_name,
        fetched_at_utc=fetched_at,
        received_count=0,
        created_count=0,
        updated_count=0,
        skipped_count=0,
        errors=[],
    )

    engine = get_engine()

    with Session(engine) as session:
        for raw_job in adapter.fetch_jobs(since=since):
            result.received_count += 1

            try:
                action = _upsert_job(session, raw_job, fetched_at)
                if action == "created":
                    result.created_count += 1
                elif action == "updated":
                    result.updated_count += 1
                else:
                    result.skipped_count += 1

                # Commit in batches of 100
                if result.received_count % 100 == 0:
                    session.commit()
                    logger.info(
                        f"Ingested {result.received_count} jobs "
                        f"(created={result.created_count}, updated={result.updated_count})"
                    )

            except Exception as e:
                error_msg = f"Failed to upsert job {raw_job.external_id}: {e}"
                logger.error(error_msg)
                result.errors.append(error_msg)
                result.skipped_count += 1

        # Final commit
        session.commit()

    logger.info(
        f"Ingestion complete for {adapter.source_name}: "
        f"received={result.received_count}, created={result.created_count}, "
        f"updated={result.updated_count}, skipped={result.skipped_count}"
    )

    return result


def _upsert_job(
    session: Session,
    raw: RawJobPosting,
    ingested_at: datetime,
) -> str:
    """
    Upsert a job posting into the database.

    Returns:
        'created', 'updated', or 'skipped'
    """
    # Try to find existing job by (source, external_id)
    existing = None

    if raw.external_id:
        stmt = select(JobPostingDB).where(
            JobPostingDB.source == raw.source,
            JobPostingDB.external_id == raw.external_id,
        )
        existing = session.exec(stmt).first()

    # If no external_id or not found, try dedupe_key fallback
    if existing is None:
        dedupe_key = _compute_dedupe_key(raw)
        stmt = select(JobPostingDB).where(JobPostingDB.dedupe_key == dedupe_key)
        existing = session.exec(stmt).first()

    if existing:
        # Update existing record
        _update_job_from_raw(existing, raw, ingested_at)
        session.add(existing)
        return "updated"
    else:
        # Create new record
        job = _create_job_from_raw(raw, ingested_at)
        session.add(job)
        return "created"


def _compute_dedupe_key(raw: RawJobPosting) -> str:
    """Compute dedupe key hash from job fields."""
    import hashlib

    components = [
        (raw.company_name or "").strip().lower(),
        (raw.title or "").strip().lower(),
        (raw.city or "").strip().lower(),
        (raw.apply_url or "").strip().lower(),
    ]
    combined = "|".join(components)
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:32]


def _create_job_from_raw(raw: RawJobPosting, ingested_at: datetime) -> JobPostingDB:
    """Create a new JobPostingDB from raw data."""
    job_id = str(uuid.uuid4())
    dedupe_key = _compute_dedupe_key(raw) if not raw.external_id else None

    return JobPostingDB(
        job_id=job_id,
        source=raw.source,
        external_id=raw.external_id,
        title=raw.title,
        description=raw.description,
        company_name=raw.company_name,
        location_country_code=raw.country_code,
        location_region=raw.region,
        location_city=raw.city,
        location_postal_code=raw.postal_code,
        location_raw=raw.location_raw,
        employment_type=raw.employment_type,
        remote_type=raw.remote_type,
        seniority=raw.seniority,
        salary_min=raw.salary_min,
        salary_max=raw.salary_max,
        salary_currency=raw.salary_currency,
        salary_period=raw.salary_period,
        apply_url=raw.apply_url,
        apply_urls_json=json.dumps(raw.apply_urls) if raw.apply_urls else None,
        posted_at_utc=raw.posted_at_utc,
        expires_at_utc=raw.expires_at_utc,
        ingested_at_utc=ingested_at,
        updated_at_utc=ingested_at,
        status="active",
        occupations_json=json.dumps(raw.occupations) if raw.occupations else None,
        skills_json=json.dumps(raw.skills) if raw.skills else None,
        dedupe_key=dedupe_key,
    )


def _update_job_from_raw(job: JobPostingDB, raw: RawJobPosting, updated_at: datetime) -> None:
    """Update an existing job record with new data."""
    job.title = raw.title
    job.description = raw.description
    job.company_name = raw.company_name
    job.location_country_code = raw.country_code
    job.location_region = raw.region
    job.location_city = raw.city
    job.location_postal_code = raw.postal_code
    job.location_raw = raw.location_raw
    job.employment_type = raw.employment_type
    job.remote_type = raw.remote_type
    job.seniority = raw.seniority
    job.salary_min = raw.salary_min
    job.salary_max = raw.salary_max
    job.salary_currency = raw.salary_currency
    job.salary_period = raw.salary_period
    job.apply_url = raw.apply_url
    job.apply_urls_json = json.dumps(raw.apply_urls) if raw.apply_urls else None
    job.posted_at_utc = raw.posted_at_utc
    job.expires_at_utc = raw.expires_at_utc
    job.updated_at_utc = updated_at
    job.occupations_json = json.dumps(raw.occupations) if raw.occupations else None
    job.skills_json = json.dumps(raw.skills) if raw.skills else None
