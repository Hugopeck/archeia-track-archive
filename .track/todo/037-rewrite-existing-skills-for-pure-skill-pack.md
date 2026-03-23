---
id: "037"
title: "[Implement] Rewrite 6 existing skills to reference PROTOCOL.md and remove cargo run"
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
  - ".claude/skills/track-new/**"
  - ".claude/skills/track-move/**"
  - ".claude/skills/track-list/**"
  - ".claude/skills/track-show/**"
  - ".claude/skills/track-board/**"
  - ".claude/skills/track-stats/**"
---

## Context

### Problem
The 6 existing skills reference `cargo run -- validate` and `cargo run -- build` which no longer exist after the Rust archival. They also repeat protocol rules inline instead of referencing PROTOCOL.md.

### Affected Files
- .claude/skills/track-new/SKILL.md
- .claude/skills/track-move/SKILL.md
- .claude/skills/track-list/SKILL.md
- .claude/skills/track-show/SKILL.md
- .claude/skills/track-board/SKILL.md
- .claude/skills/track-stats/SKILL.md

## Acceptance Criteria

- [ ] All 6 skills reference PROTOCOL.md instead of repeating rules
- [ ] All cargo run invocations removed
- [ ] Each skill has agents/openai.yaml

## Verification

- grep -r "cargo run" .claude/skills/ returns no matches
- grep -r "PROTOCOL.md" .claude/skills/track-{new,move,list,show,board,stats}/SKILL.md returns 6 matches

## Notes

- 2026-03-22 agent: Part of pure skill pack pivot.
