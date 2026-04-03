---
description: seed — Seed workspace & validate prerequisites
---

# /seed — Seed workspace & validate prerequisites

READ:
- process/PROCESS_REFERENCE.md
- product/PRD.md
- process/PROGRESS.md
- product/ARCH.md
- product/contracts/*

DO:
1) Confirm folder structure and required files exist.
2) Propose or confirm the `make check` entrypoint (lint/typecheck/tests/contract validation).
3) Run `make check` and log result as evidence.
4) Update PROGRESS:
   - set current phase to P0
   - log any missing prerequisites as Issues (I-###)
5) Ask only for missing information required to proceed.