# Assumptions

<!-- ASSUMPTION INDEX
| ID    | Domain       | Assumption                                                        | Status       | Confidence |
|-------|--------------|-------------------------------------------------------------------|--------------|------------|
| A-001 | Market       | Primary users are developers already working with agents          | Believed     | High       |
| A-002 | Technical    | Context limits still matter, but native tool use beats pipelines  | Validated    | High       |
| A-003 | Market       | Solo developers and small teams are the best early wedge          | Believed     | Medium     |
| A-004 | Business     | 5% free-to-paid conversion is a useful planning anchor            | Invalidated  | High       |
| A-005 | Product      | Architecture guidance is useful even without language-specific tooling | Believed | Medium     |
| A-006 | Distribution | gstack and adjacent agent ecosystems can amplify discovery        | Untested     | Medium     |
| A-007 | Product      | Scanner-only output is valuable enough as the V0 product          | Invalidated  | High       |
| A-008 | Product      | Minimal commands are better than a large command surface          | Believed     | High       |
| A-009 | Product      | Agents follow `AGENTS.md` and `CLAUDE.md` reliably enough         | Untested     | Medium     |
| A-010 | Product      | A cloud service is categorically better than git-native workflows | Invalidated  | High       |
| A-011 | Product      | Templates plus instructions beat a custom scanner pipeline for V0 | Believed     | Medium     |
| A-012 | Product      | Token efficiency is measurable enough to be a product claim       | Untested     | Medium     |
-->

---

## A-001 — Primary users are developers already working with agents

**Domain:** Market  
**Status:** Believed  
**Confidence:** High — the product only makes sense if users already trust agents enough to care about agent behavior.
**Basis:** Existing demand for `AGENTS.md`, `CLAUDE.md`, and repo-specific coding instructions.

**Depends on:** Nothing upstream  
**Depended on by:** D-029, D-032, D-033

**Invalidated when:** most interested users want a standalone UI rather than an in-agent workflow.

**If invalidated:** reconsider the primary surface area and onboarding model.

---

## A-002 — Context limits still matter, but native tool use beats pipelines

**Domain:** Technical  
**Status:** Validated  
**Confidence:** High — building the old pipeline clarified that the real scarce resource is useful context, not file access.
**Basis:** Historical scanner work plus everyday agent usage showed that good tool sequencing beats an extra compiled layer for V0.

**Depends on:** A-001  
**Depended on by:** D-029, D-031

**Invalidated when:** native agent exploration becomes too unreliable or too expensive compared with a custom runtime.

**If invalidated:** reconsider whether a dedicated analysis layer belongs back in the product.

---

## A-003 — Solo developers and small teams are the best early wedge

**Domain:** Market  
**Status:** Believed  
**Confidence:** Medium — they feel doc rot quickly and can adopt without procurement.
**Basis:** Product shape, pricing posture, and git-native workflows are easiest for small teams.

**Depends on:** A-001  
**Depended on by:** BUSINESS_PLAN.md, ROADMAP.md

**Invalidated when:** larger teams adopt first or the solo wedge does not retain.

**If invalidated:** revisit maintenance defaults and distribution priorities.

---

## A-004 — 5% free-to-paid conversion is a useful planning anchor

**Domain:** Business  
**Status:** Invalidated  
**Confidence:** High — there is no paid model worth anchoring on yet.
**Basis:** The cloud monetization story was removed; early work should optimize for retention and clarity, not conversion math.

**Depends on:** Nothing upstream  
**Depended on by:** historical business docs only

**Invalidated when:** already invalidated.

**If invalidated:** done; do not use conversion math to justify V0 scope.

---

## A-005 — Architecture guidance is useful even without language-specific tooling

**Domain:** Product  
**Status:** Believed  
**Confidence:** Medium — repo structure, standards, constraints, and decisions matter across stacks.
**Basis:** The most valuable outputs are prose instructions and maintenance workflows, not parser-specific state.

