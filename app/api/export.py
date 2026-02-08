"""
app/api/export.py
FastAPI router for exporting job data as CSV or JSON.
"""

import csv
import io
import json
import logging
from collections.abc import Sequence
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlmodel import Session, or_, select

from app.db import get_session
from app.models import JobPostingDB

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/jobs")
def export_jobs(
    session: Annotated[Session, Depends(get_session)],
    format: str = Query("json", pattern="^(json|csv)$"),
    q: str | None = Query(None, description="Full-text search query"),
    country_code: str | None = Query(None, min_length=2, max_length=2),
    source: str | None = Query(None, min_length=1),
    updated_after: datetime | None = Query(None),
) -> StreamingResponse:
    """
    Export job postings as CSV or JSON.

    Supports the same filters as the /jobs endpoint.
    Returns a streaming response to handle large datasets.
    """
    # Build query
    stmt = select(JobPostingDB).where(JobPostingDB.status == "active")

    if country_code:
        stmt = stmt.where(JobPostingDB.location_country_code == country_code.upper())

    if source:
        stmt = stmt.where(JobPostingDB.source == source)

    if updated_after:
        stmt = stmt.where(JobPostingDB.updated_at_utc > updated_after)

    if q:
        search_term = f"%{q}%"
        # Note: type: ignore needed for SQLModel column operations
        stmt = stmt.where(
            or_(
                JobPostingDB.title.ilike(search_term),  # type: ignore[attr-defined,union-attr]
                JobPostingDB.company_name.ilike(search_term),  # type: ignore[attr-defined,union-attr]
                JobPostingDB.description.ilike(search_term),  # type: ignore[attr-defined,union-attr]
            )
        )

    stmt = stmt.order_by(JobPostingDB.job_id)

    # Fetch all matching jobs
    results = session.exec(stmt).all()

    if format == "csv":
        return _export_csv(results)
    else:
        return _export_json(results)


def _export_json(jobs: Sequence[JobPostingDB]) -> StreamingResponse:
    """Export jobs as JSON array."""

    def generate():
        yield "["
        for i, job in enumerate(jobs):
            if i > 0:
                yield ","
            yield json.dumps(_job_to_dict(job), default=str)
        yield "]"

    return StreamingResponse(
        generate(),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=jobs.json"},
    )


def _export_csv(jobs: Sequence[JobPostingDB]) -> StreamingResponse:
    """Export jobs as CSV."""
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    headers = [
        "job_id",
        "source",
        "external_id",
        "title",
        "company_name",
        "country_code",
        "city",
        "region",
        "employment_type",
        "apply_url",
        "posted_at_utc",
        "expires_at_utc",
        "status",
    ]
    writer.writerow(headers)

    # Write data rows
    for job in jobs:
        row = [
            job.job_id,
            job.source,
            job.external_id or "",
            job.title,
            job.company_name or "",
            job.location_country_code,
            job.location_city or "",
            job.location_region or "",
            job.employment_type or "",
            job.apply_url or "",
            job.posted_at_utc.isoformat() if job.posted_at_utc else "",
            job.expires_at_utc.isoformat() if job.expires_at_utc else "",
            job.status,
        ]
        writer.writerow(row)

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=jobs.csv"},
    )


def _job_to_dict(job: JobPostingDB) -> dict:
    """Convert job to dictionary for JSON export."""
    return {
        "job_id": job.job_id,
        "source": job.source,
        "external_id": job.external_id,
        "title": job.title,
        "description": job.description,
        "company_name": job.company_name,
        "location": {
            "country_code": job.location_country_code,
            "region": job.location_region,
            "city": job.location_city,
            "postal_code": job.location_postal_code,
        },
        "employment_type": job.employment_type,
        "remote_type": job.remote_type,
        "apply_url": job.apply_url,
        "posted_at_utc": job.posted_at_utc,
        "expires_at_utc": job.expires_at_utc,
        "ingested_at_utc": job.ingested_at_utc,
        "updated_at_utc": job.updated_at_utc,
        "status": job.status,
    }
