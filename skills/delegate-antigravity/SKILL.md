---
name: delegate-antigravity
description: Delegate work from Codex to Antigravity CLI (`agy`) through temp-file handoffs. Use when Codex should ask Antigravity to implement, inspect, review, debug, or continue work in a workspace and return a structured handoff.
---

# Delegate Antigravity

Delegate work to Antigravity CLI with a file handoff stored in the user's temp directory, outside the repo. Use the wrapper default model unless the caller names a model.

## Workflow

1. Confirm `agy` is available with `agy --help` when this has not been checked in the current session.
2. Translate caller intent into wrapper options: named model, read-only versus tool-enabled work, sandbox mode, extra readable directories, timeout, and output contract.
3. Write the delegation brief as a handoff file, not as a large shell prompt.
4. Store all handoff files under the user's temp profile directory, outside the workspace. Use `scripts/invoke-antigravity.ps1` unless the task requires a custom command.
5. Choose permissions from the task:
   - For read-only inspection, omit tool auto-approval.
   - For expected edits, internet access, terminal commands, or other tool use, pass `-AllowAgentTools`. The wrapper then adds `--dangerously-skip-permissions` only when the workspace is inside a Git worktree.
   - For restricted experiments, pass `-Sandbox`; sandboxed terminal-command delegation may fail in environments that have not preconfigured tool access.
6. Run the wrapper, which invokes `agy --print` from the target workspace. Use the wrapper default model unless the caller named a model, and always use a large print timeout of at least `1h` so Antigravity is less likely to be terminated mid-execution.
7. If another agent or wrapper invokes `scripts/invoke-antigravity.ps1`, it must never set an outer command timeout shorter than the script's own `-PrintTimeout`. Prefer a safety margin above that value.
8. Read the returned handoff file and use it as evidence. Do not assume success from process exit alone.
9. Accept the handoff only when it is non-empty and includes status, objective or result, files touched or inspected, verification, risks, and next steps. If the handoff is missing, empty, or malformed, read the transcript and report a blocked run with the transcript and handoff paths.

Completion criterion: Codex has either incorporated Antigravity's completed handoff into the user's task or reported a blocked Antigravity run with the stdout/stderr and handoff path.

## Wrapper

Run the bundled wrapper from PowerShell. For read-only inspection, omit tool auto-approval:

```powershell
& "<skill-dir>\scripts\invoke-antigravity.ps1" `
  -Workspace "C:\path\to\repo" `
  -Task "Inspect the requested area and write the handoff."
```

For edits or tool-enabled work, allow Antigravity tools:

```powershell
& "<skill-dir>\scripts\invoke-antigravity.ps1" `
  -Workspace "C:\path\to\repo" `
  -Task "Implement the requested change, run relevant verification, and write the handoff." `
  -AllowAgentTools
```

Use `-Model` when the caller names a model. Use `-HandoffFile` when the brief already exists. Use `-ExtraDir` for additional readable directories. Use `-AllowAgentTools` when Antigravity is expected to edit files, access the network, run terminal commands, or use tools; it is guarded by Git worktree detection. Use `-Sandbox` for restricted runs; the wrapper automatically adds its temp handoff run directory when sandbox mode is enabled. Use `-ForceWithoutSourceControl` only for disposable directories that are not under Git. If this script is called by another wrapper or agent, the outer command timeout must be greater than or equal to `-PrintTimeout`, ideally with extra buffer.

The wrapper prints a JSON object with:

- `handoffIn`: temp input file passed to Antigravity
- `handoffOut`: temp output file Antigravity was instructed to write
- `transcript`: temp stdout/stderr capture
- `exitCode`: `agy` process exit code
- `model`: model passed to `agy`
- `sourceControlled`: whether the workspace was detected inside a Git worktree
- `allowAgentTools`: whether tool permission auto-approval was passed to `agy`
- `handoffOutExists`: whether the output handoff file exists

## Handoff Contract

Use this structure for the input brief:

```markdown
# Agent Handoff

## Objective
...

## Workspace
Repo/path, branch, relevant commands.

## Current State
What has already been done.

## Constraints
Do not touch..., preserve..., expected style...

## Required Work
1. ...
2. ...

## Verification
Run these commands:
- ...

## Output Contract
Write the output handoff with status, objective or result, files touched or inspected, verification, risks, and next steps.
Print only:
STATUS: success|blocked
HANDOFF: <absolute output handoff path>
```

## Direct Command

If the wrapper is unsuitable, use the same pattern manually:

```powershell
Set-Location "C:\path\to\repo"
agy --print "Read <temp>\handoff.in.md, execute it, write <temp>\handoff.out.md, then print only STATUS and HANDOFF." --print-timeout 1h
```

Add `--model "<caller-named model>"` only when the caller requested a specific model.
