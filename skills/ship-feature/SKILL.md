---
name: ship-feature
description: "Ship a scoped feature end-to-end: delegate implementation, run Codex-owned QA, obtain independent review, address findings, commit/push, and optionally merge. Use for /ship-feature or requests to ship a feature from a spec or legacy PRD, ticket, or direct request."
---

# Ship Feature

## Scope

Use this skill for one scoped feature or spec-backed change. Existing PRDs are legacy specs and remain valid sources of truth. Keep the slice narrow, preserve unrelated worktree changes, and follow repository instructions before this workflow.

Default mode is commit and push. Merge only when the user explicitly asks for merge mode, for example `/ship-feature --merge`.

## Custom Agent Prerequisite

Use these exact custom agent roles from the central Codex agent configuration:

- `implementer`
- `code-reviewer`

These roles are defined by TOMLs under `$CODEX_HOME/agents` (or `~/.codex/agents` when `CODEX_HOME` is unset). Their centralized TOMLs own the model, reasoning effort, sandbox, standing behavior, and generic output contract. This skill supplies only task-local context to those roles; this repository does not install or duplicate these two agent configurations. If a required role is unavailable, report the setup blocker and stop that fallback path; do not substitute a generic subagent.

The spawn brief owns only task-local facts: source of truth, workspace, current state, scope, acceptance criteria or invariants, relevant files, verification evidence or commands, and task-specific output requirements.

## Non-Negotiable Fallbacks

Do not skip delegation fallback gates.

- If `$delegate-antigravity` implementation fails because of quota, model availability, timeout, empty output, missing handoff, malformed handoff, or another runtime error, run exactly one `implementer` custom agent with task-local context, the same acceptance criteria, and explicit permission to edit the source-controlled workspace.
- Treat the implementation fallback subagent as the implementation path. Integrate and inspect its work before verification.
- If no usable implementation handoff exists after the Antigravity attempt and fallback subagent, stop and report the implementation as blocked. Do not silently switch to local implementation.
- If Opus review and the Gemini Antigravity review fallback both fail to produce usable review evidence, run exactly one `code-reviewer` custom agent before treating independent review as unavailable.

## Preflight

1. Identify the source of truth: current user request, spec, ticket, or design doc.
2. Inspect repo instructions, current branch, `git status --short`, and relevant docs/code.
3. State assumptions and the implementation/verification plan.
4. If unrelated dirty files touch the target area, work with them carefully; ask only when they make the task unsafe or impossible.
5. Create or switch to an appropriate feature branch when requested or when repo practice requires it.

## Delegation Context

Use task-local context for all delegated workers: objective, source of truth, workspace path, current state, constraints, required work, verification, and output contract. Exclude the `ship-feature` orchestration process, phase names, planned gates, prior conclusions, expected findings, and downstream validators.

## Implement

Delegate implementation to `$delegate-antigravity` instead of editing directly.

1. Create a precise implementation handoff for `$delegate-antigravity` with the source of truth, workspace path, branch/worktree state, constraints, expected files or areas, and required verification.
2. Tell `$delegate-antigravity` the implementation requires edits and may need terminal, internet, or tool use in the source-controlled workspace.
3. Tell `$delegate-antigravity` to use model `Gemini 3.5 Flash (Medium)` for implementation unless the user requests another model. Because the implementer is lower-capability than the orchestrator, make the handoff unusually explicit: include concrete acceptance criteria, relevant files or search targets, invariants, edge cases, examples, commands to run, and known non-goals.
4. If `$delegate-antigravity` implementation fails because of quota, model availability, timeout, empty output, missing handoff, malformed handoff, or another runtime error, do not retry Antigravity and do not implement locally. Run one `implementer` custom agent using task-local context, the same acceptance criteria, and explicit permission to edit the source-controlled workspace.
5. The fallback `implementer` task-local brief must explicitly state: preserve unrelated working-tree changes; edit only the feature scope; do not commit, push, open or update a PR, modify a tracker, or spawn agents; and report `blocked` when an essential requirement is missing or contradictory. Require the implementer to make the smallest change that satisfies the spec or request, keep rule/business validation in the authoritative layer, preserve public contracts unless explicitly changed, update docs/memory when durable behavior or workflow changes, and run relevant local verification.
6. Require the fallback `implementer` handoff to contain `status: complete|blocked`, a result, files changed, verification commands with results, coverage of each acceptance criterion, residual risks, and next steps. Read the usable handoff and inspect the resulting diff before continuing. The gate passes only when the status is one of those values and all required fields are present and consistent with the diff; a blocked status, missing/contradictory essential requirement, or missing/malformed handoff blocks the implementation path. If both implementation attempts produce missing, blocked, or diff-inconsistent handoffs, stop and report blocked instead of taking over implementation locally.
7. Treat the delegated implementer as the implementer only; Codex remains responsible for final verification, QA, corrections, review delegation, tracker updates, commit, push, and final report.

