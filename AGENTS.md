# Agent Instructions

## Repository Overview

This repo is the Archeia monorepo. It contains two markdown-first products:

- **Archeia** — architecture knowledge generation and query skills
- **Track** — file-based multi-agent task coordination skills

The product surface is local skill packs, templates, protocol docs, and a small amount of maintenance tooling. There is no app server, no SaaS backend, and no compiled product runtime.

## Repository Structure

```
.claude/skills/               <- Canonical source for all skills
  archeia/                    <- /archeia write path + templates
  archeia-ask/                <- /archeia-ask read path
  track-*/                    <- Track coordination skills
plugins/                      <- Claude Code plugin distributions
  archeia/                    <- /archeia:init and /archeia:ask
  track/                      <- /track:* commands
skills/                       <- skills.sh / Codex / Cursor distributions
scripts/                      <- Maintenance scripts (skill sync, commit checks)
tools/                        <- Deterministic validation tooling
.track/                       <- Track protocol + dogfooding workspace
  tasks/                      <- Track task states and claims
  projects/                   <- Track project briefs for active initiatives
.archeia/                     <- Archeia's own product docs
docs/ONTOLOGY.md              <- Shared ontology + authority hierarchy
docs/designs/                 <- Strategic design documents
```

## Key Boundaries

- **Canonical source is `.claude/skills/`** — edit canonical skills first, then sync distributions
- **Skills are markdown-first** — product behavior lives in `SKILL.md`, templates, and `.track/PROTOCOL.md`
- **Protocols own durable contracts** — shared terms live in `docs/ONTOLOGY.md`, Track rules in `.track/PROTOCOL.md`, Archeia rules in `.archeia/PROTOCOL.md`
- **Track protocol is strict** — do not silently widen schema, status vocabulary, or claim rules
- **Maintenance tooling is local** — `scripts/sync-skills.sh` and `tools/track-lint.py` keep distributions and `.track/` honest
- **`.archeia/` is self-referential** — it documents this repo's own product architecture

## Working in This Repo

When modifying Archeia:
1. Edit `.claude/skills/archeia/` or `.claude/skills/archeia-ask/` directly
2. Keep templates minimal — structure and hints, not rigid prose
3. Run `bash scripts/sync-skills.sh` after changing canonical skill files or templates
4. Update `.archeia/` docs when Archeia's product direction, layout, or maintenance flow changes

When modifying Track:
1. Read `.track/PROTOCOL.md` before changing task schema, validation rules, or skill behavior
2. Edit `.claude/skills/track-*/` directly
3. Keep `tools/track-lint.py`, `.track/PROTOCOL.md`, and Track skill behavior aligned in the same change
4. Run `python3 tools/track-lint.py` and `python3 tools/tests/test_track_lint.py` when Track rules or tooling change

When modifying distributions:
1. Do not hand-edit generated copies in `plugins/*/skills/` or `skills/*/` unless you are fixing the sync process itself
2. Run `bash scripts/sync-skills.sh --check` before landing distribution-related changes

## What Not to Do

- Do not add a CLI, daemon, or cloud service
- Do not edit generated skill copies instead of the canonical source
- Do not silently widen Track's schema, statuses, priorities, types, or modes
- Do not modify `.archeia/` docs casually — they describe the repo's actual product architecture
