# Archeia Plugin

Archeia is an architecture knowledge framework for Claude Code.

This plugin ships two skills:

- `/archeia:init` — explores a repository and generates or refreshes `.archeia/` docs, `AGENTS.md`, and `CLAUDE.md`
- `/archeia:ask` — answers architecture questions from an existing Archeia knowledge base

## What it generates

`/archeia:init` can generate and maintain:

- `.archeia/ARCHITECTURE.md`
- `.archeia/DECISIONS.md`
- `.archeia/CONSTRAINTS.md`
- `.archeia/STANDARDS.md`
- `.archeia/GUIDE.md`
- `.archeia/PREFERENCES.md`
- `.archeia/ASSUMPTIONS.md`
- `AGENTS.md`
- `CLAUDE.md`

## Install locally

From this repository:

```shell
claude --plugin-dir ./archeia-plugin
```

Or point Claude Code at a copied checkout of `archeia-plugin/`.

## Usage

Generate or refresh the knowledge base:

```text
/archeia:init
```

Ask architecture questions:

```text
/archeia:ask what should I read before changing this subsystem?
```

## Notes

- Templates for the init flow live in `skills/init/templates/`
- The repository also publishes standalone skill directories for non-plugin installs
