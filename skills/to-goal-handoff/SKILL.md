---
name: to-goal-handoff
description: Adapt a $to-tickets-agentic execution package into a durable /goal handoff and compact operational memory. Use when a coordinated feature graph is ready to run through repeated $implement-slice iterations followed by one $finalize-feature gate.
---

# To Goal Handoff

Initialize a long-running `/goal` from an existing execution package. Treat the package as authoritative planning output; adapt it without reconstructing the graph or reinterpreting the spec.

This generation turn creates guidance and memory only. The resulting goal performs implementation and finalization later.

## 1. Load And Validate The Package

Read current chat context for the latest objective, explicit constraints, destination paths, branch expectations, and publishing authority. Then read:

- `.scratch/<feature-slug>/execution-plan.md`;
- its parent source;
- every implementation and finalization node;
- relevant ADRs or decision artifacts linked by the plan;
- existing operational memory, when present.

If the execution plan or agent-ready graph is missing, stop and recommend `$to-tickets-agentic`.

Validate without redesigning:

- the graph is acyclic, its initial frontier contains only `ready` implementation nodes, and dependency-bound nodes are `waiting`;
- every implementation node names exactly `Execution: $implement-slice`;
- exactly one terminal node names `Execution: $finalize-feature` and depends on every implementation leaf;
- the acceptance matrix defines each feature criterion once under a unique stable ID and maps each ID reciprocally to contributing nodes and final evidence;
- canonical lifecycle and tracker mappings distinguish dependency `waiting` from actual `blocked`;
- base branch, immutable base revision, exact feature branch, and commit, push, PR, and merge authority are explicit;
- change-producing work with `commit: false` also has `push: false`, `pr: false`, and `merge: false`;
- chat-only constraints are recorded as a divergence when they change the package.

Reject legacy packages that assign `$ship-feature` or another runner to implementation nodes. Recommend regenerating or explicitly migrating them with `$to-tickets-agentic`, including economical checks, downstream contracts, stable acceptance-criterion IDs, and final-QA mappings.

Complete this step only when the first implementation node and terminal finalization conditions are unambiguous.

## 2. Establish The Publishing Boundary

Keep the handoff-generation turn separate from goal execution:

- generation creates the handoff and operational memory;
- `$implement-slice` creates scoped local commits during execution;
- `$finalize-feature` is the sole push, PR, and merge phase;
- merge eligibility begins only after finalization succeeds;
- explicit user or repository rules override default local commits or publication authority.

Treat commit, push, PR, and merge as separate values. Cite the source of every prohibition or authorization.

## 3. Encode The Feature-Branch Bootstrap

Write this bootstrap as the first phase of the durable `/goal` objective; do not execute branch operations during handoff generation:

1. verify the recorded immutable base revision belongs to the recorded base branch;
2. create the exact feature branch at that revision when it does not exist;
3. otherwise switch to the existing feature branch and verify the base revision is its ancestor;
4. block when HEAD is detached, another worktree owns the branch, or working-tree changes make the switch unsafe.

Require the later goal to complete bootstrap only when HEAD is attached to the exact planned feature branch at valid base ancestry.

## 4. Define The Goal Loop

Write the `/goal` objective as this executable loop:

1. Select the first `ready` implementation node in dependency order.
2. Run `$implement-slice` with the node, execution plan, branch state, and compact operational memory; it owns the transitions to `in-progress` and then `implemented` or `blocked`.
3. When commit authority is enabled, require a scoped commit. When it is explicitly disabled, require a recorded no-commit rationale and scoped diff evidence. In both cases, verify that the node and memory contain implementation evidence, downstream assumptions, divergences, and one checkpoint result of `run|skipped`.
4. Consume the recorded checkpoint result without executing another check.
5. Recompute the frontier, promote every newly dependency-clear implementation node from `waiting` to `ready` in the tracker and operational memory, and select only `ready` nodes.
6. Continue until every implementation node is `implemented`.
7. Promote the terminal node from `waiting` to `ready`, then `in-progress`.
8. Run the single `$finalize-feature` node over the aggregate diff and acceptance matrix.
9. Require its complete structured result. Finish only on `delivery_status: complete` with `quality_status: clean` or policy-accepted `clean-with-waiver`; treat a missing or incoherent field as `blocked`. A failure before merge sets the terminal node to `blocked`; a non-source-controlled tracker failure after merge becomes a follow-up and leaves the successful terminal verdict unchanged.

Feature-wide QA, broad test suites, browser acceptance walkthroughs, and independent review occur at finalization. Per-node checks remain economical and deterministic.

## 5. Create Compact Operational Memory

Create or update `ongoing-implementation.md` beside the execution plan unless the user gives another path. Keep it as a delta log and index, not a copy of sources.

Include:

- execution-plan, parent-source, tracker, repository, base-revision, and branch references;
- current node, frontier, implemented nodes, and terminal-node state;
- canonical state mappings;
- downstream contracts and implementation-time assumptions still relevant;
- useful economical commands and feature-wide finalization commands;
- discovered files or modules;
- checkpoint decisions and evidence;
- blockers, risks, durable decisions, and plan-versus-code divergences;
- local commits and publication state;
- next recommended node.

Record final verification and independent-review evidence once at feature level after `$finalize-feature`, not once per implementation node.

## 6. Create The Handoff

Save the handoff in the user's OS temporary directory unless another destination is requested. Reference the durable execution plan and operational memory instead of copying their content.

Include:

- `/goal` objective and completion criterion;
- repository, base revision, branch, and publishing authority;
- execution-plan, source, tracker, and memory paths;
- first `ready` implementation node;
- the four-step feature-branch bootstrap before node selection;
- the operating loop and canonical lifecycle;
- architectural guardrails and current divergences;
- checkpoint activation rule;
- finalization-node contract;
- explicit note that this generation turn implements, commits, pushes, and merges nothing.

Suggest `$implement-slice`, `$finalize-feature`, and `$codebase-documentation-architect` when durable repository memory must change. `$ship-feature` remains available for independent one-feature delivery but is not an implementation-node runner in this coordinated loop.

## 7. Validate And Report

Finish only when:

- the handoff and operational-memory files exist at the reported paths;
- every referenced source and local blocker resolves;
- ticket counts, frontier, lifecycle, and terminal-node dependencies agree;
- the handoff defers integrated QA and independent review to the terminal node;
- the handoff embeds the feature-branch bootstrap and generation executed no branch operation;
- checkpoint wording uses the downstream-rework rule;
- publication authority matches explicit user and repository sources;
- no ticket implementation or publication action occurred during generation;
- modified repository docs pass their normal validation.

Report the handoff path, operational-memory path, first node, terminal node, publishing policy, validation results, and any missing or inconsistent source.
