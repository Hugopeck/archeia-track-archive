---
name: track-move
description: Move an existing Track task between `.track/` status directories, update frontmatter, and validate.
---

# Track Move

## Overview

Transition a Track task between workflow states by editing the file directly.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Locate task file by ID under `.track/`.
3. Verify transition is valid (see PROTOCOL.md transitions table).
4. Update as needed: `updated` to today, `cancelled_reason` for cancelled, check criteria for done, verify deps for active/review/done, verify ready gate for todo.
5. Move file to `.track/{target_status}/`.
6. Update `status` in frontmatter.
7. Preserve filename slug and body byte-for-byte.
8. Run `track-validate` skill or verify consistency.

## Response

Report: old path → new path, changed fields, validation status.
