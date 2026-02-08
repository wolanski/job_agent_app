# PRD (Stories-First, Lean)

## 0. Metadata
- **Product:** Job Applicant Assistant App (SE + NO)
- **Owner (Human):** Christopher Wolanski
- **Current Version:** MVP
- **Last Updated:** 2026-02-08T20:26:50Z

---

## 1. Vision
**One-liner**
- A lightweight service that **mirrors job postings from Sweden and Norway** into a local database, **dedupes + normalizes** them, and exposes a **simple search/export API** with **daily refresh**.

**Primary user**
- A job-seeker / consultant (you) who wants a **single, searchable**, locally owned dataset of job ads for SE + NO.

**Problem statement**
- Job ads are fragmented across sources, change over time, contain duplicates, and use inconsistent titles/locations/categories. A local “mirror” enables reliable search, change tracking, and later analytics.

**Non-goals (explicitly out-of-scope for this version)**
- Applying to jobs, ATS functionality, CV parsing, or auto-fill/auto-apply.
- Paid/vendor APIs that require commercial contracts (MVP uses public/free sources only).
- Full EU coverage (MVP is **SE + NO only**).
- Real-time streaming updates (MVP is **batch + daily delta**).

---

## 2. Scope boundaries

**In-scope (this version)**
- **Ingestion connectors** for at least **1 Sweden** public job source and **1 Norway** public job source.
- **Initial load + daily refresh** (delta updates where possible; otherwise safe backfill + dedupe).
- **Canonical storage** of job posts (raw + normalized fields) with stable internal IDs.
- **Deduplication**:
  - Primary key: `(source, external_id)` when available.
  - Fallback: fuzzy match on `(company, title, location, apply_url)`.
- **Normalization (MVP-grade)**:
  - Canonicalize company/title/location strings.
  - Store optional mapping hooks for future taxonomy alignment (e.g., ESCO), but keep MVP mapping light.
- **FastAPI endpoints** for browsing/searching:
  - list/search with filters + pagination
  - get-by-id
  - export (CSV/JSON)
- **Operational baseline**:
  - scheduled job runner
  - logging + basic metrics
  - `make check` gate for “Done”.

**Out-of-scope (this version)**
- User accounts, authentication, personalization, notifications.
- Advanced skills extraction/NER pipelines and heavy ML ranking.
- Full-text search engines (Elastic/Meilisearch) — keep DB + basic indexes.
- Web UI beyond minimal developer-friendly docs (OpenAPI/Swagger).
- Cloud production hardening (HA, autoscaling, multi-region) — optional later.

**Constraints**
- **Tech:** FastAPI + uv (pyproject.toml) + pytest; run locally first.
- **Cost:** minimal; default local dev and optional small VM.
- **Compliance:** store **public job data only**; no personal data; respect source terms/rate limits.
- **Reliability:** daily refresh must be idempotent; ingestion must tolerate partial failures.

---

## 3. Requirements (optional)
> Keep this section small. In this process, **Stories + Acceptance Criteria** are the primary scope control.

### Functional requirements (FR)
- FR-001: The system can ingest job posts from configured SE and NO sources.
- FR-002: The system can refresh daily without creating duplicates.
- FR-003: Users can search/filter job posts and export results.

### Non-functional requirements (NFR)
- NFR-001: Idempotent ingestion (re-running a sync produces the same canonical dataset).
- NFR-002: Observability baseline (structured logs + minimal metrics).
- NFR-003: Performance (MVP): list/search endpoints return within acceptable latency for local use.

---

## 4. Story Backlog (authoritative)

### Story principles
- A **Story** is the boundary between Human intent and Agent implementation.
- Stories must be **vertical slices deliverable in ≤ 1 day**.
- If a story is too large: split it.
- The Agent may create **Tasks** (JIT) in `process/PROGRESS.md`, but the Human approves stories.
- Optional **UC tags** can group stories, but they are only labels (no separate use-case hierarchy).

### ID conventions
- Stories: `S-V001`, `S-V002`, ... (V = current version; keep sequential)
- Tasks (JIT per story): `T-V001.01`, `T-V001.02`, ...

### Story index (plan)
| Story ID | Title | UC tags (optional) | Notes |
|---|---|---|---|
| S-V001 | Ingest Sweden source into DB (raw + minimal normalized) | UC:INGEST, UC:SE | First working end-to-end import for SE |
| S-V002 | Ingest Norway source into DB (raw + minimal normalized) | UC:INGEST, UC:NO | Second connector |
| S-V003 | Deduplication + canonicalization baseline | UC:NORM | Apply `(source, external_id)` + fuzzy fallback |
| S-V004 | Search/list API with filters + pagination | UC:API, UC:BROWSE | API usable via Swagger |
| S-V005 | Daily refresh scheduler + idempotency | UC:OPS | Cron-like runner + safe re-runs |
| S-V006 | Export endpoint (CSV/JSON) | UC:EXPORT | Minimal dataset export |

---

### Story template

#### S-V### — [Story title]
- **UC tags (optional):** [UC:...]
- **Summary:** [1–3 sentences]
- **Acceptance criteria:**
  - AC-01: [Given/When/Then or checklist]
  - AC-02: ...
- **Out of scope:**
  - [Explicitly excluded behaviors]
- **Dependencies (optional):**
  - [Other stories, external systems]
- **Notes / assumptions:**
  - [Anything the Agent must not guess]

---

## 5. Optional UC tags (lightweight grouping)

UC tags are **optional labels** used only to group related stories.
- They are **not** separate objects that require decomposition.
- If you don't need grouping, leave this section empty.

| UC tag | Meaning | Notes |
|---|---|---|
| UC:SE | Sweden-specific scope | Connector + source constraints |
| UC:NO | Norway-specific scope | Connector + source constraints |
| UC:INGEST | Source ingestion + parsing | Includes rate limiting + retries |
| UC:NORM | Normalization + dedupe | Canonicalization rules |
| UC:API | Public API surface | FastAPI endpoints |
| UC:BROWSE | Search/browse UX (API-level) | Filters/pagination |
| UC:EXPORT | Dataset export | CSV/JSON |
| UC:OPS | Operations/scheduling | Daily refresh + idempotency |

---

## 6. Roadmap (versions → stories)

| Version | Target stories (IDs) | Notes |
|---|---|---|
| MVP | S-V001…S-V006 | SE + NO mirror, daily refresh, search/export |
| V1.1 | (TBD) | Better normalization + more filters |
| V2 | (TBD) | More countries / richer taxonomy mapping |

---

## 7. Open questions (optional)
> Canonical Qs should be tracked in `process/PROGRESS.md` as Issues (`I-###`).
- Which exact SE and NO public sources are in-scope for MVP?
- What fields are the minimum normalized schema for search/export?

---

## Traceability Log
| Timestamp (UTC) | Actor | Change | Why |
|---|---|---|---|
| 2026-02-08T12:00:00Z | Seed (generator) | Initial PRD template | Provide a minimal scope truth file for the process. |
| 2026-02-08T15:52:05Z | Seed (generator) | Aligned PRD IDs with process gates and FastAPI+uv assumptions | Keep templates consistent with starter pack wiring. |
| 2026-02-08T20:26:50Z | Agent (ChatGPT) | Added Job Mirror (SE+NO) vision, boundaries, and MVP story index | Provide concrete product direction and scope constraints for agentic delivery. |
