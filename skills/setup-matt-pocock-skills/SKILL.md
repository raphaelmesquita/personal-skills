---
name: setup-matt-pocock-skills
description: Configure the current repository for spec-and-ticket-first engineering skills, including lossless migration from deprecated PRD- and issue-first setups, with AGENTS.md as the canonical instructions and a CLAUDE.md forwarding shim.
---

# Setup Matt Pocock Skills

Configure the repository contract consumed by `$to-spec`, `$to-tickets`, and the other engineering skills:

- **Spec publishing** — where the root spec is represented and how its ready state is recorded
- **Ticket tracker** — where logical tickets are represented and how blocking edges and the frontier work
- **Triage vocabulary** — the tracker-specific strings for the canonical triage roles
- **Domain docs** — where context glossaries and ADRs live

A spec is the canonical source artifact; an existing PRD is a legacy spec. A ticket is the logical unit of implementation work. GitHub and GitLab store both as issues; local Markdown stores the spec at `.scratch/<feature>/spec.md` and tickets under `.scratch/<feature>/issues/`. Keep these distinctions explicit in every generated document.

Treat the repository as the complete input. A zero-argument invocation must explore, infer the legacy or default route, present the resulting edit set, confirm it, and write. Ask for missing context only when the repository contains a genuine ambiguity or a lossy choice.

## Process

### 1. Inspect the repository

Read:

- `git remote -v` and `.git/config`;
- root `CLAUDE.md` and `AGENTS.md`, including their complete contents, any forwarding directive, and every `## Agent skills` block;
- `docs/agents/ticket-tracker.md` and the legacy `docs/agents/issue-tracker.md`;
- `docs/agents/triage-labels.md` and `docs/agents/domain.md`;
- root `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, and context-scoped ADR directories;
- `.scratch/`, especially `spec.md`, case-insensitive legacy `PRD.md`/`prd.md`, ticket files, indexes, statuses, and blocker references; distinguish active work from `_done`, `archive`, `archived`, and other repository-defined historical areas;
- repository references to `to-prd` invocations, canonical PRD wording, `issue-tracker.md`, `### Issue tracker`, and issue-first setup wording;
- installed skills, including `triage`;
- monorepo signals such as `pnpm-workspace.yaml`, package workspaces, or multiple populated packages.

Classify the repository as **unconfigured**, **spec-and-ticket-first**, or **legacy**. Legacy markers include an active `to-prd` invocation, PRD as the canonical source term, `prd.md`, the old tracker document or heading, or local conventions that call logical work units implementation issues. Historical mentions alone do not make a configured repository legacy.

Classify the instruction topology separately: missing `AGENTS.md`, canonical `AGENTS.md`, exact `CLAUDE.md` shim (`@AGENTS.md` after trimming whitespace), missing `CLAUDE.md`, or substantive `CLAUDE.md` content.

Complete this step only when the tracker representation, instruction topology, triage availability, domain layout, active-versus-historical boundary, and migration state are known.

### 2. Load the applicable references

Read exactly one tracker template in full after choosing or inferring the representation:

- [ticket-tracker-github.md](references/ticket-tracker-github.md)
- [ticket-tracker-gitlab.md](references/ticket-tracker-gitlab.md)
- [ticket-tracker-local.md](references/ticket-tracker-local.md)

Read [triage-labels.md](references/triage-labels.md) when `triage` is installed. Read [domain.md](references/domain.md) for every setup.

When legacy markers exist, read [migration.md](references/migration.md) in full and include every applicable conversion in the proposed edit set.

### 3. Infer the route

Reuse choices established by a spec-and-ticket-first or legacy configuration. Existing repository convention outranks remote-host inference; a configured local tracker remains local even when the Git remote is GitHub or GitLab.

For an unconfigured repository, apply defaults without asking:

