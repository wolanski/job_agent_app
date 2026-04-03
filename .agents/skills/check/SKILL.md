---
name: Check
description: Run the authoritative project validation suite (Definition of Done gate).
---

# Check (optional Skill)

**Purpose:** Provide a deterministic "Done" gate by running the canonical validation entrypoint.

## Instructions
1) Run:
   - `make check`
2) If it fails, **triage before fixing**:
   - Capture the error output (short excerpt).
   - Determine the failure category:
     - **Contract failure** (schema mismatch, OpenAPI generation error, field drift, or `test_contract_conformance.py` failure) → this is a **contract issue**, not a code bug. **STOP** and raise a CCR (see `/ccr` workflow). Do not attempt a code workaround.
     - **Lint / format / typecheck failure** → propose the minimal code fix and re-run `make check`.
     - **Test failure** → investigate whether the test or the code is wrong. If the test reflects a contract expectation, treat as contract failure above.
     - **Environment / infra failure** (missing `uv`, broken venv, network timeout, missing system tool) → this is not a code issue. Log as Issue (I-###) in PROGRESS, fix the environment, and re-run. Do not conflate with code or contract failures.
3) If it passes:
   - Log evidence in `process/PROGRESS.md` (command + outcome).

## Definition of Done
See `process/PROCESS_REFERENCE.md` § Definition of Done (single source of truth).

## Notes
- This skill is optional. The process works without it.
- Determinism comes from the repo's `Makefile` and the `check` target, not from markdown.
