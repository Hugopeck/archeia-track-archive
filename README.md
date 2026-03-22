# Archeia

Architecture knowledge framework for AI coding agents.

Type `/archeia`, and the agent stops making avoidable mistakes about the repo.

## What it does

Archeia generates and maintains architecture guidance that AI agents actually read:

- `.archeia/` — knowledge base (architecture, decisions, constraints, standards)
- `AGENTS.md` — behavioral contract for agent work
- `CLAUDE.md` — Claude-specific workflow guide

The docs stay current through commit-time checks and PR-based review.

## Install

### As a plugin

```shell
/plugin install archeia@marketplace
```

### As standalone skills

Copy `.claude/skills/archeia/` and `.claude/skills/archeia-ask/` into your project's `.claude/skills/` directory.

## Usage

### Generate docs

```
/archeia
```

Explores the repo, generates the knowledge base from templates, and writes `AGENTS.md` + `CLAUDE.md`.

### Ask questions

```
/archeia-ask how does the auth system work?
```

Loads the knowledge base and answers architecture questions with evidence paths.

## How it works

Archeia is two skills plus templates. The agent is the scanner — Archeia provides the instructions, templates, and maintenance workflow that make the agent use its code-reading power well.

The product outcome: docs that stay accurate after two weeks of real development.

## License

MIT
