# Architect's Ideation Process -- Step-by-Step Manual

> Companion guide for `product/diagrams/IDEATION_PROCESS_v2.puml`.
> Complete this process **before** running `/seed` to hand off to the coding agent.

---

## Overview

The Ideation Process is a **solo, pre-agent design workflow** organized into three hierarchical phases that progressively narrow from abstract problem space to concrete, buildable artifacts. Each step uses proven design frameworks to extract specific insights, and every output maps to an exact location in the repository.

```
H1: WHAT & WHY (Problem Space)        H1.1-H1.3     -> PRD.md S1-S2
H2: LOGICAL DESIGN (Decomposition)    H2.1-H2.3b    -> PRD.md S3-S5, product/diagrams/
H3: PHYSICAL DESIGN (Architecture)    H3.1-H3.3c    -> ARCH.md S1-S7, product/contracts/
HANDOFF (Distillation)                HO.1-HO.2     -> Consistency check, /seed
```

**Who does this?** You (the architect / human operator), working alone or with stakeholders. The coding agent is not involved yet.

**When is it done?** When all consistency checks in HO.1 pass, and you run `/seed` (HO.2) to activate the coding agent at Gate G0.

---

## Output Target Reference

| File | Sections filled by this process |
|------|------|
| `product/PRD.md` | S0 (Metadata), S1 (Vision), S2 (Scope), S3 (Requirements), S4 (Story Backlog), S5 (UC Tags), S6 (Roadmap) |
| `product/ARCH.md` | S0 (Metadata), S1 (Constraints), S2 (Tech Stack), S3 (Repo Map), S4 (Architecture C4-lite), S5 (Conventions), S6 (Extension Points), S7 (Security) |
| `product/contracts/schemas.py` | Pydantic models (DTOs) |
| `product/contracts/openapi.yaml` | OpenAPI 3.x specification |
| `product/contracts/CONTRACTS.md` | Naming conventions, error model, invariants, compatibility policy |
| `product/diagrams/` | Visual artifacts (use-case diagrams, ERDs, C4 diagrams, wireframes, etc.) |

---

## H1: WHAT & WHY (Problem Space)

**Goal:** Establish the foundational constraints -- what you are building, for whom, and why it matters. Everything downstream derives from these three steps. They are **sequential** because each step depends on the previous one.

---

### H1.1: Vision & Value

**Purpose:** Define the business model, value proposition, and market fit. This is the single most important step -- an ambiguous vision cascades into endless drift during implementation. The narrower and more explicit your vision, the faster and more stable the build will be.

#### Frameworks & Tools

**Lean Canvas** (Ash Maurya)
- **What it is:** A one-page business model template with 9 blocks: Problem, Customer Segments, Unique Value Proposition, Solution, Channels, Revenue Streams, Cost Structure, Key Metrics, Unfair Advantage.
- **Why use it:** Forces you to articulate the core problem and solution in under 20 minutes. Prevents over-engineering by making you commit to what matters *most*. Explicitly separates the problem from the solution.
- **How to use it:**
  1. Start with the **Problem** block -- list the top 1-3 problems your users face.
  2. Fill **Customer Segments** -- who has these problems? Be specific (e.g., "Nordic recruiters managing 50+ job postings across 3 country boards" not "recruiters").
  3. Fill **Unique Value Proposition** -- one sentence that explains why your solution is different and worth paying attention to.
  4. Fill the remaining blocks. Spend no more than 30 minutes total.
- **What insight it brings:** Clarifies whether you are solving a real problem for a real audience. Exposes assumptions early ("Do we actually know recruiters need cross-country aggregation?").

**Business Model Canvas** (Osterwalder)
- **What it is:** A broader, more strategic version of Lean Canvas with 9 blocks focused on value delivery: Key Partners, Key Activities, Key Resources, Value Propositions, Customer Relationships, Channels, Customer Segments, Cost Structure, Revenue Streams.
- **Why use it:** Better for established products or when you need to model partnerships and operational logistics. Use it *instead of* Lean Canvas if the product has complex stakeholder relationships.
- **How to use it:** Same process as Lean Canvas but spend more time on Key Partners (who do you depend on -- e.g., job board APIs?) and Key Resources (what infrastructure do you need?).

**Wardley Mapping** (Simon Wardley)
- **What it is:** A value-chain map that positions components on two axes: *visibility to user* (vertical) and *evolution stage* (horizontal, from Genesis to Commodity).
- **Why use it:** Reveals which components are strategic differentiators vs. commodity infrastructure. Prevents you from building what you should buy and from buying what you should build.
- **How to use it:**
  1. Start with the **user need** at the top of the map.
  2. List every component needed to serve that need (e.g., job data API, search index, auth layer, hosting).
  3. Place each component on the evolution axis: Genesis (novel, uncertain) -> Custom-Built -> Product -> Commodity.
  4. Draw dependency lines (e.g., "Search" depends on "Data Store" depends on "Cloud Compute").
  5. Look for components in the "Custom-Built" zone that could be commodities (build vs. buy decision).
- **What insight it brings:** Identifies where your competitive advantage actually lives. For a job engine, search relevance might be Genesis/Custom-Built (strategic), while hosting is Commodity (use a platform).

#### How to do it

1. Fill out a Lean Canvas (or Business Model Canvas) for your product idea. Keep it to a single page.
2. Optionally create a Wardley Map to visualize your value chain and identify build-vs-buy boundaries.
3. Distill the canvas into a **one-liner vision statement** that answers: "What is this app, for whom, solving what problem?"

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| One-liner vision statement | `product/PRD.md` > **S1. Vision** > **One-liner** |
| Primary user description | `product/PRD.md` > **S1. Vision** > **Primary user** |
| Problem statement (from Lean Canvas "Problem" block) | `product/PRD.md` > **S1. Vision** > **Problem statement** |
| Non-goals (from the Lean Canvas "not this" boundaries) | `product/PRD.md` > **S1. Vision** > **Non-goals** |
| Lean Canvas PDF (optional, for reference) | `product/docs/lean_canvas.pdf` |
| Wardley Map image (optional, for reference) | `product/docs/wardley_map.png` |

**Example PRD.md S1 output:**
```markdown
## 1. Vision
**One-liner**
- A job-posting ingestion and search engine that aggregates Nordic public employment board listings into a single normalized, searchable API.

**Primary user**
- Recruitment platforms and HR tech integrators who need a unified feed of job postings across SE, NO, FI, DK.

**Problem statement**
- Nordic job boards (Arbetsformedlingen, NAV, TE-palvelut, Jobnet) each have different APIs, schemas, and update cadences. Integrators must build and maintain 4+ separate connectors.

**Non-goals (explicitly out-of-scope for this version)**
- No user-facing frontend (API only for MVP)
- No resume/candidate matching
- No job board write-back (posting jobs)
```

---

### H1.2: Actors & Personas

**Purpose:** Identify every actor that will interact with the system -- human users, admin roles, external APIs, background processes. This step creates the trust boundary map that drives both security design (H3.3c) and story decomposition (H2.2).

#### Frameworks & Tools

**User Personas** (Alan Cooper)
- **What it is:** Fictional, archetypal profiles of your key user types. Each persona has a name, role, goals, frustrations, and tech comfort level.
- **Why use it:** Prevents designing for an abstract "user." Forces you to think about *specific* people with *specific* goals. Different personas lead to different stories and different UI priorities.
- **How to use it:**
  1. For each user type, write a 3-5 sentence profile: name, role, primary goal, key frustration, tech skill level.
  2. Limit yourself to 2-4 personas maximum for an MVP. More than 4 means your scope is too wide.
  3. Mark one persona as the **primary** -- this is who you optimize for when tradeoffs arise.
