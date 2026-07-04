---
name: to-issues-agentic
description: Break a PRD, plan, or handoff into agent-ready implementation issues optimized for $ship-feature execution.
---

# To Issues Agentic

Turn a plan into an issue graph that agents can execute one slice at a time with `$ship-feature`.

Preserve the `$to-issues` tracer-bullet rules: prefer vertical slices, publish in dependency order, and quiz the user before publishing unless they explicitly asked to create the issues now.

## Process

### 1. Gather Sources

Read the source material the user names: PRD, plan, handoff, decision log, existing issues, comments, ADRs, and local tracker conventions. If the source is an issue reference, fetch the full body and comments.

Identify the parent artifact, issue tracker location, status convention, user stories, non-goals, accepted decisions, and validation expectations.

If the issue tracker or triage label vocabulary is missing, ask for it or run the repo's setup flow when one exists.

Complete this step only when the parent source, tracker target, constraints, and acceptance themes are known.

### 2. Explore Just Enough Code

If the current implementation is not already understood, inspect the smallest useful code and docs set. Use project domain vocabulary, respect ADRs, and identify likely seams, test commands, and risky integration points.

Avoid embedding implementation file paths in issue bodies unless a path is the source artifact, a stable tracker file, or a validation command anchor. Implementation paths go stale.

Complete this step only when issue titles and descriptions can use the project's real vocabulary without guessing.

### 3. Draft Agentic Vertical Slices

Start with tracer-bullet vertical slices: each issue should deliver a narrow but complete path through the relevant integration layers and be demoable or verifiable on its own.

Then split for agent execution. A good agentic issue should:

- fit one `$ship-feature` session;
- have one clear source of truth;
- have a narrow blast radius;
- be independently verifiable and reviewable;
- have objective acceptance criteria;
- leave no hidden architecture decision for the implementer;
- produce a committable change even when later issues remain unfinished.

Prefer early issues for prefactoring, contracts, validation packs, instrumentation, and compatibility seams when they make later vertical slices safer. Avoid broad "migrate everything" issues except final cleanup and validation.

### 4. Check Agent Readiness

Before showing the proposal, test every draft issue against this checklist:

- The first unblocked issue can start immediately.
- Every blocker is real, named, and earlier in the graph.
- The blocker graph is acyclic.
- Acceptance criteria are observable, not merely implementation intentions.
- Required validation evidence is explicit where risk is high.
- The issue does not require the agent to re-litigate accepted architecture.
- Discovery-only work has a concrete artifact as its deliverable.
- Temporary compatibility paths are paired with a later removal or validation issue.

If an issue fails the checklist, split it, merge it, or mark it blocked instead of publishing it as ready.

### 5. Quiz The User

Present the proposed breakdown as a numbered list. For each issue show:

- **Title**
- **Blocked by**
- **User stories covered** when the source has user stories
- **Why this is one agent-sized slice** when granularity is not obvious

Ask whether the granularity, dependency order, and merge/split choices are right. Iterate until the user approves. If the user explicitly asked to create/publish issues now, publish after a concise final sanity check.

### 6. Publish The Issues

Publish issues in dependency order so blockers can reference real issue identifiers. For local Markdown trackers, use sortable filenames such as `01-short-slug.md`.

Use the tracker's existing format. If no stricter format exists, use:

```md
# Issue Title

Status: ready-for-agent

## Parent

Reference the parent PRD, plan, or issue.

## What to build

Describe the end-to-end behavior or artifact this slice delivers. Do not describe a layer-by-layer task list.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- Reference blocking issue files or tickets.
```

Use `None - can start immediately.` when there are no blockers.

Apply the tracker's ready-for-agent status or triage label unless the user instructed a different state.

Do not close or modify a parent issue. Do not implement the issues while publishing them.

### 7. Add Operational Memory For Long Runs

When the issue set is intended for a long `/goal`, or the user asks for persistent implementation guidance, create or update an operational memory file beside the tracker, commonly named `ongoing-implementation.md`.

Include at minimum: current issue, completed issues, implementation-time decisions, useful validation commands, discovered files/modules, active risks, blockers, next steps, PR/commit links, and any divergence between the plan and code reality.

### 8. Exit Check

Finish only when:

- every published issue has status, parent, scope, acceptance criteria, and blockers;
- issue links or ticket references resolve;
- the first ready issue is obvious;
- the index or parent artifact points to the published issues;
- any operational memory requested by the user exists;
- no accepted architectural decision was reopened without concrete evidence.
