---
id: "024"
title: "[Implement] Document Conductor scripts versus AGENTS.md guidance"
status: done
mode: implement
priority: low
project_id: "0"
created: 2026-03-17
updated: 2026-03-17
depends_on:
  - "022"
  - "023"
files: []
pr: ""
---

## Context

### Problem
If we add shared Conductor scripts without documenting the boundary, contributors may duplicate behavior between `conductor.json`, shell wrappers, and `AGENTS.md`.

### Cause
Conductor scripts are for executable workspace automation, while `AGENTS.md` is for human/agent policy and repo-specific instructions. That split should be documented in the repo once the shared scripts exist.

### Affected Files
- `README.md`
- `AGENTS.md` — only if a small boundary reminder is still needed after the docs update

### References
- Depends on: tasks 022, 023

## Acceptance Criteria

- [x] Contributor docs explain what belongs in Conductor scripts versus `AGENTS.md`
- [x] Docs point contributors at the committed shared workflow instead of personal script setup
- [x] No repo policy is duplicated unnecessarily across multiple instruction surfaces

## Verification

- Read the updated contributor docs and confirm the ownership split is clear
- Search for contradictory guidance about Conductor scripts or `AGENTS.md`

## Notes

- 2026-03-17 codex: This task stays blocked until the recommendation and shared scripts are both in place.
- 2026-03-17 agent: Documented the shared `conductor.json` workflow in `README.md` and `docs/contributing.md`, keeping executable automation in Conductor scripts and repo policy in `AGENTS.md`.
