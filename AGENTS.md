# Agent Instructions

## Repository Overview

This repo is the Archeia monorepo. It contains two markdown-first products:

- **Archeia** — architecture knowledge generation and query skills
- **Track** — git-native task coordination via `CLAUDE.md`, `.track/`, and Bash scripts

There is no app server, no SaaS backend, and no compiled product runtime.

## Repository Structure

```text
.claude/skills/               <- Canonical Archeia skill sources
  archeia/                    <- /archeia write path + templates
  archeia-ask/                <- /archeia-ask read path
plugins/                      <- Claude Code plugin distributions
  archeia/                    <- /archeia:init and /archeia:ask
skills/                       <- skills.sh / Codex / Cursor distributions
scripts/                      <- Maintenance scripts and Track helpers
.track/
  projects/                   <- Track project briefs
    README.md                 <- Project brief contract
  tasks/                      <- Flat Track task files
.archeia/                     <- Archeia's own product docs
CLAUDE.md                     <- Always-on repo and Track workflow guide
TODO.md                       <- Generated, gitignored Track view
docs/ONTOLOGY.md              <- Shared ontology + authority hierarchy
```

## Key Boundaries

- **Canonical Archeia source is `.claude/skills/`** — edit canonical skills first, then sync distributions
- **Track is instruction-first** — the durable coordination contract lives in `CLAUDE.md`, `.track/projects/*.md`, and `.track/tasks/*.md`
- **Track in-flight state is git-native** — default-branch task files own backlog state; open GitHub PRs own effective `active` / `review`
- **`TODO.md` is derived** — regenerate it with `bash scripts/track-todo.sh`; never treat it as canonical
- **Validation is local-first Bash** — `scripts/track-validate.sh` is the enforcement layer for Track state
- **`.archeia/` is self-referential** — it documents this repo's own product architecture

## Working in This Repo

When modifying Archeia:
1. Edit `.claude/skills/archeia/` or `.claude/skills/archeia-ask/` directly
2. Keep templates minimal — structure and hints, not rigid prose
3. Run `bash scripts/sync-skills.sh` after changing canonical skill files or templates
4. Update `.archeia/` docs when Archeia's product direction, layout, or maintenance flow changes

When modifying Track:
1. Read `CLAUDE.md` and `docs/ONTOLOGY.md` before changing task schema, task lifecycle, or generator behavior
2. Edit `.track/projects/*.md` for scope and `.track/tasks/*.md` for work items
3. Keep `scripts/track-validate.sh`, `scripts/track-todo.sh`, `CLAUDE.md`, and `.track/projects/README.md` aligned in the same change when rules move
4. Refresh the derived view with `bash scripts/track-todo.sh` after Track state changes
5. Run `bash scripts/track-validate.sh` when Track rules or task files change

When modifying distributions:
1. Do not hand-edit generated copies in `plugins/archeia/` or `skills/archeia-*` unless you are fixing the sync process itself
2. Run `bash scripts/sync-skills.sh --check` before landing distribution-related changes

## What Not to Do

- Do not add a CLI, daemon, or cloud service
- Do not edit generated Archeia copies instead of the canonical source
- Do not reintroduce `.track/config.yaml`, `.track/PROTOCOL.md`, claims, status subdirectories, or Python Track tooling
- Do not hand-edit `TODO.md`; regenerate it from canonical Track state
- Do not modify `.archeia/` docs casually — they describe the repo's actual product architecture