## Verification Gate

Choose commands from repo docs and the touched surface. Do not invent heavy test coverage when targeted checks are enough.

Common examples:

- Frontend change: build, relevant browser QA, and any existing frontend tests.
- Backend/API change: targeted pytest plus contract tests.
- Catalog/docs change: catalog/link validation scripts.
- Full-stack behavior change: backend tests, frontend build, and browser QA.

Do not continue to commit while required local verification is failing.

## Orchestrator QA

After implementation and first verification, Codex must personally QA the behavior against the source of truth and user-visible acceptance criteria. Do not use a QA subagent for this gate.

Build a short acceptance checklist from the spec or request, then exercise the changed behavior directly through the most relevant surface: tests, CLI commands, API calls, browser flows, rendered artifacts, or file inspection. Include negative or edge cases when they are part of the requested behavior or likely regression surface.

Address valid QA findings yourself. Keep fixes scoped, preserve unrelated worktree changes, and rerun affected verification after fixes. Record any out-of-scope findings for the final report instead of expanding the slice silently.

## Antigravity Review

After Codex QA is clean, obtain independent review before commit/push.

1. Ask `$delegate-antigravity` for a read-only code review with model `Claude Opus 4.6 (Thinking)`. Tell `$delegate-antigravity` the review must not modify the workspace; any active commands must be inspection-only.
2. Use task-local context: source of truth, repo path, final diff context or commands to inspect the diff, relevant verification results, and output contract.
3. Ask for code-review findings prioritizing bugs, regressions, missing tests, boundary violations, data loss, security or privacy issues, and unsafe assumptions.
4. Accept the review only when the handoff is non-empty and clearly reports `clean`, `findings`, or `blocked`. For the Codex `code-reviewer` fallback, also validate every required field and the verdict/status mapping from step 7; a missing essential input or incoherent status/verdict is `blocked`, not a clean review.
5. If the Opus run fails because of quota, model availability, timeout, empty output, malformed handoff, or another runtime error, do not retry Opus. If the transcript contains usable review findings despite a bad handoff, use the transcript as review evidence and note the malformed handoff.
6. When Opus produces no usable review evidence, run one fallback read-only Antigravity review with model `Gemini 3.1 Pro (High)` and a stricter checklist-style review prompt.
7. If fallback review is also empty, invalid, or blocked, run one `code-reviewer` custom agent using a task-local brief that provides the exact feature diff, base revision, and in-scope paths, explicitly excludes changes outside the feature, and requires read-only inspection (no edits, commits, pushes, PR/tracker updates, or agent spawning). Require its handoff to contain `status: clean|findings|blocked` in addition to `verdict: APPROVE|REQUEST_CHANGES|COMMENT`, files inspected, verification commands/results, findings by severity with file/line and a concrete correction, residual risks, and next steps. Enforce the mapping `APPROVE => clean`; `REQUEST_CHANGES => findings`; `COMMENT => clean` only when there are no actionable findings, otherwise `findings`; missing essential inputs => `blocked`. Record that independent Antigravity review was unavailable.
8. For low- or normal-risk changes, Codex may continue after passing verification, orchestrator QA, and independent review. For high-risk changes, skip commit/push if no independent review succeeded unless the user explicitly accepts that risk.

Address valid review findings yourself. Record false positives or out-of-scope findings for the final report.

## Source Tracker Update

Before committing, update the related ticket, spec, or tracker artifact when the implementation came from one. Mark delivered slices as implemented or complete, record important verification and review outcomes, and capture any new follow-up work as explicit remaining scope instead of leaving stale acceptance criteria.

Keep tracker updates factual and scoped to the delivered change. Do not rewrite unrelated backlog items or close future slices just because the current branch touched nearby code.

## Commit And Push

1. Recheck `git status --short` and review the final diff.
2. Stage only files that belong to the feature.
3. Commit with a concise message describing the behavior or architecture change.
4. Push the branch.
5. If the user asked for merge mode, confirm the pushed branch, base branch, CI/check status, and merge strategy before merging. Do not merge with failing or unknown required checks unless the user explicitly accepts that risk.

## Final Report

Report:

- what changed;
- verification run and result;
- orchestrator QA result;
- independent review result;
- commit hash and pushed branch;
- PR or merge status when applicable;
- any residual risk or follow-up.

If any gate could not run, say exactly why and whether the commit/push/merge was skipped.
