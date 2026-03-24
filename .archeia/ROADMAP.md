# Roadmap

Operational work items live in `.track/`, with `TODO.md` generated from task files and live PR state. This document covers strategic direction, product shape, and historical mapping only.

## Current Product Shape

Archeia is a skill-based product distributed as a Claude Code plugin:
- `/archeia:init` (plugin) or `/archeia` (standalone)
- `/archeia:ask` (plugin) or `/archeia-ask` (standalone)
- templates used to generate and maintain repo knowledge

The plugin format is the primary distribution path. Standalone skill files are maintained alongside for users who prefer manual control.

## What Happened to the Scanner

We built roughly 3,900 lines of scanner, renderer, CLI, and supporting package code. That work was not wasted. It taught us which outputs matter, what evidence looks like, and where trust comes from.

But it also made something obvious: the agent already has file access, search, shell, and reasoning. A dedicated scanner is not the product. The historical code remains in the repo as learning and reference material.

## What Happened to the Cloud Service

The cloud idea assumed we needed a separate coordination layer. In practice, git and pull requests already provide the critical behaviors we need: sharing, review, history, and confirmation.

The cloud service is removed from the roadmap. If a hosted product ever returns, it must earn its place from a clear gap that git-native workflows cannot cover.

## What Happened to Hooks

We evaluated Claude Code lifecycle hooks (PostToolUse, Stop, SessionStart, PostCompact) for automatic maintenance. All were found redundant with existing primitives:
- Context injection → native CLAUDE.md/AGENTS.md loading already handles this
- Per-edit drift detection → too noisy; commit/PR-time is the right granularity
- Stop-time enforcement → heavy-handed when CI checks cover it
- Post-compaction re-injection → native doc loading handles this

See `docs/designs/plugin-extensibility.md` for the full analysis.

## Strategic Themes

### Distribution

Archeia should remain easy to install in the primary environments we care
about: Claude Code plugins plus generated standalone skill distributions.

### Knowledge Base Generation

The write path should keep getting better at producing evidence-backed guidance,
asking higher-value Layer 2 questions, and preserving human-authored nuance when
existing docs are absorbed.

### Maintenance

Maintenance should stay git-native: inline updates, PR-time confirmation, or
CI-time checks. Hooks, services, or hidden automation do not belong in the core
product unless they solve a problem the current workflow cannot.

## What We Learned

- [x] L-001: deterministic file walking clarified which repo facts are stable enough to document
- [x] L-002: schema work clarified the recurring shape of decisions, constraints, and standards
- [x] L-003: renderer work showed that stable phrasing and predictable structure increase trust
- [x] L-004: CLI experiments proved that explicit entry points help adoption
- [x] L-005: deep test coverage exposed edge cases that matter for repo understanding
- [x] L-006: the agent already has the primitives; the product should be instructions and maintenance
- [x] L-007: the plugin's value is distribution, not hooks; native doc loading handles context injection
- [x] L-008: commit/PR-time enforcement is the right granularity, not per-edit or per-turn

## Near-Term Success Criteria

The product is working if:
- real users install the plugin without friction
- generated docs are good enough to commit
- at least some repos keep the docs current for two weeks
- pull-request-based confirmation feels natural
- token efficiency improves enough that users notice

## After V0 — Unknown

Possible directions without commitment:
- richer maintenance automation
- stack-specific template packs
- better diff summarization and evidence linking
- multi-repo reporting for teams
- gstack integration (architecture-aware /review and /plan-eng-review)

No scanner revival, Rust rewrite, or cloud roadmap belongs in the plan unless user evidence makes it necessary.

## Historical Feature Mapping

These IDs are preserved so older design docs and decisions remain resolvable.
They are historical references, not the active backlog.

| Historical ID | Meaning at the time | Current interpretation |
|---------------|---------------------|------------------------|
| F-001 | Claude Code plugin with `/archeia:init` and `/archeia:ask` | Core distribution direction; plugin remains primary |
| F-002 | Official Anthropic marketplace submission | Deferred distribution follow-on; not an active roadmap commitment |
| F-003 | Standalone skill files alongside plugin | Still part of the supported distribution model |
| F-004 | `/archeia:init` initializes and updates guidance surfaces | Core write-path capability |
| F-005 | `/archeia:ask` answers from generated knowledge base | Query-path capability tracked operationally in `.track/` |
| F-006 | Template set for framework docs and colocated README generation | Template-contract evolution theme |
| F-007 | Doc migration flow that absorbs existing architecture docs | Migration/absorption capability theme |
| F-008 | GitHub Action template for drift detection | Maintenance automation theme tracked operationally in `.track/` |
| F-009 | PR template for confirmation flow | Maintenance workflow theme tracked operationally in `.track/` |
| F-010 | `archeia check` deterministic drift detection | Future deterministic maintenance capability tracked operationally in `.track/` |
