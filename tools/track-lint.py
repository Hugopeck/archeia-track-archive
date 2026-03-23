#!/usr/bin/env python3
"""Track lint — CI enforcement layer for .track/ task files.

Validates schema, structure, and consistency of Track task files.
Full parity with the archived Rust validator.

Usage:
    python3 tools/track-lint.py [--track-dir .track/]

Dependencies:
    pip install pyyaml

Exit codes:
    0 — all checks pass (warnings may exist)
    1 — errors found
"""

import argparse
import os
import re
import sys
import yaml
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KNOWN_FIELDS = {
    "id", "title", "status", "mode", "priority", "type",
    "scopes", "project", "cycle", "created", "updated",
    "assigned_to", "pr", "depends_on", "cancelled_reason", "files",
}

VALID_MODES = {"investigate", "plan", "implement"}

# Legacy field — warn but don't error
LEGACY_FIELDS = {"agent_ready"}

REQUIRED_FIELDS = {
    "id", "title", "status", "mode", "priority", "type",
    "created", "updated", "depends_on",
}

REQUIRED_SECTIONS = [
    "## Context",
    "## Acceptance Criteria",
    "## Verification",
    "## Notes",
]

READY_GATE_STATUSES = {"todo", "active", "review", "done"}

CYCLE_PATTERN = re.compile(r"^\d{4}-W(0[1-9]|[1-4]\d|5[0-3])$")

FILENAME_ID_PATTERN = re.compile(r"^(\d{3,})-[a-z0-9-]+\.md$")


# ---------------------------------------------------------------------------
# Issue collection
# ---------------------------------------------------------------------------

class Issue:
    def __init__(self, path, message, severity="error"):
        self.path = path
        self.message = message
        self.severity = severity

    def __str__(self):
        prefix = "Error" if self.severity == "error" else "Warning"
        path_str = str(self.path) if self.path else "<global>"
        return f"  {prefix}: {path_str}: {self.message}"


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(track_dir):
    """Load and validate config.yaml."""
    config_path = track_dir / "config.yaml"
    if not config_path.exists():
        return None, [Issue(config_path, "config.yaml not found")]

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return None, [Issue(config_path, f"failed to parse config yaml: {e}")]

    if not isinstance(config, dict):
        return None, [Issue(config_path, "config.yaml must be a YAML mapping")]

    return config, []


# ---------------------------------------------------------------------------
# Task file parsing
# ---------------------------------------------------------------------------

def split_frontmatter(content, path):
    """Split a task file into frontmatter string and body string."""
    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None, [Issue(path, "file must start with --- frontmatter delimiter")]

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None, None, [Issue(path, "missing closing --- frontmatter delimiter")]

    fm_str = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1:])
    return fm_str, body, []


def parse_frontmatter(fm_str, path):
    """Parse YAML frontmatter string into a dict."""
    try:
        data = yaml.safe_load(fm_str)
    except yaml.YAMLError as e:
        return None, [Issue(path, f"invalid YAML in frontmatter: {e}")]

    if not isinstance(data, dict):
        return None, [Issue(path, "frontmatter must be a YAML mapping")]

    # Coerce id to zero-padded string (YAML parses unquoted 001 as int 1)
    if "id" in data and not isinstance(data["id"], str):
        data["id"] = str(data["id"]).zfill(3)

    return data, []


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

