---
id: "029"
title: "[Implement] Ship remaining planning and triage workflow skills"
status: cancelled
mode: implement
priority: high
project_id: "0"
created: 2026-03-22
updated: 2026-03-22
depends_on:
  - "028"
files: []
pr: ""
cancelled_reason: "Superseded by pure skill pack pivot"
---

## Context

### Problem
The repo-local skill pack now covers creation, movement, listing, showing, board reading, and stats, but the launch story still has a gap around the higher-level planning helpers that Option C explicitly called out for triage and planning workflows.

### Affected Files
- .claude/skills/track-triage/SKILL.md
- .claude/skills/track-triage/agents/openai.yaml
- .claude/skills/track-plan/SKILL.md
- .claude/skills/track-plan/agents/openai.yaml
- docs/README.md
- docs/commands.md
- docs/specs/track-spec.md
- docs/specs/track-build-plan.md
- tests/skill_pack.rs

### References
- docs/specs/track-spec.md
- docs/specs/track-build-plan.md
- .context/attachments/plan.md

## Acceptance Criteria

- [ ] Add a repo-local `track-triage` skill focused on refining incomplete work in `.track/triage/`
- [ ] Add a repo-local `track-plan` skill focused on sequencing and dependency planning for ready work
- [ ] Document both skills in the active docs alongside the existing skill pack
- [ ] Extend `tests/skill_pack.rs` to prove the new skills exist and point back to active docs plus validation flows

## Verification

- Run `cargo test --test skill_pack`
- Run `cargo run -- validate`
- Run `cargo fmt --check`

## Notes

- 2026-03-22 agent: Seeded from the launch-readiness planning pass so the launch story includes the higher-level skills promised by Option C.
