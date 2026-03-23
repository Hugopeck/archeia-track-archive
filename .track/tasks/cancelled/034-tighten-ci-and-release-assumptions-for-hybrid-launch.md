---
id: "034"
title: "[Implement] Tighten CI and release assumptions for hybrid launch"
status: cancelled
mode: implement
priority: high
type: infra
project: launch-readiness
created: 2026-03-22
updated: 2026-03-22
depends_on:
  - "032"
cancelled_reason: "Superseded by pure skill pack pivot"
---

## Context

### Problem
If the clean-clone and release-path investigation finds mismatches, the repo will need targeted workflow, docs, or generated-artifact fixes so the hybrid launch does not rely on assumptions that only work for maintainers who already know the codebase.

### Affected Files
- .github/workflows/track-ci.yml
- .github/workflows/release.yml
- .github/workflows/semantic-release.yml
- docs/ci-cd.md
- README.md
- src/generator/ci.rs
- tests/release_automation.rs

### References
- .github/workflows/track-ci.yml
- .github/workflows/release.yml
- .github/workflows/semantic-release.yml
- docs/ci-cd.md
- tests/release_automation.rs

## Acceptance Criteria

- [ ] Apply the minimal fixes needed to make CI and release assumptions match the hybrid launch story
- [ ] Keep generated workflow artifacts and generators aligned in the same change
- [ ] Preserve the crates.io publish contract and existing release automation expectations
- [ ] Add or update tests when the launch hardening changes repo behavior

## Verification

- Run `cargo test --test release_automation`
- Run `cargo run -- validate`
- Run `cargo clippy -- -D warnings`

## Notes

- 2026-03-22 agent: Scope this to real launch blockers found by task 032, not speculative workflow churn.
