"""
app/main.py
FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI

from app.api.export import router as export_router
from app.api.jobs import router as jobs_router
from app.config import get_settings
from app.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    from app.services.scheduler import start_scheduler, stop_scheduler

    # Startup: ensure database tables exist
    create_db_and_tables()

    # Start scheduler if enabled
    if settings.scheduler_enabled:
        start_scheduler()

    yield

    # Shutdown: stop scheduler
    if settings.scheduler_enabled:
        stop_scheduler()


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

# Include routers
app.include_router(jobs_router)
app.include_router(export_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "time_utc": datetime.now(UTC).isoformat()}


@app.get("/meta/version")
def version() -> dict[str, str]:
    """Version metadata endpoint."""
    return {"version": settings.app_version}
