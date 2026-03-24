# Archeia Protocol

This document is the protocol for Archeia's knowledge-generation and guidance
surfaces. It defines which document families exist, how they are created, and
which files own the durable contract for Archeia behavior.

## Purpose

Archeia is a markdown-first product. Its durable output is maintained guidance,
not a one-time scan report. The protocol exists so that repo knowledge,
templates, and generated guidance can evolve without drifting into multiple
competing definitions.

## Canonical Contract Surfaces

- **Executable skill contract:** `.claude/skills/archeia/SKILL.md`
- **Template contracts:** `.claude/skills/archeia/templates/*.md`
- **Query skill:** `.claude/skills/archeia-ask/SKILL.md`
- **Generated guidance surface:** `.archeia/*.md`, `AGENTS.md`, `CLAUDE.md`
- **Shared definitions:** `docs/ONTOLOGY.md`
- **Strategy only:** `.archeia/ROADMAP.md`

If this document conflicts with a template-specific requirement, the template is
the more specific contract for that document type.

## Document Families By Layer

### Layer 3 — Evidence-generated

Layer 3 documents are generated from observed repository evidence. They should
be factual, cite files where appropriate, and avoid turning uncertainty into
storytelling.

Primary documents:
- `ARCHITECTURE.md`
- `STANDARDS.md`
- `GUIDE.md`

### Layer 2 — Human-confirmed

Layer 2 documents combine repo evidence with targeted human confirmation. The
skill should only ask questions where the repo cannot reliably answer them.

Primary documents:
- `DECISIONS.md`
- `CONSTRAINTS.md`
- `ASSUMPTIONS.md`
- `PREFERENCES.md`

### Layer 1 — Business/context-heavy and explicitly requested

Layer 1 documents capture business direction, product intent, and strategic
context. They should be created or refreshed only when the developer asks for
full business context.

Primary documents:
- `VISION.md`
- `BUSINESS_PLAN.md`
- `ROADMAP.md`

## Template Meta-Structure

Each Archeia template follows the meta-structure defined in
`.claude/skills/archeia/SKILL.md`:

1. YAML frontmatter
2. Purpose
3. Required Sections
4. Conditional Sections
5. Inference Signals
6. Quality Rubric
7. Anti-Patterns
8. Example Output (Layer 3 templates only)

Template frontmatter fields are:
- `layer`
- `depends_on`
- `required_evidence`
- `validation`

The skill consumes this metadata to determine generation order, evidence
requirements, and self-validation criteria. Template frontmatter is not copied
into generated output.

## Refresh And Overwrite Modes

When `.archeia/` already exists, Archeia should treat refresh and overwrite as
different maintenance modes.

- **Refresh** regenerates Layer 3 outputs and preserves human-confirmed Layer 2
  materials unless the user explicitly asks to replace them.
- **Overwrite** regenerates the guidance surface from scratch and may replace
  existing Layer 2 and Layer 1 materials.

Refresh is the default recommended path because it minimizes accidental loss of
human-authored nuance.

## Migration And Absorption Rules

If a repo already has architecture or workflow docs, the skill should treat them
as migration inputs rather than noise.

- preserve human-authored nuance where possible
- prefer explicit migration or absorption over silent replacement
- record uncertainty instead of flattening conflicting docs into a fake single truth

## Maintenance Modes

Archeia supports three durable maintenance modes:

1. **Inline maintenance** — update docs in the same change that modifies the code
2. **Drift to PR** — propose a docs-only review flow when wording needs review
3. **CI-time checks** — detect drift at PR time or on a schedule

These are maintenance patterns, not separate products.

## Ownership Matrix

| Document | Ownership mode | Notes |
|----------|----------------|-------|
| `ARCHITECTURE.md` | Generated, evidence-backed | Layer 3 system map |
| `STANDARDS.md` | Generated, evidence-backed | Layer 3 conventions and tools |
| `GUIDE.md` | Generated, evidence-backed | Layer 3 operational handbook |
| `DECISIONS.md` | Human-confirmed | Layer 2 decision log |
| `CONSTRAINTS.md` | Human-confirmed | Layer 2 hard boundaries |
| `ASSUMPTIONS.md` | Human-confirmed | Layer 2 uncertainty tracking |
| `PREFERENCES.md` | Human-confirmed | Layer 2 style and workflow preferences |
| `VISION.md` | Human-authored or heavily guided | Layer 1 strategic intent |
| `BUSINESS_PLAN.md` | Human-authored or heavily guided | Layer 1 business framing |
| `ROADMAP.md` | Human-authored strategy surface | Strategy only, not operational backlog |
| `AGENTS.md` | Generated guidance surface | Top-level agent workflow guide |
| `CLAUDE.md` | Generated guidance surface | Claude-oriented workflow guide |

## Change Rules

1. Update this protocol when Archeia adds a new durable document family.
2. Update the relevant template and `SKILL.md` in the same change when template
   structure or generation logic changes.
3. Keep `.archeia/ROADMAP.md` strategic.
4. Do not introduce hand-maintained duplicate schema/spec files for Archeia
   unless tooling consumes them or they are generated mirrors of canonical data.

