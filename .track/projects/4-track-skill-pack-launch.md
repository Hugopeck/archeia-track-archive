# Track Skill Pack Launch

## Goal

Finish shipping Track as a pure skill pack with a strict protocol, a deterministic
validator, and enough dogfooding to trust the operating model.

## Why Now

Open launch tasks already exist, but they still point at the old
`launch-readiness` label. This brief gives the project a real scope contract so
the remaining launch work is easier to reason about and validate.

## In Scope

- rewrite remaining Track skills for the pure skill pack shape
- planning and coordination skill coverage
- validator completion and validation coverage
- dogfooding the Track operating model with multiple agents

## Out Of Scope

- reintroducing the archived Rust CLI
- widening Track vocabulary or status semantics casually
- turning Track into a service

## Shared Context

The canonical Track contract is `.track/PROTOCOL.md` plus `tools/track-lint.py`.
This project is about finishing the operating model, not changing the product
shape away from markdown-first coordination.

## Dependency Notes

Governance work upgrades the project model that this launch work now uses.
Launch validation should continue to reference archived launch work for history
without reopening those archived projects.

## Success Definition

- remaining launch tasks validate against the new project registry
- Track skills and validator agree on the same protocol
- dogfooding produces enough evidence to trust the launch path

## Candidate Task Seeds

- complete tasks 4.1–4.6 under the new project key
- add any missing project-aware planning behavior
- capture launch readiness evidence and unresolved risks
