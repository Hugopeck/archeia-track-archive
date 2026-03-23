#!/usr/bin/env python3
"""Test suite for tools/track-lint.py — full parity with the archived Rust validator.

Run:
    python3 -m pytest tools/tests/test_track_lint.py -v

Or without pytest:
    python3 tools/tests/test_track_lint.py
"""

import os
import sys
import tempfile
import shutil
from datetime import date, timedelta
from pathlib import Path

# Add project root to path so we can import track-lint
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import from track_lint (we'll handle the hyphenated filename)
import importlib.util
spec = importlib.util.spec_from_file_location("track_lint", Path(__file__).parent.parent / "track-lint.py")
track_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(track_lint)


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

def make_config(scopes=None, projects=None):
    """Create a minimal valid config dict."""
    projects = projects or {}
    active_numeric_keys = []
    for key, info in projects.items():
        if str(key).isdigit() and isinstance(info, dict) and info.get("status") == "active":
            active_numeric_keys.append(int(key))

    config = {
        "schema_version": "0.1",
        "statuses": ["triage", "todo", "active", "review", "done", "cancelled"],
        "priorities": ["urgent", "high", "medium", "low"],
        "types": ["bug", "feature", "improvement", "debt", "infra", "spike"],
        "scopes": scopes or [],
        "projects": projects,
        "project_counter": (max(active_numeric_keys) + 1) if active_numeric_keys else 1,
    }
    return config


def make_task_content(fm_overrides=None, body=None):
    """Create a valid task file content string."""
    fm = {
        "id": '"1.1"',
        "title": '"[Implement] Sample task"',
        "status": "triage",
        "mode": "implement",
        "priority": "high",
        "type": "feature",
        "project": '"1"',
        "created": "2026-03-01",
        "updated": "2026-03-10",
        "depends_on": "[]",
    }
    if fm_overrides:
        fm.update(fm_overrides)

    fm_lines = "\n".join(f"{k}: {v}" for k, v in fm.items())

    if body is None:
        body = """
## Context

### Problem
This is a detailed problem description with enough content to pass validation checks.

### Cause
Root cause analysis here.

### Affected Files
- src/main.rs

### References
- docs/specs/track-spec.md

## Acceptance Criteria

- [ ] Primary outcome achieved
- [ ] Exit condition verified

## Verification

- Run the tests
- Check the output

## Notes

- 2026-03-10 human: Created task.
"""

    return f"---\n{fm_lines}\n---\n{body}"


def setup_track_dir(tasks=None, config=None, claims=None, briefs=None):
    """Create a temporary .track/ directory with tasks."""
    tmpdir = tempfile.mkdtemp()
    track_dir = Path(tmpdir) / ".track"

    for status in ["triage", "todo", "active", "review", "done", "cancelled", "claims"]:
        (track_dir / "tasks" / status).mkdir(parents=True, exist_ok=True)
    (track_dir / "projects").mkdir(parents=True, exist_ok=True)

    # Write config
    import yaml
    config = config or make_config()
    with open(track_dir / "config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    # Write tasks
    if tasks:
        for path, content in tasks.items():
            task_path = Path(path)
            if task_path.parts and task_path.parts[0] != "tasks":
                filepath = track_dir / "tasks" / task_path
            else:
                filepath = track_dir / task_path
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content)

    # Write claims
    if claims:
        for path, content in claims.items():
            filepath = track_dir / "tasks" / "claims" / path
            filepath.write_text(content)

    # Write project briefs
    if briefs:
        for path, content in briefs.items():
            filepath = track_dir / path
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content)

    return track_dir, tmpdir


def teardown(tmpdir):
    """Clean up temporary directory."""
    shutil.rmtree(tmpdir, ignore_errors=True)


def get_errors(issues):
    """Filter to error-severity issues only."""
    return [i for i in issues if i.severity == "error"]


def get_warnings(issues):
    """Filter to warning-severity issues only."""
    return [i for i in issues if i.severity == "warning"]


