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
Every response must include exactly these six sections:
- **READ** — what you read (PRD/ARCH/PROGRESS/contracts + relevant code)
- **DECIDE** — what you will do and why; what you will not do (scope guardrails)
- **ACT** — actions executed or proposed
- **VERIFY** — how you verified (tests/commands/contract validation) + results
- **UPDATE** — what you updated in PROGRESS and/or trace-controlled docs
- **ASK** — minimal set of questions/approvals needed from the human

See `.agents/skills/process-steward/resources/RESPONSE_PROTOCOL.md` for the fill-in template.

**Important:** Workflow steps (`/seed`, `/plan`, `/next`, etc.) define *what* to do. This protocol defines *how* to structure every response. Always apply both together.

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
Prefer the workspace workflows:
- `/seed` → `/plan` → `/next` loop → `/release`
- `/ccr` — escalation (can be triggered from any phase)
- `/explore` — investigatory or exploratory work outside the linear pipeline

If the user asks in natural language (without slash commands), you can still follow the same sequence.
