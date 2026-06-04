# Personal Skills

Repository for personal agent skills.

## Available Skills

- `gen-tokens`: generates Roll20-ready 3x3 NPC portrait grids and extracts them into individual hex-safe PNG tokens.

## Requirements

- Node.js with `npx` available.
- Git, if installing from a cloned repository.

## Install All Skills From This Repository

Clone the repository and enter its root directory:

```powershell
git clone https://github.com/raphaelmesquita/personal-skills.git
cd personal-skills
```

Install all skills globally under `~/.agents` for Codex:

```powershell
npx -y skills add . --global --agent codex --skill "*" -y --full-depth
```

List the skills detected in this repository:

```powershell
npx -y skills add . --list --full-depth
```

Install skills from the repository root for the current project:

```powershell
npx -y skills add .
```

To install all skills for all supported agents, use:

```powershell
npx -y skills add . --all --full-depth
```

Note: `--all` targets every agent known to the CLI. Some agents may not support a given installation scope, such as PromptScript with global installs. For a clean global install under `~/.agents`, prefer the first command above or pass specific agent ids with `--agent`.

## Verify Installation

List installed project skills:

```powershell
npx -y skills list
```

List installed global skills:

```powershell
npx -y skills list --global
```

## Update Installed Skills

From any project using these skills:

```powershell
npx -y skills update -y
```

For global skills:

```powershell
npx -y skills update --global -y
```

## Remove Skills

Remove interactively:

```powershell
npx -y skills remove
```

Remove a specific skill:

```powershell
npx -y skills remove gen-tokens -y
```

## Notes

- Run the install commands from the repository root so the CLI can discover skills under `skills/`.
- Use `--full-depth` to ensure nested skill folders are detected.
- Review skills before use; installed skills run with agent permissions.
