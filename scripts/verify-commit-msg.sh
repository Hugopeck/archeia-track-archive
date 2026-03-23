#!/usr/bin/env bash

set -euo pipefail

message_file=${1:?"commit message file is required"}
subject_line=$(awk '!/^[[:space:]]*#/ && NF { print; exit }' "$message_file")
pattern='^(feat|fix|refactor|test|docs|chore|ci|build|perf|revert)\([a-z0-9][a-z0-9._/-]*\)(!)?: [^[:space:]].+$'

if [[ -z "$subject_line" ]] || ! [[ "$subject_line" =~ $pattern ]]; then
  cat >&2 <<'EOF'
Commit message must follow Conventional Commits with the repository's required scope:

  <type>(<scope>): <subject>

Allowed types: feat, fix, refactor, test, docs, chore, ci, build, perf, revert
Example:      feat(release): add semantic-release pipeline
EOF
  exit 1
fi
