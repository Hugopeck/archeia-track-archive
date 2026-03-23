# Track Projects

This directory contains the narrative scope contracts for active Track projects.

## Purpose

Each project brief explains the initiative behind a group of tasks. The brief owns
scope, boundaries, shared context, and success definition. `.track/config.yaml`
owns the machine-readable registry for the same projects.

## Conventions

- Active brief paths use `.track/projects/{project-number}-{slug}.md`
- The H1 must match the project's `title` in `.track/config.yaml`
- Briefs are markdown-only in this phase; do not add frontmatter
- Archived projects may exist only in `.track/config.yaml` without a brief

## Required Sections

- `## Goal`
- `## Why Now`
- `## In Scope`
- `## Out Of Scope`
- `## Shared Context`
- `## Dependency Notes`
- `## Success Definition`
- `## Candidate Task Seeds`

See `.track/PROTOCOL.md` for the full contract.
