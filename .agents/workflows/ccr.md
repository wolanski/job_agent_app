---
description: ccr — Raise a Contract Change Request (CCR)
---

# /ccr — Raise a Contract Change Request (CCR)

READ:
- process/PROGRESS.md
- product/contracts/*
- product/PRD.md (acceptance impact)

DO:
1) Create a new `CCR-###` entry in PROGRESS with:
   - problem statement
   - failing evidence (what broke / where — include `make check` output if applicable)
   - minimal change proposal (what to change in product/contracts/*)
   - impact analysis (what code/stories/tests are affected)
2) **STOP** all implementation on the affected task.
3) Ask for a human decision (approve/reject/defer).
4) Only apply contract changes after approval is recorded.

RESPONSE: Follow the READ/DECIDE/ACT/VERIFY/UPDATE/ASK protocol.