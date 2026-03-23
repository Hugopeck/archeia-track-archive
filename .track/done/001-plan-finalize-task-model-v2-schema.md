---
id: "001"
title: "[Plan] Finalize task-model-v2 schema, dependency doctrine, and transition rules"
status: done
mode: plan
priority: high
type: spike
scopes: []
project: task-model-v2
cycle: "2026-W12"
created: 2026-03-16
updated: 2026-03-16
assigned_to:
pr:
depends_on: []
---

## Context

### Problem
Define the final task-model-v2 contract for status, mode, dependency semantics, availability, task validity, and transition semantics so implementation work can proceed without schema ambiguity.

### Cause
The current repository now has a target spec and project plan, but the migration still needs one implementation-facing planning artifact that freezes the exact schema, dependency doctrine, and command expectations before code changes begin.

### Affected Files
- `track-spec.md`
- `task-taxonomy.md`
- `task-model-v2-project-plan.md`
- `track-build-plan.md`

### References
- Related: task 002, task 003, task 010
- Root docs: `track-spec.md`, `task-taxonomy.md`, `task-model-v2-project-plan.md`

## Acceptance Criteria

- [x] A single implementation-facing schema contract is written down for `status`, `mode`, dependency semantics, and task validity rules
- [x] The allowed status transitions for the new model are explicit, including `todo -> triage` demotion and blocker-aware `todo -> active` rules
- [x] The migration tasks that follow have a stable contract to implement against, including required `depends_on` and derived availability

## Verification

- Read the final planning artifact and confirm it covers schema, dependency doctrine, transitions, and validation behavior
- Confirm task 003 through task 010 can reference this task without open contract questions about blockers or availability

## Notes

- 2026-03-16 human: Seeded migration project from the task-model-v2 project plan.
- 2026-03-16 agent: Wrote `docs/task-model-v2-contract.md` covering: frontmatter schema with mode enum and agent_ready removal, status transitions with guards, dependency doctrine (availability, reverse blockers, cycle detection), ready gates, command behavior changes, config changes, IndexTask v2 schema, and 9 ambiguity resolutions.
