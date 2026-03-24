# Claude Code Instructions

## Project Context

This is the Archeia repo. It ships architecture knowledge generation and query skills for AI coding agents.

## Key Files

- `.claude/skills/archeia/SKILL.md` — Archeia write-path skill
- `.claude/skills/archeia-ask/SKILL.md` — Archeia query skill
- `.claude/skills/archeia/templates/` — Archeia canonical template set
- `plugins/archeia/` — Claude Code plugin distribution for `/archeia:init` and `/archeia:ask`
- `skills/archeia-init/`, `skills/archeia-ask/` — generated standalone distributions
- `docs/ONTOLOGY.md` — shared ontology and source-of-truth hierarchy
- `scripts/sync-skills.sh` — syncs Archeia canonical skills to distribution targets
- `.github/workflows/ci.yml` — Archeia sync check
- `.archeia/` — Archeia's own product documentation
- `.archeia/PROTOCOL.md` — Archeia protocol for document families and maintenance modes

## Workflow

- This repo has no app build step and no service runtime
- GitHub Actions runs semantic-release on pushes to `main`
- CI checks Archeia distribution sync (`ci.yml`)
- Most changes are documentation or skill markdown
- Use conventional commits so release automation can infer versions
- Keep PRs focused — one concern per PR

## Commit Conventions

| Prefix | Bump | When to use |
|--------|------|-------------|
| `feat(archeia):` | Minor | New Archeia capability or template change |
| `fix(skills):` | Patch | Fix in Archeia skill logic, sync logic, or generated content |
| `docs:` | None | Routine documentation edits that should not release |
| `feat!:` / `fix!:` | Major | Breaking change to a public skill interface or repo workflow |

## Important Context

- Archeia was extracted from a larger TypeScript monorepo — the historical packages are gone
- Lifecycle hooks were evaluated and rejected — native doc loading plus PR-time/CI-time enforcement are sufficient
- Edit canonical Archeia skills in `.claude/skills/` first, then run `bash scripts/sync-skills.sh`
- Read `.archeia/VISION.md` and `.archeia/PRODUCT.md` for full product context
