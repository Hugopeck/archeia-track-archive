# Decisions

<!-- DECISION INDEX (agents: scan this first, load full entries as needed)
| Date       | Domain       | Title                                                          | Status     |
|------------|--------------|----------------------------------------------------------------|------------|
| 2026-03-27 | Product      | D-036: Internal evaluation is not a product lane               | Accepted   |
| 2026-03-23 | Product      | D-035: Instruction architecture before workflow machinery     | Accepted   |
| 2026-03-22 | Distribution | D-034: Plugin conversion (dual-format)                         | Accepted   |
| 2026-03-21 | Product      | D-027: Kill the scanner as V0 product                          | Accepted   |
| 2026-03-21 | Product      | D-028: Kill the cloud service                                  | Accepted   |
| 2026-03-21 | Product      | D-029: Skill-only V0 (two SKILL.md + templates)                | Accepted   |
| 2026-03-21 | Product      | D-030: Enforcement via GitHub Action template                  | Accepted   |
| 2026-03-21 | Product      | D-031: Token efficiency as testable claim                      | Accepted   |
| 2026-03-21 | Product      | D-032: Auto-maintaining AGENTS.md as core value prop           | Accepted   |
| 2026-03-21 | Product      | D-033: Confirmation via PR, not custom Q&A                     | Accepted   |
| 2026-03-21 | Product      | D-018: Two skills: `/archeia` + `/archeia-ask`                 | Accepted   |
| 2026-03-21 | Architecture | D-019: LLM skill as primary init, scanner as validation        | Superseded |
| 2026-03-21 | Product      | D-020: Bottom-up init flow (Layer 3 → git history → Layer 2)  | Accepted   |
| 2026-03-21 | Product      | D-021: MAP.md renamed to ARCHITECTURE.md in generated output   | Accepted   |
| 2026-03-21 | Product      | D-022: Docs auto-populate from conversation                    | Accepted   |
| 2026-03-21 | Architecture | D-023: `.archeia/` for knowledge base, `docs/` for deliverables| Accepted   |
| 2026-03-21 | Product      | D-024: report.html as interactive HTML deliverable             | Accepted   |
| 2026-03-21 | Product      | D-025: Git history analysis as init step                       | Accepted   |
| 2026-03-21 | Product      | D-026: Adaptive depth, not modes                              | Accepted   |
| 2026-03-20 | Product      | D-010: One skill `/archeia`, not multiple commands             | Superseded |
| 2026-03-20 | Product      | D-011: AGENTS.md as index, docs/ as depth                     | Accepted   |
| 2026-03-20 | Product      | D-012: Framework docs live in docs/, not hidden                | Superseded |
| 2026-03-20 | Product      | D-013: Scan-only mode (80% value, no Q&A)                     | Superseded |
| 2026-03-17 | Product      | D-001: Agent-native pivot                                     | Accepted   |
| 2026-03-17 | Architecture | D-002: Skill-first architecture                               | Accepted   |
| 2026-03-17 | Architecture | D-003: Bun for scanner/CLI runtime                            | Superseded |
| 2026-03-17 | Architecture | D-004: No MCP in any phase                                    | Accepted   |
| 2026-03-17 | Architecture | D-005: Single YAML state as source of truth                   | Accepted   |
| 2026-03-17 | Quality      | D-006: Evidence-based claims                                  | Accepted   |
| 2026-03-17 | Product      | D-007: Diagnostic-first output                                | Accepted   |
| 2026-03-17 | Business     | D-008: Model E monetization                                   | Superseded |
| 2026-03-17 | Distribution | D-009: gstack composability                                   | Accepted   |
| 2026-03-17 | Architecture | D-014: Package architecture (scanner/state/renderers/cli + experiments) | Superseded |
| 2026-03-17 | Product      | D-015: Claude and Codex as first agent targets                | Accepted   |
| 2026-03-17 | Product      | D-016: Conductor as Phase 1 host environment                  | Accepted   |
| 2026-03-16 | Research     | D-017: Experiments 2 and 3 deferred                           | Accepted   |
-->

---


## 2026-03-27 — D-036: Internal evaluation is not a product lane

**Domain:** Product
**Status:** Accepted

**Context:** The repo accumulated historical exploration work (scanner, CLI, renderer, cloud experiments — ~3,900 lines) and internal evaluation tasks (template determinism measurement, dogfooding exercises) alongside the shipped Archeia product. Task 1.3 asked whether these form a separate "internal evaluation lane" that needs its own boundary rules, or whether existing structures already handle them.

**Decision:** Internal evaluation work is not a product lane. It is ordinary task work that happens to investigate product quality. No separate directory, document family, or governance layer is needed. The existing structure already provides the right homes:

- **Historical learning** (scanner, CLI, experiments) → already documented as context in `.archeia/ROADMAP.md` "What Happened to..." sections and superseded decisions in `DECISIONS.md`. These are reference material, not a lane.
- **Quality investigation tasks** (template determinism, dogfooding) → ordinary `.track/` tasks with `mode: investigate`. They produce findings that land as decisions, assumption updates, or product changes — not as a parallel output stream.
- **Product validation artifacts** (if any emerge) → belong in `docs/designs/` as design documents, or as evidence in existing `.archeia/` docs. They do not need a separate evaluation directory.

The key boundary rule: **if a piece of evaluation work produces a durable artifact that agents should read, it must land in an existing document family** (`.archeia/`, `AGENTS.md`, `CLAUDE.md`, `docs/designs/`). If it does not produce a durable artifact, it is a task that completes and closes.

**Assumptions relied on:** A-008 (minimal surface area), A-011 (templates + instructions beat custom pipelines)
**Constraints respected:** Product shape (single product lane), Ontology (source-of-truth hierarchy)

**Consequences:**
- No `evaluation/`, `reports/`, or `internal/` directory should be created.
- Future investigation tasks decompose as `.track/` tasks, not as a parallel product concern.
- Findings from evaluation work update existing docs (decisions, assumptions, roadmap) rather than creating a new document family.
- The "What We Learned" section in `ROADMAP.md` remains the right place for historical learning summaries.

**Alternatives considered:**
- Create a dedicated `docs/evaluations/` directory → rejected because it would create a document family without a clear owner or maintenance path, risking the same drift that `.archeia/` was designed to prevent.
- Add an "Evaluation" layer to the Protocol → rejected because evaluation is a task mode, not a document layer. Adding it would blur the Layer 1/2/3 model.

---

## 2026-03-23 — D-035: Instruction architecture before workflow machinery

