---
description: next — Execute the next safe unit of work
---

# /next — Execute the next safe unit of work

READ:
- product/PRD.md
- process/PROGRESS.md
- product/ARCH.md
- product/contracts/*

DO:
1) Select next story/task according to PRD sequence and PROGRESS state.
2) If story has no JIT task list, create one (5–15 tasks) using `T-V###.##` naming with risk tags (`LOW`/`MED`/`HIGH`).
3) Update phase to P5 (planning), P6 (implementing), or P7 (handshake) as appropriate.
4) Implement next task minimally + add/adjust tests.
5) Run `make check`:
   - If it fails due to **contract drift** → STOP and raise CCR-### (use `/ccr`).
   - If it fails due to **code/lint/test issue** → fix minimally and re-run.
6) Log evidence in PROGRESS.
7) If HIGH-risk task: ask for approval before acting.