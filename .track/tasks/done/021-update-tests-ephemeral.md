---
id: "021"
title: "[Implement] Update tests and fixtures for ephemeral model"
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
depends_on: ["013", "014"]
---

## Context

### Problem
Several test files validate the old committed-derived-files behavior: freshness validation tests check for stale/missing `index.json` and `BOARD.md`, and init tests verify `.gitattributes` creation. These must be removed or rewritten.

### Cause
Dead tests that assert removed behavior will either fail or give false confidence. Tests must match the new ephemeral model.

### Affected Files
- `tests/phase7_validate.rs` — remove freshness validation tests (~lines 478-530)
- `src/commands/init.rs` — update tests for `.gitignore` instead of `.gitattributes` (~lines 181-230)

### References
- Depends on: tasks 013, 014
- Contract: `ephemeral-derived-project-plan.md`

## Acceptance Criteria

- [x] No tests assert freshness validation of `index.json` or `BOARD.md`
- [x] Init tests verify `.track/.gitignore` creation instead of `.gitattributes` merge entries
- [x] `cargo test` passes with all changes applied

## Verification

- Run `cargo test` — all green
- Search test files for "freshness", "stale_index", "stale_board", "gitattributes" — no active test assertions

## Notes

- 2026-03-17 human: Seeded from ephemeral-derived-project-plan.md.
- 2026-03-17 human: Moved to todo; project plan serves as the contract (task 012 deleted).
- 2026-03-17 agent: Renamed the last freshness-era validate fixture, replaced the obsolete init `.gitattributes` test with `.track/.gitignore` coverage, and rechecked the docs guards so task-021 verification stays clean.
