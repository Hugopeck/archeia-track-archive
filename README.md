# Archeia Monorepo

Local-first skill packs for AI coding agents.

This repo now ships two sibling products:

- **Archeia** — generates and maintains architecture guidance that agents actually read
- **Track** — coordinates parallel agent work through repo-local `.track/` task files

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

Track keeps multi-agent coordination inside the repository:

- `.track/PROTOCOL.md` — task and claim protocol
- `.track/config.yaml` — schema vocabulary and ID counter
- `.track/{triage,todo,active,review,done,cancelled}/` — task states
- `.track/claims/` — advisory task claims

Plugin commands:

- `/track:init`, `/track:new`, `/track:move`, `/track:show`, `/track:list`
- `/track:board`, `/track:stats`, `/track:claim`, `/track:release`
- `/track:available`, `/track:validate`, `/track:decompose`, `/track:plan`

## Install

### Claude Code plugins

Run either plugin locally during development and testing:

```shell
claude --plugin-dir ./plugins/archeia
claude --plugin-dir ./plugins/track
```

### Canonical Claude skills

Copy the canonical skill directories from `.claude/skills/` into your repo's `.claude/skills/` directory.

- Archeia: `.claude/skills/archeia/`, `.claude/skills/archeia-ask/`
- Track: `.claude/skills/track-*/`

### skills.sh / Codex / Cursor distribution

Use the generated `skills/` directories with tools that consume the Agent Skills format.

- Archeia: `skills/archeia-init/`, `skills/archeia-ask/`
- Track: `skills/track-*/`

## Development

- Canonical source lives in `.claude/skills/`
- Sync generated distributions with `bash scripts/sync-skills.sh`
- Verify generated copies with `bash scripts/sync-skills.sh --check`
- Validate Track dogfooding with `python3 tools/track-lint.py`
- Run Track validator tests with `python3 tools/tests/test_track_lint.py`

`tools/track-lint.py` requires `pyyaml` when run locally.

## Layout

- `plugins/` — Claude Code plugin distributions
- `skills/` — skills.sh / Codex / Cursor distributions
- `scripts/` — maintenance scripts
- `tools/` — deterministic validation tooling
- `.claude/skills/` — canonical skill sources
- `.track/` — Track dogfooding workspace
- `.archeia/` — Archeia's own product docs

## License

MIT
