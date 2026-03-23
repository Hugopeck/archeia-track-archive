# Knowledge Generation Pipeline

## Goal

Extend Archeia from Layer 3 evidence generation into a fuller knowledge
pipeline that includes targeted human confirmation and explicit Layer 1 support
when requested.

## Why Now

Layer 3 generation is already in place. The next leverage comes from improving
how Archeia asks better questions, captures non-obvious decisions, and scopes
business-context generation deliberately.

## In Scope

- git-history-informed Layer 2 preparation
- targeted Q&A flow for Layer 2 documents
- explicit Layer 1 generation boundaries
- template determinism measurement and tightening

## Out Of Scope

- a scanner revival
- a hosted knowledge service
- speculative new document families without a protocol update

## Shared Context

`.claude/skills/archeia/SKILL.md` already defines the exploration and template
meta-structure for Layer 3. Future work here should build on that contract,
not replace it.

## Dependency Notes

Depends on the governance project keeping Archeia protocol and ontology terms
stable. Query and maintenance work depends on the knowledge base being durable
enough to trust.

## Success Definition

- Layer 2 and optional Layer 1 flows are explicit, reviewable, and grounded
- templates get more deterministic where variance is currently too high
- the knowledge pipeline stays markdown-first and evidence-backed

## Candidate Task Seeds

- add git history analysis between Layer 3 generation and Layer 2 questions
- define the Layer 2 Q&A flow and output contract
- clarify explicit triggers for Layer 1 generation
- measure repeat-run variance and tighten unstable sections

