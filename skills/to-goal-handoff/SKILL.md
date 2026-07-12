---
name: to-goal-handoff
description: Create a goal-ready handoff from a spec or legacy PRD and ordered tickets for a /goal loop that executes each ticket with $ship-feature and maintains operational memory.
---

# To Goal Handoff

Create a specialized handoff for a long-running `/goal` that will implement every ticket in a spec-backed ticket set.

This is not a generic summary handoff. It must produce an actionable execution guide plus persistent operational memory so a fresh agent can pick the first unblocked ticket, run `$ship-feature`, update trackers, and continue without rediscovery.

## Process

### 1. Gather Sources

Read the current chat context first. Extract the user's latest objective, explicit constraints, named skills, destination paths, branch/commit expectations, and any implementation-loop rules that may not yet be persisted.

Then read the sources the user names: spec, ticket index, ticket directory, decision log, ideal-state document, problem statement, open questions, ADRs, existing handoffs, and existing operational memory. Treat an existing PRD as a legacy spec and preserve its path, title, and tracker identifier.

Use chat context as an auxiliary source, not a replacement for persisted artifacts. If chat context and files conflict, follow the latest explicit user instruction and record the divergence in the handoff or operational memory.

If the spec does not already have an agent-ready ticket set, stop and recommend `$to-tickets-agentic` before creating the `/goal` handoff.

Complete this step only when the parent spec, ticket tracker path, dependency order, accepted decisions, chat-only constraints, and implementation constraints are known.

### Publishing Authority Boundary

Keep the handoff-generation turn separate from the later `/goal` execution loop.

- The handoff-generation turn creates guidance and operational memory only. It does not claim tickets, implement code, create commits, push, open PRs, or merge.
- That generation-time non-action does **not** restrict the later `/goal` loop. Do not infer that commits are forbidden merely because the handoff invocation did not explicitly request a commit.
- When the loop executes each ticket with `$ship-feature`, preserve `$ship-feature`'s normal local per-ticket commit behavior unless the user or repository explicitly prohibits commits.
- Treat commit, push, PR, and merge as distinct authorities. A local commit does not imply permission to push, open a PR, or merge.
- Record an execution-time prohibition only when it comes from an explicit user instruction or repository rule. Cite that source in the handoff instead of inventing a prohibition from silence.

### 2. Build The Execution Map

Extract the ticket graph in dependency order. Identify:

- the first unblocked ticket;
- all ticket status values currently in use;
- blocker relationships;
- required tracker updates per ticket;
- validation evidence expected by the spec or tickets;
- required skills for implementation, review, browser QA, docs, or diagnosis;
- branch, commit, push, PR, and documentation expectations.

If no explicit execution-time publishing rule exists, state the default precisely: local per-ticket commits follow `$ship-feature`; push, PR, and merge follow the user's or repository's separately established authority. Never summarize silence as “no commit was requested” or use it to disable local commits.

Do not reopen accepted architecture decisions. Record that they may be revisited only if implementation proves a concrete incompatibility.

### 3. Define The Goal Loop

Write the `/goal` objective as an executable loop, not as a vague project description.

The loop must say that each ticket is implemented with `$ship-feature`, in dependency order, and that each iteration updates:

- the ticket `Status:`;
- completed acceptance criteria;
- validation evidence;
- review evidence;
- blockers or follow-ups;
- implementation-time decisions;
- commits or PR links;
- operational memory.

State explicitly that the handoff does not implement tickets.

Phrase this as a boundary on the current handoff-generation turn, not as a restriction on the resulting `/goal`. The goal loop must retain the commit/publishing policy established under **Publishing Authority Boundary**.

### 4. Create Operational Memory

Create or update a persistent operational file beside the spec or tracker. Prefer `ongoing-implementation.md` unless the user gives a different path.

Include at minimum:

- current ticket;
- tickets completed;
- published ticket order;
- operating loop;
- ticket update protocol;
- architectural guardrails;
- useful validation commands;
- discovered files/modules;
- active risks;
- blockers;
- decisions taken during implementation;
- validation evidence log;
- commits and PRs;
- plan-vs-code divergences;
- next recommended step.

Reference source artifacts by path instead of duplicating specs, decisions, or ticket bodies.

### 5. Create The Handoff

Save the handoff document to the user's OS temporary directory unless the user explicitly asks for another destination. Also reference the persistent operational memory file from the handoff.

The handoff must include:

- focus and `/goal` objective;
- primary source paths;
- chat context used, or a note that no additional chat-only constraints were found;
- suggested skills, including `$ship-feature` and `$codebase-documentation-architect`;
- current state and first unblocked ticket;
- operating loop;
- architectural guardrails;
- tracker update rules;
- useful validation commands;
- known relevant files/modules when discovered;
- completion definition;
- explicit note that tickets are not being implemented now.

The explicit note must say that the handoff-generation turn performs no ticket or publishing actions. It must not say or imply that the later `/goal` execution cannot create local per-ticket commits unless an explicit source actually prohibits them.

Follow generic handoff hygiene: do not duplicate content already captured in specs, tickets, ADRs, or plans; redact secrets; prefer paths/URLs over copied prose.

### 6. Validate

Before finishing, check:

- the handoff file exists at the reported path;
- the operational memory file exists at the reported path;
- the ticket count and ready/current statuses are coherent;
- internal ticket links or blocker references resolve when they are local files;
- no ticket implementation work was started;
- generation-time non-action was not accidentally converted into an execution-time commit prohibition;
- any restriction on commits, pushes, PRs, or merges cites an explicit user or repository source;
- any repository docs or memory touched by the handoff pass their normal validation.

Do not invent heavy validation. Use the repository's existing docs, tracker, and validation conventions.

### 7. Report

Return the handoff path, operational memory path, what was updated, validation results, and whether any ticket set or source artifact was missing or inconsistent.

Keep the report short. The durable details belong in the handoff and operational memory.
