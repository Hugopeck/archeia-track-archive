# Markdown Validation Architecture

## Purpose

This design describes the future validation architecture for markdown-first
artifacts in the Archeia monorepo. It deliberately stops at architecture and
contract boundaries; it does not introduce a generic validation engine or a new
canonical schema surface in this migration.

## Goals

- make validation rules legible across Track, Archeia, and future document families
- preserve a single canonical extraction path for each rule
- avoid shadow specs that drift away from the files agents and scripts actually read

## Four Validation Levels

| Level | What it validates | Canonical source today | Likely execution surface |
|-------|-------------------|------------------------|--------------------------|
| 1. Frontmatter / lightweight schema | required fields, allowed values, path conventions | `CLAUDE.md`, `.track/projects/*.md`, `.track/tasks/*.md` | deterministic CI/local checks |
| 2. Structural contract | required headings, section order, document-family structure | `CLAUDE.md`, `.track/projects/README.md`, Archeia templates, `.archeia/PROTOCOL.md` | deterministic CI/local checks |
| 3. Formatting | markdown style and lint rules | formatter/linter configuration | deterministic CI/local checks |
| 4. Semantic quality | evidence quality, truthfulness, completeness, rubric fit | template validation guidance and protocol-level quality rules | on-demand or assisted validation |

## Canonicality Rule

Future generic schema or spec files are allowed only when one of these is true:

1. the tooling reads them as the authoritative source, or
2. they are generated mirrors of the authoritative source

Hand-maintained duplicate schema files are out of scope because they create a
shadow spec that will eventually diverge from the real contracts.

## Current Canonical Sources

### Track

- `CLAUDE.md` defines the operative Track workflow and task lifecycle
- `.track/projects/*.md` define project scope and membership by `project_id`
- `.track/tasks/*.md` define backlog state on the default branch
- open GitHub PRs define effective in-flight state for non-terminal tasks
- `scripts/track-validate.sh` and `scripts/track-todo.sh` are the executable maintenance contracts

### Archeia

- `.archeia/PROTOCOL.md` defines document-family ownership and maintenance modes
- `.claude/skills/archeia/SKILL.md` defines template meta-structure and workflow
- `.claude/skills/archeia/templates/*.md` define template-specific structure and semantic rubrics

## Extraction Path For Future Tooling

If a generic markdown validation pipeline is built later, the preferred order is:

1. extract rules from the owning protocol, instruction surface, or template contract
2. normalize them into a machine-readable intermediate representation if needed
3. run deterministic checks against that representation
4. optionally layer semantic or assisted evaluation on top

The extraction step matters more than the eventual tool choice because that is
what prevents drift between prose contracts and executable checks.

## Non-Deliverables In This Migration

- no hand-maintained duplicate schema files
- no generic `md-lint.py`
- no new CI lane covering every markdown family
- no attempt to retrofit every archived document into a new validation format

## Follow-On Work

The `markdown-validation-architecture` Track project should decide:

- which document families justify deterministic validation first
- whether a single validator should span Track and Archeia or only share extraction concepts
- when formatting rules are worth enforcing repo-wide
- which semantic checks are valuable enough to keep as explicit rubrics
