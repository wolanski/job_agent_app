---
description: check — Run the validation gate (make check)
---

# /check — Run the validation gate
**Phases:** Any (mandatory before marking a task Done)

READ:
- process/PROGRESS.md (current task context)

DO:
1) Run `make check`.
2) Triage failures per `.agents/skills/check/SKILL.md` (if unfamiliar with triage rules, use `view_file` to read it first).
3) Log result in PROGRESS § Evidence log.
