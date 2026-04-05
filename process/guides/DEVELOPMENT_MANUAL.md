# Human Operator Development Manual -- Step-by-Step Guide

> Companion guide for `process/diagrams/USER_JOURNEY.puml`.
> Prerequisite: `product/docs/IDEATION_MANUAL.md` completed (all design artifacts committed, Gate G0 passed).

---

## Overview

This manual walks you through the **full development lifecycle** from first code to production release. It continues where the Ideation Process ended (Gate G0) and covers every human action, every workflow command, every decision point, and every artifact update through Gate G5 (Released).

The lifecycle has three phases that repeat per version:

```
Phase A: COLLABORATIVE DESIGN (P1-P4)    Steps 1-5    -> Approved stories + locked ARCH
Phase B: DISCIPLINED BUILD (P5-P7)       Steps 6-8    -> Working code, story-by-story
Phase C: RELEASE & ITERATE (P8-P12)      Steps 9-12   -> Deployed product + version archive
VERSION LOOP                                           -> Repeat for next version
```

**Who does what?**
- **You (Human Operator):** Type workflow commands, approve scope, review acceptance, decide CCRs, deploy.
- **Agent (Process Steward):** Read docs, draft proposals, write code, run tests, maintain state in PROGRESS.md.

**Core rule:** You control *product truth* (PRD, ARCH, contracts). The agent controls *process state* (PROGRESS.md, code, tests).

---

## Prerequisites

Before starting this manual, ensure:
- [x] Ideation Process complete (Steps 1-15 of IDEATION_MANUAL.md)
- [x] All design artifacts committed to repo (`product/PRD.md`, `product/ARCH.md`, `product/contracts/*`, `product/diagrams/*`)
- [x] `/seed` executed and Gate G0 = PASS in `process/PROGRESS.md`
- [x] `make check` runs green

---

## Truth Sources

These files govern the entire lifecycle. Know where to find each one:

