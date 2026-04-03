# ARCH (Architecture + Repo Rules Snapshot)
> **Static truth**: architecture, repo map, conventions.
> **Rule**: treat as **read-only during build** (P5–P7), except by explicit **human** decision logged in `process/PROGRESS.md`.

## 0. Metadata
- App name: [TBD]
- Last updated: [YYYY-MM-DD]
- Status: [Draft|Stable]

## 1. Constraints and principles
- Constraints: [time/budget/platform]
- Principles:
  - keep V1 simple; avoid over-engineering
  - ship vertical slices (stories) quickly
  - tests + `make check` are the gate for “Done”
  - interfaces are stable (contracts) unless a CCR is approved

## 2. Tech stack (starter defaults)
- Backend: **FastAPI** (Python 3.12)
- Dependency management: **uv** (`pyproject.toml`, `uv.lock`)
- Quality gates:
  - Lint: `ruff check .`
  - Format check: `ruff format . --check`
  - Typecheck: `mypy .`
  - Tests: `pytest`
- Run (dev): `make run` (calls `uv run fastapi dev`)
- Verify (DoD): `make check` (single deterministic entrypoint)

## 3. Repo map (authoritative)
| Area | Path | Responsibility |
|---|---|---|
| App code | `app/` | FastAPI app, routers, services |
| Tests | `tests/` | unit/integration/e2e tests (as added) |
| Product truth | `product/` | PRD, ARCH, contracts, product diagrams/docs |
| Executable contracts | `product/contracts/` | OpenAPI + schemas/types (RO during build unless CCR approved) |
| Process truth | `process/` | PROCESS_REFERENCE + PROGRESS + human guides + process diagrams |
| Antigravity config | `.agents/` | rules/workflows/skills |
| Tooling | `Makefile`, `pyproject.toml` | deterministic `make check`, `make run`, dependencies |

### Recommended internal layout (create only when needed)
- `app/api/` — routers (FastAPI `APIRouter`s)
- `app/models/` — Pydantic models (if not fully covered by `product/contracts/schemas.py`)
- `app/services/` — business logic
- `app/adapters/` — external integrations

## 4. Architecture snapshot (C4-lite)
- Container: **FastAPI service** (single service for MVP)
- Trust boundaries:
  - “outside” → HTTP boundary
  - secrets via environment/secret manager (later)
- Key flows (examples):
  - Health: `GET /health` → returns status

## 5. Conventions
- Naming:
  - Python packages/modules: `snake_case`
  - API JSON fields: prefer `snake_case` unless contract says otherwise
- Errors: define a consistent error envelope in `product/contracts/openapi.yaml` when adding real endpoints
- Logging/metrics: start with `logging` stdlib; add structured logging later
- Testing:
  - unit tests for story tasks
  - integration/e2e added in phases P8–P10 as needed

## 6. Extension points (optional drivers)
Link extension points to **Story tags** or specific Stories in PRD:
- Example: UC:AUTH → [auth module boundary]
- Example: UC:IMPORT → [background job interface]
- Example: S-V003 → [plugin interface]

Rule: keep this list short; add items only when they influence today's design.

## 7. Security and privacy (minimum)
- Data classification: [PII?]
- Secrets: never commit; use environment or secret manager
- Threat notes (top 3): [TBD]

## Traceability Log
*(Historical rows cleared to preserve clean template state)*
| Timestamp (UTC) | Actor | Change | Why |
|---|---|---|---|