def has_issue_containing(issues, text):
    """Check if any issue message contains the given text."""
    return any(text in i.message for i in issues)


# ---------------------------------------------------------------------------
# Schema validation tests (parity with Rust schema.rs tests)
# ---------------------------------------------------------------------------

class TestSchemaValidation:

    def test_rejects_unknown_frontmatter_fields(self):
        fm = {"id": "001", "future_field": True, "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "unknown field 'future_field'")

    def test_validates_status_membership(self):
        fm = {"id": "001", "status": "invalid_status", "priority": "high",
              "type": "feature", "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "status 'invalid_status'")

    def test_validates_priority_membership(self):
        fm = {"id": "001", "status": "triage", "priority": "critical",
              "type": "feature", "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "priority 'critical'")

    def test_validates_type_membership(self):
        fm = {"id": "001", "status": "triage", "priority": "high",
              "type": "epic", "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "type 'epic'")

    def test_validates_cycle_format(self):
        fm = {"id": "001", "status": "triage", "priority": "high",
              "type": "feature", "cycle": "2026-13", "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "cycle")

    def test_accepts_valid_cycle(self):
        fm = {"id": "001", "status": "triage", "priority": "high",
              "type": "feature", "cycle": "2026-W11", "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert not has_issue_containing(issues, "cycle")

    def test_requires_cancelled_reason(self):
        fm = {"id": "001", "status": "cancelled", "priority": "high",
              "type": "feature", "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "cancelled_reason")

    def test_accepts_cancelled_with_reason(self):
        fm = {"id": "001", "status": "cancelled", "priority": "high",
              "type": "feature", "depends_on": [],
              "cancelled_reason": "No longer needed"}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert not has_issue_containing(issues, "cancelled_reason")

    def test_validates_scope_membership(self):
        fm = {"id": "001", "status": "triage", "priority": "high",
              "type": "feature", "scopes": ["missing"], "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "scope 'missing'")

    def test_accepts_known_scope(self):
        fm = {"id": "001", "status": "triage", "priority": "high",
              "type": "feature", "scopes": ["api"], "depends_on": []}
        config = make_config(scopes=["api"])
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert not has_issue_containing(issues, "scope")

    def test_validates_project_membership(self):
        fm = {"id": "001", "status": "triage", "priority": "high",
              "type": "feature", "project": "missing-project", "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "project 'missing-project'")

    def test_accepts_known_project(self):
        fm = {"id": "1.1", "status": "triage", "priority": "high",
              "type": "feature", "project": "1", "depends_on": []}
        config = make_config(projects={"1": {
            "title": "API v2",
            "description": "Active project.",
            "status": "active",
            "brief": "projects/1-api-v2.md",
            "task_counter": 2,
        }})
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert not has_issue_containing(issues, "project")

    def test_open_task_cannot_reference_archived_project(self):
        fm = {"id": "001", "status": "todo", "priority": "high",
              "type": "feature", "project": "legacy", "depends_on": []}
        config = make_config(projects={
            "legacy": {
                "title": "Legacy",
                "description": "Historical project.",
                "status": "archived",
            }
        })
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "archived project 'legacy'")

    def test_done_task_can_reference_archived_project(self):
        fm = {"id": "001", "status": "done", "priority": "high",
              "type": "feature", "project": "legacy", "depends_on": []}
        config = make_config(projects={
            "legacy": {
                "title": "Legacy",
                "description": "Historical project.",
                "status": "archived",
            }
        })
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert not has_issue_containing(issues, "archived project")

    def test_dotted_id_must_match_project(self):
        fm = {"id": "4.2", "status": "todo", "priority": "high",
              "type": "feature", "project": "3", "depends_on": []}
        config = make_config(projects={
            "3": {
                "title": "Query",
                "description": "Ship query path.",
                "status": "active",
                "brief": "projects/3-query.md",
                "task_counter": 3,
            }
        })
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "must match project '3'")

    def test_open_task_rejects_legacy_id(self):
        fm = {"id": "042", "status": "triage", "priority": "high",
              "type": "feature", "project": "4", "depends_on": []}
        config = make_config(projects={
            "4": {
                "title": "Launch",
                "description": "Finish launch.",
                "status": "active",
                "brief": "projects/4-launch.md",
                "task_counter": 7,
            }
        })
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "open tasks must use dotted")


# ---------------------------------------------------------------------------
# Project registry validation tests
# ---------------------------------------------------------------------------

class TestProjectRegistryValidation:

    def test_active_project_requires_brief(self):
        track_dir, tmpdir = setup_track_dir(config=make_config(projects={
            "governance": {
                "title": "Governance",
                "description": "Define repo governance.",
                "status": "active",
                "task_counter": 1,
            }
        }))
        try:
            config, _ = track_lint.load_config(track_dir)
            issues = track_lint.validate_project_registry(config, track_dir)
            assert has_issue_containing(issues, "active project 'governance' must define brief")
        finally:
            teardown(tmpdir)

    def test_missing_brief_path_fails(self):
        track_dir, tmpdir = setup_track_dir(config=make_config(projects={
            "1": {
                "title": "Governance",
                "description": "Define repo governance.",
                "status": "active",
                "brief": "projects/1-governance.md",
                "task_counter": 1,
            }
        }))
        try:
            config, _ = track_lint.load_config(track_dir)
            issues = track_lint.validate_project_registry(config, track_dir)
            assert has_issue_containing(issues, "brief file does not exist")
        finally:
            teardown(tmpdir)

    def test_brief_h1_must_match_title(self):
        brief = "# Wrong Title\n\n## Goal\n\n## Why Now\n\n## In Scope\n\n## Out Of Scope\n\n## Shared Context\n\n## Dependency Notes\n\n## Success Definition\n\n## Candidate Task Seeds\n"
        track_dir, tmpdir = setup_track_dir(
            config=make_config(projects={
                "1": {
                    "title": "Governance",
                    "description": "Define repo governance.",
                    "status": "active",
                    "brief": "projects/1-governance.md",
                    "task_counter": 1,
                }
            }),
            briefs={"projects/1-governance.md": brief},
        )
        try:
            config, _ = track_lint.load_config(track_dir)
            issues = track_lint.validate_project_registry(config, track_dir)
            assert has_issue_containing(issues, "H1 must match config title 'Governance'")
        finally:
            teardown(tmpdir)

    def test_brief_requires_all_sections(self):
        brief = "# Governance\n\n## Goal\n\n## Why Now\n\n## In Scope\n"
        track_dir, tmpdir = setup_track_dir(
            config=make_config(projects={
                "1": {
                    "title": "Governance",
                    "description": "Define repo governance.",
                    "status": "active",
                    "brief": "projects/1-governance.md",
                    "task_counter": 1,
                }
            }),
            briefs={"projects/1-governance.md": brief},
        )
        try:
            config, _ = track_lint.load_config(track_dir)
            issues = track_lint.validate_project_registry(config, track_dir)
            assert has_issue_containing(issues, "missing required section ## Out Of Scope")
        finally:
            teardown(tmpdir)

    def test_archived_project_without_brief_is_valid(self):
        track_dir, tmpdir = setup_track_dir(config=make_config(projects={
            "legacy": {
                "title": "Legacy",
                "description": "Historical project.",
                "status": "archived",
            }
        }))
        try:
            config, _ = track_lint.load_config(track_dir)
            issues = track_lint.validate_project_registry(config, track_dir)
            assert len(get_errors(issues)) == 0
        finally:
            teardown(tmpdir)

    def test_warns_on_legacy_agent_ready(self):
        fm = {"id": "001", "status": "triage", "priority": "high",
              "type": "feature", "agent_ready": True, "depends_on": []}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        warnings = get_warnings(issues)
        assert has_issue_containing(warnings, "agent_ready")

    def test_requires_depends_on_field(self):
        fm = {"id": "001", "status": "triage", "priority": "high",
              "type": "feature"}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        assert has_issue_containing(issues, "depends_on")

    def test_requires_all_required_fields(self):
        fm = {}
        config = make_config()
        issues = track_lint.validate_schema(fm, "", Path("test.md"), config)
        errors = get_errors(issues)
        for field in ["id", "title", "status", "mode", "priority", "type", "created", "updated", "depends_on"]:
            assert has_issue_containing(errors, f"'{field}'"), f"Should require field '{field}'"


# ---------------------------------------------------------------------------
# Structure validation tests (parity with Rust structure.rs tests)
# ---------------------------------------------------------------------------

class TestStructureValidation:

    def test_detects_missing_sections(self):
        fm = {"status": "triage"}
        body = "## Context\n\n### Problem\nshort\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert has_issue_containing(issues, "## Acceptance Criteria")
        assert has_issue_containing(issues, "## Verification")
        assert has_issue_containing(issues, "## Notes")

    def test_detects_short_problem(self):
        fm = {"status": "triage"}
        body = "## Context\n\n### Problem\nshort\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n- check\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert has_issue_containing(issues, "Problem")

    def test_accepts_long_enough_problem(self):
        fm = {"status": "triage"}
        body = "## Context\n\n### Problem\nThis is a detailed problem description with enough content.\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n- check\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert not has_issue_containing(issues, "Problem")

    def test_strips_comments_from_problem(self):
        fm = {"status": "triage"}
        body = "## Context\n\n### Problem\n<!-- ignore this -->\nActual problem text is long enough to validate.\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n- check\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert not has_issue_containing(issues, "Problem")

    def test_strips_placeholders_from_problem(self):
        fm = {"status": "triage"}
        body = "## Context\n\n### Problem\nREQUIRED: Fill this in\nOptional: more context\nActual problem text is definitely long enough.\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n- check\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert not has_issue_containing(issues, "Problem")

    def test_requires_acceptance_criteria(self):
        fm = {"status": "triage"}
        body = "## Context\n\n### Problem\nDetailed problem with enough content here.\n\n## Acceptance Criteria\n\n## Verification\n\n- check\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert has_issue_containing(issues, "acceptance criterion")

    def test_warns_many_acceptance_criteria(self):
        fm = {"status": "triage"}
        criteria = "\n".join(f"- [ ] Criterion {i}" for i in range(11))
        body = f"## Context\n\n### Problem\nDetailed problem with enough content here.\n\n## Acceptance Criteria\n\n{criteria}\n\n## Verification\n\n- check\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        warnings = get_warnings(issues)
        assert has_issue_containing(warnings, "11 acceptance criteria")

    def test_requires_affected_files_for_todo(self):
        fm = {"status": "todo"}
        body = "## Context\n\n### Problem\nDetailed problem with enough content here.\n\n### Affected Files\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n- check\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert has_issue_containing(issues, "Affected Files")

    def test_does_not_require_affected_files_for_triage(self):
        fm = {"status": "triage"}
        body = "## Context\n\n### Problem\nDetailed problem with enough content here.\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n- check\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert not has_issue_containing(issues, "Affected Files")

    def test_requires_verification_for_todo(self):
        fm = {"status": "todo"}
        body = "## Context\n\n### Problem\nDetailed problem with enough content here.\n\n### Affected Files\n- src/main.rs\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert has_issue_containing(issues, "Verification")

    def test_does_not_require_verification_for_triage(self):
        fm = {"status": "triage"}
        body = "## Context\n\n### Problem\nDetailed problem with enough content here.\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n## Notes\n"
        issues = track_lint.validate_structure(fm, body, Path("test.md"))
        assert not has_issue_containing(issues, "Verification section must")

    def test_warns_stale_active_task(self):
        fm = {"status": "active", "updated": "2026-03-01"}
        body = "## Context\n\n### Problem\nDetailed problem with enough content here.\n\n### Affected Files\n- src/main.rs\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n- check\n\n## Notes\n"
        today = date(2026, 3, 15)
        issues = track_lint.validate_structure(fm, body, Path("test.md"), today)
        warnings = get_warnings(issues)
        assert has_issue_containing(warnings, "5 days without a note")

    def test_no_stale_warning_when_recent(self):
        fm = {"status": "active", "updated": "2026-03-14"}
        body = "## Context\n\n### Problem\nDetailed problem with enough content here.\n\n### Affected Files\n- src/main.rs\n\n## Acceptance Criteria\n\n- [ ] one\n\n## Verification\n\n- check\n\n## Notes\n"
        today = date(2026, 3, 15)
        issues = track_lint.validate_structure(fm, body, Path("test.md"), today)
        warnings = get_warnings(issues)
        assert not has_issue_containing(warnings, "5 days")


# ---------------------------------------------------------------------------
# Consistency validation tests (parity with Rust consistency.rs tests)
# ---------------------------------------------------------------------------

class TestConsistencyValidation:

    def test_detects_status_directory_mismatch(self):
        tasks = [{"fm": {"id": "001", "status": "todo", "depends_on": []},
                  "body": "", "path": Path(".track/tasks/active/001-test.md"),
                  "rel_path": "active/001-test.md"}]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert has_issue_containing(issues, "directory mismatch")

    def test_detects_bad_filename(self):
        tasks = [{"fm": {"id": "001", "status": "todo", "depends_on": []},
                  "body": "", "path": Path(".track/tasks/todo/001-Bad_Slug.md"),
                  "rel_path": "todo/001-Bad_Slug.md"}]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert has_issue_containing(issues, "filename must match")

    def test_accepts_good_filename(self):
        tasks = [{"fm": {"id": "001", "status": "todo", "depends_on": []},
                  "body": "", "path": Path(".track/tasks/todo/001-good-slug.md"),
                  "rel_path": "todo/001-good-slug.md"}]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert not has_issue_containing(issues, "filename must match")

    def test_detects_missing_dependency(self):
        tasks = [{"fm": {"id": "001", "status": "triage", "depends_on": ["999"]},
                  "body": "", "path": Path(".track/tasks/triage/001-test.md"),
                  "rel_path": "triage/001-test.md"}]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert has_issue_containing(issues, "missing task '999'")

    def test_detects_self_reference(self):
        tasks = [{"fm": {"id": "001", "status": "triage", "depends_on": ["001"]},
                  "body": "", "path": Path(".track/tasks/triage/001-test.md"),
                  "rel_path": "triage/001-test.md"}]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert has_issue_containing(issues, "may not reference task itself")

    def test_detects_duplicate_ids(self):
        tasks = [
            {"fm": {"id": "001", "status": "todo", "depends_on": []},
             "body": "", "path": Path(".track/tasks/todo/001-first.md"),
             "rel_path": "todo/001-first.md"},
            {"fm": {"id": "001", "status": "triage", "depends_on": []},
             "body": "", "path": Path(".track/tasks/triage/001-second.md"),
             "rel_path": "triage/001-second.md"},
        ]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert has_issue_containing(issues, "duplicate task id '001'")

    def test_detects_simple_cycle(self):
        tasks = [
            {"fm": {"id": "001", "status": "triage", "depends_on": ["002"]},
             "body": "", "path": Path(".track/tasks/triage/001-a.md"),
             "rel_path": "triage/001-a.md"},
            {"fm": {"id": "002", "status": "triage", "depends_on": ["001"]},
             "body": "", "path": Path(".track/tasks/triage/002-b.md"),
             "rel_path": "triage/002-b.md"},
        ]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert has_issue_containing(issues, "dependency cycle")

    def test_detects_three_node_cycle(self):
        tasks = [
            {"fm": {"id": "001", "status": "triage", "depends_on": ["002"]},
             "body": "", "path": Path(".track/tasks/triage/001-a.md"),
             "rel_path": "triage/001-a.md"},
            {"fm": {"id": "002", "status": "triage", "depends_on": ["003"]},
             "body": "", "path": Path(".track/tasks/triage/002-b.md"),
             "rel_path": "triage/002-b.md"},
            {"fm": {"id": "003", "status": "triage", "depends_on": ["001"]},
             "body": "", "path": Path(".track/tasks/triage/003-c.md"),
             "rel_path": "triage/003-c.md"},
        ]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert has_issue_containing(issues, "dependency cycle")

    def test_no_cycle_in_dag(self):
        tasks = [
            {"fm": {"id": "001", "status": "triage", "depends_on": []},
             "body": "", "path": Path(".track/tasks/triage/001-a.md"),
             "rel_path": "triage/001-a.md"},
            {"fm": {"id": "002", "status": "triage", "depends_on": ["001"]},
             "body": "", "path": Path(".track/tasks/triage/002-b.md"),
             "rel_path": "triage/002-b.md"},
            {"fm": {"id": "003", "status": "triage", "depends_on": ["001", "002"]},
             "body": "", "path": Path(".track/tasks/triage/003-c.md"),
             "rel_path": "triage/003-c.md"},
        ]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert not has_issue_containing(issues, "cycle")

    def test_active_task_requires_done_blockers(self):
        tasks = [
            {"fm": {"id": "001", "status": "todo", "depends_on": []},
             "body": "", "path": Path(".track/tasks/todo/001-a.md"),
             "rel_path": "todo/001-a.md"},
            {"fm": {"id": "002", "status": "active", "depends_on": ["001"]},
             "body": "", "path": Path(".track/tasks/active/002-b.md"),
             "rel_path": "active/002-b.md"},
        ]
        issues = track_lint.validate_consistency(tasks, Path(".track"))
        assert has_issue_containing(issues, "depends_on targets to be done")


# ---------------------------------------------------------------------------
# Claim validation tests
# ---------------------------------------------------------------------------

class TestClaimValidation:

    def test_detects_orphaned_claim(self):
        track_dir, tmpdir = setup_track_dir(
            claims={
                "999.md": "---\ntask_id: '999'\nagent: test\nclaimed_at: '2026-03-22T10:00:00Z'\nexpires_at: '2026-03-22T23:00:00Z'\n---\n"
            }
        )
        try:
            issues = track_lint.validate_claims(track_dir, {})
            assert has_issue_containing(issues, "non-existent task '999'")
        finally:
            teardown(tmpdir)

    def test_warns_expired_claim(self):
        track_dir, tmpdir = setup_track_dir(
            claims={
                "001.md": "---\ntask_id: '001'\nagent: test\nclaimed_at: '2020-01-01T10:00:00Z'\nexpires_at: '2020-01-01T16:00:00Z'\n---\n"
            }
        )
        try:
            issues = track_lint.validate_claims(track_dir, {"001": {"fm": {"id": "001"}}})
            warnings = get_warnings(issues)
            assert has_issue_containing(warnings, "expired")
        finally:
            teardown(tmpdir)

    def test_detects_scope_overlap(self):
        track_dir, tmpdir = setup_track_dir(
            claims={
                "001.md": "---\ntask_id: '001'\nagent: agent-a\nclaimed_at: '2026-03-22T10:00:00Z'\nfiles:\n  - 'src/auth/**'\nexpires_at: '2099-01-01T00:00:00Z'\n---\n",
                "002.md": "---\ntask_id: '002'\nagent: agent-b\nclaimed_at: '2026-03-22T10:00:00Z'\nfiles:\n  - 'src/auth/login.rs'\nexpires_at: '2099-01-01T00:00:00Z'\n---\n",
            }
        )
        try:
            tasks_by_id = {"001": {"fm": {"id": "001"}}, "002": {"fm": {"id": "002"}}}
            issues = track_lint.validate_claims(track_dir, tasks_by_id)
            assert has_issue_containing(issues, "overlapping file scopes")
        finally:
            teardown(tmpdir)

    def test_no_overlap_different_dirs(self):
        track_dir, tmpdir = setup_track_dir(
            claims={
                "001.md": "---\ntask_id: '001'\nagent: agent-a\nclaimed_at: '2026-03-22T10:00:00Z'\nfiles:\n  - 'src/auth/**'\nexpires_at: '2099-01-01T00:00:00Z'\n---\n",
                "002.md": "---\ntask_id: '002'\nagent: agent-b\nclaimed_at: '2026-03-22T10:00:00Z'\nfiles:\n  - 'src/db/**'\nexpires_at: '2099-01-01T00:00:00Z'\n---\n",
            }
        )
        try:
            tasks_by_id = {"001": {"fm": {"id": "001"}}, "002": {"fm": {"id": "002"}}}
            issues = track_lint.validate_claims(track_dir, tasks_by_id)
            assert not has_issue_containing(issues, "overlapping")
        finally:
            teardown(tmpdir)


# ---------------------------------------------------------------------------
# Glob overlap tests
# ---------------------------------------------------------------------------

class TestGlobOverlap:

    def test_parent_child_overlap(self):
        assert track_lint.globs_overlap(["src/**"], ["src/auth/**"])

    def test_same_path_overlaps(self):
        assert track_lint.globs_overlap(["src/auth/**"], ["src/auth/**"])

    def test_different_dirs_no_overlap(self):
        assert not track_lint.globs_overlap(["src/auth/**"], ["src/db/**"])

    def test_root_glob_overlaps_everything(self):
        assert track_lint.globs_overlap(["**"], ["src/auth/**"])

    def test_empty_globs_no_overlap(self):
        assert not track_lint.globs_overlap([], ["src/**"])
        assert not track_lint.globs_overlap(["src/**"], [])
        assert not track_lint.globs_overlap([], [])


# ---------------------------------------------------------------------------
# Integration tests (end-to-end with real files)
# ---------------------------------------------------------------------------

class TestIntegration:

    def test_valid_task_passes(self):
        content = make_task_content()
        config = make_config(projects={
            "1": {
                "title": "Project One",
                "description": "A valid active project.",
                "status": "active",
                "brief": "projects/1-project-one.md",
                "task_counter": 2,
            }
        })
        track_dir, tmpdir = setup_track_dir(
            tasks={"triage/1.1-sample.md": content},
            config=config,
            briefs={
                "projects/1-project-one.md": "# Project One\n\n## Goal\n\n## Why Now\n\n## In Scope\n\n## Out Of Scope\n\n## Shared Context\n\n## Dependency Notes\n\n## Success Definition\n\n## Candidate Task Seeds\n"
            },
        )
        try:
            tasks, parse_issues = track_lint.discover_tasks(track_dir)
            assert len(tasks) == 1
            assert len(parse_issues) == 0

            all_issues = []
            all_issues.extend(track_lint.validate_project_registry(config, track_dir))
            for t in tasks:
                all_issues.extend(track_lint.validate_schema(t["fm"], t["body"], t["path"], config))
                all_issues.extend(track_lint.validate_structure(t["fm"], t["body"], t["path"]))
            all_issues.extend(track_lint.validate_consistency(tasks, track_dir))

            errors = get_errors(all_issues)
            assert len(errors) == 0, f"Unexpected errors: {[str(e) for e in errors]}"
        finally:
            teardown(tmpdir)

    def test_invalid_frontmatter_fails(self):
        content = "---\nid: 1.1\nproject: '1'\n---\n## Context\n"
        track_dir, tmpdir = setup_track_dir(
            tasks={"triage/1.1-bad.md": content},
            config=make_config(projects={
                "1": {
                    "title": "Project One",
                    "description": "A valid active project.",
                    "status": "active",
                    "brief": "projects/1-project-one.md",
                    "task_counter": 2,
                }
            }),
            briefs={
                "projects/1-project-one.md": "# Project One\n\n## Goal\n\n## Why Now\n\n## In Scope\n\n## Out Of Scope\n\n## Shared Context\n\n## Dependency Notes\n\n## Success Definition\n\n## Candidate Task Seeds\n"
            },
        )
        try:
            tasks, parse_issues = track_lint.discover_tasks(track_dir)
            config = make_config(projects={
                "1": {
                    "title": "Project One",
                    "description": "A valid active project.",
                    "status": "active",
                    "brief": "projects/1-project-one.md",
                    "task_counter": 2,
                }
            })
            all_issues = list(parse_issues)
            all_issues.extend(track_lint.validate_project_registry(config, track_dir))
            for t in tasks:
                all_issues.extend(track_lint.validate_schema(t["fm"], t["body"], t["path"], config))
                all_issues.extend(track_lint.validate_structure(t["fm"], t["body"], t["path"]))
            errors = get_errors(all_issues)
            assert len(errors) > 0
        finally:
            teardown(tmpdir)

    def test_existing_track_dir_passes(self):
        """Test against the real .track/ directory in this repo."""
        track_dir = Path(__file__).parent.parent.parent / ".track"
        if not track_dir.exists():
            return  # Skip if not running from repo root

        config, config_issues = track_lint.load_config(track_dir)
        assert len(config_issues) == 0, f"Config issues: {config_issues}"

        tasks, parse_issues = track_lint.discover_tasks(track_dir)
        assert len(parse_issues) == 0, f"Parse issues: {parse_issues}"

        all_issues = []
        all_issues.extend(track_lint.validate_project_registry(config, track_dir))
        for t in tasks:
            all_issues.extend(track_lint.validate_schema(t["fm"], t["body"], t["path"], config))
            all_issues.extend(track_lint.validate_structure(t["fm"], t["body"], t["path"]))
        all_issues.extend(track_lint.validate_consistency(tasks, track_dir))

        errors = get_errors(all_issues)
        assert len(errors) == 0, f"Errors in real .track/: {[str(e) for e in errors]}"


# ---------------------------------------------------------------------------
# Problem text extraction tests
# ---------------------------------------------------------------------------

class TestProblemExtraction:

    def test_extracts_simple_problem(self):
        body = "## Context\n\n### Problem\nThis is the problem.\n\n### Cause\nSomething.\n"
        text = track_lint.extract_problem_text(body)
        assert text == "This is the problem."

    def test_strips_html_comments(self):
        body = "## Context\n\n### Problem\n<!-- ignore -->\nActual content here.\n\n### Cause\n"
        text = track_lint.extract_problem_text(body)
        assert "ignore" not in text
        assert "Actual content" in text

    def test_strips_placeholder_lines(self):
        body = "## Context\n\n### Problem\nREQUIRED: Fill this\nOptional: More\nReal content here.\n\n### Cause\n"
        text = track_lint.extract_problem_text(body)
        assert "REQUIRED" not in text
        assert "Optional" not in text
        assert "Real content" in text


# ---------------------------------------------------------------------------
# Run tests without pytest
# ---------------------------------------------------------------------------

def run_tests():
    """Simple test runner for environments without pytest."""
    test_classes = [
        TestSchemaValidation,
        TestStructureValidation,
        TestProjectRegistryValidation,
        TestConsistencyValidation,
        TestClaimValidation,
        TestGlobOverlap,
        TestIntegration,
        TestProblemExtraction,
    ]

    total = 0
    passed = 0
    failed = 0

    for cls in test_classes:
        instance = cls()
        for name in dir(instance):
            if not name.startswith("test_"):
                continue
            total += 1
            try:
                getattr(instance, name)()
                passed += 1
                print(f"  PASS: {cls.__name__}.{name}")
            except Exception as e:
                failed += 1
                print(f"  FAIL: {cls.__name__}.{name}: {e}")

    print(f"\n{total} tests, {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
