"""
app/db.py
Database setup with SQLModel + PostgreSQL.
"""

from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

# Create engine with connection pooling
_engine = None


def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(
            settings.database_url,
            echo=False,
            pool_pre_ping=True,
        )
    return _engine


def create_db_and_tables() -> None:
    """Create all tables defined by SQLModel metadata."""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency that yields a database session."""
    engine = get_engine()
    with Session(engine) as session:
        yield session
