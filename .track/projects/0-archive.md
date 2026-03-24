# Archive

## Goal

Provide a stable project bucket for historical Track tasks that predate the
current flat-task, `project_id`-based model.

## Why Now

Legacy completed and cancelled tasks still carry useful history, but they should
not block or distort active project planning.

## In Scope

- legacy numeric archived tasks
- historical references from prior Track iterations
- preserving task IDs and notes for traceability

## Out Of Scope

- reopening archived work automatically
- assigning new active work to the archive project
- changing historical task narratives unless needed for schema migration

## Shared Context

The archive project exists so the repo can keep useful history without carrying
forward old project registry formats or workflow assumptions.

## Dependency Notes

Archive tasks may still appear in `depends_on` chains for historical context,
but they should not receive new open work.

## Success Definition

- legacy done/cancelled tasks validate under the new schema
- historical task IDs remain stable
- active planning does not depend on resurrecting archived project metadata

## Candidate Task Seeds

- none; this project is historical only
