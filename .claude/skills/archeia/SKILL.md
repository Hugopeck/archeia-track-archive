---
name: archeia
version: 0.2.0
description: |
  Generate and maintain architecture guidance for a repository. Explores the
  repo via LLM, reads directory structure, manifests, configs, and imports,
  then generates `.archeia/` docs, `AGENTS.md`, and `CLAUDE.md`. Maximizes
  determinism through structured templates, evidence grounding, and
  self-validation.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - Write
  - AskUserQuestion
---

## Purpose

`/archeia` is the write path for Archeia.

Its job is to:
- understand the repository from real evidence
- generate or update `.archeia/` docs using structured templates
- write `AGENTS.md` and `CLAUDE.md`
- keep those instructions current over time

The durable output is maintained guidance, not a one-time scan report.

<!-- TEMPLATE META-STRUCTURE
Every template in templates/ follows this structure:
1. YAML frontmatter (layer, depends_on, required_evidence, validation)
2. Purpose — what this document is and who reads it
3. Required Sections — sections that MUST appear in output
4. Conditional Sections — sections that appear only if evidence supports them
5. Inference Signals — what repo evidence maps to what content for this template
6. Quality Rubric — completeness, truthfulness, conciseness, determinism criteria
7. Anti-Patterns — DO NOT examples of bad output
8. Example Output — condensed example of good output (Layer 3 templates only)

Frontmatter fields:
- layer: 3 (auto-generate from evidence) or 2 (requires human confirmation)
- depends_on: comma-separated template names that must be generated first
- required_evidence: comma-separated file patterns to read before generating
- validation: comma-separated quality checks for the self-validation pass

The skill reads frontmatter to determine generation order and validation
criteria. Frontmatter is consumed by the skill — it is NOT included in
generated output.
-->

## Workflow

### Phase 1: Detection

Before exploring the repo, check if `.archeia/` already exists.

- If `.archeia/` exists: ask the user whether to **refresh** (regenerate Layer 3
  docs only, preserve all Layer 2 docs) or **overwrite** (regenerate everything
  from scratch). Refresh is the default recommendation.
- If `.archeia/` does not exist: proceed with full init.

### Phase 2: Exploration

Read repo files in this exact priority order. Within each category, read files
alphabetically. Stop exploring after reading ~30 files total — shift to
generation if the budget is reached. If a critical file is discovered late,
reading it is fine.

**Priority 1 — Root manifests** (read all that exist):
`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`,
`composer.json`, `pom.xml`, `build.gradle`, `Mix.exs`, `deno.json`

**Priority 2 — Root configs** (read all that exist):
`tsconfig.json`, `tsconfig*.json`, `ruff.toml`, `pyproject.toml [tool.*]`,
`.eslintrc*`, `.prettierrc*`, `biome.json`, `Makefile`, `Justfile`,
`Taskfile.yml`, `Dockerfile`, `docker-compose.yml`, `fly.toml`, `render.yaml`,
`railway.json`, `vercel.json`, `netlify.toml`

