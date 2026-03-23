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
tools/                        <- Deterministic validation and board tooling
PROJECTS.md                   <- Gitignored root portfolio view derived from Track state
TASKS.md                      <- Gitignored root task index derived from Track state
BOARD.md                      <- Gitignored root kanban view derived from Track state
.track/                       <- Track protocol + dogfooding workspace
  config.yaml                 <- Track registry for vocabularies, projects, and counters
  projects/                   <- Track project briefs for active initiatives
    README.md                 <- Project brief contract and required sections
  tasks/                      <- Track task states and claims
    README.md                 <- Task/claim layout and ID conventions
.archeia/                     <- Archeia's own product docs
docs/ONTOLOGY.md              <- Shared ontology + authority hierarchy
docs/designs/                 <- Strategic design documents
```

## Key Boundaries

- **Canonical source is `.claude/skills/`** — edit canonical skills first, then sync distributions
- **Skills are markdown-first** — product behavior lives in `SKILL.md`, templates, and `.track/PROTOCOL.md`
- **Protocols own durable contracts** — shared terms live in `docs/ONTOLOGY.md`, Track rules in `.track/PROTOCOL.md`, Archeia rules in `.archeia/PROTOCOL.md`
- **Registry and briefs have separate jobs** — `.track/config.yaml` owns Track vocabulary, project membership, and counters; `.track/projects/*.md` owns narrative scope and success definition
- **Track protocol is strict** — do not silently widen schema, status vocabulary, or claim rules
- **Maintenance tooling is local** — `scripts/sync-skills.sh`, `tools/track-lint.py`, and `tools/track-build.py` keep distributions and local Track views honest
- **`.archeia/` is self-referential** — it documents this repo's own product architecture

## Working in This Repo

When modifying Archeia:
1. Edit `.claude/skills/archeia/` or `.claude/skills/archeia-ask/` directly
2. Keep templates minimal — structure and hints, not rigid prose
3. Run `bash scripts/sync-skills.sh` after changing canonical skill files or templates
4. Update `.archeia/` docs when Archeia's product direction, layout, or maintenance flow changes

When modifying Track:
1. Read `.track/PROTOCOL.md` and `docs/ONTOLOGY.md` before changing task schema, validation rules, or skill behavior
2. Edit `.claude/skills/track-*/` directly
3. Treat `.track/config.yaml` as the machine-readable registry and `.track/projects/*.md` as the narrative scope contract
4. Keep `tools/track-lint.py`, `tools/track-build.py`, `.track/PROTOCOL.md`, `.track/tasks/README.md`, and `.track/projects/README.md` aligned in the same change when rules move
5. Refresh local derived views with `bash scripts/track-build.sh` after Track state changes or skill updates that affect the board
6. Run `python3 tools/track-lint.py`, `python3 tools/tests/test_track_lint.py`, and `python3 tools/tests/test_track_build.py` when Track rules or tooling change

When modifying distributions:
1. Do not hand-edit generated copies in `plugins/*/skills/` or `skills/*/` unless you are fixing the sync process itself
2. Run `bash scripts/sync-skills.sh --check` before landing distribution-related changes

## What Not to Do

- Do not add a CLI, daemon, or cloud service
- Do not edit generated skill copies instead of the canonical source
- Do not silently widen Track's schema, statuses, priorities, types, or modes
- Do not reintroduce legacy flat `.track/{status}/` task paths or `.track/claims/` claim paths
- Do not hand-edit `PROJECTS.md`, `TASKS.md`, `BOARD.md`, or `.track/index.json`; rebuild them from canonical Track state
- Do not modify `.archeia/` docs casually — they describe the repo's actual product architecture