def validate_schema(fm, body, path, config):
    """Config-backed frontmatter validation."""
    issues = []

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in fm:
            issues.append(Issue(path, f"missing required field '{field}'"))

    # Unknown fields
    for field in fm:
        if field not in KNOWN_FIELDS and field not in LEGACY_FIELDS:
            issues.append(Issue(path, f"unknown field '{field}' in task frontmatter"))

    # Legacy field warning
    if "agent_ready" in fm:
        issues.append(Issue(path, "agent_ready is deprecated; remove it from task frontmatter", "warning"))

    # Status vocabulary
    statuses = [s if isinstance(s, str) else s for s in config.get("statuses", [])]
    status = fm.get("status", "")
    if status and status not in statuses:
        issues.append(Issue(path, f"status '{status}' is not enabled in config.yaml"))

    # Priority vocabulary
    priorities = config.get("priorities", [])
    priority = fm.get("priority", "")
    if priority and priority not in priorities:
        issues.append(Issue(path, f"priority '{priority}' is not enabled in config.yaml"))

    # Type vocabulary
    types = config.get("types", [])
    task_type = fm.get("type", "")
    if task_type and task_type not in types:
        issues.append(Issue(path, f"type '{task_type}' is not enabled in config.yaml"))

    # Mode vocabulary
    mode = fm.get("mode", "")
    if mode and mode not in VALID_MODES:
        issues.append(Issue(path, f"mode '{mode}' must be one of: {', '.join(sorted(VALID_MODES))}"))

    # Cycle format
    cycle = fm.get("cycle")
    if cycle and not CYCLE_PATTERN.match(str(cycle)):
        issues.append(Issue(path, f"cycle must be a valid ISO week like 2026-W11; found {cycle}"))

    # Cancelled reason
    if fm.get("status") == "cancelled":
        reason = fm.get("cancelled_reason", "")
        if not reason or (isinstance(reason, str) and not reason.strip()):
            issues.append(Issue(path, "cancelled tasks must include cancelled_reason"))

    # Scopes membership
    config_scopes = config.get("scopes", [])
    for scope in fm.get("scopes", []):
        if scope not in config_scopes:
            issues.append(Issue(path, f"scope '{scope}' is not defined in config.yaml"))

    # Project membership
    project = fm.get("project")
    config_projects = config.get("projects", {})
    if project and project not in config_projects:
        issues.append(Issue(path, f"project '{project}' is not defined in config.yaml"))

    return issues


# ---------------------------------------------------------------------------
# Structure validation
# ---------------------------------------------------------------------------

def validate_structure(fm, body, path, today=None):
    """Body-structure validation for sections, content quality, and workflow smells."""
    issues = []

    # Required H2 sections
    body_lines = body.split("\n") if body else []
    for section in REQUIRED_SECTIONS:
        if not any(line.strip() == section for line in body_lines):
            issues.append(Issue(path, f"missing required section {section}"))

    # Problem text length
    problem_text = extract_problem_text(body)
    if len(problem_text) < 20:
        issues.append(Issue(path, "Problem subsection must contain at least 20 characters of real content"))

    # Acceptance criteria
    criteria = extract_acceptance_criteria(body)
    if not criteria:
        issues.append(Issue(path, "task must include at least one acceptance criterion"))
    elif len(criteria) > 10:
        issues.append(Issue(path, f"task has {len(criteria)} acceptance criteria; consider decomposing it", "warning"))

    # Ready gate checks
    status = fm.get("status", "")
    if status in READY_GATE_STATUSES:
        affected_files = extract_subsection(body, "### Affected Files")
        if not affected_files or not affected_files.strip():
            issues.append(Issue(path, "Affected Files subsection must contain at least one path for tasks in todo, active, review, or done"))

        verification = extract_section(body, "## Verification")
        if not verification or not verification.strip():
            issues.append(Issue(path, "Verification section must contain at least one step for tasks in todo, active, review, or done"))

    # Stale active task warning
    if status == "active" and today:
        updated = fm.get("updated")
        if updated:
            if isinstance(updated, str):
                try:
                    updated_date = datetime.strptime(updated, "%Y-%m-%d").date()
                except ValueError:
                    updated_date = None
            else:
                updated_date = updated

            if updated_date:
                days_since = (today - updated_date).days
                if days_since > 5:
                    issues.append(Issue(path, "active task has gone more than 5 days without a note", "warning"))

    return issues


def extract_problem_text(body):
    """Extract Problem subsection text, stripping comments and placeholders."""
    text = extract_subsection(body, "### Problem")
    if not text:
        return ""

    # Strip HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    # Filter placeholder lines
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith("REQUIRED:") and not stripped.startswith("Optional:"):
            lines.append(stripped)

    return " ".join(lines).strip()


def extract_acceptance_criteria(body):
    """Extract acceptance criteria (checkbox items) from the body."""
    section = extract_section(body, "## Acceptance Criteria")
    if not section:
        return []

    criteria = []
    for line in section.split("\n"):
        stripped = line.strip()
        if re.match(r"^- \[[ x]\] ", stripped):
            criteria.append(stripped)

    return criteria


def extract_section(body, heading):
    """Extract content between an H2 heading and the next H2."""
    lines = body.split("\n")
    in_section = False
    content_lines = []

    for line in lines:
        if line.strip() == heading:
            in_section = True
            continue
        if in_section:
            if line.startswith("## ") and line.strip() != heading:
                break
            content_lines.append(line)

    return "\n".join(content_lines) if content_lines else ""


def extract_subsection(body, heading):
    """Extract content between an H3 heading and the next H2/H3."""
    lines = body.split("\n")
    in_section = False
    content_lines = []

    for line in lines:
        if line.strip() == heading:
            in_section = True
            continue
        if in_section:
            if re.match(r"^#{2,3} ", line):
                break
            content_lines.append(line)

    return "\n".join(content_lines) if content_lines else ""


