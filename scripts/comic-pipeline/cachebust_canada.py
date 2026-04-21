#!/usr/bin/env python3
"""Add `?v=2` cache-bust to the 53 regenerated Canada scam comics ONLY.

Leaves the 22 unchanged (good v1) comics with their original src so we don't
force a re-fetch on already-correct images. Also skips any scam that was
flagged (regen failed) in /tmp/canada-audit.jsonl — those keep the old v1
image until the next retry.

Idempotent: skips any img src that already has a ?v= query string.

Usage:
    python3 scripts/comic-pipeline/cachebust_canada.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from regen_canada import TARGETS  # noqa: E402

REPO = _HERE.parent.parent
CACHE_VERSION = "2"
AUDIT_LOG = Path("/tmp/canada-audit.jsonl")


def _load_flagged() -> set[tuple[str, int]]:
    """Return set of (city, n) pairs whose regen failed — skip cache-busting these."""
    flagged: set[tuple[str, int]] = set()
    if not AUDIT_LOG.exists():
        print(f"WARN: {AUDIT_LOG} not found — treating all TARGETS as regenerated")
        return flagged
    for line in AUDIT_LOG.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec.get("status") == "flagged":
            flagged.add((rec["city"], rec["n"]))
    return flagged


def cachebust_city(city: str, wanted: list[int], flagged: set[tuple[str, int]]) -> tuple[int, list[str]]:
    path = REPO / f"scams/{city}/index.html"
    html = path.read_text()
    changed = 0
    changes: list[str] = []
    for n in wanted:
        if (city, n) in flagged:
            changes.append(f"  {city}/scam-{n}: SKIP (regen flagged — keeping old image)")
            continue
        # match the scam-N.jpg src in an img.scam-comic tag; skip if already has ?v=
        src_re = re.compile(
            rf'(<img\s+class="scam-comic"\s+src="https://img\.tabiji\.ai/scams/{re.escape(city)}/scam-{n}\.jpg)(?!\?v=)(")',
        )
        new_html, k = src_re.subn(rf'\1?v={CACHE_VERSION}\2', html)
        if k == 0:
            # maybe already cachebust'd, or the src is structured differently
            already = re.search(
                rf'<img\s+class="scam-comic"\s+src="https://img\.tabiji\.ai/scams/{re.escape(city)}/scam-{n}\.jpg\?v=',
                html,
            )
            if already:
                changes.append(f"  {city}/scam-{n}: already cache-busted")
                continue
            changes.append(f"  {city}/scam-{n}: NO MATCH (investigate)")
            continue
        if k > 1:
            changes.append(f"  {city}/scam-{n}: WARNING matched {k}× (using first)")
        html = new_html
        changed += 1
        changes.append(f"  {city}/scam-{n}: ok")
    path.write_text(html)
    return changed, changes


def main() -> int:
    flagged = _load_flagged()
    if flagged:
        print(f"[flagged regen: {len(flagged)} scams skipped] {sorted(flagged)}")
    total_changed = 0
    for city, wanted in TARGETS.items():
        changed, changes = cachebust_city(city, wanted, flagged)
        total_changed += changed
        print(f"[{city}] {changed}/{len(wanted)} cache-busted")
        for line in changes:
            print(line)
    print(f"\nDONE: {total_changed} scam img src tags updated with ?v={CACHE_VERSION}")
    return 0 if total_changed > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
