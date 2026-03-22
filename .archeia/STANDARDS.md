# Standards

## Repository Shape

- Treat the product surface as skill files plus templates.
- Keep framework docs under `.archeia/`.
- Keep repo-wide agent instructions in `AGENTS.md` and `CLAUDE.md`.
- Maintain template sync across all three distribution directories.

## Skill Files

- Use YAML frontmatter with `name`, `version`, `description`, and `allowed-tools`.
- Write skills as operational instructions, not marketing copy.
- Keep workflows concrete: what to read, how to decide, what to write.
- Prefer steps that can be verified through repo evidence.

## Templates

- Keep templates valid Markdown.
- Use clear placeholders such as `{{PROJECT_NAME}}` and `{{EVIDENCE_PATHS}}`.
- Favor section structures that are easy for agents to fill and humans to review.
- Do not hide critical assumptions inside placeholder text.

## Writing Style

- Prefer direct language over slogans.
- Call out uncertainty explicitly.
- Separate observed facts from inferred conclusions.
- Keep generated instructions short enough to reload during normal work.

## Deferred Work Comments

- Use `// TODO(name): description. Issue #N`.
- Use the same format for `FIXME` and `HACK`.
- Every deferred-work comment must reference a GitHub issue number.
- If the fix is small and self-contained, fix it instead of leaving a deferred note.

## Validation

- Skill changes are tested by running them against real repositories.
- Template changes are tested by generating docs and reviewing the output.

## Commit Policy

**Header:** `<type>(<scope>): <subject>`

**Types:** feat, fix, refactor, test, docs, chore, ci, build, perf, revert

**Scope:** use a real concern such as `skills`, `framework`, `repo`, or `docs`

**Body sections:**
- `Why:`
- `What:`
- `Validation:`
