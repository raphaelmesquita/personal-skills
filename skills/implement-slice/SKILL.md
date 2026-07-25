---
name: implement-slice
description: Implement one slice inside an established feature delivery flow, producing a scoped local commit and compact evidence while deferring feature-wide QA, independent review, and publication to $finalize-feature. Use only when $ship-feature or a coordinated /goal delegates an implementation slice.
---

# Implement Slice

Implement exactly one source-backed slice and leave the feature branch ready for the next slice. This skill makes an implementation claim, not a feature-quality claim. `$finalize-feature` owns integrated QA, independent review, and publication.

## Inputs

Require:

- the ticket, request, or other source of truth;
- the repository, recorded base revision, and exact planned feature branch;
- objective implementation criteria and boundaries;
- the downstream contract, when later slices depend on this one;
- economical checks and final-QA contribution, preferably from the execution plan;
- current branch plus tracker and operational-memory state when those artifacts exist.

For a coordinated goal, require the execution-plan path. For standalone `$ship-feature`, treat its source as a one-slice plan.

Inspect repository instructions, `git status --short`, relevant code, and unrelated working-tree changes before delegation. Verify that HEAD is attached to the exact planned feature branch and that the recorded base revision is an ancestor of HEAD. A detached HEAD, branch mismatch, or invalid base ancestry blocks the slice before delegation or commit.

Before delegation, set the canonical node state to `in-progress`. Persist it in the ticket and operational memory when those artifacts exist; otherwise keep it in the slice handoff. `$implement-slice` owns the current node's updates; the goal orchestrator owns graph-level frontier transitions.

## Implementation Delegation

Delegate implementation to `$delegate-antigravity` with model `Gemini 3.6 Flash (Medium)` unless the user requests another model. Supply only task-local context:

- source of truth and execution-plan paths;
- workspace, branch, and current state;
- concrete implementation criteria, downstream contract, invariants, edge cases, and non-goals;
- likely files or search targets;
- tests to add or update;
- economical verification commands;
- a compact output contract.

State that the implementation requires edits and may use terminal, internet, or tools in the source-controlled workspace.

Treat Antigravity as the implementer only. Require it to preserve unrelated changes, edit only the slice, and leave commits, pushes, PR or tracker updates, operational-memory updates, and agent spawning to the orchestrator.

If Antigravity fails because of quota, model availability, timeout, empty output, missing or malformed handoff, or another runtime error, run exactly one `implementer` custom agent. Do not retry Antigravity or silently take over the implementation.

The fallback brief must:

- permit edits in the source-controlled workspace;
- preserve unrelated changes and limit edits to the slice;
- leave commits, pushes, PR or tracker updates, operational-memory updates, and agent spawning to the orchestrator;
- keep business validation in the authoritative layer and preserve public contracts unless the source changes them;
- require relevant tests and economical local verification;
- report `status: complete|blocked`, result, files changed, commands and results, implementation-criteria coverage, residual risks, and next steps.

The fallback `implementer` role must come from the central Codex agent configuration. If it is unavailable, or neither implementation attempt produces a complete handoff consistent with the diff, report the slice as blocked.

## Integrate The Slice

Read the implementation handoff and inspect the resulting diff. Confirm that:

- every changed file belongs to the slice;
- implementation criteria and downstream contract are reflected in the code;
- tests were added or updated where the slice introduces testable behavior;
- durable behavior or workflow changes update the appropriate documentation or memory;
- no unrelated working-tree change was overwritten.

Resolve small integration defects within the slice. A missing or contradictory essential requirement blocks the slice instead of expanding it by assumption.

## Economical Checks

Run the cheapest deterministic checks that keep the branch useful for subsequent work. Prefer targeted compilation, type checking, linting, syntax or schema validation, and fast tests for the touched surface.

Tests are implementation artifacts: create them while the behavior is fresh, even when their broad execution belongs to finalization.

Feature-wide suites, browser QA, acceptance walkthroughs, and independent review belong to `$finalize-feature`.

### Dependency Checkpoint

Run one focused checkpoint before dependent slices only when all conditions hold:

1. later slices will build directly on the implemented interface or behavior;
2. implementation exposed a concrete uncertainty about that dependency;
3. resolving it now is likely to avoid substantial downstream rework;
4. one small check can resolve it much more cheaply now than during finalization.

Validate only that uncertainty. Importance, sensitivity, ticket size, or general confidence do not activate a checkpoint. When the benefit is unclear, record the assumption and defer the check.

## Record And Commit

Update the ticket and operational memory when present. For a standalone source without those artifacts, record the same evidence in the slice handoff:

- canonical state `implemented`, never `verified` or `complete`;
- implementation criteria covered;
- files changed and tests added or updated;
- economical checks and results;
- downstream contract and assumptions;
- checkpoint decision and rationale;
- blockers, divergences, risks, and follow-ups.

If implementation blocks, set canonical state `blocked`, preserve the evidence and exact blocker, and create no slice commit.

Stage only files belonging to the slice and create one concise local commit unless an explicit user or repository rule prohibits commits. Leave push, PR, merge, feature-wide QA, and independent review to `$finalize-feature`.

Return a compact handoff:

```yaml
status: implemented|blocked
source: <ticket or source reference>
commit: <hash or "not created">
files_changed: [...]
implementation_criteria: [...]
tests_added_or_updated: [...]
checks: [...]
downstream_contract: [...]
checkpoint:
  result: run|skipped
  rationale: <why>
risks_or_follow_ups: [...]
next_step: <next ticket or blocker>
```
