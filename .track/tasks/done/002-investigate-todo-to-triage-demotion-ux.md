---
id: "002"
title: "[Investigate] Decide whether todo-to-triage demotion needs explicit CLI UX"
status: done
mode: investigate
priority: medium
type: spike
scopes: []
project: task-model-v2
cycle: "2026-W12"
created: 2026-03-16
updated: 2026-03-16
assigned_to:
pr:
depends_on: ["001"]
---

## Context

### Problem
Determine how explicit Track should be when a task that was thought to be ready in `todo` turns out to have an incomplete assignment contract and must move back to `triage`.

### Cause
The new target model makes `todo -> triage` a meaningful demotion, but the repository had not yet decided whether that needs dedicated CLI messaging, notes guidance, or extra transition hints.

### Affected Files
- `track-spec.md`
- `docs/task-model-v2-contract.md`
- `task-model-v2-project-plan.md`
- `track-build-plan.md`

### References
- Depends on: task 001
- Related: task 005, task 008

## Acceptance Criteria

- [x] A clear recommendation exists for whether `todo -> triage` needs dedicated CLI UX beyond normal move behavior
- [x] The recommendation names any required help text, note guidance, or transition messaging
- [x] The recommendation is concrete enough for a follow-up implementation task to execute directly

## Verification

- Read the investigation output and confirm it ends with one explicit recommendation
- Confirm the output names affected command/error surfaces if extra UX is recommended

## Notes

- 2026-03-16 human: Created as a ready investigation task because the question and output are already clear.
- 2026-03-16 agent: Recommendation: keep `todo -> triage` as plain `track move <id> triage` with no dedicated flag, no extra frontmatter, and no transition-specific prompt.
- 2026-03-16 agent: Follow-up surfaces are the target docs and planned `track move` help/examples so the demotion remains discoverable; if context matters, capture it in `## Notes` rather than adding demotion metadata.
