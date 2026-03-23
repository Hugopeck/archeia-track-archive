---
id: "020"
title: "[Implement] Update docs/ quick-reference files"
status: done
mode: implement
priority: low
type: improvement
scopes: []
project: ephemeral-derived
cycle:
created: 2026-03-17
updated: 2026-03-17
assigned_to:
pr:
depends_on: ["017"]
---

## Context

### Problem
Several docs/ quick-reference files reference the old committed-derived-files model: `commands.md` describes `.gitattributes` updates in `track init`, `data-model.md` describes derived files without noting they're ephemeral, and other files may reference freshness validation.

### Cause
The docs/ directory is meant to be code-aligned quick-reference material. It must stay consistent with the spec and codebase.

### Affected Files
- `docs/commands.md` — init/build/validate descriptions
- `docs/data-model.md` — derived files description
- Any other docs/ files referencing gitattributes, freshness, or committed derived files

### References
- Depends on: task 017 (spec must be updated first)
- Contract: `ephemeral-derived-project-plan.md`

## Acceptance Criteria

- [x] `docs/commands.md` accurately describes `track init` (creates `.track/.gitignore`, no `.gitattributes`), `track build` (ephemeral local refresh), and `track validate` (no freshness check)
- [x] `docs/data-model.md` clarifies that `index.json` and `BOARD.md` are gitignored ephemeral files
- [x] No docs/ files reference `.gitattributes` merge strategy or derived-file freshness checking

## Verification

- Search docs/ for "gitattributes", "freshness", "stale" — no hits in committed-derived-files context
- Read updated commands.md and data-model.md sections and confirm they match the spec

## Notes

- 2026-03-17 human: Seeded from ephemeral-derived-project-plan.md.
- 2026-03-17 human: Moved to todo; project plan serves as the contract (task 012 deleted).
- 2026-03-17 agent: Updated the quick-reference docs to describe `.track/.gitignore`, local-only derived views, and validation without derived-file comparisons.
