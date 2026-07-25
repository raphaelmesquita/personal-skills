---
name: to-tickets-agentic
description: "Compile a spec, plan, legacy PRD, handoff, or conversation into a coordinated feature execution package: an agent-sized implementation graph, shared acceptance matrix, downstream contracts, economical checks, and one terminal $finalize-feature node. Use when autonomous agents will implement a feature through a long-running /goal."
---

# To Tickets Agentic

Compile one feature source into a durable execution package for a coordinated feature branch. The package is the interface between planning and the `/goal` loop: implementation nodes run with `$implement-slice`; one terminal node runs with `$finalize-feature`.

## 1. Gather The Source

Read the relevant conversation and every named source: spec, plan, handoff, issue body and comments, ADR, decision log, and tracker convention. Treat an existing PRD as a legacy spec.

Identify:

- the parent source and accepted decisions;
- exhaustive feature acceptance criteria;
- non-goals, invariants, compatibility and data constraints;
- feature-branch and publishing expectations;
- tracker target and ready-state convention;
- known validation surfaces.

Record absent information as an explicit constraint or unresolved decision. Complete this step only when no implementation node contains a product or architecture choice that an implementing agent would have to invent.

## 2. Explore The Implementation Surface

Inspect the smallest useful set of code and documentation. Use project domain language, respect ADRs, locate stable verification surfaces, and identify dependencies that determine implementation order.

Complete exploration when the graph can use real project vocabulary, define meaningful downstream contracts, and avoid rediscovery of basic architecture in each fresh context.

## 3. Build The Execution Plan

Create `.scratch/<feature-slug>/execution-plan.md` as the shared manifest, including when tickets live in a remote tracker. Record:

- parent source, repository, base branch, immutable base revision, and intended feature branch;
- canonical lifecycle `ready → in-progress → implemented → verified → complete`, plus `waiting` for unmet dependencies and `blocked` for actual blockers;
- commit, push, PR, and merge authority as separate values;
- architectural guardrails and shared constraints;
- implementation graph and first frontier;
- cheap deterministic checks available during implementation;
- feature-wide verification surfaces;
- acceptance matrix assigning each feature criterion one stable ID and mapping it to contributing nodes and final evidence;
- the single terminal finalization node;
- definition of complete.

Local commits are the default for implementation nodes unless an explicit source prohibits them. `$finalize-feature` is the sole publication phase. The feature branch becomes merge-eligible only after the terminal node passes its pre-merge success gate, with merge as the final source-control action.

For change-producing work, `commit: false` requires `push: false`, `pr: false`, and `merge: false`. Reject incompatible authority before publishing the graph.

Complete the plan only when every acceptance criterion is defined exactly once under a stable ID and the matrix has reciprocal mappings between each ID and every contributing node.

## 4. Draft Implementation Nodes

Prefer tracer-bullet slices, but optimize the graph for coordinated delivery rather than independent release. Each implementation node must:

- fit one fresh agent context;
- produce one coherent, committable change;
- define objective implementation criteria;
- state the interface or behavior downstream nodes may assume;
- name economical deterministic checks;
- list the stable acceptance-criterion IDs they contribute to final QA;
- leave product completion claims to the terminal node.

Split only when a fresh context, dependency fan-out, isolated rollback, or materially clearer downstream contract earns the extra handoff. Merge tightly coupled sequential work when no useful checkpoint exists between it.

Preparatory, contract, migration, instrumentation, or discovery nodes are valid when they unlock later work. A discovery node must produce a durable decision artifact.

For wide refactors, preserve compatibility across intermediate commits only when required for data safety, external consumers, branch usability, or downstream implementation. Do not create compatibility scaffolding solely to make an internal feature-branch commit independently releasable.

Declare only genuine implementation blockers. Keep the graph acyclic and expose a non-empty frontier unless external work blocks the feature.

## 5. Define Checkpoint Candidates

The default after an implementation node is to continue to the next node. Name a potential dependency checkpoint only when a specific downstream dependency may justify it.

For each candidate, record:

