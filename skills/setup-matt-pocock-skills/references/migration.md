# Legacy PRD- and Issue-First Migration

Use this branch when the repository contains output from the deprecated PRD- or issue-first setup.

## Preserve before translating

Inventory `$to-prd` and `/to-prd` references, PRD terminology and files case-insensitively, the legacy tracker document, every Agent skills block, complete `AGENTS.md` and `CLAUDE.md` contents, cross-references, custom commands, label overrides, domain choices, local work files, archive conventions, and remote identifiers. Treat user-authored additions as source material, not template noise.

The conversion is lossless only when every live legacy convention has a destination or an explicit user-approved retirement.

## Translate the canonical contract

Apply these semantic conversions:

| Legacy contract | Spec-and-ticket-first contract |
| --- | --- |
| `$to-prd` or `/to-prd` | `$to-spec` |
| PRD as the canonical source artifact | Spec as the canonical source artifact |
| Existing PRD tracker item | Legacy spec with stable identifier and history |
| Local `PRD.md`/`prd.md` | Canonical `spec.md`, after collision and link checks |
| `docs/agents/issue-tracker.md` | `docs/agents/ticket-tracker.md` |
| `### Issue tracker` | `### Ticket tracker` |
| Logical work units called issues | Logical work units called tickets |
| Tracker-specific issue commands as the abstraction | Tickets represented by tracker issues or local files |
| Dependency prose without execution semantics | Blocking edges plus an explicit frontier query |
| Publish an issue | Publish a ticket in dependency order |

Update active workflow references from `$to-prd` to `$to-spec` and use **spec** for the canonical source artifact. Preserve **PRD** in historical titles, URLs, quoted content, and compatibility notes. Update repository references to the canonical tracker filename and heading. Preserve **issue** where it names a real GitHub/GitLab object, CLI command, API, or historical identifier.

The rename does not introduce a product interview. `$to-spec` synthesizes the existing conversation and codebase understanding, checking only that the proposed testing seams match the user's expectations before publication.

Write `ticket-tracker.md` first, read it back, and confirm it contains all preserved conventions. Then remove `issue-tracker.md` so there is one source of truth. When unmapped custom content remains, keep the migration incomplete and ask the user where it belongs instead of maintaining two canonical files.

## Consolidate instruction routing

Use root `AGENTS.md` as the canonical instruction file and root `CLAUDE.md` as a one-line `@AGENTS.md` forwarding shim.

- When `CLAUDE.md` is absent, create the shim.
- When its trimmed content is exactly `@AGENTS.md`, preserve it.
- When `AGENTS.md` is absent and `CLAUDE.md` is substantive, move the complete instruction content into a new `AGENTS.md`, apply the setup edits there, read it back, then replace `CLAUDE.md` with the shim.
- When both files are substantive, build one merged `AGENTS.md`: preserve unique instructions, collapse exact duplication, and ask the user about contradictory rules. Replace `CLAUDE.md` only after every live instruction has one verified home.
- When Agent skills blocks exist in both files, merge them into the single block in `AGENTS.md` and preserve repository-specific additions.

Show the consolidation in the proposed edit set. The shim write is the final instruction-routing operation, after canonical-content validation.

## Convert existing source artifacts

### GitHub, GitLab, or another remote tracker

Treat an existing PRD issue as a spec in place. Keep its identifier, title, URL, body, comments, labels, relationships, and history stable. Update active indexes and workflow documentation to call it a spec and invoke `$to-spec`; historical items need no bulk rename.

### Local Markdown

Use `.scratch/<feature>/spec.md` as the canonical path. Match legacy `PRD.md`/`prd.md` case-insensitively. A legacy PRD already stored at `spec.md` needs only terminology and workflow-reference updates.

Infer active and historical areas from repository indexes, statuses, and archive directory conventions such as `_done`, `archive`, and `archived`. Migrate active source artifacts. Preserve historical filenames and links unless they break the live workflow.

When an active legacy PRD file exists without `spec.md`, propose a rename to `spec.md` together with every link and index update. Perform the rename after confirming that `spec.md` is free. When both files exist, compare their roles and ask the user to choose or merge the canonical source; preserve both until that ambiguity is resolved.

## Convert existing tickets

### GitHub, GitLab, or another remote tracker

Keep issue identifiers, URLs, comments, labels, parent relationships, and history stable. Reinterpret each implementation issue as a ticket represented by an issue.

Document native blocking relationships and frontier queries in the new configuration. Translate existing textual `Blocked by` edges into native relationships only when the mapping is unambiguous and the user explicitly approves those remote writes. Otherwise preserve the textual edges and record the supported native form for new tickets.

Historical ticket issues need no bulk rename. Update open parent indexes or repository docs only when they point at the retired configuration filename or use terminology that changes execution semantics.

### Local Markdown

Keep `.scratch/<feature>/issues/` as the physical directory because `$to-tickets` uses that stable path. Treat every existing one-file-per-item entry as a ticket in place; preserve its filename, number, status, body, and history.

For active work:

- ensure one ticket per file;
- keep or add a `Status:` value using the configured vocabulary;
- keep `Blocked by` references when they resolve;
- add `None — can start immediately` only when the absence of blockers is known;
- update indexes and links to call the entries tickets;
- preserve completed historical files unless a broken reference requires repair.

Split a combined work file only after showing the proposed ticket boundaries, new filenames, blocker graph, and link rewrites to the user. Preserve the original content in the resulting tickets; retire the combined file after all references resolve.

## Migration completion check

Finish the migration only when:

- `AGENTS.md` is canonical, contains every live instruction, and owns the sole Agent skills block;
- `CLAUDE.md` exists as the exact `@AGENTS.md` forwarding shim;
- active workflow references invoke `$to-spec` rather than `to-prd`;
- spec is the canonical source term, with PRD retained only for history or compatibility;
- active local efforts use `spec.md`, or any unresolved legacy PRD collision is explicitly blocking completion;
- `docs/agents/ticket-tracker.md` is canonical;
- the Agent skills block uses `### Ticket tracker`;
- live references to `issue-tracker.md` are updated;
- the legacy tracker document is removed;
- local active blocker references resolve and do not form a known cycle;
- remote identifiers and history remain stable unless mutations were explicitly approved;
- every preserved custom convention has exactly one home.