- **What insight it brings:** Clarifies priority. If your primary persona is an API integrator (developer), you optimize for clean docs and predictable schemas, not a dashboard UI.

**Actor-Goal Lists** (UML)
- **What it is:** A simple table listing every actor (human or system) alongside their primary goals. Actors can be "primary" (directly trigger use cases) or "supporting" (provide data or services).
- **Why use it:** Catches actors that personas miss -- especially system-to-system actors (cron jobs, external APIs, webhook receivers). These non-human actors generate some of the most important stories.
- **How to use it:**
  1. List every entity that sends data to or receives data from your system.
  2. For each actor, write 1-3 goals (what they want to achieve through the system).
  3. Mark actors as "primary" (human initiators), "supporting" (external systems), or "offstage" (regulatory/compliance actors).
- **What insight it brings:** Surfaces integration boundaries. For a job engine, you discover actors like "Ingestion Pipeline" (automated), "Search API Consumer" (developer), and "Admin" (human) -- each with different auth requirements.

**C4 Context Diagram** -- Level 1 (Simon Brown)
- **What it is:** The highest-level C4 diagram. Shows your system as a single box in the center, with all external actors (people and systems) around it, connected by labeled arrows showing data flow.
- **Why use it:** Creates a shared visual understanding of system boundaries. Makes trust boundaries explicit -- every arrow crossing the system boundary is a potential security concern.
- **How to use it:**
  1. Draw your system as a single box in the center.
  2. Place every actor from your Actor-Goal List around it.
  3. Draw arrows labeled with what data flows (e.g., "Job postings (JSON)" from "Arbetsformedlingen API" to "Job Engine").
  4. Draw arrows for outbound flows (e.g., "Search results" from "Job Engine" to "API Consumer").
  5. Mark trust boundaries (dashed lines separating internal from external).
- **What insight it brings:** Makes integration complexity visible. If you have 4 external job board APIs feeding in and 2 types of consumers pulling out, that is visible at a glance. The trust boundary tells you where auth is needed.

#### How to do it

1. Write 2-4 persona profiles for your human users. Mark one as primary.
2. Create an Actor-Goal list that includes both human and system actors.
3. Draw a C4 Context diagram showing your system, all actors, and data flows. Mark trust boundaries.

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| Persona profiles (name, role, goals, frustrations) | `product/PRD.md` > **S1. Vision** > append under **Primary user** (or create a Personas subsection) |
| Actor-Goal list (actor, type, goals) | `product/PRD.md` > **S1. Vision** > append as Actor-Goal table |
| Trust boundary identification | `product/ARCH.md` > **S4. Architecture snapshot** > **Trust boundaries** |
| C4 Context diagram image | `product/diagrams/c4_context.drawio` or `.puml` |

**Example Actor-Goal list:**
```markdown
| Actor | Type | Goals |
|-------|------|-------|
| API Integrator | Primary (human) | Search/filter jobs via REST API; get stable pagination |
| Ingestion Pipeline | Supporting (system) | Push batches of job postings from source APIs |
| Admin Operator | Primary (human) | Monitor ingestion health; trigger re-ingestion |
| Arbetsformedlingen API | Supporting (external) | Provide SE job listings |
| NAV API | Supporting (external) | Provide NO job listings |
```

---

### H1.3: Scope Boundaries

**Purpose:** Draw a hard line between what is in this version and what is deferred. This is the constraint that prevents scope creep during build. Everything the coding agent builds must fall within these boundaries.

#### Frameworks & Tools

