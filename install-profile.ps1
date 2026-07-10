[CmdletBinding()]
param(
    [string]$RepositoryRoot = $PSScriptRoot,
    [string]$SkillsDestination,
    [string]$AgentsDestination,
    [string]$ManifestPath,
    [switch]$DryRun,
    [switch]$KeepStale
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($SkillsDestination)) {
    $SkillsDestination = Join-Path (Join-Path $HOME ".agents") "skills"
}

$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
if ([string]::IsNullOrWhiteSpace($AgentsDestination)) {
    $AgentsDestination = Join-Path $codexHome "agents"
}
if ([string]::IsNullOrWhiteSpace($ManifestPath)) {
    $ManifestPath = Join-Path (Join-Path $HOME ".agents") "personal-skills-install.json"
}

function Get-AbsolutePath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.Path]::GetFullPath(
        $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
    )
}

function Assert-ChildPath {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Root
    )

    $absolutePath = Get-AbsolutePath $Path
    $absoluteRoot = (Get-AbsolutePath $Root).TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
    $rootPrefix = $absoluteRoot + [System.IO.Path]::DirectorySeparatorChar
    if (-not $absolutePath.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to manage path outside destination root: $absolutePath"
    }
    return $absolutePath
}

function Get-SkillName {
    param([Parameter(Mandatory = $true)][System.IO.FileInfo]$SkillFile)

    $lines = Get-Content -LiteralPath $SkillFile.FullName
    if ($lines.Count -lt 3 -or $lines[0].Trim() -ne "---") {
        throw "Skill frontmatter is missing in $($SkillFile.FullName)"
    }

    $name = $null
    for ($index = 1; $index -lt $lines.Count; $index += 1) {
        $line = $lines[$index]
        if ($line.Trim() -eq "---") { break }
        if ($line -match '^\s*name\s*:\s*(.+?)\s*$') {
            $name = $Matches[1].Trim()
            if (($name.StartsWith('"') -and $name.EndsWith('"')) -or
                ($name.StartsWith("'") -and $name.EndsWith("'"))) {
                $name = $name.Substring(1, $name.Length - 2)
            }
        }
    }

    if ([string]::IsNullOrWhiteSpace($name)) {
        throw "Skill name is missing in $($SkillFile.FullName)"
    }
    if ($name -notmatch '^[a-z0-9-]+$') {
        throw "Skill name '$name' is invalid in $($SkillFile.FullName)"
    }
    return $name
}

function Get-AgentName {
    param([Parameter(Mandatory = $true)][System.IO.FileInfo]$AgentFile)

    $content = Get-Content -LiteralPath $AgentFile.FullName -Raw
    $nameMatch = [regex]::Match($content, '(?m)^\s*name\s*=\s*"([^"]+)"\s*$')
    if (-not $nameMatch.Success) {
        throw "Agent name is missing or invalid in $($AgentFile.FullName)"
    }
    foreach ($requiredField in @("description", "developer_instructions")) {
        if ($content -notmatch "(?m)^\s*$requiredField\s*=") {
            throw "Agent field '$requiredField' is missing in $($AgentFile.FullName)"
        }
    }
    return $nameMatch.Groups[1].Value
}

$RepositoryRoot = Get-AbsolutePath $RepositoryRoot
$SkillsDestination = Get-AbsolutePath $SkillsDestination
$AgentsDestination = Get-AbsolutePath $AgentsDestination
$ManifestPath = Get-AbsolutePath $ManifestPath
$skillsSource = Join-Path $RepositoryRoot "skills"
$agentsSource = Join-Path $RepositoryRoot "agents"

if (-not (Test-Path -LiteralPath $skillsSource -PathType Container)) {
    throw "Skills source directory not found: $skillsSource"
}
if (-not (Test-Path -LiteralPath $agentsSource -PathType Container)) {
    throw "Agents source directory not found: $agentsSource"
}

$skills = @(
    Get-ChildItem -LiteralPath $skillsSource -Recurse -Filter "SKILL.md" -File |
        ForEach-Object {
            $name = Get-SkillName $_
            [pscustomobject]@{
                name = $name
                source = $_.Directory.FullName
                destination = Assert-ChildPath (Join-Path $SkillsDestination $name) $SkillsDestination
            }
        }
)

$agents = @(
    Get-ChildItem -LiteralPath $agentsSource -Recurse -Filter "*.toml" -File |
        ForEach-Object {
            [pscustomobject]@{
                name = Get-AgentName $_
                fileName = $_.Name
                source = $_.FullName
                destination = Assert-ChildPath (Join-Path $AgentsDestination $_.Name) $AgentsDestination
            }
        }
)

$duplicateSkills = @($skills | Group-Object name | Where-Object Count -gt 1)
if ($duplicateSkills.Count -gt 0) {
    throw "Duplicate skill names: $($duplicateSkills.Name -join ', ')"
}
$duplicateAgentNames = @($agents | Group-Object name | Where-Object Count -gt 1)
if ($duplicateAgentNames.Count -gt 0) {
    throw "Duplicate agent names: $($duplicateAgentNames.Name -join ', ')"
}
$duplicateAgentFiles = @($agents | Group-Object fileName | Where-Object Count -gt 1)
if ($duplicateAgentFiles.Count -gt 0) {
    throw "Duplicate agent filenames: $($duplicateAgentFiles.Name -join ', ')"
}

