---
id: "011"
title: "[Implement] Add derived availability to index.json"
status: done
mode: implement
priority: high
type: improvement
scopes: []
project: task-model-v2
cycle: "2026-W12"
created: 2026-03-16
updated: 2026-03-17
assigned_to:
pr:
depends_on: ["003", "007"]
---

## Context

### Problem
Expose derived task availability in `.track/index.json` so agents and tooling can tell which ready tasks are actually startable without parsing `BOARD.md`.

### Cause
The board now derives and displays todo availability from dependency completion, but the machine-readable index still lacks that derived signal. Agents should be able to consume availability directly from `index.json`.

### Affected Files
- `src/models/index.rs`
- `src/generator/index.rs`
- `src/generator/board.rs`
- `.track/index.json`
- `tests/output_snapshots.rs`
- `tests/phase6_build.rs`

### References
- Depends on: task 003, task 007
- Related: task 006

## Acceptance Criteria

- [x] `index.json` includes a derived availability field for the relevant task summaries
- [x] Availability is computed from dependency completion rather than stored in task frontmatter
- [x] Generator tests and snapshots cover the new machine-readable availability contract

## Verification

- Run `cargo test` — index generator and snapshot tests stay green
- Inspect the generated `.track/index.json` and confirm availability is present and derived correctly

## Notes

- 2026-03-16 human: Added after board availability landed so agents can consume the same signal from the index.
- 2026-03-17 agent: Added derived `available` to `index.json`, updated the board generator to read the same signal, and covered the contract with generator, build, and snapshot tests.
