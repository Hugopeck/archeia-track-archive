---
id: "028"
title: "[Plan] Define hybrid launch-readiness plan and exit criteria"
status: done
mode: plan
priority: high
project_id: "0"
created: 2026-03-22
updated: 2026-03-22
depends_on: []
files: []
pr: ""
---

## Context

### Problem
Track now has the hybrid Option C architecture in place, but the repo needs a clear launch-readiness plan so the remaining work is grouped, prioritized, and testable before any public launch push.

### Affected Files
- .track/config.yaml
- .track/done/028-define-hybrid-launch-readiness-plan-and-exit-criteria.md
- .track/todo/029-ship-remaining-planning-and-triage-workflow-skills.md
- .track/todo/030-publish-launch-ready-quickstart-and-migration-guide.md
- .track/todo/031-add-launch-smoke-checklist-for-hybrid-workflow.md
- .track/todo/032-dry-run-clean-clone-install-and-release-paths.md
- .track/todo/033-dogfood-hybrid-workflow-in-a-scratch-repo.md
- .track/todo/034-tighten-ci-and-release-assumptions-for-hybrid-launch.md
- .track/todo/035-run-final-launch-readiness-review-and-go-no-go.md

### References
- docs/specs/track-spec.md
- docs/specs/track-build-plan.md
- README.md

## Acceptance Criteria

- [x] The launch work is grouped into product, docs, quality, dogfooding, and release-readiness buckets
- [x] Each remaining launch item exists as its own atomic task under `.track/`
- [x] The final launch gate task depends on the concrete launch work rather than a vague checklist alone
- [x] The backlog uses the current hybrid contract instead of the retired all-in-one CLI story

## Verification

- Review the new `.track/todo/` tasks for launch coverage
- Run `cargo run -- validate`
- Run `cargo run -- build`

## Notes

- 2026-03-22 agent: Seeded the hybrid launch-readiness backlog and added the `launch-readiness` project.
- 2026-03-22 agent: Grouped launch work into skill coverage, migration docs, smoke checks, dogfooding, CI/release hardening, and final go/no-go review.
