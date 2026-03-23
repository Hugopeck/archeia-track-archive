---
name: track:board
description: Generate or read the Track board view from task files.
---

# Track Board

## Overview

Display the Track board — tasks grouped by status.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. If `.track/BOARD.md` exists and user just wants to see it, display it.
3. To regenerate: read all task files, group by status (Active, Review, Todo, Triage), create table (ID | Title | Priority | Type | Mode | Depends On | Available), add summary line, write to `.track/BOARD.md`.
4. Also regenerate `.track/index.json` if needed.

## Rules

Only writes derived files (BOARD.md, index.json). Sort by priority then ID within each group.

## Response

Display the board contents.
