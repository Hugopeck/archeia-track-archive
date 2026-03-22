# Product Spec

## Summary

Archeia is two skills plus templates, distributed as a Claude Code plugin and as standalone skill files.

- `/archeia:init` (plugin) or `/archeia` (standalone) initializes and maintains repo architecture guidance
- `/archeia:ask` (plugin) or `/archeia-ask` (standalone) answers questions from that guidance

The job is to create and keep useful instruction files current, not to ship a separate analyzer runtime.

## Product Outcome

The output a user should care about is:
- a trustworthy `.archeia/` knowledge base
- an `AGENTS.md` that changes how agents work in the repo
- a `CLAUDE.md` tuned for Claude-style workflows

If those files are still accurate after two weeks of real development, the product is working.

## Installation

### Plugin (primary)

Install from the Claude Code plugin marketplace:

```shell
/plugin install archeia@marketplace
```

This registers `/archeia:init` and `/archeia:ask` as available skills. The plugin bundles the skills and templates together.

### Standalone (alternative)

Place the skill directories in the agent's skill discovery path:

```text
.claude/skills/
├── archeia/
│   ├── SKILL.md
│   └── templates/
└── archeia-ask/
    └── SKILL.md
```

This registers `/archeia` and `/archeia-ask`. The standalone path is for users who prefer manual control or don't use the plugin system.

### Plugin Structure

```text
archeia/                         ← plugin root
├── .claude-plugin/
│   └── plugin.json              ← name="archeia", version, description
├── skills/
│   ├── init/
│   │   ├── SKILL.md             ← /archeia:init
│   │   └── templates/
│   └── ask/
│       └── SKILL.md             ← /archeia:ask
└── hooks/
    └── hooks.json               ← empty, ready for future use
```

## `/archeia:init` Workflow

`/archeia:init` handles both init and update.

### Step 1: Explore the repository

The skill starts with evidence gathering, not with assumptions. It should inspect:
- root docs and config
- package or service boundaries
- deployment and CI files
- test layout
- existing agent guidance such as `AGENTS.md`, `CLAUDE.md`, or stack-specific instructions

The skill should prefer breadth before depth: get a map of the codebase, then inspect the most important files.

### Step 2: Generate Layer 3 docs from templates

The first draft should come from observed evidence plus templates, not from a blank page. Typical Layer 3 docs include:
- `ARCHITECTURE.md`
- `STANDARDS.md`
- `GUIDE.md`
- `DECISIONS.md`
- `CONSTRAINTS.md`
- `ASSUMPTIONS.md`
- `PREFERENCES.md`

The skill writes these directly into `.archeia/`.

### Step 3: Analyze git history

The skill should inspect history for the changes that add explanatory power:
- large dependency shifts
- major directory moves
- architecture migrations
- ownership patterns
- churn hotspots

This step is important because it turns static description into story: not just what exists, but what changed and why that likely matters.

### Step 4: Ask Layer 2 questions only where evidence is insufficient

The skill should not ask broad, generic questions up front.

Good questions resolve ambiguity that the repo cannot answer reliably, such as:
- which tradeoff mattered most in a migration
- whether a temporary constraint is still active
- what audience or business boundary the repo actually serves

Questions should be sparse, specific, and grounded in observed files.

### Step 5: Write `AGENTS.md`

`AGENTS.md` is the behavioral handoff to everyday agent work. It should summarize:
- what the repo is
- where the important boundaries are
- which docs to read first
- how to validate work
- what not to break

The file should be short enough to load often and strong enough to influence behavior.

### Step 6: Write `CLAUDE.md`

`CLAUDE.md` is a Claude-oriented companion file. It can be slightly more specific about workflow expectations, review style, and task sequencing where that helps Claude perform better.

### Step 7: Offer doc migration

If the repo already has architecture docs in other locations, the skill should offer to migrate or absorb them into the new structure.

The migration path should be explicit and reviewable. The skill should preserve human-authored nuance when possible rather than flattening everything into a template.

