---
id: "036"
title: "[Implement] Write PROTOCOL.md as single source of truth for Track protocol"
status: done
mode: implement
priority: high
project_id: "0"
created: 2026-03-22
updated: 2026-03-22
depends_on: []
files:
  - ".track/PROTOCOL.md"
pr: ""
---

## Context

### Problem
All Track skills need a single source of truth for the task schema, validation rules, naming conventions, and coordination protocol. Without it, each skill repeats rules independently, creating drift and DRY violations.

### Affected Files
- .track/PROTOCOL.md

### References
- docs/specs/track-spec.md
- archive/rust-cli/src/validator/

## Acceptance Criteria

- [x] PROTOCOL.md covers task file format, frontmatter schema, body sections
- [x] PROTOCOL.md covers fixed vocabularies and valid transitions
- [x] PROTOCOL.md covers ready gate rules
- [x] PROTOCOL.md covers claim protocol with TTL and scope overlap
- [x] PROTOCOL.md covers all validation rules (schema, structure, consistency)
- [x] PROTOCOL.md includes task templates

## Verification

- python3 track-lint.py passes
- All skills reference PROTOCOL.md

## Notes

- 2026-03-22 agent: Created as part of pure skill pack pivot.
