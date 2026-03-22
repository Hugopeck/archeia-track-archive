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

## Existing Code (Historical)

The `packages/` monorepo remains in this repository. It contains scanner, renderer, CLI, analyzer, and experiment code that informed the direction shift.

That code is historical and educational for V0. It is not the product definition.

## Repo Tooling

The repo still uses existing tooling for itself:
- `pnpm` for workspace management
- TypeScript for the historical package code
- vitest and repository automation for legacy validation
- semantic-release and GitHub workflows for repo maintenance

Those tools support the repository. They are not Archeia V0's user-facing architecture.
