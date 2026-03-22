---
name: archeia-init
version: 0.1.0
description: |
  Generate and maintain architecture guidance for a repository. Use this skill
  to explore the repo, write `.archeia/` framework docs, refresh `AGENTS.md`
  and `CLAUDE.md`, migrate existing docs, and offer repo-native maintenance
  flows such as PR confirmation and GitHub Action recipes.
---

## Purpose

`archeia-init` is the write path for Archeia.

Its job is to:
- understand the repository from real evidence
- generate or update `.archeia/` docs
- write `AGENTS.md` and `CLAUDE.md`
- keep those instructions current over time

The durable output is maintained guidance, not a one-time scan report.

## Workflow

1. Map the repository before asking questions.
2. Read existing root docs, package or service boundaries, CI, and test setup.
3. Generate or update `.archeia/` docs using the templates in `templates/`.
4. Inspect git history when it adds useful explanatory context.
5. Ask only the questions that the repo cannot answer reliably.
6. Write or refresh `AGENTS.md` and `CLAUDE.md`.
7. Offer to migrate good existing docs into the Archeia structure.
8. Offer GitHub Action and PR-template guidance when maintenance should be automated.
9. Confirm changes through a normal diff or pull request, not a custom approval flow.

## Operating Rules

- Prefer evidence-backed claims over inferred stories.
- Prefer short, high-signal docs agents can reload frequently.
- Use placeholders from templates as guidance, not as final prose.
- If evidence is weak, say so and ask a targeted question.
- Do not position the historical scanner or cloud service as the current product.

## Expected Outputs

Typical outputs include:
- `.archeia/ARCHITECTURE.md`
- `.archeia/DECISIONS.md`
- `.archeia/CONSTRAINTS.md`
- `.archeia/STANDARDS.md`
- `.archeia/GUIDE.md`
- `.archeia/PREFERENCES.md`
- `.archeia/ASSUMPTIONS.md`
- `AGENTS.md`
- `CLAUDE.md`

## Maintenance Modes

Choose the lightest mode that fits the repo:
- inline doc updates during normal coding work
- drift captured in a dedicated PR
- GitHub Action-based maintenance for scheduled or review-time checks

## Done When

The run is successful when:
- the key docs exist or were refreshed
- the instructions reflect current repo reality
- important claims point back to evidence
- the user can review the result through normal git workflows
