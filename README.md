# Human Operator Guide (Quickstart + Playbook) — Antigravity Process Steward (Stories-first)

This guide explains how to run the **Stories-first, doc-driven** workflow where the **Agent** acts as a *Process Steward* and the **Human** stays in control of scope, acceptance, and architecture.

**Canonical process spec (agent must read first each session):** `process/PROCESS_REFERENCE.md`

---

## 1) Mental model

- **Story = the bridge** between Human intent and Agent execution.
  - Human defines **value + acceptance**.
  - Agent plans and executes **tasks** to satisfy acceptance.
- **Docs are the control surface** (the agent’s “memory” lives in the repo):
  - `product/PRD.md` = **what** to build (stories, acceptance, ordering)
  - `product/ARCH.md` = **how** to build (static rules; approval-controlled)
  - `product/contracts/*` = **interfaces** (schemas/contracts; RO during build unless CCR)
  - `process/PROGRESS.md` = **state + evidence** (single source of truth)
- **Deterministic verifier:** `make check` is the Definition-of-Done gate for tasks/stories.

---

## 2) Roles and responsibilities

### Human (owner of intent)
You control:
- **Vision + priorities** (what matters now)
- **Story acceptance criteria** (what “Done” means)
- **Approval-controlled truths:** scope, acceptance, architecture, contracts
- **CCR decisions** (contract changes)
- **Deployment action** (if applicable)

### Agent (owner of execution)
The agent owns:
- Proposing drafts for PRD/ARCH/contracts (when asked)
- Creating JIT task plans per story
- Implementing code + tests
- Running `make check` and logging evidence
- Maintaining `process/PROGRESS.md` as a reliable state database

**Rule of thumb:**
- Human edits **product truth**; Agent edits **process state**.
- Agent may *draft* product truth, but Human must explicitly approve before it becomes binding.

---

## 3) Two-phase operating mode (recommended)

### Phase A — Design (functional + technical)
Goal: converge on a stable **Story backlog** + minimal architecture/contracts so implementation can run smoothly.

Phase A typically starts with `/explore` (investigate unfamiliar areas) and `/advise` (get structured recommendations on key decisions), then moves to `/seed` (validate workspace) and `/plan` (draft stories + architecture).

You can run Phase A:
- **A1: Human-led** (you write PRD/ARCH; agent reviews), or
- **A2: Agent-augmented** (you provide vision; agent drafts; you approve).

### Phase B — Implementation (story-by-story)
Goal: the Agent implements each story as a vertical slice, with tests and evidence, until release.

**Important:** in Phase B, only the Agent writes code. The Human validates acceptance and makes CCR/approval decisions.

---

## 4) How to run Phase A (Design)