# ---------------------------------------------------------------------------
# Consistency validation
# ---------------------------------------------------------------------------

def validate_consistency(tasks, track_dir):
    """Cross-file validation for IDs, filenames, directories, and dependencies."""
    issues = []
    known_ids = {t["fm"]["id"] for t in tasks if "id" in t["fm"]}
    tasks_by_id = {}
    for t in tasks:
        tid = t["fm"].get("id")
        if tid and tid not in tasks_by_id:
            tasks_by_id[tid] = t

    # Per-task checks
    for t in tasks:
        fm = t["fm"]
        path = t["path"]
        rel_path = t["rel_path"]

        # Status directory match
        parent_dir = Path(rel_path).parent.name
        status = fm.get("status", "")
        if parent_dir != status:
            issues.append(Issue(path, f"status directory mismatch: frontmatter says '{status}', file is under '{parent_dir}'"))

        # Filename pattern
        filename = Path(rel_path).name
        task_id = fm.get("id", "")
        expected_pattern = re.compile(rf"^{re.escape(task_id)}-[a-z0-9-]+\.md$")
        if not expected_pattern.match(filename):
            issues.append(Issue(path, f"filename must match {task_id}-{{slug}}.md"))

        # Dependency checks
        depends_on = fm.get("depends_on", [])
        if depends_on is None:
            depends_on = []

        for dep_id in depends_on:
            dep_id = str(dep_id)

            # Self-reference
            if dep_id == task_id:
                issues.append(Issue(path, f"depends_on may not reference task itself ('{dep_id}')"))

            # Missing target
            if dep_id not in known_ids:
                issues.append(Issue(path, f"depends_on references missing task '{dep_id}'"))

            # Blocker status for active/review/done
            if status in ("active", "review", "done") and dep_id in tasks_by_id:
                blocker = tasks_by_id[dep_id]
                blocker_status = blocker["fm"].get("status", "")
                if blocker_status != "done":
                    issues.append(Issue(path, f"tasks in active, review, and done require depends_on targets to be done; '{dep_id}' is {blocker_status}"))

    # Cycle detection (DFS)
    for t in tasks:
        task_id = t["fm"].get("id", "")
        cycle = find_cycle(task_id, tasks_by_id)
        if cycle:
            issues.append(Issue(t["path"], f"dependency cycle detected: {' -> '.join(cycle)}"))

    # Duplicate ID detection
    id_counts = defaultdict(list)
    for t in tasks:
        tid = t["fm"].get("id")
        if tid:
            id_counts[tid].append(t["rel_path"])

    for tid, paths in id_counts.items():
        if len(paths) > 1:
            joined = ", ".join(sorted(paths))
            for t in tasks:
                if t["fm"].get("id") == tid:
                    issues.append(Issue(t["path"], f"duplicate task id '{tid}' also appears in {joined}"))

    return issues


def find_cycle(start_id, tasks_by_id):
    """DFS-based circular dependency detection."""
    def walk(current_id, path):
        if current_id in path:
            idx = path.index(current_id)
            return path[idx:] + [current_id]

        if current_id not in tasks_by_id:
            return None

        task = tasks_by_id[current_id]
        depends_on = task["fm"].get("depends_on", [])
        if depends_on is None:
            depends_on = []

        path.append(current_id)
        for dep_id in depends_on:
            dep_id = str(dep_id)
            result = walk(dep_id, path)
            if result:
                return result
        path.pop()
        return None

    return walk(start_id, [])


# ---------------------------------------------------------------------------
# Claim validation
# ---------------------------------------------------------------------------

