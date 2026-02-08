"""
app/api/jobs.py
FastAPI router for job search and retrieval.
Implements GET /jobs (list/search with filters) and GET /jobs/{job_id}.
"""

import logging
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, or_, select

from app.db import get_session
from app.models import JobPostingDB
from product.contracts.schemas import (
    ErrorResponse,
    JobListResponse,
    JobPosting,
    Location,
    PageInfo,
    Salary,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _db_to_response(job: JobPostingDB) -> JobPosting:
    """Convert database model to API response model."""
    import json

    # Build location
    location = Location(
        country_code=job.location_country_code,
        region=job.location_region,
        city=job.location_city,
        postal_code=job.location_postal_code,
        raw=job.location_raw,
    )

    # Build salary if any fields present
    salary = None
    if any([job.salary_min, job.salary_max, job.salary_currency, job.salary_period]):
        salary = Salary(
            min_amount=job.salary_min,
            max_amount=job.salary_max,
            currency=job.salary_currency,
            period=job.salary_period,
        )

    # Parse JSON arrays
    occupations = None
    if job.occupations_json:
        occupations = json.loads(job.occupations_json)

    skills = None
    if job.skills_json:
        skills = json.loads(job.skills_json)

    apply_urls = None
    if job.apply_urls_json:
        apply_urls = json.loads(job.apply_urls_json)

    return JobPosting(
        job_id=job.job_id,
        source=job.source,
        external_id=job.external_id,
        title=job.title,
        description=job.description,
        company_name=job.company_name,
        company_id=job.company_id,
        location=location,
        employment_type=job.employment_type,
        remote_type=job.remote_type,
        seniority=job.seniority,
        salary=salary,
        apply_url=job.apply_url,  # type: ignore[arg-type]
        apply_urls=apply_urls,
        posted_at_utc=job.posted_at_utc,
        expires_at_utc=job.expires_at_utc,
        ingested_at_utc=job.ingested_at_utc,
        updated_at_utc=job.updated_at_utc,
        status=job.status,  # type: ignore[arg-type]
        occupations=occupations,
        skills=skills,
        dedupe_key=job.dedupe_key,
    )


@router.get("", response_model=JobListResponse)
def list_jobs(
    session: Annotated[Session, Depends(get_session)],
    q: str | None = Query(None, description="Full-text search query"),
    country_code: str | None = Query(None, min_length=2, max_length=2),
    source: str | None = Query(None, min_length=1),
    updated_after: datetime | None = Query(None),
    cursor: str | None = Query(None, description="Pagination cursor (job_id)"),
    limit: int = Query(50, ge=1, le=200),
) -> JobListResponse:
    """
    List/search job postings with filters and pagination.

    Pagination uses cursor-based approach where cursor is the last job_id seen.
    """
    # Base query
    stmt = select(JobPostingDB).where(JobPostingDB.status == "active")

    # Apply filters
    if country_code:
        stmt = stmt.where(JobPostingDB.location_country_code == country_code.upper())

    if source:
        stmt = stmt.where(JobPostingDB.source == source)

    if updated_after:
        stmt = stmt.where(JobPostingDB.updated_at_utc > updated_after)

    if q:
        # Simple text search across title, company, description
        search_term = f"%{q}%"
        # Note: type: ignore needed for SQLModel column operations
        stmt = stmt.where(
            or_(
                JobPostingDB.title.ilike(search_term),  # type: ignore[attr-defined,union-attr]
                JobPostingDB.company_name.ilike(search_term),  # type: ignore[attr-defined,union-attr]
                JobPostingDB.description.ilike(search_term),  # type: ignore[attr-defined,union-attr]
            )
        )

    # Apply cursor (pagination)
    if cursor:
        stmt = stmt.where(JobPostingDB.job_id > cursor)

    # Order by job_id for stable pagination
    stmt = stmt.order_by(JobPostingDB.job_id).limit(limit + 1)

    # Execute query
    results = list(session.exec(stmt))

    # Determine if there are more results
    has_more = len(results) > limit
    if has_more:
        results = results[:limit]

    # Convert to response models
    items = [_db_to_response(job) for job in results]

    # Build page info
    next_cursor = items[-1].job_id if items and has_more else None
    page_info = PageInfo(next_cursor=next_cursor, has_more=has_more)

    return JobListResponse(items=items, page_info=page_info)


@router.get("/{job_id}", response_model=JobPosting, responses={404: {"model": ErrorResponse}})
def get_job_by_id(
    job_id: str,
    session: Annotated[Session, Depends(get_session)],
) -> JobPosting:
    """Get a job posting by its internal ID."""
    stmt = select(JobPostingDB).where(JobPostingDB.job_id == job_id)
    job = session.exec(stmt).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": f"Job {job_id} not found"},
        )

    return _db_to_response(job)
