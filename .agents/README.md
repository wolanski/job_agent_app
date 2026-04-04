# Antigravity Workspace Customization (.agents)

Antigravity loads workspace customizations from this folder.

## What's inside
- `rules/` — always-on instructions (system-like constraints)
- `workflows/` — saved prompts you trigger with `/` (e.g., `/explore`, `/advise`, `/seed`, `/plan`, `/next`, `/check`, `/release`)
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

### Phase A — Collaborative Design (relaxed ceremony)
```
/explore × N  — spike unfamiliar areas, tech research
/advise  × N  — get structured recommendations on decisions
/seed          — validate workspace
/plan          — informed story planning (ARCH + contracts + stories)
```

### Phase B — Disciplined Build (frozen ARCH/contracts)
```
/next  × N     — implement with frozen ARCH/contracts
/check         — validate (make check gate)
/release       — harden and ship
```

`/ccr` and `/explore` remain available at any phase.
`/advise` is most valuable in Phase A but can be used anytime.

## Frontmatter schema

| Type | Required fields | Notes |
|------|----------------|-------|
| Rule | `trigger:` (`always_on` or condition) | Loaded automatically by Antigravity |
| Skill | `name:`, `description:` | Loaded on demand via `view_file` |
| Workflow | `description:` | Triggered by `/command` slash syntax |
