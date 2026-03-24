# Work Items

Generated from `origin/main` `.track/` state plus live open PR metadata. Updated 2026-03-24 03:26 UTC.

6 projects derived from `.track/` state.

---

## Project 1: Governance Foundation

Define the durable governance stack for the repo so that shared definitions, always-on instructions, executable contracts, strategy docs, and operational work surfaces each have a clear owner.

**Brief:** [`.track/projects/1-governance-foundation.md`](.track/projects/1-governance-foundation.md)

| ID | Task | Mode | Priority | Depends | Status |
| --- | --- | --- | --- | --- | --- |
| [1.1](.track/tasks/1.1-define-governance-stack-and-source-of-truth-rules.md) | [[Plan] Define governance stack and source-of-truth follow-through rules](.track/tasks/1.1-define-governance-stack-and-source-of-truth-rules.md) | plan | high | — | todo |
| [1.2](.track/tasks/1.2-define-archeia-protocol-and-document-family-ownership.md) | [[Plan] Define Archeia protocol follow-on and document-family ownership gaps](.track/tasks/1.2-define-archeia-protocol-and-document-family-ownership.md) | plan | high | — | todo |
| [1.3](.track/tasks/1.3-decide-internal-evaluation-lane-boundaries.md) | [[Investigate] Decide internal evaluation lane boundaries](.track/tasks/1.3-decide-internal-evaluation-lane-boundaries.md) | investigate | medium | — | todo |

---

## Project 2: Knowledge Generation Pipeline

Extend Archeia from Layer 3 evidence generation into a fuller knowledge pipeline that includes targeted human confirmation and explicit Layer 1 support when requested.

**Brief:** [`.track/projects/2-knowledge-generation-pipeline.md`](.track/projects/2-knowledge-generation-pipeline.md)

| ID | Task | Mode | Priority | Depends | Status |
| --- | --- | --- | --- | --- | --- |
| [2.1](.track/tasks/2.1-extend-layer-2-and-layer-1-knowledge-generation.md) | [[Plan] Extend Layer 2 and Layer 1 knowledge generation](.track/tasks/2.1-extend-layer-2-and-layer-1-knowledge-generation.md) | plan | high | — | todo |
| [2.2](.track/tasks/2.2-measure-template-determinism-and-tighten-templates.md) | [[Investigate] Measure template determinism and tighten templates](.track/tasks/2.2-measure-template-determinism-and-tighten-templates.md) | investigate | medium | — | todo |

---

## Project 3: Query And Maintenance

Ship the read path and durable maintenance model for Archeia so that generated guidance can be queried, reviewed, and kept current without inventing a new runtime.

**Brief:** [`.track/projects/3-query-and-maintenance.md`](.track/projects/3-query-and-maintenance.md)

| ID | Task | Mode | Priority | Depends | Status |
| --- | --- | --- | --- | --- | --- |
| [3.1](.track/tasks/3.1-ship-archeia-ask-and-maintenance-model.md) | [[Plan] Ship /archeia:ask and maintenance model](.track/tasks/3.1-ship-archeia-ask-and-maintenance-model.md) | plan | high | — | todo |

---

## Project 5: Markdown Validation Architecture

Design a future markdown validation stack that strengthens contracts without creating a second canonical spec surface.

**Brief:** [`.track/projects/5-markdown-validation-architecture.md`](.track/projects/5-markdown-validation-architecture.md)

| ID | Task | Mode | Priority | Depends | Status |
| --- | --- | --- | --- | --- | --- |
| [5.1](.track/tasks/5.1-design-markdown-validation-extraction-path.md) | [[Plan] Design markdown validation extraction path](.track/tasks/5.1-design-markdown-validation-extraction-path.md) | plan | high | — | todo |

---

## Project 0: Archive

Provide a stable project bucket for historical Track tasks that predate the current flat-task, `project_id`-based model.

**Brief:** [`.track/projects/0-archive.md`](.track/projects/0-archive.md)