**Domain:** Product
**Status:** Accepted

**Context:** Comparing Track's generated board with a simpler manual TODO system showed that strong templates, clear ownership, and readable views outperform thin automated exhaust.

**Decision:** Prefer canonical markdown records + strong instructions + opinionated derived views before adding more orchestration or tooling.

**Consequences:**
- Invest first in templates, doc contracts, and projections.
- Treat extra systems as a follow-on only if the simpler approach fails.

---


## 2026-03-22 — D-034: Plugin conversion (dual-format)

**Domain:** Distribution
**Status:** Accepted

**Context:** Archeia currently ships as standalone skill files that users copy into `.claude/skills/`. Claude Code plugin packaging adds one-command install, marketplace discovery, and versioned distribution, but the product still needs to work as plain skills in repositories that prefer direct file copies. Hooks were evaluated already and are not required for V0 because native `AGENTS.md` and `CLAUDE.md` loading plus CI-time checks cover the important behavior.

**Decision:** Add a plugin distribution alongside the existing standalone files. Create `plugins/archeia/` with plugin metadata, rename the packaged skills to `/archeia:init` and `/archeia:ask`, copy the init templates into the plugin skill, and keep `.claude/skills/archeia/` and `.claude/skills/archeia-ask/` unchanged as the standalone format.

**Assumptions relied on:** A-001 (agent-native users), A-009 (agents follow instruction files), A-011 (templates plus instructions beat scanner pipeline for V0)
**Constraints respected:** Distribution (plugin + standalone), Design (no lifecycle hooks), Product shape (skill-first)

**Consequences:**
- Archeia can be installed either as a Claude Code plugin or as copied standalone skills.
- Marketplace submission and plugin-based discovery are now unblocked.
- The plugin format stays minimal because native doc loading handles the key behavior without custom hooks.
- Existing standalone users do not need to migrate or rename their current commands.

**Alternatives considered:**
- Plugin-only distribution — rejected because standalone skill copying is still useful and already works.
- Adding lifecycle hooks now — rejected because native doc loading and CI-time checks are sufficient for V0.
- Leaving distribution as standalone files only — rejected because it blocks plugin install flows and marketplace discovery.

**Cascades to:** TODO.md, docs/designs/plugin-extensibility.md, plugin packaging, marketplace submission


## 2026-03-21 — D-027: Kill the scanner as V0 product

**Domain:** Product
**Status:** Accepted

**Context:** The scanner, state, renderer, and CLI work produced real learning, but the agent already has file access, search, shell, and reasoning. Keeping the scanner as the V0 product would duplicate capabilities the user already has while preserving complexity that the product no longer needs.

**Decision:** The scanner is not the V0 product. Archeia V0 is skill-first and template-first. Historical package code remains in the repo as reference material and proof of learning, but the product the user installs is not a compiled scanner or validation binary.

**Assumptions relied on:** A-002 (native tool use beats pipelines), A-011 (templates plus instructions beat scanner pipeline for V0)
**Constraints respected:** Architectural (product shape), Financial ($0 to build and operate)

**Consequences:**
- The product surface becomes two skills plus templates.
- Historical package code can remain without defining roadmap scope.
- Repo docs must stop describing the scanner as the current product.

**Alternatives considered:**
- Keep the scanner as the shipped V0 product — rejected because it duplicates agent-native capabilities.
- Keep a hybrid product definition — rejected because it preserves complexity without clarifying value.

**Cascades to:** VISION.md, ROADMAP.md, ARCHITECTURE.md, PRODUCT.md, CONSTRAINTS.md, AGENTS.md, README.md

---

## 2026-03-21 — D-028: Kill the cloud service

**Domain:** Product
**Status:** Accepted

**Context:** The cloud plan assumed Archeia needed hosted coordination, storage, and review flows. In practice, git and pull requests already provide version history, sharing, confirmation, and rollback for V0.

**Decision:** Remove the cloud service from the active product plan. Archeia V0 should run entirely in the user's agent session and repository workflow. Any future hosted component must justify itself against what git-native workflows already do well.

**Assumptions relied on:** A-001 (agent-native users), A-003 (small-team early wedge)
**Constraints respected:** Financial ($0 build and operate), Infrastructure (no infrastructure)

**Consequences:**
- No cloud monetization story should shape V0 scope.
- Repo docs must stop presenting hosted infrastructure as inevitable.
- Pull requests become the natural confirmation surface.

**Alternatives considered:**
- Keep cloud on the near-term roadmap — rejected because the need is not yet real.
- Build a minimal sync service anyway — rejected because git already covers the core use case.

**Cascades to:** VISION.md, BUSINESS_PLAN.md, ROADMAP.md, PRODUCT.md, CONSTRAINTS.md, README.md

---

## 2026-03-21 — D-029: Skill-only V0 (two SKILL.md + templates)

**Domain:** Product
**Status:** Accepted

**Context:** Once the scanner and cloud were removed from the V0 definition, the remaining durable product was clear: a write path, a read path, and the templates that keep output consistent.

**Decision:** Archeia V0 is exactly two skills plus templates:
- `/archeia` — generate and maintain the knowledge base plus agent-facing docs
- `/archeia-ask` — answer questions from that knowledge base
- templates — provide stable document shapes for the generated docs

**Assumptions relied on:** A-005 (guidance useful without language-specific tooling), A-008 (minimal commands), A-011 (templates plus instructions beat scanner pipeline for V0)
**Constraints respected:** Design (two skills only), Architectural (product shape)

**Consequences:**
- Installation becomes skill-directory placement, not package installation.
- Product work shifts toward templates, docs, and maintenance flow quality.
- Legacy package code becomes supporting context rather than the center of the roadmap.

**Alternatives considered:**
- Expand to many specialized skills — rejected because the surface becomes harder to learn.
- Collapse back to one skill — rejected because query and maintenance benefit from different loading strategies.

**Cascades to:** ARCHITECTURE.md, PRODUCT.md, GUIDE.md, AGENTS.md, README.md, skill implementation

---

## 2026-03-21 — D-030: Enforcement via GitHub Action template

**Domain:** Product
**Status:** Accepted

**Context:** Repos that want ongoing doc maintenance need an enforcement path, but V0 should not introduce a proprietary service or review system to get it.

**Decision:** Archeia should offer a GitHub Action template and recipe as the default automation path for drift detection and maintenance prompts. Enforcement stays repo-native and optional.

**Assumptions relied on:** A-006 (agent ecosystem discovery), A-009 (agents follow repo instructions reliably enough)
**Constraints respected:** Infrastructure (optional GitHub automation only), Design (confirmation via PR)