**MoSCoW Prioritization** (Dai Clegg)
- **What it is:** A prioritization scheme that categorizes every requirement or feature into: **Must have** (MVP-critical, non-negotiable), **Should have** (important but not blocking), **Could have** (nice-to-have), **Won't have** (explicitly out-of-scope for this version).
- **Why use it:** Creates an unambiguous priority ordering. During build, when something is harder than expected, you know exactly what to cut (Could/Won't) and what to protect (Must). Prevents the "everything is priority 1" anti-pattern.
- **How to use it:**
  1. List all candidate features/capabilities from H1.1-H1.2.
  2. For each, ask: "If we launched without this, would the product be useless?" If yes -> Must. If no -> Should/Could/Won't.
  3. Aim for: ~60% Must, ~20% Should, ~10% Could, ~10% Won't.
  4. The Must items become your in-scope list. The Won't items become your explicit out-of-scope list.
- **What insight it brings:** Forces binary decisions. "Full-text search" might be Must, while "faceted search by salary range" might be Could. This distinction shapes story sizing and architecture (you might not need Elasticsearch for basic text search).

**Kano Model** (Noriaki Kano)
- **What it is:** Classifies features by user satisfaction impact into: **Basic** (expected, absence causes dissatisfaction), **Performance** (more is better, linear satisfaction), **Excitement** (unexpected delight).
- **Why use it:** Reveals which features are hygiene factors (must work or users leave) vs. differentiators (create competitive advantage). Helps you invest effort where it creates the most user value.
- **How to use it:**
  1. For each candidate feature, ask two questions: "How do you feel if this feature is present?" and "How do you feel if this feature is absent?"
  2. Map responses to Kano categories: Basic (absence = angry, presence = neutral), Performance (scales linearly), Excitement (absence = neutral, presence = delighted).
  3. All Basic features are Must-haves. Excitement features are candidates for differentiation stories.
- **What insight it brings:** "Returning search results" is Basic (users expect it). "Cursor-based pagination" is Performance (better than offset). "Real-time webhook on new matching jobs" is Excitement (delight, but defer to V2).

**TOGAF Architecture Vision** (The Open Group)
- **What it is:** A structured approach to defining the architecture vision that constrains what is architecturally feasible within the given time, budget, and team constraints.
- **Why use it:** Grounds scope decisions in reality. A feature might be "Must have" from a business perspective but architecturally infeasible for an MVP (e.g., real-time streaming requires infrastructure you don't have).
- **How to use it:**
  1. List your hard constraints: time (e.g., 2 weeks to MVP), budget (e.g., $0 infrastructure for dev), team (e.g., 1 developer + AI agent), platform (e.g., Python/FastAPI mandated).
  2. For each Must-have feature, verify it is achievable within these constraints.
  3. Downgrade any infeasible Must-haves to Should/Could, and document why.
- **What insight it brings:** Prevents committing to scope that cannot be delivered. If you have 2 weeks and one developer, "multi-tenant auth with OAuth2" might need to be deferred even if it is logically a Must.

#### How to do it

1. List all candidate features from H1.1-H1.2.
2. Apply MoSCoW to categorize them. Optionally use Kano to validate the prioritization.
3. Verify Must-haves against your constraints (TOGAF lens: time, budget, team, platform).
4. Write the definitive in-scope and out-of-scope lists.

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| In-scope items (Must + selected Should) | `product/PRD.md` > **S2. Scope boundaries** > **In-scope** |
| Out-of-scope items (Won't + deferred Could/Should) | `product/PRD.md` > **S2. Scope boundaries** > **Out-of-scope** |
| Constraints (time, budget, platform, team) | `product/PRD.md` > **S2. Scope boundaries** > **Constraints** |
| Same constraints mirrored to ARCH | `product/ARCH.md` > **S1. Constraints and principles** |
| MoSCoW classification table (optional, for reference) | `product/docs/scope_matrix.md` |

**Example PRD.md S2 output:**
```markdown
## 2. Scope boundaries
**In-scope (this version)**
- Batch ingestion endpoint for job postings (POST /ingest/jobs)
- Search/list endpoint with text query and country filter (GET /jobs)
- Cursor-based pagination
- Health check endpoint
- Contract conformance tests (schemas.py matches openapi.yaml)

**Out-of-scope (this version)**
- User-facing frontend / dashboard
- Real-time webhook notifications
- Resume / candidate matching
- OAuth2 / multi-tenant auth (use API key for MVP)
- Elasticsearch (use SQLite FTS or in-memory for MVP)

**Constraints**
- Timeline: 2-week MVP
- Team: 1 human architect + AI coding agent
- Platform: Python 3.12, FastAPI, uv package manager
- Budget: $0 cloud spend for dev (local-only)
```

---

### H1 Checkpoint

At this point you should have:
- [x] `product/PRD.md` S1 filled (Vision, Primary user, Problem statement, Non-goals)
- [x] `product/PRD.md` S2 filled (In-scope, Out-of-scope, Constraints)
- [x] `product/ARCH.md` S1 started (Constraints mirrored from PRD)
- [x] `product/ARCH.md` S4 started (Trust boundaries from C4 Context)
- [x] Optional reference docs in `product/docs/`

---

## H2: LOGICAL DESIGN (Decomposition & Flows)

**Goal:** Break the scope into buildable units. This phase converts your vision and boundaries into concrete use cases, stories with acceptance criteria, requirements, and user journeys. H2.3a and H2.3b run **in parallel** because they address independent concerns (technical requirements vs. user experience).

---

### H2.1: Use Case Modeling

**Purpose:** Map all system behaviors into functional groups. Use cases are the bridge between "what the system does" (scope) and "how we slice the work" (stories). They establish the functional topology that shapes your service boundaries and code module structure.

#### Frameworks & Tools

**UML Use Case Diagrams**
- **What it is:** A diagram showing actors (stick figures) connected by lines to use case ovals (system behaviors), all contained within a system boundary box.
- **Why use it:** Provides a visual inventory of every distinct behavior the system supports. Makes it immediately obvious if you have missed an actor-behavior pair. The system boundary box physically represents your scope.
- **How to use it:**
  1. Draw a rectangle representing your system boundary.
  2. Place all actors from H1.2 outside the rectangle.
  3. Inside the rectangle, draw an oval for each distinct behavior: "Search Jobs," "Ingest Job Batch," "Check Health," "Get Job by ID."
  4. Connect each actor to the use cases they participate in.
  5. Look for `<<include>>` relationships (use case A always triggers use case B) and `<<extend>>` relationships (use case A sometimes triggers use case B).
- **What insight it brings:** Shows the complete functional surface area at a glance. For a job engine, you see that "API Consumer" connects to "Search Jobs" and "Get Job by ID," while "Ingestion Pipeline" connects only to "Ingest Job Batch." This asymmetry drives different auth strategies.

**DDD Bounded Contexts** (Eric Evans)
- **What it is:** A Domain-Driven Design technique that groups related concepts into self-contained "contexts," each with its own internal model/language. Contexts communicate through explicit interfaces.
- **Why use it:** Prevents a monolithic model where everything depends on everything. Even in a small app, separating "Ingestion" from "Search" means changes to ingestion logic don't ripple into search code.
- **How to use it:**
  1. List your domain concepts (Job, Company, Location, SearchQuery, IngestBatch, etc.).
  2. Group them by which concepts change together: "IngestBatch + JobUpsert + deduplication" belong together; "SearchQuery + pagination + filtering" belong together.
  3. Draw a boundary around each group. Name the boundaries (e.g., "Ingestion Context," "Search Context").
  4. Identify shared concepts that cross boundaries (e.g., "JobPosting" is read by Search but written by Ingestion). Decide who "owns" the model.
- **What insight it brings:** Defines module boundaries in your code. The Ingestion Context might become `app/services/ingest.py` and the Search Context might become `app/services/search.py`. The shared `JobPosting` model lives in `contracts/schemas.py` because it is the contract between contexts.

**Event Storming** (Alberto Brandolini)
- **What it is:** A collaborative modeling technique where you list all domain events (things that happen) on sticky notes, then group them into aggregates, commands, and policies.
- **Why use it:** Discovers behaviors that use-case diagrams miss -- especially asynchronous events, side effects, and policies. "Job Ingested" is an event that might trigger "Update Search Index" as a policy.
- **How to use it:**
  1. List all events in past tense: "Job Batch Received," "Job Validated," "Job Upserted," "Search Executed," "Health Checked."
  2. For each event, identify the command that triggers it: "Submit Ingest Batch" -> "Job Batch Received."
  3. For each event, identify downstream effects (policies): "Job Upserted" -> "Index Updated" (if using a search index).
  4. Group events into aggregates (clusters that share a lifecycle): the "JobPosting" aggregate owns all events related to a single job's lifecycle.
- **What insight it brings:** Surfaces workflows you haven't thought about. "What happens when an ingested job has an external_id that already exists?" -> "Job Deduplicated" event. This becomes a story.

#### How to do it

1. Draw a UML Use Case diagram with all actors from H1.2 and all system behaviors.
2. Optionally run an Event Storming exercise to discover events, commands, and policies.
3. Group related use cases into bounded contexts using DDD.
4. Assign **UC tags** to each functional group (e.g., `UC:SEARCH`, `UC:INGEST`, `UC:ADMIN`).

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| UC tag glossary (tag -> meaning) | `product/PRD.md` > **S5. UC tags** table |
| Use case diagram | `product/diagrams/use_cases.puml` or `.drawio` |
| Bounded context map (optional) | `product/diagrams/context_map.png` |
| Event storm summary (optional) | `product/docs/event_storm.md` |

**Example PRD.md S5 output:**
```markdown
## 5. Optional UC tags
| UC tag | Meaning | Notes |
|--------|---------|-------|
| UC:SEARCH | Job search and listing | GET /jobs, GET /jobs/{id} |
| UC:INGEST | Batch job ingestion pipeline | POST /ingest/jobs |
| UC:META | Health and version metadata | GET /health, GET /meta/version |
```

---

### H2.2: Story Decomposition

**Purpose:** Convert use cases into implementable **vertical slices** (stories). Each story must be deliverable in one day or less by the coding agent. Stories are the **approval boundary** between you and the agent -- the agent can never build what is not in a story.

#### Frameworks & Tools

**User Story Mapping** (Jeff Patton)
- **What it is:** A two-dimensional layout where the horizontal axis shows the user's workflow (steps in sequence) and the vertical axis shows priority (Must-have at top, Nice-to-have at bottom). Each card is a story.
- **Why use it:** Ensures stories follow the user's natural workflow rather than being isolated features. Reveals gaps in the flow -- if you have "Search Jobs" and "View Job Detail" but nothing for "Filter by Country," the map shows the missing step.
- **How to use it:**
  1. Lay out the user's end-to-end workflow across the top (left to right): e.g., "Discover Jobs" -> "Filter Results" -> "View Details" -> "Apply."
  2. Under each workflow step, stack story cards vertically by priority (top = Must, bottom = Could).
  3. Draw a horizontal line across the map: everything above the line is your MVP release; everything below is V2+.
  4. Each card above the line becomes a story (S-V###).
- **What insight it brings:** Shows the minimum viable *journey*, not just minimum viable *features*. If "Filter by Country" is below the line but "View Details" is above it, you get searchable jobs with detail views but no country filter in V1. Users can still complete the core journey.

**INVEST Criteria** (Bill Wake)
- **What it is:** A quality checklist for well-formed user stories: **I**ndependent (can be built in any order), **N**egotiable (details can flex), **V**aluable (delivers user value), **E**stimable (small enough to estimate), **S**mall (deliverable in 1 day), **T**estable (has clear acceptance criteria).
- **Why use it:** Catches bad stories before build. A story that fails "Small" will stall the agent mid-implementation. A story that fails "Testable" will fail acceptance review.
- **How to use it:**
  1. Write each story using the template: "As a [actor], I want [goal] so that [value]."
  2. Check each INVEST letter. The most critical for this process: **S** (must be <= 1 day) and **T** (must have Given/When/Then acceptance criteria).
  3. If a story fails S: split it. "Implement full search" fails S. "Return all jobs with pagination" and "Filter jobs by text query" are two smaller stories that pass S.
- **What insight it brings:** Prevents stories that are too big, too vague, or untestable. Each story will be handed to the coding agent, which needs precise, bounded work units.

**Gherkin Given/When/Then** (Cucumber)
- **What it is:** A structured format for writing acceptance criteria: **Given** (precondition), **When** (action), **Then** (expected outcome).
- **Why use it:** Unambiguous, testable acceptance criteria. The coding agent uses these to know exactly what "done" means. They also translate directly into test assertions.
- **How to use it:**
  1. For each story, write 2-5 acceptance criteria in Given/When/Then format.
  2. Cover the happy path, one edge case, and one error case.
  3. Example: "Given the database has 100 jobs, When GET /jobs?limit=10 is called, Then the response contains exactly 10 items and page_info.has_more is true."
- **What insight it brings:** Eliminates ambiguity. "Search should work" is untestable. "Given a job with title 'Python Developer', When GET /jobs?q=python, Then the response includes that job" is testable.

#### Scrum Mapping to Process Steward

If you come from Scrum, here is how concepts translate:

| Scrum concept | Process Steward equivalent | Notes |
|---------------|---------------------------|-------|
| Theme | Not tracked | Strategic alignment only |
| Epic | UC tag (label only) | e.g., UC:SEARCH -- grouping, not a work unit |
| Story | S-V### (in PRD.md S4) | The approval boundary. Human approves these. |
| Task | T-V###.## (JIT in PROGRESS.md) | Agent creates these at runtime. Not your concern now. |

#### How to do it

1. Create a story map using User Story Mapping: lay out the user workflow, stack stories by priority.
2. Slice each story to pass INVEST (especially S: <= 1 day, T: has acceptance criteria).
3. Write acceptance criteria in Given/When/Then (Gherkin) format for each story.
4. Assign UC tags from H2.1 to each story.
5. Assign risk tags: `LOW` (trivial, agent proceeds), `MED` (moderate, agent proceeds but human reviews), `HIGH` (destructive/irreversible, agent asks first).
6. Sequence the stories (dependency order).

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| Story index table (ID, title, UC tag, risk) | `product/PRD.md` > **S4. Story Backlog** > **Story index** table |
| Full story definitions (summary, acceptance criteria, out-of-scope, dependencies) | `product/PRD.md` > **S4. Story Backlog** > one **S-V### block per story** (using the Story template) |
| Story map image (optional, for reference) | `product/docs/story_map.png` |

**Example PRD.md S4 output:**
```markdown
### Story index (plan)
| Story ID | Title | UC tags | Notes |
|----------|-------|---------|-------|
| S-V001 | Health and version endpoints | UC:META | LOW risk, foundational |
| S-V002 | Batch job ingestion | UC:INGEST | MED risk, core data pipeline |
| S-V003 | List jobs with cursor pagination | UC:SEARCH | LOW risk |
| S-V004 | Full-text search by query param | UC:SEARCH | LOW risk, depends on S-V003 |
| S-V005 | Get job by ID | UC:SEARCH | LOW risk |

---

#### S-V003 -- List jobs with cursor pagination
- **UC tags:** UC:SEARCH
- **Summary:** As an API consumer, I want to list all job postings with cursor-based pagination so that I can reliably iterate through large result sets without offset drift.
- **Acceptance criteria:**
  - AC-01: Given the database has 100 jobs, When GET /jobs?limit=10, Then response contains 10 items and page_info.has_more=true and page_info.next_cursor is non-null.
  - AC-02: Given next_cursor from AC-01, When GET /jobs?cursor={next_cursor}&limit=10, Then response contains the next 10 items.
  - AC-03: Given the last page of results, When GET /jobs?cursor={last_cursor}, Then page_info.has_more=false and page_info.next_cursor is null.
  - AC-04: Given an invalid cursor value, When GET /jobs?cursor=garbage, Then response is 400 with ErrorResponse.
- **Out of scope:** Sorting options, filtering by any field (that is S-V004+).
- **Dependencies:** S-V002 (needs ingested data to paginate).
```

---

### H2.3a: Requirements (FR + NFR)

> **Runs in parallel with H2.3b.**

**Purpose:** Formalize functional requirements (derived from stories) and non-functional requirements (performance, security, reliability). NFRs shape architecture decisions -- if you need sub-100ms latency, that eliminates certain database choices.

#### Frameworks & Tools

**Quality Attribute Scenarios** (SEI/CMU)
- **What it is:** A structured format for specifying non-functional requirements: Source -> Stimulus -> Environment -> Artifact -> Response -> Response Measure.
- **Why use it:** Turns vague NFRs ("the system should be fast") into testable specifications ("Under normal load, search endpoint responds in < 200ms at p95"). Testable NFRs become acceptance criteria or monitoring alerts.
- **How to use it:**
  1. For each quality attribute (performance, availability, security, etc.), fill the template:
     - Source: Who/what triggers it? (e.g., "100 concurrent API consumers")
     - Stimulus: What happens? (e.g., "send search queries")
     - Environment: Under what conditions? (e.g., "normal operation, 50K jobs in DB")
     - Artifact: What is affected? (e.g., "GET /jobs endpoint")
     - Response: What should happen? (e.g., "return results")
     - Response Measure: How to measure success? (e.g., "p95 latency < 200ms")
  2. Write 3-5 scenarios for the most critical quality attributes.
- **What insight it brings:** Converts "fast" into "p95 < 200ms under 100 concurrent users with 50K jobs." This number drives database choice, indexing strategy, and caching decisions.

**12-Factor App** (Heroku / Adam Wiggins)
- **What it is:** Twelve principles for building cloud-native applications: codebase in VCS, explicit dependencies, config in environment, backing services as attached resources, strict build/release/run separation, stateless processes, port binding, concurrency, disposability, dev/prod parity, logs as streams, admin processes as one-off tasks.
- **Why use it:** Provides a checklist of operational NFRs that are easy to forget. "Config in environment" means no hardcoded connection strings. "Logs as streams" means stdout, not file-based logging.
- **How to use it:**
  1. Review each of the 12 factors against your design.
  2. Note any factors that your current architecture violates or hasn't addressed.
  3. Add relevant factors as NFRs (e.g., NFR-003: "All config via environment variables, no hardcoded secrets").
- **What insight it brings:** Catches operational requirements that stories miss. Stories describe *features*; 12-Factor describes *how features should be built operationally*.

**OWASP Top 10** (OWASP Foundation)
- **What it is:** The ten most critical web application security risks, updated periodically. Includes: Injection, Broken Auth, Sensitive Data Exposure, XML External Entities, Broken Access Control, Security Misconfiguration, XSS, Insecure Deserialization, Known Vulnerabilities, Insufficient Logging.
- **Why use it:** Provides a security baseline checklist. Every API should address at least the top 5 OWASP risks as NFRs. The coding agent needs to know which security measures are required.
- **How to use it:**
  1. Review each OWASP risk against your API surface.
  2. For each applicable risk, write a security NFR: "NFR-005: All user input must be validated via Pydantic strict models (extra='forbid') to prevent injection."
  3. Flag risks that need dedicated stories (e.g., "Implement API key auth" -> S-V00X).
- **What insight it brings:** Surfaces security requirements that should be part of every story's implementation (e.g., input validation) vs. requirements that need their own stories (e.g., auth system).

#### How to do it

1. List functional requirements by referencing your stories: "FR-001: System must support batch ingestion (ref: S-V002)."
2. Write 3-5 non-functional requirements using Quality Attribute Scenarios format.
3. Review against 12-Factor App principles -- add any missing operational NFRs.
4. Review against OWASP Top 10 -- add any missing security NFRs.
5. Check: do any NFRs invalidate your architecture assumptions? (If so, this is the feedback loop back to H2.1-H2.2.)

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| Functional requirements table (FR-###) | `product/PRD.md` > **S3. Requirements** > **Functional requirements** |
| Non-functional requirements table (NFR-###) | `product/PRD.md` > **S3. Requirements** > **Non-functional requirements** |
| Architecture constraints derived from NFRs | `product/ARCH.md` > **S1. Constraints and principles** |

**Example PRD.md S3 output:**
```markdown
## 3. Requirements
### Functional requirements (FR)
- FR-001: Batch ingest endpoint accepts 1-1000 job postings per request (ref: S-V002)
- FR-002: Search endpoint supports full-text query across title, company, description (ref: S-V004)
- FR-003: Cursor-based pagination with configurable limit 1-200, default 50 (ref: S-V003)

### Non-functional requirements (NFR)
- NFR-001: GET /jobs p95 latency < 500ms with 50K jobs in database
- NFR-002: POST /ingest/jobs processes 1000 jobs in < 10s
- NFR-003: All config via environment variables; no hardcoded secrets (12-Factor)
- NFR-004: All input validated via Pydantic strict models (OWASP: Injection)
- NFR-005: Structured JSON logging to stdout (12-Factor: Logs)
```

---

### H2.3b: User Journeys & UI

> **Runs in parallel with H2.3a.**

**Purpose:** Trace the end-user's path through the system and design the information hierarchy. For API-only products, this step focuses on the API consumer's developer experience (DX). For products with a frontend, it produces wireframes and component structure.

#### Frameworks & Tools

**User Journey Maps**
- **What it is:** A timeline visualization of a user's steps when interacting with the system, annotated with their thoughts, emotions, pain points, and touchpoints.
- **Why use it:** Reveals gaps in the story backlog. If the journey shows "Developer reads API docs -> tries first call -> gets error -> reads error message -> fixes call -> succeeds," each touchpoint needs a story or acceptance criterion (good error messages, good docs).
- **How to use it:**
  1. Pick one persona from H1.2.
  2. Map their end-to-end journey in 5-10 steps.
  3. For each step: note the action, the touchpoint (API endpoint, docs page, CLI), the expected response, and potential pain points.
  4. Repeat for each primary persona.
- **What insight it brings:** For an API product, the journey reveals DX requirements: "The developer needs to discover the API structure" -> OpenAPI docs story. "The developer needs clear error messages when input is invalid" -> error envelope spec.

**Atomic Design** (Brad Frost) -- *Frontend only*
- **What it is:** A methodology for building design systems from smallest to largest: Atoms (buttons, inputs) -> Molecules (search bar = input + button) -> Organisms (header = logo + nav + search bar) -> Templates (page layout) -> Pages (filled template).
- **Why use it:** Ensures consistent, reusable UI components. Prevents "every page looks different" syndrome.
- **How to use it:** Only relevant if your product has a frontend. For API-only MVPs, skip this.

**Wireframing (low-fidelity)**
- **What it is:** Rough, grayscale sketches of UI screens showing layout, content hierarchy, and interaction flow. No colors, no branding, no pixel-perfect design.
- **Why use it:** Quickly validates information architecture without getting distracted by visual design. A wireframe of the search results page shows: search bar, filter sidebar, results list, pagination controls -- before any CSS is written.
- **How to use it:**
  1. For each key screen/view, sketch the layout on paper or in Figma.
  2. Focus on: what information is shown, where it is placed, what actions are available.
  3. Annotate with the API endpoint(s) that power each section.
  4. For API-only products: create wireframes of the API response structure instead (JSON shape annotations).

#### How to do it

1. Trace 1-2 user journeys for your primary persona(s).
2. For API-only products: map the developer journey (discover -> authenticate -> first call -> paginate -> handle errors).
3. For frontend products: create low-fi wireframes for key screens.
4. Review: do the journeys reveal missing stories or acceptance criteria? If so, update PRD.md S4.

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| User journey maps | `product/diagrams/user_flows.fig` or `.md` |
| Wireframes (if frontend) | `product/diagrams/wireframes.fig` or `.png` |
| Component tree (if frontend) | `product/diagrams/component_tree.drawio` |
| Refinements to story acceptance criteria | `product/PRD.md` > **S4. Story Backlog** > update affected stories |

---

### H2 Decision Gate: NFR Feedback Loop

After H2.3a and H2.3b, check: **Do any NFRs invalidate your architecture assumptions?**

- If NFR-001 says "p95 < 50ms" but your planned SQLite database can't deliver that -> revise the architecture assumption or relax the NFR.
- If this happens, return to H2.1-H2.2 to re-scope stories and adjust the architecture boundaries.

This feedback loop is expected. It is cheaper to discover architecture conflicts here than during build.

---

### H2 Decision Gate: Frontend Needed?

- **If yes:** Include frontend concerns in the architecture scope (H3.1). Wireframes from H2.3b drive component design. Add frontend tech stack to ARCH.md S2.
- **If API only:** Skip frontend architecture. Backend-only scope keeps the architecture simpler.

---

### H2 Checkpoint

At this point you should have:
- [x] `product/PRD.md` S3 filled (FR and NFR tables)
- [x] `product/PRD.md` S4 filled (complete story backlog with acceptance criteria)
- [x] `product/PRD.md` S5 filled (UC tag glossary)
- [x] `product/ARCH.md` S1 updated (constraints from NFRs)
- [x] `product/diagrams/` contains use-case diagram, user journeys, optional wireframes

---

## H3: PHYSICAL DESIGN (Architecture, Data, Cloud, APIs)

**Goal:** Convert logical design into concrete technology decisions. H3.1 (Architecture) runs first, then three tracks run **in parallel** because they address independent concerns: tech stack selection, data + API design, and cloud + security.

---

### H3.1: Architecture (C4 Model)

**Purpose:** Design the system at three zoom levels: Context (done in H1.2), Container (services, databases, queues), and Component (modules within each container). Record key Architecture Decision Records (ADRs).

#### Frameworks & Tools

**C4 Model** (Simon Brown)
- **What it is:** A hierarchical approach to diagramming software architecture at four levels: Context (L1, done in H1.2), Container (L2), Component (L3), Code (L4, usually too detailed).
- **Why use it:** Provides a shared vocabulary and consistent zoom levels. Level 2 (Container) shows your deployment units; Level 3 (Component) shows your code modules. This maps directly to your repo structure.
- **How to use it:**
  1. **L2 Container diagram:** Draw each deployment unit as a box: "FastAPI Service," "SQLite Database," "Redis Cache" (if applicable). Show how they communicate (HTTP, SQL, etc.).
  2. **L3 Component diagram:** For each container, draw the internal modules: "API Router," "Ingest Service," "Search Service," "DB Adapter." Show dependencies between modules.
  3. Each container/component maps to a path in your repo (e.g., "Ingest Service" -> `app/services/ingest.py`).
- **What insight it brings:** Makes the code structure visual. When the coding agent creates files, it follows the component structure you define here. Mismatches between the diagram and the code are caught in HO.1.

**Hexagonal Architecture / Ports & Adapters** (Alistair Cockburn)
- **What it is:** An architecture pattern where business logic (core) is surrounded by ports (interfaces) and adapters (implementations). The core knows nothing about HTTP, databases, or external APIs.
- **Why use it:** Makes the codebase testable and swappable. You can test business logic without a database. You can swap SQLite for PostgreSQL by changing only the adapter, not the core.
- **How to use it:**
  1. Define your **core domain** (pure business logic with no framework imports): validation rules, deduplication logic, search ranking.
  2. Define **ports** (interfaces): `JobRepository` (abstract), `SearchIndex` (abstract).
  3. Define **adapters** (implementations): `SQLiteJobRepository`, `InMemorySearchIndex`.
  4. Map to repo structure: `app/services/` (core), `app/adapters/` (adapters), `app/api/` (HTTP adapter).
- **What insight it brings:** Forces clean dependency direction. The `ingest_service` depends on a `JobRepository` port, not on `sqlite3` directly. This is what makes your codebase maintainable.

**Architecture Decision Records (ADRs)** (Michael Nygard)
- **What it is:** A short document recording a significant architecture decision: Context, Decision, Status, Consequences.
- **Why use it:** Captures *why* you chose SQLite over PostgreSQL, or *why* you chose monolith over microservices. Without ADRs, future developers (including the coding agent) don't know why things are the way they are and may accidentally undo good decisions.
- **How to use it:**
  1. For each significant decision, write: **Context** (what is the situation?), **Decision** (what did we choose?), **Consequences** (what are the tradeoffs?).
  2. Keep ADRs in ARCH.md S1 as principles, or log as Decisions (D-###) in PROGRESS.md.

#### Architecture Decision: Monolith or Distributed?

- **Monolith (recommended for MVP):** Single-service architecture. Modular monolith with clean internal boundaries (Hexagonal Architecture). Faster to build, easier to deploy, lower operational complexity. Defer splitting to V2+.
- **Distributed:** Multi-service architecture with API gateways, message queues, separate data stores. Only if your NFRs or team structure demand it (e.g., separate ingestion service for independent scaling).

#### How to do it

1. Draw a C4 Level 2 (Container) diagram showing your deployment units and communication.
2. Draw a C4 Level 3 (Component) diagram for your main container showing internal modules.
3. Decide: monolith or distributed? (Monolith for MVP unless NFRs force otherwise.)
4. Record key ADRs (at minimum: why monolith/distributed, why chosen database, why chosen auth approach).

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| C4 Container diagram (L2) | `product/diagrams/c4_container.puml` or `.drawio` |
| C4 Component diagram (L3) | `product/diagrams/c4_component.puml` or `.drawio` |
| Architecture snapshot (text description of C4) | `product/ARCH.md` > **S4. Architecture snapshot** |
| ADR principles | `product/ARCH.md` > **S1. Constraints and principles** |
| Module-to-path mapping | `product/ARCH.md` > **S3. Repo map** (update the table) |

---

### H3.2a: Tech Stack (Track A -- parallel)

**Purpose:** Select the specific technology for every layer of the system. Each technology choice is an implicit ADR.

#### Frameworks & Tools

**Technology Radar** (ThoughtWorks)
- **What it is:** A periodic assessment of technologies in four rings: **Adopt** (proven, use by default), **Trial** (promising, use on non-critical paths), **Assess** (interesting, evaluate), **Hold** (avoid for new work).
- **Why use it:** Prevents choosing bleeding-edge tech for critical components. For an MVP, bias heavily toward Adopt-ring technologies.
- **How to use it:**
  1. For each layer (web framework, database, cache, auth, CI/CD, monitoring), list candidate technologies.
  2. Rate each candidate: Adopt/Trial/Assess/Hold based on maturity, community support, and your team's familiarity.
  3. Choose the Adopt-ring option unless there is a strong reason not to.
- **What insight it brings:** Prevents tech choice regret. FastAPI is Adopt-ring for Python APIs. SQLite is Adopt-ring for single-node MVP databases. An experimental vector DB is Trial-ring at best.

**TOGAF Technology Architecture**
- **What it is:** A framework for aligning technology choices with business and architecture constraints.
- **Why use it:** Ensures tech stack choices serve the requirements, not the other way around.

**12-Factor App** (revisited from H2.3a)
- **Why revisit:** Tech stack choices must align with 12-Factor principles. Your dependency manager (uv) handles Factor 2. Your database choice must support Factor 4 (backing services as attached resources).

#### How to do it

1. For each layer (backend, database, cache, auth, testing, CI, monitoring, IaC), list 1-2 candidates.
2. Select based on: maturity (Adopt-ring), team familiarity, alignment with NFRs, and constraints from H1.3.
3. Document each choice with brief rationale.

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| Tech stack table (layer -> technology -> rationale) | `product/ARCH.md` > **S2. Tech stack** |
| Quality gate tools (linter, formatter, type checker, test runner) | `product/ARCH.md` > **S2. Tech stack** (already has starter defaults) |
| Dependencies matching the stack | `pyproject.toml` (verify listed dependencies match ARCH.md S2) |

---

### H3.2b: Data Model / ERD (Track B -- sequential with H3.3b)

**Purpose:** Design the data entities, relationships, constraints, and indexes. The Pydantic models in `schemas.py` are the **single source of truth** for data shapes -- they feed both the database layer and the API.

#### Frameworks & Tools

**Entity-Relationship Diagrams (ERD)** (Peter Chen / Crow's Foot notation)
- **What it is:** A diagram showing entities (tables/objects), their attributes, and relationships (one-to-many, many-to-many, etc.).
- **Why use it:** Visualizes data structure before writing code. Catches relationship mistakes (e.g., "Does a Job have one Location or many?") before they become schema migrations.
- **How to use it:**
  1. List all entities from your domain model: JobPosting, Location, Salary, TaxonomyTag, SkillTag, etc.
  2. For each entity, list attributes with types and constraints (required, unique, nullable).
  3. Draw relationships: JobPosting *has-one* Location, JobPosting *has-many* SkillTags.
  4. Note indexes: "Search by title" -> full-text index on title field.
- **What insight it brings:** Surfaces data modeling decisions. "Is Location embedded in Job or a separate entity?" The ERD makes this explicit. For a document-style API, embedding (denormalization) is simpler; for relational queries, normalization is better.

**DDD Aggregates** (Eric Evans)
- **What it is:** A cluster of domain objects treated as a single unit for data changes. The "aggregate root" is the entry point (e.g., JobPosting is the root; Location and Salary are value objects within it).
- **Why use it:** Defines transaction boundaries. When you upsert a Job, you upsert its Location and Salary atomically. You never update a Location without its parent Job.
- **How to use it:**
  1. Identify which entities change together (JobPosting + Location + Salary = one aggregate).
  2. Identify which entities are independent (IngestBatch is a separate aggregate from JobPosting).
  3. The aggregate root's ID is the primary key for the aggregate.

**Pydantic StrictModel** (already in the codebase)
- **What it is:** Pydantic models with `extra="forbid"` configuration that reject any fields not explicitly defined. This is the project's convention.
- **Why use it:** Prevents contract drift. If someone adds a field to the API response without updating the schema, Pydantic raises an error. This is enforced by `make check`.

#### How to do it

1. Draw an ERD of all domain entities with attributes, types, and relationships.
2. Define aggregates (which entities change together atomically).
3. Write/update Pydantic models in `product/contracts/schemas.py` to match the ERD.
4. Ensure every model uses `StrictModel` (inherits `extra="forbid"` config).

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| ERD diagram | `product/diagrams/erd.puml` or `.drawio` |
| Pydantic models (DTOs) | `product/contracts/schemas.py` |
| Naming conventions (snake_case, ID formats, timestamps) | `product/contracts/CONTRACTS.md` > **S2. Naming conventions** |

---

### H3.3b: API Design (Track B -- sequential after H3.2b)

**Purpose:** Define the HTTP API contract: endpoints, methods, request/response schemas, error envelope, pagination scheme, and auth. The OpenAPI spec is written **before** code (contract-first design). Schemas from H3.2b feed directly into OpenAPI components.

#### Frameworks & Tools

**Contract-First Design**
- **What it is:** The practice of writing the API specification (OpenAPI) before writing any implementation code. The spec is the contract; the code must conform to it.
- **Why use it:** Prevents the API from being shaped by implementation accidents. The coding agent builds code that matches the spec, not the other way around. During build (P5-P7), the spec is frozen -- changes require a CCR.
- **How to use it:**
  1. Write the OpenAPI YAML file with all paths, operations, parameters, and response schemas.
  2. Reference Pydantic models from H3.2b as the component schemas.
  3. Validate that every endpoint traces to at least one story in PRD.md S4.

**RESTful API Guidelines**
- **What it is:** Best practices for REST API design: use nouns for resources, HTTP methods for actions, consistent error responses, meaningful status codes.
- **Why use it:** Creates a predictable, developer-friendly API. Consumers can guess the endpoint for a new resource without reading docs.
- **How to use it:**
  1. Resources as nouns: `/jobs`, `/jobs/{job_id}`, `/ingest/jobs`.
  2. HTTP methods: GET (read), POST (create/action), PUT/PATCH (update), DELETE (remove).
  3. Consistent error envelope: `{ code, message, trace_id?, details? }` for all error responses.
  4. Consistent success responses: list endpoints return `{ items, page_info }`.

**Cursor Pagination**
- **What it is:** Pagination using an opaque cursor token instead of offset/limit. The server returns `next_cursor`; the client passes it back to get the next page.
- **Why use it:** Stable under concurrent writes (offset pagination breaks when new items are inserted). More efficient for large datasets (no "count all rows" query).
- **How to use it:**
  1. Define `PageInfo` schema with `next_cursor` (nullable string) and `has_more` (boolean).
  2. List endpoints accept `cursor` and `limit` query parameters.
  3. Server encodes the position in the cursor (e.g., base64-encoded last-seen ID).

#### How to do it

1. Write the OpenAPI spec (`openapi.yaml`) with all endpoints, referencing schemas from H3.2b.
2. For each endpoint, verify it maps to at least one story in PRD.md S4.
3. Define the standard error envelope in both `openapi.yaml` and `schemas.py`.
4. Define pagination scheme (cursor-based) in both spec and schemas.

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| OpenAPI specification | `product/contracts/openapi.yaml` |
| Error model documentation | `product/contracts/CONTRACTS.md` > **S3. Error model** |
| Invariants (idempotency, pagination, validation rules) | `product/contracts/CONTRACTS.md` > **S4. Invariants** |
| Compatibility policy (what changes are breaking) | `product/contracts/CONTRACTS.md` > **S5. Compatibility / migration policy** |
| Endpoint-to-story traceability | Verify: every path in `openapi.yaml` maps to >= 1 S-V### in `PRD.md` S4 |

---

### H3.2c: Cloud Architecture (Track C -- sequential with H3.3c)

**Purpose:** Design the deployment topology: compute, networking, data persistence, observability, CI/CD, and Infrastructure-as-Code. For local-only MVPs, this step may be lightweight (document the local setup and defer cloud to V2).

#### Frameworks & Tools

**AWS Well-Architected Framework** (Amazon) / equivalent for GCP/Azure
- **What it is:** Five pillars for evaluating cloud architectures: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization.
- **Why use it:** Provides a checklist for cloud design. Even for an MVP, reviewing the five pillars catches obvious gaps (e.g., no monitoring, no backup strategy).
- **How to use it:**
  1. For each pillar, ask: "What is the minimum we need for MVP?"
  2. **Operational Excellence:** Structured logging, health endpoint, `make check` CI.
  3. **Security:** API key auth (defer OAuth2), TLS, no secrets in code.
  4. **Reliability:** Graceful shutdown, health checks for orchestrators.
  5. **Performance:** Validate against NFRs from H2.3a.
  6. **Cost:** Free-tier compatible for MVP.

**Infrastructure as Code (IaC)** -- Terraform, Pulumi, CDK
- **What it is:** Defining infrastructure in code files (version-controlled, reproducible) rather than clicking through cloud consoles.
- **Why use it:** Reproducible deployments. If the server dies, you re-run the IaC and everything is back.
- **How to use it:** For MVP, document the target deployment platform. IaC files can be added as a story in V1.1+.

**GitOps**
- **What it is:** Using Git as the single source of truth for infrastructure and application state. Changes are deployed by merging to a branch.
- **Why use it:** Auditable, reversible deployments.

#### How to do it

1. Choose your deployment target: local-only (MVP), single cloud service (Fly.io, Railway, Cloud Run), or full cloud architecture (AWS/GCP/Azure).
2. Document compute, networking, data, and observability choices.
3. For MVP: keep it minimal. Document the local dev setup and defer cloud IaC to a future story.

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| Deployment topology description | `product/ARCH.md` > **S4. Architecture snapshot** (append deployment topology) |
| Extension points for cloud (e.g., "swap SQLite for RDS") | `product/ARCH.md` > **S6. Extension points** |
| Cloud architecture diagram (if applicable) | `product/diagrams/cloud_arch.puml` or `.drawio` |

---

### H3.3c: Security & Compliance (Track C -- sequential after H3.2c)

**Purpose:** Define authentication, authorization, data classification, secrets management, and threat model. Cloud topology from H3.2c shapes secrets management (e.g., AWS Secrets Manager vs. environment variables).

#### Frameworks & Tools

**OWASP Top 10** (revisited from H2.3a, now with implementation specifics)
- **What it is:** The ten most critical web security risks, now applied to your specific architecture.
- **Why use it:** Turns abstract security risks into concrete mitigations.
- **How to use it:**
  1. For each of the top 10 risks, assess: "Does our architecture address this?"
  2. **Injection:** Pydantic strict models with `extra="forbid"` handle input validation. SQL parameterization handles database queries.
  3. **Broken Auth:** Define auth mechanism (API key for MVP, JWT/OAuth2 for prod).
  4. **Sensitive Data Exposure:** Classify data fields (PII: company_name? No. Email addresses? Not in current schema).
  5. Document mitigations in ARCH.md S7.

**STRIDE Threat Modeling** (Microsoft)
- **What it is:** A structured threat identification framework: **S**poofing (impersonation), **T**ampering (data modification), **R**epudiation (denial of actions), **I**nformation Disclosure (data leaks), **D**enial of Service, **E**levation of Privilege.
- **Why use it:** Systematically identifies attack vectors specific to your system. Prevents "we didn't think of that" security incidents.
- **How to use it:**
  1. For each component in your C4 diagram, ask each STRIDE question:
     - **Spoofing:** Can someone impersonate the Ingestion Pipeline? -> Require auth on POST /ingest/jobs.
     - **Tampering:** Can someone modify job data in transit? -> Use TLS.
     - **Repudiation:** Can we prove who ingested what? -> Log source + timestamp.
     - **Information Disclosure:** Can someone read all jobs without auth? -> GET /jobs is public (by design for search). POST /ingest requires auth (write access).
     - **Denial of Service:** Can someone flood the ingest endpoint? -> Rate limiting story.
     - **Elevation of Privilege:** Can a search consumer call the ingest endpoint? -> Separate auth scopes.
  2. Prioritize the top 3 attack vectors. These become security NFRs or stories.
- **What insight it brings:** Produces specific, actionable security requirements. "Spoofing on ingest" becomes story S-V00X: "Implement bearer token auth on POST /ingest/jobs."

**Data Classification**
- **What it is:** Labeling data by sensitivity: Public (search results), Internal (ingest pipeline data), Confidential (auth tokens, API keys).
- **Why use it:** Determines which data needs encryption, which needs access control, and which can be freely cached.

#### How to do it

1. Run STRIDE threat analysis against your C4 diagram components.
2. Review OWASP Top 10 against your specific endpoints.
3. Classify your data fields (public/internal/confidential).
4. Define auth mechanism, secrets management approach, and top-3 threat mitigations.
5. Check: does the threat model generate new security stories? If yes, add them to PRD.md S4 (this is the feedback loop).

#### Expected output and where to add it

| Output | Target location |
|--------|----------------|
| Auth mechanism description | `product/ARCH.md` > **S7. Security and privacy** |
| Data classification | `product/ARCH.md` > **S7. Security and privacy** > **Data classification** |
| Secrets management approach | `product/ARCH.md` > **S7. Security and privacy** |
| Threat notes (top 3 attack vectors + mitigations) | `product/ARCH.md` > **S7. Security and privacy** > **Threat notes** |
| Threat model diagram (optional) | `product/diagrams/threat_model.puml` or `.md` |
| New security stories (if any) | `product/PRD.md` > **S4. Story Backlog** (append new S-V### entries) |

---

### H3 Feedback Loop: Security Stories

If H3.3c's threat model reveals new requirements (e.g., "We need rate limiting on the ingest endpoint"), add these as new stories to PRD.md S4. Update the story index and roadmap. This feedback loop from security analysis back to the story backlog is expected and healthy.

---

### H3 Checkpoint

At this point you should have:
- [x] `product/ARCH.md` fully filled (S1-S7)
- [x] `product/contracts/schemas.py` with all Pydantic models
- [x] `product/contracts/openapi.yaml` with all endpoints
- [x] `product/contracts/CONTRACTS.md` with naming, errors, invariants, compatibility
- [x] `product/diagrams/` contains C4, ERD, and optionally cloud/threat diagrams
- [x] `product/PRD.md` S4 complete (including any security stories from feedback loop)
- [x] `product/PRD.md` S6 Roadmap updated (versions -> stories mapping)

---

## HANDOFF: Distillation & Agent Initialization

**Goal:** Validate that all artifacts are internally consistent, commit them to the repo, and hand off to the coding agent via `/seed`.

---

### HO.1: Artifact Distillation & Consistency Checks

**Purpose:** Cross-validate all design outputs before the coding agent starts. Inconsistencies found here are cheap to fix; inconsistencies found during build trigger CCRs and stall progress.

#### Consistency checks to perform

Run each check manually. If any fails, return to the affected step and fix the discrepancy.

| # | Check | How to verify | If fails, return to |
|---|-------|---------------|---------------------|
| 1 | **Every OpenAPI path maps to >= 1 story** | For each path in `openapi.yaml`, find the corresponding S-V### in PRD.md S4 | H2.2 (add missing story) or H3.3b (remove orphan endpoint) |
| 2 | **Pydantic models match OpenAPI schemas** | Field names, types, optionality, and enum values in `schemas.py` match `openapi.yaml` components | H3.2b-H3.3b (align schemas) |
| 3 | **ARCH repo map matches actual directory structure** | Every path in ARCH.md S3 table exists (or will be created by a story) | H3.1 (update repo map) |
| 4 | **pyproject.toml deps match ARCH.md S2 tech stack** | Every technology in ARCH.md S2 has a corresponding dependency in pyproject.toml | H3.2a (add missing deps or update ARCH) |
| 5 | **Every story has acceptance criteria** | Each S-V### in PRD.md S4 has at least 2 AC lines | H2.2 (add criteria) |
| 6 | **Every story fits in <= 1 day** | No story looks bigger than a single vertical slice | H2.2 (split oversized stories) |
| 7 | **UC tags used in stories are defined in S5** | Every UC:XXX tag in the story index appears in the UC tag glossary | H2.1 (add missing tags) |
| 8 | **Constraints in PRD.md S2 match ARCH.md S1** | Same constraints listed in both files | H1.3 / H3.1 (align) |
| 9 | **NFRs have architecture support** | Each NFR in PRD.md S3 has a corresponding design decision in ARCH.md | H2.3a / H3.1 (add missing support) |
| 10 | **Security threats have stories or NFRs** | Each threat in ARCH.md S7 is addressed by an NFR or a story | H3.3c / H2.2 (add mitigation) |

#### How to do it

1. Go through each check in the table above.
2. For each failure, return to the indicated step and fix the discrepancy.
3. Repeat until all 10 checks pass.

#### Expected output

All consistency checks pass. No new files are produced -- this step validates existing artifacts.

---

### HO.2: Execute /seed

**Purpose:** The formal handoff from architect (you) to coding agent. Running `/seed` triggers Phase P0 (Install and Wire), activating the Process Steward agent.

#### How to do it

1. Commit all artifacts to the repo:
   - `product/PRD.md` (fully filled S1-S6)
   - `product/ARCH.md` (fully filled S1-S7)
   - `product/contracts/schemas.py`, `openapi.yaml`, `CONTRACTS.md`
   - `product/diagrams/*` (all diagram files)
   - `product/docs/*` (optional reference materials)
2. Open the IDE chat console.
3. Type `/seed` and press Enter.

#### What the agent does

The agent reads all artifacts, validates the workspace, runs `make check`, and records the result:

- **If `make check` PASS:** Agent records Gate G0 = PASS in PROGRESS.md. You are ready for Phase A (P1-P4) of the development lifecycle.
- **If `make check` FAIL:** Agent logs Issues (I-###) and attempts fixes. You may need to resolve environment setup problems.

#### What follows

After G0 passes, the development lifecycle begins (see `process/diagrams/DEVELOPMENT_PROCESS.puml`):

```
/seed (G0) -> /plan (P1-P4, G1+G2) -> /next (P5-P7, G3 per story) -> /release (P8-P11, G4+G5)
```

---

## Quick Reference: All Outputs by File

### product/PRD.md

| Section | Filled by step |
|---------|---------------|
| S0. Metadata | H1.1 |
| S1. Vision (one-liner, primary user, problem, non-goals) | H1.1 + H1.2 (actors/personas) |
| S2. Scope boundaries (in-scope, out-of-scope, constraints) | H1.3 |
| S3. Requirements (FR + NFR tables) | H2.3a |
| S4. Story Backlog (index + full story definitions) | H2.2 + H3.3c (security stories) |
| S5. UC tags (glossary table) | H2.1 |
| S6. Roadmap (versions -> stories) | H2.2 |

### product/ARCH.md

| Section | Filled by step |
|---------|---------------|
| S0. Metadata | H1.1 |
| S1. Constraints and principles (constraints + ADRs) | H1.3 + H2.3a (NFR constraints) + H3.1 (ADRs) |
| S2. Tech stack | H3.2a |
| S3. Repo map | H3.1 |
| S4. Architecture snapshot (C4-lite + trust + deployment) | H1.2 (trust) + H3.1 (C4) + H3.2c (deployment) |
| S5. Conventions (naming, errors, logging, testing) | H3.1 + H3.3b |
| S6. Extension points | H3.2c |
| S7. Security and privacy | H3.3c |

### product/contracts/

| File | Filled by step |
|------|---------------|
| `schemas.py` (Pydantic models) | H3.2b |
| `openapi.yaml` (API specification) | H3.3b |
| `CONTRACTS.md` (naming, errors, invariants, compatibility) | H3.2b + H3.3b |

### product/diagrams/

| File | Filled by step |
|------|---------------|
| `c4_context.puml` / `.drawio` | H1.2 |
| `use_cases.puml` / `.drawio` | H2.1 |
| `erd.puml` / `.drawio` | H3.2b |
| `c4_container.puml` / `.drawio` | H3.1 |
| `c4_component.puml` / `.drawio` | H3.1 |
| `cloud_arch.*` (optional) | H3.2c |
| `threat_model.*` (optional) | H3.3c |
| `user_flows.*` | H2.3b |
| `wireframes.*` (if frontend) | H2.3b |
