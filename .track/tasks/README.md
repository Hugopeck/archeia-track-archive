# Track Tasks

This directory contains Track's operational work items, grouped by workflow state.

## Layout

- `triage/` — not yet ready to work
- `todo/` — ready to be claimed and worked
- `active/` — currently being worked
- `review/` — awaiting review
- `done/` — completed
- `cancelled/` — cancelled historical tasks
- `claims/` — advisory claim files for active coordination

## Conventions

- Task files use the path `.track/tasks/{status}/{id}-{slug}.md`
- Active tasks use dotted IDs like `1.2` or `4.6`
- Legacy numeric IDs remain valid only for historical archived tasks
- Claims live in `claims/` and reference task IDs, not filenames

See `.track/PROTOCOL.md` for the full contract.
