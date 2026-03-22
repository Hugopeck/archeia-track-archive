#!/usr/bin/env bash
# sync-templates.sh — Copy canonical templates to distribution directories.
# Canonical source: .claude/skills/archeia/
# Targets: archeia-plugin/skills/init/, skills/archeia-init/
#
# Usage: bash scripts/sync-templates.sh
#
# This script is idempotent and one-directional (canonical → targets).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

CANONICAL_SKILL="$REPO_ROOT/.claude/skills/archeia/SKILL.md"
CANONICAL_TEMPLATES="$REPO_ROOT/.claude/skills/archeia/templates"

TARGETS=(
  "archeia-plugin/skills/init|archeia:init"
  "skills/archeia-init|archeia-init"
)

if [ ! -f "$CANONICAL_SKILL" ]; then
  echo "ERROR: Canonical SKILL.md not found at $CANONICAL_SKILL" >&2
  exit 1
fi

for entry in "${TARGETS[@]}"; do
  IFS='|' read -r rel_dir skill_name <<< "$entry"
  target_dir="$REPO_ROOT/$rel_dir"
  target_templates="$target_dir/templates"

  if [ ! -d "$target_dir" ]; then
    echo "SKIP: $rel_dir does not exist" >&2
    continue
  fi

  # Sync SKILL.md with adjusted name field
  sed "s/^name: archeia$/name: $skill_name/" "$CANONICAL_SKILL" > "$target_dir/SKILL.md"
  echo "  SKILL.md → $rel_dir/SKILL.md (name: $skill_name)"

  # Sync all template files
  mkdir -p "$target_templates"
  for tmpl in "$CANONICAL_TEMPLATES"/*; do
    fname="$(basename "$tmpl")"
    cp "$tmpl" "$target_templates/$fname"
    echo "  templates/$fname → $rel_dir/templates/$fname"
  done
done

echo "Sync complete."
