# Spec and Ticket Tracker: GitHub

Specs and tickets for this repository are represented by GitHub issues. Use the `gh` CLI for tracker operations.

## Core operations

- **Create a ticket:** `gh issue create --title "..." --body "..."`; publish blockers before blocked tickets.
- **Read a ticket:** `gh issue view <number> --comments`, including labels and relationship data when relevant.
- **List tickets:** `gh issue list --state open --json number,title,body,labels,assignees` with appropriate filters.
- **Comment:** `gh issue comment <number> --body "..."`.
- **Label:** `gh issue edit <number> --add-label "..."` or `--remove-label "..."`.
- **Claim:** `gh issue edit <number> --add-assignee @me`.
- **Close:** `gh issue close <number> --comment "..."`.

Infer the repository from the current clone's remote.

## Spec publishing

Publish the spec as one GitHub issue and apply the configured ready-state label. Resolve it from the `ready-for-agent` triage mapping when present; otherwise use the literal `ready-for-agent` label. That issue is the canonical parent source for tickets created from the spec. Keep it open and unchanged while publishing child tickets. An existing PRD issue is a legacy spec and keeps its title, number, URL, comments, and history.

## Ticket graph

- **Parent:** keep the source parent issue open and unchanged. Use GitHub sub-issues when available; otherwise include a `Parent` reference in the ticket body.
- **Blocking edge:** prefer GitHub's native issue dependencies. Add an edge with `gh api --method POST repos/<owner>/<repo>/issues/<blocked>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, where the database ID comes from `gh api repos/<owner>/<repo>/issues/<number> --jq .id`. Fall back to a `Blocked by: #<number>` body line when dependencies are unavailable.
- **Ready state:** apply the configured ready-state label resolved from the `ready-for-agent` mapping, or the literal `ready-for-agent` fallback when no triage mapping exists.
- **Frontier:** list open tickets in the approved graph, exclude assigned tickets and any ticket with an open native or textual blocker, then preserve the graph's dependency order.

Native and textual edges must agree when both exist. A ticket becomes unblocked when every blocker is closed.

## Pull requests as a triage surface

**PRs as a request surface: no.** Set this to `yes` only when external PRs enter the same triage state machine.

When enabled, use `gh pr view`, `gh pr diff`, `gh pr list`, `gh pr comment`, `gh pr edit`, and `gh pr close`. Keep only external authors when building a triage queue. GitHub shares issue and PR numbers, so resolve an ambiguous `#42` as a PR first and fall back to an issue.

## Skill phrases

- **Publish a spec to the configured tracker:** create one GitHub issue containing the spec and apply the configured ready-state label.
- **Publish tickets to the configured tracker:** create one GitHub issue per ticket in dependency order and record its blocking edges.
- **Fetch the relevant ticket:** run `gh issue view <number> --comments` and retrieve relationship data needed to evaluate blockers.
- **Work the frontier:** choose an open, unassigned ticket whose blockers are all closed.

## Wayfinding operations

The map is one issue labelled `wayfinder:map`; its child tickets are sub-issues when available or carry `Part of #<map>`. Label each child `wayfinder:<type>`.

Use the same native dependency and frontier rules as ordinary tickets. Claim before work. Resolve by commenting with the answer, closing the child, and appending a context pointer to the map's Decisions-so-far.
