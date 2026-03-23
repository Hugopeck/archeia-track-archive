# Track Protocol

This is the single source of truth for the Track file-based coordination protocol.
All Track skills reference this document. Agents and humans read this to understand
how to create, manage, and coordinate tasks.

## Overview

Track is a file-based multi-agent coordination system. Tasks are markdown files with
YAML frontmatter stored in `.track/`. Agents coordinate by claiming tasks, declaring
file scopes, and following workflow rules. There is no compiled binary — the agent IS
the runtime.

## Directory Structure

```
PROJECTS.md             # Derived, gitignored — portfolio view at repo root
TASKS.md                # Derived, gitignored — global task index at repo root
BOARD.md                # Derived, gitignored — kanban view at repo root
.track/
├── config.yaml         # Schema, project registry, and numbering counters
├── PROTOCOL.md         # This file — protocol specification
├── projects/           # Project briefs for active projects
├── tasks/              # Task state folders + claims
│   ├── triage/         # Tasks not yet ready to work
│   ├── todo/           # Tasks ready to be claimed and worked
│   ├── active/         # Tasks currently being worked
│   ├── review/         # Tasks awaiting review
│   ├── done/           # Completed tasks
│   ├── cancelled/      # Cancelled tasks
│   └── claims/         # Advisory claim files (one per claimed task)
├── index.json          # Derived, gitignored — machine-readable task index
└── .gitignore          # Ignores index.json (repo root .gitignore ignores the root markdown views)
```

Quick orientation:

- `.track/projects/README.md` explains project brief naming and required sections
- `.track/tasks/README.md` explains task-state folders, dotted task IDs, and claims

## Task File Format

Every task is a markdown file at `.track/tasks/{status}/{id}-{slug}.md`.

### Filename Convention

- New-style `{id}` is `{project}.{task}` (e.g., `4.2`, `1.1`)
- Legacy archived tasks may still use zero-padded numeric IDs (e.g., `001`, `042`)
- `{slug}` is a lowercase hyphenated summary (e.g., `add-claim-protocol`)
- Full example: `.track/tasks/todo/4.2-add-claim-protocol.md`

### Frontmatter Schema

```yaml
---
id: "4.2"
title: "[Implement] Add claim protocol for multi-agent coordination"
status: todo
mode: implement
priority: high
type: feature
scopes: []              # Optional, must match config.yaml scopes
project: "4"           # Required for new-style task IDs; must match config.yaml projects
cycle: "2026-W13"       # Optional, ISO week format YYYY-Www
created: 2026-03-22
updated: 2026-03-22
assigned_to:             # Optional
pr:                      # Optional, PR URL
depends_on: []           # Required, list of task IDs that block this task
cancelled_reason:        # Required when status is cancelled
files:                   # Optional, list of glob patterns for file ownership
  - "src/auth/**"
  - "tests/auth/**"
---
```

### Required Frontmatter Fields

Every task must have: `id`, `title`, `status`, `mode`, `priority`, `type`,
`created`, `updated`, `depends_on`.

## Project Registry

Projects are first-class Track objects with two surfaces:

- `.track/config.yaml` is the machine-readable registry
- `.track/projects/{project-key}.md` is the narrative scope contract

Tasks may reference a project by key through frontmatter, but they do not own a
project's goal, scope, or success definition.

### Registry Rules

Each project entry in `.track/config.yaml` must include:

- active project key as a quoted integer string (`"1"`, `"2"`, `"3"`)
- `title` — required human-readable title
- `description` — required one-sentence summary
- `status` — required, one of `active` or `archived`
- `brief` — required for active projects, optional for archived projects
- `task_counter` — required for active projects; next available task number within that project

`.track/config.yaml` also includes `project_counter`, the next available active
project number.

Open tasks (`triage`, `todo`, `active`, `review`) may reference only `active`
projects. Historical tasks (`done`, `cancelled`) may reference archived projects.
Open tasks must use the `{project}.{task}` ID format. Legacy numeric IDs remain
valid only for historical tasks.

### Project Brief Contract

Each active project must have a brief at `.track/projects/{project-key}-{slug}.md`.

Project briefs are markdown-only in this phase. Do not add frontmatter.

Required shape:

```markdown
# {Project Title}

## Goal
## Why Now
## In Scope
## Out Of Scope
## Shared Context
## Dependency Notes
## Success Definition
## Candidate Task Seeds
```

Rules:

- H1 must match `projects.{key}.title`
- the brief path must match `projects.{key}.brief`
- active project brief paths should begin with `projects/{project-key}-`
- the brief owns narrative scope; `config.yaml` owns machine-readable metadata
- archived projects may omit a brief when they only exist for historical task references

### Body Sections

Every task must have these four H2 sections in this order:

