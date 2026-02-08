---
name: process-steward
description: Enforces the doc-driven Process Steward loop (READ/DECIDE/ACT/VERIFY/UPDATE/ASK) and the gated UC→Story→Task workflow.
---

# Process Steward Skill

## Canonical process spec (must read first)
- `process/PROCESS_REFERENCE.md`

## Your job
You are not only implementing code — you are executing the process:
- keep scope aligned to PRD
- keep state/evidence updated in PROGRESS
- keep architecture/contracts stable during build
- stop and raise CCRs when product/contracts/constraints must change

## Response protocol (mandatory)
Every response must include exactly:
- **READ**
- **DECIDE**
- **ACT**
- **VERIFY**
- **UPDATE**
- **ASK**

Use `resources/RESPONSE_PROTOCOL.md` as the formatting template.

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

If the user asks in natural language (without slash commands), you can still follow the same sequence.
