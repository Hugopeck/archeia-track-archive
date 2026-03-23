# Governance Foundation

## Goal

Define the durable governance stack for the repo so that shared definitions,
product protocols, executable contracts, strategy docs, and operational work
surfaces each have a clear owner.

## Why Now

The repo previously spread “what to do” and “what is true” across `TODO.md`,
`.track/`, `.archeia/ROADMAP.md`, templates, and scattered product docs. This
project consolidates authority before more work lands on top of the old overlap.

## In Scope

- shared ontology and source-of-truth hierarchy
- Archeia protocol definition
- Track project registry and project brief contract
- backlog surface migration from pointer docs into `.track/`
- cross-linking the governance model through top-level repo docs

## Out Of Scope

- a generic schema engine
- full repo-wide terminology cleanup in archived history
- new runtime services or a new CLI

## Shared Context

`docs/ONTOLOGY.md` is the shared vocabulary. `.track/PROTOCOL.md` and
`.archeia/PROTOCOL.md` own product-specific rules. `TODO.md` is now a pointer,
not a backlog.

## Dependency Notes

This project underpins the rest of the migration program. Validation and future
tooling work should reference these contracts instead of inventing new ones.

## Success Definition

- every durable artifact family has a named owner and protocol
- operational work lives in `.track/`
- strategic direction lives in `.archeia/ROADMAP.md`
- pointer files no longer duplicate backlog state

## Candidate Task Seeds

- audit remaining docs for outdated authority claims
- refine the governance hierarchy as new artifact families appear
- define how future generated schema/spec mirrors should be produced

