# Personal Skills

Repository for personal Codex skills and custom agents.

## Available Skills

- `delegate-antigravity`: delegates implementation, inspection, review, and debugging through Antigravity CLI handoffs.
- `gen-tokens`: generates Roll20-ready NPC portrait grids and extracts individual Roll20 tokens.
- `setup-matt-pocock-skills`: configures a repository for spec-and-ticket-first engineering workflows and migrates legacy PRD- and issue-first setups.
- `ship-feature`: ships a scoped feature through implementation, QA, review, commit, and push.
- `to-goal-handoff`: prepares a persistent goal handoff from a spec and ordered tickets.
- `to-tickets-agentic`: turns a plan or spec into an agent-executable graph of tracer-bullet tickets.

Custom agents are discovered automatically from `agents/**/*.toml` by the profile installer.

## Requirements

- PowerShell 5.1 or newer.
- Git, if installing from a cloned repository.
- Node.js with `npx`, only when using the optional Skills CLI workflow.

## Install or Update the Complete Profile

Clone the repository and enter its root directory:

```powershell
git clone https://github.com/raphaelmesquita/personal-skills.git
cd personal-skills
```

Install every discovered skill and custom agent:

```powershell
.\install-profile.ps1
```

The installer recursively discovers:

- every `SKILL.md` below `skills/`, using its frontmatter `name` as the installed directory;
- every custom-agent TOML below `agents/`, using its filename in the installed profile.

The installer continues to support repository-local TOMLs in `agents/`. The `ship-feature` skill instead depends on the centralized `implementer` and `code-reviewer` agents, so this repository intentionally does not duplicate those configurations.

It installs skills into `~/.agents/skills/`, agents into `$CODEX_HOME/agents/` (or `~/.codex/agents/`), and records owned destinations in `~/.agents/personal-skills-install.json`. A later run updates current entries and safely removes only previously managed entries that no longer exist in this repository.

Preview an installation without changing the profile:

```powershell
.\install-profile.ps1 -DryRun
```

Keep previously managed entries that were removed from the repository:

```powershell
.\install-profile.ps1 -KeepStale
```

Start a new Codex task after installation so newly installed skills and agents are discovered.

## Optional Skills CLI Workflow

The upstream Skills CLI installs skills but does not install this repository's custom agents. To install only the skills globally:

```powershell
npx -y skills add . --global --agent codex --skill "*" -y --full-depth
```

List the skills detected in this repository:

```powershell
npx -y skills add . --list --full-depth
```

Install only skills from the repository root for the current project:

```powershell
npx -y skills add .
```

To install all skills for all supported agents, use:

```powershell
npx -y skills add . --all --full-depth
```

Note: `--all` targets every agent known to the CLI. Some agents may not support a given installation scope, such as PromptScript with global installs. For a clean global install under `~/.agents`, prefer the first command above or pass specific agent ids with `--agent`.

## Verify Installation

Inspect the installed profile:

```powershell
Get-ChildItem ~/.agents/skills
Get-ChildItem $(if ($env:CODEX_HOME) { "$env:CODEX_HOME/agents" } else { "~/.codex/agents" })
Get-Content ~/.agents/personal-skills-install.json
```

The Skills CLI can also list skills it knows about:

```powershell
npx -y skills list --global
```

## Notes

- Run `install-profile.ps1` from any location; it resolves sources relative to its own repository root.
- Custom destinations are available through `-SkillsDestination`, `-AgentsDestination`, and `-ManifestPath`, which are useful for testing or isolated profiles.
- Use `--full-depth` when using the optional Skills CLI so nested skill folders are detected.
- Review skills before use; installed skills run with agent permissions.
