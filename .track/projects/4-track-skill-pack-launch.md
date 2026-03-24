# Track Convention Simplification

## Goal

Finish simplifying Track into a zero-dependency coordination convention driven by
`CLAUDE.md`, flat task files, Bash scripts, and provisional PR state.

## Why Now

The repo no longer needs a Track skill pack, Python validator, or claim system.
The remaining work is to keep the git-native operating model coherent and easy
to dogfood.

## In Scope

- `CLAUDE.md` as the always-on Track contract
- flat `.track/tasks/*.md` files with `project_id`
- Bash validation and `TODO.md` generation
- provisional PR lifecycle and post-merge completion writeback
- dogfooding the simplified operating model in this repo

## Out Of Scope

- reintroducing a Track plugin or standalone Track skill pack
- reintroducing claims, status subdirectories, or Python tooling
- turning Track into a service or daemon

## Shared Context

Track is now a repo convention, not a product runtime. Default-branch task files
own backlog state. Open GitHub PRs own effective in-flight state. `TODO.md` is a
derived view.

## Dependency Notes

Governance work still defines source-of-truth boundaries. Any follow-on Track
work should preserve the zero-dependency, git-native direction established by
this simplification.

## Success Definition

- the repo can validate Track state with Bash only
- `TODO.md` accurately reflects default-branch tasks plus open PR overlays
- task ownership is visible from provisional PRs without a claim system
- agents can follow Track purely from `CLAUDE.md` and `.track/`

## Candidate Task Seeds

- dogfood the provisional PR workflow across a few real tasks
- tighten TODO generation if overlap heuristics prove too loose
- add bootstrap snippets for other repos that want the same convention