**Depends on:** A-001, A-002  
**Depended on by:** D-029, CONSTRAINTS.md

**Invalidated when:** users consistently need deep language semantics before the docs become useful.

**If invalidated:** narrow scope again or add targeted stack-specific template layers.

---

## A-006 — gstack and adjacent agent ecosystems can amplify discovery

**Domain:** Distribution  
**Status:** Untested  
**Confidence:** Medium — the product spreads well if it can live where agents already look for skills.
**Basis:** Skill directories and shared repo instructions create a natural discovery path.

**Depends on:** A-001  
**Depended on by:** ROADMAP.md, AGENTS.md

**Invalidated when:** users mostly install Archeia outside skill ecosystems or discovery remains poor despite integration.

**If invalidated:** invest in a clearer standalone install path and documentation.

---

## A-007 — Scanner-only output is valuable enough as the V0 product

**Domain:** Product  
**Status:** Invalidated  
**Confidence:** High — the historical implementation taught us that output shape matters, but the scanner itself should not be the product.
**Basis:** The agent already has the primitives the scanner was duplicating.

**Depends on:** A-002  
**Depended on by:** historical D-013, historical D-019

**Invalidated when:** already invalidated.

**If invalidated:** done; optimize the skill workflow and maintenance loop instead.

---

## A-008 — Minimal commands are better than a large command surface

**Domain:** Product  
**Status:** Believed  
**Confidence:** High — users should not have to memorize a product taxonomy to keep docs current.
**Basis:** The more behavior that can flow through normal conversation plus two explicit skills, the better.

**Depends on:** A-001  
**Depended on by:** D-018, D-029

**Invalidated when:** users need many specialized entry points to get reliable behavior.

**If invalidated:** add commands only where a separate context-loading strategy is clearly justified.

---

## A-009 — Agents follow `AGENTS.md` and `CLAUDE.md` reliably enough

**Domain:** Product  
**Status:** Untested  
**Confidence:** Medium — this is the core bet, but behavior varies by agent and prompt stack.
**Basis:** Current agents do often respect repo-level instructions, but consistency is not guaranteed.

**Depends on:** A-001  
**Depended on by:** D-032, AGENTS.md, CLAUDE.md templates

**Invalidated when:** updated instruction files do not materially change agent behavior in practice.

**If invalidated:** Archeia must shift toward review and retrieval value, not behavioral steering.

---

## A-010 — A cloud service is categorically better than git-native workflows

**Domain:** Product  
**Status:** Invalidated  
**Confidence:** High — git already solves the most important coordination and confirmation needs for V0.
**Basis:** Pull requests, history, and repo-local docs are enough to test the real value proposition.

**Depends on:** Nothing upstream  
**Depended on by:** historical D-008

**Invalidated when:** already invalidated.

**If invalidated:** done; do not force a hosted product into the roadmap without new evidence.

---

## A-011 — Templates plus instructions beat a custom scanner pipeline for V0

**Domain:** Product  
**Status:** Believed  
**Confidence:** Medium — strong templates let the agent spend its effort on repo-specific reasoning.
**Basis:** The key value is document quality and maintenance, not a perfectly normalized intermediate representation.

**Depends on:** A-002, A-009  
**Depended on by:** D-027, D-029, D-032

**Invalidated when:** template-driven skill output is too inconsistent or too expensive to trust.

**If invalidated:** reconsider which parts need deterministic support.

---

## A-012 — Token efficiency is measurable enough to be a product claim

**Domain:** Product  
**Status:** Untested  
**Confidence:** Medium — users notice wasted exploration, but the metric has to be simple enough to observe.
**Basis:** Agents often burn many reads before acting. Better instructions should reduce that overhead.

**Depends on:** A-002, A-009  
**Depended on by:** D-031, BUSINESS_PLAN.md

**Invalidated when:** measurement is too noisy to compare or users do not value the improvement.

**If invalidated:** keep token efficiency as an internal optimization, not external messaging.