**Consequences:**
- Teams can adopt automation without adding Archeia-specific infrastructure.
- The product can remain small while still supporting maintenance.
- GitHub-native workflows become part of the product story.

**Alternatives considered:**
- No enforcement path at all — rejected because some teams need a repeatable maintenance loop.
- Build a custom enforcement service — rejected because it violates the V0 simplicity constraint.

**Cascades to:** ROADMAP.md, PRODUCT.md, GUIDE.md, templates, AGENTS.md

---

## 2026-03-21 — D-031: Token efficiency as testable claim

**Domain:** Product
**Status:** Accepted

**Context:** "Better architecture awareness" is directionally true but too vague to test. Archeia needs a claim that shows up directly in agent behavior.

**Decision:** Treat token efficiency as a primary testable claim. The simplest practical measure is how many exploratory tool calls, file reads, or blind searches happen before the agent takes a first useful action.

**Assumptions relied on:** A-002 (context limits still matter), A-012 (token efficiency is measurable)
**Constraints respected:** Design (testable claim), Financial ($0 validation path)

**Consequences:**
- Product messaging can anchor on observable agent behavior, not just nicer docs.
- The team can evaluate whether `AGENTS.md` and `CLAUDE.md` actually save exploration effort.
- Success criteria shift from output volume toward better first moves.

**Alternatives considered:**
- Message quality without measurement — rejected because it is too easy to hand-wave.
- Treat speed alone as the claim — rejected because fast wrong actions are not a win.

**Cascades to:** BUSINESS_PLAN.md, ROADMAP.md, PRODUCT.md, CONSTRAINTS.md

---

## 2026-03-21 — D-032: Auto-maintaining AGENTS.md as core value prop

**Domain:** Product
**Status:** Accepted

**Context:** The pain users feel is not a lack of one-time architecture output. It is that the instruction files agents actually read drift away from reality.

**Decision:** The primary value proposition is auto-maintaining `AGENTS.md` and `CLAUDE.md`, supported by `.archeia/` framework docs. Archeia wins when those files stay useful enough to shape daily agent behavior.

**Assumptions relied on:** A-009 (agents follow instruction files), A-011 (templates plus instructions beat scanner pipeline for V0)
**Constraints respected:** Design (core outcome), Product shape (skill-first)

**Consequences:**
- Work that improves doc maintenance is more important than work that expands one-time generation breadth.
- `AGENTS.md` and `CLAUDE.md` should be treated as first-class outputs.
- Retention depends on maintenance quality, not initial wow factor alone.

**Alternatives considered:**
- Sell the one-time scan report as the core value — rejected because it does not solve file rot.
- Focus on hidden framework docs only — rejected because agent-facing instructions are the behavioral lever.

**Cascades to:** VISION.md, BUSINESS_PLAN.md, PRODUCT.md, AGENTS.md, README.md, templates

---

## 2026-03-21 — D-033: Confirmation via PR, not custom Q&A

**Domain:** Product
**Status:** Accepted

**Context:** Once the output becomes maintained repo docs, the most trustworthy confirmation path is the repo's existing review process. A separate confirmation UI would duplicate a behavior teams already have.

**Decision:** Confirm Archeia updates through diffs and pull requests. The skill may ask targeted questions to fill knowledge gaps, but final confirmation should happen in the repo's normal review workflow.

**Assumptions relied on:** A-001 (agent-native users), A-009 (repo instructions can shape behavior)
**Constraints respected:** Infrastructure (git-native coordination), Design (confirmation via PR)

**Consequences:**
- Archeia fits the workflow users already trust.
- Reviewable diffs become the ground truth for whether the docs are right.
- The product does not need a custom approval subsystem.

**Alternatives considered:**
- Custom confirmation wizard — rejected because it competes with pull requests.
- No confirmation story — rejected because maintenance needs a trustworthy review surface.

**Cascades to:** PRODUCT.md, GUIDE.md, AGENTS.md, README.md, templates

---


## 2026-03-21 — D-018: Two skills: `/archeia` + `/archeia-ask`

**Domain:** Product
**Status:** Accepted

**Context:** D-010 established one skill. But querying the knowledge base is a distinct use case from init/update — it needs a different context loading strategy than normal coding work. Two skills is the right minimum.

**Decision:** Two skills only:
- `/archeia` — explores the repo, generates or updates the knowledge base, asks targeted questions only when evidence is insufficient, and refreshes `AGENTS.md` plus `CLAUDE.md`.
- `/archeia-ask` — queries the knowledge base, loads the relevant `.archeia/` docs, and answers questions about the project's architecture, decisions, constraints, and history.

Everything else — recording decisions, checking constraints, updating docs when code changes, flagging stale content — is agent behavior driven by AGENTS.md instructions during normal conversation.

**Assumptions relied on:** A-008 (minimal commands — two is the new minimum), A-009 (agents follow AGENTS.md instructions for everything else)
**Constraints respected:** Design (skill-first architecture)

**Consequences:**
- `/archeia-ask` provides a dedicated query UX without the overhead of re-scanning.
- AGENTS.md behavior instructions still handle day-to-day doc maintenance.
- Two skills is easy to learn; everything else is natural conversation.

**Alternatives considered:**
- One skill only (D-010) — superseded because query needs a different context loading strategy.
- Multiple skills (6+) — rejected because AGENTS.md-driven behavior handles everything else.

**Cascades to:** AGENTS.md, CONSTRAINTS.md (design section), skill implementation, PRODUCT.md

---

## 2026-03-21 — D-019: LLM skill as primary init, scanner as validation

**Domain:** Architecture
**Status:** Superseded by D-027 and D-029

**Context:** The binary scanner was built for a scenario where someone downloads a CLI tool and runs it without an agent session. But the actual user is already in an agent session with an LLM. The skill can navigate the repo more intelligently than the binary's heuristics. The scanner's strength is determinism, not intelligence.

**Decision:** The LLM-guided `/archeia` skill is the primary init and update mechanism. The skill navigates the repo, reads files, reasons about what it finds, asks clarifying questions, and generates the knowledge base docs directly.

The binary scanner shifts to validation infrastructure:
- historical validation work used deterministic snapshots to compare repo understanding against generated docs.
- The old design reserved deterministic indexing work for possible future infrastructure.
- CI pipelines use the scanner because they need deterministic, LLM-free checks.

The docs are generated by the skill directly. Any deterministic validation path is secondary to the generated Markdown knowledge base.

