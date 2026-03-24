#!/usr/bin/env bash
# sync-skills.sh — Sync canonical Archeia skills to plugin and standalone distributions.
# Canonical source: .claude/skills/
# Targets: plugins/archeia/skills/, skills/archeia-*/
#
# Usage:
#   bash scripts/sync-skills.sh
#   bash scripts/sync-skills.sh --check

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHECK_MODE=0

if [[ "${1:-}" == "--check" ]]; then
  CHECK_MODE=1
elif [[ $# -gt 0 ]]; then
  echo "Usage: bash scripts/sync-skills.sh [--check]" >&2
  exit 1
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

STATUS=0

rewrite_name() {
  local source_file="$1"
  local output_file="$2"
  local target_name="$3"

  sed "s/^name: .*/name: $target_name/" "$source_file" > "$output_file"
}

stage_skill() {
  local source_dir="$1"
  local output_dir="$2"
  local target_name="$3"

  mkdir -p "$output_dir"
  rewrite_name "$source_dir/SKILL.md" "$output_dir/SKILL.md" "$target_name"

  if [[ -d "$source_dir/templates" ]]; then
    cp -R "$source_dir/templates" "$output_dir/templates"
  fi

  if [[ -d "$source_dir/agents" ]]; then
    mkdir -p "$output_dir/agents"
    cp -R "$source_dir/agents/." "$output_dir/agents/"
  fi
}

sync_or_check() {
  local staged_dir="$1"
  local target_dir="$2"

  if [[ $CHECK_MODE -eq 1 ]]; then
    if ! diff -ruN "$staged_dir" "$target_dir" > /dev/null; then
      echo "OUT OF SYNC: ${target_dir#$REPO_ROOT/}" >&2
      diff -ruN "$staged_dir" "$target_dir" || true
      STATUS=1
    else
      echo "OK: ${target_dir#$REPO_ROOT/}"
    fi
    return
  fi

  mkdir -p "$target_dir"
  find "$target_dir" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
  cp -R "$staged_dir/." "$target_dir/"
  echo "SYNCED: ${target_dir#$REPO_ROOT/}"
}

sync_mapping() {
  local source_rel="$1"
  local plugin_rel="$2"
  local plugin_name="$3"
  local skills_rel="$4"
  local skills_name="$5"

  local source_dir="$REPO_ROOT/$source_rel"
  local staged_plugin="$TMP_DIR/plugin/$plugin_rel"
  local staged_skills="$TMP_DIR/skills/$skills_rel"
  local target_plugin="$REPO_ROOT/$plugin_rel"
  local target_skills="$REPO_ROOT/$skills_rel"

  if [[ ! -f "$source_dir/SKILL.md" ]]; then
    echo "ERROR: Missing canonical skill at $source_rel" >&2
    exit 1
  fi

  stage_skill "$source_dir" "$staged_plugin" "$plugin_name"
  stage_skill "$source_dir" "$staged_skills" "$skills_name"

  sync_or_check "$staged_plugin" "$target_plugin"
  sync_or_check "$staged_skills" "$target_skills"
}

sync_mapping \
  ".claude/skills/archeia" \
  "plugins/archeia/skills/init" \
  "archeia:init" \
  "skills/archeia-init" \
  "archeia-init"

sync_mapping \
  ".claude/skills/archeia-ask" \
  "plugins/archeia/skills/ask" \
  "archeia:ask" \
  "skills/archeia-ask" \
  "archeia-ask"

if [[ $CHECK_MODE -eq 1 ]]; then
  exit "$STATUS"
fi

echo "Skill sync complete."
