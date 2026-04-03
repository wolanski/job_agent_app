# PROGRESS (Dashboard + Trackers + Evidence + CCR Log)
> **Dynamic truth**: this file changes frequently.
> Reference: `process/diagrams/PROCESS_MAIN.puml`, `process/diagrams/STATE_MODEL.puml`, and `process/diagrams/PROCESS_STEWARD_SEQUENCE.puml`.
> Human guide: see `README.md` (repo root).
> Archives: `process/archive/` (shipped releases; see PROCESS_REFERENCE § PROGRESS archiving)

## 0. Current status
- Current version: [NONE]
- Current release: [NONE]
- Current phase: P0
- Current story: [NONE]
- Current task: [NONE]

## 1. Policy (how the agent is allowed to operate)
- Approval level: STORY (human approves story set and acceptance; tasks JIT)
- High-risk review: human reviews HIGH-risk tasks only
- Reorder: agent may reorder LOW-risk tasks within a story if dependencies allow
- Contracts: **RO during build** unless CCR approved
- ARCH: **RO during build** unless explicit decision at a gate
- Definition of "Done": see `process/PROCESS_REFERENCE.md` § Definition of Done

## 2. Gates (Milestones)
| Gate | Phase | Meaning | Status | Evidence |
|---|---|---|---|---|
| G0 | P0 | Installed (artifacts exist + check runnable) | PENDING | |
| G1 | P1 | Scope approved (PRD accepted) | PENDING | |
| G2 | P4 | Ready-to-build (contracts validate + check green) | PENDING | |
| G3 | P7 | Story done (repeats per story) | PENDING | |
| G4 | P10 | Release candidate (hardening complete) | PENDING | |
| G5 | P11 | Released (deployed + smoke + notes) | PENDING | |

## 3. Phase tracker (P0..P12)
| Phase | Name | Status | Notes |
|---|---|---|---|
| P0 | Install and Wire | PENDING | |
| P1 | Functional Framing | PENDING | |
| P2 | Architecture (Lite) | PENDING | |
| P3 | Contract Baseline | PENDING | |
| P4 | Story Baseline | PENDING | |
| P5 | JIT Planning | PENDING | |
| P6 | Iterative Implementation | PENDING | |
| P7 | Story Handshake | PENDING | |
| P8 | Integration Testing | PENDING | |
| P9 | E2E Automation | PENDING | |
| P10 | Manual E2E (optional) | PENDING | |
| P11 | Deploy | PENDING | |
| P12 | Post-release Feedback | PENDING | |

## 4. Optional UC tag glossary (lightweight)
> UC tags are optional labels used only to group stories. Keep this table tiny or leave it empty.

| UC tag | Meaning | Notes |
|---|---|---|

## 5. Story tracker (authoritative operational list)
| Story ID | Title | UC tags (optional) | Risk | Status | Evidence |
|---|---|---|---:|---|---|

## 6. Current story JIT tasks (rewrite this section per story)
### Story: [NONE]
| Task ID | Title | Risk | Status | Evidence |
|---|---|---:|---|---|

## 7. CCR log (Contract Change Requests)
> Raised when product/contracts/spec must change. Rule: **STOP** and ask; no workaround.
| CCR ID | Date | Related task | Summary | Decision | Evidence |
|---|---|---|---|---|---|

## 8. Issues log
| ID | Date | Type | Summary | Status | Link |
|---|---|---|---|---|---|

## 9. Decisions log
| ID | Date | Decision | Rationale | Impact |
|---|---|---|---|---|

## 10. Evidence log (checks and artifacts)
| Date | What ran | Result | Where |
|---|---|---|---|

## 11. Artifacts added (append)
| Date | Artifact | Type | Purpose | Link |
|---|---|---|---|---|

## 12. Release notes (append per release)
