---
name: track:show
description: Display a single Track task by ID. Read-only.
---

# Track Show

## Overview

Display a single Track task by finding and reading its file.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Search `.track/` status directories for file matching `{id}-*.md`.
3. Present full contents: frontmatter and body sections.
4. Note any PROTOCOL.md violations if file looks malformed.

## Response

Structured summary: ID, title, status, mode, priority, type, deps, availability, body.
