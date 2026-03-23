---
id: "039"
title: "[Implement] Create planning skills: decompose and plan"
status: todo
mode: implement
priority: high
type: feature
project: launch-readiness
created: 2026-03-22
updated: 2026-03-22
depends_on:
  - "036"
files:
  - ".claude/skills/track-decompose/**"
  - ".claude/skills/track-plan/**"
---

## Context

### Problem
Track needs planning skills that decompose goals into tasks with non-overlapping file scopes. track-decompose is the core coordination primitive — atomized tasks prevent merge conflicts.

### Affected Files
- .claude/skills/track-decompose/SKILL.md
- .claude/skills/track-plan/SKILL.md

## Acceptance Criteria

- [ ] track-decompose produces tasks with non-overlapping files: scopes
- [ ] track-decompose validates scope non-overlap before creating tasks
- [ ] track-plan creates project-level plans that decompose into tasks
- [ ] Each skill has agents/openai.yaml

## Verification

- Both skill directories exist with SKILL.md and agents/openai.yaml
- python3 track-lint.py passes

## Notes

- 2026-03-22 agent: Part of pure skill pack pivot. Decompose is lightweight — optionally reads .archeia/ for module boundaries, doesn't duplicate codebase scanning.
