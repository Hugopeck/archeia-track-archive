# Claude Code Instructions

## Project Context

This is the Archeia repository — an architecture knowledge framework delivered as Claude Code skills. The entire product surface is markdown files: two skills and their templates.

## Key Files

- `.claude/skills/archeia/SKILL.md` — the main skill that generates architecture docs
- `.claude/skills/archeia-ask/SKILL.md` — the query skill
- `.claude/skills/archeia/templates/` — 10 template files that shape generated output
- `.archeia/` — Archeia's own product documentation (self-referential)
- `TODO.md` — current development priorities

## Workflow

- This repo has no build step, no tests, no CI pipeline
- Changes are documentation and skill markdown changes
- Use conventional commits: `docs(skills):`, `feat(skills):`, `docs(framework):`
- Keep PRs focused — one concern per PR

## Important Context

- Archeia was extracted from a larger TypeScript monorepo — the historical packages are gone
- The plugin conversion (adding `.claude-plugin/plugin.json`) is a near-term TODO
- Lifecycle hooks were evaluated and rejected — native doc loading + CI checks are sufficient
- Read `.archeia/VISION.md` and `.archeia/PRODUCT.md` for full product context
