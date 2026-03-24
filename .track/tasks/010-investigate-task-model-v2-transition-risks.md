---
id: "010"
title: "[Investigate] Identify transition risks in migrating existing repos to task-model-v2"
status: done
mode: investigate
priority: medium
project_id: "0"
created: 2026-03-16
updated: 2026-03-16
depends_on:
  - "001"
files: []
pr: ""
---

## Context

### Problem
Identify the highest-risk migration edges for repositories that already use the current Track task schema so the code migration does not strand existing tasks, dependency graphs, or docs in an inconsistent state.

### Cause
The repository now has a target model, but we still need one explicit investigation into compatibility risks around existing tasks, generated files, help/output contracts, and how older repos will backfill dependency data.

### Affected Files
- `track-spec.md`
- `track-build-plan.md`
- `tests/fixtures/`
- `.track/`

### References
- Depends on: task 001
- Related: task 009
- Investigation output: `docs/task-model-v2-migration-risks.md`

## Acceptance Criteria

- [x] The major migration risks are written down explicitly
- [x] The investigation covers how existing task files can be migrated safely, including backfilling `depends_on: []`
- [x] The output is specific enough to guide later implementation and fixture migration work

## Verification

- Read the investigation output and confirm it lists concrete risks and recommendations
- Confirm the recommendations are actionable for follow-up implementation tasks

## Notes

- 2026-03-16 human: Created as a ready investigation task to de-risk the migration sequence.
- 2026-03-16 agent: Wrote `docs/task-model-v2-migration-risks.md` covering the rollout order, `depends_on: []` backfill guidance, CLI/derived-file compatibility risks, fixture migration sequencing, and the dogfooded repo migration checklist.
