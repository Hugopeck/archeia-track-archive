# Guide

## Setup

Three install options:

**Claude Code plugin** (recommended for local dev):
```shell
claude --plugin-dir ./archeia-plugin
```

**Claude Code skills** (copy into any project):
```text
.claude/skills/archeia/
.claude/skills/archeia-ask/
```

**Agent Skills** (for Codex CLI, Cursor, etc.):
```text
skills/archeia-init/
skills/archeia-ask/
```

## Using `/archeia` (or `/archeia:init`)

Use `/archeia` (or `/archeia:init` via the plugin) when you want to:
- initialize architecture docs for a repo
- refresh stale docs after meaningful code changes
- migrate existing architecture notes into the Archeia structure
- generate or update `AGENTS.md` and `CLAUDE.md`

Recommended workflow:
1. let the skill map the repo first
2. review generated `.archeia/` docs
3. confirm `AGENTS.md` and `CLAUDE.md`
4. choose whether maintenance should stay inline or move into a PR / GitHub Action flow

## Using `/archeia-ask` (or `/archeia:ask`)

Use `/archeia-ask` (or `/archeia:ask` via the plugin) when you want architecture answers from the existing knowledge base without regenerating it.

Good uses:
- onboarding questions
- "why is this service shaped this way?"
- "where should I make this change?"
- "which constraints matter before I touch this package?"

## Editing the Skills

- Update the `SKILL.md` files when workflow behavior changes.
- Update templates when the generated document shape should change.
- Keep the instructions aligned with the actual repo outputs.

## Working With Templates

Templates live under `.claude/skills/archeia/templates/` (canonical copy).

Use them to:
- create a consistent first draft
- preserve recurring section structure
- make it obvious what evidence is missing

Do not over-template the writing. The template should guide the document, not replace repo-specific thinking.

After editing templates, run `bash scripts/sync-templates.sh` to propagate changes to the plugin and agent-skills distributions.

## Shipping Changes

Skill-only changes do not require a build step.

The normal ship path is:
1. edit skill or template Markdown
2. test against a real repo
3. review the generated docs
4. commit the changes

## Debugging Skill Discovery

If a skill does not appear:
- verify the directory name matches the command name
- verify `SKILL.md` has valid frontmatter
- verify the skill lives in the agent's discovery path
- restart or refresh the agent session if needed
