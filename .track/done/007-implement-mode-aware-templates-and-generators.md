---
id: "007"
title: "[Implement] Update task templates, generators, and derived views for required dependencies"
status: done
mode: implement
priority: high
type: debt
scopes: []
project: task-model-v2
cycle: 2026-W12
created: 2026-03-16
updated: 2026-03-17
assigned_to:
pr:
depends_on: ["003"]
---

## Context

### Problem
Make Track generate task files and derived task views that match the new status-plus-mode contract instead of the old generic pre-`mode` template.

### Cause
The repository now has target templates, a clear matrix of `triage|todo` by `investigate|plan|implement`, and a dependency doctrine that requires explicit blockers and derived availability, so generator work can be scoped and assigned directly once `mode` exists in the schema.

### Affected Files
- `src/generator/template.rs`
- `task-templates/`
- `tests/fixtures/`
- `.track/index.json`
- `.track/BOARD.md`
- `tests/phase5_commands.rs`

### References
- Depends on: task 003
- Related: task 005

## Acceptance Criteria

- [x] Generator output can produce the appropriate status-plus-mode task contract with explicit `depends_on`
- [x] Generated templates and derived views align with the ready-gate and availability rules
- [x] Template, command, and derived-output tests cover the new output variants

## Verification

- Run `cargo test` — template, command, and derived-output tests stay green
- Compare generated task output against the intended status-plus-mode templates and dependency doctrine

## Notes

- 2026-03-16 human: Seeded as ready because the target template matrix already exists in the repo.
