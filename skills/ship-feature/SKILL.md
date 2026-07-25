---
name: ship-feature
description: Ship one scoped feature end-to-end by composing implementation with feature-wide QA, independent review, corrections, commit, and push. Use for /ship-feature or a ticket, request, spec, or legacy PRD that should be delivered independently; merge only when explicitly requested.
---

# Ship Feature

Ship one independent feature through the complete delivery contract. Preserve unrelated worktree changes and follow repository instructions.

Default mode creates scoped local commits and pushes the feature branch. Merge mode requires an explicit request such as `/ship-feature --merge`.

## 1. Establish The Feature

Identify the user request, ticket, spec, or legacy PRD as the source of truth. Inspect repository instructions, branch, `git status --short`, relevant code and docs, acceptance criteria, and publication authority.

Create or switch to an appropriate feature branch when requested or required by repository practice.

Treat the source as a one-slice feature:

- implementation criteria come from its acceptance criteria;
- its observable behavior becomes the final acceptance matrix;
- its current base revision anchors the final aggregate diff;
- its default authority matrix is `commit: true`, `push: true`, `pr: false`, `merge: false`;
- explicit user instructions override individual authority values.

For a change-producing run, `commit: false` requires `push: false`, `pr: false`, and `merge: false`. Stop before implementation when the authority matrix is incompatible.

Complete this step only when scope, base revision, branch, verification surfaces, and merge mode are known.

## 2. Implement The Slice

Run `$implement-slice` with the feature source and standalone context. Require a usable `implemented` handoff. When commit authority is enabled, require a scoped local commit; otherwise require a recorded no-commit rationale and scoped diff evidence.

If implementation is blocked, stop. Report the blocking attempt, verification evidence, working-tree state, and that finalization and publication did not run.

## 3. Finalize The Feature

Run `$finalize-feature` over the one-slice feature. Pass:

- the original source and acceptance matrix;
- the recorded base revision plus the implementation commit or no-commit scoped-diff evidence;
- the aggregate diff and verification surfaces;
- the complete authority matrix, including explicit `false` values.

`$finalize-feature` owns feature-wide verification, Codex QA, independent review, corrections, tracker completion, final publication, and the final report.

Require its structured `quality_status` and `delivery_status`. Report `blocked` instead of inferring success when any required result field is absent, incoherent, or does not satisfy the authority matrix.

## Coordinated Goals

A multi-ticket feature goal uses `$implement-slice` for each implementation node and `$finalize-feature` once after all nodes are implemented. It does not weaken or partially execute `$ship-feature`; standalone `$ship-feature` always retains the complete delivery contract.
