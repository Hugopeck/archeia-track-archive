---
layer: 3
depends_on: none
required_evidence: package.json, pyproject.toml, Cargo.toml, go.mod, src/, lib/, app/
validation: all-required-sections-present, all-claims-cite-evidence, no-marketing-language, all-cited-paths-exist
---

## Purpose

ARCHITECTURE.md is the system-level map of the repository. It describes what
the system is, how it is structured, what its major components are, and how
data flows through it. It is read by coding agents before making structural
changes and by humans onboarding to the codebase.

This document must be factual and evidence-backed. Every claim must cite a
file path. If evidence is insufficient for a section, use:
`<!-- INSUFFICIENT EVIDENCE: [what is missing] -->`

---

## Required Sections

### System Overview

**Always include.** One paragraph describing what this project is and what
technology it uses.

Content must include:
- Primary language and version (from manifest)
- Primary framework (from dependencies)
- What the system does in one sentence (from README or manifest description)

**Format:**
```
This is a [language] [type] built with [framework]. It [one-sentence purpose].

**Evidence:** `[manifest file]` ([key dependency versions]), `[config file]`
```

### Topology

**Always include.** The highest-level structural view.

Content must include:
- **Type:** monolith, modular monolith, microservices, serverless, library, CLI,
  or hybrid. Infer from: single vs multiple entry points, presence of
  `docker-compose.yml` with multiple services, workspace configs, deploy configs.
- **Primary areas:** top-level source directories and their roles
- **External systems:** databases, caches, message queues, third-party APIs
  (infer from dependencies and config files)

**Format:**
```
- **Type:** [topology type]
- **Primary areas:** `[dir1]/` ([role]), `[dir2]/` ([role])
- **External systems:** [system] (via `[dependency]` in `[manifest]`)

**Evidence:** [file paths]
```

### Module Boundaries

**Always include.** A table of the major modules/packages/directories and
their relationships.

| Module | Path | Responsibility | Dependencies |
|--------|------|---------------|-------------|
| [Name] | `[path]/` | [What it does] | [What it imports from] |

Infer from: directory structure, import/require statements in entry point files,
workspace configurations.

**Evidence:** directory listing, import patterns in sampled source files.

### Data Flow

**Always include.** Numbered steps showing how data moves through the system
for the primary use case.

1. [Entry point] receives [input type]
2. [Component] processes/validates
3. [Component] executes logic
4. [Component] persists/queries data
5. [Output] returned

Infer from: route files, handler functions, service layer patterns, model/ORM
files.

**Evidence:** import chains in source files.

### Build and Development

**Always include.** How to build, run, and develop the project.

Content must include:
- **Package manager:** (from lockfile type)
- **Build command:** (from manifest scripts or Makefile)
- **Dev command:** (from manifest scripts or Makefile)
- **Test runner:** (from test config files or manifest scripts)
- **Task automation:** (Makefile, Justfile, Taskfile — if present)

**Evidence:** manifest scripts section, lockfile, task runner config.

---

## Conditional Sections

### Deployment

**Include if** deployment config files exist (Dockerfile, fly.toml, vercel.json,
render.yaml, railway.json, CI/CD workflows with deploy steps).

Content: deployment target, container configuration, CI/CD pipeline summary.

### API Surface

**Include if** the project exposes an API (route files, OpenAPI spec, GraphQL
schema, CLI argument parser).

Content: list of endpoints/commands, request/response format, authentication
method (if detectable from middleware or config).

### Workspace Structure

**Include if** the project is a monorepo (packages/, apps/, workspace config
in manifest).

Content: table of packages/apps with their purpose and inter-dependencies.

### Change Notes

**Include if** any of the following are detectable:
- High-risk areas (files with complex logic, auth, payment, data migration)
- Stable areas (configuration, simple CRUD, static assets)

Content:
- **High-risk areas:** [paths and why]
- **Stable areas:** [paths and why]
- **Open questions:** deferred to DECISIONS.md

---

## Inference Signals

These signals map repo evidence to ARCHITECTURE.md content:

| Evidence | Maps to section | Conclusion |
|----------|----------------|-----------|
| Manifest dependencies | System Overview, Topology | Language, framework, external systems |
| Directory structure (`src/`, `lib/`, `app/`) | Module Boundaries | Module layout and roles |
| Import statements in entry points | Data Flow, Module Boundaries | Dependency direction |
| Manifest scripts (build, dev, test) | Build and Development | Dev workflow |
| Lockfile type | Build and Development | Package manager |
| Dockerfile, deploy configs | Deployment | Deploy target and method |
| Route files, OpenAPI spec | API Surface | Endpoints and format |
| Workspace config (workspaces field) | Workspace Structure | Monorepo layout |
| `docker-compose.yml` services | Topology | External system dependencies |
| Test config files | Build and Development | Test runner and setup |

---

## Quality Rubric

The self-validation pass checks these criteria:

- **COMPLETENESS:** Every Required Section is present. Every table has at least
  one row. System Overview names the language and framework.
- **TRUTHFULNESS:** Every factual claim cites a file path in `**Evidence:**`
  format. No technologies are listed that weren't found in manifests or imports.
  All cited file paths exist in the repo (verified by Glob).
- **CONCISENESS:** No section exceeds 30 lines. No marketing language. No filler
  phrases like "leverages modern best practices" or "robust and scalable."
- **DETERMINISM:** Sections appear in the order listed above. Tables use the
  exact column headers specified. Evidence citations use consistent format.

---

## Anti-Patterns

DO NOT produce output like this:

- `This project uses modern best practices for web development.`
  → No evidence, marketing language. Instead: `This is a Python 3.12 API built
  with FastAPI. Evidence: pyproject.toml`
- `The architecture follows clean, well-organized patterns.`
  → Vague, no file references. Instead: `Three-layer structure: routes
  (src/routes/) → services (src/services/) → models (src/models/). Evidence:
  src/ directory listing`
- `Technologies: React, Node.js, PostgreSQL, Redis, Docker, Kubernetes`
  → Listing technologies not found in manifests. Only list what evidence
  confirms.
- A Data Flow section that describes hypothetical flows not traceable to
  actual source files.
- A Module Boundaries table with modules inferred from general knowledge
  rather than actual directory structure.
