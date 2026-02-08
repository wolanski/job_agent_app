"""
app/adapters/run_ingestion.py
CLI entry point for running ingestion from source adapters.

Usage:
    python -m app.adapters.run_ingestion se          # Ingest from Sweden (Arbetsförmedlingen)
    python -m app.adapters.run_ingestion se --init   # Initial full load (snapshot)
"""

import argparse
import logging
import sys
from datetime import datetime, timedelta

from app.adapters.arbetsformedlingen import ArbetsformedlingenAdapter
from app.db import create_db_and_tables
from app.services.ingestion import ingest_from_adapter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Run job ingestion from source adapters")
    parser.add_argument(
        "source",
        choices=["se"],
        help="Source to ingest from: 'se' for Sweden (Arbetsförmedlingen)",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Run initial full load (snapshot) instead of delta update",
    )
    parser.add_argument(
        "--since-hours",
        type=int,
        default=25,
        help="For delta updates, fetch jobs updated in the last N hours (default: 25)",
    )

    args = parser.parse_args()

    # Ensure database tables exist
    logger.info("Ensuring database tables exist...")
    create_db_and_tables()

    # Determine since timestamp
    since = None
    if not args.init:
        since = datetime.utcnow() - timedelta(hours=args.since_hours)
        logger.info(f"Running delta update since {since}")
    else:
        logger.info("Running initial full load (snapshot)")

    # Run ingestion based on source
    if args.source == "se":
        run_sweden_ingestion(since)
    else:
        logger.error(f"Unknown source: {args.source}")
        sys.exit(1)


def run_sweden_ingestion(since: datetime | None):
    """Run ingestion from Arbetsförmedlingen."""
    logger.info("Starting Sweden (Arbetsförmedlingen) ingestion...")

    with ArbetsformedlingenAdapter() as adapter:
        result = ingest_from_adapter(adapter, since=since)

    logger.info(f"Ingestion result: {result}")

    if result.errors:
        logger.warning(f"Encountered {len(result.errors)} errors during ingestion")
        for error in result.errors[:10]:
            logger.warning(f"  - {error}")

    print("\n✅ Ingestion complete:")
    print(f"   Source: {result.source}")
    print(f"   Received: {result.received_count}")
    print(f"   Created: {result.created_count}")
    print(f"   Updated: {result.updated_count}")
    print(f"   Skipped: {result.skipped_count}")
    print(f"   Errors: {len(result.errors)}")


if __name__ == "__main__":
    main()
