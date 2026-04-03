# Antigravity Workspace Customization (.agents)

Antigravity loads workspace customizations from this folder.

## What's inside
- `rules/` — always-on instructions (system-like constraints)
- `workflows/` — saved prompts you trigger with `/` (e.g., `/seed`, `/plan`, `/next`, `/explore`, `/release`)
- `skills/` — optional "lazy-loaded" specialized guides (metadata + detailed instructions)

The Process Steward workflow is defined by:
- Rules: `rules/process-steward.md` (always loaded — persona, source-of-truth pointers, non-negotiables)
- Skill (optional): `skills/process-steward/SKILL.md` (operational shortcuts, CCR protocol, response protocol template)
- Canonical spec: `process/PROCESS_REFERENCE.md` (authoritative detail — phases, naming, traceability)

## How they relate
```
rules/process-steward.md      ← always on; sets persona + invariants
       ↓ points to
process/PROCESS_REFERENCE.md  ← canonical detail (phases, naming, traceability)
       ↓ elaborated by
skills/process-steward/        ← operational helpers (CCR protocol, response template)
skills/check/                  ← `make check` gate + failure triage
```

The **rules** file is thin (constraints + pointers). **PROCESS_REFERENCE** is the single detailed spec. **Skills** provide actionable steps the agent loads on demand.

## Start
1) `/seed`
2) `/plan`
3) `/next` (repeat)
4) `/release`

Use `/explore` for investigatory or ad-hoc work outside the linear pipeline.
Use `/ccr` to raise a Contract Change Request at any time.
