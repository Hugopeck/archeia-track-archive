# Ontology

## Purpose

This document defines the shared vocabulary for the Archeia repo. It explains
which artifacts are durable, which surfaces are derived, and which file wins
when multiple views of the same concept exist.

## Source Of Truth Hierarchy

1. **Canonical repo state**
   - Archeia: `.claude/skills/archeia/SKILL.md`, `.claude/skills/archeia/templates/`, `.claude/skills/archeia-ask/SKILL.md`
2. **Always-on workflow instructions**
   - `CLAUDE.md`
   - `AGENTS.md`
3. **Executable maintenance contracts**
   - `scripts/sync-skills.sh`
4. **Shared definitions**
   - `docs/ONTOLOGY.md`
5. **Strategic direction**
   - `.archeia/ROADMAP.md`

If two files disagree, prefer the higher item in the hierarchy unless a human
explicitly redefines ownership.

## Core Terms

### Document

A markdown artifact with a durable owner and maintenance path.

### Protocol

A product-specific rule set for creating and maintaining a document family.
Archeia has an explicit protocol in `.archeia/PROTOCOL.md`.

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

### Distribution

A generated format for delivering Archeia skills to other tools or environments.

## Document Families

### Archeia

- **Protocol:** `.archeia/PROTOCOL.md`
- **Executable contracts:** `.claude/skills/archeia/SKILL.md`, `.claude/skills/archeia/templates/`, `.claude/skills/archeia-ask/SKILL.md`
- **Guidance output:** `.archeia/*.md`, `AGENTS.md`, `CLAUDE.md`
- **Strategy:** `.archeia/ROADMAP.md`

## Change Rules

1. **Do not create duplicate canonical specs.**
2. **Keep derived files lightweight.**
3. **When product shape changes, update instructions and scripts together.**