- the concrete uncertainty that could emerge during implementation;
- which downstream work would be substantially reworked if the assumption is wrong;
- one focused check capable of resolving it.

The runtime still skips the checkpoint unless implementation actually exposes that uncertainty and the focused check is clearly cheaper than the likely rework. General risk, importance, or ticket size is not a candidate.

## 6. Add The Terminal Node

Create exactly one finalization node blocked by every implementation leaf. Set `Execution: $finalize-feature`. It owns:

- the acceptance matrix;
- full relevant verification;
- integrated Codex QA;
- independent aggregate review;
- corrections and rechecks;
- promotion from `implemented` to `verified` and `complete`;
- authorized push, PR, and merge.

The terminal node may change implementation code only to address finalization findings. It never delegates a second implementation pass over already completed nodes.

## 7. Audit And Confirm The Graph

Audit every implementation node:

- **What to implement** states one outcome, not a layer-by-layer activity list.
- **Context and constraints** contain the durable facts needed in a fresh context.
- **Implementation criteria** are objective and exhaustive for the node.
- **Downstream contract** makes dependent assumptions explicit.
- **Economical checks** avoid feature-wide QA.
- **Final QA contribution** lists stable IDs whose matrix entries reciprocally name the node.
- **Boundaries** preserve material non-goals and contracts.
- **Blocked by** contains every genuine prerequisite and no convenient predecessor.

Avoid volatile file predictions and working code snippets. Stable source paths, domain terms, and validation commands are useful.

Present the plan and numbered graph to the user. For each node show title, execution skill, blockers, delivered outcome, downstream contract, and sizing rationale when needed. Show the terminal node and acceptance-matrix coverage. Resolve graph, granularity, and architecture decisions before publication.

## 8. Publish

Publish blockers first so downstream nodes can reference real identifiers.

- **Local tracker:** create one file per node at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`.
- **Remote tracker:** create one issue per node and use native blockers or textual identifiers. Keep the local execution plan as the shared manifest.

Use the configured tracker value for ready nodes. Record dependency-bound nodes as `waiting` and actual failures as `blocked` in the closest native states; when the tracker lacks the canonical lifecycle, persist canonical state in the body, a comment, or operational memory.

Use this template for implementation nodes:

```md
# <NN> — <Title>

Status: <canonical state>
Execution: $implement-slice
Blocked by: <identifiers, or "None">

## Parent
<Source reference>

## Execution plan
<Path>

## What to implement
<One coherent outcome>

## Context and constraints
<Durable decisions, invariants, and compatibility requirements>

## Implementation criteria
- [ ] <Objective implementation result>

## Downstream contract
- <What later nodes may assume>

## Economical checks
- <Cheap deterministic evidence>

## Potential dependency checkpoint
- Default: skip
- Trigger: <specific implementation-time uncertainty, or "None">
- Focused check: <one check, or "None">

## Final QA contribution
- <Acceptance-criterion ID>

## Boundaries
- <Non-goal or preserved contract>
```

Use this template for the terminal node:

```md
# <NN> — Finalize <feature>

Status: waiting
Execution: $finalize-feature
Blocked by: <every implementation leaf>

## Parent
<Source reference>

## Execution plan
<Path>

## What to finalize
Validate, review, correct, and publish the integrated feature.

## Acceptance matrix
<Execution-plan section>

## Feature-wide verification
- <Required integrated evidence>

## Publishing authority
<Commit, push, PR, and merge policy>

## Boundaries
- Preserve unrelated work and defer follow-up scope explicitly.
```

## 9. Verify Publication

Finish only when:

- the execution plan and every approved node exist exactly once;
- all references and blockers resolve and the graph is acyclic;
- every implementation node passes the agent contract;
- the frontier is obvious;
- exactly one terminal node depends on every implementation leaf;
- every acceptance-criterion ID is defined once and maps reciprocally to implementation nodes and final evidence;
- checkpoint candidates satisfy the downstream-rework rule;
- no compatibility work exists only for independent release of an internal commit;
- the parent source remains unchanged.

Report the execution-plan path, tracker location, graph frontier, terminal node, validation results, and any unresolved external blocker.
