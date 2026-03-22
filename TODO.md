# TODO

## Next Up

### [ ] Marketplace submission

Submit the Archeia plugin to the official Anthropic marketplace (`claude-plugins-official`). Requires: plugin name, description, version, homepage, public GitHub repo. Submit via claude.ai/settings/plugins/submit or platform.claude.com/plugins/submit.

Deferred pending more real-world testing of the local plugin and standalone skill distributions.

### [ ] gstack integration PR

Open a PR to gstack adding Archeia-awareness to `/plan-eng-review` and `/review`. If `.archeia/` exists, gstack skills become architecture-aware automatically.

## Skills

### [ ] Git history analysis step

Add git history analysis between Layer 3 and Layer 2. The skill reads git log, identifies major dependency shifts, structural changes, architectural inflection points, contributor patterns, module churn. Feeds into Layer 2 questions.

### [ ] Layer 2 Q&A flow

Build the Layer 2 conversation flow informed by git history. Generate DECISIONS.md, PREFERENCES.md, CONSTRAINTS.md, ASSUMPTIONS.md in `.archeia/`. Questions are targeted and context-rich.

### [ ] Layer 1 depth (full business context)

Generate VISION.md, BUSINESS_PLAN.md, ROADMAP.md in `.archeia/` when developer explicitly requests full business context.

### [ ] `/archeia:ask` query skill

Build the query skill. Loads all `.archeia/` docs, answers questions about architecture, decisions, constraints, history. Different context loading strategy from normal coding work.

### [ ] AGENTS.md detection patterns

Add detection patterns to generated AGENTS.md so agents maintain `.archeia/` docs naturally. Developer mentions cost → check CONSTRAINTS.md. Developer makes a choice → append to DECISIONS.md. Developer expresses a preference → check PREFERENCES.md.

## Maintenance

### [ ] `archeia check` drift detection

Deterministic drift detection: compare state snapshot against `.archeia/` docs. Check for missing READMEs, undocumented deps, stale exports, schema validity. CI-ready with `--ci` flag.

### [ ] GitHub Action template

Action recipe for scheduled or on-PR drift detection. Runs `archeia check` and comments on PRs when architecture drift is detected.

### [ ] PR template

Pull request template that asks reviewers to confirm doc changes when architecture shifts.

### [ ] Reproducibility measurement

Measure template determinism by running `/archeia:init` on the same repo 3 times and diffing outputs. Track which sections vary (likely Data Flow, Change Notes) vs which are stable (Prerequisites, Project Structure). Use findings to tighten templates where variance is high.

## Low Priority

### [ ] report.html interactive deliverable

Self-contained HTML with system topology, module cards, evolution timeline. Opens in any browser, no server needed.

### [ ] Internal eval lane cleanup

Decide which internal reports remain canonical. Define comparison workflows between agent-authored outputs and internal baselines. Keep the internal lane as leverage for the product lane, not as a separate product.

## Completed

### [x] LLM-guided Layer 3 init

Build the `/archeia:init` skill's bottom-up init flow. The skill navigates the repo via LLM, reads directory structure, manifests, configs, imports, and generates ARCHITECTURE.md, STANDARDS.md, GUIDE.md directly in `.archeia/`. No human input needed for Layer 3.

**Completed:** v1.1.0 (2026-03-22) — Phase 1 shipped: rewritten SKILL.md with exploration algorithm, inference signal table, self-validation; rewritten ARCHITECTURE.md, STANDARDS.md, GUIDE.md templates with frontmatter, quality rubrics, anti-patterns; sync script for 3-way template distribution.

### [x] Plugin conversion (dual-format)

Convert Archeia to a Claude Code plugin while maintaining standalone skill files.

- Create plugin directory with `.claude-plugin/plugin.json` (name: `archeia`)
- Create `skills/init/SKILL.md` (renamed from archeia, produces `/archeia:init`)
- Create `skills/ask/SKILL.md` (renamed from archeia-ask, produces `/archeia:ask`)
- Copy `templates/` into `skills/init/templates/`
- Verify with `claude --plugin-dir ./archeia-plugin`
- Keep standalone `.claude/skills/archeia/` and `.claude/skills/archeia-ask/` alongside

Design doc: `docs/designs/plugin-extensibility.md`

Historical work that informed the current direction (P0-P2):
- Pivot alignment and repo realignment
- Product-lane foundations (CLI, scanner, state, renderers, golden tests)
- End-to-end local product loop (init, update, context-budget reporting)
- Claude Code and Codex target outputs
- Conductor workflow targeting

See `.archeia/DECISIONS.md` for the full decision history.
