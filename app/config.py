"""
app/config.py
Application configuration via environment variables.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/jobmirror"

    # Arbetsförmedlingen API
    af_jobstream_base_url: str = "https://jobstream.api.jobtechdev.se"

    # Scheduler
    scheduler_enabled: bool = True
    scheduler_cron_hour: int = 6  # Run at 06:00 daily
    scheduler_cron_minute: int = 0

    # App
    app_name: str = "Job Mirror (SE + NO)"
    app_version: str = "0.1.0"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
