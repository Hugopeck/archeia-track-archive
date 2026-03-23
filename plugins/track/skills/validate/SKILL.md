---
name: track:validate
description: Check `.track/` state for consistency — schema, structure, dependencies, claims.
---

# Track Validate

## Overview

Validate the entire `.track/` directory. Local counterpart to track-lint.py (CI). Same rules, agent-based.

## Workflow

1. Read `.track/PROTOCOL.md` — it defines every validation rule. This is your checklist.
2. Load `.track/config.yaml`.
3. For each task file, check:

   **Schema:** required fields, vocabulary membership, cycle format, cancelled_reason, unknown fields, depends_on present.

   **Structure:** four H2 sections, problem ≥20 chars, acceptance criteria exist, ready gate for todo/active/review/done.

   **Consistency:** correct status directory, filename pattern, no duplicate IDs, deps exist, no self-refs, no cycles, active/review/done deps must be done.

4. Check `.track/claims/`: refs exist, expired warnings, scope overlap.
5. Report all issues with severity.

## Response

Total tasks, errors, warnings, issue list, PASS/FAIL assessment.
