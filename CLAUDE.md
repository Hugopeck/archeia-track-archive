# Claude Code Instructions

## Project Context

This is the Archeia monorepo. It ships two local-first products:

- **Archeia** — architecture knowledge generation and query skills
- **Track** — git-native task coordination driven by `CLAUDE.md`, `.track/`, and GitHub PR state

## Key Files

- `.claude/skills/archeia/SKILL.md` — Archeia write-path skill
- `.claude/skills/archeia-ask/SKILL.md` — Archeia query skill
- `.claude/skills/archeia/templates/` — Archeia canonical template set
- `plugins/archeia/` — Claude Code plugin distribution for `/archeia:init` and `/archeia:ask`
- `skills/archeia-init/`, `skills/archeia-ask/` — generated standalone distributions
- `docs/ONTOLOGY.md` — shared ontology and source-of-truth hierarchy
- `.track/projects/*.md` — Track project briefs
- `.track/projects/README.md` — Track project brief contract
- `.track/tasks/*.md` — flat Track task files
- `scripts/track-validate.sh` — Bash validator for Track state
- `scripts/track-todo.sh` — Bash generator for `TODO.md`
- `scripts/sync-skills.sh` — syncs Archeia canonical skills to distribution targets
- `.github/workflows/ci.yml` — sync check + Track validation
- `.github/workflows/track-complete.yml` — post-merge Task completion workflow
- `.archeia/` — Archeia's own product documentation
- `.archeia/PROTOCOL.md` — Archeia protocol for document families and maintenance modes
- `TODO.md` — generated Track view (gitignored)

## Workflow

- This repo has no app build step and no service runtime
- GitHub Actions runs semantic-release on pushes to `main`
- CI checks Archeia distribution sync and Track validation
- Most changes are documentation, skill markdown, or Track state changes
- Use conventional commits so release automation can infer versions
- Keep PRs focused — one concern per PR

## Commit Conventions

| Prefix | Bump | When to use |
|--------|------|-------------|
| `feat(archeia):` | Minor | New Archeia capability or template change |
| `feat(track):` | Minor | New Track convention or workflow capability |
| `fix(skills):` | Patch | Fix in Archeia skill logic, sync logic, or generated content |
| `fix(track):` | Patch | Fix in Track scripts, task lifecycle, or generator behavior |
| `docs:` | None | Routine documentation edits that should not release |
| `feat!:` / `fix!:` | Major | Breaking change to a public skill interface or repo workflow |

## Important Context

- Archeia was extracted from a larger TypeScript monorepo — the historical packages are gone
- Track is now a zero-dependency repo convention, not a plugin skill pack
- Lifecycle hooks were evaluated and rejected — native doc loading plus PR-time/CI-time enforcement are sufficient
- Edit canonical Archeia skills in `.claude/skills/` first, then run `bash scripts/sync-skills.sh`
- Track backlog state lives in default-branch `.track/tasks/*.md`
- Track in-flight state lives in open GitHub PRs whose branches match `task/{id}-{slug}`
- `TODO.md` is a derived convenience view; regenerate it with `bash scripts/track-todo.sh`
- Read `.archeia/VISION.md` and `.archeia/PRODUCT.md` for full product context

## Track — Task Coordination

Projects and tasks live in `.track/`. `TODO.md` is the generated shared view of current work.

### Layout
- `.track/projects/{project_id}-{slug}.md` — project briefs
- `.track/tasks/{task_id}-{slug}.md` — flat task files
- `TODO.md` — generated view; gitignored and never canonical

### Task Format

```yaml
---
id: "{project_id}.{task_id}"
title: "One-line objective"
status: todo
mode: implement
priority: high
project_id: "{project_id}"
created: YYYY-MM-DD
updated: YYYY-MM-DD
depends_on: []
files: []
pr: ""
---

## Context
What needs to happen and why.

## Acceptance Criteria
- [ ] Primary outcome

## Notes
Append-only log.
```

### Fields
- `status`: `todo | active | review | done | cancelled`
- `mode`: `investigate | plan | implement`
- `priority`: `urgent | high | medium | low`
- `project_id`: filename-derived project identifier from `.track/projects/`
- `depends_on`: blocking task IDs
- `files`: glob patterns for files the task expects to modify
- `pr`: optional on raw task files; populated on `done` for historical traceability
- `cancelled_reason`: required when `status: cancelled`

### Raw vs Effective Status
- Raw status is the `status:` field stored in the task file
- Effective status is what `TODO.md` shows
- If raw status is `done` or `cancelled`, effective status matches it
- Otherwise, an open draft PR for `task/{id}-{slug}` makes the task effectively `active`
- Otherwise, an open ready-for-review PR for `task/{id}-{slug}` makes the task effectively `review`
- Otherwise, effective status is `todo`

### Before Starting Work
1. Read `TODO.md` or scan `.track/tasks/*.md`
2. Check `files:` overlap against tasks already shown as `active` / `review`
3. Pick work that has no unresolved `depends_on` blockers
4. Use a dedicated worktree or branch per task

### Working a Task (Provisional PR lifecycle)
1. Create branch `task/{id}-{slug}` from `main`
2. First commit updates the task file only:
   - set raw `status: active`
   - update `updated:`
3. Push and open a **draft PR** immediately
4. Do the implementation work with as many commits as needed
5. When ready for review:
   - set raw `status: review`
   - update `updated:`
   - mark the PR ready for review
6. When the PR merges, the post-merge workflow writes `status: done`, `pr:`, and `updated:` on `main`

### Creating a Task
- Every task belongs to a project and uses `project_id`
- Open work must use dotted IDs like `4.1`
- Historical archived tasks may keep legacy numeric IDs like `001`
- Put scope and success definition in the project brief, not the task

### Decomposing a Goal
- Analyze module boundaries first
- Create one task per independent unit with non-overlapping `files:` scopes
- Use `depends_on` to sequence foundation work before integration work
- Prefer small reviewable PRs over multi-goal tasks

### Regenerating `TODO.md`
After creating, updating, cancelling, or completing tasks, regenerate the shared view:

```shell
bash scripts/track-todo.sh
```

Useful modes:

```shell
bash scripts/track-todo.sh --local
bash scripts/track-todo.sh --offline
```

### Validation
Run Track validation after changing task files, project briefs, or task lifecycle scripts:

```shell
bash scripts/track-validate.sh
```
