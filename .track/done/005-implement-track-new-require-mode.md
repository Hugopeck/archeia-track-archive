---
id: "005"
title: "[Implement] Make track new require mode, emit depends_on, and support direct todo creation"
status: done
mode: implement
priority: high
type: improvement
scopes: []
project: task-model-v2
cycle: 2026-W12
created: 2026-03-16
updated: 2026-03-18
assigned_to:
pr:
depends_on: ["003"]
---

## Context

### Problem
Update `track new` so `--mode` is a required argument, `depends_on: []` is always emitted, `agent_ready` is never emitted, and a `--status todo` flag validates the ready gate before creating the file.

### Cause
Task 003 added the `mode` field to the schema, and the template already emits `mode` and `depends_on: []`. But `--mode` is still optional (defaults to implement), and there is no path to create a task directly in todo with ready-gate validation. The contract (section 6) requires `--mode` to be mandatory and `--status todo` to enforce the gate.

### Affected Files
- `src/cli.rs` — change `mode: Option<TaskMode>` to required `mode: TaskMode`
- `src/commands/new.rs` — remove mode defaulting to Implement, accept required mode, add `--status todo` flag with ready-gate validation before file creation
- `src/generator/template.rs` — confirm template already emits `depends_on: []` and `mode` (no changes expected)
- `tests/phase5_commands.rs` — update new-task tests to always pass `--mode`, add tests for `--status todo` with passing/failing ready gate

### References
- Depends on: task 003
- Related: task 002 (demotion UX, done), task 007 (mode-aware templates, done)
- Contract: `docs/task-model-v2-contract.md` section 6 (`track new`)

## Acceptance Criteria

- [x] `track new` errors if `--mode` is not provided
- [x] `depends_on: []` is always present in generated task files
- [x] `agent_ready` is never emitted in generated task files
- [x] `track new --status todo --mode implement` validates the ready gate before creating; rejects if gate fails
- [x] `track new --mode investigate "question"` creates a triage task with mode=investigate
- [x] Help text and examples updated for required `--mode`
- [x] `cargo test` passes, including updated phase5 command tests

## Verification

- `cargo test` — phase5 command tests pass
- `track new --mode implement "test task"` creates correct file in `.track/triage/`
- `track new "test task"` (no mode) errors with a clear message
- `track new --status todo --mode implement "test task"` with incomplete body is rejected

## Notes

- 2026-03-16 human: Left in triage until task 002 clarifies demotion UX and task 003 lands mode support.
- 2026-03-17 human: Refined with concrete acceptance criteria and verification. Tasks 002, 003, and 007 are all done; promoted to todo.
- 2026-03-18 agent: Verified the CLI contract (`--mode` required, ready-gated `--status todo`, canonical `depends_on`, no emitted `agent_ready`) and ran `cargo test`, plus focused `ux_contracts`, `help_snapshots`, and `phase5_commands`; task moved through `active` and `review` to `done`.
