# PRD (Stories-First, Lean)

## 0. Metadata
- **Product:** [App Name]
- **Owner (Human):** [Name]
- **Current Version:** [e.g., MVP]
- **Last Updated:** [UTC timestamp]

---

## 1. Vision
**One-liner**
- [What is this app?]

**Primary user**
- [Who uses it?]

**Problem statement**
- [What pain does it solve?]

**Non-goals (explicitly out-of-scope for this version)**
- [Non-goal 1]
- [Non-goal 2]

---
## 2. Scope boundaries
**In-scope (this version)**
- [In-scope item 1]
- [In-scope item 2]

**Out-of-scope (this version)**
- [Out-of-scope item 1]
- [Out-of-scope item 2]

**Constraints**
- [Time/budget/platform constraints]
- [Security/privacy constraints]

---

## 3. Requirements (optional)
> Keep this section small. In this process, **Stories + Acceptance Criteria** are the primary scope control.

### Functional requirements (FR)
- FR-001: [Requirement]

### Non-functional requirements (NFR)
- NFR-001: [Performance/Security/Reliability requirement]

---
## 4. Story Backlog (authoritative)

### Story principles
- A **Story** is the boundary between Human intent and Agent implementation.
- Stories must be **vertical slices deliverable in ≤ 1 day** (for a single agent session/day).
- If a story is too large: split it.
- The Agent may create **Tasks** (JIT) in `process/PROGRESS.md`, but the Human approves stories.
- Optional **UC tags** can group stories, but they are only labels (no separate use-case hierarchy).

### ID conventions
- Stories: `S-V001`, `S-V002`, ... (V = current version; keep sequential)
- Tasks (JIT per story): `T-V001.01`, `T-V001.02`, ...

### Story index (plan)
| Story ID | Title | UC tags (optional) | Notes |
|---|---|---|---|
| S-V001 | ... | UC:AUTH | |
| S-V002 | ... | | |

---

### Story template

#### S-V### — [Story title]
- **UC tags (optional):** [UC:...]
- **Summary:** [1–3 sentences]
- **Acceptance criteria:**
  - AC-01: [Given/When/Then or checklist]
  - AC-02: ...
- **Out of scope:**
  - [Explicitly excluded behaviors]
- **Dependencies (optional):**
  - [Other stories, external systems]
- **Notes / assumptions:**
  - [Anything the Agent must not guess]

---
## 5. Optional UC tags (lightweight grouping)

UC tags are **optional labels** used only to group related stories.
- They are **not** separate objects that require decomposition.
- If you don't need grouping, leave this section empty.

| UC tag | Meaning | Notes |
|---|---|---|
| UC:AUTH | Authentication/session | |
| UC:... | ... | |

---

## 6. Roadmap (versions → stories)

| Version | Target stories (IDs) | Notes |
|---|---|---|
| MVP | S-V001, S-V002 | |
| V1.1 | S-V003, ... | |

---

## 7. Open questions (optional)
> Canonical Qs should be tracked in `process/PROGRESS.md` as Issues (`I-###`).
- [Question]

---

## Traceability Log
| Timestamp (UTC) | Actor | Change | Why |
|---|---|---|---|
| 2026-02-08T12:00:00Z | Seed (generator) | Initial PRD template | Provide a minimal scope truth file for the process. |
| 2026-02-08T15:52:05Z | Seed (generator) | Aligned PRD IDs with process gates and FastAPI+uv assumptions | Keep templates consistent with starter pack wiring. |
| 2026-02-08T17:32:05Z | Seed (generator) | Reorganized repo folders (product vs process) | Clarify what belongs to product truth vs process truth. |
| 2026-02-08T18:18:12Z | Seed (generator) | Converted PRD to stories-first with optional UC tags | Reduce bureaucracy; keep Stories as the Human–Agent handshake boundary. |
