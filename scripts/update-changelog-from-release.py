#!/usr/bin/env python3

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


def normalize(text: str) -> str:
    return text.replace("\ufeff", "").replace("\r\n", "\n").replace("\r", "\n")


def build_heading(tag: str, url: str, date: str) -> str:
    if url:
        return f"## [{tag}]({url}) - {date}"
    return f"## {tag} - {date}"


def remove_existing_entry(content: str, tag: str) -> str:
    escaped = re.escape(tag)
    pattern = re.compile(
        rf"(?ms)^## (?:\[{escaped}\]\([^\n)]*\)|{escaped}) - [^\n]*\n(?:.*?)(?=^## |\Z)"
    )
    return pattern.sub("", content).strip()


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "CHANGELOG.md")
    tag = os.environ["RELEASE_TAG"].strip()
    date = os.environ.get("RELEASE_DATE", "").strip()[:10]
    url = os.environ.get("RELEASE_URL", "").strip()
    notes = normalize(os.environ.get("RELEASE_NOTES", "")).strip()

    if not tag:
        raise SystemExit("RELEASE_TAG is required")
    if not date:
        raise SystemExit("RELEASE_DATE is required")
    if not notes:
        notes = "- See the GitHub release for details."

    existing = normalize(path.read_text(encoding="utf-8") if path.exists() else "").strip()
    existing = re.sub(r"(?m)^# Changelog\s*$\n?", "", existing).strip()
    existing = remove_existing_entry(existing, tag)

    sections = ["# Changelog", "", build_heading(tag, url, date), "", notes.strip()]
    if existing:
        sections.extend(["", existing])

    path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
