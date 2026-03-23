---
name: track-new
description: Create a new Track task file inside `.track/triage/` or `.track/todo/`, increment `.track/config.yaml` `id_counter`, and validate the result.
---

# Track New

## Overview

Create a new Track task by editing repo files directly.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Load `.track/config.yaml` and note `id_counter`. New task ID = zero-padded counter (e.g., `042`).
3. Gather inputs: title, status (triage/todo, default triage), mode (investigate/plan/implement), priority (default medium), type (default bug), optional project/cycle/depends_on/files.
4. Write task file at `.track/{status}/{id}-{slug}.md` following PROTOCOL.md template.
5. Always include `depends_on: []` unless the user names blockers.
6. Increment `id_counter` in config.yaml.
7. Run `track-validate` skill or verify against PROTOCOL.md rules.

## Writing Rules

- Use vocabularies from config.yaml only.
- Include four body sections: Context, Acceptance Criteria, Verification, Notes.
- If status is `todo`, task must pass ready gate (see PROTOCOL.md).
- For `implement` tasks, include Affected Files under Context.
- Set created/updated to today's date.

## Defaults

status: triage, priority: medium, type: bug, depends_on: [], files: []

## Response

Report: created task path, chosen status/mode/priority, whether validation passed.
