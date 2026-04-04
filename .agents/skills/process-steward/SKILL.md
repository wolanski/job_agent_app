---
name: process-steward
description: Enforces the doc-driven Process Steward loop (READ/DECIDE/ACT/VERIFY/UPDATE/ASK) and the gated Story→Task workflow.
---

# Process Steward Skill

## Canonical process spec (must read first)
- `process/PROCESS_REFERENCE.md` — the single source of detail for phases, naming conventions, traceability policy, and artifact authoring rules.

This skill provides **operational shortcuts**; PROCESS_REFERENCE is authoritative if anything here conflicts.

## Your job
You are not only implementing code — you are executing the process:
- keep scope aligned to PRD
- keep state/evidence updated in PROGRESS
- keep architecture/contracts stable during build (P5–P7)
- stop and raise CCRs when product/contracts/constraints must change

## Response protocol (mandatory)
Always apply the response protocol exactly as defined in `process/PROCESS_REFERENCE.md` and related templates.

## CCR escalation protocol (mandatory)
If you detect contract drift, missing fields, incompatible naming, or a required contract change:
1) **STOP** implementation of the affected task
2) Write a new `CCR-###` entry in `process/PROGRESS.md` including:
   - evidence (failing tests / validation output)
   - minimal change proposal
   - impact analysis (what breaks / migration)
3) Ask the human to approve/reject/defer
4) Only apply contract changes if approved.

## How to use workflows

### Phase A — Collaborative Design (P0–P4, relaxed ceremony)
- `/explore` — spike unfamiliar areas, tech research, investigations
- `/advise` — get structured recommendations on decisions (2–3 options + recommendation)
- `/seed` — validate workspace and `make check` gate
- `/plan` — build-ready context, ARCH/contracts drafting, story planning

### Phase B — Disciplined Build (P5+, frozen ARCH/contracts)
- `/next` — implement next task (JIT tasks + tests + evidence)
- `/check` — run `make check` validation gate
- `/release` — hardening, release candidate, release notes

### Any phase
- `/ccr` — raise Contract Change Request (STOP — required in P5–P7 for ARCH/contract changes)
- `/explore` — ad-hoc investigation (also useful in Phase B for debugging)

If the user asks in natural language (without slash commands), you can still follow the same sequence.
