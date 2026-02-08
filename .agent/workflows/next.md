# /next — Execute the next safe unit of work

READ:
- product/PRD.md
- process/PROGRESS.md
- product/ARCH.md
- product/contracts/*

DO:
1) Select next story/task according to PRD sequence and PROGRESS state.
2) If story has no JIT task list, create one (5–15 tasks) with risk tags.
3) Implement next task minimally + add/adjust tests.
4) Run `make check` and log evidence in PROGRESS.
5) If contract drift detected: STOP and raise CCR-### (no workaround).
6) Ask only if HIGH-risk approval or CCR decision is needed.
