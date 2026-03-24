---
id: "017"
title: "[Implement] Update track-spec.md for ephemeral derived files"
status: done
mode: implement
priority: medium
project_id: "0"
created: 2026-03-17
updated: 2026-03-17
depends_on: []
files: []
pr: ""
---

## Context

### Problem
`track-spec.md` currently describes `index.json` and `BOARD.md` as committed artifacts with `.gitattributes` merge=ours strategy and freshness validation. These sections must be updated to describe the ephemeral model.

### Cause
The spec is the authoritative target document. If it describes committed derived files, implementers will build the wrong thing.

### Affected Files
- `track-spec.md` — multiple sections

### References
- Contract: `ephemeral-derived-project-plan.md`
- Sections to update: `track init`, `track build`, `track validate`, CI Integration, Folder Structure, Why derived files

## Acceptance Criteria

- [x] `track init` section describes `.track/.gitignore` creation instead of `.gitattributes` merge strategy
- [x] `track build` section describes ephemeral "refresh local view" pattern
- [x] `track validate` section no longer lists freshness checking
- [x] CI Integration section shows separate validate/build steps
- [x] Folder structure diagram shows `.gitignore` in `.track/` and marks `index.json`/`BOARD.md` as local-only
- [x] "Why derived files" design decision explains the ephemeral model and the merge-conflict motivation

## Verification

- Read each updated section and confirm it accurately describes the ephemeral behavior
- Confirm no remaining references to committed derived files, `.gitattributes` merge strategy, or freshness validation for derived files

## Notes

- 2026-03-17 human: Seeded from ephemeral-derived-project-plan.md.
- 2026-03-17 agent: Reviewed the `track init`, `track build`, `track validate`, CI, folder structure, and rationale sections; spec matches the ephemeral-derived model.
