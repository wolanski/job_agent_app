---
description: advise — Get structured recommendations on a decision
---

# /advise — Get structured recommendations

Use this workflow when facing a decision where you want the agent's analysis before choosing. Especially useful during design phases (P0–P4) and for unfamiliar technical areas.

READ:
- product/PRD.md (scope constraints)
- product/ARCH.md (current architecture decisions)
- product/contracts/* (interface commitments)
- process/PROGRESS.md (current state, prior decisions)
- Relevant code, docs, or external references for the decision at hand

DO:
1) State the decision to be made and the context clearly.
2) Present **2–3 options**, each with:
   - Brief description
   - Tradeoffs: complexity, scalability, maintenance burden, fit with user's skillset
   - Alignment with existing ARCH / contracts / PRD
3) Give a **recommendation** with rationale (1–3 sentences).
4) Assess **impact** on existing artifacts:
   - Would ARCH need updating?
   - Would contracts change?
   - Which stories/tasks are affected?
5) Ask the human to choose (or propose a hybrid / alternative).
6) After the human chooses, log a **Decision (D-###)** in `process/PROGRESS.md` with rationale and impact.

NOTES:
- During P0–P4, ARCH and contracts are drafts — decisions can reshape them freely without CCR.
- During P5–P7, if the chosen option requires ARCH/contract changes, raise a CCR via `/ccr`.
- This workflow uses the lightweight response protocol (READ/ACT/ASK) unless the chosen option triggers implementation.
