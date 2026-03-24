---
id: "033"
title: "[Investigate] Dogfood hybrid workflow in a scratch repo"
status: cancelled
mode: investigate
priority: high
project_id: "0"
created: 2026-03-22
updated: 2026-03-22
depends_on:
  - "029"
  - "030"
  - "031"
files: []
pr: ""
cancelled_reason: "Superseded by pure skill pack pivot"
---

## Context

### Problem
The hybrid launch is only credible if a scratch repository can follow the current bootstrap, docs, and skill guidance without depending on Track-internal tribal knowledge, so the repo needs a dogfooding pass that captures real rough edges.

### Affected Files
- README.md
- docs/manual-smoke-tests.md
- docs/specs/track-spec.md
- .claude/skills/


### References
- README.md
- docs/manual-smoke-tests.md
- docs/specs/track-spec.md
- .claude/skills/

## Acceptance Criteria

- [ ] Exercise the hybrid flow in a scratch repo from initialization through validation and board generation
- [ ] Use the repo-local skills as the primary orchestration path during the dogfood pass
- [ ] Record concrete friction points, confusing copy, or missing steps
- [ ] Turn any discovered blockers into follow-up tasks or directly linked fixes

## Verification

- Run the documented smoke flow in a scratch repo
- Run `cargo run -- validate`
- Capture the findings in task notes or linked follow-up tasks

## Notes

- 2026-03-22 agent: This task depends on the skill and docs work so the dogfood pass reflects the intended launch surface.
