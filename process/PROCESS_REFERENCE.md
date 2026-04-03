# Process Reference (Lean Agentic Dev, Antigravity)

**This is the canonical process spec the agent must read first each session.**

## Source of truth
- Scope: `product/PRD.md`
- Architecture (static): `product/ARCH.md` (**drafts in P0–P4**; **approval-controlled / RO during build P5+**)
- Interfaces: `product/contracts/*` (**drafts in P0–P4**; **RO during build P5+ unless CCR approved**)
- State + evidence: `process/PROGRESS.md` (single source of truth)
- Process diagrams (human-facing reference, optional reads unless explicitly requested):
  - `process/diagrams/PROCESS_MAIN.puml`
  - `process/diagrams/STATE_MODEL.puml`
  - `process/diagrams/PROCESS_STEWARD_SEQUENCE.puml` (detailed sequence)

## Non-negotiable rules
1. **Not in PRD = not built.**
2. **ARCH and contract mutability:**
   - **P0–P4 (design phases):** `product/ARCH.md` and `product/contracts/*` are **drafts** — freely modifiable without CCR. Log significant changes as Decisions (D-###) in PROGRESS.
   - **P5–P7 (build phases):** `product/ARCH.md` and `product/contracts/*` are **read-only**. Changes require a CCR.
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

**Note:** Workflow steps (`/seed`, `/plan`, `/next`, etc.) define *what* to do. The response protocol defines *how* to structure every response. Always apply both.

### Lightweight mode
The lightweight response protocol (READ / ACT / ASK) may be used in two situations:

1. **Informational queries** (any phase): For purely informational questions ("What phase are we in?", "Summarize PROGRESS", "Explain X") that involve **no code changes, no state mutations, and no decisions**.

2. **Design-phase responses** (P0–P4): During design phases, any response that does **not** involve production code implementation may use the lightweight protocol. This includes `/explore` findings, `/advise` recommendations, ARCH/contract drafting, story planning, and decision discussion.

Use the full 6-section protocol (READ / DECIDE / ACT / VERIFY / UPDATE / ASK) for:
- All implementation work (P5+)
- Any response that changes production code, regardless of phase
- Release and deployment activities (P8+)

## Phase model (P0–P12)
Phases define where the project is in its lifecycle. During **P0–P4**, ARCH and contracts are drafts (freely modifiable). During **P5–P7**, ARCH and contracts are **frozen** (RO unless CCR approved).

| Phase | Name | Activity | Workflow | Gate |
|-------|------|----------|----------|------|
| P0 | Install and Wire | Validate workspace, `make check` runs | `/seed` | G0 |
| P1 | Functional Framing | Draft/refine PRD scope and acceptance | `/plan` | G1 |
| P2 | Architecture (Lite) | Draft/stabilize ARCH | `/plan` | — |
| P3 | Contract Baseline | Define executable contracts | `/plan` | — |
| P4 | Story Baseline | Stories approved, trackers set | `/plan` | G2 |
| P5 | JIT Planning | Create task list for next story | `/next` | — |
| P6 | Iterative Implementation | Implement tasks, run `make check` | `/next` | — |
| P7 | Story Handshake | Verify story acceptance criteria met | `/next` | G3 |
| P8 | Integration Testing | Cross-story integration checks | `/release` | — |
| P9 | E2E Automation | Automated end-to-end tests | `/release` | — |
| P10 | Manual E2E (optional) | Human-run smoke tests | `/release` | G4 |
| P11 | Deploy | Ship release candidate | `/release` | G5 |
| P12 | Post-release Feedback | Retrospective, backlog grooming | `/explore` | — |

**P5–P7 repeat per story** (loop via `/next`). Contracts/ARCH are frozen during these phases unless a CCR is approved.

### Contracts-first projects
In some projects (especially architect-led ones), detailed contracts may exist before stories are written. In this case, `/plan` should derive stories from the existing contracts rather than designing contracts from stories. The stories-first principle still applies to the _approval boundary_ (stories are what the Human approves), even if contracts were the design starting point.

### Phase regression
Real projects sometimes need to revisit earlier phases:
- **Requirements change during build (P5–P7):** If the change invalidates the story baseline (P4), raise a CCR if contracts are affected, or log a Decision (D-###) in PROGRESS. Update the affected stories/tasks and re-enter P4 (story baseline) before resuming P5.
- **Architecture change needed during build:** Requires a CCR (since ARCH is RO during P5–P7). If approved, re-enter P2/P3 to stabilize ARCH and contracts before resuming P5.
- **General rule:** Log the regression as a Decision in PROGRESS with rationale. Update the phase tracker to reflect the current phase accurately.
- **Design-phase iteration (P0–P4):** ARCH and contracts are expected to evolve. No CCR is needed — simply update the documents and log a Decision (D-###) in PROGRESS if the change is significant. The `/advise` workflow can help structure these decisions.

## Story & task naming conventions
- **Stories:** `S-V###` (e.g., `S-V001`, `S-V002`). The `V` prefix denotes the product version.
- **Tasks:** `T-V###.##` (e.g., `T-V001.01`). The prefix matches the parent story.
- **Risk tags:** `LOW` (agent proceeds autonomously), `MED` (agent proceeds, human reviews), `HIGH` (agent stops and asks before acting).
- **CCR IDs:** `CCR-###` (e.g., `CCR-001`). Sequential, logged in PROGRESS.
- **Decision IDs:** `D-###`. **Issue IDs:** `I-###`. Sequential in PROGRESS.

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
- `.agents/rules/process-steward.md`
- `product/PRD.md`
- `product/ARCH.md`
- `product/contracts/CONTRACTS.md` *(policy/invariants/index)*

### All other files (no per-file trace table)
For everything else (including `process/PROGRESS.md`, setup guides, workflows, diagrams, and any docs you create):
- **Do not maintain per-file trace tables.**
- Rely on **Git diff/history** for the *what*.
- Record the *why* in `process/PROGRESS.md` using:
  - **Decisions log** (D-###) for intentional choices
  - **Issues log** (I-###) for problems/questions
  - **Evidence log** for `make check` outputs

### Executable contracts (`product/contracts/*`)
- **P0–P4 (design phases):** Changes are expected (drafts). Log significant changes as Decisions (D-###) in PROGRESS. No CCR required.
- **P5–P7 (build phases):** Changes require a **CCR entry** + human decision in `process/PROGRESS.md`.
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
| 2026-04-03T11:06:00Z | Agent (audit fix) | Fixed `.agent/` → `.agents/` path; added Phase Model (P0–P12) section; added Story & Task naming conventions; connected workflows to response protocol | Audit findings: undefined phases, missing naming spec, broken path, workflow-protocol disconnect. |
| 2026-04-03T12:35:00Z | Agent (audit fix) | Added lightweight response mode; added phase regression guidance; mapped P12 to `/explore` | Fixes W-03, W-05, I-06 from `.agents/` audit. |
| 2026-04-03T14:00:00Z | Agent (process update) | Expanded lightweight mode to P0–P4 design phases; made ARCH/contract draft status during P0–P4 explicit; added /advise workflow reference | Shift to two-phase model: relaxed ceremony in design, disciplined build in P5+. |
| 2026-04-03T15:30:00Z | Agent (review fix) | Added P0–P4 draft status to Source of Truth header; added contracts-first project note | Fixes I-07 (missing draft status in header) and W-03 (inverted stories-first guidance). |