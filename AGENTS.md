# Agent Instructions

## Repository Overview

This repo is the Archeia repo. It contains a markdown-first architecture knowledge product:

- **Archeia** — architecture knowledge generation and query skills

There is no app server, no SaaS backend, and no compiled product runtime.

## Repository Structure

```text
.claude/skills/               <- Canonical Archeia skill sources
  archeia/                    <- /archeia write path + templates
  archeia-ask/                <- /archeia-ask read path
plugins/                      <- Claude Code plugin distributions
  archeia/                    <- /archeia:init and /archeia:ask
skills/                       <- skills.sh / Codex / Cursor distributions
scripts/                      <- Maintenance scripts
.archeia/                     <- Archeia's own product docs
CLAUDE.md                     <- Always-on repo workflow guide
docs/ONTOLOGY.md              <- Shared ontology + authority hierarchy
```

## Key Boundaries

- **Canonical Archeia source is `.claude/skills/`** — edit canonical skills first, then sync distributions
- **`.archeia/` is self-referential** — it documents this repo's own product architecture

## Working in This Repo

When modifying Archeia:
1. Edit `.claude/skills/archeia/` or `.claude/skills/archeia-ask/` directly
2. Keep templates minimal — structure and hints, not rigid prose
3. Run `bash scripts/sync-skills.sh` after changing canonical skill files or templates
4. Update `.archeia/` docs when Archeia's product direction, layout, or maintenance flow changes

When modifying distributions:
1. Do not hand-edit generated copies in `plugins/archeia/` or `skills/archeia-*` unless you are fixing the sync process itself
2. Run `bash scripts/sync-skills.sh --check` before landing distribution-related changes

## What Not to Do

- Do not add a CLI, daemon, or cloud service
- Do not edit generated Archeia copies instead of the canonical source
- Do not modify `.archeia/` docs casually — they describe the repo's actual product architecture
