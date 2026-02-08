# PROGRESS (Dashboard + Trackers + Evidence + CCR Log)
> **Dynamic truth**: this file changes frequently.
> Reference: `process/diagrams/PROCESS_MAIN.puml`, `process/diagrams/STATE_MODEL.puml`, and `process/diagrams/PROCESS_STEWARD_SEQUENCE.puml`.
> Human guide: `process/guides/HUMAN_OPERATOR_GUIDE.md`.

## 0. Current status
- Current version: MVP
- Current release: R-20260208-01
- Current phase: P4 (Story Baseline) — stories approved, ready to build
- Current story: S-V001
- Current task: NONE

## 1. Policy (how the agent is allowed to operate)
- Approval level: STORY (human approves story set and acceptance; tasks JIT)
- High-risk review: human reviews HIGH-risk tasks only
- Reorder: agent may reorder LOW-risk tasks within a story if dependencies allow
- Contracts: **RO during build** unless CCR approved
- ARCH: **RO during build** unless explicit decision at a gate
- Definition of "Done":
  - `make check` green (tests + lint/typecheck + contract validation)
  - evidence logged (link to CI output or command output)
  - PRD acceptance satisfied (story handshake)

## 2. Gates (Milestones)
| Gate | Meaning | Status | Evidence |
|---|---|---|---|
| G0 | Installed (artifacts exist + check runnable) | PENDING | |
| G1 | Scope approved (PRD accepted) | PENDING | |
| G2 | Ready-to-build (contracts validate + check green) | PENDING | |
| G3 | Story done (repeats per story) | PENDING | |
| G4 | Release candidate (hardening complete) | PENDING | |
| G5 | Released (deployed + smoke + notes) | PENDING | |

## 3. Phase tracker (P0..P12)
| Phase | Name | Status | Notes |
|---|---|---|---|
| P0 | Install and Wire | PENDING | |
| P1 | Functional Framing | PENDING | |
| P2 | Architecture (Lite) | PENDING | |
| P3 | Contract Baseline | PENDING | |
| P4 | Story Baseline | PENDING | |
| P5 | JIT Planning | PENDING | |
| P6 | Iterative Implementation | PENDING | |
| P7 | Story Handshake | PENDING | |
| P8 | Integration Testing | PENDING | |
| P9 | E2E Automation | PENDING | |
| P10 | Manual E2E (optional) | PENDING | |
| P11 | Deploy | PENDING | |
| P12 | Post-release Feedback | PENDING | |

## 4. Optional UC tag glossary (lightweight)
> UC tags are optional labels used only to group stories.

| UC tag | Meaning | Notes |
|---|---|---|
| UC:SE | Sweden-specific scope | Arbetsförmedlingen source |
| UC:INGEST | Source ingestion + parsing | Adapters + rate limiting |
| UC:NORM | Normalization + dedupe | Canonicalization rules |
| UC:API | Public API surface | FastAPI endpoints |
| UC:BROWSE | Search/browse UX (API-level) | Filters + pagination |
| UC:EXPORT | Dataset export | CSV/JSON |
| UC:OPS | Operations/scheduling | Daily refresh |

## 5. Story tracker (authoritative operational list)
| Story ID | Title | UC tags (optional) | Risk | Status | Evidence |
|---|---|---|---:|---|---|
| S-V001 | Ingest Sweden source (Arbetsförmedlingen) | UC:INGEST, UC:SE | MED | APPROVED | |
| S-V002 | Ingest Norway source (NAV) | UC:INGEST | MED | DEFERRED | User decision: skip for MVP |
| S-V003 | Deduplication + canonicalization baseline | UC:NORM | LOW | APPROVED | |
| S-V004 | Search/list API with filters + pagination | UC:API, UC:BROWSE | LOW | APPROVED | |
| S-V005 | Daily refresh scheduler + idempotency | UC:OPS | MED | APPROVED | |
| S-V006 | Export endpoint (CSV/JSON) | UC:EXPORT | LOW | APPROVED | |

## 6. Current story JIT tasks (rewrite this section per story)
### Story: S-V001
| Task ID | Title | Risk | Status | Evidence |
|---|---|---:|---|---|
| T-V001.01 | ... | LOW | PLANNED | |
| T-V001.02 | ... | MED | PLANNED | |

## 7. CCR log (Contract Change Requests)
> Raised when product/contracts/spec must change. Rule: **STOP** and ask; no workaround.
| CCR ID | Date | Related task | Summary | Decision | Evidence |
|---|---|---|---|---|---|
| CCR-001 | YYYY-MM-DD | T-V001.02 | ... | PENDING | link/log |

## 8. Issues log
| ID | Date | Type | Summary | Status | Link |
|---|---|---|---|---|---|
| I-001 | YYYY-MM-DD | Bug/TechDebt/Question | ... | OPEN | |

## 9. Decisions log
| ID | Date | Decision | Rationale | Impact |
|---|---|---|---|---|
| D-001 | 2026-02-08 | Use PostgreSQL instead of SQLite | User preference for robust DB | Requires Postgres setup (Docker/native) |
| D-002 | 2026-02-08 | Defer S-V002 (NO Ingest) for MVP | User scope reduction | MVP is SE-only; NO source can be added later |
| D-003 | 2026-02-08 | Use simple hash for dedupe fallback | MVP simplicity | Hash of (company+title+location+url); no fuzzy ML |

## 10. Evidence log (checks and artifacts)
| Date | What ran | Result | Where |
|---|---|---|---|
| YYYY-MM-DD | check | PASS | CI link or console output |

## 11. Artifacts added (append)
| Date | Artifact | Type | Purpose | Link |
|---|---|---|---|---|
| YYYY-MM-DD | ... | doc/diagram/contract | ... | relative path |

## 12. Release notes (append per release)
### Release R-YYYYMMDD-01
- Scope shipped:
  - Stories: S-V001, S-V002
- Known issues:
  - ...
- How to verify:
  - ...
- Rollback notes:
  - ...
