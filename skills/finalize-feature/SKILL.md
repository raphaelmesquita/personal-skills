---
name: finalize-feature
description: Finalize a fully implemented feature as one integrated change through feature-wide verification, Codex-owned QA, independent review, corrections, tracker completion, and authorized publication. Use after all slices in a coordinated /goal are implemented or when $ship-feature reaches its finalization phase.
---

# Finalize Feature

Produce the quality and publication claim for one complete feature. Run this expensive gate once over the aggregate behavior and diff.

## Finalization Gate

Require:

- the spec, request, or other feature-level source of truth;
- the base revision and feature branch;
- the implementation commits, or recorded no-commit rationale with scoped diff evidence for each slice, plus the final aggregate diff;
- every planned implementation slice in canonical state `implemented`;
- the execution plan and acceptance matrix for a coordinated goal;
- a complete authority matrix for commit, push, PR, and merge.

For standalone `$ship-feature`, build a compact acceptance matrix that assigns each criterion one stable ID before verification. For a coordinated goal, use the published stable IDs and reciprocal mappings, reconciling only implementation-time decisions or plan-versus-code divergences.

For change-producing work, `commit: false` requires `push: false`, `pr: false`, and `merge: false`. Reject an incompatible authority matrix before running finalization.

Inspect repository instructions, `git status --short`, the aggregate diff, implementation evidence, and unrelated working-tree changes. Begin finalization only when every required slice is implemented and the feature scope is coherent.

## Feature-Wide Verification

Choose the relevant full checks from repository instructions and the changed surface. Examples include:

- frontend build, existing frontend tests, and browser flows;
- targeted plus contract tests for backend or API work;
- catalog, link, render, or artifact validation;
- backend tests, frontend build, and integrated behavior for full-stack changes.

Use the acceptance matrix to account for every feature criterion. Required failing checks block publication.

## Orchestrator QA

Codex must personally exercise the integrated behavior through its most relevant surface. Validate:

- every acceptance-matrix row;
- interactions across slices;
- negative and edge cases required by the source;
- preserved contracts and likely regression surfaces;
- the feature as a user experiences it, not only its internal implementation.

Keep corrections within the feature scope and preserve unrelated changes. Rerun affected checks after each correction.

## Independent Review

After QA is clean, ask `$delegate-antigravity` for a read-only code review with model `Claude Opus 4.6 (Thinking)`. Provide the feature source, repository, base revision, aggregate diff commands, acceptance matrix, verification results, and implementation-time decisions. Require inspection-only commands and a non-empty result of `clean`, `findings`, or `blocked`.

Prioritize bugs, regressions, missing tests, cross-slice contract failures, data loss, security or privacy issues, boundary violations, and unsafe assumptions.

If the Opus run fails or produces no usable review evidence:

1. use usable findings from its transcript when available;
2. otherwise run one read-only Antigravity fallback with model `Gemini 3.1 Pro (High)` and a checklist-style prompt;
3. if that also fails, run exactly one read-only `code-reviewer` custom agent.

The `code-reviewer` brief must include the source, base revision, exact aggregate diff, in-scope paths, acceptance matrix, and verification evidence. It must forbid edits, commits, pushes, PR or tracker updates, and agent spawning. Require:

- `status: clean|findings|blocked`;
- `verdict: APPROVE|REQUEST_CHANGES|COMMENT`;
- files inspected and commands/results;
- actionable findings by severity with file and line;
- residual risks and next steps.

Enforce `APPROVE => clean`, `REQUEST_CHANGES => findings`, and `COMMENT => clean` only without actionable findings. Missing essential inputs mean `blocked`. The role must come from the central Codex agent configuration.

Unavailable independent review blocks clean finalization and publication for every risk class. Continue only when the user explicitly waives independent review after the failure is known. Record `review: waived`, the reason, the unavailable attempts, and the accepted residual risk.

## Correct And Recheck

Address valid findings directly and record false positives or out-of-scope findings. Rerun:

- checks affected by each correction;
- the final integrated smoke path;
- the full feature-wide gate when a correction changes a cross-slice contract or invalidates earlier evidence.

Set `quality_status` to `clean` only when the acceptance matrix, required verification, orchestrator QA, and independent review have coherent evidence. An explicit review waiver produces `clean-with-waiver`; it permits publication and merge eligibility only when the publishing policy accepts that named residual risk.

