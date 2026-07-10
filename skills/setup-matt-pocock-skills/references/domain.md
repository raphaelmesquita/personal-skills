# Domain Docs

Define how engineering skills consume this repository's domain language and architectural decisions.

## Read before exploration

- Read root `CONTEXT.md`, or use root `CONTEXT-MAP.md` to locate the relevant context glossary.
- Read relevant ADRs under `docs/adr/` and context-scoped ADR directories.
- Proceed when these files are absent; create domain docs lazily through the repository's domain-modeling flow when terms or decisions are resolved.

## Layout

Use a root `CONTEXT.md` and `docs/adr/` for a single-context repository. For a genuine multi-context repository, use root `CONTEXT-MAP.md`, system-wide `docs/adr/`, and a `CONTEXT.md` plus ADR directory inside each context.

## Vocabulary and decisions

Use glossary terms in ticket titles, descriptions, tests, and architectural work. Treat an undefined term as a prompt to verify repository language or record a domain-modeling gap.

Surface any conflict with an existing ADR explicitly and identify the concrete evidence for reopening it.
