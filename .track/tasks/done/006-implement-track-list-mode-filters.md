---
id: "006"
title: "[Implement] Replace agent-ready list filters with mode and availability filters"
status: done
mode: implement
priority: medium
type: improvement
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
Replace the `--agent-ready` boolean filter on `track list` with `--mode <mode>` and `--available` filters so the queue can be filtered by explicit task mode and by dependency-derived availability.

### Cause
The current `--agent-ready` flag filters on the legacy `agent_ready` boolean which is being removed. The contract (section 6) specifies replacing it with `--mode` (filters by TaskMode enum) and `--available` (filters to todo tasks with all depends_on resolved to done). Availability is computed at query time, not stored.

### Affected Files
- `src/cli.rs` — remove `agent_ready: bool` from `ListArgs`, add `mode: Option<TaskMode>` and `available: bool`
- `src/commands/list.rs` — replace agent_ready filter with mode filter and availability filter; availability = status==todo && all depends_on done
- `src/models/task.rs` — may need helper to compute availability from a summary + all task statuses
- `tests/phase5_commands.rs` — remove agent-ready filter tests, add mode and available filter tests
- `tests/help_snapshots.rs` — update help snapshot for `track list`

### References
- Depends on: task 003
- Related: task 004 (removes agent_ready from models), task 009 (snapshot migration), task 011 (index availability)
- Contract: `docs/task-model-v2-contract.md` section 4b (availability) and section 6 (`track list`)

## Acceptance Criteria

- [x] `--agent-ready` flag removed from `track list`
- [x] `--mode <mode>` filter added: shows only tasks with matching mode
- [x] `--available` flag added: shows only tasks in todo with all depends_on resolved to done
- [x] `--mode` and `--available` can be combined with existing filters (AND logic)
- [x] Help text updated; help snapshots regenerated
- [x] `cargo test` passes, including updated phase5 and help snapshot tests

## Verification

- `cargo test` — phase5 command tests and help snapshots pass
- `track list --mode implement` shows only implement-mode tasks
- `track list --available` shows only available todo tasks
- `track list --help` shows new flags, no `--agent-ready`

## Notes

- 2026-03-16 human: Left in triage because command-surface details still need refinement.
- 2026-03-17 human: Refined with concrete filter specs from the V2 contract. Task 003 is done; promoted to todo.
