# Makefile (Lean Agentic Dev - FastAPI + uv)
# Deterministic validation entrypoint for both Human and Agent.
#
# Usage:
#   make check   # Definition of Done gate
#   make run     # Run FastAPI dev server
#
# Notes:
# - Uses `uv` for environment + dependency management.
# - `uv sync` will create `.venv/` and `uv.lock` if missing.

.PHONY: sync check lint format typecheck contractcheck test run

sync:
	uv sync

check: sync lint format typecheck contractcheck test
	@echo "✅ check passed"

lint:
	uv run ruff check .

format:
	uv run ruff format . --check

typecheck:
	uv run mypy .

contractcheck:
	@echo "--- Validating executable contracts (schemas + OpenAPI generation) ---"
	uv run python -m py_compile product/contracts/schemas.py
	uv run python -c "from app.main import app; app.openapi(); print('OpenAPI generation OK')"
	@echo "--- Contract conformance (committed spec vs generated) runs in pytest (test_contract_conformance.py) ---"

test:
	uv run pytest -q

run: sync
	uv run fastapi dev
