---
name: track-init
description: Bootstrap a new `.track/` directory with config, status dirs, claims dir, gitignore, and PROTOCOL.md.
---

# Track Init

## Overview

Initialize Track in a repository.

## Workflow

1. Check if `.track/` exists — warn before overwriting.
2. Create: `.track/{triage,todo,active,review,done,cancelled,claims}/` with `.gitkeep` files.
3. Write `.track/config.yaml` with defaults (see PROTOCOL.md). Include scopes if user specified them.
4. Write `.track/.gitignore`: `index.json` and `BOARD.md`.
5. Write `.track/PROTOCOL.md` from the canonical template.
6. Optionally generate `.github/workflows/track-ci.yml`.
7. Write empty BOARD.md and index.json.

## Response

Report: directory structure, config scopes, whether CI was generated.
