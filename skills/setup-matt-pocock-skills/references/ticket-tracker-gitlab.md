# Spec and Ticket Tracker: GitLab

Specs and tickets for this repository are represented by GitLab issues. Use the `glab` CLI for tracker operations.

## Core operations

- **Create a ticket:** `glab issue create --title "..." --description "..."`; publish blockers before blocked tickets.
- **Read a ticket:** `glab issue view <number> --comments`; use `-F json` when structured data is required.
- **List tickets:** `glab issue list -O json` with appropriate filters.
- **Comment:** `glab issue note <number> --message "..."`.
- **Label:** `glab issue update <number> --label "..."` or `--unlabel "..."`.
- **Claim:** `glab issue update <number> --assignee @me`.
- **Close:** post any closing note, then run `glab issue close <number>`.

Infer the project from the current clone's remote.

## Spec publishing

Publish the spec as one GitLab issue and apply the configured ready-state label. Resolve it from the `ready-for-agent` triage mapping when present; otherwise use the literal `ready-for-agent` label. That issue is the canonical parent source for tickets created from the spec. Keep it open and unchanged while publishing child tickets. An existing PRD issue is a legacy spec and keeps its title, number, URL, notes, and history.

## Ticket graph

- **Parent:** keep the source parent issue open and unchanged. Use a supported parent/child relationship when available; otherwise include `Parent: #<number>` in the ticket description.
- **Blocking edge:** prefer GitLab's native blocking link using the `/blocked_by #<number>` quick action in a note. On tiers without blocking links, use a `Blocked by: #<number>` description line.
- **Ready state:** apply the configured ready-state label resolved from the `ready-for-agent` mapping, or the literal `ready-for-agent` fallback when no triage mapping exists.
- **Frontier:** list open tickets in the approved graph, exclude assigned tickets and any ticket with an open native or textual blocker, then preserve the graph's dependency order. Query native links with `glab api projects/:id/issues/:iid/links` when required.

Native and textual edges must agree when both exist. A ticket becomes unblocked when every blocker is closed.

## Merge requests as a triage surface

**MRs as a request surface: no.** Set this to `yes` only when external merge requests enter the same triage state machine.

When enabled, use the `glab mr` equivalents for reading, diffing, listing, commenting, labelling, and closing. GitLab numbers issues and merge requests separately, so retain the surface type with every reference.

## Skill phrases

- **Publish a spec to the configured tracker:** create one GitLab issue containing the spec and apply the configured ready-state label.
- **Publish tickets to the configured tracker:** create one GitLab issue per ticket in dependency order and record its blocking edges.
- **Fetch the relevant ticket:** run `glab issue view <number> --comments` and retrieve relationship data needed to evaluate blockers.
- **Work the frontier:** choose an open, unassigned ticket whose blockers are all closed.

## Wayfinding operations

The map is one issue labelled `wayfinder:map`; child tickets carry `Part of #<map>` and `wayfinder:<type>` unless a native hierarchy is configured.

Use the same blocking-link and frontier rules as ordinary tickets. Claim before work. Resolve by posting the answer, closing the child, and appending a context pointer to the map's Decisions-so-far.
