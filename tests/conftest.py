"""
tests/conftest.py
Pytest configuration and fixtures.

Sets up test database using SQLite in-memory to avoid PostgreSQL dependency in tests.
"""

import os

import pytest

# Set DATABASE_URL to SQLite before importing app modules
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from sqlmodel import SQLModel

from app.db import get_engine


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test database tables once per test session."""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    yield
    # Cleanup after all tests
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database state between tests by deleting all rows."""
    from sqlmodel import Session

    from app.models import JobPostingDB

    engine = get_engine()
    with Session(engine) as session:
        # Delete all jobs before each test
        session.exec(JobPostingDB.__table__.delete())  # type: ignore[attr-defined]
        session.commit()
    yield