1. **Spec and ticket tracker:** GitHub for a GitHub remote, GitLab for a GitLab remote, otherwise local Markdown.
2. **Ready state and triage labels:** always resolve the canonical `ready-for-agent` role to one concrete tracker value. When `triage` is installed, use its mapping and default the five roles to `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. When `triage` is unavailable, use the literal `ready-for-agent` value and record it directly in `ticket-tracker.md`.
3. **Domain layout:** use single-context unless existing context boundaries make a multi-context layout unambiguous.
4. **Instruction routing:** create `AGENTS.md` as canonical and `CLAUDE.md` as its forwarding shim.

Ask only when evidence conflicts: multiple established trackers, two source artifacts competing for canonical status, substantive instruction files with incompatible rules, unclear active-versus-historical boundaries, or another choice that would discard meaning. Remote tracker writes and splitting a combined local work file always require explicit confirmation.

Complete this step when the route is fully inferred and every remaining ambiguity has a user decision.

### 4. Present the complete edit set

Show drafts of:

- canonical `AGENTS.md` changes and the exact `CLAUDE.md` shim;
- the `## Agent skills` block;
- `docs/agents/ticket-tracker.md`;
- `docs/agents/domain.md`;
- `docs/agents/triage-labels.md`, when applicable;
- every legacy file or reference to update or retire;
- any local ticket-file normalization or confirmed remote tracker write.

State which existing conventions and user-authored additions will be preserved. Obtain approval before writing.

### 5. Write the canonical configuration

Make root `AGENTS.md` the single source of repository instructions. Update its existing `## Agent skills` block in place, or create the file and block when absent. Preserve all surrounding user content. Use this shape:

```markdown
## Agent skills

### Ticket tracker

[One-line summary of where specs and tickets are represented and how blockers are recorded]. See `docs/agents/ticket-tracker.md`.

### Triage labels

[One-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[One-line summary of the single-context or multi-context layout]. See `docs/agents/domain.md`.
```

Make root `CLAUDE.md` a forwarding shim whose trimmed content is exactly:

```text
@AGENTS.md
```

Preserve an existing exact shim. Create it when absent. When `CLAUDE.md` contains substantive instructions, follow the preservation procedure in `migration.md`: place every unique live instruction in `AGENTS.md`, resolve conflicts, read back the canonical file, and only then replace `CLAUDE.md` with the shim.

Omit the triage subsection and file when `triage` is unavailable. In that branch, render `ready-for-agent` as the explicit ready-state value in `ticket-tracker.md`. Render the selected references into the canonical docs with one concrete ready-state value and no unresolved placeholder, adapting repository-specific values without discarding their spec publishing or ticket graph conventions.

For an "other" tracker, write `ticket-tracker.md` from the user's workflow and include: spec publication and ready state, ticket representation, create/read/update/close operations, parent references, blocking-edge storage, frontier query, claim semantics, ready-state mapping, and failure fallback.

When migrating, follow `migration.md` through retirement of the legacy configuration. The repository must end with one canonical tracker document.

### 6. Validate the resulting contract

Read every written file back and verify:

- root `AGENTS.md` exists, contains the sole `## Agent skills` block, and preserves every live repository instruction;
- root `CLAUDE.md` exists and its trimmed content equals `@AGENTS.md`;
- no substantive instruction was lost while consolidating `CLAUDE.md` into `AGENTS.md`;
- the Agent skills block links to files that exist;
- `ticket-tracker.md` defines how `$to-spec` publishes the root spec and applies `ready-for-agent`;
- `ticket-tracker.md` distinguishes logical tickets from their storage representation;
- creation is dependency-ordered and every representation defines blocking edges and a frontier;
- local Markdown uses one file per ticket under `.scratch/<feature>/issues/<NN>-<slug>.md`;
- local Markdown uses `.scratch/<feature>/spec.md` as the canonical spec path;
- `ready-for-agent` resolves to one concrete tracker value through the triage vocabulary when present, or through the explicit `ready-for-agent` fallback in `ticket-tracker.md`;
- parent work items remain unchanged unless the user explicitly approved a mutation;
- legacy canonical references are gone after migration;
- preserved custom conventions remain represented exactly once.

For local active tickets, verify referenced blockers resolve and the known graph is acyclic. Report ambiguous historical items without inventing edges.

Complete this step only when all generated links resolve, instruction routing satisfies the invariant, and the repository has a single coherent spec-and-ticket-first contract.

### 7. Report

List created, updated, retired, and intentionally preserved files. State whether the repository was newly configured or migrated, which tracker representation is active, whether any external work items changed, and which engineering skills can now consume the contract.

Mention that later tracker or vocabulary changes can be made directly in `docs/agents/*.md`; rerun this setup for a guided conversion.
