#!/usr/bin/env python3
"""Bump the ?v=N cache-bust query param on specific scam-comic image tags.

After regenerating a comic at the same R2 path, the Cloudflare CDN may
serve the stale version for ~5 minutes. The convention (per pipeline.md)
is to append/increment a ?v=<N> query param on the <img class="scam-comic">
src so browsers and the CDN fetch fresh bytes immediately.

Usage:
    python3 scripts/comic-pipeline/cachebust.py new-orleans 2 3 7
    python3 scripts/comic-pipeline/cachebust.py chicago 1 5 7 --dry-run
    python3 scripts/comic-pipeline/cachebust.py --targets <file>      # one "city N" per line
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def bump_one(html: str, city: str, n: int) -> tuple[str, str | None]:
    """Bump (or add) ?v= for one scam img. Returns (new_html, action_taken)."""
    # Match the src for scam-N.jpg, optionally with ?v=N
    pat = re.compile(
        rf'(src="https://img\.tabiji\.ai/scams/{re.escape(city)}/scam-{n}\.jpg)(\?v=(\d+))?"'
    )
    m = pat.search(html)
    if not m:
        return html, None
    base, _, current_ver = m.group(1), m.group(2), m.group(3)
    new_ver = int(current_ver) + 1 if current_ver else 2
    new_src = f'{base}?v={new_ver}"'
    new_html = pat.sub(new_src, html, count=1)
    action = f"v={current_ver or '∅'} -> v={new_ver}"
    return new_html, action


def bump_city(city: str, scams: list[int], dry_run: bool = False) -> int:
    path = REPO / f"scams/{city}/index.html"
    if not path.exists():
        print(f"  [{city}] HTML not found at {path}")
        return 0
    html = path.read_text()
    bumped = 0
    for n in scams:
        new_html, action = bump_one(html, city, n)
        if action is None:
            print(f"  [{city}/scam-{n}] no img tag found, skipping")
            continue
        html = new_html
        bumped += 1
        print(f"  [{city}/scam-{n}] {action}")
    if bumped > 0 and not dry_run:
        path.write_text(html)
    return bumped


def parse_targets_file(path: Path) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        city = parts[0]
        for n_str in parts[1:]:
            out.setdefault(city, []).append(int(n_str))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("city", nargs="?", help="city slug (omit if --targets is used)")
    p.add_argument("scams", nargs="*", type=int, help="scam numbers to bump")
    p.add_argument("--targets", help="file with `city N N N` per line")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if args.targets:
        groups = parse_targets_file(Path(args.targets))
    elif args.city and args.scams:
        groups = {args.city: args.scams}
    else:
        sys.exit("usage: cachebust.py <city> <scam_n>... | --targets <file>")

    total = 0
    for city, scams in groups.items():
        print(f"\n→ {city}")
        total += bump_city(city, scams, dry_run=args.dry_run)
    label = "[dry-run] would bump" if args.dry_run else "bumped"
    print(f"\n{label} {total} cache-bust version(s) across {len(groups)} cities")


if __name__ == "__main__":
    main()
