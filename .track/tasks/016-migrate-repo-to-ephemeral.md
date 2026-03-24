---
id: "016"
title: "[Implement] Migrate this repo's .track/ to ephemeral derived files"
status: done
mode: implement
priority: medium
project_id: "0"
created: 2026-03-17
updated: 2026-03-17
depends_on:
  - "013"
  - "014"
files: []
pr: ""
---

## Context

### Problem
This repo still tracks `index.json` and `BOARD.md` in git. It needs to finish migrating to the ephemeral model by removing them from version control and relying on the existing `.track/.gitignore`.

### Cause
Track should dogfood its own ephemeral derived files model.

### Affected Files
- `.track/.gitignore` — keep `index.json` and `BOARD.md` ignored
- `.track/index.json` — stop tracking it in git
- `.track/BOARD.md` — stop tracking it in git

### References
- Depends on: tasks 013, 014
- Contract: `ephemeral-derived-project-plan.md`

## Acceptance Criteria

- [x] `.gitattributes` no longer contains `merge=ours` entries for derived files
- [x] `.track/.gitignore` exists with `index.json` and `BOARD.md`
- [x] `git ls-files .track/index.json .track/BOARD.md` returns nothing (not tracked)
- [x] `track build` regenerates both files locally

## Verification

- Run `git ls-files .track/index.json .track/BOARD.md` — empty output
- Run `track build` then `git status` — derived files not shown
- Run `track validate` — passes without derived files in git

## Notes

- 2026-03-17 human: Seeded from ephemeral-derived-project-plan.md.
- 2026-03-17 human: Moved to todo; project plan serves as the contract (task 012 deleted).
- 2026-03-17 agent: Verified `.track/.gitignore` was already present, removed `.track/index.json` and `.track/BOARD.md` from git tracking, and regenerated the local derived views with `track build`.
