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
*(Historical rows cleared to preserve clean template state)*
| Timestamp (UTC) | Actor | Change | Why |
|---|---|---|---|
