# Archeia Monorepo

Local-first guidance and coordination for AI coding agents.

This repo ships two sibling products:

- **Archeia** — generates and maintains architecture guidance that agents actually read
- **Track** — coordinates work through repo-local task files, `CLAUDE.md`, and GitHub PR state

## Products

### Archeia

Archeia generates and maintains repo guidance such as:

- `.archeia/` — knowledge base (architecture, decisions, constraints, standards)
- `AGENTS.md` — behavioral contract for agent work
- `CLAUDE.md` — Claude-specific workflow guide

Standalone commands:

- `/archeia`
- `/archeia-ask ...`

Plugin commands:

- `/archeia:init`
- `/archeia:ask ...`

### Track

Track is a zero-dependency repo convention:

- `CLAUDE.md` — always-on task coordination instructions
- `.track/projects/*.md` — project briefs
- `.track/tasks/*.md` — flat task files
- `scripts/track-validate.sh` — Bash validation
- `scripts/track-todo.sh` — shared `TODO.md` generation
- `TODO.md` — generated view from default-branch `.track/` plus live open PR metadata

Track does not ship a plugin, daemon, claim system, or Python runtime.

## Install

### Claude Code plugin

Run the Archeia plugin locally during development and testing:

```shell
claude --plugin-dir ./plugins/archeia
```

### Canonical Claude skills

Copy the canonical Archeia skill directories from `.claude/skills/` into your repo's `.claude/skills/` directory.

- `.claude/skills/archeia/`
- `.claude/skills/archeia-ask/`

### skills.sh / Codex / Cursor distribution

Use the generated `skills/` directories with tools that consume the Agent Skills format.

- `skills/archeia-init/`
- `skills/archeia-ask/`

## Development

- Canonical Archeia source lives in `.claude/skills/`
- Shared definitions live in `docs/ONTOLOGY.md`
- Archeia protocol lives in `.archeia/PROTOCOL.md`
- Sync generated Archeia distributions with `bash scripts/sync-skills.sh`
- Verify generated copies with `bash scripts/sync-skills.sh --check`
- Validate Track state with `bash scripts/track-validate.sh`
- Regenerate the shared Track view with `bash scripts/track-todo.sh`
- Conductor `setup` / `run` regenerate `TODO.md` for the workspace
- `gh` is used opportunistically for live PR overlays in `TODO.md`

## Layout

- `plugins/` — Claude Code plugin distributions
- `skills/` — generated standalone Archeia skill distributions
- `scripts/` — maintenance and Track helper scripts
- `docs/ONTOLOGY.md` — shared ontology and source-of-truth hierarchy
- `.claude/skills/` — canonical skill sources
- `.track/` — Track project briefs and task files
- `.archeia/` — Archeia's own product docs
- `TODO.md` — generated, gitignored Track view

## License

MIT
