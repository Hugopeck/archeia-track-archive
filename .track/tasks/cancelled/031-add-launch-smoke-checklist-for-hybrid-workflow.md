---
id: "031"
title: "[Implement] Add launch smoke checklist for hybrid workflow"
status: cancelled
mode: implement
priority: high
type: infra
project: launch-readiness
created: 2026-03-22
updated: 2026-03-22
depends_on:
  - "028"
cancelled_reason: "Superseded by pure skill pack pivot"
---

## Context

### Problem
Before launch, the repo needs a single smoke-test checklist that exercises the current hybrid workflow from bootstrap through validation and derived views so maintainers know exactly what to rerun before cutting a release.

### Affected Files
- docs/manual-smoke-tests.md
- docs/testing.md
- README.md
- tests/skill_pack.rs

### References
- docs/manual-smoke-tests.md
- docs/testing.md
- conductor.json
- docs/conductor-workspace.md

## Acceptance Criteria

- [ ] Add a launch-oriented smoke checklist that covers `track init`, `track validate`, `track build`, and the repo-local skill pack
- [ ] Make the checklist explicit about what still requires human eyes versus what is already automated
- [ ] Keep the active test docs aligned with the launch checklist
- [ ] Avoid reintroducing archived workflow assumptions or stale derived-file guidance

## Verification

- Run `cargo test --test documentation_cleanup --test skill_pack`
- Run `cargo run -- validate`
- Review the smoke checklist end-to-end in the docs

## Notes

- 2026-03-22 agent: This task exists so launch validation is repeatable rather than spread across several docs.
