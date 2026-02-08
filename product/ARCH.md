# ARCH (Architecture + Repo Rules Snapshot)
> **Static truth**: architecture, repo map, conventions.
> **Rule**: treat as **read-only during build** (P5–P7), except by explicit **human** decision logged in `process/PROGRESS.md`.

## 0. Metadata
- App name: **Job Mirror (SE + NO)**
- Last updated: 2026-02-08
- Status: Draft (pending story approval)

## 1. Constraints and principles
- Constraints:
  - **Time**: MVP deliverable in ≤ 1 week of agent time
  - **Cost**: minimal; local dev first, optional small VM later
  - **Platform**: macOS/Linux local; single-instance deployment OK for MVP
- Principles:
  - keep V1 simple; avoid over-engineering
  - ship vertical slices (stories) quickly
  - tests + `make check` are the gate for "Done"
  - interfaces are stable (contracts) unless a CCR is approved

## 2. Tech stack (starter defaults + MVP additions)
- Backend: **FastAPI** (Python 3.12)
- Dependency management: **uv** (`pyproject.toml`, `uv.lock`)
- **Database**: PostgreSQL (via SQLModel/SQLAlchemy) — robust local/prod DB
- **HTTP client**: `httpx` for async source fetches
- **Scheduler**: APScheduler (lightweight in-process scheduler)
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
| App code | `app/` | FastAPI app, routers, services, adapters |
| Tests | `tests/` | unit/integration/e2e tests (as added) |
| Product truth | `product/` | PRD, ARCH, contracts, product diagrams/docs |
| Executable contracts | `product/contracts/` | OpenAPI + schemas/types (RO during build unless CCR approved) |
| Process truth | `process/` | PROCESS_REFERENCE + PROGRESS + human guides + process diagrams |
| Antigravity config | `.agent/` | rules/workflows/skills |
| Tooling | `Makefile`, `pyproject.toml` | deterministic `make check`, `make run`, dependencies |

### Internal layout (MVP)
- `app/api/` — routers (`jobs.py`, `export.py`)
- `app/models.py` — SQLModel ORM (JobPosting table)
- `app/db.py` — SQLite engine + session factory
- `app/services/` — ingestion, dedupe, scheduler logic
- `app/adapters/` — source connectors (arbetsformedlingen, nav_arbeidsplassen)

## 4. Architecture snapshot (C4-lite)
- Container: **FastAPI service** (single service for MVP)
- Database: **PostgreSQL** (local Docker or native install)
- External systems:
  - Arbetsförmedlingen JobStream API (SE)
  - NAV Arbeidsplassen public feed (NO)
- Trust boundaries:
  - "outside" → HTTP boundary (API consumers)
  - "ingestion" → outbound HTTP to public job feeds
  - secrets via environment (NAV JWT token)
- Key flows:
  - Health: `GET /health` → returns status
  - Search: `GET /jobs?country_code=SE` → paginated job list
  - Ingestion: Scheduler → Adapters → Dedupe → DB upsert

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
| Timestamp (UTC) | Actor | Change | Why |
|---|---|---|---|
| 2026-02-08T12:00:00Z | Seed (generator) | Initial v4 template | Pack created/updated for Antigravity and folder split (product vs process). |
| 2026-02-08T18:10:00Z | Seed (consistency fix) | Updated repo map + stack to FastAPI/uv and folder names | Align ARCH with v9 starter structure (`app/`, `product/`, `process/`, `.agent/`) and deterministic `make check`. |
| 2026-02-08T18:18:12Z | Seed (generator) | Replaced use-case driver links with stories/tag-based drivers | Align ARCH with stories-first PRD; UC tags are optional labels. |
| 2026-02-08T21:35:00Z | Agent | Populated Job Mirror MVP architecture (SQLite, httpx, adapters layout) | Draft baseline for story approval. |