### Step 8: Offer GitHub Action and PR template setup

The skill should optionally write:
- a GitHub Action recipe for drift detection or scheduled maintenance
- a pull request template that asks reviewers to confirm doc changes when architecture shifts

This is how maintenance becomes part of normal repo operations.

### Step 9: Confirm through pull request, not custom Q&A

The confirmation loop should be a diff that humans can review. Archeia should not invent a separate approval system if the repo already has one.

The right question is not "did the agent say it is done?" The right question is "does this diff look right in the repo's normal workflow?"

## `/archeia:ask`

`/archeia:ask` is the query surface.

It should:
- load `AGENTS.md`, `CLAUDE.md`, and `.archeia/*.md`
- answer architecture and history questions from those docs
- point to evidence paths when claims matter
- say when the docs appear stale or incomplete
- recommend rerunning `/archeia:init` when the knowledge base is not trustworthy enough

It should not silently regenerate docs. Query and maintenance are separate actions.

## Templates

The templates directory exists to make output consistent without making it generic.

Template set:
- `ARCHITECTURE.md`
- `DECISIONS.md`
- `CONSTRAINTS.md`
- `STANDARDS.md`
- `GUIDE.md`
- `AGENTS.md`
- `CLAUDE.md`
- `PREFERENCES.md`
- `ASSUMPTIONS.md`
- `README-colocated.md`

Each template should provide:
- a stable section structure
- placeholder markers for repo-specific content
- hints about what evidence belongs in each section

Templates should not force identical prose across repositories.

## Generated Knowledge Base

The typical generated structure looks like this:

```text
.archeia/
├── ARCHITECTURE.md
├── ASSUMPTIONS.md
├── CONSTRAINTS.md
├── DECISIONS.md
├── GUIDE.md
├── PREFERENCES.md
└── STANDARDS.md

AGENTS.md
CLAUDE.md
```

Repos may choose to add more docs, but these are the core primitives.

## Maintenance Model

Archeia supports three ways to keep docs current.

### 1. Inline maintenance

During normal coding work, the agent notices a relevant architecture change and updates the affected docs in the same change.

Best for:
- solo developers
- small repos
- teams already comfortable with agents editing docs directly

### 2. Drift to PR

The agent detects that the docs are stale and opens or proposes a pull request containing only documentation updates.

Best for:
- teams that want review on architectural wording
- repos where code changes and doc changes often happen at different times

### 3. CI-time checks

A GitHub Action runs `archeia check` on PRs or on a schedule, detects drift, and flags it for review.

Best for:
- repos with many contributors
- teams that want a predictable enforcement mechanism

### Why not lifecycle hooks?

We evaluated Claude Code hooks (PostToolUse, Stop, SessionStart, PostCompact) for automatic maintenance and found them redundant:
- Context injection at session start is already handled by native CLAUDE.md/AGENTS.md loading
- Per-edit drift detection is too noisy — commit/PR-time is the right granularity
- Stop-time enforcement is heavy-handed when CI checks already cover it

## Evidence Standard

Archeia should make evidence-backed claims whenever possible. A useful architecture doc is not just correct-sounding; it is traceable to real files, history, and conventions.

When evidence is weak, the skill should say so and ask a targeted question rather than turning uncertainty into fact.

## What This Product Is Not

This product does not require:
- a compiled scanner binary
- a custom backend
- a hosted database
- a proprietary review flow
- lifecycle hooks for context injection
- language-specific parsing coverage before it can be useful

Those may become relevant later, but they are not the current product definition.

## Success Metric

The primary success metric is simple:

Are the docs still accurate and helpful after two weeks of normal development?

Supporting signals:
- faster first useful action from the agent
- fewer avoidable architecture mistakes
- cleaner coordination across parallel agent sessions
- willingness to commit the generated files to the repo
- frictionless installation via plugin marketplace

## Failure Mode

If the product only creates an impressive first draft and then the docs rot, it has failed.

The product wins only if maintenance becomes natural enough that the guidance stays alive.
