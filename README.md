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
- `.track/config.yaml` — schema vocabulary, project registry, and counters
- `.track/projects/` — project briefs for active initiatives
- `.track/projects/README.md` — project brief conventions and required sections
- `.track/tasks/{triage,todo,active,review,done,cancelled}/` — task states
- `.track/tasks/claims/` — advisory task claims
- `.track/tasks/README.md` — task-state and claim-layout overview
- `PROJECTS.md` — gitignored root portfolio view generated from Track state
- `TASKS.md` — gitignored root task index generated from Track state
- `BOARD.md` — gitignored root kanban generated from Track state

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

Shared Conductor workspaces can also use the committed `conductor.json` to prebuild the local Track views on setup and run a watcher from the Run button.

### skills.sh / Codex / Cursor distribution

Use the generated `skills/` directories with tools that consume the Agent Skills format.

- Archeia: `skills/archeia-init/`, `skills/archeia-ask/`
- Track: `skills/track-*/`

## Development

- Canonical source lives in `.claude/skills/`
- Shared definitions live in `docs/ONTOLOGY.md`
- Archeia protocol lives in `.archeia/PROTOCOL.md`
- Sync generated distributions with `bash scripts/sync-skills.sh`
- Verify generated copies with `bash scripts/sync-skills.sh --check`
- Refresh local derived views with `bash scripts/track-build.sh`
- Conductor `setup` builds `PROJECTS.md`, `TASKS.md`, `BOARD.md`, and `.track/index.json` for each new workspace
- Conductor `run` launches `bash scripts/track-watch.sh` for live local refresh of all Track views
- Validate Track dogfooding with `python3 tools/track-lint.py`
- Run Track validator tests with `python3 tools/tests/test_track_lint.py`
- Run Track board/index tests with `python3 tools/tests/test_track_build.py`

`tools/track-lint.py` and `tools/track-build.py` require `pyyaml` when run locally.

## Layout

- `plugins/` — Claude Code plugin distributions
- `skills/` — skills.sh / Codex / Cursor distributions
- `scripts/` — maintenance scripts
- `tools/` — deterministic validation and derived-view tooling
- `docs/ONTOLOGY.md` — shared ontology and source-of-truth hierarchy
- `.claude/skills/` — canonical skill sources
- `.track/` — Track dogfooding workspace
- `.track/projects/` — Track project briefs
- `PROJECTS.md` — gitignored root portfolio view derived from Track state
- `TASKS.md` — gitignored root task index derived from Track state
- `BOARD.md` — gitignored root kanban view derived from Track state
- `.archeia/` — Archeia's own product docs

## License

MIT
