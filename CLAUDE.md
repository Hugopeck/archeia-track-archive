# Claude Code Instructions

## Project Context

This is the Archeia monorepo. It ships two local-first products:

- **Archeia** — architecture knowledge generation and query skills
- **Track** — file-based multi-agent coordination skills

Most product logic lives in markdown skill files, Archeia templates, and Track protocol docs. The only deterministic code path is Track's Python validator.

## Key Files

- `.claude/skills/archeia/SKILL.md` — Archeia write-path skill
- `.claude/skills/archeia-ask/SKILL.md` — Archeia query skill
- `.claude/skills/track-*/SKILL.md` — Track coordination skills
- `.claude/skills/archeia/templates/` — Archeia's canonical template set
- `docs/ONTOLOGY.md` — shared ontology and source-of-truth hierarchy
- `plugins/archeia/` — Claude Code plugin distribution for `/archeia:init` and `/archeia:ask`
- `plugins/track/` — Claude Code plugin distribution for `/track:*`
- `skills/` — skills.sh / Codex / Cursor distributions
- `.track/config.yaml` — Track registry for vocabulary, project membership, and counters
- `.track/PROTOCOL.md` — source of truth for Track's task format and coordination rules
- `.track/projects/` — Track project briefs for active projects
- `.track/projects/README.md` — project brief contract and required sections
- `.track/tasks/` — Track task-state directories and claim files
- `.track/tasks/README.md` — task-layout, dotted-ID, and claim conventions
- `PROJECTS.md` — gitignored root portfolio view derived from Track state
- `TASKS.md` — gitignored root task index derived from Track state
- `BOARD.md` — gitignored root kanban view derived from Track state
- `conductor.json` — shared Conductor setup/run automation for local Track views
- `tools/track-build.py` — deterministic Track board/index generator entrypoint
- `tools/track-watch.py` — local polling watcher for live Track board refresh
- `tools/track-lint.py` — deterministic Track validator used in CI
- `scripts/track-build.sh` — shell wrapper used by skills and Conductor
- `scripts/sync-skills.sh` — syncs canonical skills to both distribution targets
- `.releaserc.json` — semantic-release configuration for versioning and GitHub releases
- `.github/workflows/ci.yml` — sync check + Track validation
- `.github/workflows/release.yml` — release automation on pushes to `main`
- `.archeia/` — Archeia's own product documentation (self-referential)
- `.archeia/PROTOCOL.md` — Archeia protocol for document families and maintenance modes
- `TODO.md` — pointer to the operational backlog in `.track/`

## Workflow

- This repo has no app build step and no service runtime
- GitHub Actions runs semantic-release on pushes to `main`
- CI checks skill sync plus Track validation and tests
- Most changes are documentation and skill markdown changes
- Use conventional commits so release automation can infer versions
- Keep PRs focused — one concern per PR

## Commit Conventions

| Prefix | Bump | When to use |
|--------|------|-------------|
| `feat(archeia):` | Minor | New Archeia capability or template change |
| `feat(track):` | Minor | New Track skill or protocol capability |
| `fix(skills):` | Patch | Fix in skill logic, sync logic, or distribution content |
| `fix(track):` | Patch | Fix in Track protocol or validator behavior |
| `docs:` | None | Routine documentation edits that should not release |
| `feat!:` / `fix!:` | Major | Breaking change to a public skill interface or protocol |

## Important Context

- Archeia was extracted from a larger TypeScript monorepo — the historical packages are gone
- Track is now co-located here as a sibling product with its own protocol and validator
- Lifecycle hooks were evaluated and rejected — native doc loading, local board refresh, and CI checks are sufficient
- Edit canonical skills in `.claude/skills/` first, then run `bash scripts/sync-skills.sh`
- `.track/config.yaml` owns Track's machine-readable registry; `.track/projects/*.md` owns project narrative scope
- Open work lives in `.track/tasks/{triage,todo,active,review}/`; historical work lives in `.track/tasks/{done,cancelled}/`
- Open Track tasks use dotted IDs like `4.5`; legacy numeric IDs are historical-only
- Track changes that touch protocol or local board tooling should run `bash scripts/track-build.sh`, `python3 tools/track-lint.py`, `python3 tools/tests/test_track_lint.py`, and `python3 tools/tests/test_track_build.py`
- `PROJECTS.md`, `TASKS.md`, and `BOARD.md` are gitignored root Track projections; `.track/index.json` is their machine-readable sibling
- Conductor `setup` prebuilds local Track views and Conductor `run` starts `bash scripts/track-watch.sh`
- `TODO.md` is a pointer into `.track/`, not the canonical backlog
- Read `.archeia/VISION.md` and `.archeia/PRODUCT.md` for full product context
