#!/usr/bin/env python3
"""Three audit P1 fixes batched into one pass:

  #16 Add datePublished/dateModified to all 34 hub pages' CollectionPage
      JSON-LD schema. Dates are derived from git history (file's first
      commit = datePublished, file's latest commit = dateModified).
  #17 Add `<meta name="robots" content="index, follow, max-image-preview:large">`
      to the 17 country sub-hubs that lack it.
  #18 Trim ` (2026 Comparison)` from titles on 208 leaves whose <title> is
      >65 characters. Apply the trim to <title>, og:title, twitter:title,
      and JSON-LD name/headline so all surface forms stay in sync.

Usage:
  python3 scripts/fix_p1_schema_meta.py            # apply
  python3 scripts/fix_p1_schema_meta.py --dry-run  # report only
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMPARE = REPO / "compare"

ALL_HUBS = {
    "asia", "australia", "bali", "cities", "colombia", "countries", "croatia",
    "culture", "egypt", "europe", "global-mixed", "greece", "hawaii", "iceland",
    "islands", "italy", "japan", "latin-america", "luxury", "maldives", "mexico",
    "middle-east-africa", "morocco", "nature", "new-zealand", "north-america",
    "oceania", "portugal", "spain", "taiwan", "thailand", "trip-style-guides",
    "vietnam",
}
COUNTRY_HUBS = {
    "australia", "bali", "colombia", "croatia", "egypt", "greece", "hawaii",
    "iceland", "italy", "japan", "maldives", "mexico", "morocco", "new-zealand",
    "portugal", "spain", "taiwan", "thailand", "vietnam",
}


def git_date(path: Path, first: bool) -> str | None:
    """Return ISO 8601 date for first or latest commit touching this path."""
    args = ["git", "log", "--format=%aI", str(path.relative_to(REPO))]
    if first:
        args.insert(2, "--diff-filter=A")
    try:
        out = subprocess.check_output(args, cwd=REPO, text=True).strip()
    except subprocess.CalledProcessError:
        return None
    if not out:
        return None
    # If --diff-filter=A returns nothing (rare for files renamed), use earliest.
    lines = out.splitlines()
    return lines[-1] if first else lines[0]


# Match the CollectionPage JSON-LD that ends with `}}}` (after closing the
# nested mainEntity ItemList). We inject datePublished/dateModified just
# before the closing of the outer object.
COLLECTION_INSERT = re.compile(
    r'("publisher":\{"@type":"Organization","name":"tabiji\.ai","url":"https://tabiji\.ai"\})'
    r'(,"mainEntity":\{"@type":"ItemList","numberOfItems":\d+\}\})'
)


def fix_hub_dates(path: Path, dry_run: bool) -> bool:
    """Inject datePublished + dateModified into CollectionPage JSON-LD."""
    txt = path.read_text(errors="replace")
    if '"datePublished"' in txt:
        return False
    pub = git_date(path, first=True)
    mod = git_date(path, first=False)
    if not pub or not mod:
        return False
    insertion = f',"datePublished":"{pub}","dateModified":"{mod}"'
    new = COLLECTION_INSERT.sub(rf"\1{insertion}\2", txt, count=1)
    if new == txt:
        return False
    if not dry_run:
        path.write_text(new)
    return True


# Match an existing meta charset/viewport block and inject robots after viewport.
ROBOTS_META = '<meta name="robots" content="index, follow, max-image-preview:large">'
ROBOTS_INJECT = re.compile(
    r'(<meta name="twitter:image" content="[^"]+">)'
    r'(?!<meta name="robots")'
)


def fix_country_hub_robots(path: Path, dry_run: bool) -> bool:
    txt = path.read_text(errors="replace")
    if 'name="robots"' in txt:
        return False
    new = ROBOTS_INJECT.sub(rf"\1{ROBOTS_META}", txt, count=1)
    if new == txt:
        return False
    if not dry_run:
        path.write_text(new)
    return True


# #18: trim " (2026 Comparison)" from titles on leaves whose title is >65c.
# Replace in <title>, og:title, twitter:title, and JSON-LD name/headline.
SUFFIX = " (2026 Comparison)"


def trim_long_title(path: Path, dry_run: bool) -> bool:
    txt = path.read_text(errors="replace")
    m = re.search(r"<title>([^<]+)</title>", txt)
    if not m:
        return False
    title = m.group(1)
    if len(title) <= 65 or SUFFIX not in title:
        return False
    new_title = title.replace(SUFFIX, "", 1)
    # Replace in all surface forms.
    txt2 = txt.replace(title, new_title)
    # Also handle JSON-string-escaped form if present
    if txt2 == txt:
        return False
    if not dry_run:
        path.write_text(txt2)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    # Counters
    hubs_dated = 0
    country_robots_added = 0
    titles_trimmed = 0

    # #16: dates on all 34 hubs
    hub_paths = [COMPARE / "index.html"] + [
        COMPARE / h / "index.html" for h in sorted(ALL_HUBS)
        if (COMPARE / h / "index.html").exists()
    ]
    for p in hub_paths:
        if fix_hub_dates(p, args.dry_run):
            hubs_dated += 1

    # #17: robots meta on 17 country hubs
    for h in sorted(COUNTRY_HUBS):
        p = COMPARE / h / "index.html"
        if not p.exists():
            continue
        if fix_country_hub_robots(p, args.dry_run):
            country_robots_added += 1

    # #18: trim long titles on leaves
    leaves = [p for p in COMPARE.glob("*/index.html") if p.parent.name not in ALL_HUBS]
    for leaf in leaves:
        if trim_long_title(leaf, args.dry_run):
            titles_trimmed += 1

    print(f"#16 hub dates added:       {hubs_dated} / 34")
    print(f"#17 country-hub robots:    {country_robots_added} / 17")
    print(f"#18 long titles trimmed:   {titles_trimmed}")
    if args.dry_run:
        print("\n[dry-run — no files modified]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
