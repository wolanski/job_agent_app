---
name: Check
description: Run the authoritative project validation suite (Definition of Done gate).
---

# Check (optional Skill)

**Purpose:** Provide a deterministic “Done” gate by running the canonical validation entrypoint.

## Instructions
1) Run:
   - `make check`
2) If it fails:
   - capture the error output (short excerpt)
   - propose the minimal fix
   - re-run `make check`
3) If it passes:
   - log evidence in `process/PROGRESS.md` (command + outcome)

## Notes
- This skill is optional. The process works without it.
- Determinism comes from the repo’s `Makefile` and the `check` target, not from markdown.
