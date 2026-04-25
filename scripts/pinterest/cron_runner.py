#!/usr/bin/env python3
"""Cron runner for Pinterest pin posting.

Designed to be invoked every 30 min by launchd. Picks the next manifest
scam where not all 3 formats are in state.json, then invokes pin.py for
that slug. Exits cleanly with no error if all manifest scams are posted.

Usage:
    python3 scripts/pinterest/cron_runner.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = REPO / "scripts" / "pinterest"
LOG_FILE = HERE / "cron.log"
MANIFEST = HERE / "manifest.json"
STATE = HERE / "state.json"
PIN_PY = HERE / "pin.py"
FORMATS = ("stacked", "hook", "lesson")


def log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")


def find_next_unposted() -> str | None:
    """Walk manifest in order, return first slug missing any format in state."""
    manifest = json.loads(MANIFEST.read_text())
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    for s in manifest["scams"]:
        slug = s["slug"]
        formats_in_manifest = list(s.get("formats", {}).keys())
        if all(f"{slug}:{fmt}" in state for fmt in formats_in_manifest):
            continue
        return slug
    return None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would be done without invoking pin.py")
    args = p.parse_args()

    slug = find_next_unposted()
    if slug is None:
        log("ALL POSTED — nothing to do.")
        return 0

    if args.dry_run:
        log(f"DRY-RUN would process: {slug}")
        print(f"would process: {slug}")
        return 0

    log(f"START {slug}")
    result = subprocess.run(
        ["python3", str(PIN_PY), "--slug", slug],
        capture_output=True, text=True, cwd=str(REPO),
        timeout=180,
    )
    if result.stdout:
        for line in result.stdout.strip().splitlines():
            log(f"  out: {line}")
    if result.stderr:
        for line in result.stderr.strip().splitlines()[-10:]:
            log(f"  err: {line}")
    log(f"DONE {slug} exit={result.returncode}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
