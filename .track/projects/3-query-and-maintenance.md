# Query And Maintenance

## Goal

Ship the read path and durable maintenance model for Archeia so that generated
guidance can be queried, reviewed, and kept current without inventing a new
runtime.

## Why Now

Generation without retrieval and maintenance leaves the product half-finished.
The repo already frames PR-time and CI-time workflows as the right enforcement
granularity, so this project should turn that into a coherent product surface.

## In Scope

- `/archeia:ask`
- maintenance model decisions and docs
- drift detection design and enforcement boundaries
- GitHub Action and PR-template support where appropriate

## Out Of Scope

- silently mutating docs during query flows
- per-tool hooks that duplicate native doc loading
- backend services for maintenance orchestration

## Shared Context

`.archeia/PROTOCOL.md` defines maintenance modes. `.archeia/ROADMAP.md` keeps
strategy narrative only; operational follow-on work lives here.

## Dependency Notes

Depends on the knowledge-generation pipeline for trustworthy docs and on the
governance foundation for protocol ownership.

## Success Definition

- `/archeia:ask` is clearly separated from write-path behavior
- maintenance workflows are reviewable and git-native
- follow-on automation is framed as support, not a second product

## Candidate Task Seeds

- implement `/archeia:ask`
- define deterministic drift-detection boundaries
- add PR template guidance for doc confirmation
- design or ship CI-time drift signaling

