---
id: "025"
title: "[Investigate] Decide whether task-model-v2 should bump schema_version"
status: done
mode: investigate
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
Produce a short findings note that answers one exact question: should Track keep `schema_version: "0.1"` for the shipped task-model-v2 behavior, or should it land a dedicated follow-up that bumps the repo to `"0.2"`? The output must compare the two options against the current code, checked-in config, docs, fixtures, and dogfooded `.track/` workspace, then recommend one path clearly enough to turn into a follow-up task.

### Cause
The behavioral migration shipped incrementally and never took a separate config-version migration. That left the code, spec examples, and dogfooded repo on `0.1` while some contract docs continued to describe `0.2` as if it were part of the completed rollout. The cleanup pass corrected the live docs to match current behavior, but it intentionally left the versioning decision unresolved.

### Affected Files
- `docs/task-model-v2-contract.md`
- `docs/task-model-v2-migration-risks.md`
- `track-spec.md`
- `.track/config.yaml`
- `src/models/config.rs`
- `tests/fixtures/minimal_config.yaml`
- `tests/fixtures/valid_config.yaml`
- `docs/schema-version-decision.md`

### References
- `README.md`
- `track-build-plan.md`
- `docs/archive/task-model-v2-project-plan.md`
- `docs/archive/ephemeral-derived-project-plan.md`

## Acceptance Criteria

- [x] The findings note states whether `schema_version` should stay `0.1` or move to `0.2`
- [x] The findings note names the code, docs, fixtures, and repo-migration consequences of the recommended path
- [x] The findings note lists the exact next implementation step or follow-up task implied by the recommendation

## Verification

- Confirm the findings note matches the current values in `.track/config.yaml`, `src/models/config.rs`, and fixture config files
- Confirm the findings note explains the current doc wording in `docs/task-model-v2-contract.md` and `docs/task-model-v2-migration-risks.md`

## Notes

- 2026-03-18 agent: Created during cleanup after finding behavior-level V2 completion but unresolved schema-version contract drift.
- 2026-03-18 agent: Added `docs/schema-version-decision.md`, linked it from the active docs surface, and aligned the contract note with the explicit keep-`0.1` decision.