```markdown
## Context

### Problem
<!-- REQUIRED: At least 20 characters of real content (excluding comments and placeholders). -->

### Cause
<!-- Optional but recommended. Root cause, constraints, non-goals. -->

### Affected Files
<!-- Required for todo/active/review/done. List files/modules to inspect. -->

### References
<!-- Optional. Links to specs, ADRs, related tasks. -->

## Acceptance Criteria

- [ ] Primary outcome
- [ ] Exit condition proving completion

## Verification

- Exact command or check for primary outcome
- Regression check

## Notes

<!-- Append-only. Format: - YYYY-MM-DD author: message -->
```

### Task Template (triage)

```yaml
---
id: "{next_id}"
title: "[{Mode}] One-line objective"
status: triage
mode: {investigate|plan|implement}
priority: medium
type: {bug|feature|improvement|debt|infra|spike}
scopes: []
project: "{project_number}"
cycle:
created: {today}
updated: {today}
assigned_to:
pr:
depends_on: []
files: []
---

## Context

### Problem
State the objective and expected output.

### Cause

### Affected Files

### References

## Acceptance Criteria

- [ ] Primary outcome
- [ ] Exit condition

## Verification

## Notes
```

### Task Template (todo — implement)

Same as triage but with status `todo` and all ready gate fields filled. New
tasks should use dotted IDs derived from the project's `task_counter`.
- Problem section has 20+ characters of real content
- Affected Files lists concrete paths
- Verification has at least one step
- Acceptance criteria are specific and reviewable

## Fixed Vocabularies

These are defined in `config.yaml` and must not be extended without updating the config.

### Statuses

| Status | Directory | Description |
|--------|-----------|-------------|
| triage | `triage/` | Not yet ready to work |
| todo | `todo/` | Ready to be claimed |
| active | `active/` | Currently being worked |
| review | `review/` | Awaiting review |
| done | `done/` | Completed |
| cancelled | `cancelled/` | Cancelled with reason |

### Valid Transitions

```
triage → todo, cancelled
todo → triage, active, cancelled
active → review, cancelled
review → done, active, cancelled
done → (terminal)
cancelled → (terminal)
```

### Priorities

`urgent`, `high`, `medium`, `low` (ordered by severity)

### Types

`bug`, `feature`, `improvement`, `debt`, `infra`, `spike`

### Modes

`investigate`, `plan`, `implement`

## Ready Gate

Tasks in `todo`, `active`, `review`, or `done` must satisfy:

1. `## Context`, `## Acceptance Criteria`, `## Verification`, `## Notes` sections exist
2. Problem subsection has ≥20 characters of real content (comments/placeholders excluded)
3. At least one acceptance criterion exists
4. `### Affected Files` has at least one path
5. `## Verification` has at least one step

Additional rules:
- `done` tasks must not have unchecked acceptance criteria
- `active`, `review`, and `done` tasks must have all `depends_on` targets in `done` status
- `cancelled` tasks must have a non-empty `cancelled_reason`

## Dependencies

- `depends_on` lists task IDs that block this task
- Self-references are forbidden
- Circular dependencies are forbidden (validated by DFS)
- A task is **available** when: status is `todo`, all `depends_on` targets are in `done`, and no active claim overlaps its `files:` scope

## Claim Protocol

Claims are advisory, local to the worktree. They prevent two agents in the same
workspace from working on the same task or overlapping file scopes.

### Claim File Format

```yaml
# .track/tasks/claims/{task-id}.md
---
task_id: "4.2"
agent: "conductor-workspace-melbourne"
claimed_at: "2026-03-22T17:20:00Z"
files:
  - "src/auth/**"
  - "tests/auth/**"
expires_at: "2026-03-22T23:20:00Z"  # 6-hour TTL
---
```

### Claiming Rules

1. Before claiming, check `.track/tasks/claims/` for an existing claim on the same task
2. If a claim exists and is not expired → fail, report who holds the claim
3. If a claim exists but is expired → treat as stale, proceed
4. Write the claim file with a 6-hour TTL
5. Copy the task's `files:` scope into the claim

### Releasing Rules

1. Remove the claim file when the task is completed or abandoned
2. If no claim file exists → warn, do nothing

### File Scope Overlap

A task's `files:` field declares which files/directories the task will modify.
When checking availability (`track-available`), exclude tasks whose `files:` scope
overlaps with any actively claimed task's scope.

Overlap means: any glob pattern in one task's `files:` could match the same
file as any glob pattern in another task's `files:`.

### Stale Claim Cleanup

- `track-validate` flags expired claims as warnings
- `track-available` ignores expired claims
- Agents should release claims when done

## Validation Rules

These rules are enforced by `tools/track-lint.py` in CI and by the `track-validate` skill locally.

