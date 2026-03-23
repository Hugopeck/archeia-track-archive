---
name: track:board
description: Generate or read the Track kanban view from task files, alongside PROJECTS.md and TASKS.md.
---

# Track Board

## Overview

Display the Track kanban board — a vertical workflow view backed by the same generated PM surfaces as `PROJECTS.md` and `TASKS.md`.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. If `BOARD.md` exists and the user just wants to see it, display it.
3. If `BOARD.md` is missing or the user asks to regenerate, run `bash scripts/track-build.sh`.
4. Display `BOARD.md`.

## Rules

Only writes derived files (`PROJECTS.md`, `TASKS.md`, `BOARD.md`, `.track/index.json`). `BOARD.md` is the kanban view.

## Response

Display the board contents.
