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
- `plugins/archeia/` — Claude Code plugin distribution for `/archeia:init` and `/archeia:ask`
- `plugins/track/` — Claude Code plugin distribution for `/track:*`
- `skills/` — skills.sh / Codex / Cursor distributions
- `.track/PROTOCOL.md` — source of truth for Track's task format and coordination rules
- `tools/track-lint.py` — deterministic Track validator used in CI
- `scripts/sync-skills.sh` — syncs canonical skills to both distribution targets
- `.releaserc.json` — semantic-release configuration for versioning and GitHub releases
- `.github/workflows/ci.yml` — sync check + Track validation
- `.github/workflows/release.yml` — release automation on pushes to `main`
- `.archeia/` — Archeia's own product documentation (self-referential)
- `TODO.md` — current development priorities

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
- Lifecycle hooks were evaluated and rejected — native doc loading + CI checks are sufficient
- Edit canonical skills in `.claude/skills/` first, then run `bash scripts/sync-skills.sh`
- Track changes that touch protocol or lint rules should also run `python3 tools/track-lint.py` and `python3 tools/tests/test_track_lint.py`
- Read `.archeia/VISION.md` and `.archeia/PRODUCT.md` for full product context