$previousManifest = $null
if (Test-Path -LiteralPath $ManifestPath -PathType Leaf) {
    $previousManifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    if ($previousManifest.version -ne 1) {
        throw "Unsupported install manifest version in $ManifestPath"
    }
    foreach ($previousSkill in @($previousManifest.skills)) {
        [void](Assert-ChildPath ([string]$previousSkill.destination) $SkillsDestination)
    }
    foreach ($previousAgent in @($previousManifest.agents)) {
        [void](Assert-ChildPath ([string]$previousAgent.destination) $AgentsDestination)
    }
}

Write-Output "Discovered $($skills.Count) skill(s) and $($agents.Count) custom agent(s)."
if ($DryRun) {
    foreach ($skill in $skills) { Write-Output "[dry-run] skill $($skill.name) -> $($skill.destination)" }
    foreach ($agent in $agents) { Write-Output "[dry-run] agent $($agent.name) -> $($agent.destination)" }
}
else {
    New-Item -ItemType Directory -Path $SkillsDestination -Force | Out-Null
    New-Item -ItemType Directory -Path $AgentsDestination -Force | Out-Null

    foreach ($skill in $skills) {
        $staging = Assert-ChildPath (
            Join-Path $SkillsDestination ".personal-skills-$($skill.name)-$([guid]::NewGuid().ToString('N'))"
        ) $SkillsDestination
        try {
            Copy-Item -LiteralPath $skill.source -Destination $staging -Recurse -Force
            if (Test-Path -LiteralPath $skill.destination) {
                Remove-Item -LiteralPath $skill.destination -Recurse -Force
            }
            Move-Item -LiteralPath $staging -Destination $skill.destination
        }
        finally {
            if (Test-Path -LiteralPath $staging) {
                Remove-Item -LiteralPath $staging -Recurse -Force
            }
        }
        Write-Output "Installed skill: $($skill.name)"
    }

    foreach ($agent in $agents) {
        $staging = Assert-ChildPath (
            Join-Path $AgentsDestination ".$($agent.fileName).$([guid]::NewGuid().ToString('N')).tmp"
        ) $AgentsDestination
        try {
            Copy-Item -LiteralPath $agent.source -Destination $staging -Force
            Move-Item -LiteralPath $staging -Destination $agent.destination -Force
        }
        finally {
            if (Test-Path -LiteralPath $staging) {
                Remove-Item -LiteralPath $staging -Force
            }
        }
        Write-Output "Installed custom agent: $($agent.name)"
    }
}

$desiredSkillPaths = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
$desiredAgentPaths = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::OrdinalIgnoreCase
)
foreach ($skill in $skills) { [void]$desiredSkillPaths.Add($skill.destination) }
foreach ($agent in $agents) { [void]$desiredAgentPaths.Add($agent.destination) }

$retainedStaleSkills = @()
$retainedStaleAgents = @()
if ($null -ne $previousManifest) {
    foreach ($previousSkill in @($previousManifest.skills)) {
        $destination = Assert-ChildPath ([string]$previousSkill.destination) $SkillsDestination
        if (-not $desiredSkillPaths.Contains($destination)) {
            if ($KeepStale) {
                $retainedStaleSkills += $previousSkill
                Write-Output "Retained stale skill: $($previousSkill.name)"
            }
            elseif ($DryRun) {
                Write-Output "[dry-run] remove stale skill: $($previousSkill.name)"
            }
            elseif (Test-Path -LiteralPath $destination) {
                Remove-Item -LiteralPath $destination -Recurse -Force
                Write-Output "Removed stale skill: $($previousSkill.name)"
            }
        }
    }
    foreach ($previousAgent in @($previousManifest.agents)) {
        $destination = Assert-ChildPath ([string]$previousAgent.destination) $AgentsDestination
        if (-not $desiredAgentPaths.Contains($destination)) {
            if ($KeepStale) {
                $retainedStaleAgents += $previousAgent
                Write-Output "Retained stale custom agent: $($previousAgent.name)"
            }
            elseif ($DryRun) {
                Write-Output "[dry-run] remove stale custom agent: $($previousAgent.name)"
            }
            elseif (Test-Path -LiteralPath $destination) {
                Remove-Item -LiteralPath $destination -Force
                Write-Output "Removed stale custom agent: $($previousAgent.name)"
            }
        }
    }
}

if (-not $DryRun) {
    $manifestSkills = @($skills | ForEach-Object {
        [ordered]@{ name = $_.name; destination = $_.destination }
    }) + @($retainedStaleSkills)
    $manifestAgents = @($agents | ForEach-Object {
        [ordered]@{ name = $_.name; destination = $_.destination }
    }) + @($retainedStaleAgents)
    $manifest = [ordered]@{
        version = 1
        repository = $RepositoryRoot
        installedAt = (Get-Date).ToUniversalTime().ToString("o")
        skills = $manifestSkills
        agents = $manifestAgents
    }

    $manifestDirectory = Split-Path -Parent $ManifestPath
    New-Item -ItemType Directory -Path $manifestDirectory -Force | Out-Null
    $manifestStaging = Join-Path $manifestDirectory ".$([System.IO.Path]::GetFileName($ManifestPath)).$([guid]::NewGuid().ToString('N')).tmp"
    try {
        $json = $manifest | ConvertTo-Json -Depth 5
        [System.IO.File]::WriteAllText(
            $manifestStaging,
            $json + [Environment]::NewLine,
            [System.Text.UTF8Encoding]::new($false)
        )
        Move-Item -LiteralPath $manifestStaging -Destination $ManifestPath -Force
    }
    finally {
        if (Test-Path -LiteralPath $manifestStaging) {
            Remove-Item -LiteralPath $manifestStaging -Force
        }
    }
    Write-Output "Profile installation complete. Start a new Codex task to load changes."
}
