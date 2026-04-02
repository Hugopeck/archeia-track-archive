---
title: "PR Instructions"
status: approved
created: 2026-04-02
updated: 2026-04-02
---

## Purpose

Use this when opening or updating a PR in this repo.
Keep it simple: link tracked work correctly, let Track own task status, and keep PRs mergeable under the `main` branch rules.

## Tracked PRs

Use a tracked PR when the work matches one task.

- branch: `task/{id}-{slug}`
- title: include the task ID, such as `[6.2] ...` or `feat(scope): [6.2] ...`
- body: include `Track-Task: {id}` on its own line
- draft PR means the task should be `active`
- ready-for-review PR means the task should be `review`

Do not hand-edit task status to `done`; Track handles completion after merge.

## Untracked PRs

Use an untracked PR when no task clearly fits.

- any non-`task/` branch is fine
- start the body with `untracked task`
- do not mutate `.track/tasks/*.md` just to make the PR fit a task

The automated changelog PRs are untracked PRs.

## Before Review

Before asking for review or merging:

1. run `bash .track/scripts/track-validate.sh`
2. make sure required checks are green
3. rebase or merge `main` if the PR is behind
4. confirm the PR title and body still match the task, if tracked

## Release Note

Releases publish from `main`, but release automation does not push commits back to `main`.
Instead, published release notes are copied into `CHANGELOG.md` by a separate PR flow.
