# Business Plan

## The Problem

Teams are starting to rely on agent instructions such as `AGENTS.md` and `CLAUDE.md`, but those files rot quickly. Once stale, they become worse than missing because they confidently steer the agent in the wrong direction.

The pain is not "generate architecture docs once." The pain is "keep the instructions the agent actually reads accurate over time."

## Value Proposition

Archeia helps a repo keep its architecture guidance current.

Core promise:
- generate a usable knowledge base quickly
- turn that into agent-facing instruction files
- keep those files maintained as the codebase changes

If this works, the user gets better agent behavior every day, not just a one-time report.

## Why This Product Shape

The V0 product is intentionally small:
- two skills: `/archeia` and `/archeia-ask`
- markdown templates
- git-native maintenance workflows

This keeps build cost at $0, operating cost at $0, and iteration speed high. It also aligns with where the user already is: inside an agent session with read, grep, glob, and shell access.

## Revenue Model — Honest Assessment

The original cloud story was weaker than it looked. Git already gives us:
- version history
- review flows
- diff-based confirmation
- team distribution
- rollback

That means a hosted sync layer is not automatically valuable. A cloud service may exist later, but it is not the obvious business model today and should not be treated as inevitable.

## What Might Actually Make Money (Unresolved)

None of these are commitments. They are plausible paths worth watching.

1. Managed doc-drift automation for organizations that want policy and review controls
2. Premium template packs for specific stacks or compliance-heavy environments
3. Repo portfolio reporting for teams running many codebases
4. Hosted evaluation and benchmarking for architecture quality over time
5. Consulting/advisory built around migration and enforcement patterns

V0 does not need any of these to prove value.

## Testable Claims

Two claims are worth testing immediately:

### 1. Token efficiency

Archeia should reduce wasted exploration before first useful action. A practical measure is the number of tool calls or file reads before the agent does something materially useful.

### 2. Parallel agent alignment

When multiple agents work in parallel, shared repo instructions should reduce contradictory choices and repeated discovery work. If one good `AGENTS.md` helps every parallel workspace, the benefit multiplies.

## Distribution

Distribution is git-native and agent-native:
- commit the generated docs
- let teammates and future agents inherit them by cloning the repo
- optionally add a GitHub Action and PR template so maintenance happens in the repo's normal workflow

This is simpler than trying to build a separate distribution network.

## Month 1 Plan

Success in month 1 is not 1,000 repos.

Success is:
- 5 real users
- 5 real repositories
- repeated use after the first run
- at least a few examples where the docs stayed useful as the repo changed

The goal is proof of pain and proof of retention, not top-of-funnel vanity.

## Month 2-6 Focus

If month 1 works, the next questions are:
- Which maintenance mode users prefer: inline updates, drift-to-PR, or scheduled GitHub Action?
- Which template outputs matter most?
- Whether `/archeia-ask` becomes a daily tool or only a bootstrap aid
- Whether token-efficiency gains are visible enough to message clearly

No projections beyond month 6 belong here yet.

## Economics

V0 should cost $0 to build and $0 to operate beyond the founder's time.

That constraint is a feature. It forces the product toward a shape that is honest, simple, and easy to test with real users.

## Risks

The main risks are:
- agents may not follow instruction files reliably enough
- users may value initial generation but not maintenance
- manual review burden may still feel too high
- the perceived pain may be narrower than expected

## Decision Rule

Keep investing only if real users come back because the maintained instruction files change how their agents behave.

If the product only produces a nice first report, that is not enough.