**Assumptions relied on:** A-002 (context windows — skill works within agent's window), A-009 (agents follow instructions)
**Constraints respected:** Architectural (scanner stays deterministic, no network)

**Consequences:**
- The old renderer pipeline becomes historical implementation detail rather than the primary generation path.
- The skill writes `.archeia/` docs directly during init/update.
- The historical scanner package can stay in the repo without defining the product.

**Alternatives considered:**
- Scanner-only generation (current approach) — superseded because LLM-guided analysis produces richer output.
- LLM-only generation was considered too risky in the earlier design because deterministic validation still felt necessary.

**Cascades to:** PRODUCT.md, ARCHITECTURE.md, ROADMAP.md, README.md, CONSTRAINTS.md

---

## 2026-03-21 — D-020: Bottom-up init flow (Layer 3 → git history → Layer 2)

**Domain:** Product
**Status:** Accepted

**Context:** The previous init tried to generate all docs simultaneously from a structured intermediate model. The better approach: start with the concrete observable layer (what's in the repo), analyze how it evolved (git history), then ask targeted questions informed by both.

**Decision:** The `/archeia` init flow follows this sequence:

1. ARCHITECTURE.md (Layer 3) — skill navigates repo: directory structure, package.json, imports, configs, CI. Builds topology with mermaid diagrams.
2. STANDARDS.md (Layer 3) — skill reads linter config, tsconfig, code patterns. Infers conventions.
3. GUIDE.md (Layer 3) — skill reads package.json scripts, CI config, deploy config. Generates procedures.
4. Git history analysis — skill reads git log. Identifies major changes, pattern shifts, architectural inflection points. Feeds into Layer 2 conversation.
5. docs/report.html — interactive HTML report from Layer 3 + git history.
6. DECISIONS.md (Layer 2) — informed by git history. "PostgreSQL replaced SQLite on Jan 15 — performance or scaling?"
7. PREFERENCES.md (Layer 2) — "I noticed consistent early returns. Conscious preference?"
8. CONSTRAINTS.md, ASSUMPTIONS.md (Layer 2) — budget, team size, compliance. 2-5 questions.
9. VISION.md, BUSINESS_PLAN.md, ROADMAP.md (Layer 1) — only if `--depth full`.

**Assumptions relied on:** A-002 (context windows), A-009 (agents follow instructions)
**Constraints respected:** Design (diagnostic-first — Layer 3 findings before questions)

**Consequences:**
- Layer 2 questions are dramatically better when informed by git history.
- Layer 3 completes without human input — the user sees results before being asked anything.
- Init is a conversation, not a one-shot command.

**Alternatives considered:**
- Simultaneous generation from an intermediate model — superseded because bottom-up produces better questions.
- Top-down (vision first) — rejected because it requires the user to articulate abstract goals before seeing concrete state.

**Cascades to:** PRODUCT.md (init flow), ROADMAP.md (build sequence), TODO.md

---

## 2026-03-21 — D-021: MAP.md renamed to ARCHITECTURE.md in generated output

**Domain:** Product
**Status:** Accepted

**Context:** "MAP.md" was a framework-internal name. "ARCHITECTURE.md" is an emerging standard that developers expect to find.

**Decision:** Rename MAP.md to ARCHITECTURE.md everywhere. ARCHITECTURE.md becomes the single "understand this project" document: system overview, module boundaries, dependency graph, data flow, key infrastructure. With mermaid diagrams. ARCHITECTURE.md is the entry point of the `/archeia` init — the first doc generated.

**Assumptions relied on:** A-001 (developer users expect standard filenames)
**Constraints respected:** None directly — naming convention change

**Consequences:**
- The repo's own MAP.md is renamed to ARCHITECTURE.md for consistency.
- All renderers that produce MAP.md must be updated.
- Cross-references throughout all docs must be updated.

**Alternatives considered:**
- Keep MAP.md — rejected because ARCHITECTURE.md is more widely recognized.
- TOPOLOGY.md — rejected because "architecture" covers more than topology.

**Cascades to:** Renderers, PRODUCT.md, AGENTS.md, all cross-references

---

## 2026-03-21 — D-022: Docs auto-populate from conversation

**Domain:** Product
**Status:** Accepted

**Context:** The previous design generated all framework docs upfront during init, even if some were nearly empty. This creates files that feel like bureaucratic overhead.

**Decision:** Framework docs are optional and emerge from conversation. The set of possible doc types is defined (with schemas and detection patterns). The actual docs in any repo are whatever the conversation has produced.

During init, the bottom-up flow generates Layer 3 docs from the scan. Layer 2 docs are generated during Q&A if the conversation produces content. Layer 1 docs only appear if `--depth full`.

After init, AGENTS.md includes detection patterns. If the developer mentions a budget and .archeia/CONSTRAINTS.md doesn't exist, the agent creates it.

Detection patterns:
- Developer mentions cost, budget, spend → check/create CONSTRAINTS.md
- Developer states a belief or assumption → check/create ASSUMPTIONS.md
- Developer makes a technical or business choice → append to DECISIONS.md
- Developer expresses a preference → check/create PREFERENCES.md

**Assumptions relied on:** A-009 (agents follow AGENTS.md detection patterns)
**Constraints respected:** Design (diagnostic-first — don't create empty docs)

**Consequences:**
- Repos only have docs that contain real content.
- AGENTS.md detection patterns must be well-designed to avoid false positives.
- Some docs may never be created if topics never arise in conversation.

**Alternatives considered:**
- Generate all docs upfront — rejected because empty docs feel like overhead.
- No detection patterns (manual creation only) — rejected because agents can handle this naturally.

**Cascades to:** PRODUCT.md, AGENTS.md (detection patterns), ROADMAP.md

---

## 2026-03-21 — D-023: `.archeia/` for knowledge base, `docs/` for deliverables

**Domain:** Architecture
**Status:** Accepted

**Context:** Tension between hiding framework docs (they're Archeia-managed) and showing them (they're useful to browse). The resolution: `.archeia/` is Archeia's managed state. `docs/` is for polished deliverables rendered from that state.

**Decision:**

`.archeia/` — Knowledge base (source, agent-consumed, Archeia-managed). Flat directory. All framework docs live here. Agents access them via pointers in AGENTS.md. Committed to git.

```
.archeia/
├── ARCHITECTURE.md
├── STANDARDS.md
├── GUIDE.md
├── DECISIONS.md
├── PREFERENCES.md
├── CONSTRAINTS.md      (if populated)
├── ASSUMPTIONS.md       (if populated)
├── VISION.md            (if populated)
├── BUSINESS_PLAN.md     (if populated)
└── ROADMAP.md           (if populated)
```

`docs/` — Deliverables (rendered, human-consumed, shareable). Polished outputs rendered from the knowledge base.

```
docs/
├── report.html          ← Interactive architecture report
├── adr.md               ← Formatted decision log
└── ...                  ← Developer's own docs
```

Root-level: AGENTS.md + CLAUDE.md (Archeia-generated), README.md (human-owned).

Archeia-generated files in `docs/` include a header: `<!-- Generated by Archeia. Do not edit. Regenerate with /archeia -->`

**Assumptions relied on:** A-009 (agents find docs via AGENTS.md pointers)
**Constraints respected:** Architectural (clear separation of concerns)

**Consequences:**
- `.archeia/` is the IR (intermediate representation). `docs/` files are compiled output.
- Supersedes D-012 which placed all framework docs in visible `docs/`.
- Agents navigate by filename from AGENTS.md pointers.

**Alternatives considered:**
- Everything in docs/ (D-012) — superseded because it conflates source and rendered output.
- Everything hidden in .archeia/ with no docs/ — rejected because deliverables should be browsable.

**Cascades to:** PRODUCT.md, renderers (output paths), AGENTS.md (pointers), README.md

---

## 2026-03-21 — D-024: report.html as interactive HTML deliverable

**Domain:** Product
**Status:** Accepted

**Context:** ARCHITECTURE.md with mermaid codeblocks is useful for agents but not visually compelling for humans. A standalone HTML file with interactive diagrams is the "wow" moment.

**Decision:** The primary human-facing output is `docs/report.html` — a self-contained HTML file with embedded CSS/JS, mermaid rendering, and all data inlined. No server, no dependencies, opens in any browser.

Contents: system topology with interactive dependency graph, module cards with metrics, architecture patterns with evidence, data flow diagrams, git history evolution timeline, standards summary, findings and recommendations.

The renderer reads the generated Layer 3 docs plus git history data and produces one `docs/report.html`.

**Assumptions relied on:** A-001 (developers appreciate visual output), A-002 (context windows — HTML isn't loaded by agents)
**Constraints respected:** Financial ($0 — self-contained, no server)

**Consequences:**
- report.html is the shareable artifact — the thing developers screenshot and share.
- Replaces REPORT.md as the primary human-facing output.
- Requires an HTML renderer (new build work).

**Alternatives considered:**
- REPORT.md only — rejected because Markdown can't render interactive diagrams.
- Hosted dashboard — rejected because it requires infrastructure (Phase 1 is $0).

**Cascades to:** PRODUCT.md, renderers (new HTML renderer), ROADMAP.md, TODO.md

---

## 2026-03-21 — D-025: Git history analysis as init step

**Domain:** Product
**Status:** Accepted

**Context:** Layer 2 questions are much better when informed by how the codebase evolved. Git history reveals when decisions were made, what was replaced, and how patterns shifted.

**Decision:** Between Layer 3 generation and Layer 2 questioning, the `/archeia` skill analyzes git history:

- Major dependency additions/removals (first/last commit with each dep)
- Structural changes (new directories, file reorganizations)
- Pattern shifts (class → functional, REST → tRPC)
- Architectural inflection points (monolith split, CI introduction)
- Contributor patterns (who owns what areas)
- Module churn (which areas are stable vs. volatile)

This data enriches the knowledge base and feeds into better Layer 2 questions plus the report.html evolution timeline.

**Assumptions relied on:** A-002 (context windows — git log is compact enough to process)
**Constraints respected:** Architectural (scanner can pre-compute git history deterministically for CI)

**Consequences:**
- Init becomes a richer conversation with project-specific context.
- Git history extraction can be done by the scanner deterministically for the CI path.
- The skill uses extraction + LLM reasoning for the init conversation.

**Alternatives considered:**
- No history analysis (current state only) — rejected because it produces cold, uninformed questions.
- Full git blame analysis — rejected because it's too expensive for context windows.

**Cascades to:** PRODUCT.md (init flow), historical scanner package, TODO.md

---

## 2026-03-21 — D-026: Adaptive depth, not modes

**Domain:** Product
**Status:** Accepted

**Context:** The idea of Solo/Team/Corporate modes or scan-only vs. full modes was proposed. The reframe: the actual variable isn't company size or mode — it's what context the repo owns.

**Decision:** No modes. Archeia adapts to what context the repo owns. The conversation depth determines which docs get populated. Enforcement follows from what exists, not from a configuration flag.

Optional conversation hints: `--depth full` (ask everything, repo is the company brain), `--depth technical` (skip business context), `--depth minimal` (architecture and compliance only). These are Q&A presets, not enforcement configurations.

`archeia check` enforces what exists. If BUSINESS_PLAN.md was never generated, it's not enforced. If CONSTRAINTS.md has a financial section, it's validated.

**Assumptions relied on:** A-009 (agents adapt to what exists in `.archeia/`)
**Constraints respected:** Design (adaptive, not prescriptive)

**Consequences:**
- No configuration complexity — depth emerges from conversation.
- Supersedes D-013 (scan-only mode) — there's no separate "scan-only" flag; `--depth minimal` covers the same ground.
- Users don't need to understand modes or choose upfront.

**Alternatives considered:**
- Scan-only mode (D-013) — superseded because adaptive depth is more flexible.
- Solo/Team/Corporate modes — rejected because the variable is repo context, not company size.

**Cascades to:** PRODUCT.md (design decisions), CLI flags, CONSTRAINTS.md

---

## 2026-03-20 — D-010: One skill `/archeia`, not multiple commands

**Domain:** Product
**Status:** Superseded by D-018

**Context:** The developer is already talking to an agent. Asking them to learn 6 slash commands (/archeia-diagnose, /archeia-decide, /archeia-review, etc.) is friction. The agent can determine what to do based on whether repo guidance already exists, and AGENTS.md instructions handle the rest.

**Decision:** One skill that handles init (no knowledge base yet) and update (knowledge base already exists). Everything else is AGENTS.md-driven behavior. The agent decides whether to record a decision, update assumptions, or check constraints based on conversational context, not explicit invocation.

**Assumptions relied on:** A-008 (one command better than many), A-009 (agents follow AGENTS.md instructions)
**Constraints respected:** Design (skill-first architecture)

**Consequences:**
- AGENTS.md instructions must be comprehensive enough to guide agent behavior without explicit commands.
- The single skill must detect repo state and branch accordingly (init vs. update).
- Users who want explicit control lose granularity — they must trust the agent.

**Alternatives considered:**
- Multiple skills (/archeia-diagnose, /archeia-decide, /archeia-review) — rejected because AGENTS.md-driven behavior is lower friction and more natural in conversation.
- Zero skills (pure AGENTS.md, no slash command at all) — rejected because the scanner binary needs explicit invocation and init is a distinct operation.

**Cascades to:** AGENTS.md (instructions must be comprehensive), GUIDE.md, skill implementation

---

## 2026-03-20 — D-011: AGENTS.md as index, docs/ as depth

**Domain:** Product
**Status:** Accepted

**Context:** A 50-entry decision history doesn't fit in a 300-line AGENTS.md. But agents need some context on every session start. Loading all docs upfront wastes context budget. The solution is progressive disclosure: a compact summary that points to depth.

**Decision:** AGENTS.md is a compact summary (~300 tokens) pointing to docs/ files for depth. Agents read AGENTS.md first, then load specific docs/ files as needed based on the task at hand.

**Assumptions relied on:** A-002 (context windows are the binding constraint)
**Constraints respected:** Design (AGENTS.md is the index, docs/ is the depth)

**Consequences:**
- AGENTS.md must be kept small and high-signal — every line earns its place.
- Renderers must keep the index (AGENTS.md) and detail files aligned from the same source material.
- Agents that don't support multi-file reads get less value.

**Alternatives considered:**
- Mega-AGENTS.md with everything inline — rejected because it bloats context on every session.
- Docs-only with no AGENTS.md — rejected because agents don't proactively read docs/ without a pointer.
- Separate config file pointing to docs — rejected because AGENTS.md is already the convention agents look for.

**Cascades to:** AGENTS.md format, renderers (must produce index + detail), docs/ directory structure

---

## 2026-03-20 — D-012: Framework docs live in docs/, not hidden

**Domain:** Product
**Status:** Superseded by D-023

**Context:** Some tools hide their state in dotfiles (.archeia/docs/). But Archeia's framework docs (ASSUMPTIONS.md, DECISIONS.md, etc.) are meant to be read by humans and agents alike. They should be visible, version-controlled, and reviewable in PRs.

**Decision:** Framework documentation files live in `docs/`, not in `.archeia/` or other hidden directories. This was later superseded when `.archeia/` became the knowledge-base location.

**Assumptions relied on:** A-009 (agents follow AGENTS.md instructions — they need to find the docs)
**Constraints respected:** Architectural (compiler pattern — state in .archeia/, renders in docs/)

**Consequences:**
- Docs are visible in GitHub file browser and PR diffs.
- Teams can review documentation changes alongside code changes.
- The docs/ directory may grow large for repos with extensive decision histories.

**Alternatives considered:**
- `.archeia/docs/` hidden directory — rejected because it reduces visibility and makes PR review harder.
- Root-level files (DECISIONS.md at repo root) — rejected because it clutters the root; docs/ is the conventional location.

**Cascades to:** Renderer output paths, AGENTS.md pointer paths, .gitignore patterns

---

## 2026-03-20 — D-013: Scan-only mode (80% value, no Q&A)

**Domain:** Product
**Status:** Superseded by D-026

**Context:** The conversation layer (Q&A to refine scanner output) adds complexity and delays shipping. Scanner-only output — stack detection, patterns, conventions, module structure, dependencies — already provides substantial value. Waiting for Q&A means waiting longer to validate with real users.

**Decision:** Ship scan-only mode first via `archeia init --scan-only`. Scanner output would populate the generated docs without any conversation. Q&A would be additive, not required.

**Assumptions relied on:** A-007 (scanner-only is 80% valuable), A-002 (context windows binding — scanner optimizes for this)
**Constraints respected:** Design (scan-only mode exists), Operational (ship incrementally)

**Consequences:**
- An earlier release could ship without the conversation layer.
- Scanner accuracy matters more — there's no Q&A to correct mistakes.
- Users may perceive output as incomplete without understanding the 80% framing.

**Alternatives considered:**
- Ship scanner + Q&A together — rejected because it delays validation and adds scope.
- Ship Q&A only (no scanner) — rejected because Q&A without scanner context is just a chatbot.

**Cascades to:** historical roadmap scope, CLI implementation, validation plan

---

## 2026-03-17 — D-001: Agent-native pivot

**Domain:** Product
**Status:** Accepted

**Context:** The previous plan was a hosted analyzer MVP that would process repos server-side. Strategic reframe: users already sit inside powerful agents (Claude Code, Cursor, Codex). Archeia doesn't need to resell model inference — it needs to make the agent smarter about the repo it's already working in.

**Decision:** Full pivot to agent-native architecture tooling. The skill is the surface, and the repo guidance is the contract that shapes agent behavior. No hosted inference is needed for the core product.

**Assumptions relied on:** A-001 (developer users who already use agents), A-002 (context windows are the binding constraint)
**Constraints respected:** Financial ($0 infrastructure in Phase 1), Architectural (no hosted services)

**Consequences:**
- Phase 1 has zero infrastructure cost — the product runs entirely in the user's environment.
- Revenue model shifts to cloud analysis (Phase 2) rather than hosted inference.
- The product is only as good as the agent it runs inside — quality depends on Claude/Cursor/Codex capabilities.

**Alternatives considered:**
- Hosted analyzer MVP — rejected because it carried unnecessary infrastructure weight and competed with the agent the user already has.
- VS Code extension — rejected because it ties distribution to one editor and misses the agent-native trend.

**Cascades to:** CONSTRAINTS.md, ARCHITECTURE.md, ROADMAP.md, PREFERENCES.md, all architecture decisions

---

## 2026-03-17 — D-002: Skill-first architecture

**Domain:** Architecture
**Status:** Accepted

**Context:** The agent-native pivot requires a surface area that works inside existing agents. Skills (slash commands) are the native interaction model for Claude Code and similar tools. A skill can invoke the scanner binary, read state, and guide agent behavior — all without MCP or custom protocols.

**Decision:** Skills are the primary integration surface. One `/archeia` skill handles all user-facing interaction. The skill follows AGENTS.md instructions for ongoing behavior and may use supporting tooling where helpful.

**Assumptions relied on:** A-008 (one command better than many), A-001 (developers using agents)
**Constraints respected:** Architectural (no MCP), Design (skill-first)

**Consequences:**
- Integration with new agents requires only a skill definition, not a protocol adapter.
- The skill layer is thin — most logic lives in the scanner and renderers.
- Agents without skill support (e.g., basic Copilot) can still benefit from AGENTS.md alone.

**Alternatives considered:**
- MCP server — rejected because MCP adds protocol complexity and isn't universally supported.
- CLI-only (no skill wrapper) — rejected because it requires users to leave the agent conversation to run commands.

**Cascades to:** Skill implementation, AGENTS.md design, CLI interface

---

## 2026-03-17 — D-003: Bun for scanner/CLI runtime

**Domain:** Architecture
**Status:** Superseded by D-029

**Context:** The scanner and CLI need fast startup time — users invoke `/archeia` in conversation and expect near-instant results. Node.js startup is adequate but Bun offers noticeably faster cold starts and native TypeScript execution without a build step.

**Decision:** Use Bun as the runtime for the earlier compiled product tooling. Node.js 20 LTS remains the runtime for repo tooling (tests, builds, CI).

**Assumptions relied on:** A-001 (developer users expect fast tools)
**Constraints respected:** Architectural (runtime specification)

**Consequences:**
- Scanner startup is fast enough for interactive use inside agent conversations.
- Two runtimes in the monorepo (Bun for product, Node for tooling) adds some complexity.
- Bun compatibility issues may arise with some npm packages.

**Alternatives considered:**
- Node.js for everything — rejected because startup latency matters for conversational UX.
- Deno — rejected because Bun has better npm compatibility and faster adoption in the target audience.

**Cascades to:** Package.json scripts, CI configuration, developer setup instructions

---

## 2026-03-17 — D-004: No MCP in any phase

**Domain:** Architecture
**Status:** Accepted

**Context:** MCP (Model Context Protocol) is emerging as a standard for agent-tool communication. However, it adds protocol complexity, requires a running server, and isn't universally supported across target agents. Skills + CLI + shell commands achieve the same goals with less overhead.

**Decision:** No MCP in any phase. All agent integration happens through skills, shell commands, and other simple agent-native interfaces. This is a deliberate simplification.

**Assumptions relied on:** A-001 (developer users comfortable with CLI)
**Constraints respected:** Architectural (no MCP — explicit constraint)

**Consequences:**
- Simpler architecture — no protocol server to maintain.
- May miss agents that only support MCP and not skills.
- If MCP becomes the dominant standard, this decision will need revisiting.

**Alternatives considered:**
- MCP server alongside skills — rejected because maintaining two integration surfaces doubles the work for a solo developer.
- MCP only — rejected because it isn't universally supported and adds infrastructure.

**Cascades to:** CONSTRAINTS.md, integration architecture, agent support matrix

---

## 2026-03-17 — D-005: Single YAML state as source of truth

**Domain:** Architecture
**Status:** Superseded by D-029

**Context:** The earlier compiler-pattern design wanted one structured intermediate representation from which all output could be rendered deterministically. That was a coherent architecture for the old scanner-first product.

**Decision:** At the time, a single structured repo state was chosen as the intermediate representation for generated output. V0 no longer requires that model because the skills now write the Markdown knowledge base directly.

**Assumptions relied on:** A-002 (context windows binding), A-005 (scope discipline keeps structure manageable)
**Constraints respected:** Architectural (single YAML state, compiler pattern)

**Consequences:**
- All renders are deterministic and reproducible.
- Structured diffs felt meaningful in PRs — reviewers could see exactly what changed.
- Large repos may produce intermediate artifacts that become unwieldy.

**Alternatives considered:**
- Multiple state files per concern (decisions.yaml, assumptions.yaml) — rejected because it complicates the compiler and splits atomic state.
- SQLite database — rejected because it's not git-diffable and adds a binary dependency.
- JSON — rejected because YAML is more human-readable for the expected content.

**Cascades to:** historical schema design, renderer implementation, scanner output format, CONSTRAINTS.md

---

## 2026-03-17 — D-006: Evidence-based claims

**Domain:** Quality
**Status:** Accepted

**Context:** Architecture documentation tools that hallucinate are worse than no documentation. If the scanner claims "this repo uses the repository pattern," it must point to a specific file and line range that demonstrates it. Trust requires evidence.

**Decision:** Every architectural claim in scanner output must link to specific file evidence (path + line range). Claims without evidence are downgraded to "inferred" status. The renderer shows evidence paths alongside claims.

**Assumptions relied on:** A-002 (context windows — evidence paths help agents verify without loading full files)
**Constraints respected:** Design (evidence-based claims only), Compliance (evidence integrity)

**Consequences:**
- Scanner must track evidence provenance for every finding.
- Output is verifiable — users and agents can check claims against actual code.
- Scanner complexity increases — every detection must record its evidence.

**Alternatives considered:**
- Confidence scores without evidence — rejected because scores without evidence are unverifiable.
- LLM-generated explanations — rejected because they can hallucinate evidence paths.

**Cascades to:** historical scanner implementation, evidence tracking, renderer output format

---

## 2026-03-17 — D-007: Diagnostic-first output

**Domain:** Product
**Status:** Accepted

**Context:** Users evaluating Archeia need to see value immediately. Showing "here's what we found in your repo" (diagnostics/findings) is more compelling than "here are rules to follow." Findings demonstrate competence; rules demonstrate value only after the user trusts the tool.

**Decision:** Scanner output leads with findings (what was detected, what patterns exist, what might be wrong) before presenting rules and conventions. Diagnostics are the acquisition hook; rules are the retention mechanism.

**Assumptions relied on:** A-007 (scanner-only is 80% valuable — findings are the 80%)
**Constraints respected:** Design (diagnostic-first output)

**Consequences:**
- First-run experience emphasizes discovery and insight.
- Users may not immediately understand the rules/conventions value.
- Marketing and docs should emphasize "see what Archeia finds" over "set up your rules."

**Alternatives considered:**
- Rules-first (like .cursorrules) — rejected because it requires user effort before showing value.
- Equal weight — rejected because it dilutes the first-impression impact.

**Cascades to:** Renderer output ordering, AGENTS.md structure, marketing copy

---

## 2026-03-17 — D-008: Model E monetization

**Domain:** Business
**Status:** Superseded by D-028

**Context:** The product needed a sustainable business model that aligned with the earlier agent-native pivot. The original idea was a free local layer plus a paid hosted layer.

**Decision:** Model E proposed a free local layer paired with paid hosted analysis. That pricing and packaging model is retained here only as historical record; it is no longer the active plan.

**Assumptions relied on:** A-004 (5% conversion achievable), A-010 (cloud is categorically better)
**Constraints respected:** Financial (positive unit economics from launch)

**Consequences:**
- Free product has real value — drives adoption without revenue pressure.
- Cloud service must be demonstrably better to justify $9.99/mo.
- Phase 2 requires infrastructure investment that Phase 1 avoids.

**Alternatives considered:**
- Fully free / donation-based — rejected because it doesn't build a sustainable business.
- Feature-gated free tier (limited repos) — rejected because artificial limits feel hostile to developers.
- Per-repo pricing — rejected because it penalizes the multi-repo users who are the primary market.

**Cascades to:** BUSINESS_PLAN, CONSTRAINTS (financial), pricing page, Phase 2 architecture

---

## 2026-03-17 — D-009: gstack composability

**Domain:** Distribution
**Status:** Accepted

**Context:** gstack is already vendored in repos and used by developers daily. If gstack skills become Archeia-aware when a repo has Archeia docs, every gstack user gets Archeia benefits passively. This is a distribution multiplier that costs nothing.

**Decision:** Design Archeia to be composable with gstack. When a repo has Archeia docs, gstack skills can read them for context. Archeia does not depend on gstack, but gstack can optionally consume Archeia output.

**Assumptions relied on:** A-006 (gstack integration multiplies distribution), A-007 (scanner output is valuable)
**Constraints respected:** Architectural (no coupling — optional integration)

**Consequences:**
- gstack integration is a distribution channel, not a dependency.
- Archeia's generated docs must be stable enough for gstack to rely on.
- Coordination between Archeia and gstack development is needed.

**Alternatives considered:**
- Tight gstack coupling (Archeia requires gstack) — rejected because it limits Archeia's standalone use.
- No gstack integration — rejected because it wastes a free distribution channel.

**Cascades to:** State.yaml schema stability, gstack PR, ROADMAP F-002

---

## 2026-03-17 — D-014: Package architecture (scanner/state/renderers/cli + experiments)

**Domain:** Architecture
**Status:** Superseded by D-027

**Context:** The agent-native pivot required clear separation between the shipped product and internal evaluation tooling. Product packages must be stable and dependency-free. Internal packages can experiment freely without risking the product.

**Decision:** Product lane: `scanner`, `state`, `renderers`, `cli`. Internal lane: `analyzer`, `experiments`. Product-lane packages must not depend on internal-lane packages. Internal packages may depend on product packages.

**Assumptions relied on:** A-002 (context windows — scanner is the optimizer), A-005 (JS/TS+Python scope)
**Constraints respected:** Architectural (product-lane isolation), Operational (monorepo)

**Consequences:**
- Clear dependency direction prevents internal experimentation from destabilizing the product.
- Internal packages can be removed entirely without affecting the shipped product.
- Some code duplication may occur between lanes — this is acceptable.

**Alternatives considered:**
- Single package — rejected because it couples experimental code with shipped code.
- Separate repos — rejected because it complicates development for a solo developer.

**Cascades to:** ARCHITECTURE.md, CONSTRAINTS.md (dependency rules), package.json workspaces, CI pipeline

---

## 2026-03-17 — D-015: Claude and Codex as first agent targets

**Domain:** Product
**Status:** Accepted

**Context:** There are many agents to support (Claude Code, Cursor, Codex, Copilot, Windsurf, etc.). Trying to support all of them at once means supporting none well. Claude Code and Codex have the best AGENTS.md compliance and the most aligned user base.

**Decision:** Make Claude Code and Codex the first-class agent targets. Optimize AGENTS.md format, skill implementation, and testing for these two agents first. Broaden support only after these are excellent.

**Assumptions relied on:** A-001 (developer users), A-009 (agents follow AGENTS.md — Claude Code does this best)
**Constraints respected:** Operational (agent targets — Claude Code and Codex first)

**Consequences:**
- Focused testing and optimization for two agents.
- Cursor and other agent users may have a suboptimal experience initially.
- AGENTS.md format may be biased toward Claude Code's instruction-following style.

**Alternatives considered:**
- Support all agents equally — rejected because quality would be thin across all of them.
- Cursor first (larger market share) — rejected because Cursor's AGENTS.md compliance is less reliable than Claude Code's.

**Cascades to:** Testing matrix, AGENTS.md format decisions, skill implementation priorities

---

## 2026-03-17 — D-016: Conductor as Phase 1 host environment

**Domain:** Product
**Status:** Accepted

**Context:** Archeia needs a development environment for Phase 1. Conductor (the workspace management tool) is already in use and provides the multi-repo context that Archeia is designed for. Dogfooding Archeia inside Conductor validates both products.

**Decision:** Use Conductor as the primary development and testing environment for Phase 1. Archeia runs inside Conductor workspaces, which provides real multi-repo scenarios for testing.

**Assumptions relied on:** A-003 (solo devs with multiple repos — Conductor is exactly this)
**Constraints respected:** Financial ($0 infrastructure — Conductor is already available)

**Consequences:**
- Dogfooding provides continuous real-world testing.
- Archeia's design may be biased toward Conductor's workspace model.
- Users without Conductor must still have a good experience.

**Alternatives considered:**
- Standalone development environment — rejected because it misses the dogfooding opportunity.
- GitHub Codespaces — rejected because it adds cost and doesn't match the local-first constraint.

**Cascades to:** Development workflow, testing strategy, initial user scenarios

---

## 2026-03-16 — D-017: Experiments 2 and 3 deferred

**Domain:** Research
**Status:** Accepted

**Context:** Experiment 2 (fixed vs. modular analysis domains) and Experiment 3 (template vs. LLM rules) are research questions about the optimal analysis architecture. They are important but don't block Phase 1 — the scanner works with fixed domains and template rules. Answering them now would delay shipping.

**Decision:** Defer Experiments 2 and 3 to the internal evaluation lane. Don't let research block the shipped product. The experiments can run in the `experiments` package without affecting product-lane packages.

**Assumptions relied on:** A-007 (scanner-only is 80% valuable without these optimizations)
**Constraints respected:** Architectural (product-lane isolation — experiments don't block product)

**Consequences:**
- Phase 1 ships with fixed domains and template rules — good enough for validation.
- Research continues in parallel without blocking the product timeline.
- If experiments reveal a fundamentally better approach, refactoring may be needed later.

**Alternatives considered:**
- Run experiments before shipping — rejected because it delays validation by weeks/months.
- Abandon experiments entirely — rejected because they may reveal important architectural improvements.

**Cascades to:** ROADMAP (F-011 nice-to-have), experiments package scope, internal evaluation plan
