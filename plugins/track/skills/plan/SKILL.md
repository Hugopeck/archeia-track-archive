---
name: track:plan
description: Create a project-level plan that decomposes into Track tasks with phases and dependencies.
---

# Track Plan

## Overview

Plan a large initiative — define scope, phases, and sequence — then create tasks via track-decompose.

## Workflow

1. Read `.track/PROTOCOL.md` if you haven't already this session.
2. Understand the project goal and decide whether the initiative deserves a new project or fits an existing one.
3. If creating a new project, take the next number from `project_counter`, add the project to `.track/config.yaml`, and initialize `task_counter` to `1`.
4. Create or update `.track/projects/{project-key}-{slug}.md` with Goal, Why Now, In Scope, Out of Scope, Shared Context, Dependency Notes, Success Definition, and Candidate Task Seeds.
5. Scope the project through the brief before creating tasks. The brief is the narrative contract; config is the machine registry.
6. Phase if large: foundation → core → integration → validation.
7. Decompose each phase using track-decompose workflow, keeping tasks aligned to the brief.
8. Present dependency graph before creating tasks.

## Response

Report: project key/title, brief path, phases, task count, max parallelism, dependency graph.
