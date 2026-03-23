---
name: track-release
description: Release a claimed Track task by removing its claim file from `.track/tasks/claims/`.
---

# Track Release

## Overview

Release a task claim so other agents can pick it up.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Look for `.track/tasks/claims/{task-id}.md`.
   - Exists → delete it.
   - Doesn't exist → warn "No active claim found for task {id}."
3. Task status is NOT automatically changed. Move the task separately with track-move.

## Response

Report: released task ID, whether claim was found and removed.
