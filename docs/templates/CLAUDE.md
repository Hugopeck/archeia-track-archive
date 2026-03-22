# Claude Code Guide

_Illustrative hand-written template. The product pipeline currently renders this deterministically from validated Archeia state._

This file is the repo-specific starting point for Claude Code work.

- Schema version: `<schema-version>`
- Project: `<project-name>`
- Files analyzed: `<count>`

## Working Summary

`<short description of the repo's architecture and current priorities>`

## Claude Code Priorities

- Follow the recorded agent rules before falling back to generic coding habits.
- Preserve confirmed decisions and repository conventions unless the task explicitly changes them.
- Ask for clarification when the request conflicts with recorded evidence or the repo state is ambiguous.

## Agent Rules

- `<repo-specific rule>`
- `<repo-specific rule>`

## Stack

- `<tool-or-framework> <version> (<confidence>)`

## Architecture

### Domain 1: `<domain-name>`
- Status: `<consistent|mixed|unknown|...>`
- Primary: `<primary pattern or subsystem>`
- Secondary: `<secondary pattern or subsystem>`
- Evidence:
  - `<path/to/file>`

## Decisions

### Decision 1: `<decision title>`
- ID: `<ADR-001 or null>`
- Status: `<detected|confirmed|deprecated|...>`
- Rationale: `<why this decision exists>`
- Alternatives:
  - `<alternative option>`

## Findings

### Finding 1
- Severity: `<info|warning|critical>`
- Description: `<what was observed>`
- Recommendation: `<optional next action>`
- Evidence:
  - `<path/to/file>`

## Conventions

### Convention 1
- Category: `<formatting|testing|structure|...>`
- Tool: `<tool-name>`
- Rule: `<repo convention stated in plain language>`
- Evidence: `<path/to/file>`

## Handshake Context

### Handshake 1
```json
{
  "question": "<question to resolve ambiguity>",
  "status": "<pending|resolved>",
  "answer": "<optional answer>",
  "evidence": [
    "<path/to/file>"
  ]
}
```
