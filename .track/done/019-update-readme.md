---
id: "019"
title: "[Implement] Update README.md status and capabilities"
status: done
mode: implement
priority: medium
type: improvement
scopes: []
project: ephemeral-derived
cycle:
created: 2026-03-17
updated: 2026-03-17
assigned_to:
pr:
depends_on: []
---

## Context

### Problem
README.md's status section says "mid-migration from agent_ready to explicit task mode" without specifics on what's done. The capabilities list doesn't mention mode-aware parsing or ephemeral derived files. References to `.gitattributes` merge strategy and derived-file freshness need removal.

### Cause
README.md is the first thing people read. It must reflect the current state accurately.

### Affected Files
- `README.md` — Status section, Current Capabilities, Current source documents

### References
- Depends on: tasks 017, 018 (spec and build plan must be updated first so README can reference them accurately)
- Contract: `ephemeral-derived-project-plan.md`

## Acceptance Criteria

- [x] Status section reflects Phase 11 progress with specifics on what's done and remaining
- [x] Current Capabilities mentions mode-aware parsing and ephemeral derived files
- [x] No references to `.gitattributes` merge strategy or derived-file freshness checking
- [x] Source documents list includes `docs/task-model-v2-contract.md` and `docs/task-model-v2-migration-risks.md`

## Verification

- Read the updated README and confirm the status description matches the actual codebase state
- Search for "gitattributes", "freshness", "stale" — should not appear in committed-derived-files context

## Notes

- 2026-03-17 human: Seeded from ephemeral-derived-project-plan.md.
- 2026-03-17 human: Moved to todo; project plan serves as the contract (task 012 deleted).
- 2026-03-17 agent: Updated `README.md` to describe the shipped ephemeral-derived model, the current hybrid `mode` migration state, and the canonical migration-reference docs.
