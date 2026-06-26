---
name: ship-feature
description: "End-to-end feature delivery workflow for Codex: implement a scoped feature, run verification, use independent QA and review subagents, address findings, commit, push, and optionally merge. Use when the user says /ship-feature, asks to ship a feature, or asks for a reproducible implement-QA-review-commit-push-merge loop."
---

# Ship Feature

## Scope

Use this skill for one scoped feature or PRD-backed change. Keep the slice narrow, preserve unrelated worktree changes, and follow repository instructions before this workflow.

Default mode is commit and push. Merge only when the user explicitly asks for merge mode, for example `/ship-feature --merge`.

## Preflight

1. Identify the source of truth: current user request, PRD, issue, or design doc.
2. Inspect repo instructions, current branch, `git status --short`, and relevant docs/code.
3. State assumptions and the implementation/verification plan.
4. If unrelated dirty files touch the target area, work with them carefully; ask only when they make the task unsafe or impossible.
5. Create or switch to an appropriate feature branch when requested or when repo practice requires it.

## Implement

1. Make the smallest change that satisfies the PRD/request.
2. Keep rule/business validation in the authoritative layer for the repo.
3. Preserve public contracts unless the source of truth explicitly changes them.
4. Update docs and memory when behavior, architecture, workflow, or durable knowledge changes.
5. Run the relevant local verification before asking any subagent to review.

## Verification Gate

Choose commands from repo docs and the touched surface. Do not invent heavy test coverage when targeted checks are enough.

Common examples:

- Frontend change: build, relevant browser QA, and any existing frontend tests.
- Backend/API change: targeted pytest plus contract tests.
- Catalog/docs change: catalog/link validation scripts.
- Full-stack behavior change: backend tests, frontend build, and browser QA.

Do not continue to commit while required local verification is failing.

## QA Subagent

After implementation and first verification, run an independent QA subagent when subagent tooling is available.

Ask the QA subagent to validate behavior against the PRD/request and user-visible acceptance criteria. Give it the PRD/request path, relevant local URL or commands, and the current diff context. Do not tell it your expected result beyond the acceptance criteria.

Address valid QA findings. Record false positives or out-of-scope findings for the final report. Rerun affected verification after fixes.

## Review Subagent

After QA is clean, run a separate review subagent when subagent tooling is available.

Ask the review subagent for code-review findings on the final diff, prioritizing bugs, regressions, missing tests, boundary violations, and unsafe assumptions. Keep this separate from QA so behavior testing and code review are independent passes.

Address valid review findings. Record false positives or out-of-scope findings for the final report. Rerun affected verification after fixes.

## Source Tracker Update

Before committing, update the related issue, PRD, or tracker artifact when the implementation came from one. Mark delivered slices as implemented or complete, record important verification and review outcomes, and capture any new follow-up work as explicit remaining scope instead of leaving stale acceptance criteria.

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
- QA subagent result;
- review subagent result;
- commit hash and pushed branch;
- PR or merge status when applicable;
- any residual risk or follow-up.

If any gate could not run, say exactly why and whether the commit/push/merge was skipped.
