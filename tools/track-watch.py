#!/usr/bin/env python3
"""Poll Track inputs and rebuild local derived views on change."""

from __future__ import annotations

import argparse
import signal
import sys
import time
from pathlib import Path

import track_build
from track_build import BuildError

KEEP_RUNNING = True


def handle_signal(_signum, _frame):
    global KEEP_RUNNING
    KEEP_RUNNING = False


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Watch Track inputs and rebuild local derived views")
    parser.add_argument("--track-dir", default=".track", help="Track directory path (default: .track)")
    parser.add_argument("--board-path", default="BOARD.md", help="Board output path (default: BOARD.md at repo root)")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds (default: 1.0)")
    return parser.parse_args(argv)


def build(track_dir: Path, board_path: Path, reason: str) -> bool:
    try:
        track_build.build_outputs(track_dir, board_path)
    except BuildError as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        return False

    print(reason)
    return True


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    track_dir = Path(args.track_dir).resolve()
    board_path = Path(args.board_path).resolve()

    build(track_dir, board_path, "initial build complete")

    previous = track_build.fingerprint_inputs(track_dir)
    while KEEP_RUNNING:
        time.sleep(args.interval)
        current = track_build.fingerprint_inputs(track_dir)
        if current == previous:
            continue
        previous = current
        build(track_dir, board_path, "change detected: rebuilt views")

    print("watch stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
