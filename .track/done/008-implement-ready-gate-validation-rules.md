---
id: "008"
title: "[Implement] Rewrite validator rules around minimum task definition, dependency integrity, and ready gates"
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
depends_on: ["001"]
---

## Context

### Problem
Update `track validate` to enforce the V2 contract: minimum task definition in triage, mode-specific ready gates for todo and beyond, dependency integrity (self-reference, cycles), blocker-aware status rules, and `depends_on` source-presence checking.

### Cause
The current validator checks field values and basic structure but lacks: cycle detection in the dependency graph, self-reference detection, ready-gate enforcement for non-triage tasks, blocker checks for active/review/done, and source-level `depends_on` presence validation. The V2 contract (section 5, 6) specifies all of these.

### Affected Files
- `src/validator/schema.rs` — add ready-gate enforcement for todo/active/review/done; add blocker check for active/review/done; add `depends_on` YAML source-presence check
- `src/validator/structure.rs` — add `### Affected Files` content check as part of ready gate; ensure verification requirement applies to all non-triage tasks
- `src/validator/consistency.rs` — add cycle detection (DFS walk), add self-reference check
- `tests/phase7_validate.rs` — add tests for: cycle detection error, self-reference error, ready-gate failure on todo task, blocker-unfinished error on active task, depends_on absent from YAML source error

### References
- Depends on: task 001
- Related: task 004 (removes agent_ready validator rules), task 002 (demotion UX)
- Contract: `docs/task-model-v2-contract.md` sections 4f, 4g, 5, 6

## Acceptance Criteria

- [x] Validator errors if `depends_on` key is absent from YAML source (not just empty — actually missing)
- [x] Validator errors on self-referencing `depends_on` (task lists own ID)
- [x] Validator errors on dependency cycles (A→B→A, or longer chains)
- [x] Validator errors if todo/active/review/done task fails ready gate (Problem ≥20 chars, Affected Files has content, ≥1 AC, Verification has content)
- [x] Validator errors if active/review/done task has depends_on targets not in done status
- [x] Triage tasks are exempt from ready-gate enforcement
- [x] All new rules have corresponding test cases in `tests/phase7_validate.rs`
- [x] `cargo test` passes

## Verification

- `cargo test` — all phase7 validate tests pass
- Create a task in todo with empty verification → `track validate` errors
- Create two tasks with circular depends_on → `track validate` errors
- Create an active task with an undone blocker → `track validate` errors
- `track validate` on the repo's own `.track/` tasks passes clean

## Notes

- 2026-03-16 human: Left in triage because validator scope still needs one more planning pass.
- 2026-03-17 human: Refined with exact rules from V2 contract sections 4-6. Task 001 is done; promoted to todo.
