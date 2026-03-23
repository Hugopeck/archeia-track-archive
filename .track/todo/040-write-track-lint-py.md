---
id: "040"
title: "[Implement] Write track-lint.py with full validation parity"
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
  - "track-lint.py"
  - "tests/lint/**"
---

## Context

### Problem
CI needs a deterministic enforcement layer that validates all PROTOCOL.md rules without requiring a compiled binary. track-lint.py replaces the Rust validator with full parity.

### Affected Files
- track-lint.py
- tests/lint/test_track_lint.py

## Acceptance Criteria

- [ ] Python script using only stdlib yaml module (PyYAML)
- [ ] Full parity with Rust validator: schema, structure, consistency checks
- [ ] Circular dependency detection via DFS
- [ ] Claim validation (expired, orphaned, scope overlap)
- [ ] Exit 0 on pass, exit 1 on errors
- [ ] Test suite with full parity against Rust test cases
- [ ] Reuses existing tests/fixtures/ as test corpus

## Verification

- python3 track-lint.py passes on current .track/
- python3 tests/lint/test_track_lint.py — all tests pass

## Notes

- 2026-03-22 agent: Part of pure skill pack pivot.
