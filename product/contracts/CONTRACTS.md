# CONTRACTS (Index + invariants + compatibility)
> Optional index/overview for executable contracts stored under `product/contracts/`.
> Contracts are treated as **read-only during build** unless a CCR is approved (see `process/PROGRESS.md` CCR log).

## 1. Contract files (expected)
- `product/contracts/openapi.yaml` — API contract snapshot (optional early on; if present it's authoritative for HTTP payloads)
- `product/contracts/schemas.py` — Pydantic models (authoritative internal DTO schema)
- Optional: `product/contracts/spectral.yaml` — Spectral rules/config (if you add Spectral)
- Optional: generated clients/stubs under `app/generated/` (if used)

### Validation & tooling (starter)
- Canonical validation gate for code + tests: `make check`


## 2. Naming conventions
- Field naming: [snake_case recommended for Python]
- IDs: [uuid|int|external_id rules]
- Time: [ISO-8601 UTC]

## 3. Error model (standard envelope)
- shape: `{ code, message, details?, trace_id? }`
- HTTP mapping: [list]

## 4. Invariants (must always hold)
- Idempotency: ...
- Pagination: ...
- Validation: ...
- Dedupe rules: ...

## 5. Compatibility / migration policy
- Backwards compatible changes allowed: [add optional fields, etc.]
- Breaking changes: require [version bump + CCR + migration notes]
- Deprecation policy: [timeline]

## 6. CCR rule (summary)
If implementation reveals a contract gap:
1) STOP
2) Raise CCR with evidence + minimal change proposal
3) Wait for human decision
4) If approved: update `product/contracts/*` and re-run validation

## Traceability Log
| Timestamp (UTC) | Actor | Change | Why |
|---|---|---|---|
| 2026-02-08T12:00:00Z | Seed (generator) | Initial v4 template | Pack created/updated for Antigravity and folder split (product vs process). |
| 2026-02-08T15:53:51Z | Seed (generator) | Adjusted contracts list for FastAPI-only starter | Removed TS types; clarified schemas.py + OpenAPI snapshot option. |
| 2026-02-08T16:22:00Z | Seed (consistency fix) | Clarified contract file list and removed duplicate OpenAPI entry | Avoid confusion; align with v9 FastAPI+uv folder layout. |
| 2026-02-08T19:14:13Z | Seed (docs cleanup) | Added  as canonical validation reference in CONTRACTS.md | Reduce README sprawl; keep contract guidance in canonical index file. |
| 2026-02-08T19:14:26Z | Seed (docs cleanup) | Added make check as canonical validation reference in CONTRACTS.md | Reduce README sprawl; keep contract guidance in canonical index file. |
| 2026-04-03T15:07:00Z | Agent (audit fix) | Moved to product/contracts/ directory | Clarified directory boundaries; product/ root isolated for human-authored docs. |
