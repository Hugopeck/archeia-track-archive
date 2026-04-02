# Architecture

## Product Definition

Archeia V0 is not a compiled application. The product is:
- two skill definitions
- a templates directory
- the repo conventions those skills generate and maintain

The primary skill surface lives here:

```text
.claude/skills/
├── archeia/
│   ├── SKILL.md
│   └── templates/
└── archeia-ask/
    └── SKILL.md
```

## Core Components

### `/archeia`

Reads the repository, gathers evidence, generates `.archeia/` framework docs, writes `AGENTS.md` and `CLAUDE.md`, and offers follow-on maintenance helpers such as a pull-request confirmation flow or GitHub Action recipe.

### `/archeia-ask`

Loads the generated knowledge base and answers architecture questions from it. Its job is retrieval and interpretation, not regeneration.

### Templates

Templates provide the initial shape for framework docs and colocated docs. They keep output consistent while still allowing the agent to write repo-specific content.

### Generated Outputs

The skills primarily write:
- `.archeia/*.md` for the knowledge base
- `AGENTS.md` for general agent guidance
- `CLAUDE.md` for Claude-oriented instructions

## Data Flow

1. User runs `/archeia`
2. Skill explores the repo using native agent tools
3. Skill gathers evidence from real files, history, and conventions
4. Skill generates or updates Layer 3 docs in `.archeia/`
5. Skill asks only the Layer 2 questions that cannot be inferred reliably
6. Skill writes or refreshes `AGENTS.md` and `CLAUDE.md`
7. Skill optionally offers doc migration, PR-based confirmation, and GitHub Action setup
8. User or team reviews changes through normal git workflows

`/archeia-ask` is the read path: it loads the generated docs and answers questions without re-running init unless the docs appear stale.

## Design Principles

- agent-native over custom runtime
- templates over compiled generation pipelines
- evidence-backed claims over inferred narratives
- PR confirmation over custom approval UI
- maintenance workflow over one-time scan output

## Distribution Channels

Archeia ships in three formats from a single source of truth:

- **Claude Code skills** — `.claude/skills/archeia/` and `.claude/skills/archeia-ask/` (copy into any project)
- **Claude Code plugin** — `plugins/archeia/` (install with `claude --plugin-dir`)
- **Agent Skills** — `skills/archeia-init/` and `skills/archeia-ask/` (for Codex CLI, Cursor, etc.)

Templates are canonical in `.claude/skills/archeia/templates/` and synced to the other distributions via `scripts/sync-skills.sh`.

## Repo Tooling

- semantic-release and GitHub Actions for versioning, tags, and GitHub releases
- Release automation does not push changelog commits to `main`; release notes are mirrored into `CHANGELOG.md` through a separate PR
- No build step, no runtime dependencies — the product is markdown files
