---
id: "023"
title: "[Implement] Add shared Conductor scripts for track"
status: done
mode: implement
priority: medium
project_id: "0"
created: 2026-03-17
updated: 2026-03-17
depends_on:
  - "022"
files: []
pr: ""
---

## Context

### Problem
Once the repo's ephemeral-derived migration is complete, teammates should be able to get a consistent Conductor workspace experience without hand-configuring personal scripts.

### Cause
Conductor supports a committed `conductor.json` for shared `setup`, `run`, and optional `archive` scripts. This repo does not yet provide one, so every teammate must configure scripts manually.

### Affected Files
- `conductor.json`
- `scripts/conductor/` — only if wrapper scripts are needed for readability or reuse

### References
- Depends on: task 022
- Source: `https://docs.conductor.build/core/conductor-json`
- Source: `https://docs.conductor.build/core/scripts`

## Acceptance Criteria

- [x] `conductor.json` defines the agreed shared setup and run workflow for this repo
- [x] `runScriptMode` is set deliberately for the chosen workflow
- [x] Shared scripts avoid unnecessary `.track/` churn and match the repo's documented workflow

## Verification

- Inspect `conductor.json` against the Conductor schema docs
- Create a fresh workspace or equivalent proof and confirm setup/run scripts behave as intended

## Notes

- 2026-03-17 codex: Keep `conductor.json` small unless script wrappers materially improve clarity.
- 2026-03-17 agent: Added the repo-root `conductor.json` with shared `setup`/`run` scripts and `runScriptMode: nonconcurrent`; this was later revised so shared setup also runs `track build` by default.
- 2026-03-17 human: Updated the shared workflow so `setup` now runs `cargo fetch --locked && cargo run -- build`, making the board available by default in each workspace.
