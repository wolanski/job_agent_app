---
description: archive — Continuously clean up PROGRESS.md by moving old logs to an archive
---

# /archive — Continuously clean up PROGRESS.md
**Phases:** Any (Continuous/Mid-Release)

Use this workflow to prevent the Agent's context window from bloating by archiving old or resolved logs from `process/PROGRESS.md` before a full release gate (G5) is passed.

READ:
- process/PROGRESS.md
- process/PROCESS_REFERENCE.md (Archiving policy)

DO:
1) Analyze `process/PROGRESS.md` for obsolete logs. Look specifically for:
   - Closed or Resolved Issues
   - Approved/Rejected CCRs that are no longer actively relevant
   - Old Evidence logs tied to completed stories
2) If an archive file does not exist for the current cycle, create one: `process/archive/WIP-YYYYMMDD.md` (use today's date). If it exists, append to it.
3) Move the obsolete logs into the archive file under corresponding headers (e.g., `## Issues`, `## CCRs`, `## Evidence`).
4) Remove those rows cleanly from `process/PROGRESS.md`.
5) Ensure active stories, current JIT tasks, and Open/Pending decisions remain in `PROGRESS.md`.
6) If creating a new archive file, register it in `PROGRESS.md` § 11 Artifacts added.
7) Run `make check` to ensure no accidental formatting issues were introduced.

NOTES:
- Archiving is a structural refactor, not a logic change.
- Never modify the PRD, ARCH, or Contacts during an archive operation.
