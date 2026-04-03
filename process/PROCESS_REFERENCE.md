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

2. **Design-phase responses** (P0–P4): During design phases, any response that does **not** involve production code implementation may use the lightweight protocol. This includes `/explore` findings, ARCH/contract drafting, story planning, and decision discussion. (Note: `/advise` requires the full protocol because it logs a Decision in PROGRESS.)

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

## PROGRESS archiving (post-release)
After a release gate (G5) is passed, archive shipped data to keep `process/PROGRESS.md` lean for the agent's context window:
1. Create `process/archive/R-YYYYMMDD.md` (using the release ID from PROGRESS § Release notes).
2. Move to the archive file:
   - Completed stories and their JIT task tables
   - Closed CCR entries (APPROVED/REJECTED)
   - Resolved Issues (CLOSED)
   - Decisions related to shipped stories
   - Evidence log entries for the shipped release
   - The release notes block for that release
3. In PROGRESS.md:
   - Remove the archived rows from each table
   - Reset "Current story" and "Current task" to [NONE]
   - Update the phase tracker for the new version
4. Register the archive file in PROGRESS § Artifacts added.

The archive files are read-only historical records. Do not modify them after creation.

## Traceability policy (lean)

**Goal:** capture the *reason* for changes to governing truth without turning every doc edit into ceremony.

### Trace-controlled documents (per-file log required)
If you modify any file in this list, you **must append exactly one new row** to its **Traceability Log** table (append-only, UTC `YYYY-MM-DDThh:mm:ssZ`).
- `process/PROCESS_REFERENCE.md`
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
*(Historical rows cleared to preserve clean template state)*
| Timestamp (UTC) | Actor | Change | Why |
|---|---|---|---|