# Layer 3 Plugin Launch

## Goal

Ship Archeia's Layer 3 knowledge generation as a stable, tested Claude Code plugin. Cut scope to the minimum needed: evidence-generated docs (ARCHITECTURE.md, STANDARDS.md, GUIDE.md) plus the `/archeia:ask` read path. Defer or cancel all work that does not directly serve this release.

## Why Now

The current backlog spans governance, L2/L1 generation, validation architecture, and query/maintenance — too many fronts for a first stable release. Focusing on Layer 3 alone gives a shippable product that delivers immediate value (accurate, evidence-backed architecture docs) without waiting for human-confirmation workflows or strategic-layer generation.

## In Scope

- Audit existing projects (P1–P5) and recommend defer/cancel/keep for each
- Identify gaps in the Layer 3 write path that block a stable release
- Identify gaps in the `/archeia:ask` read path if included in the launch bundle
- Define what "stable release" means for the plugin (test coverage, template quality, known limitations)
- Produce a concrete launch checklist

## Out Of Scope

- Implementing fixes — this project is investigation/planning only
- Layer 2 or Layer 1 generation work
- Non-Claude-Code distribution (standalone skills, other agent platforms)
- New feature development

## Shared Context

- Layer 3 docs are defined in `.archeia/PROTOCOL.md` — evidence-generated, no speculation, cite files precisely
- The plugin lives in `plugins/archeia/` with skills `init` and `ask`
- Distribution sync is handled by `scripts/sync-skills.sh`
- Key decisions: D-029 (skill-only V0), D-034 (plugin conversion), D-035 (instructions over machinery)
- All 6 open tasks (1.1, 1.2, 2.1, 2.2, 3.1, 5.1) need triage against this narrower scope

## Dependency Notes

- This project's findings will determine the fate of tasks in P1, P2, P3, and P5
- No hard dependencies on other work — this is a scoping/planning exercise

## Success Definition

- Clear defer/cancel/keep recommendation for every open task
- Identified list of gaps and blockers for a Layer 3 plugin release
- Launch checklist that can be decomposed into implementation tasks

## Candidate Task Seeds

- 6.1: Audit open projects and tasks — recommend defer/cancel/keep
- 6.2: Gap analysis for Layer 3 write path stability
- 6.3: Gap analysis for `/archeia:ask` read path inclusion
- 6.4: Define launch criteria and produce release checklist
