"""
product/contracts/schemas.py
Starter Pydantic models that match product/contracts/openapi.yaml.

Conventions:
- snake_case JSON fields
- extra fields are forbidden to prevent contract drift
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, AnyUrl, ConfigDict


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorDetail(StrictModel):
    field: Optional[str] = None
    message: str


class ErrorResponse(StrictModel):
    code: str
    message: str
    trace_id: Optional[str] = None
    details: Optional[List[ErrorDetail]] = None


class VersionInfo(StrictModel):
    version: str
    build_sha: Optional[str] = None
    build_time_utc: Optional[datetime] = None


class PageInfo(StrictModel):
    next_cursor: Optional[str] = None
    has_more: bool


class Location(StrictModel):
    country_code: str = Field(..., min_length=2, max_length=2)
    region: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    raw: Optional[str] = None


class Salary(StrictModel):
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    currency: Optional[str] = None
    period: Optional[str] = None


class TaxonomyTag(StrictModel):
    taxonomy: str
    code: str
    label: Optional[str] = None
    confidence: Optional[float] = Field(default=None, ge=0, le=1)


class SkillTag(StrictModel):
    name: str
    taxonomy: Optional[str] = None
    code: Optional[str] = None
    confidence: Optional[float] = Field(default=None, ge=0, le=1)


JobStatus = Literal["active", "expired", "removed"]


class JobPosting(StrictModel):
    job_id: str
    source: str
    external_id: Optional[str] = None

    title: str
    description: Optional[str] = None

    company_name: Optional[str] = None
    company_id: Optional[str] = None

    location: Location

    employment_type: Optional[str] = None
    remote_type: Optional[str] = None
    seniority: Optional[str] = None

    salary: Optional[Salary] = None

    apply_url: Optional[AnyUrl] = None
    apply_urls: Optional[List[AnyUrl]] = None

    posted_at_utc: Optional[datetime] = None
    expires_at_utc: Optional[datetime] = None

    ingested_at_utc: datetime
    updated_at_utc: datetime

    status: JobStatus

    occupations: Optional[List[TaxonomyTag]] = None
    skills: Optional[List[SkillTag]] = None

    dedupe_key: Optional[str] = None


class JobListResponse(StrictModel):
    items: List[JobPosting]
    page_info: PageInfo


class JobUpsert(StrictModel):
    source: str
    external_id: Optional[str] = None

    title: str
    description: Optional[str] = None

    company_name: Optional[str] = None

    location: Location

    employment_type: Optional[str] = None
    remote_type: Optional[str] = None
    seniority: Optional[str] = None

    salary: Optional[Salary] = None

    apply_url: Optional[AnyUrl] = None
    apply_urls: Optional[List[AnyUrl]] = None

    posted_at_utc: Optional[datetime] = None
    expires_at_utc: Optional[datetime] = None

    status: Optional[JobStatus] = "active"

    occupations: Optional[List[TaxonomyTag]] = None
    skills: Optional[List[SkillTag]] = None


class IngestJobsRequest(StrictModel):
    source: str
    fetched_at_utc: datetime
    jobs: List[JobUpsert]


class IngestJobsResponse(StrictModel):
    source: str
    fetched_at_utc: datetime
    received_count: int
    created_count: int
    updated_count: int
    skipped_count: int
    warnings: Optional[List[str]] = None
