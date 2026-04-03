"""
product/contracts/schemas.py
Starter Pydantic models that match product/contracts/openapi.yaml.

Conventions:
- snake_case JSON fields
- extra fields are forbidden to prevent contract drift
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import AnyUrl, BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorDetail(StrictModel):
    field: str | None = None
    message: str


class ErrorResponse(StrictModel):
    code: str
    message: str
    trace_id: str | None = None
    details: list[ErrorDetail] | None = None


class VersionInfo(StrictModel):
    version: str
    build_sha: str | None = None
    build_time_utc: datetime | None = None


class PageInfo(StrictModel):
    next_cursor: str | None = None
    has_more: bool


class Location(StrictModel):
    country_code: str = Field(..., min_length=2, max_length=2)
    region: str | None = None
    city: str | None = None
    postal_code: str | None = None
    raw: str | None = None


class Salary(StrictModel):
    min_amount: float | None = None
    max_amount: float | None = None
    currency: str | None = None
    period: str | None = None


class TaxonomyTag(StrictModel):
    taxonomy: str
    code: str
    label: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)


class SkillTag(StrictModel):
    name: str
    taxonomy: str | None = None
    code: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)


JobStatus = Literal["active", "expired", "removed"]


class JobPosting(StrictModel):
    job_id: str
    source: str
    external_id: str | None = None

    title: str
    description: str | None = None

    company_name: str | None = None
    company_id: str | None = None

    location: Location

    employment_type: str | None = None
    remote_type: str | None = None
    seniority: str | None = None

    salary: Salary | None = None

    apply_url: AnyUrl | None = None
    apply_urls: list[AnyUrl] | None = None

    posted_at_utc: datetime | None = None
    expires_at_utc: datetime | None = None

    ingested_at_utc: datetime
    updated_at_utc: datetime

    status: JobStatus

    occupations: list[TaxonomyTag] | None = None
    skills: list[SkillTag] | None = None

    dedupe_key: str | None = None


class JobListResponse(StrictModel):
    items: list[JobPosting]
    page_info: PageInfo


class JobUpsert(StrictModel):
    source: str
    external_id: str | None = None

    title: str
    description: str | None = None

    company_name: str | None = None

    location: Location

    employment_type: str | None = None
    remote_type: str | None = None
    seniority: str | None = None

    salary: Salary | None = None

    apply_url: AnyUrl | None = None
    apply_urls: list[AnyUrl] | None = None

    posted_at_utc: datetime | None = None
    expires_at_utc: datetime | None = None

    status: JobStatus = "active"

    occupations: list[TaxonomyTag] | None = None
    skills: list[SkillTag] | None = None


class IngestJobsRequest(StrictModel):
    source: str
    fetched_at_utc: datetime
    jobs: list[JobUpsert]


class IngestJobsResponse(StrictModel):
    source: str
    fetched_at_utc: datetime
    received_count: int
    created_count: int
    updated_count: int
    skipped_count: int
    warnings: list[str] | None = None
