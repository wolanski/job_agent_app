# PROGRESS (Dashboard + Trackers + Evidence + CCR Log)
> **Dynamic truth**: this file changes frequently.
> Reference: `process/diagrams/PROCESS_MAIN.puml`, `process/diagrams/STATE_MODEL.puml`, and `process/diagrams/PROCESS_STEWARD_SEQUENCE.puml`.
> Human guide: see `README.md` (repo root).

## 0. Current status
- Current version: [MVP]
- Current release: [R-YYYYMMDD-01]
- Current phase: [P0..P12]
- Current story: [S-V001 or NONE]
- Current task: [T-... or NONE]

## 1. Policy (how the agent is allowed to operate)
- Approval level: STORY (human approves story set and acceptance; tasks JIT)
- High-risk review: human reviews HIGH-risk tasks only
- Reorder: agent may reorder LOW-risk tasks within a story if dependencies allow
- Contracts: **RO during build** unless CCR approved
- ARCH: **RO during build** unless explicit decision at a gate
- Definition of "Done": see `process/PROCESS_REFERENCE.md` § Definition of Done

## 2. Gates (Milestones)
| Gate | Meaning | Status | Evidence |
|---|---|---|---|
| G0 | Installed (artifacts exist + check runnable) | PENDING | |
| G1 | Scope approved (PRD accepted) | PENDING | |
| G2 | Ready-to-build (contracts validate + check green) | PENDING | |
| G3 | Story done (repeats per story) | PENDING | |
| G4 | Release candidate (hardening complete) | PENDING | |
| G5 | Released (deployed + smoke + notes) | PENDING | |

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
| UC:AUTH | Authentication/session | |
| UC:... | ... | |

## 5. Story tracker (authoritative operational list)
| Story ID | Title | UC tags (optional) | Risk | Status | Evidence |
|---|---|---|---:|---|---|
| S-V001 | ... | UC:AUTH | MED | TODO | |
| S-V002 | ... | | LOW | TODO | |

## 6. Current story JIT tasks (rewrite this section per story)
### Story: S-V001
| Task ID | Title | Risk | Status | Evidence |
|---|---|---:|---|---|
| T-V001.01 | ... | LOW | PLANNED | |
| T-V001.02 | ... | MED | PLANNED | |

## 7. CCR log (Contract Change Requests)
> Raised when product/contracts/spec must change. Rule: **STOP** and ask; no workaround.
| CCR ID | Date | Related task | Summary | Decision | Evidence |
|---|---|---|---|---|---|
| CCR-001 | YYYY-MM-DD | T-V001.02 | ... | PENDING | link/log |

## 8. Issues log
| ID | Date | Type | Summary | Status | Link |
|---|---|---|---|---|---|
| I-001 | 2026-04-03 | Question | Persistence/database strategy not yet decided. Use `/advise` to explore options (SQLite, PostgreSQL, etc.) before P5. | OPEN | product/PRD.md § Open questions |

## 9. Decisions log
| ID | Date | Decision | Rationale | Impact |
|---|---|---|---|---|
| D-001 | 2026-04-03 | Adopted two-phase model (Collaborative Design + Disciplined Build); added /advise workflow | ML/Architect user benefits from exploratory design before committing to frozen-ARCH build. Reduces ceremony in P0–P4, preserves rigor in P5+. | README, help, SKILL.md, PROCESS_REFERENCE, rules/process-steward updated; advise.md created |
| D-002 | 2026-04-03 | Added contract conformance test; fixed health endpoint contract mismatch; updated root README for /explore and /advise; flagged persistence as I-001 | Review identified runtime contract gap, missing /explore+/advise in human guide, stale references, and no persistence guidance. | main.py, test_health.py, test_contract_conformance.py, schemas.py, Makefile, README.md, PROCESS_REFERENCE.md, PRD.md, PROGRESS.md, SKILL.md, check/SKILL.md, plan.md updated |

## 10. Evidence log (checks and artifacts)
| Date | What ran | Result | Where |
|---|---|---|---|
| YYYY-MM-DD | check | PASS | CI link or console output |

## 11. Artifacts added (append)
| Date | Artifact | Type | Purpose | Link |
|---|---|---|---|---|
| YYYY-MM-DD | ... | doc/diagram/contract | ... | relative path |

## 12. Release notes (append per release)
### Release R-YYYYMMDD-01
- Scope shipped:
  - Stories: S-V001, S-V002
- Known issues:
  - ...
- How to verify:
  - ...
- Rollback notes:
  - ...
