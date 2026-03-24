# Ontology

## Purpose

This document defines the shared vocabulary for the Archeia monorepo. It explains
which artifacts are durable, which surfaces are derived, and which file wins
when multiple views of the same concept exist.

Use this document to resolve naming drift between Archeia, Track, repo docs,
and maintenance scripts.

## Source Of Truth Hierarchy

1. **Canonical repo state**
   - Track: default-branch `.track/projects/*.md`, default-branch `.track/tasks/*.md`, and open GitHub PR metadata for in-flight state
   - Archeia: `.claude/skills/archeia/SKILL.md`, `.claude/skills/archeia/templates/`, `.claude/skills/archeia-ask/SKILL.md`
2. **Always-on workflow instructions**
   - `CLAUDE.md`
   - `AGENTS.md`
3. **Executable maintenance contracts**
   - `scripts/track-validate.sh`
   - `scripts/track-todo.sh`
   - `scripts/sync-skills.sh`
4. **Shared definitions**
   - `docs/ONTOLOGY.md`
5. **Strategic direction**
   - `.archeia/ROADMAP.md`
6. **Derived navigation surfaces**
   - `TODO.md`

If two files disagree, prefer the higher item in the hierarchy unless a human
explicitly redefines ownership.

## Core Terms

### Document

A markdown artifact with a durable owner and maintenance path.

### Protocol

A product-specific rule set for creating and maintaining a document family.
Archeia has an explicit protocol in `.archeia/PROTOCOL.md`. Track's operative
rules live in `CLAUDE.md` plus the Track Bash scripts.

### Template

An Archeia generation contract for a document type. Templates define the shape,
required sections, and evidence expectations for generated guidance.

### Knowledge Document

A generated or maintained document in `.archeia/` that captures architecture,
standards, assumptions, or decisions.

### Guidance Surface

A document humans and agents read to understand how to work in a repository.
In this repo the main guidance surfaces are `.archeia/*.md`, `AGENTS.md`, and
`CLAUDE.md`.

### Project Brief

A markdown scope contract in `.track/projects/{project_id}-{slug}.md`. The brief
owns project goal, boundaries, and success definition.

### Task

A Track work item stored at `.track/tasks/{task_id}-{slug}.md` with YAML
frontmatter and required body sections.

### Raw Status

The `status:` field stored in a Track task file.

### Effective Status

The status shown in `TODO.md`. Effective status is derived from raw status plus
live open PR state.

### Provisional PR

An implementation PR opened as soon as work starts on a task. A draft PR makes a
non-terminal task effectively `active`; a ready-for-review PR makes it
effectively `review`.

### Distribution

A generated format for delivering Archeia skills to other tools or environments.

### View / Pointer

A non-canonical navigation surface. `TODO.md` is the primary Track view in this
repo, but it never owns the underlying work state.

## Document Families

### Archeia

- **Protocol:** `.archeia/PROTOCOL.md`
- **Executable contracts:** `.claude/skills/archeia/SKILL.md`, `.claude/skills/archeia/templates/`, `.claude/skills/archeia-ask/SKILL.md`
- **Guidance output:** `.archeia/*.md`, `AGENTS.md`, `CLAUDE.md`
- **Strategy:** `.archeia/ROADMAP.md`

### Track

- **Project briefs:** `.track/projects/*.md`
- **Task files:** `.track/tasks/*.md`
- **Always-on instructions:** `CLAUDE.md`
- **Executable contracts:** `scripts/track-validate.sh`, `scripts/track-todo.sh`
- **Derived view:** `TODO.md`

## Change Rules

1. **Do not create duplicate canonical specs.** New Track rules should land in `CLAUDE.md` and the Bash scripts, not in a second protocol file.
2. **Keep project scope and executable work separate.** Scope belongs in `.track/projects/*.md`; work belongs in `.track/tasks/*.md`.
3. **Keep derived files lightweight.** `TODO.md` summarizes the backlog but never replaces `.track/` or PR metadata.
4. **Prefer Bash for Track maintenance.** Validation and generation should stay dependency-light and repo-local.
5. **When product shape changes, update instructions and scripts together.**
