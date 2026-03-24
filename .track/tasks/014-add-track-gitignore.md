---
id: "014"
title: "[Implement] Add .track/.gitignore for derived files in track init"
status: done
mode: implement
priority: high
project_id: "0"
created: 2026-03-17
updated: 2026-03-17
depends_on: []
files: []
pr: ""
---

## Context

### Problem
`track init` must create a `.track/.gitignore` that ignores `index.json` and `BOARD.md` so these generated files are never staged or committed.

### Cause
Replacing the `.gitattributes` merge=ours strategy with a `.gitignore` is the core mechanism that makes derived files ephemeral. Without this, `git add .track/` would stage the generated files.

### Affected Files
- `src/commands/init.rs` — add `.track/.gitignore` creation

### References
- Contract: `ephemeral-derived-project-plan.md`

## Acceptance Criteria

- [x] `track init` creates `.track/.gitignore` containing `index.json` and `BOARD.md`
- [x] Running `track build` after `track init` generates the files but `git status` does not show them as untracked
- [x] Repeated `track init` does not duplicate `.gitignore` entries

## Verification

- Run `track init` in a fresh temp directory, verify `.track/.gitignore` exists with correct entries
- Run `track build`, then `git status` — derived files should not appear
- Run `cargo test` — all green

## Notes

- 2026-03-17 human: Seeded from ephemeral-derived-project-plan.md.
- 2026-03-17 agent: Verified `.track/.gitignore` creation, idempotence, and ignored derived outputs in init tests.
