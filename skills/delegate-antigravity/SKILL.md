---
name: delegate-antigravity
description: Delegate tasks from Codex to Antigravity CLI (`agy`) through file-based handoffs. Use when Codex should ask Antigravity to implement, inspect, review, debug, or continue work in a workspace and return a structured handoff.
---

# Delegate Antigravity

Delegate work to Antigravity CLI with a file handoff stored in the user's temp directory, outside the repo. Default to model `Gemini 3.5 Flash (Medium)` unless the user requests another model.

## Workflow

1. Confirm `agy` is available with `agy --help` when this has not been checked in the current session.
2. Write the delegation brief as a handoff file, not as a large shell prompt.
3. Store all handoff files under the user's temp profile directory, outside the workspace. Use `scripts/invoke-antigravity.ps1` unless the task requires a custom command.
4. Choose permissions from the task:
   - For read-only inspection, omit tool auto-approval.
   - For expected edits, internet access, terminal commands, or other tool use, pass `-AllowAgentTools`. The wrapper then adds `--dangerously-skip-permissions` only when the workspace is inside a Git worktree.
   - For restricted experiments, pass `-Sandbox`; sandboxed terminal-command delegation may fail in environments that have not preconfigured tool access.
5. Run `agy --print` from the target workspace. Pass `--model "Gemini 3.5 Flash (Medium)"` by default and a longer `--print-timeout` for implementation work.
6. Read the returned handoff file and use it as evidence. Do not assume success from process exit alone; verify that the handoff exists and includes status, changes, verification, risks, and next steps.

Completion criterion: Codex has either incorporated Antigravity's completed handoff into the user's task or reported a blocked Antigravity run with the stdout/stderr and handoff path.

## Wrapper

Run the bundled wrapper from PowerShell:

```powershell
& "<skill-dir>\scripts\invoke-antigravity.ps1" `
  -Workspace "C:\path\to\repo" `
  -Task "Implement the requested change, run relevant verification, and write the handoff." `
  -AllowAgentTools
```

Use `-HandoffFile` when the brief already exists. Use `-ExtraDir` for additional readable directories. Use `-AllowAgentTools` when Antigravity is expected to edit files, access the network, run terminal commands, or use tools; it is guarded by Git worktree detection. Use `-Sandbox` for restricted runs; the wrapper automatically adds its temp handoff run directory when sandbox mode is enabled. Use `-ForceWithoutSourceControl` only for disposable directories that are not under Git.

The wrapper prints a JSON object with:

- `handoffIn`: temp input file passed to Antigravity
- `handoffOut`: temp output file Antigravity was instructed to write
- `transcript`: temp stdout/stderr capture
- `exitCode`: `agy` process exit code
- `model`: model passed to `agy`
- `sourceControlled`: whether the workspace was detected inside a Git worktree
- `allowAgentTools`: whether tool permission auto-approval was passed to `agy`

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
Write the output handoff with objective, changes, files touched, verification, risks, and next steps.
Print only:
STATUS: success|blocked
HANDOFF: <absolute output handoff path>
```

## Direct Command

If the wrapper is unsuitable, use the same pattern manually:

```powershell
Set-Location "C:\path\to\repo"
agy --print "Read <temp>\handoff.in.md, execute it, write <temp>\handoff.out.md, then print only STATUS and HANDOFF." --model "Gemini 3.5 Flash (Medium)" --print-timeout 45m
```