| File | What it contains | Who owns it |
|------|-----------------|-------------|
| `product/PRD.md` | Scope: vision, stories (S-V###), acceptance criteria, roadmap | **Human** (approval-controlled) |
| `product/ARCH.md` | Architecture: tech stack, repo map, conventions, security | **Human** (read-only during P5-P7) |
| `product/contracts/*` | Interfaces: Pydantic schemas, OpenAPI spec, contract invariants | **Human** (read-only during P5-P7) |
| `process/PROGRESS.md` | State: current phase, story tracker, JIT tasks, CCRs, decisions, evidence | **Agent** (maintained continuously) |
| `process/PROCESS_REFERENCE.md` | Rules: phase model, naming conventions, traceability, response protocol | **Canonical spec** (append-only) |

---

## Workflow Commands Reference

You interact with the agent primarily through workflow commands typed in the IDE chat console. Each command activates a specific behavioral protocol in the agent.

| Command | Phase | Purpose | Modifies state? |
|---------|-------|---------|----------------|
| `/seed` | P0 | Validate workspace, run baseline `make check` | Yes (PROGRESS.md G0) |
| `/plan` | P1-P4 | Draft/refine stories, ARCH, contracts | Yes (PRD, ARCH, contracts, PROGRESS) |
| `/explore` | Any | Read-only investigation, research, spikes | Minimal (optionally I-### in PROGRESS) |
| `/advise` | Any | Structured decision analysis (2-3 options) | Yes (D-### in PROGRESS, may update ARCH/contracts in P0-P4) |
| `/next` | P5-P7 | Execute next task or story | Yes (code, tests, PROGRESS) |
| `/check` | Any | Run `make check` validation gate | Yes (evidence in PROGRESS) |
| `/ccr` | P5-P7 | Raise Contract Change Request escalation | Yes (CCR-### in PROGRESS, blocks task) |
| `/release` | P8-P11 | Hardening, release notes, deploy checklist | Yes (PROGRESS G4, G5, release notes) |
| `/archive` | Any | Sweep old logs from PROGRESS.md | Yes (PROGRESS trimmed, archive file created) |
| `/help` | Any | Print workflow index | No |

---

## Phase A: COLLABORATIVE DESIGN (P1-P4)

**Goal:** Converge on a stable story backlog with approved acceptance criteria, a locked architecture, and validated contracts so implementation can run smoothly.

**Key property:** During this phase, `product/ARCH.md` and `product/contracts/*` are **drafts** -- freely modifiable without a CCR. Iteration is expected and encouraged.

---

### Step 1: Scope Framing -- `/plan` (P1)

**Purpose:** Convert your vision into a concrete, approved story backlog. The agent reads your PRD vision and drafts stories with acceptance criteria, risk tags, and recommended sequencing. This is where human intent becomes buildable scope.

#### What you do

1. Open your IDE chat console.
2. Ensure `product/PRD.md` has at minimum a filled **S1. Vision** section (one-liner, primary user, problem statement). If you completed the Ideation Process, this is already done.
3. Type `/plan` and press Enter.
4. Wait for the agent to respond. It will present a proposed story backlog.

#### What the agent does

The agent executes the `/plan` workflow:
1. **Reads:** `product/PRD.md` (vision, scope), `product/ARCH.md` (constraints), `product/contracts/*` (existing interfaces), `process/PROGRESS.md` (current state), `process/PROCESS_REFERENCE.md` (naming conventions).
2. **Drafts:** A story backlog using `S-V###` naming (e.g., S-V001, S-V002):
   - Each story is a **vertical slice deliverable in <= 1 day**.
   - Each story has **acceptance criteria** in Given/When/Then format.
   - Each story has a **risk tag**: `LOW` (agent proceeds autonomously), `MED` (agent proceeds, human reviews), `HIGH` (agent stops and asks before acting).
   - Stories are grouped with optional **UC tags** (e.g., UC:SEARCH, UC:INGEST).
   - Stories are sequenced by dependency order.
3. **Updates:** `process/PROGRESS.md` phase to P1.
4. **Asks:** For your review and approval of the story-level scope.

#### What to look for in the agent's proposal

- **Story size:** Each story should be completable in one agent session (one day). If a story looks like more than a day of work, tell the agent to split it.
- **Acceptance criteria quality:** Each story needs 2-5 acceptance criteria in Given/When/Then format. Vague criteria ("should work well") will fail acceptance review later.
- **Risk tags:** HIGH-risk stories should be rare (destructive operations, irreversible changes). Most stories should be LOW or MED.
- **Sequencing:** Stories should build on each other. Foundation stories (health endpoint, data model) come before feature stories (search, ingestion).
- **Scope alignment:** Every story must trace back to your in-scope items from PRD.md S2. If the agent proposes a story that wasn't in your scope, reject it.

#### Expected output and where it goes

| Output | Target location |
|--------|----------------|
| Story index table (ID, title, UC tag, risk) | `product/PRD.md` > **S4. Story Backlog** > Story index |
| Full story definitions (summary, acceptance criteria, out-of-scope, dependencies) | `product/PRD.md` > **S4. Story Backlog** > one S-V### block per story |
| Roadmap mapping (version -> story IDs) | `product/PRD.md` > **S6. Roadmap** |
| Story tracker (operational copy) | `process/PROGRESS.md` > **S5. Story tracker** |
| Phase update | `process/PROGRESS.md` > **S0. Current status** > phase = P1 |

---

### Step 2: Research Spike -- `/explore`

**Purpose:** Investigate unknowns before committing to design decisions. This is a **safe sandbox** -- the agent reads code, docs, and external references but makes **no production code changes** and records **no architectural decisions**. Use it when you are unsure about a technology, a library's behavior, or how existing code works.

#### When to use it

- You encounter a technology or library you are unfamiliar with.
- You want to understand how an existing API works before designing an integration.
- You need to debug or audit existing code.
- You want to validate an assumption before committing to it in ARCH.md.

Use `/explore` *instead of* `/advise` when you need **raw information** (facts, research, code analysis) rather than a **structured decision** (options + recommendation).

#### What you do

1. Type `/explore` followed by your question or investigation goal. Be specific.
   - Good: `/explore How does cursor-based pagination work with SQLite? Show me a code example.`
   - Good: `/explore Investigate the Arbetsformedlingen API -- what auth does it require and what is the response format?`
   - Bad: `/explore Look into databases.` (too vague, the agent cannot scope the investigation)
2. Read the agent's findings summary.
3. If the findings are actionable (reveal a bug, a missing capability, or a design concern), tell the agent to log it as an Issue (I-###) in PROGRESS.md.

#### What the agent does

1. **Reads:** `process/PROGRESS.md` (current state awareness), optionally `product/PRD.md` and `product/ARCH.md` (if the investigation touches scope or architecture), and whatever source files, docs, or external references are relevant.
2. **Investigates:** Reads code, runs read-only commands, researches APIs or libraries.
3. **Summarizes:** Presents findings with evidence (code snippets, command output, API response examples).
4. **Optionally logs:** If findings reveal actionable work, logs an Issue (I-###) in PROGRESS.md.
5. **Does NOT:** Modify production code, log Decisions (D-###), or update ARCH/contracts. Those actions belong to `/advise` and `/plan`.

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Findings summary | IDE chat (not persisted to a file) |
| Actionable issues (if any) | `process/PROGRESS.md` > **S8. Issues log** (I-###) |

#### How it feeds back into the process

Findings from `/explore` inform your decisions in `/advise` and your scope in `/plan`. If the exploration reveals that a planned approach is infeasible, you return to `/plan` to adjust stories or to `/advise` to make a formal decision.

---

### Step 3: Decision Analysis -- `/advise`

**Purpose:** Get structured analysis when facing a design choice. Unlike `/explore` (which gathers information), `/advise` always produces a **logged Decision (D-###)** with rationale. Use it when you need to choose between alternatives and want the tradeoffs laid out clearly.

#### When to use it

- Choosing between technologies (SQLite vs. PostgreSQL, sync vs. async).
- Choosing between architectural patterns (monolith vs. microservices, embedded vs. separate search index).
- Any decision that will be hard to reverse once code is written.

Use `/advise` *instead of* `/explore` when you need a **recommendation** (which option to pick and why) rather than **raw information** (how something works).

#### What you do

1. Type `/advise` followed by the decision context. Be specific about what you are choosing between.
   - Good: `/advise Should we use SQLite FTS5 or a separate Elasticsearch instance for job search in the MVP? Our NFR says p95 < 500ms with 50K jobs.`
   - Good: `/advise Monolith vs. two services (ingestion + search). We have 1 developer and a 2-week timeline.`
   - Bad: `/advise What database should we use?` (too vague -- list the candidates and constraints)
2. Read the agent's analysis (2-3 options with tradeoffs and a recommendation).
3. Choose an option. Type your choice in chat: "Go with option 2" or "I prefer SQLite FTS5."
4. The agent logs your decision as D-### in PROGRESS.md.

#### What the agent does

1. **Reads:** `product/PRD.md` (scope constraints), `product/ARCH.md` (current architecture), `product/contracts/*` (interface commitments), `process/PROGRESS.md` (prior decisions), and any relevant code or external references.
2. **Presents 2-3 options**, each with:
   - Brief description of the approach.
   - **Tradeoffs:** complexity, scalability, maintenance burden, fit with your team's skills.
   - **Alignment:** How well does this option fit the existing ARCH, contracts, and PRD scope?
3. **Gives a recommendation** with a 1-3 sentence rationale.
4. **Assesses impact:** Would ARCH.md need updating? Would contracts change? Which stories are affected?
5. **Asks you to choose** (or propose a hybrid / alternative).
6. **After your choice:** Logs a **Decision (D-###)** in `process/PROGRESS.md` with the rationale and impact.
7. **If P0-P4:** May directly update `product/ARCH.md` or `product/contracts/*` to reflect the decision (these are drafts, so no CCR is needed).
8. **If P5-P7:** If the chosen option requires ARCH/contract changes, raises a CCR via `/ccr` (because ARCH/contracts are frozen during build).

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Decision record | `process/PROGRESS.md` > **S9. Decisions log** (D-###) |
| ARCH updates (if decision reshapes architecture, P0-P4 only) | `product/ARCH.md` > affected section |
| Contract updates (if decision reshapes interfaces, P0-P4 only) | `product/contracts/*` > affected file |

#### The key difference: /explore vs. /advise

| | `/explore` | `/advise` |
|-|-----------|----------|
| **Purpose** | Gather information | Make a decision |
| **Output** | Chat summary + optional I-### | Logged Decision D-### |
| **Modifies ARCH/contracts?** | Never | Yes (during P0-P4) |
| **Requires your choice?** | No | Yes (you pick an option) |
| **Response protocol** | Lightweight (READ/ACT/ASK) | Full (READ/DECIDE/ACT/VERIFY/UPDATE/ASK) |

---

### Step 4: Architecture & Contracts -- `/plan` (P2-P3)

**Purpose:** Stabilize the architecture and contracts baseline so they can be frozen for build. The agent drafts ARCH.md and contracts; you review and iterate using `/explore` and `/advise` for any unresolved tradeoffs.

#### What you do

1. If not already in a `/plan` session, type `/plan` to continue the planning workflow.
2. Review the agent's proposed ARCH.md updates:
   - **Tech stack (S2):** Does it match your `/advise` decisions?
   - **Repo map (S3):** Are the paths reasonable for your project structure?
   - **Architecture snapshot (S4):** Does the C4-lite description match your mental model?
   - **Conventions (S5):** Naming, error handling, logging -- are these what you want?
3. Review the agent's proposed contracts baseline:
   - **schemas.py:** Do the Pydantic models cover all entities from your data model?
   - **openapi.yaml:** Do the endpoints cover all stories? Are request/response shapes correct?
   - **CONTRACTS.md:** Naming conventions, error model, invariants -- acceptable?
4. For any disagreements, use `/advise` (if choosing between options) or give direct feedback in chat.
5. The agent runs `make check` to validate contracts compile and tests pass.

#### What the agent does

1. **Drafts** `product/ARCH.md` sections S1-S7 (or updates existing sections).
2. **Drafts** minimal `product/contracts/` baseline: Pydantic models in `schemas.py`, OpenAPI spec in `openapi.yaml`, governance rules in `CONTRACTS.md`.
3. **Runs** `make check` to validate the baseline compiles and passes.
4. **Updates** `process/PROGRESS.md` phase to P2 (architecture) then P3 (contracts).
5. **Logs** significant changes as Decisions (D-###) in PROGRESS.md.

#### The design feedback loop

This step often iterates. The pattern is:

```
/plan (propose) -> you review -> /explore or /advise (resolve unknowns) -> /plan (revise) -> you review -> ...
```

This loop is expected and healthy. No ceremony is required for changes during P0-P4 -- ARCH and contracts are drafts. Iterate until the architecture and contracts align with your vision and stories.

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Architecture rules | `product/ARCH.md` > S1-S7 |
| Pydantic models | `product/contracts/schemas.py` |
| OpenAPI specification | `product/contracts/openapi.yaml` |
| Contract governance | `product/contracts/CONTRACTS.md` |
| Decisions logged | `process/PROGRESS.md` > **S9. Decisions log** |
| Phase update | `process/PROGRESS.md` > **S0. Current status** > phase = P2/P3 |

---

### Step 5: Baseline Approval -- `/plan` (P4)

**Purpose:** The point of no return. Once you approve, ARCH.md and contracts become **read-only** for the entire build phase (P5-P7). Any subsequent changes require a formal CCR (Contract Change Request) with your explicit approval.

#### What you do

1. Open `product/PRD.md` in your editor. Read every story (S-V###), its acceptance criteria, and its risk tag. Verify:
   - Every story is a vertical slice deliverable in <= 1 day.
   - Acceptance criteria are specific and testable (Given/When/Then).
   - Story sequence makes sense (dependencies respected).
   - No scope creep (every story traces to in-scope items in S2).
2. Open `product/ARCH.md` in your editor. Read the entire document. Verify:
   - Tech stack matches your decisions.
   - Repo map reflects your intended project structure.
   - Conventions are what you want the agent to follow.
   - Security notes are adequate for MVP.
3. Open `product/contracts/openapi.yaml`. Verify:
   - Every endpoint maps to at least one story.
   - Request/response schemas match `schemas.py`.
   - Error envelope is consistent.
4. When satisfied, return to the IDE chat console and type **"Approved"**.

#### What happens when you approve

The agent:
1. Finalizes story sequence and risk tags in PRD.md.
2. Sets governance policy in PROGRESS.md (approval levels, CCR rules, reorder rules).
3. Runs a final `make check` to confirm ready-to-build state.
4. Records **Gate G1** (Scope Approved: PRD stories accepted by Human) in PROGRESS.md with evidence.
5. Records **Gate G2** (Ready-to-Build: contracts validate + check green) in PROGRESS.md with evidence.

#### What is now locked

After G2, during all of P5-P7:
- `product/ARCH.md` is **read-only**. The agent cannot modify it. If the agent discovers ARCH needs to change, it must STOP and raise a CCR.
- `product/contracts/*` are **read-only**. Same rule -- changes require a CCR.
- `product/PRD.md` stories are the authoritative scope. "Not in PRD = not built."

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Governance policy | `process/PROGRESS.md` > **S1. Policy** |
| Gate G1 evidence | `process/PROGRESS.md` > **S2. Gates** > G1 row |
| Gate G2 evidence | `process/PROGRESS.md` > **S2. Gates** > G2 row |
| Phase update | `process/PROGRESS.md` > **S0. Current status** > phase = P4 |

---

### Phase A Checkpoint

At this point you should have:
- [x] `product/PRD.md` S4 complete (approved story backlog with acceptance criteria)
- [x] `product/ARCH.md` S1-S7 complete (architecture locked)
- [x] `product/contracts/*` complete (schemas, OpenAPI, governance locked)
- [x] `process/PROGRESS.md` Gates G1 + G2 = PASS
- [x] `process/PROGRESS.md` Story tracker populated

---

## Phase B: DISCIPLINED BUILD (P5-P7)

**Goal:** The agent implements each story as a vertical slice with tests and evidence. You validate acceptance. This is the high-tempo phase where `/next` is your primary command.

**Key property:** During this phase, `product/ARCH.md` and `product/contracts/*` are **frozen** (read-only). Changes require a CCR. This prevents specification drift and forces the agent to build what was agreed, not what is convenient.

---

### Step 6: JIT Task Planning -- `/next` (P5)

**Purpose:** The agent decomposes the next story into atomic, implementable tasks. Tasks are planned **Just-In-Time** (per-story, not upfront) because the optimal task breakdown often depends on what was learned in previous stories.

#### What you do

1. Type `/next` in the IDE chat console. No additional context is needed -- the agent tracks all state via PROGRESS.md.
2. The agent selects the next unstarted story from the PRD sequence and presents a JIT task plan.
3. Review the task plan, paying attention to:
   - **Task count:** 5-15 tasks is typical. Fewer may mean the story is too coarse; more may mean it is over-decomposed.
   - **HIGH-risk tasks:** If any tasks are tagged HIGH, you must explicitly approve them before the agent will act (see Human Risk Review below).
   - **Dependencies:** Tasks should be ordered logically (create model before write endpoint).
4. If the plan looks good and no HIGH-risk tasks exist, type `/next` again to start execution.
5. If HIGH-risk tasks exist, approve them first (see below).

#### What the agent does

1. **Reads:** `product/PRD.md` (story sequence and acceptance criteria), `process/PROGRESS.md` (current state, which stories are done).
2. **Selects:** Next unstarted story (S-V###) per PRD sequence.
3. **Decomposes:** Creates a JIT task checklist (5-15 tasks) using `T-V###.##` naming (e.g., T-V001.01, T-V001.02), with dependencies and risk tags.
4. **Updates:** `process/PROGRESS.md`:
   - Marks story as IN_PROGRESS in S5 (Story tracker).
   - Writes task list to S6 (Current story JIT tasks).
   - Sets phase to P5.

#### Human Risk Review (HIGH-risk tasks only)

HIGH-risk tasks involve destructive or irreversible operations: database schema drops, deployment script changes, security-critical code, external service integrations.

When HIGH-risk tasks exist:
1. The agent presents the task plan and **STOPS** on HIGH tasks.
2. Open `process/PROGRESS.md` > S6 and read the HIGH-risk task descriptions.
3. For each HIGH-risk task, type one of:
   - **"Approve T-V###.##"** -- the agent proceeds with that task.
   - **"Reject T-V###.##: [reason]"** -- the agent re-plans the task or removes it.
   - **"Modify T-V###.##: [instructions]"** -- the agent adjusts the task scope.
4. LOW and MED tasks proceed autonomously per the policy in PROGRESS.md S1.

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| JIT task checklist (T-V###.## entries) | `process/PROGRESS.md` > **S6. Current story JIT tasks** |
| Story status = IN_PROGRESS | `process/PROGRESS.md` > **S5. Story tracker** |
| Phase update | `process/PROGRESS.md` > **S0. Current status** > phase = P5, current story = S-V### |

---

### Step 7: Iterative Implementation -- `/next` + `/check` (P6)

**Purpose:** The agent implements each task minimally, runs tests, and logs evidence. This is the high-velocity execution loop where the agent writes code and you monitor progress.

#### What you do

1. **Keep typing `/next`** to advance through each task. The agent handles one task per `/next` invocation.
2. **Remove hands from keyboard** while the agent works. The agent is:
   - Reading the current task definition.
   - Writing minimal production code in `app/`.
   - Writing or updating unit tests in `tests/`.
   - Running `make check` automatically.
   - Logging evidence in PROGRESS.md.
3. **Monitor terminal output** for `make check` results. Green = task done. Red = agent is fixing.
4. The agent marks each task DONE and advances to the next task automatically.
5. Repeat `/next` until the agent signals that all story tasks are complete.

#### What the agent does per task

For each task `T-V###.##`:
1. **Marks** task as IN_PROGRESS in PROGRESS.md S6.
2. **Implements** minimal code change + unit tests (only enough to satisfy the task).
3. **Runs** `make check` automatically (lint, format, typecheck, contract validation, tests).
4. **If `make check` PASS:** Marks task as DONE, appends evidence to PROGRESS.md S10, advances to next task.
5. **If `make check` FAIL due to code/lint/test issue:** Fixes minimally and re-runs `make check`. Repeats until green.
6. **If `make check` FAIL due to contract drift:** STOPS and triggers `/ccr` escalation (see Step 7a).
7. **Updates** phase to P6.

#### What `make check` validates

`make check` is the single deterministic validation gate. It runs:

| Step | Command | What it catches |
|------|---------|-----------------|
| sync | `uv sync` | Missing dependencies |
| lint | `ruff check .` | Code quality issues, unused imports, style violations |
| format | `ruff format . --check` | Formatting inconsistencies |
| typecheck | `mypy .` | Type errors, missing annotations |
| contractcheck | schemas.py compile + OpenAPI validation | Schema drift between Pydantic models and OpenAPI spec |
| test | `pytest -q` | Functional regressions, failing assertions |

#### Failure triage protocol

When `make check` fails, the agent triages before fixing (per `.agents/skills/check/SKILL.md`):

| Failure type | Agent action | Your action |
|--------------|-------------|-------------|
| **Contract failure** (schema mismatch, OpenAPI drift, `test_contract_conformance.py` failure) | STOP. Raise CCR-###. | You decide: APPROVE, REJECT, or DEFER (see Step 7a) |
| **Lint / format / typecheck failure** | Fix minimally, re-run `make check`. | None (autonomous) |
| **Test failure** | Investigate: is the test wrong or the code wrong? If test reflects a contract expectation, treat as contract failure. | None unless escalated |
| **Environment failure** (missing uv, broken venv, network timeout) | Log Issue (I-###), fix environment, re-run. | May need to help resolve environment issues |

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Production code | `app/` (routers, services, adapters, models) |
| Unit tests | `tests/` |
| Task completion evidence | `process/PROGRESS.md` > **S10. Evidence log** |
| Task status = DONE | `process/PROGRESS.md` > **S6. Current story JIT tasks** |
| Phase update | `process/PROGRESS.md` > **S0. Current status** > phase = P6 |

---

### Step 7a: Contract Escalation -- `/ccr`

**Purpose:** The core safety mechanism of the Antigravity process. When the agent detects a mismatch between implementation reality and the frozen contracts/ARCH, it **STOPS** and escalates to you. No silent workarounds are allowed. This prevents specification drift -- the gap between what was designed and what was built.

#### When it happens

The agent triggers a CCR automatically when:
- A `make check` failure traces to a schema mismatch (Pydantic model vs. OpenAPI spec).
- Implementation reveals that an endpoint needs a field that doesn't exist in the contract.
- A test reflects a contract expectation that the code cannot satisfy without changing the contract.
- The agent discovers that ARCH.md conventions are impossible to follow for the current task.

#### What happens

1. The agent **STOPS** all implementation on the affected task.
2. The agent creates a **CCR-### entry** in `process/PROGRESS.md` > S7 containing:
   - **Problem statement:** What is the mismatch?
   - **Failing evidence:** `make check` output, specific test failures, the code-vs-contract conflict.
   - **Minimal change proposal:** The smallest possible change to contracts/ARCH that resolves the issue.
   - **Impact analysis:** What code, stories, and tests are affected by the proposed change?
3. The agent marks the current task as **BLOCKED** (reason: CCR-###).
4. The agent asks for your decision.

#### What you do

1. Open `process/PROGRESS.md` > S7 (CCR log) and read the CCR-### entry carefully.
2. Evaluate the evidence and the proposed change.
3. In the IDE chat, type exactly one of:

| Your response | What happens |
|--------------|-------------|
| **"APPROVE CCR-###"** | Agent updates `product/contracts/*` (or ARCH.md) with the minimal change, re-runs `make check`, verifies the fix, marks CCR as APPLIED+VERIFIED, resumes the blocked task. |
| **"REJECT CCR-###"** | Agent discards the proposed change, reverts any partial implementation for the affected task, marks the task as BLOCKED or re-plans it to honor the original contract. Logs a Decision (D-###) explaining the rollback. |
| **"DEFER CCR-###"** | Agent marks the task as BLOCKED, logs the deferral, and uses `/next` to move to the next unblocked task. The deferred CCR stays open for later resolution. |

#### Critical anti-pattern: Blind Approval

**Never approve a CCR without reading the evidence and proposal.** If the agent proposes removing a required field to make a test pass, your downstream integrations will break. The CCR mechanism exists to give you control -- use it.

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| CCR entry (problem, evidence, proposal, impact) | `process/PROGRESS.md` > **S7. CCR log** |
| Contract/ARCH update (if approved) | `product/contracts/*` or `product/ARCH.md` |
| Decision record (if rejected) | `process/PROGRESS.md` > **S9. Decisions log** (D-###) |
| Task status = BLOCKED | `process/PROGRESS.md` > **S6. Current story JIT tasks** |

---

### Step 7b: Context Cleanup -- `/archive`

**Purpose:** Keep the agent's working memory lean. As PROGRESS.md grows with completed tasks, closed CCRs, and old evidence, the agent's context window fills up, degrading response quality and speed. Archiving moves completed data to a separate file without losing it.

#### When to use it

- The agent's responses become slower or less focused.
- The agent starts forgetting constraints or repeating questions it already answered.
- PROGRESS.md has grown large (many completed stories, many evidence entries).
- General rule: archive after every 2-3 completed stories, or whenever you notice degradation.

#### What you do

1. Type `/archive` in the IDE chat console.
2. The agent sweeps PROGRESS.md and reports what was archived.
3. Verify that active stories and current JIT tasks were **not** archived (they should remain in PROGRESS.md).

#### What the agent does

1. **Reads:** `process/PROGRESS.md` (identifies obsolete logs), `process/PROCESS_REFERENCE.md` (archiving policy).
2. **Identifies** archivable data:
   - Completed tasks (all tasks marked DONE for finished stories).
   - Closed or Resolved Issues (I-###).
   - Approved/Rejected CCRs that are no longer actively relevant.
   - Old Evidence log entries tied to completed stories.
3. **Creates** (or appends to) an archive file: `process/archive/WIP-YYYYMMDD.md`.
4. **Moves** the obsolete logs into the archive file under corresponding headers.
5. **Removes** the archived rows from PROGRESS.md.
6. **Preserves:** All active stories, current JIT tasks, open Issues, pending CCRs, and pending Decisions.
7. **Registers** the archive file in PROGRESS.md > S11 (Artifacts added).
8. **Runs** `make check` to ensure no formatting issues were introduced.

#### What is safe

- `/archive` **never** modifies source code, PRD, ARCH, or contracts.
- `/archive` **never** removes active/in-progress work.
- Archive files are **read-only historical records**. Do not edit them after creation.

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Archive file | `process/archive/WIP-YYYYMMDD.md` (new or appended) |
| Lean PROGRESS.md | `process/PROGRESS.md` (obsolete rows removed) |
| Archive registration | `process/PROGRESS.md` > **S11. Artifacts added** |

---

### Step 8: Story Acceptance -- `/next` (P7)

**Purpose:** Verify that the completed story actually works for humans, not just for tests. A green `make check` proves the code is syntactically correct and tests pass, but it does **not** prove the feature delivers user value. This is the human quality gate.

#### What happens

When all tasks for a story are DONE, the agent enters Story Handshake mode (P7):
1. The agent summarizes what was built, which tests pass, and how the acceptance criteria are covered.
2. The agent asks you to validate: **"PASS or FAIL + notes?"**

#### What you do

1. **Boot the application:** Run `make run` (or `uv run fastapi dev`) to start the dev server locally.
2. **Physically test the feature:**
   - For API endpoints: use `curl`, `httpie`, or a tool like Postman to send requests and inspect responses.
   - For UI features: open the browser and interact with the interface.
   - For background processes: trigger the process and verify the output.
3. **Cross-reference against acceptance criteria:** Open `product/PRD.md` > S4 and read the Given/When/Then criteria for this story. Verify each one.
4. **Respond in IDE chat:**
   - **"PASS"** -- the story meets all acceptance criteria. Story is Done.
   - **"FAIL + notes"** -- describe what is wrong. Be specific: "FAIL. GET /jobs?q=python returns 0 results even though there are jobs with 'python' in the title." or "FAIL. Pagination cursor returns the same page when used twice."

#### If you respond PASS

The agent:
1. Marks the story as **DONE** in PROGRESS.md > S5 (Story tracker).
2. Records **Gate G3** evidence for this story in PROGRESS.md > S2 (Gates).
3. Clears the JIT task list in PROGRESS.md > S6.
4. If more stories remain in the backlog, prepares for the next `/next` cycle (returns to Step 6).
5. If all stories are done, signals readiness for Phase C (release).

#### If you respond FAIL

The agent:
1. Logs your feedback in PROGRESS.md.
2. Creates targeted fix tasks.
3. Implements the fixes.
4. Re-runs `make check`.
5. Asks for re-validation: **"PASS or FAIL?"**
6. Repeats until you respond PASS.

#### Critical anti-pattern: Fake QA

**Never type "PASS" without physically testing.** Automated tests verify code correctness. Only you can verify that the feature delivers the intended user experience. A search endpoint that returns results in random order will pass all tests but fail user expectations.

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Story status = DONE | `process/PROGRESS.md` > **S5. Story tracker** |
| G3 gate evidence (per story) | `process/PROGRESS.md` > **S2. Gates** > G3 row |
| JIT task list cleared | `process/PROGRESS.md` > **S6. Current story JIT tasks** |

---

### Story Loop

Steps 6-8 **repeat for each story** in the PRD backlog. The cycle is:

```
/next (P5: plan tasks) -> /next /next /next (P6: implement) -> acceptance review (P7: PASS/FAIL)
  |                                                                         |
  |                        ┌── /ccr if contract drift (Step 7a)             |
  |                        ├── /archive if context bloated (Step 7b)        |
  |                        └── /check for ad-hoc validation                 |
  |                                                                         |
  └─────────────────── next story ──────────────────────────────────────────┘
```

When all stories are DONE, proceed to Phase C.

---

### Phase B Checkpoint

At this point you should have:
- [x] All stories in PRD.md S4 marked DONE in PROGRESS.md S5
- [x] All tasks completed with evidence in PROGRESS.md S10
- [x] All CCRs resolved (APPLIED, REJECTED, or DEFERRED)
- [x] `make check` green
- [x] Each story physically validated by you (PASS)

---

## Phase C: RELEASE & ITERATE (P8-P12)

**Goal:** Verify cross-story integration, harden for production, deploy, and prepare for the next version.

---

### Step 9: Release Hardening -- `/release` (P8-P10)

**Purpose:** Shift from per-story validation to global system verification. During build, each story was tested in isolation. Release hardening tests that all stories work together correctly -- catching integration regressions, edge cases at story boundaries, and cross-cutting concerns (auth, error handling, logging).

#### What you do

1. Verify that all stories in the PRD are DONE (check PROGRESS.md > S5).
2. Type `/release` in the IDE chat console.
3. Wait for the agent to run global integration checks and E2E tests.
4. Review the draft release notes and deployment runbook.
5. **Optional manual E2E (P10):** The agent may ask you to run manual smoke tests against the running application. This is your last chance to catch issues before deployment.

#### What the agent does

1. **Verifies:** All stories are DONE (per PROGRESS.md S5 and PRD.md S4 acceptance criteria).
2. **Updates:** Phase to P8 (Integration Testing).
3. **Runs:** Global integration checks and cross-story E2E tests (if configured in the test suite). This is different from per-task `make check` -- it tests the full system end-to-end.
4. **Fixes:** Any regressions found during the global sweep.
5. **Drafts:** In PROGRESS.md > S12 (Release notes):
   - Version label and release date.
   - Summary of what was built (stories delivered).
   - Known issues and limitations.
   - Deployment runbook (steps to deploy, expected verification).
6. **Records:** Gate G4 (Release Candidate) in PROGRESS.md > S2.
7. **Optionally asks:** For manual E2E sign-off at P10 (smoke tests you run yourself).

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Integration test results | `process/PROGRESS.md` > **S10. Evidence log** |
| Release notes draft | `process/PROGRESS.md` > **S12. Release notes** |
| G4 gate evidence | `process/PROGRESS.md` > **S2. Gates** > G4 row |
| Phase update | `process/PROGRESS.md` > **S0. Current status** > phase = P8/P9/P10 |

---

### Step 10: Deployment -- `/release` (P11)

**Purpose:** Ship the release candidate to a live environment. The agent provides the runbook and checklist, but **you** perform the actual deployment. The agent cannot push to production autonomously -- deployment is always a human action.

#### What you do

1. Open the deployment runbook in PROGRESS.md > S12 (Release notes).
2. Deploy to your target environment using your preferred platform:
   - **Local/dev:** `make run` or `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Cloud platforms:** Fly.io (`fly deploy`), Railway, Render, Vercel, Cloud Run, etc.
   - **Container:** Build Docker image and push to registry.
   - **AWS/GCP/Azure:** Use your IaC pipeline or manual console deployment.
3. Run smoke tests against the live environment:
   - Hit the `/health` endpoint: `curl https://your-domain.com/health`
   - Hit key feature endpoints: search, ingest, etc.
   - Verify responses match the OpenAPI contract.
4. Report back to the agent in IDE chat:
   - **"DEPLOYED_OK"** + brief smoke test results.
   - **"FAIL + logs"** + paste the relevant error logs or describe the failure.

#### If deployment succeeds

The agent:
1. Records **Gate G5** (Released) in PROGRESS.md > S2 with deployment evidence and smoke results.
2. Finalizes release notes in PROGRESS.md > S12.
3. Updates phase to P11.

#### If deployment fails

The agent:
1. Diagnoses the failure from the logs you provide.
2. Proposes targeted fixes.
3. Re-runs `make check`.
4. Asks you to re-deploy.
5. This loop repeats until deployment succeeds or you decide to abort.

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| G5 gate evidence | `process/PROGRESS.md` > **S2. Gates** > G5 row |
| Finalized release notes | `process/PROGRESS.md` > **S12. Release notes** |
| Phase update | `process/PROGRESS.md` > **S0. Current status** > phase = P11 |

---

### Step 11: Retrospective -- `/explore` (P12)

**Purpose:** Reflect on the version just shipped. What worked well? What was painful? What should change for the next version? The retrospective produces insights that feed directly into the next version's planning cycle.

#### What you do

1. Share feedback with the agent:
   - What features worked well in production?
   - What user complaints or telemetry issues have surfaced?
   - What technical debt accumulated during build?
   - What priorities have changed since the original PRD?
2. Use `/explore` to analyze specific concerns (e.g., "Explore performance characteristics of the search endpoint under load").
3. Use `/advise` for strategic next-version decisions (e.g., "Advise: Should V1.1 prioritize performance optimization or new features?").
4. The agent proposes roadmap candidates for the next version.

#### What the agent does

1. **Summarizes** version learnings: stories delivered, CCRs raised and resolved, issues encountered, time spent per story.
2. **Proposes** backlog candidates for the next version based on your feedback and accumulated issues/decisions.
3. **Updates** `product/PRD.md` > S6 (Roadmap) with future story candidates.
4. **Logs** retrospective findings in PROGRESS.md.

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Roadmap candidates for next version | `product/PRD.md` > **S6. Roadmap** (updated) |
| Retrospective learnings | `process/PROGRESS.md` > **S9. Decisions log** or **S8. Issues log** |

---

### Step 12: Version Archive -- `/archive`

**Purpose:** Close out the completed version's tracking data and prepare a clean slate for the next version. Unlike mid-release archiving (Step 7b), this is a **full post-release archive** that moves everything from the shipped version into a permanent read-only record.

#### What you do

1. Type `/archive` in the IDE chat console.
2. The agent creates a release archive file and clears PROGRESS.md.
3. Verify that PROGRESS.md is clean and ready for the next version.

#### What the agent does

1. **Creates** `process/archive/R-YYYYMMDD.md` (using the release date or ID).
2. **Moves** to the archive file:
   - All completed stories and their JIT task tables.
   - All closed CCR entries (APPROVED/REJECTED).
   - All resolved Issues (CLOSED).
   - All Decisions related to shipped stories.
   - All Evidence log entries for the shipped release.
   - The release notes block for this release.
3. **In PROGRESS.md:**
   - Removes the archived rows from each table.
   - Resets "Current story" and "Current task" to [NONE].
   - Resets phase tracker for the new version.
4. **Registers** the archive file in PROGRESS.md > S11 (Artifacts added).

#### What you get and where it goes

| Output | Target location |
|--------|----------------|
| Release archive | `process/archive/R-YYYYMMDD.md` (permanent, read-only) |
| Clean PROGRESS.md | `process/PROGRESS.md` (all trackers reset) |
| Archive registration | `process/PROGRESS.md` > **S11. Artifacts added** |

---

## Version Loop (MVP -> V1.1 -> V2 ...)

When you are ready for the next version:

1. **Add new stories** to `product/PRD.md` > S4 (tag them for the new version in S6 Roadmap).
2. **Update** `process/PROGRESS.md` > S0: set the new version label and reset gate statuses (G0-G5 = PENDING).
3. **Decide:** Does the new version need architecture or contract changes?
   - **If yes:** Run `/plan` to scope the new version. ARCH and contracts unlock as drafts during P1-P4 again. Iterate with `/explore` and `/advise`.
   - **If no:** Proceed directly to `/next` to start building new stories.
4. The full lifecycle repeats: Phase A -> Phase B -> Phase C -> archive -> next version.

Do **not** rename existing story IDs from previous versions. Previous S-V### IDs live in the archive. New stories get the next sequential IDs.

---

## Emergency Procedures

### If the agent stops following the process

Paste this exact prompt in the IDE chat:

```
Stop. Re-read process/PROCESS_REFERENCE.md and process/PROGRESS.md. Resume in Process Steward mode. Use the response protocol appropriate for the current phase (see PROCESS_REFERENCE § Lightweight mode). Do not modify approval-controlled files without explicit approval.
```

### If the agent hallucinates features not in the PRD

1. Type "STOP" in the IDE chat.
2. Check `product/PRD.md` > S4 -- is the feature in a story?
3. If not, tell the agent: "This feature is not in the PRD. Revert and return to the current task."

### If the agent modifies ARCH/contracts during build without CCR

1. Type "STOP" in the IDE chat.
2. Check `git diff product/ARCH.md product/contracts/` to see what changed.
3. Tell the agent: "You modified approval-controlled files without a CCR. Revert those changes and raise a CCR if the change is needed."

### If PROGRESS.md is corrupted or inconsistent

1. Check `git log process/PROGRESS.md` to find the last good state.
2. Restore: `git checkout <commit> -- process/PROGRESS.md`
3. Tell the agent: "PROGRESS.md has been restored to [commit]. Re-read it and resume."

---

## Quick Reference: All Commands by Phase

### Phase A: Collaborative Design (P1-P4)

| Step | You type | What happens | Key output |
|------|----------|-------------|------------|
| 1 | `/plan` | Agent drafts story backlog | PRD.md S4 stories |
| 2 | `/explore [question]` | Agent researches (read-only) | Chat summary, optional I-### |
| 3 | `/advise [decision]` | Agent presents options, you choose | PROGRESS D-###, optional ARCH/contract updates |
| 4 | `/plan` (continue) | Agent drafts ARCH + contracts | ARCH.md, contracts/* |
| 5 | "Approved" | Gates G1 + G2 recorded, ARCH/contracts lock | PROGRESS G1, G2 |

### Phase B: Disciplined Build (P5-P7)

| Step | You type | What happens | Key output |
|------|----------|-------------|------------|
| 6 | `/next` | Agent decomposes next story into tasks | PROGRESS S6 task list |
| 6 (if HIGH) | "Approve T-V###.##" | Agent proceeds with HIGH-risk task | Task unblocked |
| 7 | `/next` (repeat) | Agent implements one task per invocation | Code + tests + evidence |
| 7a | "APPROVE/REJECT/DEFER CCR-###" | Resolve contract drift escalation | Contracts updated or task blocked |
| 7b | `/archive` | Sweep completed logs | Lean PROGRESS.md |
| 8 | "PASS" or "FAIL + notes" | Accept or reject story | Story DONE + G3 evidence |

### Phase C: Release & Iterate (P8-P12)

| Step | You type | What happens | Key output |
|------|----------|-------------|------------|
| 9 | `/release` | Agent runs global verification, drafts release notes | G4 evidence, release notes |
| 10 | "DEPLOYED_OK" or "FAIL + logs" | Confirm deployment result | G5 evidence |
| 11 | `/explore` + `/advise` | Retrospective and next-version planning | PRD roadmap updated |
| 12 | `/archive` | Full version archive | process/archive/R-*.md |
