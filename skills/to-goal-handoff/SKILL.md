---
name: to-goal-handoff
description: Create a goal-ready handoff from a PRD and ordered issues for a /goal loop that executes each issue with $ship-feature and maintains operational memory.
---

# To Goal Handoff

Create a specialized handoff for a long-running `/goal` that will implement every issue in a PRD-backed issue set.

This is not a generic summary handoff. It must produce an actionable execution guide plus persistent operational memory so a fresh agent can pick the first unblocked issue, run `$ship-feature`, update trackers, and continue without rediscovery.

## Process

### 1. Gather Sources

Read the current chat context first. Extract the user's latest objective, explicit constraints, named skills, destination paths, branch/commit expectations, and any implementation-loop rules that may not yet be persisted.

Then read the sources the user names: PRD, issue index, issue directory, decision log, ideal-state document, problem statement, open questions, ADRs, existing handoffs, and existing operational memory.

Use chat context as an auxiliary source, not a replacement for persisted artifacts. If chat context and files conflict, follow the latest explicit user instruction and record the divergence in the handoff or operational memory.

If the PRD does not already have an agent-ready issue set, stop and recommend `$to-issues-agentic` before creating the `/goal` handoff.

Complete this step only when the parent PRD, issue tracker path, dependency order, accepted decisions, chat-only constraints, and implementation constraints are known.

### 2. Build The Execution Map

Extract the issue graph in dependency order. Identify:

- the first unblocked issue;
- all issue status values currently in use;
- blocker relationships;
- required tracker updates per issue;
- validation evidence expected by the PRD or issues;
- required skills for implementation, review, browser QA, docs, or diagnosis;
- branch, commit, push, PR, and documentation expectations.

Do not reopen accepted architecture decisions. Record that they may be revisited only if implementation proves a concrete incompatibility.

### 3. Define The Goal Loop

Write the `/goal` objective as an executable loop, not as a vague project description.

The loop must say that each issue is implemented with `$ship-feature`, in dependency order, and that each iteration updates:

- the issue `Status:`;
- completed acceptance criteria;
- validation evidence;
- review evidence;
- blockers or follow-ups;
- implementation-time decisions;
- commits or PR links;
- operational memory.

State explicitly that the handoff does not implement issues.

### 4. Create Operational Memory

Create or update a persistent operational file beside the PRD or tracker. Prefer `ongoing-implementation.md` unless the user gives a different path.

Include at minimum:

- current issue;
- issues completed;
- published issue order;
- operating loop;
- issue update protocol;
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

Reference source artifacts by path instead of duplicating PRDs, decisions, or issue bodies.

### 5. Create The Handoff

Save the handoff document to the user's OS temporary directory unless the user explicitly asks for another destination. Also reference the persistent operational memory file from the handoff.

The handoff must include:

- focus and `/goal` objective;
- primary source paths;
- chat context used, or a note that no additional chat-only constraints were found;
- suggested skills, including `$ship-feature` and `$codebase-documentation-architect`;
- current state and first unblocked issue;
- operating loop;
- architectural guardrails;
- tracker update rules;
- useful validation commands;
- known relevant files/modules when discovered;
- completion definition;
- explicit note that issues are not being implemented now.

Follow generic handoff hygiene: do not duplicate content already captured in PRDs, issues, ADRs, or plans; redact secrets; prefer paths/URLs over copied prose.

### 6. Validate

Before finishing, check:

- the handoff file exists at the reported path;
- the operational memory file exists at the reported path;
- the issue count and ready/current statuses are coherent;
- internal issue links or blocker references resolve when they are local files;
- no issue implementation work was started;
- any repository docs or memory touched by the handoff pass their normal validation.

Do not invent heavy validation. Use the repository's existing docs, tracker, and validation conventions.

### 7. Report

Return the handoff path, operational memory path, what was updated, validation results, and whether any issue set or source artifact was missing or inconsistent.

Keep the report short. The durable details belong in the handoff and operational memory.
