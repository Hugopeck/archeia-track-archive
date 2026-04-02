# Claude Code Instructions

## Project Context

This is the Archeia repo. It ships architecture knowledge generation and query skills for AI coding agents.

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
- `.track/scripts/track-validate.sh` — Bash validator for Track state
- `.track/scripts/track-todo.sh` — Bash generator for `TODO.md`
- `scripts/sync-skills.sh` — syncs Archeia canonical skills to distribution targets
- `.github/workflows/ci.yml` — Archeia sync check
- `.archeia/` — Archeia's own product documentation
- `.archeia/PROTOCOL.md` — Archeia protocol for document families and maintenance modes

## Workflow

- This repo has no app build step and no service runtime
- GitHub Actions runs semantic-release on pushes to `main` to publish tags and GitHub releases
- The release workflow must not push release commits back to `main`; changelog updates land through a separate PR
- CI checks Archeia distribution sync (`ci.yml`)
- Most changes are documentation or skill markdown
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
- Lifecycle hooks were evaluated and rejected — native doc loading plus PR-time/CI-time enforcement are sufficient
- Edit canonical Archeia skills in `.claude/skills/` first, then run `bash scripts/sync-skills.sh`
- Track backlog state lives in default-branch `.track/tasks/*.md`
- Track in-flight state lives in open GitHub PRs whose branches match `task/{id}-{slug}`
- Repo-local PR expectations live in `.track/specs/pr-instructions.md`
- Automated changelog PRs are intentionally untracked and use non-`task/` branches
- `TODO.md` is a derived convenience view; regenerate it with `bash .track/scripts/track-todo.sh`
- Read `.archeia/VISION.md` and `.archeia/PRODUCT.md` for full product context

<!-- TRACK:START -->
## Track — Task Coordination

Track is a git-native coordination system. It works in the background — follow its conventions and it keeps everything organized. The protocol below is both reference and guide.

Projects and tasks live in `.track/`. `TODO.md` is the generated shared view of current work.

### Layout
- `.track/projects/{project_id}-{slug}.md` — project briefs
- `.track/tasks/{task_id}-{slug}.md` — flat task files
- `.track/plans/{slug}.md` — short-lived plan documents (auto-expire after 7 days)
- `.track/scripts/` — bash enforcement scripts (managed by Track)
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

### Agent Protocol (primary)

1. Read `TODO.md` for current state. Pick a `todo` task or resume an `active` one.
2. Check `files:` overlap against tasks already shown as `active` / `review` — do not touch files owned by another in-progress task.
3. Open a **draft PR** to start work. No PR = not started.
4. Implement. When ready, mark the PR ready for review.
5. If `gh` auth fails or PR creation fails, **stop and surface the error.**

`TODO.md` is generated — edit task files in `.track/tasks/`, not TODO.md directly.

`/track:work` contains the full protocol with edge cases. Use it when this section is insufficient.

### Starting Work (details)
1. Read the task's `## Context` and `## Notes` — previous sessions may have left important context
2. Pick work that has no unresolved `depends_on` blockers
3. If the task's mode is `investigate` or `plan`, focus on understanding and documenting findings before writing implementation code
4. If acceptance criteria seem incomplete, update them before starting
5. Use a dedicated worktree or branch per task

### Working a Task (Provisional PR lifecycle)
1. Create branch `task/{id}-{slug}` from `main`
2. First commit updates the task file only:
   - set raw `status: active`
   - update `updated:`
3. Push and open a **draft PR** immediately
   - PR title must include the task ID in brackets or parentheses: `[4.1] Title` or `feat(scope): (4.1) Title`
   - CI will lint the branch name and PR title against the task file
4. Do the implementation work with as many commits as needed
5. When ready for review:
   - set raw `status: review`
   - update `updated:`
   - mark the PR ready for review
6. When the PR merges, the post-merge workflow writes `status: done`, `pr:`, and `updated:` on `main`

### Creating a Task
- Every task belongs to a project and uses `project_id`
- Open work must use dotted IDs like `1.1`
- Put scope and success definition in the project brief, not the task

### Decomposing a Goal
- Analyze module boundaries first
- Create one task per independent unit with non-overlapping `files:` scopes
- Use `depends_on` to sequence foundation work before integration work
- Prefer small reviewable PRs over multi-goal tasks

### Saving Plans
When any planning, investigation, or design work produces a plan, **automatically save it** to `.track/plans/`. Do not wait for the user to ask — persistence is the default.
- Filename: `{task_id}-{slug}.md` when linked to a task, or `{slug}.md` otherwise
- Add YAML frontmatter with `title`, `created` (today's date), and optionally `task_id`/`project_id`
- The body is freeform — paste the plan content as-is, no reformatting needed
- Plans auto-expire 7 days after `created`; update the date to keep one longer

### Regenerating `TODO.md`
After creating, updating, cancelling, or completing tasks, regenerate the shared view:

```shell
bash .track/scripts/track-todo.sh
```

Useful modes:

```shell
bash .track/scripts/track-todo.sh --local
bash .track/scripts/track-todo.sh --offline
```

### Validation
Run Track validation after changing task files, project briefs, or task lifecycle scripts:

```shell
bash .track/scripts/track-validate.sh
```

### Working Principles

- **Investigate before implementing.** When a task has mode `investigate` or `plan`, explore the codebase thoroughly before writing code. Read related files, check for existing patterns, understand dependencies. Only move to implementation when you have a clear path.
- **Update task files as you work, not after.** When you discover new context, constraints, or dead ends, append to the task's `## Notes` immediately. Future sessions depend on this context.
- **Check for conflicts before starting.** Scan active and review tasks for overlapping `files:` globs. Starting work on contested files creates merge conflicts.
- **Scope aggressively.** If a task grows beyond its acceptance criteria, split the new work into a separate task rather than expanding the current one.
- **Let the system track status.** Don't manually update status fields to show progress. Open a draft PR — Track knows you're active. Mark it ready for review — Track knows you're in review. The PR lifecycle is the status lifecycle.
- **Validate early and often.** Run `bash .track/scripts/track-validate.sh` after every task file change. Errors caught locally are cheap; errors caught in CI block the team.
<!-- TRACK:END -->
