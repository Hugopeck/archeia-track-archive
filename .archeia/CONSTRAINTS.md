# Constraints

These are non-negotiable boundaries. Agents should treat them as hard edges unless a human explicitly changes the framework docs.

## Financial

- **Founder model:** Keep the company operable by a solo founder.
- **Build cost:** V0 must cost $0 to build beyond founder time.
- **Operating cost:** V0 must cost $0 to operate. No required servers, hosted APIs, or paid infrastructure.
- **Revisit when:** a user need appears that cannot be satisfied inside the user's own agent session and git workflow.

## Architectural

- **No MCP** in any phase.
- **Product shape:** the product is `SKILL.md` files plus Markdown templates.
- **Agent-native first:** prefer the agent's native read, search, shell, and edit capabilities over custom binaries.
- **Evidence-backed claims:** architecture claims should map to real files, history, or explicit user confirmation.
- **Historical code may remain:** `packages/` can stay in the repo as learning and reference material, but it is not the V0 product surface.
- **Revisit when:** users repeatedly hit a limitation that skills plus templates cannot solve cleanly.

## Infrastructure

- **No infrastructure:** Archeia runs in the user's local or hosted agent session.
- **Git-native coordination:** confirmation happens through commits and pull requests, not a custom backend.
- **Optional GitHub automation only:** Actions may help with maintenance, but the core product must work without them.
- **Revisit when:** users need shared state or enforcement that git-native workflows genuinely cannot provide.

## Design

- **Two skills only:** `/archeia` and `/archeia-ask`.
- **Core outcome:** auto-maintained `AGENTS.md` and `CLAUDE.md`.
- **Templates over pipelines:** give the agent a strong document shape instead of building a larger generation stack.
- **Confirmation via PR:** use the repo's existing review loop rather than a custom approval UI.
- **Token efficiency is a testable claim:** measure wasted exploration before first useful action.
- **Revisit when:** users consistently want a different interaction model than skills plus repo docs.

## Compliance & Security

- **Secrets:** never commit API keys or secrets.
- **Evidence integrity:** do not fabricate file paths, commands, or architecture evidence.
- **Minimal destructiveness:** avoid destructive git or file operations unless the user explicitly asks.
- **Revisit when:** enterprise compliance requirements become a real adoption blocker.

## Operational

- **Agent targets:** make Claude Code and Codex excellent first.
- **Language posture:** V0 is language-agnostic at the skill level; examples may still skew toward JS/TS and Python.
- **Repo docs stay in sync with shipped behavior:** when the product shape changes, update the framework docs in the same change.
- **Revisit when:** support burden or user demand clearly favors a different target order.
