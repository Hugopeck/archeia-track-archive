# Vision

## Mission

Type `/archeia`, and the agent stops making avoidable mistakes about the repo.

Archeia exists to keep architectural context close enough, current enough, and actionable enough that an AI coding agent can make good choices without re-discovering the codebase from scratch every session.

## What We Learned

We spent real time building a scanner, renderers, a CLI, and a monorepo around deterministic analysis. That work was useful because it taught us what matters and what does not.

What mattered:
- the shape of the docs the agent needs
- the kinds of evidence that create trust
- the maintenance problem after the first draft exists
- the value of explicit constraints, standards, and decisions

What did not need to be the product:
- a compiled binary to walk files the agent can already read
- a custom pipeline to answer questions the agent can already ask
- a hosted service for coordination that git and pull requests already provide
- lifecycle hooks for context injection that native CLAUDE.md/AGENTS.md loading already handles

The honest lesson is simple: the agent is already the scanner. Archeia is the instructions, templates, and maintenance workflow that make the agent use that power well.

## Thesis

Architecture knowledge does not fail because teams cannot generate it once. It fails because the guidance files that agents actually read go stale.

Archeia's thesis is that the right product is a pair of skills plus templates, distributed as a Claude Code plugin:
- `/archeia:init` generates and updates the knowledge base
- `/archeia:ask` answers architecture questions from that knowledge base

The durable outcome is not a report. It is an `AGENTS.md` and `CLAUDE.md` that stay accurate enough to change agent behavior in normal coding work.

## Distribution Insight

The plugin's value is distribution, not automation. Claude Code's native CLAUDE.md and AGENTS.md loading already provides session-start context — every conversation begins informed because the agent loads these files automatically. Commit-time and PR-time enforcement (`archeia check`, GitHub Actions) is the right granularity for maintenance.

Hooks for context injection, drift detection, and stop-time enforcement were evaluated and found redundant with existing primitives. The plugin format solves the real gap: one-command install, marketplace discovery, versioning, and team adoption.

## Non-Goals

Archeia is not:
- a CLI tool or compiled binary product
- a cloud service
- an MCP server
- a replacement for git, pull requests, or code review
- a generic project management system
- a set of lifecycle hooks (native doc loading and CI-time checks cover these)

The repo contains historical code and experiments that informed the direction. Those are not the product.

## Why This Matters

When an agent has good repo instructions, it chooses the right files faster, asks better questions, and makes fewer expensive mistakes. That compounds across every session.

The immediate value is not abstraction purity. It is fewer wrong edits, fewer dead-end explorations, and faster first useful action.

## North Star

Every repo has `AGENTS.md`, `CLAUDE.md`, and supporting `.archeia/` docs that remain accurate without becoming a manual documentation chore.

Users install Archeia with one command. The generated docs stay current through commit-time checks and PR-based review. After two weeks of normal development, the instructions still help more than they hurt.

That is the product.