### Schema Checks
- All required frontmatter fields present
- `status`, `priority`, `type`, `mode` values in config.yaml vocabulary
- `scopes` values in config.yaml scopes list
- `project` value in config.yaml projects
- open tasks must use `{project}.{task}` IDs and match the project key
- open tasks may not reference archived projects
- `cycle` matches ISO week format `YYYY-Www`
- `cancelled_reason` present and non-empty when status is `cancelled`
- No unknown frontmatter fields (known: id, title, status, mode, priority, type,
  scopes, project, cycle, created, updated, assigned_to, pr, depends_on,
  cancelled_reason, files)
- `depends_on` field must be present

### Structure Checks
- All four H2 sections present: Context, Acceptance Criteria, Verification, Notes
- Problem subsection ≥20 characters of real content
- At least one acceptance criterion
- Ready gate enforced for todo/active/review/done
- Affected Files required for todo/active/review/done
- Verification required for todo/active/review/done

### Consistency Checks
- Task file is in the correct status directory
- Filename matches `{id}-{slug}.md` pattern (lowercase, hyphens)
- No duplicate task IDs across all directories
- `depends_on` targets exist as real task IDs
- No self-references in `depends_on`
- No circular dependencies (DFS cycle detection)
- `active`/`review`/`done` tasks: all `depends_on` targets must be in `done`
- active projects in config have valid briefs with the required structure

### Claim Checks
- Claim files reference existing tasks
- Expired claims flagged as warnings
- No two active claims overlap on `files:` scope

### Warnings (non-blocking)
- Legacy `agent_ready` field present → warn to remove
- More than 10 acceptance criteria → suggest decomposition
- Active task with no notes for 5+ days → flag as stale

## Config Schema

```yaml
schema_version: '0.1'
statuses:
  - triage
  - todo
  - active
  - review
  - done
  - cancelled
priorities:
  - urgent
  - high
  - medium
  - low
types:
  - bug
  - feature
  - improvement
  - debt
  - infra
  - spike
scopes: []
projects:
  '1':
    title: "Human-readable title"
    description: "Required one-sentence summary"
    status: active
    brief: projects/1-project-name.md
    task_counter: 1
project_counter: 2
```

`task_counter` tracks the next available task number within a project.
`project_counter` tracks the next available active project number.

Archived project example:

```yaml
projects:
  old-project:
    title: "Historical project"
    description: "Retained for done and cancelled task references."
    status: archived
```

## Derived Views

### index.json

Machine-readable snapshot of all tasks. Includes:
- Task list with frontmatter fields
- Derived `available` flag per task
- Derived `reverse_blockers` per task
- Summary counts by status, priority, project

Built by `tools/track-build.py` by reading task files, computing availability and
reverse blockers, and writing `.track/index.json`. This file is gitignored —
each agent generates its own local copy.

### PROJECTS.md

Human-readable portfolio projection. Shows:
- immediate starts across active projects
- per-project summary counts and derived state
- brief-led project sections with next work, blocked work, open tasks, and recent done

Built by `tools/track-build.py` from canonical Track state and written to repo-root
`PROJECTS.md`. It is pure GFM, gitignored, and non-canonical.

### TASKS.md

Human-readable task index projection. Shows:
- ready, active, review, blocked, triage, recently done, and cancelled sections
- deterministic why-here reasons for each task
- status and priority summaries

Built by `tools/track-build.py` from canonical Track state and written to repo-root
`TASKS.md`. It is pure GFM, gitignored, and non-canonical.

### BOARD.md

Human-readable kanban projection. Shows:
- Active, Review, Ready, Blocked, Triage, and Recently Done lanes
- compact lane summary plus markdown-native task cards
- summary line: "Open: N | Ready: N | Active: N | Review: N | Done: N | Cancelled: N"

Built by `tools/track-build.py` from the same snapshot as `.track/index.json`
and written to repo-root `BOARD.md`. All three markdown projections are pure GFM,
optimized for IDE rendering, gitignored, and non-canonical. Conductor setup may
prebuild them for each workspace, and Track write operations should refresh them
after mutating canonical Track state.

## Skill Reference

| Skill | Purpose | Mutates .track/? |
|-------|---------|-----------------|
| track-new | Create a task file, increment project task_counter | Yes |
| track-move | Move task between status directories | Yes |
| track-show | Display a single task | No |
| track-list | List/filter tasks | No |
| track-board | Generate/read board view | Writes derived files only |
| track-stats | Summarize workflow health | No |
| track-claim | Claim a task for this agent | Yes (claims/) |
| track-release | Release a claimed task | Yes (claims/) |
| track-available | List available tasks (unclaimed, unblocked) | No |
| track-validate | Check .track/ for consistency | No |
| track-decompose | Break a goal into tasks with file scopes | Yes |
| track-plan | Project-level planning into tasks | Yes |
| track-init | Bootstrap .track/ directory | Yes |
