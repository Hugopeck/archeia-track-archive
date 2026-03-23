---
name: track:new
description: Create a new Track task file inside `.track/tasks/triage/` or `.track/tasks/todo/`, allocate a `{project}.{task}` ID from `.track/config.yaml`, and validate the result.
---

# Track New

## Overview

Create a new Track task by editing repo files directly.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Load `.track/config.yaml` and choose the target project. For new-style tasks, `project` is required.
3. Read the target project's `task_counter`. New task ID = `{project}.{task_counter}` (e.g., `4.2`).
4. Gather inputs: title, status (triage/todo, default triage), mode (investigate/plan/implement), priority (default medium), type (default bug), project, optional cycle/depends_on/files.
5. Write task file at `.track/tasks/{status}/{id}-{slug}.md` following PROTOCOL.md template.
6. Always include `depends_on: []` unless the user names blockers.
7. Increment that project's `task_counter` in config.yaml.
8. Run `track-validate` skill or verify against PROTOCOL.md rules.
9. Run `bash scripts/track-build.sh` to refresh local derived views.

## Writing Rules

- Use vocabularies from config.yaml only.
- Include four body sections: Context, Acceptance Criteria, Verification, Notes.
- If status is `todo`, task must pass ready gate (see PROTOCOL.md).
- For `implement` tasks, include Affected Files under Context.
- Set created/updated to today's date.

## Defaults

status: triage, priority: medium, type: bug, depends_on: [], files: []

## Response

Report: created task path, chosen status/mode/priority, whether validation and board refresh passed.
