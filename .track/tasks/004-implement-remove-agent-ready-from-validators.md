---
id: "004"
title: "[Implement] Remove agent_ready from validators and task rewrites"
status: done
mode: implement
priority: high
project_id: "0"
created: 2026-03-16
updated: 2026-03-17
depends_on:
  - "003"
files: []
pr: ""
---

## Context

### Problem
Remove all `agent_ready` usage from validators, models, parser, and list filtering so the codebase relies entirely on the new `mode` field and ready-gate model introduced by task 003.

### Cause
Task 003 moved `agent_ready` out of `TaskFrontmatter` and into a legacy compatibility path on `Task`/`TaskSummary`. The validator still has two rules keyed on `agent_ready` (triage warning in `schema.rs`, verification coupling in `structure.rs`), the parser still has `parse_legacy_agent_ready`, and the list command still filters on `agent_ready`. These must be removed to complete the migration.

### Affected Files
- `src/validator/schema.rs` — remove triage+agent_ready warning, add warn-if-agent_ready-present migration hint
- `src/validator/structure.rs` — remove agent_ready+verification coupling check
- `src/models/task.rs` — remove `agent_ready: bool` from `Task` and `TaskSummary`, remove `parse_legacy_agent_ready` call
- `src/parser/frontmatter.rs` — remove `parse_legacy_agent_ready` function
- `src/commands/list.rs` — remove `agent_ready` field from `TaskSummaryQuery` and filter logic
- `src/cli.rs` — remove `--agent-ready` from `ListArgs`
- `tests/phase7_validate.rs` — remove/update agent_ready test cases, add test for agent_ready-present warning
- Test fixtures (`tests/fixtures/valid_task.md` etc.) — remove `agent_ready` lines

### References
- Depends on: task 003
- Related: task 006 (replaces agent-ready list filter with mode/availability), task 008 (new validator rules)
- Contract: `docs/task-model-v2-contract.md` section 6

## Acceptance Criteria

- [x] `agent_ready` field removed from `Task` and `TaskSummary` structs
- [x] `parse_legacy_agent_ready` function removed from `src/parser/frontmatter.rs`
- [x] Validator no longer checks agent_ready for triage warning or verification coupling
- [x] Validator warns if `agent_ready` key is present in raw YAML (migration hint per contract section 6)
- [x] All test fixtures updated to remove `agent_ready` lines
- [x] `cargo test` passes with no agent_ready references in validator/model paths

## Verification

- `cargo test` — all phase7 validate tests pass
- `grep -r agent_ready src/` confirms only the migration-warn codepath remains
- `track validate` on the repo's own `.track/` tasks produces no errors

## Notes

- 2026-03-16 human: Left in triage pending final refinement after mode parsing exists.
- 2026-03-17 human: Refined acceptance criteria and affected files against current codebase; promoted to todo. Task 003 is done so dependency is satisfied.
