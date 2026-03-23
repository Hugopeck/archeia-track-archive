---
id: "032"
title: "[Investigate] Dry-run clean-clone install and release paths"
status: cancelled
mode: investigate
priority: high
type: spike
project: launch-readiness
created: 2026-03-22
updated: 2026-03-22
depends_on:
  - "028"
cancelled_reason: "Superseded by pure skill pack pivot"
---

## Context

### Problem
The launch story depends on clean-clone assumptions, GitHub release assets, and the generated CI/install flow being understandable from the outside, but the repo still needs a focused investigation that checks those assumptions from a launch-reader point of view.

### Affected Files
- README.md
- docs/ci-cd.md
- .github/workflows/release.yml
- .github/workflows/semantic-release.yml
- .github/workflows/track-ci.yml


### References
- README.md
- docs/ci-cd.md
- .github/workflows/release.yml
- .github/workflows/semantic-release.yml
- .github/workflows/track-ci.yml

## Acceptance Criteria

- [ ] Verify the clean-clone setup story against the current README and workflow files
- [ ] Verify the GitHub release asset names and install assumptions match the documented story
- [ ] Record concrete gaps or confusing steps discovered during the dry run
- [ ] Recommend the smallest follow-up changes needed before launch

## Verification

- Review `.github/workflows/release.yml`
- Review `.github/workflows/semantic-release.yml`
- Run `cargo run -- validate`

## Notes

- 2026-03-22 agent: This task should produce concrete findings, not vague confidence.
