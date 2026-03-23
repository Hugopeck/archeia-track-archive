---
id: "027"
title: "[Implement] Replace archived dogfooding guidance with current smoke-test docs"
status: done
mode: implement
priority: medium
type: improvement
scopes: []
project:
cycle:
created: 2026-03-18
updated: 2026-03-18
assigned_to:
pr:
depends_on: []
---

## Context

### Problem
Create a current smoke-test document for contributors that lists only the manual checks still worth running now that command contracts are already covered by automated tests. The change should add or update an active doc, link it from the current documentation surface, and make the manual guidance explicitly point contributors at the relevant automated suites instead of repeating them.

### Cause
The old manual dogfooding guide was archived because it contained outdated assumptions about `.gitattributes` and derived-file freshness checks. Archiving removed the stale advice from the active surface, but it also left the repository without a concise replacement for lightweight manual verification guidance.

### Affected Files
- `docs/testing.md`
- `docs/README.md`
- `README.md`
- `docs/archive/dogfooding-guide.md`
- `tests/workflow_scenarios.rs`
- `tests/phase5_commands.rs`
- `tests/phase6_build.rs`
- `tests/phase7_validate.rs`
- `docs/manual-smoke-tests.md`
- `tests/documentation_cleanup.rs`

### References
- `docs/contributing.md`
- `docs/commands.md`
- `track-spec.md`

## Acceptance Criteria

- [x] The replacement doc lists only current manual smoke tests that provide value beyond automated coverage
- [x] The replacement doc points contributors at the existing automated suites that cover the rest of the contract
- [x] The active docs link to the replacement guidance and do not send contributors to the archived dogfooding guide for current workflow instructions

## Verification

- Run `cargo test`
- Run `cargo run -- validate`
- Confirm the new smoke-test doc and links do not reference `.gitattributes` or derived-file freshness checks

## Notes

- 2026-03-18 agent: Created during cleanup after archiving the stale dogfooding guide.
- 2026-03-18 agent: Added `docs/manual-smoke-tests.md`, linked it from `docs/testing.md` and `docs/README.md`, and added doc-proof coverage in `tests/documentation_cleanup.rs`.
