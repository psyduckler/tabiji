#!/usr/bin/env python3
"""Refresh datePublished / dateModified across shipped scam HTML pages.

Early scam-page generation hard-coded `2026-03-29` (published) and
`2026-04-07` (modified) into every city page and a handful of country
hubs. Those dates now lie: a page added last week still claims 2026-03-29,
and a page edited today still claims 2026-04-07.

This script walks the scam HTML corpus and rewrites each file's date
fields from git history:

    datePublished = first commit that added the file (oldest `--follow` log)
    dateModified  = most recent commit touching the file, OR today if we're
                    about to rewrite the file in this sweep (the sweep IS
                    a modification).

Four patterns are rewritten per page (when present):

    1. JSON-LD   "datePublished": "YYYY-MM-DD..."
    2. JSON-LD   "dateModified":  "YYYY-MM-DD..."
    3. Meta      <meta property="article:published_time" content="YYYY-MM-DD...">
    4. Meta      <meta property="article:modified_time"  content="YYYY-MM-DD...">

Plus the hero "Updated {Month} {Year}" line derived from dateModified:

    <span>📅 Updated April 2026</span>                  (city pages)
    <span class="stat-pill">Updated April 2026</span>   (country hubs)

API JSON files carry no date fields (grep-verified) so they are skipped.

Guardrails:
  * Pages where datePublished is NOT the legacy `2026-03-29` are assumed
    already individualized — only dateModified is refreshed.
  * New / uncommitted files fall back to today for both dates.
  * Regex-based — BeautifulSoup is too slow over 600+ files and would
    rewrite formatting we want to preserve.

Usage:
    python3 scripts/sweep_dates.py --dry-run
    python3 scripts/sweep_dates.py --dry-run --limit 3
    python3 scripts/sweep_dates.py
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets, git_commit_times_batch

REPO = Path(__file__).resolve().parents[1]


_MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def _today_iso() -> str:
    """Today as a timezone-aware ISO-8601 timestamp (local offset)."""
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def _iso_date_part(iso: str) -> str:
    """Return the YYYY-MM-DD slice of an ISO-8601 timestamp."""
    return iso[:10]


def _hero_label(iso: str) -> str:
    """Render `Updated April 2026` from an ISO-8601 date string."""
    d = date.fromisoformat(_iso_date_part(iso))
    return f"Updated {_MONTH_NAMES[d.month - 1]} {d.year}"


# --- regex patterns (all anchored on the full YYYY-MM-DD... date token) ---
# Date values may be either "YYYY-MM-DD" or a full ISO-8601 with offset.
_DATE_RE = r"\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}|Z)?)?"

_RE_JSONLD_PUBLISHED = re.compile(rf'"datePublished":\s*"({_DATE_RE})"')
_RE_JSONLD_MODIFIED  = re.compile(rf'"dateModified":\s*"({_DATE_RE})"')
# Meta tag regex — BS4 sometimes re-emits `<meta content="..." property="..."/>`
# with attributes reversed and a self-closing slash. Match either order.
_RE_META_PUBLISHED = re.compile(
    rf'<meta\s+(?:property="article:published_time"\s+content="({_DATE_RE})"'
    rf'|content="({_DATE_RE})"\s+property="article:published_time")\s*/?>'
)
_RE_META_MODIFIED = re.compile(
    rf'<meta\s+(?:property="article:modified_time"\s+content="({_DATE_RE})"'
    rf'|content="({_DATE_RE})"\s+property="article:modified_time")\s*/?>'
)
# Hero span — two shapes: city page (`<span>📅 Updated ...`) and country hub
# (`<span class="stat-pill">Updated ...`). Match the phrase `Updated {Month} {Year}`
# where Month is a full English name (excludes the master-hub's abbreviated
# "Updated Apr 2026" per-card labels, which are child summaries — not the
# master hub's own date).
_RE_HERO_LABEL = re.compile(
    r"Updated (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}"
)


def _rewrite(text: str, published_iso: str, modified_iso: str,
             *, skip_published: bool) -> tuple[str, int]:
    """Apply the 5 substitutions. Returns (new_text, num_replacements)."""
    total = 0

    if not skip_published:
        text, n = _RE_JSONLD_PUBLISHED.subn(
            lambda _m: f'"datePublished": "{published_iso}"', text
        )
        total += n
        text, n = _RE_META_PUBLISHED.subn(
            f'<meta property="article:published_time" content="{published_iso}">',
            text,
        )
        total += n

    text, n = _RE_JSONLD_MODIFIED.subn(
        lambda _m: f'"dateModified": "{modified_iso}"', text
    )
    total += n
    text, n = _RE_META_MODIFIED.subn(
        f'<meta property="article:modified_time" content="{modified_iso}">',
        text,
    )
    total += n

    hero_label = _hero_label(modified_iso)
    text, n = _RE_HERO_LABEL.subn(hero_label, text)
    total += n

    return text, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, help="Stop after N files (for testing)")
    args = ap.parse_args()

    first_map, latest_map = git_commit_times_batch()
    targets = collect_scam_targets(
        city_pages=True,
        country_hubs=True,
        master_hub=True,
    )
    if args.limit:
        targets = targets[: args.limit]

    today_iso = _today_iso()
    files_changed = 0
    total_edits = 0

    for path in targets:
        original = path.read_text()

        first_iso = first_map.get(path) or today_iso
        last_iso = latest_map.get(path) or today_iso
        # The sweep itself is a modification — if today is newer than the
        # last-touch timestamp, prefer today.
        modified_iso = max(last_iso, today_iso)

        # Always stamp both fields from git log so meta + JSON-LD + hero
        # stay in lockstep. An earlier "skip if already-individualized"
        # guardrail caused drift: JSON-LD would be swept while the meta
        # tag with reversed attribute order was left at the old value.
        published_iso = first_iso

        fixed, n = _rewrite(
            original, published_iso, modified_iso,
            skip_published=False,
        )
        if n == 0 or fixed == original:
            continue

        files_changed += 1
        total_edits += n
        label = str(path.relative_to(REPO))
        print(
            f"  {label:55} — published={_iso_date_part(published_iso)} "
            f"modified={_iso_date_part(modified_iso)}"
        )
        if not args.dry_run:
            path.write_text(fixed)

    action = "would refresh" if args.dry_run else "refreshed"
    print(f"\n{action} {total_edits} date fields across {files_changed} files")


if __name__ == "__main__":
    main()
