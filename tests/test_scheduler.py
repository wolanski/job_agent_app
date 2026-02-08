"""
tests/test_scheduler.py
Tests for the scheduler service.
"""

from unittest.mock import MagicMock, patch

from app.services.scheduler import get_scheduler, run_immediate_ingestion


class TestScheduler:
    """Tests for scheduler functionality."""

    def test_get_scheduler_returns_instance(self) -> None:
        """Test that get_scheduler returns a scheduler instance."""
        scheduler = get_scheduler()
        assert scheduler is not None

    @patch("app.services.scheduler.ingest_from_adapter")
    @patch("app.services.scheduler.ArbetsformedlingenAdapter")
    def test_run_immediate_ingestion(
        self, mock_adapter_class: MagicMock, mock_ingest: MagicMock
    ) -> None:
        """Test immediate ingestion trigger."""
        # Setup mock
        mock_adapter = MagicMock()
        mock_adapter.__enter__ = MagicMock(return_value=mock_adapter)
        mock_adapter.__exit__ = MagicMock(return_value=None)
        mock_adapter_class.return_value = mock_adapter

        mock_result = MagicMock()
        mock_result.source = "arbetsformedlingen"
        mock_result.received_count = 100
        mock_result.created_count = 50
        mock_result.updated_count = 25
        mock_result.skipped_count = 25
        mock_result.errors = []
        mock_ingest.return_value = mock_result

        # Run
        result = run_immediate_ingestion(source="se", full_load=False)

        # Verify
        assert result["source"] == "arbetsformedlingen"
        assert result["received_count"] == 100
        assert result["created_count"] == 50
        mock_ingest.assert_called_once()

    def test_run_immediate_ingestion_unknown_source(self) -> None:
        """Test that unknown source raises error."""
        import pytest

        with pytest.raises(ValueError, match="Unknown source"):
            run_immediate_ingestion(source="unknown")
