---
name: to-tickets-agentic
description: Break a plan, spec, legacy PRD, handoff, or conversation into an agent-executable graph of tracer-bullet tickets, each sized for a fresh context and explicit about blocking edges, constraints, acceptance criteria, and validation. Use when AI agents must implement the tickets autonomously, including through $ship-feature or a long-running goal.
---

# To Tickets Agentic

Create the same ticket graph as `$to-tickets`, with a stricter contract for autonomous implementation. Every ticket must be safe for a fresh agent to pick from the **frontier** without recovering hidden context from the author.

The tracker and triage vocabulary should already be configured. Run `/setup-matt-pocock-skills` when they are missing.

## Process

### 1. Gather the source of truth

Read the relevant conversation and every named source: plan, spec, handoff, issue body and comments, ADR, decision log, and tracker convention. Treat an existing PRD as a legacy spec without requiring it to be renamed.

Identify the parent artifact, accepted decisions, non-goals, compatibility constraints, validation expectations, tracker target, and ready-for-agent status or label.

Complete this step only when those inputs are known or their absence is explicitly recorded as a ticket constraint.

### 2. Explore enough of the codebase

When the implementation is not already understood, inspect the smallest useful set of code and documentation. Use the project's domain language, respect relevant ADRs, find stable verification surfaces, and look for prefactoring that makes later changes easier.

Complete this step only when ticket scopes can use the project's real vocabulary and avoid leaving architectural discovery to the implementing agent.

### 3. Draft tracer-bullet tickets

Make each ticket a narrow but complete vertical slice through every relevant layer. A completed ticket must be independently demoable or verifiable, committable while later tickets remain open, and small enough for one fresh agent context.

Create prefactoring, contract, compatibility-seam, instrumentation, or discovery tickets first only when they unlock later vertical slices. A discovery ticket must deliver a durable decision artifact. Pair every temporary compatibility path with the ticket that removes it.

Treat a wide mechanical refactor as an expand-contract sequence:

1. Expand by adding the new form beside the old.
2. Migrate call sites in batches that can remain green independently.
3. Contract by removing the old form after every migration ticket completes.

When migration batches cannot remain green alone, use an integration branch and make them all block a final integrate-and-verify ticket.

For every ticket, declare only genuine blocking edges. The graph must be acyclic, ordered with blockers first, and expose a non-empty frontier unless external work blocks the entire plan.

### 4. Enforce the agent contract

Audit every draft ticket against all of these conditions:

- **What to build** states one end-to-end outcome rather than a layer-by-layer task list.
- **Context and constraints** link the source of truth and state accepted decisions, invariants, and compatibility requirements needed in a fresh context.
- **Acceptance criteria** are objective, observable, and exhaustive for the slice.
- **Validation** names the evidence that proves the behavior, using established repository commands or surfaces when known.
- **Boundaries** make material non-goals and preserved contracts explicit.
- **Blocked by** names every genuine prerequisite and no merely convenient predecessor.
- The implementation fits one agent context, has a narrow blast radius, and leaves no unresolved product or architecture choice.

Split, merge, clarify, or block any draft that fails the audit. Mark a ticket ready for an agent only after every condition passes.

Avoid implementation file paths and working code snippets because they age quickly. Stable source-artifact paths and validation commands are useful. A decision-rich prototype excerpt may be included when prose would lose precision; identify it as prototype-derived and trim it to the accepted decision.

### 5. Quiz the user

Present the proposed graph as a numbered list. For each ticket show:

- **Title**
- **Blocked by**
- **What it delivers**
- **Why it fits one agent context**, when the sizing is not self-evident

Ask whether the granularity, blocking edges, and split or merge choices are correct. Iterate until the user approves. An explicit request to publish an already approved breakdown counts as approval.

List any unresolved product or architecture choice surfaced during drafting and obtain a decision before publication. Keep the affected ticket blocked when the user intentionally defers that choice.

### 6. Publish in dependency order

Publish blockers first so downstream tickets can reference real identifiers.

- **Local tracker:** create one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order. Put blocker numbers and titles in `Blocked by`.
- **Real tracker:** create one issue per ticket and use native blocking or sub-issue relationships when available; otherwise reference blocking issue identifiers in the body.

Apply the configured `ready-for-agent` status or label unless the user chose another state. Preserve the parent spec or other source artifact unchanged.

Use this template for local tickets:

```md
# <NN> — <Ticket title>

Status: <configured tracker value for ready-for-agent>
Blocked by: <ticket numbers/titles, or "None — can start immediately">

## Parent

<Source artifact reference, when one exists>

## What to build

<One end-to-end outcome from the user's perspective>

## Context and constraints

<Accepted decisions, invariants, and compatibility requirements needed in a fresh context>

## Acceptance criteria

- [ ] <Observable criterion>

## Validation

- <Required evidence or established command>

## Boundaries

- <Material non-goal or contract to preserve>
```

For a real tracker, use the same sections without the local number in the title. Omit `Parent` only when no parent source exists; keep every other section, writing `None identified` where the section is intentionally empty.

### 7. Verify publication

Finish only when:

- every approved ticket exists exactly once and its references resolve;
- every ticket passes the agent contract and has the configured ready state;
- native and textual blocking edges agree, and the graph is acyclic;
- the frontier is obvious;
- wide refactors have complete expand, migrate, and contract coverage;
- the parent artifact remains unchanged.

Hand each frontier ticket independently to `$ship-feature` or the configured implementation flow. Clear context between tickets so the ticket itself remains the implementation contract.