| ID | Task | Mode | Priority | Depends | Status |
| --- | --- | --- | --- | --- | --- |
| [001](.track/tasks/001-plan-finalize-task-model-v2-schema.md) | [[Plan] Finalize task-model-v2 schema, dependency doctrine, and transition rules](.track/tasks/001-plan-finalize-task-model-v2-schema.md) | plan | high | — | done |
| [003](.track/tasks/003-implement-task-mode-enum-and-schema-support.md) | [[Implement] Add task mode enum and frontmatter schema support](.track/tasks/003-implement-task-mode-enum-and-schema-support.md) | implement | high | 001 | done |
| [004](.track/tasks/004-implement-remove-agent-ready-from-validators.md) | [[Implement] Remove agent_ready from validators and task rewrites](.track/tasks/004-implement-remove-agent-ready-from-validators.md) | implement | high | 003 | done |
| [005](.track/tasks/005-implement-track-new-require-mode.md) | [[Implement] Make track new require mode, emit depends_on, and support direct todo creation](.track/tasks/005-implement-track-new-require-mode.md) | implement | high | 003 | done |
| [007](.track/tasks/007-implement-mode-aware-templates-and-generators.md) | [[Implement] Update task templates, generators, and derived views for required dependencies](.track/tasks/007-implement-mode-aware-templates-and-generators.md) | implement | high | 003 | done |
| [008](.track/tasks/008-implement-ready-gate-validation-rules.md) | [[Implement] Rewrite validator rules around minimum task definition, dependency integrity, and ready gates](.track/tasks/008-implement-ready-gate-validation-rules.md) | implement | high | 001 | done |
| [011](.track/tasks/011-implement-add-derived-availability-to-index-json.md) | [[Implement] Add derived availability to index.json](.track/tasks/011-implement-add-derived-availability-to-index-json.md) | implement | high | 003, 007 | done |
| [013](.track/tasks/013-remove-freshness-validation.md) | [[Implement] Remove freshness validation and gitattributes generation](.track/tasks/013-remove-freshness-validation.md) | implement | high | — | done |
| [014](.track/tasks/014-add-track-gitignore.md) | [[Implement] Add .track/.gitignore for derived files in track init](.track/tasks/014-add-track-gitignore.md) | implement | high | — | done |
| [021](.track/tasks/021-update-tests-ephemeral.md) | [[Implement] Update tests and fixtures for ephemeral model](.track/tasks/021-update-tests-ephemeral.md) | implement | high | 013, 014 | done |
| [028](.track/tasks/028-define-hybrid-launch-readiness-plan-and-exit-criteria.md) | [[Plan] Define hybrid launch-readiness plan and exit criteria](.track/tasks/028-define-hybrid-launch-readiness-plan-and-exit-criteria.md) | plan | high | — | done |
| [036](.track/tasks/036-write-protocol-md.md) | [[Implement] Write PROTOCOL.md as single source of truth for Track protocol](.track/tasks/036-write-protocol-md.md) | implement | high | — | done |
| [002](.track/tasks/002-investigate-todo-to-triage-demotion-ux.md) | [[Investigate] Decide whether todo-to-triage demotion needs explicit CLI UX](.track/tasks/002-investigate-todo-to-triage-demotion-ux.md) | investigate | medium | 001 | done |
| [006](.track/tasks/006-implement-track-list-mode-filters.md) | [[Implement] Replace agent-ready list filters with mode and availability filters](.track/tasks/006-implement-track-list-mode-filters.md) | implement | medium | 003 | done |
| [009](.track/tasks/009-implement-migrate-docs-fixtures-and-snapshots.md) | [[Implement] Migrate docs, fixtures, snapshots, and dogfooded examples to task-model-v2](.track/tasks/009-implement-migrate-docs-fixtures-and-snapshots.md) | implement | medium | 004, 005, 006, 007, 008 | done |
| [010](.track/tasks/010-investigate-task-model-v2-transition-risks.md) | [[Investigate] Identify transition risks in migrating existing repos to task-model-v2](.track/tasks/010-investigate-task-model-v2-transition-risks.md) | investigate | medium | 001 | done |
| [015](.track/tasks/015-update-ci-template.md) | [[Implement] Update CI template for separate validate and build steps](.track/tasks/015-update-ci-template.md) | implement | medium | 013 | done |
| [016](.track/tasks/016-migrate-repo-to-ephemeral.md) | [[Implement] Migrate this repo's .track/ to ephemeral derived files](.track/tasks/016-migrate-repo-to-ephemeral.md) | implement | medium | 013, 014 | done |
| [017](.track/tasks/017-update-track-spec.md) | [[Implement] Update track-spec.md for ephemeral derived files](.track/tasks/017-update-track-spec.md) | implement | medium | — | done |
| [018](.track/tasks/018-update-build-plan.md) | [[Implement] Update track-build-plan.md with Phase 11 progress and ephemeral model](.track/tasks/018-update-build-plan.md) | implement | medium | — | done |
| [019](.track/tasks/019-update-readme.md) | [[Implement] Update README.md status and capabilities](.track/tasks/019-update-readme.md) | implement | medium | — | done |
| [022](.track/tasks/022-investigate-conductor-scripts-fit.md) | [[Investigate] Confirm Conductor scripts fit after ephemeral migration](.track/tasks/022-investigate-conductor-scripts-fit.md) | investigate | medium | 016, 019, 020 | done |
| [023](.track/tasks/023-add-conductor-json-for-track.md) | [[Implement] Add shared Conductor scripts for track](.track/tasks/023-add-conductor-json-for-track.md) | implement | medium | 022 | done |
| [025](.track/tasks/025-investigate-decide-whether-task-model-v2-should.md) | [[Investigate] Decide whether task-model-v2 should bump schema_version](.track/tasks/025-investigate-decide-whether-task-model-v2-should.md) | investigate | medium | — | done |
| [026](.track/tasks/026-plan-simplify-current-versus-archived.md) | [[Plan] Simplify current versus archived documentation hierarchy](.track/tasks/026-plan-simplify-current-versus-archived.md) | plan | medium | — | done |
| [027](.track/tasks/027-implement-replace-archived-dogfooding-guidance.md) | [[Implement] Replace archived dogfooding guidance with current smoke-test docs](.track/tasks/027-implement-replace-archived-dogfooding-guidance.md) | implement | medium | — | done |
| [020](.track/tasks/020-update-docs-quick-reference.md) | [[Implement] Update docs/ quick-reference files](.track/tasks/020-update-docs-quick-reference.md) | implement | low | 017 | done |
| [024](.track/tasks/024-document-conductor-scripts-boundary.md) | [[Implement] Document Conductor scripts versus AGENTS.md guidance](.track/tasks/024-document-conductor-scripts-boundary.md) | implement | low | 022, 023 | done |
| [029](.track/tasks/029-ship-remaining-planning-and-triage-workflow-skills.md) | [[Implement] Ship remaining planning and triage workflow skills](.track/tasks/029-ship-remaining-planning-and-triage-workflow-skills.md) | implement | high | 028 | cancelled |
| [030](.track/tasks/030-publish-launch-ready-quickstart-and-migration-guide.md) | [[Implement] Publish launch-ready quickstart and migration guide](.track/tasks/030-publish-launch-ready-quickstart-and-migration-guide.md) | implement | high | 028 | cancelled |
| [031](.track/tasks/031-add-launch-smoke-checklist-for-hybrid-workflow.md) | [[Implement] Add launch smoke checklist for hybrid workflow](.track/tasks/031-add-launch-smoke-checklist-for-hybrid-workflow.md) | implement | high | 028 | cancelled |
| [032](.track/tasks/032-dry-run-clean-clone-install-and-release-paths.md) | [[Investigate] Dry-run clean-clone install and release paths](.track/tasks/032-dry-run-clean-clone-install-and-release-paths.md) | investigate | high | 028 | cancelled |
| [033](.track/tasks/033-dogfood-hybrid-workflow-in-a-scratch-repo.md) | [[Investigate] Dogfood hybrid workflow in a scratch repo](.track/tasks/033-dogfood-hybrid-workflow-in-a-scratch-repo.md) | investigate | high | 029, 030, 031 | cancelled |
| [034](.track/tasks/034-tighten-ci-and-release-assumptions-for-hybrid-launch.md) | [[Implement] Tighten CI and release assumptions for hybrid launch](.track/tasks/034-tighten-ci-and-release-assumptions-for-hybrid-launch.md) | implement | high | 032 | cancelled |
| [035](.track/tasks/035-run-final-launch-readiness-review-and-go-no-go.md) | [[Plan] Run final launch-readiness review and go/no-go](.track/tasks/035-run-final-launch-readiness-review-and-go-no-go.md) | plan | high | 029, 030, 031, 032, 033, 034 | cancelled |

---

## Project 4: Track Convention Simplification

Finish simplifying Track into a zero-dependency coordination convention driven by `CLAUDE.md`, flat task files, Bash scripts, and provisional PR state.

**Brief:** [`.track/projects/4-track-skill-pack-launch.md`](.track/projects/4-track-skill-pack-launch.md)

| ID | Task | Mode | Priority | Depends | Status |
| --- | --- | --- | --- | --- | --- |
| [4.1](.track/tasks/4.1-rewrite-existing-skills-for-pure-skill-pack.md) | [[Implement] Rewrite 6 existing skills to reference PROTOCOL.md and remove cargo run](.track/tasks/4.1-rewrite-existing-skills-for-pure-skill-pack.md) | implement | high | 036 | cancelled |
| [4.2](.track/tasks/4.2-create-coordination-skills.md) | [[Implement] Create coordination skills: claim, release, available, validate, init](.track/tasks/4.2-create-coordination-skills.md) | implement | high | 036 | cancelled |
| [4.3](.track/tasks/4.3-create-planning-skills.md) | [[Implement] Create planning skills: decompose and plan](.track/tasks/4.3-create-planning-skills.md) | implement | high | 036 | cancelled |
| [4.4](.track/tasks/4.4-write-track-lint-py.md) | [[Implement] Write track-lint.py with full validation parity](.track/tasks/4.4-write-track-lint-py.md) | implement | high | 036 | cancelled |
| [4.5](.track/tasks/4.5-rewrite-agents-md-conductor-json-ci.md) | [[Implement] Rewrite AGENTS.md, conductor.json, and CI for pure skill pack](.track/tasks/4.5-rewrite-agents-md-conductor-json-ci.md) | implement | high | 4.1, 4.2, 4.4 | cancelled |
| [4.6](.track/tasks/4.6-dogfood-pure-skill-pack.md) | [[Investigate] Dogfood pure skill pack with two Conductor agents](.track/tasks/4.6-dogfood-pure-skill-pack.md) | investigate | high | 4.1, 4.2, 4.3, 4.4, 4.5 | cancelled |

## Cross-Project Dependencies

```
0 -> 4
```

## Immediate Starts

- [ ] [[Plan] Define governance stack and source-of-truth follow-through rules](.track/tasks/1.1-define-governance-stack-and-source-of-truth-rules.md) — `1` · `high`
- [ ] [[Plan] Define Archeia protocol follow-on and document-family ownership gaps](.track/tasks/1.2-define-archeia-protocol-and-document-family-ownership.md) — `1` · `high`
- [ ] [[Investigate] Decide internal evaluation lane boundaries](.track/tasks/1.3-decide-internal-evaluation-lane-boundaries.md) — `1` · `medium`
- [ ] [[Plan] Extend Layer 2 and Layer 1 knowledge generation](.track/tasks/2.1-extend-layer-2-and-layer-1-knowledge-generation.md) — `2` · `high`
- [ ] [[Investigate] Measure template determinism and tighten templates](.track/tasks/2.2-measure-template-determinism-and-tighten-templates.md) — `2` · `medium`
- [ ] [[Plan] Ship /archeia:ask and maintenance model](.track/tasks/3.1-ship-archeia-ask-and-maintenance-model.md) — `3` · `high`
- [ ] [[Plan] Design markdown validation extraction path](.track/tasks/5.1-design-markdown-validation-extraction-path.md) — `5` · `high`

## Warnings

- GH_TOKEN not set; falling back to offline mode

