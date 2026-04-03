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
     - **Contract failure** (schema mismatch, OpenAPI generation error, field drift) → this is a **contract issue**, not a code bug. **STOP** and raise a CCR (see `/ccr` workflow). Do not attempt a code workaround.
     - **Lint / format / typecheck failure** → propose the minimal code fix and re-run `make check`.
     - **Test failure** → investigate whether the test or the code is wrong. If the test reflects a contract expectation, treat as contract failure above.
3) If it passes:
   - Log evidence in `process/PROGRESS.md` (command + outcome).

## Definition of Done (unified)
A task/story is Done only when all three are true:
1. `make check` passes (Green).
2. Evidence logged in `process/PROGRESS.md`.
3. Acceptance criteria in `product/PRD.md` are satisfied.

## Notes
- This skill is optional. The process works without it.
- Determinism comes from the repo's `Makefile` and the `check` target, not from markdown.
