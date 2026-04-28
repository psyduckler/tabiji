#!/usr/bin/env python3
"""Clean up _redirects: remove unreachable + broken-target rules, retarget
broken popular-picks rules to /countries/<x>/.

Three operations:
  1. DELETE 22 compare rules whose source page now exists on disk (rule never
     fires because Cloudflare serves the file before consulting _redirects).
  2. DELETE 80 compare reverse-slug rules whose target also doesn't exist
     (the redirect 301s into a 404 — worse than no redirect at all).
  3. RETARGET 13 popular-picks rules whose target /popular-picks/<country>/
     hub doesn't exist; redirect them to the existing /countries/<country>/
     guide instead.

Output: rewritten _redirects file. Idempotent (re-running on a clean file
is a no-op).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REDIRECTS = REPO / "_redirects"
COMPARE = REPO / "compare"
COUNTRIES = REPO / "countries"
POPULAR_PICKS = REPO / "popular-picks"

HUBS = {
    "asia", "australia", "bali", "cities", "colombia", "countries", "croatia",
    "culture", "egypt", "europe", "global-mixed", "greece", "hawaii", "iceland",
    "islands", "italy", "japan", "latin-america", "luxury", "maldives", "mexico",
    "middle-east-africa", "morocco", "nature", "new-zealand", "north-america",
    "oceania", "portugal", "spain", "taiwan", "thailand", "trip-style-guides",
    "vietnam",
}


def on_disk_compare() -> set[str]:
    return {p.parent.name for p in COMPARE.glob("*/index.html")}


def on_disk_countries() -> set[str]:
    return {p.parent.name for p in COUNTRIES.glob("*/index.html")}


def on_disk_pp() -> set[str]:
    return {p.parent.name for p in POPULAR_PICKS.glob("*/index.html")}


def cleanup(dry_run: bool) -> tuple[int, int, int]:
    disk_compare = on_disk_compare()
    disk_countries = on_disk_countries()
    disk_pp = on_disk_pp()

    lines = REDIRECTS.read_text().splitlines(keepends=True)
    out: list[str] = []
    deleted_unreachable = 0
    deleted_broken_compare = 0
    retargeted_pp = 0

    for line in lines:
        stripped = line.strip()
        # Preserve comments + blank lines verbatim.
        if not stripped or stripped.startswith("#"):
            out.append(line)
            continue

        parts = stripped.split()
        if len(parts) < 2:
            out.append(line)
            continue
        src, dst = parts[0], parts[1]
        code = parts[2] if len(parts) >= 3 else "301"

        # Op 1: drop compare rules where source page exists on disk
        m_src = re.match(r"^/compare/([^/*]+)/$", src)
        if m_src and m_src.group(1) in disk_compare and code == "301":
            deleted_unreachable += 1
            continue

        # Op 2: drop compare rules where target page doesn't exist on disk
        m_dst = re.match(r"^/compare/([^/*]+)/?$", dst)
        if (
            m_dst
            and m_dst.group(1) not in disk_compare
            and m_dst.group(1) not in HUBS  # hub targets are intentional
            and code == "301"
        ):
            deleted_broken_compare += 1
            continue

        # Op 3: retarget popular-picks rules pointing to missing /popular-picks/<country>/
        m_pp_dst = re.match(r"^/popular-picks/([^/]+)/?$", dst)
        if (
            m_pp_dst
            and m_pp_dst.group(1) not in disk_pp
            and m_pp_dst.group(1) in disk_countries
            and code == "301"
        ):
            country = m_pp_dst.group(1)
            new_dst = f"/countries/{country}/"
            new_line = line.replace(dst, new_dst, 1)
            out.append(new_line)
            retargeted_pp += 1
            continue

        out.append(line)

    if not dry_run:
        REDIRECTS.write_text("".join(out))

    return deleted_unreachable, deleted_broken_compare, retargeted_pp


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pre_lines = len(REDIRECTS.read_text().splitlines())
    pre_active = sum(
        1 for ln in REDIRECTS.read_text().splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    )

    unreach, broken, retarget = cleanup(args.dry_run)

    print(f"Pre-cleanup:  {pre_lines} total lines, {pre_active} active rules")
    print(f"  Deleted unreachable:        {unreach}")
    print(f"  Deleted broken-target:      {broken}")
    print(f"  Retargeted popular-picks:   {retarget}")

    if not args.dry_run:
        post_lines = len(REDIRECTS.read_text().splitlines())
        post_active = sum(
            1 for ln in REDIRECTS.read_text().splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")
        )
        print(f"Post-cleanup: {post_lines} total lines, {post_active} active rules")
        print(f"  Net delta: {post_active - pre_active} rules ({pre_active} → {post_active})")
    else:
        print("\n[dry-run — no files modified]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