## Record Verification

Update the source spec, tickets, and operational memory when those artifacts exist:

- promote implemented slices to `verified`;
- record final verification and review evidence once at feature level;
- capture corrections, decisions, remaining risks, follow-ups, commits, PRs, and plan-versus-code divergences.

Map canonical lifecycle states to native tracker values when available. Otherwise record them in the ticket body, a tracker comment, or operational memory without inventing unsupported tracker states.

For a standalone request without tracker or durable-memory artifacts, keep lifecycle and evidence in the implementation handoff, finalization handoff, and final report. Do not create repository tracking files solely to satisfy this skill.

## Publish

Review the final diff from the recorded base revision. Stage only finalization corrections and scoped tracker or documentation changes, then create a concise finalization commit when needed.

Treat commit, push, PR, and merge as separate authorities:

- `$ship-feature` authorizes its normal local commits and push by default;
- a coordinated goal follows the execution plan's publishing policy;
- merge requires explicit user authority and known passing required checks.

Execute source-control publication in this order:

1. persist all code, documentation, and source-controlled tracker changes required before delivery;
2. commit and push them as authorized;
3. open or update the PR and obtain required checks as authorized;
4. confirm the pre-merge success gate: `quality_status` is `clean`, or accepted `clean-with-waiver`; all required commits are pushed; all required checks pass; every pre-merge tracker obligation reached its expected state; and no source-controlled bookkeeping remains;
5. merge as the final source-control action when authorized.

No file edit, commit, or push follows merge. After merge, update only non-source-controlled trackers or operational systems.

## Complete The Goal

After every publication action required by the authority matrix succeeds, promote verified slices and the terminal node to `complete`. When the policy requires no external publication, successful local finalization satisfies this condition.

Before the final permissible commit, persist only lifecycle states already earned. Whenever `complete` depends on a later push, PR, merge, or other publication action, leave source-controlled records at `verified` and record `complete` afterward only in non-source-controlled tracking state. Report that representation explicitly.

If publication fails before merge, leave slices `verified`, set the terminal node to `blocked`, record the failed action, and do not merge.

A non-source-controlled tracker failure after merge becomes an operational follow-up and does not retroactively change the finalization verdict or trigger another source-control action.

## Report

Report:

- integrated behavior delivered;
- feature-wide verification and results;
- orchestrator QA and acceptance-matrix coverage;
- independent review, waiver when applicable, and addressed findings;
- implementation and finalization commits;
- branch, push, PR, and merge status;
- residual risks or follow-ups;
- any skipped gate, its exact reason, and the resulting publication decision.

Return this machine-consumable result:

```yaml
quality_status: clean|clean-with-waiver|blocked
delivery_status: complete|blocked
source: <feature source>
base_revision: <revision>
acceptance_coverage:
  covered: [<criterion IDs>]
  missing: [<criterion IDs>]
verification:
  - command: <command>
    status: passed|failed
qa: passed|blocked
review:
  outcome: clean|findings|waived|blocked
  findings_resolution: not-applicable|all-resolved|unresolved
  evidence: <review or waiver>
tracker_states:
  - artifact: <tracker or memory reference>
    representation: source-controlled|non-source-controlled
    required_phase: pre-merge|post-merge|none
    state: verified|complete|blocked|not-applicable
    follow_up: <action or "none">
publication:
  commit: succeeded|skipped|blocked
  push: succeeded|skipped|blocked
  pr: succeeded|skipped|blocked
  merge: succeeded|skipped|blocked
commits: [<hashes>]
residual_risks: [...]
next_action: <action or "none">
```

Enforce result consistency:

- `quality_status: clean` requires no missing criterion IDs, passed verification and QA, and review outcome `clean` or `findings` with `all-resolved`;
- `quality_status: clean-with-waiver` has the same requirements with review outcome `waived`;
- unresolved findings, failed quality evidence, or an incoherent quality enum maps `quality_status` to `blocked`;
- `delivery_status: complete` requires accepted quality status, every authorized publication action succeeded, and every `pre-merge` tracker obligation reached its expected state;
- a failed required publication action or pre-merge tracker obligation maps `delivery_status` to `blocked`;
- a non-source-controlled `post-merge` tracker follow-up remains explicit without changing an otherwise `complete` delivery status.
