#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

ensure_python() {
  local venv_dir="$ROOT_DIR/.context/track-tools-venv"
  local venv_python="$venv_dir/bin/python"

  if [ -x "$venv_python" ]; then
    echo "$venv_python"
    return 0
  fi

  if python3 -c 'import yaml' >/dev/null 2>&1; then
    echo "python3"
    return 0
  fi

  python3 -m venv "$venv_dir"
  "$venv_python" -m pip install --quiet pyyaml
  echo "$venv_python"
}

PYTHON_BIN="$(ensure_python)"
"$PYTHON_BIN" tools/track-watch.py "$@"
