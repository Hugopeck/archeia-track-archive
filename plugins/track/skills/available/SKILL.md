---
name: track:available
description: List Track tasks available for work — unclaimed, unblocked, no file scope overlap.
---

# Track Available

## Overview

Find tasks ready to claim and work on.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Read all task files in `.track/todo/`.
3. For each task, check availability:
   a. Dependencies resolved: all `depends_on` targets in `.track/done/`.
   b. Not claimed: no active (non-expired) claim in `.track/claims/`.
   c. No file scope overlap: task's `files:` patterns don't overlap with any actively claimed task's `files:`.
4. Present available tasks sorted by priority then ID.
5. If nothing available, explain why.

## Glob Overlap

Two patterns overlap if one path (with ** stripped) starts with the other.

## Response

Available tasks with ID, title, priority, files scope. For unavailable: brief reason.
