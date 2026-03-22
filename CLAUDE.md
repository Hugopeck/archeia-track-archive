# Claude Code Instructions

## Project Context

This is the Archeia repository — an architecture knowledge framework delivered as Claude Code skills. The entire product surface is markdown files: two skills and their templates.

## Key Files

- `.claude/skills/archeia/SKILL.md` — the main skill that generates architecture docs
- `.claude/skills/archeia-ask/SKILL.md` — the query skill
- `.claude/skills/archeia/templates/` — 10 template files that shape generated output
- `archeia-plugin/` — Claude Code plugin distribution with `/archeia:init` and `/archeia:ask`
- `skills/` — agent-skills distribution for Codex CLI, Cursor, and compatible tools
- `.releaserc.json` — semantic-release configuration for versioning and GitHub releases
- `.github/workflows/release.yml` — release automation on pushes to `main`
- `.archeia/` — Archeia's own product documentation (self-referential)
- `TODO.md` — current development priorities

## Workflow

- This repo has no build step and no runtime test suite
- GitHub Actions runs semantic-release on pushes to `main`
- Changes are documentation and skill markdown changes
- Use conventional commits so release automation can infer versions
- Keep PRs focused — one concern per PR

## Commit Conventions

| Prefix | Bump | When to use |
|--------|------|-------------|
| `feat(skills):` | Minor | New skill capability or new template |
| `fix(skills):` | Patch | Fix in skill logic or template content |
| `feat(framework):` | Minor | New `.archeia/` document type or framework capability |
| `docs:` | None | Routine documentation edits that should not release |
| `feat!:` / `fix!:` | Major | Breaking change to a skill interface or template structure |

## Important Context

- Archeia was extracted from a larger TypeScript monorepo — the historical packages are gone
- Lifecycle hooks were evaluated and rejected — native doc loading + CI checks are sufficient
- Templates are duplicated in `.claude/skills/archeia/templates/`, `archeia-plugin/skills/init/templates/`, and `skills/archeia-init/templates/` — update all three when editing
- Read `.archeia/VISION.md` and `.archeia/PRODUCT.md` for full product context
