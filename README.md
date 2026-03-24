# Archeia

Local-first architecture guidance for AI coding agents.

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

## Layout

- `plugins/` — Claude Code plugin distributions
- `skills/` — generated standalone Archeia skill distributions
- `scripts/` — maintenance scripts
- `docs/ONTOLOGY.md` — shared ontology and source-of-truth hierarchy
- `.claude/skills/` — canonical skill sources
- `.archeia/` — Archeia's own product docs

## License

MIT
