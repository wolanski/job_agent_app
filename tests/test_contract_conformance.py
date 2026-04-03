"""
tests/test_contract_conformance.py
Lightweight contract conformance: compare FastAPI's generated OpenAPI spec
against the committed product/contracts/openapi.yaml.

Catches structural drift (missing paths, missing required fields, wrong types)
without a full Schemathesis runtime test.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
import pytest
from app.main import app

OPENAPI_PATH = Path(__file__).resolve().parent.parent / "product" / "contracts" / "openapi.yaml"


def _load_committed_spec() -> dict[str, Any]:
    """Load the committed OpenAPI YAML spec."""
    assert OPENAPI_PATH.exists(), f"Committed spec not found: {OPENAPI_PATH}"
    with open(OPENAPI_PATH) as f:
        return yaml.safe_load(f)


def _load_fastapi_spec() -> dict[str, Any]:
    """Load the spec FastAPI generates at runtime."""
    return app.openapi()


class TestContractConformance:
    """Verify committed OpenAPI spec matches FastAPI's generated spec."""

    @pytest.fixture(scope="class")
    def committed(self) -> dict[str, Any]:
        return _load_committed_spec()

    @pytest.fixture(scope="class")
    def generated(self) -> dict[str, Any]:
        return _load_fastapi_spec()

    @pytest.mark.skip(reason="Not all endpoints implemented yet; enable when entering P5")
    def test_all_committed_paths_exist_in_generated(
        self, committed: dict[str, Any], generated: dict[str, Any]
    ) -> None:
        """Every path in the committed spec must exist in the generated spec."""
        committed_paths = set(committed.get("paths", {}).keys())
        generated_paths = set(generated.get("paths", {}).keys())
        missing = committed_paths - generated_paths
        assert not missing, (
            f"Committed spec has paths not in FastAPI app: {missing}. "
            "Either implement the endpoint or update the committed spec."
        )

    def test_all_generated_paths_exist_in_committed(
        self, committed: dict[str, Any], generated: dict[str, Any]
    ) -> None:
        """Every path FastAPI generates must exist in the committed spec."""
        committed_paths = set(committed.get("paths", {}).keys())
        generated_paths = set(generated.get("paths", {}).keys())
        extra = generated_paths - committed_paths
        assert not extra, (
            f"FastAPI app has paths not in committed spec: {extra}. "
            "Update product/contracts/openapi.yaml to match."
        )

    def test_health_required_fields(self, committed: dict[str, Any]) -> None:
        """Verify /health required fields are present in committed spec."""
        health = committed.get("paths", {}).get("/health", {})
        get_resp = health.get("get", {}).get("responses", {}).get("200", {})
        schema = (
            get_resp.get("content", {})
            .get("application/json", {})
            .get("schema", {})
        )
        required = schema.get("required", [])
        assert "status" in required, "/health schema missing 'status' in required"
        assert "time_utc" in required, "/health schema missing 'time_utc' in required"
