---
id: "013"
title: "[Implement] Remove freshness validation and gitattributes generation"
status: done
mode: implement
priority: high
type: debt
scopes: []
project: ephemeral-derived
cycle:
created: 2026-03-17
updated: 2026-03-17
assigned_to:
pr:
depends_on: []
---

## Context

### Problem
Remove the freshness validation module and the `.gitattributes` merge=ours generation from Track. With derived files becoming ephemeral, there is nothing to check for staleness and no merge strategy to configure.

### Cause
`src/validator/freshness.rs` currently regenerates expected `index.json` and `BOARD.md` in memory and diffs them against committed versions. `src/commands/init.rs` appends `merge=ours` entries to `.gitattributes`. Both become dead code under the ephemeral model.

### Affected Files
- `src/validator/freshness.rs` — remove or gut entirely
- `src/commands/validate.rs` — remove `validator::freshness::validate()` call
- `src/commands/init.rs` — remove `append_gitattributes()` function and call
- `src/validator/mod.rs` — remove freshness module declaration if needed

### References
- Contract: `ephemeral-derived-project-plan.md`

## Acceptance Criteria

- [x] `src/validator/freshness.rs` no longer performs freshness checks
- [x] `track validate` succeeds without `index.json` or `BOARD.md` existing on disk
- [x] `track init` does not modify `.gitattributes`
- [x] `cargo test` passes

## Verification

- Run `track validate` in a repo with no `index.json` or `BOARD.md` — succeeds
- Run `track init` in a fresh directory — confirm no `.gitattributes` entries for derived files
- Run `cargo test` — all green

## Notes

- 2026-03-17 human: Seeded from ephemeral-derived-project-plan.md.
- 2026-03-17 agent: Reviewed against `src/commands/validate.rs`, `src/commands/init.rs`, and focused tests; acceptance criteria satisfied.