def validate_claims(track_dir, tasks_by_id):
    """Validate claim files in .track/claims/."""
    issues = []
    claims_dir = track_dir / "claims"

    if not claims_dir.exists():
        return issues

    now = datetime.now(timezone.utc)
    active_claims = []

    for claim_file in sorted(claims_dir.glob("*.md")):
        content = claim_file.read_text()
        fm_str, _, parse_issues = split_frontmatter(content, claim_file)

        if parse_issues:
            issues.extend(parse_issues)
            continue

        fm, parse_issues = parse_frontmatter(fm_str, claim_file)
        if parse_issues:
            issues.extend(parse_issues)
            continue

        if not fm:
            continue

        task_id = fm.get("task_id", "")

        # Claim references existing task
        if task_id and task_id not in tasks_by_id:
            issues.append(Issue(claim_file, f"claim references non-existent task '{task_id}'"))

        # Expired claim warning
        expires_at = fm.get("expires_at", "")
        if expires_at:
            try:
                if isinstance(expires_at, str):
                    expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
                else:
                    expiry = expires_at

                if expiry < now:
                    issues.append(Issue(claim_file, f"claim for task '{task_id}' has expired at {expires_at}", "warning"))
                else:
                    active_claims.append(fm)
            except (ValueError, TypeError):
                active_claims.append(fm)  # Can't parse, treat as active
        else:
            active_claims.append(fm)

    # File scope overlap between active claims
    for i, claim_a in enumerate(active_claims):
        for claim_b in active_claims[i + 1:]:
            files_a = claim_a.get("files", []) or []
            files_b = claim_b.get("files", []) or []

            if globs_overlap(files_a, files_b):
                id_a = claim_a.get("task_id", "?")
                id_b = claim_b.get("task_id", "?")
                issues.append(Issue(
                    claims_dir,
                    f"active claims for tasks '{id_a}' and '{id_b}' have overlapping file scopes"
                ))

    return issues


def globs_overlap(globs_a, globs_b):
    """Check if any pair of glob patterns could match the same file.

    Simple heuristic: strip ** suffixes and check if one path is a prefix of the other.
    """
    for a in globs_a:
        for b in globs_b:
            a_base = a.rstrip("*").rstrip("/")
            b_base = b.rstrip("*").rstrip("/")

            if not a_base or not b_base:
                return True  # Root-level glob overlaps with everything

            if a_base.startswith(b_base) or b_base.startswith(a_base):
                return True

    return False


# ---------------------------------------------------------------------------
# Task file discovery
# ---------------------------------------------------------------------------

STATUS_DIRS = ["triage", "todo", "active", "review", "done", "cancelled"]


def discover_tasks(track_dir):
    """Find and parse all task files."""
    tasks = []
    parse_issues = []

    for status_dir in STATUS_DIRS:
        dir_path = track_dir / status_dir
        if not dir_path.exists():
            continue

        for task_file in sorted(dir_path.glob("*.md")):
            if task_file.name.startswith("."):
                continue

            content = task_file.read_text()
            fm_str, body, issues = split_frontmatter(content, task_file)

            if issues:
                parse_issues.extend(issues)
                continue

            fm, issues = parse_frontmatter(fm_str, task_file)
            if issues:
                parse_issues.extend(issues)
                continue

            if not fm:
                continue

            rel_path = str(task_file.relative_to(track_dir))

            tasks.append({
                "fm": fm,
                "body": body or "",
                "path": task_file,
                "rel_path": rel_path,
            })

    return tasks, parse_issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Track lint — validate .track/ task files")
    parser.add_argument("--track-dir", default=".track", help="Path to .track/ directory")
    args = parser.parse_args()

    track_dir = Path(args.track_dir)

    if not track_dir.exists():
        print(f"Error: {track_dir} does not exist")
        sys.exit(1)

    # Load config
    config, config_issues = load_config(track_dir)
    if config_issues:
        for issue in config_issues:
            print(issue)
        sys.exit(1)

    # Discover and parse tasks
    tasks, parse_issues = discover_tasks(track_dir)

    # Build tasks_by_id for claim validation
    tasks_by_id = {}
    for t in tasks:
        tid = t["fm"].get("id")
        if tid and tid not in tasks_by_id:
            tasks_by_id[tid] = t

    # Run all validations
    all_issues = list(parse_issues)
    today = datetime.now().date()

    for t in tasks:
        all_issues.extend(validate_schema(t["fm"], t["body"], t["path"], config))
        all_issues.extend(validate_structure(t["fm"], t["body"], t["path"], today))

    all_issues.extend(validate_consistency(tasks, track_dir))
    all_issues.extend(validate_claims(track_dir, tasks_by_id))

    # Report
    errors = [i for i in all_issues if i.severity == "error"]
    warnings = [i for i in all_issues if i.severity == "warning"]

    if not all_issues:
        print(f"OK: {len(tasks)} tasks validated, no issues found")
        sys.exit(0)

    if errors:
        print(f"FAIL: {len(tasks)} tasks validated, {len(errors)} error(s), {len(warnings)} warning(s)\n")
    else:
        print(f"OK: {len(tasks)} tasks validated, {len(warnings)} warning(s)\n")

    for issue in sorted(all_issues, key=lambda i: (0 if i.severity == "error" else 1, str(i.path))):
        print(issue)

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
