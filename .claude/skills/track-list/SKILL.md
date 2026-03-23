---
name: track-list
description: Summarize Track tasks from `.track/` files, apply filters, and present the current queue. Read-only.
---

# Track List

## Overview

List and filter Track tasks by reading `.track/` files directly.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Read `.track/index.json` if current, otherwise read task files directly.
3. Apply filters: status, project, cycle, priority, type, mode, available.
4. Present in stable order: priority first, then ID ascending.
5. If no tasks match, say so.

## Output

Concise, scan-friendly. Include: ID, status, priority, title, assignment. Read-only — don't edit tasks.

## Response

Report: source used, filters applied.