### A1) Human-led design (minimal agent help)
1. Edit `product/PRD.md`:
   - Fill **Vision**
   - Add a small backlog of **stories** (S-V###) with acceptance criteria
   - Keep stories as **vertical slices deliverable in <= 1 day**
   - (Optional) add UC tags in the story headers, e.g. `Tags: UC:AUTH`
2. Edit `product/ARCH.md` (optional early on):
   - Set basic constraints, repo conventions, and boundaries
3. (Optional) edit `product/contracts/*`:
   - Keep it minimal at first (schemas, basic endpoints)
4. (Optional) Use `/explore` to investigate unfamiliar areas or `/advise` for key architectural decisions before proceeding.
5. Start Antigravity agent in Process Steward mode:

**Prompt:**
> You are Process Steward. Read `process/PROCESS_REFERENCE.md` and `process/PROGRESS.md`. Use `/explore` for any areas I should investigate, and `/advise` for key decisions. Then validate prerequisites with `/seed` and review `product/PRD.md` — propose improvements (story sizing, acceptance clarity, ordering), without implementing code yet.


### A2) Agent-augmented design (vision-only from Human)
Use this if you want the agent to draft most initial content.

1. Put only your **vision + boundaries** in `product/PRD.md` (keep it short).
2. Start agent in Process Steward mode.

**Prompt:**
> Process Steward mode. I only provided the vision in `product/PRD.md`. Start with `/explore` for any unfamiliar areas, then `/advise` for key architectural decisions. Run `/seed`, then `/plan`. Draft a stories-first PRD backlog (S-V###) with <= 1-day vertical slices and clear acceptance criteria. Draft minimal `product/ARCH.md` and baseline `product/contracts/*`. Propose changes and ask me to approve story-level scope and critical tradeoffs.

3. You approve in batches:
   - Approve stories + acceptance (PRD)
   - Approve key architecture choices (ARCH)
   - Approve contract semantics (contracts)

**Approval tip:** you do *not* review every line of code-like contract files; review semantics: naming, required fields, error model, and key endpoints.

---

## 5) How to run Phase B (Implementation)

### Operating loop (what you do each session)
1. Tell the agent to run `/next` (to implement) or `/check` (to validate).
2. Only intervene when the agent asks (high-risk tasks, CCR, acceptance handshake).

**Session starter prompt:**
> Process Steward mode. Execute `/next`. Follow READ/DECIDE/ACT/VERIFY/UPDATE/ASK. Implement only what is in `product/PRD.md`. Record evidence in `process/PROGRESS.md`. Use `/advise` if architectural questions arise. (Run `/check` to validate independently when needed).

### Story sizing policy
- Stories must be **vertical slices deliverable in <= 1 day**.
- If a story grows beyond that, split it into two stories and ask for approval.

### What the agent will do (internally)
For each story in PRD sequence:
1. Create a **JIT task checklist** (5–15 tasks) in `process/PROGRESS.md`.
2. Ask you to approve **only HIGH-risk tasks** (per policy).
3. For each task:
   - implement minimally + tests
   - run `make check`
   - log evidence in PROGRESS
4. Ask you for **acceptance validation** when the story is done.

### Your acceptance handshake
When the agent asks you to validate a story:
- Respond **PASS** or **FAIL + notes**.
- If FAIL, give the smallest reproducible issue list.

Example:
- PASS: “PASS. Login works with correct creds; 401 on wrong creds; tests green.”
- FAIL: “FAIL. Missing lockout after 5 attempts; also error body missing `code` field.”

---

## 6) CCR (Contract Change Request) — how to handle

A CCR happens when implementation reveals a mismatch in contracts (`product/contracts/*`) or an interface change is needed.

### What the agent must do
- **STOP** and log `CCR-###` in `process/PROGRESS.md` with:
  - failing evidence
  - minimal change proposal
  - impact

### What you must do
Reply with one of:
- **APPROVE CCR-###** (and optionally constraints: “approved but keep field optional”)
- **REJECT CCR-###** (and state alternative)
- **DEFER CCR-###** (mark blocked; revisit later)

**Rule:** No workarounds that bypass contracts. Either approve the contract change or re-scope.

---

## 7) Release / post-story hardening

When all stories for the version are DONE:

**Prompt:**
> Process Steward mode. Execute `/release`. Ensure `make check` is green, draft release notes in `process/PROGRESS.md`, and ask me for any required manual sign-off and deployment steps.

You (Human) decide if you require:
- manual E2E run
- staging/prod deploy
- smoke tests

---

## 8) Post-MVP versions (how the workflow scales)

For a new version (V1.1, V2, …):
1. Archive the previous release: move shipped stories, evidence, and CCRs from `process/PROGRESS.md` to `process/archive/R-YYYYMMDD.md` (see PROCESS_REFERENCE § PROGRESS archiving).
2. Add new stories to `product/PRD.md` (tag them for the new version in the roadmap section).
3. In `process/PROGRESS.md`, update the **current version label** and reset milestone statuses for the new iteration.
4. Run `/plan` if architecture/contracts need changes; otherwise proceed with `/next`.

**Do not rename existing story IDs.** Instead, update the roadmap/version mapping.

---

## 9) Command reference (FastAPI + uv)

- `make check` — runs lint/format/typecheck/contractcheck/tests
- `make run` — starts dev server (`uv run fastapi dev`)
- `make sync` — `uv sync`

If you need an explicit uvicorn command:
- `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`

---

## 10) If the agent stops following the process

Use a hard reset prompt:

> Stop. Re-read `process/PROCESS_REFERENCE.md` and `process/PROGRESS.md`. Resume in Process Steward mode. Use the response protocol appropriate for the current phase (see PROCESS_REFERENCE § Lightweight mode). Do not modify approval-controlled files without explicit approval.

