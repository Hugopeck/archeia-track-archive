---
name: archeia-ask
version: 0.1.0
description: |
  Answer architecture questions from an existing Archeia knowledge base. Use
  this skill to load `.archeia/` docs, `AGENTS.md`, and `CLAUDE.md`, then
  explain system boundaries, decisions, constraints, and likely change points
  without regenerating the docs.
---

## Purpose

`archeia-ask` is the read path for Archeia.

Use it when the repo already has an Archeia knowledge base and the user wants answers, not regeneration.

## Workflow

1. Load `AGENTS.md` and `CLAUDE.md` if present.
2. Load the relevant `.archeia/*.md` docs for the question.
3. Answer from the documented knowledge base first.
4. Point to evidence files when a claim matters.
5. Call out stale or missing docs when they limit confidence.
6. Recommend `archeia-init` when the right answer requires regeneration or maintenance.

## Operating Rules

- Do not silently rewrite docs.
- Distinguish documented facts from reasonable inference.
- Prefer concise answers that name the right files, decisions, and constraints.
- If the knowledge base is thin, say so clearly.

## Good Questions

- What should I read before changing this subsystem?
- Why was this boundary introduced?
- Which constraints matter before I add a new dependency?
- Where should a new feature likely live?
- Which assumptions look fragile right now?
