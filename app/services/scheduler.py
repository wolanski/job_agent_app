"""
app/services/scheduler.py
APScheduler service for daily job ingestion refresh.
"""

import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.adapters.arbetsformedlingen import ArbetsformedlingenAdapter
from app.config import get_settings
from app.services.ingestion import ingest_from_adapter

logger = logging.getLogger(__name__)

_scheduler: BackgroundScheduler | None = None


def get_scheduler() -> BackgroundScheduler:
    """Get or create the scheduler instance."""
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
    return _scheduler


def start_scheduler() -> None:
    """Start the scheduler with configured jobs."""
    settings = get_settings()
    scheduler = get_scheduler()

    if scheduler.running:
        logger.warning("Scheduler already running")
        return

    # Add daily ingestion job
    scheduler.add_job(
        run_daily_ingestion,
        trigger=CronTrigger(
            hour=settings.scheduler_cron_hour,
            minute=settings.scheduler_cron_minute,
            timezone="UTC",
        ),
        id="daily_ingestion",
        name="Daily Job Ingestion",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(
        f"Scheduler started with daily ingestion at "
        f"{settings.scheduler_cron_hour}:{settings.scheduler_cron_minute:02d} UTC"
    )


def stop_scheduler() -> None:
    """Stop the scheduler gracefully."""
    scheduler = get_scheduler()
    if scheduler.running:
        scheduler.shutdown(wait=True)
        logger.info("Scheduler stopped")


def run_daily_ingestion() -> None:
    """
    Run daily delta ingestion from all configured sources.
    Fetches updates from the last 25 hours to ensure overlap and avoid missing data.
    """
    logger.info("Starting daily ingestion run...")

    # Fetch jobs updated in the last 25 hours (25h overlap for safety)
    since = datetime.utcnow() - timedelta(hours=25)

    # Run Sweden ingestion
    try:
        with ArbetsformedlingenAdapter() as adapter:
            result = ingest_from_adapter(adapter, since=since)
            logger.info(
                f"Sweden ingestion complete: "
                f"received={result.received_count}, created={result.created_count}, "
                f"updated={result.updated_count}"
            )
    except Exception as e:
        logger.error(f"Sweden ingestion failed: {e}")

    logger.info("Daily ingestion run complete")


def run_immediate_ingestion(source: str = "se", full_load: bool = False) -> dict:
    """
    Trigger an immediate ingestion run.
    Returns result summary for API response.
    """
    since = None if full_load else datetime.utcnow() - timedelta(hours=25)

    if source == "se":
        with ArbetsformedlingenAdapter() as adapter:
            result = ingest_from_adapter(adapter, since=since)
            return {
                "source": result.source,
                "received_count": result.received_count,
                "created_count": result.created_count,
                "updated_count": result.updated_count,
                "skipped_count": result.skipped_count,
                "error_count": len(result.errors),
            }
    else:
        raise ValueError(f"Unknown source: {source}")
