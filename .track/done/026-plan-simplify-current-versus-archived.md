---
id: "026"
title: "[Plan] Simplify current versus archived documentation hierarchy"
status: done
mode: plan
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
Produce a concrete documentation plan that defines where current behavior, doctrine, quick reference, contributor workflow, and historical migration context should live in this repository. The output should map each major markdown surface to one role, identify any remaining overlap between root docs and `docs/`, and propose a minimal sequence of follow-up tasks to make the hierarchy easier to navigate.

### Cause
The repo accumulated root-level plans, migration notes, and working docs while the product model was still changing. The cleanup pass moved completed migration plans into `docs/archive/`, but the repository still lacks an intentional information architecture that explains which files are canonical entry points and which files are historical support material.

### Affected Files
- `README.md`
- `docs/README.md`
- `track-spec.md`
- `track-build-plan.md`
- `task-taxonomy.md`
- `task-dependencies.md`
- `docs/archive/README.md`
- `docs/documentation-structure.md`

### References
- `docs/archive/task-model-v2-project-plan.md`
- `docs/archive/ephemeral-derived-project-plan.md`
- `docs/archive/dogfooding-guide.md`
- `docs/contributing.md`
- `docs/testing.md`

## Acceptance Criteria

- [x] The plan identifies the canonical home for current product behavior, doctrine, quick reference, contributor workflow, and historical context
- [x] The plan names any remaining files that should move, merge, or be retired, with reasons
- [x] The plan breaks the work into a small sequence of implementation tasks that can be handed off directly

## Verification

- Confirm the proposed hierarchy matches the current tracked markdown files and link structure
- Confirm the proposed follow-up sequence does not duplicate responsibilities already covered by `README.md` or `docs/README.md`

## Notes

- 2026-03-18 agent: Created during cleanup after moving completed migration plans under `docs/archive/`.
- 2026-03-18 agent: Added `docs/documentation-structure.md` mapping canonical current docs, archive roles, overlap boundaries, and recommended follow-up tasks.
