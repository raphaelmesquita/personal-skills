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

### 2. Build The Execution Map

Extract the ticket graph in dependency order. Identify:

- the first unblocked ticket;
- all ticket status values currently in use;
- blocker relationships;
- required tracker updates per ticket;
- validation evidence expected by the spec or tickets;
- required skills for implementation, review, browser QA, docs, or diagnosis;
- branch, commit, push, PR, and documentation expectations.

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

Follow generic handoff hygiene: do not duplicate content already captured in specs, tickets, ADRs, or plans; redact secrets; prefer paths/URLs over copied prose.

### 6. Validate

Before finishing, check:

- the handoff file exists at the reported path;
- the operational memory file exists at the reported path;
- the ticket count and ready/current statuses are coherent;
- internal ticket links or blocker references resolve when they are local files;
- no ticket implementation work was started;
- any repository docs or memory touched by the handoff pass their normal validation.

Do not invent heavy validation. Use the repository's existing docs, tracker, and validation conventions.

### 7. Report

Return the handoff path, operational memory path, what was updated, validation results, and whether any ticket set or source artifact was missing or inconsistent.

Keep the report short. The durable details belong in the handoff and operational memory.
