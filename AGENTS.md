# Agent Instructions

## Repository Overview

Archeia is an architecture knowledge framework delivered as Claude Code skills. It generates and maintains `.archeia/` documentation, `AGENTS.md`, and `CLAUDE.md` for any repository.

The product is two skills plus templates — no CLI, no binary, no cloud service.

## Repository Structure

```
.claude/skills/archeia/       <- /archeia skill (generate + maintain docs)
.claude/skills/archeia-ask/   <- /archeia-ask skill (query the knowledge base)
archeia-plugin/               <- Claude Code plugin distribution
skills/                       <- Agent Skills distribution for Codex/Cursor/etc.
scripts/                      <- Maintenance scripts (template sync, etc.)
.archeia/                     <- Archeia's own knowledge base (product docs)
docs/designs/                 <- Strategic design documents
```

## Key Boundaries

- **Skills are markdown** — all product logic lives in SKILL.md files and templates
- **No runtime dependencies** — no package.json, no build step, no compiled output
- **Templates drive consistency** — `.claude/skills/archeia/templates/` contains the 10 template files that shape output
- **`.archeia/` is self-referential** — this repo uses Archeia on itself

## Working in This Repo

When modifying skills:
1. Edit the SKILL.md files directly
2. Test in a sample repo via `/archeia` or `/archeia-ask`, or via the plugin as `/archeia:init` or `/archeia:ask`
3. Update `.archeia/` docs if product direction changes

When modifying templates:
1. Templates are in `.claude/skills/archeia/templates/`
2. Changes affect what `/archeia` generates in customer repos
3. Keep templates minimal — provide structure and hints, not rigid prose
4. Update all copies: `.claude/skills/archeia/templates/`, `archeia-plugin/skills/init/templates/`, and `skills/archeia-init/templates/`

## What Not to Do

- Do not add runtime dependencies or build tooling
- Do not create a CLI entrypoint
- Do not add lifecycle hooks (evaluated and rejected — see `.archeia/DECISIONS.md`)
- Do not modify `.archeia/` docs without understanding they describe the product itself
