#!/usr/bin/env python3
"""Tests for tools/track_build.py and its wrappers."""

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

spec = importlib.util.spec_from_file_location("track_build", Path(__file__).parent.parent / "track_build.py")
track_build = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = track_build
spec.loader.exec_module(track_build)


def make_task(title, status, priority, task_id, depends_on=None, project="1", files=None, mode="implement", type_="feature", updated="2026-03-01"):
    depends_on = depends_on or []
    files = files or []
    return f"""---
id: \"{task_id}\"
title: \"{title}\"
status: {status}
mode: {mode}
priority: {priority}
type: {type_}
project: {project}
created: 2026-03-01
updated: {updated}
depends_on: {json.dumps(depends_on)}
files: {json.dumps(files)}
---

## Context

### Problem
This task body is long enough to represent a realistic task.

### Cause

### Affected Files
- src/example.py

### References
- .track/projects/{project}-sample.md

## Acceptance Criteria

- [ ] Done

## Verification

- python3 -V

## Notes
"""


def make_claim(task_id, files, expires_at="2099-03-22T23:20:00Z"):
    return f"""---
task_id: \"{task_id}\"
agent: codex
claimed_at: 2026-03-22T18:00:00Z
files: {json.dumps(files)}
expires_at: {expires_at}
---
"""


def make_brief(title, goal, body_suffix=""):
    return f"""# {title}

## Goal

{goal}

## Why Now

Need this now.

## In Scope

- scope

## Out Of Scope

- out

## Shared Context

Shared context.

## Dependency Notes

Dependency notes.

## Success Definition

- success

## Candidate Task Seeds

- seed
{body_suffix}
"""


def setup_repo(tasks, projects=None, claims=None):
    tmpdir = tempfile.TemporaryDirectory()
    root = Path(tmpdir.name)
    track_dir = root / ".track"
    (track_dir / "tasks").mkdir(parents=True)
    (track_dir / "projects").mkdir(parents=True)
    claims_dir = track_dir / "tasks" / "claims"
    claims_dir.mkdir(parents=True)

    project_config = projects or {
        "1": {
            "title": "Project One",
            "description": "First project.",
            "status": "active",
            "brief": "projects/1-project-one.md",
            "task_counter": 3,
        }
    }

    config = {
        "schema_version": "0.1",
        "statuses": ["triage", "todo", "active", "review", "done", "cancelled"],
        "priorities": ["urgent", "high", "medium", "low"],
        "types": ["bug", "feature", "improvement", "debt", "infra", "spike"],
        "scopes": [],
        "projects": project_config,
        "project_counter": len(project_config),
    }
    (track_dir / "config.yaml").write_text(json.dumps(config), encoding="utf-8")

    for project_id, project in project_config.items():
        if project.get("status") == "active":
            brief_rel = project.get("brief")
            if brief_rel:
                brief_path = track_dir / brief_rel
                brief_path.parent.mkdir(parents=True, exist_ok=True)
                brief_path.write_text(
                    make_brief(project["title"], f"Goal for {project['title']}.", body_suffix=f"\nProject {project_id}.\n"),
                    encoding="utf-8",
                )

    for relative_path, content in tasks.items():
        full_path = track_dir / "tasks" / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")

    for relative_path, content in (claims or {}).items():
        full_path = claims_dir / relative_path
        full_path.write_text(content, encoding="utf-8")

    return root, track_dir, tmpdir


