# Ontology

## Purpose

This document defines the shared vocabulary for the Archeia monorepo. It is the
cross-product contract that explains what the durable artifact types are, which
protocol governs them, and which file is authoritative when multiple views of
the same concept exist.

Use this document to resolve naming drift between Archeia, Track, repo docs,
and future validation tooling. Product-specific rules still live in their own
protocols.

## Source Of Truth Hierarchy

1. **Executable contracts** — the files that tooling or skills actually consume.
   - Track: `.track/PROTOCOL.md`, `tools/track-lint.py`
   - Archeia: `.claude/skills/archeia/SKILL.md`, `.claude/skills/archeia/templates/`
2. **Product protocols** — the markdown contracts that define how a document
   family is created, validated, and evolved.
   - Track: `.track/PROTOCOL.md`
   - Archeia: `.archeia/PROTOCOL.md`
3. **Shared definitions** — `docs/ONTOLOGY.md`
4. **Strategic direction** — `.archeia/ROADMAP.md`
5. **Operational work tracking** — `.track/`
6. **Pointers and views** — `TODO.md`, derived boards, summaries, or other
   convenience surfaces

If two files disagree, prefer the higher item in the hierarchy unless a human
explicitly redefines ownership in the relevant protocol.

## Core Terms

### Document

A markdown artifact governed by a protocol. Documents can be narrative,
generated, or coordination-oriented, but they become durable only when their
owning protocol defines how they are created and maintained.

Authoritative references: `.track/PROTOCOL.md`, `.archeia/PROTOCOL.md`

### Registry

A machine-readable configuration file that defines vocabulary or object
membership for a document family. In this repo the primary registry is
`.track/config.yaml`, which defines task vocabularies, numbered active
projects, and the counters used to allocate new project and task IDs.

Authoritative references: `.track/config.yaml`, `.track/PROTOCOL.md`

### Protocol

The rules for creating, validating, and evolving a document family. A protocol
defines ownership boundaries, structural requirements, and change rules for the
artifacts it governs.

Authoritative references: `.track/PROTOCOL.md`, `.archeia/PROTOCOL.md`

### Template

An Archeia generation contract for a document type. A template includes
frontmatter metadata plus markdown structure that tells the skill what evidence
to gather, which sections must exist, and how to self-validate the output.

Authoritative references: `.claude/skills/archeia/SKILL.md`, `.claude/skills/archeia/templates/`

### Knowledge Document

A generated or maintained document in `.archeia/` that captures a specific
facet of project understanding such as architecture, standards, assumptions, or
decisions.

Authoritative references: `.archeia/PROTOCOL.md`, `.claude/skills/archeia/templates/`

### Guidance Surface

The set of documents agents and humans read to understand how to work in a
repository: `.archeia/*.md` plus generated top-level `AGENTS.md` and
`CLAUDE.md`.

Authoritative references: `.archeia/PROTOCOL.md`, `.claude/skills/archeia/SKILL.md`

### Project Brief

A markdown scope contract for a Track project. It carries the narrative meaning
of a project — goal, boundaries, context, and success definition — while the
registry entry in `.track/config.yaml` carries the machine-readable metadata.

Authoritative references: `.track/PROTOCOL.md`, `.track/projects/`

### Task

A Track work item stored in `.track/tasks/{triage,todo,active,review,done,cancelled}/`
with frontmatter and required body sections. Tasks represent executable work,
not project strategy.

Authoritative references: `.track/PROTOCOL.md`, `tools/track-lint.py`

### Distribution

A packaged format for delivering skills to users. In this repo, distributions
are generated copies of the canonical skill sources.

Authoritative references: `plugins/`, `skills/`, `scripts/sync-skills.sh`

### View / Pointer

A non-canonical navigation surface that helps users find the real source of
truth. Pointer documents summarize where to look but do not own the underlying
state.

Authoritative references: `TODO.md`, `.track/BOARD.md` (derived)

## Document Families

### Archeia

- **Protocol:** `.archeia/PROTOCOL.md`
- **Executable contracts:** `.claude/skills/archeia/SKILL.md`, `.claude/skills/archeia/templates/`
- **Guidance output:** `.archeia/*.md`, `AGENTS.md`, `CLAUDE.md`
- **Strategy:** `.archeia/ROADMAP.md`

### Track

- **Protocol:** `.track/PROTOCOL.md`
- **Registry:** `.track/config.yaml`
- **Narrative scope contracts:** `.track/projects/*.md`
- **Operational work:** `.track/tasks/{triage,todo,active,review,done,cancelled}/`
- **Executable contract:** `tools/track-lint.py`

## Change Rules

1. **Do not create duplicate canonical specs.** If a new schema or spec file is
   introduced later, it must either become authoritative in tooling or be
   generated from the authoritative source.
2. **Keep machine and narrative contracts split.** Registry fields belong in
   `.track/config.yaml`; project scope belongs in `.track/projects/*.md`.
3. **Prefer protocol updates over scattered inline rules.** If a rule governs a
   document family, put it in the owning protocol and reference it elsewhere.
4. **Navigation files stay lightweight.** Pointer files such as `TODO.md` should
   direct users to the canonical surface instead of duplicating backlog state.
5. **When product shape changes, update the owning protocol in the same change.**
