---
name: track:decompose
description: Decompose a goal into Track tasks with non-overlapping file scopes and dependency ordering. The core coordination primitive.
---

# Track Decompose

## Overview

Break a goal into tasks that can be worked independently by multiple agents without file conflicts. Task atomization IS the coordination mechanism.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Understand the goal from the user.
3. Analyze the codebase for file/module boundaries:
   - If `.archeia/` exists, read it for architecture knowledge.
   - Otherwise, explore relevant source directories.
4. Decompose into tasks: each completable in one agent session, with clear objective and `files:` scope.
5. **Validate non-overlap** before creating tasks:
   - For every pair of tasks, check `files:` globs don't overlap.
   - Overlap = one pattern (with `**` stripped) starts with the other.
   - If overlap unavoidable, add `depends_on` between them.
6. Set dependency ordering: foundations first, implementation second, integration last.
7. Create task files using `track-new` workflow semantics, but batch the writes so the board is refreshed once for the full decomposition.
8. After the full batch is created, run `bash scripts/track-build.sh` once.

## Principles

- Atomic file scope: no two tasks modify the same file.
- Clear interfaces between tasks.
- Right-sized: 15-60 minutes per agent.
- Mode-appropriate: investigate/plan/implement.

## Response

Report: task count, dependency graph (ASCII), file scope assignments, resolved overlaps, board refresh status.
