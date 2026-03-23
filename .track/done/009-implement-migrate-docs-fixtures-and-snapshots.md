---
id: "009"
title: "[Implement] Migrate docs, fixtures, snapshots, and dogfooded examples to task-model-v2"
status: done
mode: implement
priority: medium
type: improvement
scopes: []
project: task-model-v2
cycle: 2026-W12
created: 2026-03-16
updated: 2026-03-18
assigned_to:
pr:
depends_on: ["004", "005", "006", "007", "008"]
---

## Context

### Problem
The repository still has canonical checked-in examples that do not match the current task-model-v2 contract. In particular, many dogfooded `.track/` task files still serialize deprecated `agent_ready` frontmatter, and some docs/tests still treat legacy compatibility cases as if they were canonical examples. Until those examples are migrated, Track's own repo drifts from the runtime contract and `track validate` emits avoidable migration warnings against the checked-in workspace.

### Cause
Tasks 004, 005, 006, 007, and 008 landed the runtime schema, template, list, and validation changes first, but the follow-up repo-content cleanup was left in triage until the implementation surface stabilized. This task should update only repo-owned canonical examples, fixtures, and golden outputs to the current `mode` + `depends_on` + derived-availability model. Non-goals: changing task-model semantics, inventing reverse-blocker runtime output before it exists, or rewriting historical migration docs/tests that intentionally cover deprecated `agent_ready` compatibility.

### Affected Files
- `.track/done/*.md` plus `.track/done/005-implement-track-new-require-mode.md` and `.track/done/009-implement-migrate-docs-fixtures-and-snapshots.md` — remove deprecated `agent_ready` frontmatter from the dogfooded workspace and keep checked-in task examples canonical
- `README.md`, `track-build-plan.md`, `task-model-v2-project-plan.md`, and `docs/task-model-v2-migration-risks.md` — align current status docs and historical migration context with the actual runtime contract
- `tests/conductor_workspace.rs`, `tests/phase5_commands.rs`, and `tests/phase6_build.rs` — add a repo-level proof for canonical dogfooded frontmatter and remove stale legacy helper signatures from default task-model-v2 test paths

### References
- Depends on: task 004, task 005, task 006, task 007, task 008
- Contract: `docs/task-model-v2-contract.md`
- Status and backlog context: `track-build-plan.md` Phase 11, `docs/task-model-v2-migration-risks.md`

## Acceptance Criteria

- [x] Every checked-in task file under `.track/` uses canonical task-model-v2 frontmatter with no `agent_ready` plus explicit `mode` and `depends_on`
- [x] User-facing docs and checked-in examples describe the current contract consistently: `--mode` is required, `depends_on` is required, `--available` is derived, and reverse blockers are described as remaining backlog where the code does not yet support them
- [x] Canonical fixtures, test helpers, and touched output assertions use task-model-v2 task shape by default; remaining `agent_ready` cases stay isolated to explicit compatibility tests
- [x] Any changed build/validate/help snapshots or inline golden outputs are updated in the same change and remain deterministic
- [x] Repo-level proof covers the migration surface: `cargo run -- validate`, `cargo run -- build`, `cargo check`, `cargo test`, `cargo clippy -- -D warnings`, and `cargo fmt --check` all succeed

## Verification

- `cargo run -- validate` — repo validates successfully and checked-in `.track/` tasks no longer emit deprecated-frontmatter warnings
- `cargo run -- build` — local derived views rebuild successfully after the dogfooded task migration
- `cargo test --test phase6_build --test phase7_validate --test validate_snapshots --test workflow_scenarios` — fixtures, golden outputs, and explicit compatibility coverage stay green
- `rg -n '^agent_ready:' .track tests/fixtures` — canonical checked-in task files and fixtures no longer carry the deprecated key

## Notes

- 2026-03-16 human: Left in triage because the exact migration surface depends on upstream implementation outcomes.
- 2026-03-18 agent: Refined the concrete repo migration surface from the current inventory and promoted the task to `todo`.
- 2026-03-18 agent: Removed deprecated `agent_ready` frontmatter from the checked-in dogfooded `.track/` tasks, added a repo-level regression test for canonical task-model-v2 frontmatter, cleaned stale legacy helper signatures from the canonical build/list test paths, aligned Phase 11 and migration-risk docs with the current implementation state, and re-ran repo proofs (`cargo run -- validate`, `cargo run -- build`, `cargo check`, `cargo test`, `cargo clippy -- -D warnings`, `cargo fmt --check`).
