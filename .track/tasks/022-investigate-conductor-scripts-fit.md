---
id: "022"
title: "[Investigate] Confirm Conductor scripts fit after ephemeral migration"
status: done
mode: investigate
priority: medium
project_id: "0"
created: 2026-03-17
updated: 2026-03-17
depends_on:
  - "016"
  - "019"
  - "020"
files: []
pr: ""
---

## Context

### Problem
We want to add repo-shared Conductor scripts for this project, but the repository is still finishing the shift to ephemeral derived Track files and updated docs. Adding workspace automation before that lands risks baking stale assumptions into `conductor.json`.

### Cause
Conductor scripts should automate stable, repeatable workspace actions. Right now this repo still tracks `.track/index.json` and `.track/BOARD.md`, while task 016 removes those tracked artifacts and tasks 019/020 align the docs with the current workflow.

### Affected Files
- `conductor.json` — potential shared script entrypoint
- `README.md` — contributor workflow guidance
- `AGENTS.md` — policy boundary, if any extra guidance is needed

### References
- Depends on: tasks 016, 019, 020
- Investigation output: `docs/conductor-workspace.md`
- Source: `https://docs.conductor.build/core/scripts`
- Source: `https://docs.conductor.build/core/conductor-json`

## Acceptance Criteria

- [x] Recommendation is explicit about whether to add shared Conductor scripts now or after the ephemeral migration finishes
- [x] Recommendation names which actions belong in Conductor scripts versus `AGENTS.md`
- [x] Recommended shared scripts are deterministic and safe for parallel workspaces

## Verification

- Read the Conductor scripts and `conductor.json` docs
- Compare the recommendation against the repo's current `.track/` behavior and contributor docs

## Notes

- 2026-03-17 codex: Seeded after reviewing current `.track/` drift and Conductor scripts docs.
- 2026-03-17 agent: Wrote `docs/conductor-workspace.md` and recommended adding a minimal shared `conductor.json` now that the ephemeral-derived migration is complete.
- 2026-03-17 agent: Initially recommended keeping executable, deterministic workspace actions in `conductor.json` (`cargo fetch --locked`, `cargo run -- validate`) and keeping policy, review rules, and commit/PR guidance in `AGENTS.md`; later updated so shared setup also runs `cargo run -- build`.
- 2026-03-17 human: Reversed the initial setup choice; shared Conductor setup now also runs `cargo run -- build` so each workspace opens with a fresh local board and index.
