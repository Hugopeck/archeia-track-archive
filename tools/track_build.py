#!/usr/bin/env python3
"""Deterministic local Track derived-view builder.

Builds the machine-readable `.track/index.json` snapshot plus the repo-root
`PROJECTS.md`, `TASKS.md`, and `BOARD.md` views from canonical Track state.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

STATUS_DIRS = ["triage", "todo", "active", "review", "done", "cancelled"]
OPEN_STATUSES = {"triage", "todo", "active", "review"}
PROJECT_STATE_LABELS = {
    "in_flight": "In Flight",
    "ready": "Ready",
    "blocked": "Blocked",
    "planning": "Planning",
    "complete": "Complete",
    "archived": "Archived",
}
PROJECT_STATE_ORDER = {
    "in_flight": 0,
    "ready": 1,
    "blocked": 2,
    "planning": 3,
    "complete": 4,
    "archived": 5,
}
BOARD_LANES = [
    ("active", "Active", "currently being worked"),
    ("review", "Review", "waiting on review/merge/confirmation"),
    ("ready", "Ready", "available to claim now"),
    ("blocked", "Blocked", "todo but blocked by deps or claim overlap"),
    ("triage", "Triage", "not yet ready to work"),
    ("recent_done", "Recently Done", "most recent completed work"),
]
PRIORITY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
OPEN_STATUS_DISPLAY_ORDER = {"active": 0, "review": 1, "ready": 2, "blocked": 3, "triage": 4}
DOTTED_TASK_ID_PATTERN = re.compile(r"^(\d+)\.(\d+)$")
NUMERIC_TASK_ID_PATTERN = re.compile(r"^(\d+)$")
HEADING_PATTERN = re.compile(r"^##\s+(.*)$")


class BuildError(Exception):
    """Raised when Track data cannot be rendered into derived views."""


@dataclass
class TaskRecord:
    path: Path
    status_dir: str
    frontmatter: dict[str, Any]
    body: str


@dataclass
class ClaimRecord:
    path: Path
    frontmatter: dict[str, Any]


def split_frontmatter(content: str, path: Path) -> tuple[str, str]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise BuildError(f"{path}: missing opening frontmatter delimiter")

    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break

    if closing is None:
        raise BuildError(f"{path}: missing closing frontmatter delimiter")

    frontmatter = "\n".join(lines[1:closing])
    body = "\n".join(lines[closing + 1 :])
    return frontmatter, body


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except yaml.YAMLError as exc:
        raise BuildError(f"{path}: failed to parse yaml: {exc}") from exc

    if not isinstance(data, dict):
        raise BuildError(f"{path}: expected a YAML mapping")

    return data


def load_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise BuildError(f"{path}: failed to read file: {exc}") from exc

    frontmatter_raw, body = split_frontmatter(content, path)
    try:
        frontmatter = yaml.safe_load(frontmatter_raw) or {}
    except yaml.YAMLError as exc:
        raise BuildError(f"{path}: failed to parse frontmatter yaml: {exc}") from exc

    if not isinstance(frontmatter, dict):
        raise BuildError(f"{path}: expected frontmatter to be a YAML mapping")

    return frontmatter, body


def load_config(track_dir: Path) -> dict[str, Any]:
    config_path = track_dir / "config.yaml"
    if not config_path.exists():
        raise BuildError(f"{config_path}: config.yaml not found")
    return load_yaml_mapping(config_path)


def discover_tasks(track_dir: Path) -> list[TaskRecord]:
    tasks_root = track_dir / "tasks"
    task_records: list[TaskRecord] = []

    for status_dir in STATUS_DIRS:
        status_path = tasks_root / status_dir
        if not status_path.exists():
            continue
        for task_path in sorted(status_path.glob("*.md")):
            if task_path.name.startswith("."):
                continue
            frontmatter, body = load_frontmatter(task_path)
            task_records.append(TaskRecord(task_path, status_dir, frontmatter, body))

    return task_records


def discover_claims(track_dir: Path) -> list[ClaimRecord]:
    claims_dir = track_dir / "tasks" / "claims"
    if not claims_dir.exists():
        return []

    claims: list[ClaimRecord] = []
    for claim_path in sorted(claims_dir.glob("*.md")):
        if claim_path.name.startswith("."):
            continue
        frontmatter, _body = load_frontmatter(claim_path)
        claims.append(ClaimRecord(claim_path, frontmatter))
    return claims


def normalize_depends_on(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if not isinstance(value, list):
        raise BuildError("depends_on must be a list")
    return [str(item) for item in value]


def files_globs(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if not isinstance(value, list):
        raise BuildError("files must be a list")
    return [str(item) for item in value]


def parse_iso_datetime(value: Any, path: Path) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        normalized = value.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError as exc:
            raise BuildError(f"{path}: invalid datetime '{value}'") from exc
    else:
        raise BuildError(f"{path}: expected datetime string, got {type(value).__name__}")
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_updated_sort_value(value: Any) -> tuple[int, str]:
    if not value:
        return (0, "")
    text = str(value)
    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return (1, parsed.astimezone(timezone.utc).isoformat())
    except ValueError:
        pass
    return (1, text)


def glob_base(glob: str) -> str:
    return glob.rstrip("*").rstrip("/")


def globs_overlap(globs_a: list[str], globs_b: list[str]) -> bool:
    if not globs_a or not globs_b:
        return False
    for left in globs_a:
        for right in globs_b:
            left_base = glob_base(left)
            right_base = glob_base(right)
            if not left_base or not right_base:
                return True
            if left_base.startswith(right_base) or right_base.startswith(left_base):
                return True
    return False


def task_id_sort_key(task_id: str) -> tuple[int, int, str]:
    dotted = DOTTED_TASK_ID_PATTERN.match(task_id)
    if dotted:
        return (0, int(dotted.group(1)) * 100000 + int(dotted.group(2)), task_id)
    numeric = NUMERIC_TASK_ID_PATTERN.match(task_id)
    if numeric:
        return (1, int(numeric.group(1)), task_id)
    return (2, 0, task_id)


def project_id_sort_key(project_id: str) -> tuple[int, int, str]:
    numeric = NUMERIC_TASK_ID_PATTERN.match(project_id)
    if numeric:
        return (0, int(numeric.group(1)), project_id)
    return (1, 0, project_id)


def task_priority_sort_key(record: dict[str, Any]) -> tuple[int, tuple[int, int, str]]:
    priority = str(record.get("priority", "low"))
    return (PRIORITY_ORDER.get(priority, 99), task_id_sort_key(str(record.get("id", ""))))


def updated_desc_sort_key(record: dict[str, Any]) -> tuple[tuple[int, str], tuple[int, int, str]]:
    return (parse_updated_sort_value(record.get("updated")), task_id_sort_key(str(record.get("id", ""))))


def claim_is_expired(claim: ClaimRecord, now: datetime) -> bool:
    expires_at = claim.frontmatter.get("expires_at")
    if not expires_at:
        return False
    return parse_iso_datetime(expires_at, claim.path) <= now


def markdown_escape(text: Any) -> str:
    value = str(text)
    value = value.replace("\\", "\\\\")
    value = value.replace("[", "\\[").replace("]", "\\]")
    return value.replace("|", "\\|")


def root_relative_path(root_dir: Path, path: Path) -> str:
    return str(path.relative_to(root_dir))


def link(text: str, path: str) -> str:
    return f"[{markdown_escape(text)}]({path})"


def render_generated_header(title: str) -> list[str]:
    return [
        f"# {title}",
        "",
        "> Generated from `.track/` canonical state. Do not edit directly. Rebuild with `bash scripts/track-build.sh`.",
        "",
        "[Projects](PROJECTS.md) | [Tasks](TASKS.md) | [Kanban](BOARD.md)",
        "",
    ]


def extract_goal_excerpt(brief_path: Path) -> str:
    try:
        content = brief_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise BuildError(f"{brief_path}: failed to read project brief: {exc}") from exc

    lines = content.splitlines()
    in_goal = False
    goal_lines: list[str] = []
    for line in lines:
        heading = HEADING_PATTERN.match(line)
        if heading:
            heading_text = heading.group(1).strip().lower()
            if heading_text == "goal":
                in_goal = True
                continue
            if in_goal:
                break
        if in_goal:
            goal_lines.append(line)

    paragraphs: list[str] = []
    current: list[str] = []
    for line in goal_lines:
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            continue
        current.append(stripped)
    if current:
        paragraphs.append(" ".join(current).strip())

    for paragraph in paragraphs:
        if paragraph:
            return paragraph
    raise BuildError(f"{brief_path}: missing non-empty Goal excerpt")


def derive_project_state(project_status: str, summary: dict[str, int]) -> str:
    if project_status == "archived":
        return "archived"
    if summary["active"] + summary["review"] > 0:
        return "in_flight"
    if summary["ready"] > 0:
        return "ready"
    if summary["blocked"] > 0:
        return "blocked"
    if summary["open"] == 0 and summary["done"] > 0:
        return "complete"
    return "planning"


def availability_reason(task: dict[str, Any]) -> str:
    if task["status_dir"] != "todo":
        return "not_todo"
    has_dependencies = bool(task["blocking_dependencies"])
    has_claims = bool(task["blocking_claim_tasks"])
    if has_dependencies and has_claims:
        return "blocked_by_dependencies_and_claim"
    if has_dependencies:
        return "blocked_by_dependencies"
    if has_claims:
        return "blocked_by_claim"
    return "ready"


def why_here(task: dict[str, Any]) -> str:
    status_dir = task["status_dir"]
    if status_dir == "active":
        return "in progress"
    if status_dir == "review":
        return "awaiting review"
    if status_dir == "triage":
        return "needs planning"
    if status_dir == "done":
        return "completed"
    if status_dir == "cancelled":
        return "cancelled"
    if task["availability_reason"] == "ready":
        return "ready"
    dependency_text = ", ".join(task["blocking_dependencies"])
    claim_text = ", ".join(task["blocking_claim_tasks"])
    if task["availability_reason"] == "blocked_by_dependencies":
        return f"blocked by {dependency_text}"
    if task["availability_reason"] == "blocked_by_claim":
        return f"blocked by claim overlap with {claim_text}"
    return f"blocked by {dependency_text} and claim overlap with {claim_text}"


def task_project_label(task: dict[str, Any]) -> str:
    project = task.get("project")
    title = task.get("project_title")
    if project and title and title != project:
        return f"{project} — {title}"
    return str(title or project or "—")


def task_project_ref(task: dict[str, Any]) -> str:
    label = task_project_label(task)
    if task.get("project_brief_path"):
        return link(label, str(task["project_brief_path"]))
    return markdown_escape(label)


def open_task_status(task: dict[str, Any]) -> str:
    if task["status_dir"] == "active":
        return "active"
    if task["status_dir"] == "review":
        return "review"
    if task["status_dir"] == "triage":
        return "triage"
    if task["status_dir"] == "todo" and task["available"]:
        return "ready"
    return "blocked"


def open_task_sort_key(task: dict[str, Any]) -> tuple[int, int, tuple[int, int, str]]:
    status_key = OPEN_STATUS_DISPLAY_ORDER[open_task_status(task)]
    priority = PRIORITY_ORDER.get(str(task.get("priority", "low")), 99)
    return (status_key, priority, task_id_sort_key(str(task.get("id", ""))))


def dependency_lines(task_ids: list[str], task_lookup: dict[str, dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()
    for task_id in sorted(task_ids, key=task_id_sort_key):
        task = task_lookup[task_id]
        local_dependencies = [dep for dep in task["depends_on"] if dep in task_ids]
        if not local_dependencies:
            continue
        for dep in local_dependencies:
            line = f"{dep} -> {task_id}"
            if line not in seen:
                seen.add(line)
                lines.append(line)
    return lines


def project_link(project: dict[str, Any]) -> str:
    if project.get("brief_path"):
        return link(f"{project['id']} — {project['title']}", project["brief_path"])
    return markdown_escape(f"{project['id']} — {project['title']}")


def project_priority_rank(project_tasks: list[dict[str, Any]]) -> int:
    open_tasks = [task for task in project_tasks if task["status_dir"] in OPEN_STATUSES]
    if not open_tasks:
        return 99
    return min(PRIORITY_ORDER.get(str(task.get("priority", "low")), 99) for task in open_tasks)


def build_snapshot(track_dir: Path) -> dict[str, Any]:
    config = load_config(track_dir)
    tasks = discover_tasks(track_dir)
    claims = discover_claims(track_dir)
    root_dir = track_dir.parent

    now = datetime.now(timezone.utc)
    task_records_by_id: dict[str, TaskRecord] = {}
    for task in tasks:
        task_id = str(task.frontmatter.get("id", "")).strip()
        if not task_id:
            raise BuildError(f"{task.path}: missing id in frontmatter")
        if task_id in task_records_by_id:
            raise BuildError(f"duplicate task id '{task_id}' found at {task.path} and {task_records_by_id[task_id].path}")
        task_records_by_id[task_id] = task

    reverse_blockers: dict[str, list[str]] = defaultdict(list)
    for task in tasks:
        depends_on = normalize_depends_on(task.frontmatter.get("depends_on", []))
        for dep_id in depends_on:
            if dep_id in task_records_by_id and task.status_dir in OPEN_STATUSES:
                reverse_blockers[dep_id].append(str(task.frontmatter["id"]))

    active_claims = [claim for claim in claims if not claim_is_expired(claim, now)]
    claim_globs_by_task: dict[str, list[str]] = {}
    for claim in active_claims:
        task_id = str(claim.frontmatter.get("task_id", "")).strip()
        if not task_id:
            raise BuildError(f"{claim.path}: claim missing task_id")
        claim_globs_by_task[task_id] = files_globs(claim.frontmatter.get("files", []))

    config_projects = config.get("projects", {})
    if not isinstance(config_projects, dict):
        raise BuildError(f"{track_dir / 'config.yaml'}: projects must be a mapping")

    summary_by_status = {status: 0 for status in STATUS_DIRS}
    summary_by_priority: dict[str, int] = defaultdict(int)
    summary_by_project: dict[str, int] = defaultdict(int)

    task_rows: list[dict[str, Any]] = []
    for task in tasks:
        task_id = str(task.frontmatter["id"])
        depends_on = normalize_depends_on(task.frontmatter.get("depends_on", []))
        files = files_globs(task.frontmatter.get("files", []))
        blocking_dependencies = [dep_id for dep_id in depends_on if dep_id not in task_records_by_id or task_records_by_id[dep_id].status_dir != "done"]
        blocking_claim_tasks: list[str] = []
        for claim_task_id, claim_files in claim_globs_by_task.items():
            if claim_task_id == task_id:
                continue
            if globs_overlap(files, claim_files):
                blocking_claim_tasks.append(claim_task_id)
        blocking_claim_tasks.sort(key=task_id_sort_key)

        project = task.frontmatter.get("project")
        project_key = str(project) if project not in (None, "") else None
        project_meta = config_projects.get(project_key, {}) if project_key else {}
        project_title = project_meta.get("title") if isinstance(project_meta, dict) else None
        project_brief_path = None
        if isinstance(project_meta, dict) and project_meta.get("brief"):
            project_brief_path = root_relative_path(root_dir, track_dir / str(project_meta["brief"]))

        row = {
            "id": task_id,
            "title": str(task.frontmatter.get("title", "")),
            "status": str(task.frontmatter.get("status", task.status_dir)),
            "status_dir": task.status_dir,
            "mode": task.frontmatter.get("mode"),
            "priority": task.frontmatter.get("priority"),
            "type": task.frontmatter.get("type"),
            "project": project_key,
            "project_title": str(project_title or project_key or "—"),
            "project_brief_path": project_brief_path,
            "cycle": task.frontmatter.get("cycle"),
            "assigned_to": task.frontmatter.get("assigned_to"),
            "pr": task.frontmatter.get("pr"),
            "depends_on": depends_on,
            "files": files,
            "path": root_relative_path(root_dir, task.path),
            "updated": str(task.frontmatter.get("updated", "")),
            "blocking_dependencies": blocking_dependencies,
            "blocking_claim_tasks": blocking_claim_tasks,
            "reverse_blockers": sorted(reverse_blockers.get(task_id, []), key=task_id_sort_key),
        }
        row["availability_reason"] = availability_reason(row)
        row["available"] = row["availability_reason"] == "ready"
        task_rows.append(row)

        summary_by_status[task.status_dir] += 1
        priority = str(task.frontmatter.get("priority", ""))
        if priority:
            summary_by_priority[priority] += 1
        if project_key:
            summary_by_project[project_key] += 1

    task_rows.sort(key=task_priority_sort_key)
    task_lookup = {task["id"]: task for task in task_rows}
    tasks_by_project: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for task in task_rows:
        if task["project"]:
            tasks_by_project[str(task["project"])] .append(task)

    project_rows: list[dict[str, Any]] = []
    for project_id, project_meta in config_projects.items():
        if not isinstance(project_meta, dict):
            raise BuildError(f"project '{project_id}' in .track/config.yaml must be a mapping")
        project_tasks = tasks_by_project.get(str(project_id), [])
        brief_rel = project_meta.get("brief")
        brief_path = None
        if brief_rel:
            brief_path = track_dir / str(brief_rel)
        summary = {
            "open": sum(1 for task in project_tasks if task["status_dir"] in OPEN_STATUSES),
            "ready": sum(1 for task in project_tasks if task["status_dir"] == "todo" and task["available"]),
            "blocked": sum(1 for task in project_tasks if task["status_dir"] == "todo" and not task["available"]),
            "active": sum(1 for task in project_tasks if task["status_dir"] == "active"),
            "review": sum(1 for task in project_tasks if task["status_dir"] == "review"),
            "triage": sum(1 for task in project_tasks if task["status_dir"] == "triage"),
            "done": sum(1 for task in project_tasks if task["status_dir"] == "done"),
            "cancelled": sum(1 for task in project_tasks if task["status_dir"] == "cancelled"),
        }
        state = derive_project_state(str(project_meta.get("status", "active")), summary)
        goal_excerpt = None
        if str(project_meta.get("status", "active")) == "active":
            if not brief_rel:
                raise BuildError(f"active project '{project_id}' is missing a brief path")
            if brief_path is None or not brief_path.exists():
                raise BuildError(f"active project '{project_id}' is missing brief {brief_path}")
            goal_excerpt = extract_goal_excerpt(brief_path)
        elif brief_path is not None and brief_path.exists():
            goal_excerpt = extract_goal_excerpt(brief_path)

        ready_tasks = sorted([task for task in project_tasks if task["status_dir"] == "todo" and task["available"]], key=task_priority_sort_key)
        blocked_tasks = sorted([task for task in project_tasks if task["status_dir"] == "todo" and not task["available"]], key=task_priority_sort_key)
        recent_done = sorted([task for task in project_tasks if task["status_dir"] == "done"], key=updated_desc_sort_key, reverse=True)
        project_rows.append(
            {
                "id": str(project_id),
                "title": str(project_meta.get("title", project_id)),
                "status": str(project_meta.get("status", "active")),
                "description": str(project_meta.get("description", "")).strip(),
                "brief_path": root_relative_path(root_dir, brief_path) if brief_path else None,
                "goal_excerpt": goal_excerpt,
                "state": state,
                "summary": summary,
                "next_task_ids": [task["id"] for task in ready_tasks[:2]],
                "blocked_task_ids": [task["id"] for task in blocked_tasks[:3]],
                "recent_done_task_ids": [task["id"] for task in recent_done[:3]],
            }
        )

    def project_sort_key(project: dict[str, Any]) -> tuple[int, int, int, tuple[int, int, str]]:
        project_tasks = tasks_by_project.get(project["id"], [])
        return (
            PROJECT_STATE_ORDER[project["state"]],
            project_priority_rank(project_tasks),
            -project["summary"]["ready"],
            project_id_sort_key(project["id"]),
        )

    project_rows.sort(key=project_sort_key)

    return {
        "schema_version": config.get("schema_version", "0.1"),
        "summary": {
            "by_status": summary_by_status,
            "by_priority": dict(sorted(summary_by_priority.items(), key=lambda item: PRIORITY_ORDER.get(item[0], 99))),
            "by_project": dict(sorted(summary_by_project.items(), key=lambda item: project_id_sort_key(str(item[0])))),
        },
        "projects": project_rows,
        "tasks": task_rows,
    }


def render_index(snapshot: dict[str, Any]) -> str:
    return json.dumps(snapshot, indent=2, sort_keys=True) + "\n"


def render_projects(snapshot: dict[str, Any]) -> str:
    lines = render_generated_header("Projects")
    active_projects = [project for project in snapshot["projects"] if project["status"] == "active"]
    archived_projects = [project for project in snapshot["projects"] if project["status"] == "archived"]
    task_lookup = {task["id"]: task for task in snapshot["tasks"]}
    tasks_by_project: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for task in snapshot["tasks"]:
        if task["project"]:
            tasks_by_project[str(task["project"])] .append(task)

    immediate_starts = [
        task for task in snapshot["tasks"]
        if task["status_dir"] == "todo" and task["available"] and task.get("project") in {project["id"] for project in active_projects}
    ]
    immediate_starts.sort(key=task_priority_sort_key)
    in_flight_count = sum(1 for project in active_projects if project["state"] == "in_flight")

    lines.append(f"Active projects: {len(active_projects)} | Immediate starts: {min(len(immediate_starts), 7)} | In flight: {in_flight_count}")
    lines.append("")
    for index, project in enumerate(active_projects):
        project_tasks = tasks_by_project.get(project["id"], [])
        visible_tasks = [task for task in project_tasks if task["status_dir"] != "cancelled"]
        visible_tasks.sort(key=lambda task: task_id_sort_key(task["id"]))
        summary = project["summary"]
        lines.append(f"## Project {project['id']}: {project['title']} — {PROJECT_STATE_LABELS[project['state']]}")
        lines.append("")
        if project["description"]:
            lines.append(project["description"])
            lines.append("")
        if project["brief_path"]:
            lines.append(f"**Brief:** {link(project['brief_path'], project['brief_path'])}")
            lines.append("")
        if project["goal_excerpt"]:
            lines.append(project["goal_excerpt"])
            lines.append("")
        lines.append("| # | Task | Mode | Priority | Depends | Status |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        if visible_tasks:
            for task in visible_tasks:
                depends_text = ", ".join(task["depends_on"]) if task["depends_on"] else "—"
                if task["status_dir"] == "done":
                    status = "done"
                else:
                    status = open_task_status(task)
                lines.append(
                    f"| {link(task['id'], task['path'])} | {link(task['title'], task['path'])} | {task.get('mode') or '—'} | {task.get('priority') or '—'} | {depends_text} | {status} |"
                )
        else:
            lines.append("| — | — | — | — | — | — |")
        if index != len(active_projects) - 1 or archived_projects:
            lines.append("")
            lines.append("---")
            lines.append("")
        else:
            lines.append("")

    cross_project_edges: set[str] = set()
    active_project_ids = {project["id"] for project in active_projects}
    for task in snapshot["tasks"]:
        source_project = task.get("project")
        if source_project not in active_project_ids:
            continue
        for dep_id in task["depends_on"]:
            dep_task = task_lookup.get(dep_id)
            if not dep_task:
                continue
            target_project = dep_task.get("project")
            if target_project in active_project_ids and target_project != source_project:
                cross_project_edges.add(f"{target_project} -> {source_project}")
    if cross_project_edges:
        lines.append("## Cross-Project Dependencies")
        lines.append("")
        lines.append("```")
        for edge in sorted(cross_project_edges, key=lambda item: tuple(project_id_sort_key(part.strip()) for part in item.split("->"))):
            lines.append(edge)
        lines.append("```")
        lines.append("")

    if archived_projects:
        lines.append("## Archived Projects")
        lines.append("")
        lines.append("| Project | Status | Description |")
        lines.append("| --- | --- | --- |")
        for project in sorted(archived_projects, key=lambda item: project_id_sort_key(item["id"])):
            lines.append(f"| {project_link(project)} | {project['status']} | {markdown_escape(project['description']) or '—'} |")
        lines.append("")

    lines.append("## Immediate Starts")
    lines.append("")
    if immediate_starts:
        for task in immediate_starts[:7]:
            lines.append(f"- [ ] {link(task['title'], task['path'])} — `{task_project_label(task)}` · `{task.get('priority') or '—'}`")
    else:
        lines.append("- No ready tasks.")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_tasks(snapshot: dict[str, Any]) -> str:
    lines = render_generated_header("Tasks")
    tasks = snapshot["tasks"]
    ready_tasks = sorted([task for task in tasks if task["status_dir"] == "todo" and task["available"]], key=task_priority_sort_key)
    in_flight_tasks = sorted([task for task in tasks if task["status_dir"] in {"active", "review"}], key=task_priority_sort_key)
    blocked_tasks = sorted([task for task in tasks if task["status_dir"] == "todo" and not task["available"]], key=task_priority_sort_key)
    triage_tasks = sorted([task for task in tasks if task["status_dir"] == "triage"], key=task_priority_sort_key)
    done_tasks = sorted([task for task in tasks if task["status_dir"] == "done"], key=updated_desc_sort_key, reverse=True)
    cancelled_tasks = sorted([task for task in tasks if task["status_dir"] == "cancelled"], key=updated_desc_sort_key, reverse=True)

    lines.append(
        f"Ready: {len(ready_tasks)} | In flight: {len(in_flight_tasks)} | Blocked: {len(blocked_tasks)} | Planning: {len(triage_tasks)} | Recently done shown: {min(len(done_tasks), 10)}"
    )
    lines.append("")

    def simple_section(title: str, section_tasks: list[dict[str, Any]], columns: list[str], row_builder) -> None:
        lines.append(f"## {title}")
        lines.append("")
        lines.append("| " + " | ".join(columns) + " |")
        lines.append("| " + " | ".join(["---"] * len(columns)) + " |")
        if section_tasks:
            for task in section_tasks:
                lines.append("| " + " | ".join(row_builder(task)) + " |")
        else:
            lines.append("| " + " | ".join(["—"] * len(columns)) + " |")
        lines.append("")

    simple_section(
        "Ready Now",
        ready_tasks,
        ["ID", "Task", "Project", "Priority", "Depends"],
        lambda task: [
            link(task["id"], task["path"]),
            link(task["title"], task["path"]),
            task_project_ref(task),
            str(task.get("priority") or "—"),
            ", ".join(task["depends_on"]) if task["depends_on"] else "—",
        ],
    )
    simple_section(
        "In Flight",
        in_flight_tasks,
        ["ID", "Task", "Project", "Status", "Updated"],
        lambda task: [
            link(task["id"], task["path"]),
            link(task["title"], task["path"]),
            task_project_ref(task),
            task["status_dir"],
            str(task.get("updated") or "—"),
        ],
    )
    simple_section(
        "Blocked",
        blocked_tasks,
        ["ID", "Task", "Project", "Blocked By"],
        lambda task: [
            link(task["id"], task["path"]),
            link(task["title"], task["path"]),
            task_project_ref(task),
            markdown_escape(why_here(task).replace("blocked by ", "")),
        ],
    )
    simple_section(
        "Planning",
        triage_tasks,
        ["ID", "Task", "Project", "Mode", "Priority"],
        lambda task: [
            link(task["id"], task["path"]),
            link(task["title"], task["path"]),
            task_project_ref(task),
            str(task.get("mode") or "—"),
            str(task.get("priority") or "—"),
        ],
    )
    simple_section(
        "Recent Done",
        done_tasks[:10],
        ["ID", "Task", "Project", "Updated"],
        lambda task: [
            link(task["id"], task["path"]),
            link(task["title"], task["path"]),
            task_project_ref(task),
            str(task.get("updated") or "—"),
        ],
    )

    if cancelled_tasks:
        simple_section(
            "Cancelled",
            cancelled_tasks[:10],
            ["ID", "Task", "Project", "Updated"],
            lambda task: [
                link(task["id"], task["path"]),
                link(task["title"], task["path"]),
                task_project_ref(task),
                str(task.get("updated") or "—"),
            ],
        )

    return "\n".join(lines).rstrip() + "\n"


def render_board(snapshot: dict[str, Any]) -> str:
    lines = render_generated_header("Kanban")
    tasks = snapshot["tasks"]
    lane_map = {
        "active": sorted([task for task in tasks if task["status_dir"] == "active"], key=task_priority_sort_key),
        "review": sorted([task for task in tasks if task["status_dir"] == "review"], key=task_priority_sort_key),
        "ready": sorted([task for task in tasks if task["status_dir"] == "todo" and task["available"]], key=task_priority_sort_key),
        "blocked": sorted([task for task in tasks if task["status_dir"] == "todo" and not task["available"]], key=task_priority_sort_key),
        "triage": sorted([task for task in tasks if task["status_dir"] == "triage"], key=task_priority_sort_key),
        "recent_done": sorted([task for task in tasks if task["status_dir"] == "done"], key=updated_desc_sort_key, reverse=True)[:5],
    }
    summary = snapshot["summary"]["by_status"]
    lines.append(
        f"Active: {len(lane_map['active'])} | Review: {len(lane_map['review'])} | Ready: {len(lane_map['ready'])} | Blocked: {len(lane_map['blocked'])} | Triage: {len(lane_map['triage'])}"
    )
    lines.append("")

    for lane_key, lane_title, _lane_meaning in BOARD_LANES:
        lines.append(f"## {lane_title}")
        lines.append("")
        lane_tasks = lane_map[lane_key]
        if not lane_tasks:
            lines.append("- No tasks.")
            lines.append("")
            continue
        for task in lane_tasks:
            bits = [task_project_label(task)]
            if lane_key in {"active", "review", "ready", "triage"}:
                if task.get("priority"):
                    bits.append(str(task["priority"]))
            if lane_key == "blocked":
                bits.append(why_here(task))
            if lane_key == "recent_done":
                bits.append(str(task.get("updated") or "—"))
            lines.append(f"- `{task['id']}` {link(task['title'], task['path'])} — " + " · ".join(markdown_escape(bit) for bit in bits))
        lines.append("")

    lines.append(
        f"Open: {sum(summary.get(status, 0) for status in OPEN_STATUSES)} | Ready: {len(lane_map['ready'])} | Active: {summary.get('active', 0)} | Review: {summary.get('review', 0)} | Done: {summary.get('done', 0)} | Cancelled: {summary.get('cancelled', 0)}"
    )
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=str(path.parent), delete=False) as handle:
        handle.write(content)
        temp_name = handle.name
    os.replace(temp_name, path)


def build_outputs(track_dir: Path, board_path: Path | None = None) -> dict[str, Path]:
    root_dir = track_dir.parent
    board_path = board_path or root_dir / "BOARD.md"
    outputs = {
        "projects": root_dir / "PROJECTS.md",
        "tasks": root_dir / "TASKS.md",
        "board": board_path,
        "index": track_dir / "index.json",
    }

    snapshot = build_snapshot(track_dir)
    rendered = {
        "projects": render_projects(snapshot),
        "tasks": render_tasks(snapshot),
        "board": render_board(snapshot),
        "index": render_index(snapshot),
    }

    for key, path in outputs.items():
        atomic_write(path, rendered[key])
    return outputs


def fingerprint_inputs(track_dir: Path) -> tuple[tuple[str, int, int], ...]:
    candidates: list[Path] = []
    config_path = track_dir / "config.yaml"
    if config_path.exists():
        candidates.append(config_path)
    projects_root = track_dir / "projects"
    if projects_root.exists():
        candidates.extend(sorted(projects_root.glob("**/*.md")))
    tasks_root = track_dir / "tasks"
    if tasks_root.exists():
        candidates.extend(sorted(tasks_root.glob("**/*.md")))

    entries: list[tuple[str, int, int]] = []
    for path in candidates:
        if path.is_file():
            stat = path.stat()
            entries.append((root_relative_path(track_dir.parent, path), stat.st_mtime_ns, stat.st_size))
    return tuple(entries)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build local Track derived views")
    parser.add_argument("--track-dir", default=".track", help="Track directory path (default: .track)")
    parser.add_argument("--board-path", default="BOARD.md", help="Board output path (default: BOARD.md at repo root)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    track_dir = Path(args.track_dir).resolve()
    board_path = Path(args.board_path).resolve()

    try:
        outputs = build_outputs(track_dir, board_path)
    except BuildError as exc:
        print(f"track-build: {exc}", file=sys.stderr)
        return 1

    ordered = [outputs["projects"], outputs["tasks"], outputs["board"], outputs["index"]]
    print("wrote " + ", ".join(root_relative_path(track_dir.parent, path) for path in ordered))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