class TestTrackBuild:
    def test_build_succeeds_and_writes_expected_files(self):
        root, track_dir, tmpdir = setup_repo(
            tasks={
                "todo/1.1-sample.md": make_task("[Implement] Sample", "todo", "high", "1.1"),
            }
        )
        try:
            outputs = track_build.build_outputs(track_dir, root / "BOARD.md")
            assert outputs["projects"] == root / "PROJECTS.md"
            assert outputs["tasks"] == root / "TASKS.md"
            assert (root / "PROJECTS.md").exists()
            assert (root / "TASKS.md").exists()
            assert (root / "BOARD.md").exists()
            assert (track_dir / "index.json").exists()
        finally:
            tmpdir.cleanup()

    def test_projects_view_has_immediate_starts_and_summary(self):
        projects = {
            "1": {"title": "Alpha", "description": "Alpha desc.", "status": "active", "brief": "projects/1-alpha.md", "task_counter": 4},
            "2": {"title": "Beta", "description": "Beta desc.", "status": "active", "brief": "projects/2-beta.md", "task_counter": 3},
            "launch": {"title": "Launch", "description": "Archived desc.", "status": "archived"},
        }
        root, track_dir, tmpdir = setup_repo(
            tasks={
                "todo/1.2-ready.md": make_task("[Implement] Ready", "todo", "urgent", "1.2", project="1"),
                "active/1.3-active.md": make_task("[Implement] Active", "active", "high", "1.3", project="1"),
                "todo/2.1-blocked.md": make_task("[Implement] Blocked", "todo", "medium", "2.1", depends_on=["1.3"], project="2"),
                "done/2.2-done.md": make_task("[Implement] Done", "done", "low", "2.2", project="2", updated="2026-03-05"),
            },
            projects=projects,
        )
        try:
            track_build.build_outputs(track_dir, root / "BOARD.md")
            projects_md = (root / "PROJECTS.md").read_text(encoding="utf-8")
            assert "## Immediate Starts" in projects_md
            assert r"\[Implement\] Ready" in projects_md
            assert "## Portfolio Summary" not in projects_md
            assert "In Flight" in projects_md
            assert "Blocked" in projects_md
            assert "## Archived Projects" in projects_md
        finally:
            tmpdir.cleanup()

    def test_projects_view_renders_cross_project_dependencies(self):
        projects = {
            "1": {"title": "Alpha", "description": "Alpha desc.", "status": "active", "brief": "projects/1-alpha.md", "task_counter": 3},
            "2": {"title": "Beta", "description": "Beta desc.", "status": "active", "brief": "projects/2-beta.md", "task_counter": 3},
        }
        root, track_dir, tmpdir = setup_repo(
            tasks={
                "done/1.1-foundation.md": make_task("[Implement] Foundation", "done", "high", "1.1", project="1"),
                "todo/2.1-followup.md": make_task("[Implement] Follow up", "todo", "medium", "2.1", depends_on=["1.1"], project="2"),
            },
            projects=projects,
        )
        try:
            track_build.build_outputs(track_dir, root / "BOARD.md")
            projects_md = (root / "PROJECTS.md").read_text(encoding="utf-8")
            assert "## Cross-Project Dependencies" in projects_md
            assert "1 -> 2" in projects_md
        finally:
            tmpdir.cleanup()

    def test_missing_goal_excerpt_fails_for_active_project(self):
        root, track_dir, tmpdir = setup_repo(
            tasks={"todo/1.1-sample.md": make_task("[Implement] Sample", "todo", "high", "1.1")}
        )
        try:
            brief_path = track_dir / "projects" / "1-project-one.md"
            brief_path.write_text("# Project One\n\n## Goal\n\n\n## Why Now\n\nNo goal.\n", encoding="utf-8")
            try:
                track_build.build_outputs(track_dir, root / "BOARD.md")
                assert False, "expected BuildError"
            except track_build.BuildError as exc:
                assert "Goal excerpt" in str(exc)
        finally:
            tmpdir.cleanup()

    def test_tasks_view_sections_and_why_here(self):
        root, track_dir, tmpdir = setup_repo(
            tasks={
                "todo/1.1-ready.md": make_task("[Implement] Ready", "todo", "urgent", "1.1", files=["src/ready.py"]),
                "active/1.2-active.md": make_task("[Implement] Active", "active", "high", "1.2", files=["src/active.py"]),
                "review/1.3-review.md": make_task("[Implement] Review", "review", "medium", "1.3"),
                "todo/1.4-dep-blocked.md": make_task("[Implement] Dep Blocked", "todo", "high", "1.4", depends_on=["1.2"], files=["src/dep.py"]),
                "todo/1.5-claim-blocked.md": make_task("[Implement] Claim Blocked", "todo", "high", "1.5", files=["src/shared/**"]),
                "todo/1.6-both-blocked.md": make_task("[Implement] Both Blocked", "todo", "high", "1.6", depends_on=["1.2"], files=["src/shared/file.py"]),
                "triage/1.7-plan.md": make_task("[Plan] Plan", "triage", "medium", "1.7", mode="plan"),
                "done/1.8-done.md": make_task("[Implement] Done", "done", "low", "1.8", updated="2026-03-09"),
                "cancelled/1.9-cancelled.md": make_task("[Implement] Cancelled", "cancelled", "low", "1.9", updated="2026-03-08"),
                "active/2.1-owner.md": make_task("[Implement] Owner", "active", "high", "2.1", project="1", files=["src/shared/file.py"]),
            },
            claims={"2.1.md": make_claim("2.1", ["src/shared/file.py"])},
        )
        try:
            track_build.build_outputs(track_dir, root / "BOARD.md")
            tasks_md = (root / "TASKS.md").read_text(encoding="utf-8")
            assert "## Ready Now" in tasks_md
            assert "## In Flight" in tasks_md
            assert "## In Flight" in tasks_md
            assert "## Blocked" in tasks_md
            assert "## Planning" in tasks_md
            assert "## Recent Done" in tasks_md
            assert "## Cancelled" in tasks_md
            assert "1.2" in tasks_md
            assert "claim overlap with 2.1" in tasks_md
            assert "1.2 and claim overlap with 2.1" in tasks_md
        finally:
            tmpdir.cleanup()

    def test_board_view_lane_order_and_card_fields(self):
        root, track_dir, tmpdir = setup_repo(
            tasks={
                "active/1.1-active.md": make_task("[Implement] Active", "active", "high", "1.1", files=["a.py", "b.py", "c.py", "d.py"]),
                "review/1.2-review.md": make_task("[Implement] Review", "review", "high", "1.2"),
                "todo/1.3-ready.md": make_task("[Implement] Ready", "todo", "high", "1.3"),
                "todo/1.4-blocked.md": make_task("[Implement] Blocked", "todo", "medium", "1.4", depends_on=["1.1"]),
                "triage/1.5-triage.md": make_task("[Plan] Triage", "triage", "medium", "1.5", mode="plan"),
                "done/1.6-done.md": make_task("[Implement] Done", "done", "low", "1.6", updated="2026-03-04"),
            }
        )
        try:
            track_build.build_outputs(track_dir, root / "BOARD.md")
            board = (root / "BOARD.md").read_text(encoding="utf-8")
            active_pos = board.index("## Active")
            review_pos = board.index("## Review")
            ready_pos = board.index("## Ready")
            blocked_pos = board.index("## Blocked")
            triage_pos = board.index("## Triage")
            recent_done_pos = board.index("## Recently Done")
            assert active_pos < review_pos < ready_pos < blocked_pos < triage_pos < recent_done_pos
            assert r"`1.1` [\[Implement\] Active]" in board
            assert "Track Skill Pack Launch" not in board
            assert "high" in board
        finally:
            tmpdir.cleanup()

    def test_snapshot_includes_projects_and_blocking_fields(self):
        projects = {
            "1": {"title": "Alpha", "description": "Alpha desc.", "status": "active", "brief": "projects/1-alpha.md", "task_counter": 3},
            "zeta": {"title": "Zeta", "description": "Archived desc.", "status": "archived"},
        }
        root, track_dir, tmpdir = setup_repo(
            tasks={
                "active/1.1-base.md": make_task("[Implement] Base", "active", "high", "1.1", project="1", files=["src/base.py"]),
                "todo/1.2-followup.md": make_task("[Implement] Follow up", "todo", "medium", "1.2", depends_on=["1.1"], project="1", files=["src/shared/**"]),
                "active/1.3-owner.md": make_task("[Implement] Owner", "active", "high", "1.3", project="1", files=["src/shared/file.py"]),
            },
            claims={"1.3.md": make_claim("1.3", ["src/shared/file.py"])},
            projects=projects,
        )
        try:
            snapshot = track_build.build_snapshot(track_dir)
            assert "projects" in snapshot
            assert snapshot["projects"][0]["goal_excerpt"]
            followup = next(task for task in snapshot["tasks"] if task["id"] == "1.2")
            assert followup["availability_reason"] == "blocked_by_dependencies_and_claim"
            assert followup["blocking_dependencies"] == ["1.1"]
            assert followup["blocking_claim_tasks"] == ["1.3"]
        finally:
            tmpdir.cleanup()

    def test_repeated_builds_are_byte_identical(self):
        root, track_dir, tmpdir = setup_repo(
            tasks={"todo/1.1-sample.md": make_task("[Implement] Sample", "todo", "high", "1.1")}
        )
        try:
            track_build.build_outputs(track_dir, root / "BOARD.md")
            first = {
                "projects": (root / "PROJECTS.md").read_text(encoding="utf-8"),
                "tasks": (root / "TASKS.md").read_text(encoding="utf-8"),
                "board": (root / "BOARD.md").read_text(encoding="utf-8"),
                "index": (track_dir / "index.json").read_text(encoding="utf-8"),
            }
            track_build.build_outputs(track_dir, root / "BOARD.md")
            second = {
                "projects": (root / "PROJECTS.md").read_text(encoding="utf-8"),
                "tasks": (root / "TASKS.md").read_text(encoding="utf-8"),
                "board": (root / "BOARD.md").read_text(encoding="utf-8"),
                "index": (track_dir / "index.json").read_text(encoding="utf-8"),
            }
            assert first == second
        finally:
            tmpdir.cleanup()

    def test_malformed_input_does_not_partially_replace_outputs(self):
        root, track_dir, tmpdir = setup_repo(
            tasks={"todo/1.1-sample.md": make_task("[Implement] Sample", "todo", "high", "1.1")}
        )
        try:
            track_build.build_outputs(track_dir, root / "BOARD.md")
            before = {
                "projects": (root / "PROJECTS.md").read_text(encoding="utf-8"),
                "tasks": (root / "TASKS.md").read_text(encoding="utf-8"),
                "board": (root / "BOARD.md").read_text(encoding="utf-8"),
                "index": (track_dir / "index.json").read_text(encoding="utf-8"),
            }
            (track_dir / "tasks" / "todo" / "1.1-sample.md").write_text("not-frontmatter", encoding="utf-8")
            try:
                track_build.build_outputs(track_dir, root / "BOARD.md")
                assert False, "expected BuildError"
            except track_build.BuildError:
                pass
            after = {
                "projects": (root / "PROJECTS.md").read_text(encoding="utf-8"),
                "tasks": (root / "TASKS.md").read_text(encoding="utf-8"),
                "board": (root / "BOARD.md").read_text(encoding="utf-8"),
                "index": (track_dir / "index.json").read_text(encoding="utf-8"),
            }
            assert before == after
        finally:
            tmpdir.cleanup()

    def test_fingerprint_changes_when_inputs_change(self):
        root, track_dir, tmpdir = setup_repo(
            tasks={"todo/1.1-sample.md": make_task("[Implement] Sample", "todo", "high", "1.1")}
        )
        try:
            before = track_build.fingerprint_inputs(track_dir)
            (track_dir / "projects" / "1-project-one.md").write_text(make_brief("Project One", "Updated goal."), encoding="utf-8")
            after_brief = track_build.fingerprint_inputs(track_dir)
            assert before != after_brief
            (track_dir / "tasks" / "todo" / "1.1-sample.md").write_text(make_task("[Implement] Changed", "todo", "high", "1.1"), encoding="utf-8")
            after_task = track_build.fingerprint_inputs(track_dir)
            assert after_brief != after_task
            (track_dir / "config.yaml").write_text(json.dumps({"schema_version": "0.2", "projects": {}}), encoding="utf-8")
            after_config = track_build.fingerprint_inputs(track_dir)
            assert after_task != after_config
        finally:
            tmpdir.cleanup()

    def test_cli_wrapper_writes_all_views(self):
        root, track_dir, tmpdir = setup_repo(
            tasks={"todo/1.1-sample.md": make_task("[Implement] Sample", "todo", "high", "1.1")}
        )
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "track-build.py")],
                cwd=root,
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, result.stderr
            assert (root / "PROJECTS.md").exists()
            assert (root / "TASKS.md").exists()
            assert (root / "BOARD.md").exists()
            assert (track_dir / "index.json").exists()
            assert "PROJECTS.md" in result.stdout
            assert "TASKS.md" in result.stdout
        finally:
            tmpdir.cleanup()


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
