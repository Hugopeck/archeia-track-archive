---
id: "030"
title: "[Implement] Publish launch-ready quickstart and migration guide"
status: cancelled
mode: implement
priority: high
type: improvement
project: launch-readiness
created: 2026-03-22
updated: 2026-03-22
depends_on:
  - "028"
cancelled_reason: "Superseded by pure skill pack pivot"
---

## Context

### Problem
The repo documents the hybrid model, but launch readers still need a tighter quickstart and a clearer migration path from the retired orchestration CLI to the validate-plus-skills workflow before the project is easy to adopt.

### Affected Files
- README.md
- docs/README.md
- docs/commands.md
- docs/specs/track-spec.md
- docs/specs/track-build-plan.md
- docs/manual-smoke-tests.md

### References
- README.md
- docs/specs/track-spec.md
- docs/specs/track-build-plan.md
- archive/legacy-orchestration/README.md

## Acceptance Criteria

- [ ] Add a concise launch-ready quickstart that explains how to bootstrap, validate, build, and use the skill pack
- [ ] Add a migration section that explains what happened to `track new`, `move`, `list`, `show`, `stats`, and `completions`
- [ ] Make the docs index route launch readers to the correct current docs and not the archived surface
- [ ] Keep doc claims aligned with what the current code and tests really ship

## Verification

- Run `cargo test --test documentation_cleanup --test docs_quick_reference`
- Run `cargo run -- validate`
- Review the updated docs links manually

## Notes

- 2026-03-22 agent: This task covers the reader-facing launch narrative rather than adding more product surface.
