# Triage Labels

Map the five canonical triage roles to the strings used by the configured ticket representation.

| Canonical role | Tracker value | Meaning |
| --- | --- | --- |
| `needs-triage` | `needs-triage` | Maintainer evaluation required |
| `needs-info` | `needs-info` | Waiting for reporter information |
| `ready-for-agent` | `ready-for-agent` | Spec or ticket is fully specified and agent-executable |
| `ready-for-human` | `ready-for-human` | Ticket requires human implementation |
| `wontfix` | `wontfix` | Ticket will not be actioned |

When a skill names a canonical role, use its mapped tracker value. For local Markdown, store the value in `Status:`. For a remote tracker, apply the corresponding label.

Edit only the Tracker value column when the repository already has another vocabulary.
