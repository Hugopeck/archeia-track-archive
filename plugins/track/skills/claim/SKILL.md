---
name: track:claim
description: Claim a Track task by writing a claim file in `.track/tasks/claims/`. Advisory locking for workspace coordination.
---

# Track Claim

## Overview

Claim a task so other agents know you're working on it. Claims are advisory.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Verify task exists and is in `todo` status.
3. Check `.track/tasks/claims/` for existing claim on same task ID.
   - Exists and not expired → FAIL with message.
   - Exists and expired → treat as stale, proceed.
4. Create `.track/tasks/claims/` if needed.
5. Write `.track/tasks/claims/{task-id}.md` per PROTOCOL.md claim format (task_id, agent, claimed_at, files, expires_at with 6-hour TTL).
6. Move task from `todo` to `active` using the `track-move` workflow, but treat board refresh as part of the overall claim flow rather than a separate second rebuild.
7. Ensure the flow ends with one successful `bash scripts/track-build.sh` run.

## Response

Report: claimed task ID/title, claim file path, expiry time, board refresh status.