**Priority 3 — Root docs** (read all that exist):
`README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `AGENTS.md`, `CLAUDE.md`

**Priority 4 — CI/CD** (read first 3 files alphabetically):
`.github/workflows/*.yml`, `.gitlab-ci.yml`, `.circleci/config.yml`

**Priority 5 — Test setup** (read config files, not test bodies):
`tests/conftest.py`, `jest.config.*`, `vitest.config.*`, `test/test_helper.*`,
`.nycrc`, `pytest.ini`, `setup.cfg [tool:pytest]`, `phpunit.xml`

**Priority 6 — Source sampling** (read first 5 files alphabetically):
Files in `src/`, `lib/`, `app/`, or the primary source directory. Focus on
entry points and module index files (`index.*`, `main.*`, `app.*`, `mod.rs`).

**Priority 7 — Existing `.archeia/`** (if refreshing):
All files in `.archeia/` to understand current state.

### Inference Signal Table

Use this table to map discovered files to conclusions. When signals conflict,
follow the priority order: **manifest content > file extensions > directory
structure > README claims**.

| Signal | Conclusion |
|--------|-----------|
| `package.json` exists | Node.js/JavaScript project |
| `package.json` has `"type": "module"` | ESM modules |
| `package.json` → `dependencies` has `react` | React frontend |
| `package.json` → `dependencies` has `express`/`fastify`/`hono` | HTTP server framework |
| `package.json` → `dependencies` has `next` | Next.js full-stack |
| `package.json` → `devDependencies` has `typescript` | TypeScript project |
| `package.json` → `scripts` has `test` | Has test runner |
| `tsconfig.json` exists | TypeScript (confirms) |
| `pyproject.toml` exists | Python project |
| `pyproject.toml` → `[tool.ruff]` | Uses ruff linter |
| `pyproject.toml` → `[tool.black]` | Uses black formatter |
| `pyproject.toml` → `[tool.mypy]` | Uses mypy type checker |
| `pyproject.toml` → `[tool.pytest]` | Uses pytest |
| `requirements.txt` / `setup.py` | Python (legacy packaging) |
| `Cargo.toml` exists | Rust project |
| `go.mod` exists | Go project |
| `Gemfile` exists | Ruby project |
| `composer.json` exists | PHP project |
| `pom.xml` / `build.gradle` | Java/JVM project |
| `Mix.exs` exists | Elixir project |
| `deno.json` exists | Deno runtime |
| `Dockerfile` exists | Containerized deployment |
| `docker-compose.yml` exists | Multi-service local dev |
| `fly.toml` | Deploys to Fly.io |
| `vercel.json` / `netlify.toml` | Serverless/JAMstack deploy |
| `render.yaml` / `railway.json` | PaaS deployment |
| `.github/workflows/` | GitHub Actions CI/CD |
| `.gitlab-ci.yml` | GitLab CI |
| `Makefile` / `Justfile` / `Taskfile.yml` | Has task automation |
| `tests/` / `__tests__/` / `spec/` / `test/` | Has test directory |
| `.pre-commit-config.yaml` | Uses pre-commit hooks |
| `src/` directory | Standard source layout |
| `lib/` directory | Library-style source layout |
| `app/` directory | Application-style layout (Rails, Next.js, etc.) |
| `packages/` / `apps/` | Monorepo with workspaces |
| `.env.example` | Environment-variable configuration |
| `uv.lock` / `poetry.lock` | Python lockfile (uv or poetry) |
| `pnpm-lock.yaml` / `package-lock.json` / `yarn.lock` | JS lockfile |

### Phase 3: Layer 3 Generation

Generate Layer 3 docs in this order (respecting dependencies):

1. Read `templates/ARCHITECTURE.md` frontmatter and body
2. Generate `.archeia/ARCHITECTURE.md` from collected signals
3. Read `templates/STANDARDS.md` frontmatter and body
4. Generate `.archeia/STANDARDS.md` (may reference ARCHITECTURE for topology)
5. Read `templates/GUIDE.md` frontmatter and body
6. Generate `.archeia/GUIDE.md` (may reference ARCHITECTURE + STANDARDS)

For each generated file:
- Follow the template's Required Sections exactly
- Include Conditional Sections only when evidence supports them
- Cite evidence: every factual claim must reference a file path
- Use `<!-- INSUFFICIENT EVIDENCE: [description] -->` for gaps
- Do not include the template frontmatter in output
- Do not use marketing language or unsupported superlatives

### Phase 4: Self-Validation

After generating all Layer 3 docs, run a validation pass:

**Step 1 — Rubric check:** Re-read each generated file. For each template's
quality rubric (listed at the bottom of the template), verify the output meets
every criterion. Fix issues inline using the Edit tool. One fix pass maximum —
if an issue persists after one fix attempt, note it and move on.

**Step 2 — File-existence verification:** Extract every file path cited in the
generated docs (paths like `package.json`, `src/index.ts`, etc.). Use Glob to
verify each path exists in the repo. Remove or annotate any citation where the
file does not exist.

**Step 3 — Validation summary:** Print a summary for the user:
- Number of Layer 3 docs generated
- Number of files read during exploration
- Number of issues found and fixed in validation
- Number of fabricated paths caught and removed
- Any remaining gaps (sections marked INSUFFICIENT EVIDENCE)

### Phase 5: Layer 2 Preparation

If this is a full init (not just Layer 3 refresh):

1. Ask only the questions the repo cannot answer reliably — decisions,
   constraints, preferences, and assumptions require human confirmation.
2. Generate Layer 2 docs using their templates.
3. Write or refresh `AGENTS.md` and `CLAUDE.md`.

If this is a Layer 3 refresh: skip this phase, preserve existing Layer 2 docs.

### Phase 6: Finalization

1. Offer to migrate good existing docs into the Archeia structure.
2. Offer GitHub Action and PR-template guidance when maintenance should be
   automated.
3. Confirm changes through a normal diff or pull request, not a custom
   approval flow.

## Operating Rules

- Every factual claim must cite a file path as evidence.
- When evidence is insufficient, use `<!-- INSUFFICIENT EVIDENCE: ... -->`.
- When signals conflict, follow signal priority: manifest > extensions >
  structure > README claims.
- Prefer short, high-signal docs agents can reload frequently.
- Use template structure as the output skeleton, not as final prose.
- Do not position the historical scanner or cloud service as the current product.
- Do not invent technologies, frameworks, or dependencies not found in evidence.
- Do not use marketing language, superlatives, or filler phrases.

## Expected Outputs

Layer 3 (auto-generated, no human input):
- `.archeia/ARCHITECTURE.md`
- `.archeia/STANDARDS.md`
- `.archeia/GUIDE.md`

Layer 2 (requires human confirmation):
- `.archeia/DECISIONS.md`
- `.archeia/CONSTRAINTS.md`
- `.archeia/PREFERENCES.md`
- `.archeia/ASSUMPTIONS.md`

Synthesis (combines Layer 2 + Layer 3):
- `AGENTS.md`
- `CLAUDE.md`

## Worked Example

Below is a condensed example of what `.archeia/ARCHITECTURE.md` should look
like for a Node.js Express API project. This demonstrates evidence-citing style,
section structure, and appropriate level of detail.

```markdown
# Architecture

## System Overview

This is a Node.js REST API built with Express and TypeScript. It serves as the
backend for a task management application.

**Evidence:** `package.json` (Express 4.18, TypeScript 5.3), `tsconfig.json`
(strict mode, ES2022 target)

## Topology

- **Type:** Single-process HTTP server (monolith)
- **Primary areas:** `src/routes/`, `src/services/`, `src/models/`
- **External systems:** PostgreSQL (via `pg` in dependencies), Redis
  (via `ioredis` in dependencies)

**Evidence:** `package.json` dependencies, `src/` directory structure,
`docker-compose.yml` (postgres and redis services)

## Module Boundaries

| Module | Path | Responsibility | Dependencies |
|--------|------|---------------|-------------|
| Routes | `src/routes/` | HTTP request handling | Services |
| Services | `src/services/` | Business logic | Models |
| Models | `src/models/` | Data access, ORM models | pg driver |
| Middleware | `src/middleware/` | Auth, logging, error handling | — |

**Evidence:** `src/` directory listing, import patterns in `src/routes/index.ts`

## Data Flow

1. HTTP request → Express middleware chain (`src/middleware/`)
2. Route handler (`src/routes/`) validates input
3. Service layer (`src/services/`) executes business logic
4. Model layer (`src/models/`) queries PostgreSQL
5. Response serialized and returned

**Evidence:** `src/routes/tasks.ts` imports from `src/services/taskService.ts`,
which imports from `src/models/task.ts`

## Build and Development

- **Package manager:** pnpm (`pnpm-lock.yaml` present)
- **Build:** `tsc` via `package.json` scripts.build
- **Dev server:** `tsx watch` via `package.json` scripts.dev
- **Test runner:** vitest (`vitest.config.ts` present)

**Evidence:** `package.json` scripts section, `pnpm-lock.yaml`, `vitest.config.ts`

## Change Notes

- **High-risk areas:** `src/models/` (database schema changes),
  `src/middleware/auth.ts` (authentication logic)
- **Stable areas:** `src/routes/` (thin handlers, low logic density)
- **Open questions:** None at Layer 3 — architecture decisions deferred to
  DECISIONS.md
```

## Maintenance Modes

Choose the lightest mode that fits the repo:
- inline doc updates during normal coding work
- drift captured in a dedicated PR
- GitHub Action-based maintenance for scheduled or review-time checks

## Done When

The run is successful when:
- the key docs exist or were refreshed
- the instructions reflect current repo reality
- every factual claim cites a file path as evidence
- the self-validation pass found no remaining critical gaps
- the user can review the result through normal git workflows
