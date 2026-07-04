param(
    [Parameter(Mandatory = $true)]
    [string]$Workspace,

    [string]$Task,

    [string]$HandoffFile,

    [string]$Model = "Gemini 3.5 Flash (Medium)",

    [string]$PrintTimeout = "1h",

    [string[]]$ExtraDir = @(),

    [switch]$Sandbox,

    [switch]$NoSandbox,

    [switch]$AllowAgentTools,

    [switch]$DangerouslySkipPermissions,

    [switch]$ForceWithoutSourceControl
)

$ErrorActionPreference = "Stop"

function Convert-PrintTimeoutToTimeSpan {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value
    )

    if ($Value -match '^(?<amount>\d+)(?<unit>[mh])$') {
        $amount = [int]$matches['amount']
        $unit = $matches['unit']
        switch ($unit) {
            'm' { return [TimeSpan]::FromMinutes($amount) }
            'h' { return [TimeSpan]::FromHours($amount) }
        }
    }

    throw "Unsupported -PrintTimeout format '$Value'. Use whole minutes or hours such as 60m or 1h."
}

$resolvedPrintTimeout = Convert-PrintTimeoutToTimeSpan -Value $PrintTimeout
if ($resolvedPrintTimeout -lt [TimeSpan]::FromHours(1)) {
    throw "Refusing to run with -PrintTimeout '$PrintTimeout'. Minimum supported value is 1h."
}

if (-not (Get-Command agy -ErrorAction SilentlyContinue)) {
    throw "agy was not found on PATH. Run agy install or invoke the CLI by absolute path."
}

$workspacePath = (Resolve-Path -LiteralPath $Workspace).Path
if (-not (Test-Path -LiteralPath $workspacePath -PathType Container)) {
    throw "Workspace is not a directory: $Workspace"
}

$gitControlled = $false
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    $gitOutput = & git -C $workspacePath rev-parse --is-inside-work-tree 2>$null
    $gitControlled = ($LASTEXITCODE -eq 0 -and $gitOutput -eq "true")
}

$shouldSkipPermissions = $AllowAgentTools -or $DangerouslySkipPermissions
if ($shouldSkipPermissions -and -not $gitControlled -and -not $ForceWithoutSourceControl) {
    throw "Refusing to auto-approve Antigravity tools because the workspace is not inside a Git worktree. Use -ForceWithoutSourceControl only for disposable directories."
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) "codex-antigravity-handoffs"
New-Item -ItemType Directory -Force -Path $tempRoot | Out-Null

$stamp = "{0}-{1}" -f (Get-Date -Format "yyyyMMdd-HHmmss-ffff"), ([guid]::NewGuid().ToString("N"))
$runDir = Join-Path $tempRoot "agy-$stamp"
New-Item -ItemType Directory -Force -Path $runDir | Out-Null

$handoffIn = Join-Path $runDir "handoff.in.md"
$handoffOut = Join-Path $runDir "handoff.out.md"
$transcript = Join-Path $runDir "agy.transcript.txt"

if ($HandoffFile) {
    $sourceHandoff = (Resolve-Path -LiteralPath $HandoffFile).Path
    Copy-Item -LiteralPath $sourceHandoff -Destination $handoffIn
} else {
    if (-not $Task) {
        throw "Provide either -Task or -HandoffFile."
    }

    @"
# Agent Handoff

## Objective
$Task

## Workspace
$workspacePath

## Current State
Codex is delegating this task to Antigravity CLI through a temp-file handoff.

    ## Constraints
- Keep all handoff files in this temp run directory: $runDir
- Do not create handoff files in the workspace unless the task itself explicitly requires it.
- Preserve unrelated user changes.
- This workspace is source controlled: $gitControlled

## Required Work
1. Inspect the workspace and complete the objective.
2. Run relevant verification, or explain why verification could not be run.
3. Write the output handoff to: $handoffOut

## Output Contract
Write $handoffOut with:
- Objective
- What changed
- Files touched
- Verification run and results
- Remaining risks
- Exact next steps

Print only:
STATUS: success|blocked
HANDOFF: $handoffOut
"@ | Set-Content -LiteralPath $handoffIn -Encoding UTF8
}

$prompt = @"
Read this handoff file:
$handoffIn

Execute the task in this workspace:
$workspacePath

When finished, write this output handoff:
$handoffOut

The output handoff must include objective, changes, files touched, verification, risks, and exact next steps.

Print only:
STATUS: success|blocked
HANDOFF: $handoffOut
"@

$agyArgs = @(
    "--print", $prompt,
    "--model", $Model,
    "--print-timeout", $PrintTimeout
)

if ($Sandbox -and -not $NoSandbox) {
    $agyArgs += "--sandbox"
    $agyArgs += @("--add-dir", $runDir)
}

foreach ($dir in $ExtraDir) {
    $agyArgs += @("--add-dir", (Resolve-Path -LiteralPath $dir).Path)
}

if ($shouldSkipPermissions) {
    $agyArgs += "--dangerously-skip-permissions"
}

Push-Location $workspacePath
try {
    & agy @agyArgs *> $transcript
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}

[pscustomobject]@{
    handoffIn = $handoffIn
    handoffOut = $handoffOut
    transcript = $transcript
    exitCode = $exitCode
    model = $Model
    workspace = $workspacePath
    sourceControlled = $gitControlled
    allowAgentTools = [bool]$shouldSkipPermissions
    handoffOutExists = (Test-Path -LiteralPath $handoffOut)
} | ConvertTo-Json -Depth 3

exit $exitCode
