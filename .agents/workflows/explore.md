---
description: explore — Investigatory or exploratory work (no linear pipeline)
---

# /explore — Investigatory or exploratory work

Use this workflow for tasks that don't fit the linear `/seed → /plan → /next → /release` pipeline:
- Debugging sessions
- Architecture spikes / tech research
- "How does X work?" investigations
- Code review or audit
- Ad-hoc analysis or documentation

READ:
- process/PROGRESS.md (current state awareness)
- Relevant source files or docs for the investigation

DO:
1) State the goal and scope of the exploration clearly.
2) Perform the investigation (read code, run commands, research, etc.).
3) Summarize findings with evidence (code snippets, command output, references).
4) If the exploration reveals actionable work:
   - Log it as an Issue (I-###) or Decision (D-###) in PROGRESS.
   - If it affects contracts or ARCH, raise a CCR via `/ccr`.
5) Do **not** make production code changes unless explicitly requested.
6) Still follow the READ/DECIDE/ACT/VERIFY/UPDATE/ASK response protocol.

NOTES:
- This workflow is intentionally lightweight. The response protocol still applies.
- Exploratory findings that lead to stories should be fed back into `/plan`.
