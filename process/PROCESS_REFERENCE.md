# Process Reference (Lean Agentic Dev, Antigravity)

**This is the canonical process spec the agent must read first each session.**

## Source of truth
- Scope: `product/PRD.md`
- Architecture (static): `product/ARCH.md` (**approval-controlled**; RO during build)
- Interfaces: `product/contracts/*` (**RO during build unless CCR approved**)
- State + evidence: `process/PROGRESS.md` (single source of truth)
- Process diagrams (human reference):
  - `process/diagrams/PROCESS_MAIN.puml`
  - `process/diagrams/STATE_MODEL.puml`
  - `process/diagrams/PROCESS_STEWARD_SEQUENCE.puml` (detailed sequence)

## Non-negotiable rules
1. **Not in PRD = not built.**
2. **RO during build (P5–P7):**
   - `product/ARCH.md`
   - `product/contracts/*`
3. Contract mismatch/drift → **STOP**, raise **CCR-###** in `process/PROGRESS.md` with evidence + minimal proposal; wait for human decision.
4. Nothing is Done unless:
   - `make check` is green, and
   - evidence is recorded in `process/PROGRESS.md`, and
   - acceptance criteria in `product/PRD.md` are satisfied.

## Validation entrypoint
- Authoritative gate: `make check` (uses `uv` + Python tooling)

## Definition of Done
1. `make check` passes (Green).
2. Evidence logged in `process/PROGRESS.md` (link logs/commands).
3. Story acceptance criteria met (per PRD).

## Mandatory response protocol (Process Steward)
Every response must contain exactly:
- READ / DECIDE / ACT / VERIFY / UPDATE / ASK

## Creating new artifacts
You may create new `.md` and `.puml` files when requested or beneficial:
- Product artifacts: `product/docs/`, `product/diagrams/`
- Process artifacts (operator/process docs): `process/guides/`, `process/diagrams/`

Governance note:
- If a change modifies the **rules**, **gates**, or **authority** model, treat it as approval-controlled and log a Decision in `process/PROGRESS.md`.

## Traceability policy (lean)

**Goal:** capture the *reason* for changes to governing truth without turning every doc edit into ceremony.

### Trace-controlled documents (per-file log required)
If you modify any file in this list, you **must append exactly one new row** to its **Traceability Log** table (append-only, UTC `YYYY-MM-DDThh:mm:ssZ`).
- `process/PROCESS_REFERENCE.md`
- `.agent/rules/process-steward.md` *(in this pack: `agent/rules/process-steward.md` until you rename `agent/` → `.agent/`)*
- `product/PRD.md`
- `product/ARCH.md`
- `product/CONTRACTS.md` *(policy/invariants/index)*

### All other files (no per-file trace table)
For everything else (including `process/PROGRESS.md`, setup guides, workflows, diagrams, and any docs you create):
- **Do not maintain per-file trace tables.**
- Rely on **Git diff/history** for the *what*.
- Record the *why* in `process/PROGRESS.md` using:
  - **Decisions log** (D-###) for intentional choices
  - **Issues log** (I-###) for problems/questions
  - **Evidence log** for `make check` outputs

### Executable contracts (`product/contracts/*`)
- Changes require a **CCR entry** + human decision in `process/PROGRESS.md`.
- No per-file trace table is required in the contract files.

### Response UPDATE requirements
In every response, the **UPDATE** section must state:
- which **trace-controlled** documents received a new trace row (if any), and
- which sections/entries were appended/updated in `process/PROGRESS.md`.

## Traceability Log
| Timestamp (UTC) | Actor | Change | Why |
|---|---|---|---|
| 2026-02-08T12:00:00Z | Seed (generator) | Updated paths + DoD | Split product vs process and standardized `make check`. |
| 2026-02-08T15:52:05Z | Seed (generator) | Clarified uv-based validation entrypoint | Align process DoD with FastAPI+uv Makefile gate. |
| 2026-02-08T16:10:00Z | Seed (generator) | Scoped traceability policy to 5 governing docs | Reduce noise; PROGRESS + Git remain authoritative for other changes. |
| 2026-02-08T17:05:19Z | Seed (generator) | Added explicit diagram list + referenced PROCESS_STEWARD_SEQUENCE + aligned verifier wording to `make check` | Keep process reference aligned with v7 pack artifacts and verifier. |
| 2026-02-08T17:32:05Z | Seed (generator) | Reorganized process folder (guides vs canonical truth) | Clarify that `process/` holds canonical truth and that operator docs live under `process/guides/human/`; updated new-artifact paths accordingly. |
| 2026-02-08T19:58:27Z | Seed (generator) | Updated operator guide path | Consolidated operator guidance into `process/guides/HUMAN_OPERATOR_GUIDE.md`; updated process artifact path. |