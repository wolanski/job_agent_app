# Antigravity Workspace Customization (.agent)

Antigravity loads workspace customizations from this folder.

## What’s inside
- `rules/` — always-on instructions (system-like constraints)
- `workflows/` — saved prompts you trigger with `/` (e.g., `/seed`, `/plan`, `/next`, `/release`)
- `skills/` — optional “lazy-loaded” specialized guides (metadata + detailed instructions)

The Process Steward workflow is defined by:
- Rules: `rules/process-steward.md`
- Skill (optional but recommended): `skills/process-steward/SKILL.md`
- Process spec: `process/PROCESS_REFERENCE.md`

## Start
1) `/seed`
2) `/plan`
3) `/next` (repeat)
4) `/release`
