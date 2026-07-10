# Spec and Ticket Tracker: Local Markdown

Tickets and specs for this repository are represented by Markdown files under `.scratch/`.

## Layout

- One effort per directory: `.scratch/<feature-slug>/`.
- The canonical spec: `.scratch/<feature-slug>/spec.md`.
- Tickets: one file each at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order.
- Ready state: resolve the canonical `ready-for-agent` role to one concrete value during setup. Use the triage mapping when present; otherwise use the literal `ready-for-agent`.
- Status: a `Status:` line near the top. New executable specs and tickets use the configured ready-state value; ticket execution may transition them to `claimed` and `resolved`.
- Blocking edges: a `Blocked by:` line naming ticket numbers/titles, or `None — can start immediately`.
- Conversation history: append under `## Comments`.

The `issues/` directory name is a stable storage path. Its files are logical tickets.

## Spec publishing

Publish one root spec at `.scratch/<feature-slug>/spec.md` and record the configured ready-state value in a `Status:` line near the top. That file is the canonical parent source for the effort's tickets and remains unchanged while tickets are published. Treat an existing PRD as a legacy spec. If it already uses `spec.md`, keep it in place.

## Ticket graph

Publish blockers first and create one file per ticket. Keep acceptance criteria in the ticket file and preserve parent/spec references.

The frontier contains tickets whose `Status:` equals the configured ready-state value and whose blocker files are `resolved`. Scan files in numeric order after evaluating edges; the first eligible file is the default next ticket. Claim by setting `Status: claimed` before work. Resolve by completing criteria, recording evidence, and setting `Status: resolved`.

Every blocker reference must resolve within the effort or use an explicit external reference. The graph must be acyclic.

## Skill phrases

- **Publish a spec to the configured tracker:** create `.scratch/<feature-slug>/spec.md` and record the configured ready-state value.
- **Publish tickets to the configured tracker:** create `.scratch/<feature-slug>/issues/<NN>-<slug>.md` files in dependency order.
- **Fetch the relevant ticket:** read the referenced file and its parent spec.
- **Work the frontier:** scan active ticket files, discard blocked or claimed entries, and take the first remaining number.

## Wayfinding operations

Use `.scratch/<effort>/map.md` for the map and `.scratch/<effort>/issues/<NN>-<slug>.md` for child tickets. Record `Type:`, `Status:`, and `Blocked by:` near the top.

Claim by setting `Status: claimed`. Resolve by appending the answer, setting `Status: resolved`, and adding a context pointer to the map's Decisions-so-far.
