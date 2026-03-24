---
id: "003"
title: "[Implement] Add task mode enum and frontmatter schema support"
status: done
mode: implement
priority: high
project_id: "0"
created: 2026-03-16
updated: 2026-03-17
depends_on:
  - "001"
files: []
pr: ""
---

## Context

### Problem
Introduce an explicit task `mode` field into the Track data model and parsing layer so the new target model can stop relying on the overloaded `agent_ready` boolean.

### Cause
All later command, validator, and generator changes depend on the parser and frontmatter model understanding `mode: investigate|plan|implement` first.

### Affected Files
- `src/models/task.rs`
- `src/models/enums.rs`
- `src/parser/frontmatter.rs`
- `tests/fixtures/`

### References
- Depends on: task 001
- Related: task 004, task 005, task 006, task 007, task 008

## Acceptance Criteria

- [x] Track can parse and serialize a required `mode` field with the values `investigate`, `plan`, and `implement`
- [x] The core task frontmatter model no longer needs `agent_ready` in the target schema path and preserves explicit `depends_on` data deterministically
- [x] Fixtures and parser tests cover the new `mode` field contract

## Verification

- Run `cargo test` — parser and model tests stay green
- Read the updated task model and confirm `mode` is required and typed

## Notes

- 2026-03-16 human: Seeded as a ready implementation task because the target files and output are explicit.
- 2026-03-17 codex: Removed `agent_ready` from the core `TaskFrontmatter` schema path, kept legacy compatibility reads on `Task` and `TaskSummary`, and added parser/model coverage for the hybrid migration state.
