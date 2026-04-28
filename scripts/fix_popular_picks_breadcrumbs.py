#!/usr/bin/env python3
"""Fix broken country-level breadcrumb links in popular-picks/*/index.html.

Problem
-------
Built pages were generated with a 4-level breadcrumb where level 3 used the
ISO-2 country code as the name AND in the URL, e.g.:

    name: "JO"
    item: "https://tabiji.ai/popular-picks/jo/"

But /popular-picks/<iso>/ pages do not exist; the actual country hubs live at
/popular-picks/<country-slug>/ (e.g. /popular-picks/jordan/).

Fix
---
For each page with a 4-level BreadcrumbList:
  1. Look at level-3 item; extract the slug from its URL.
  2. Map ISO -> existing hub slug + display name.
  3. If a hub exists for that country: rewrite name + URL to point to it.
  4. If no hub exists for that country: drop level 3 entirely and renumber
     level 4 -> 3 (3-level breadcrumb).

Idempotent: safe to re-run.

Usage:
  python3 scripts/fix_popular_picks_breadcrumbs.py            # all pages
  python3 scripts/fix_popular_picks_breadcrumbs.py SLUG ...   # specific slugs
  python3 scripts/fix_popular_picks_breadcrumbs.py --dry-run  # report only
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PP_DIR = REPO / "popular-picks"

# ISO-2 country code -> (display name, hub slug or None)
# None hub-slug means no /popular-picks/<slug>/ hub exists; drop the country
# level instead of pointing at a 404.
ISO_MAP = {
    "AE": ("UAE",            "uae"),
    "AR": ("Argentina",      "argentina"),
    "AT": ("Austria",        "austria"),
    "AU": ("Australia",      "australia"),
    "AZ": ("Azerbaijan",     "azerbaijan"),
    "BB": ("Barbados",       "barbados"),
    "BE": ("Belgium",        "belgium"),
    "BG": ("Bulgaria",       "bulgaria"),
    "BW": ("Botswana",       "botswana"),
    "CA": ("Canada",         "canada"),
    "CH": ("Switzerland",    "switzerland"),
    "CN": ("China",          "china"),
    "CO": ("Colombia",       "colombia"),
    "CR": ("Costa Rica",     None),
    "CZ": ("Czech Republic", None),
    "DE": ("Germany",        "germany"),
    "DK": ("Denmark",        "denmark"),
    "EG": ("Egypt",          "egypt"),
    "ES": ("Spain",          "spain"),
    "ET": ("Ethiopia",       "ethiopia"),
    "FI": ("Finland",        "finland"),
    "FR": ("France",         "france"),
    "GB": ("United Kingdom", None),
    "GE": ("Georgia",        "georgia"),
    "GH": ("Ghana",          "ghana"),
    "GR": ("Greece",         "greece"),
    "HK": ("Hong Kong",      None),
    "HR": ("Croatia",        "croatia"),
    "HU": ("Hungary",        "hungary"),
    "ID": ("Indonesia",      "indonesia"),
    "IE": ("Ireland",        "ireland"),
    "IL": ("Israel",         "israel"),
    "IN": ("India",          "india"),
    "IT": ("Italy",          "italy"),
    "JO": ("Jordan",         "jordan"),
    "JP": ("Japan",          "japan"),
    "KE": ("Kenya",          "kenya"),
    "KH": ("Cambodia",       "cambodia"),
    "KR": ("South Korea",    None),
    "KZ": ("Kazakhstan",     "kazakhstan"),
    "LB": ("Lebanon",        "lebanon"),
    "LK": ("Sri Lanka",      None),
    "MA": ("Morocco",        "morocco"),
    "ML": ("Mali",           "mali"),
    "MM": ("Myanmar",        "myanmar"),
    "MU": ("Mauritius",      "mauritius"),
    "MX": ("Mexico",         "mexico"),
    "MY": ("Malaysia",       "malaysia"),
    "NG": ("Nigeria",        "nigeria"),
    "NL": ("Netherlands",    "netherlands"),
    "NO": ("Norway",         "norway"),
    "NZ": ("New Zealand",    None),
    "PE": ("Peru",           "peru"),
    "PH": ("Philippines",    "philippines"),
    "PL": ("Poland",         "poland"),
    "PT": ("Portugal",       "portugal"),
    "RO": ("Romania",        "romania"),
    "RS": ("Serbia",         "serbia"),
    "RW": ("Rwanda",         "rwanda"),
    "SG": ("Singapore",      "singapore"),
    "SK": ("Slovakia",       "slovakia"),
    "TH": ("Thailand",       "thailand"),
    "TR": ("Turkey",         "turkey"),
    "TW": ("Taiwan",         "taiwan"),
    "TZ": ("Tanzania",       "tanzania"),
    "US": ("United States",  "usa"),
    "VN": ("Vietnam",        "vietnam"),
    "ZA": ("South Africa",   None),
}

# Some pages already use full-name slugs in level 3 — translate them to the
# canonical hub slug if they don't already match a real directory.
SLUG_ALIAS = {
    "united-states": "usa",
    "costa-rica":    None,   # no hub yet; drop the level
}

JSONLD_RE = re.compile(
    r'(<script type="application/ld\+json">)(\{.*?\})(</script>)',
    re.DOTALL,
)
URL_SLUG_RE = re.compile(r'^https://tabiji\.ai/popular-picks/([^/]+)/?$')


def _existing_hubs() -> set[str]:
    """Country-hub directories — single-word lowercase slugs only.
    Slug pages always contain hyphens (e.g. tokyo-ramen), so this excludes them."""
    return {p.name for p in PP_DIR.iterdir()
            if p.is_dir() and re.fullmatch(r'[a-z]+', p.name)}


def _resolve_level3(level3_url: str, hubs: set[str]) -> tuple[str, str] | None:
    """Return (display_name, hub_slug) for the level-3 item, or None to drop it."""
    m = URL_SLUG_RE.match(level3_url)
    if not m:
        return None  # unrecognised URL shape — drop level
    slug = m.group(1)

    # Already pointing at a real hub — leave alone (caller short-circuits).
    if slug in hubs:
        return None  # signals "no change needed"

    # ISO-2 code path: /popular-picks/jo/  ->  ('Jordan', 'jordan')
    if re.fullmatch(r'[a-z]{2,3}', slug):
        info = ISO_MAP.get(slug.upper())
        if info and info[1] is not None:
            return info
        return None  # unknown ISO, or known country but no hub exists — drop

    # Full-name slug we know about (e.g. united-states -> usa).
    if slug in SLUG_ALIAS:
        target = SLUG_ALIAS[slug]
        if target is None:
            return None  # drop
        return (ISO_MAP_BY_HUB.get(target, (target.title(), target))[0], target)

    # Unknown shape — drop the level.
    return None


# Reverse-lookup helper for SLUG_ALIAS resolution
ISO_MAP_BY_HUB = {hub: (name, hub) for iso, (name, hub) in ISO_MAP.items() if hub}


def fix_breadcrumb(obj: dict, hubs: set[str]) -> tuple[dict, str]:
    """Return (possibly-mutated obj, action) where action is 'unchanged',
    'rewrote_l3', 'dropped_l3', or 'noop_already_valid'."""
    items = obj.get("itemListElement", [])
    if len(items) != 4:
        return obj, "unchanged"  # don't touch 3-level or weird shapes

    l3 = items[2]
    l3_url = l3.get("item", "")

    m = URL_SLUG_RE.match(l3_url)
    if m and m.group(1) in hubs:
        return obj, "noop_already_valid"

    resolved = _resolve_level3(l3_url, hubs)
    if resolved is None:
        # Drop level 3, promote level 4 to position 3
        new_items = [items[0], items[1], items[3]]
        new_items[2]["position"] = 3
        obj["itemListElement"] = new_items
        return obj, "dropped_l3"

    name, hub = resolved
    l3["name"] = name
    l3["item"] = f"https://tabiji.ai/popular-picks/{hub}/"
    return obj, "rewrote_l3"


def process(path: Path, hubs: set[str], dry_run: bool) -> str:
    html = path.read_text()
    new_html = html
    action = "unchanged"

    def _sub(m: re.Match) -> str:
        nonlocal action
        prefix, body, suffix = m.group(1), m.group(2), m.group(3)
        try:
            obj = json.loads(body)
        except Exception:
            return m.group(0)
        if not isinstance(obj, dict) or obj.get("@type") != "BreadcrumbList":
            return m.group(0)
        new_obj, this_action = fix_breadcrumb(obj, hubs)
        if this_action in ("unchanged", "noop_already_valid"):
            action = this_action
            return m.group(0)
        action = this_action
        new_body = json.dumps(new_obj, indent=2, ensure_ascii=False)
        return prefix + new_body + suffix

    new_html = JSONLD_RE.sub(_sub, html, count=0)
    if new_html != html and not dry_run:
        path.write_text(new_html)
    return action


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    slugs = [a for a in argv[1:] if not a.startswith("--")]

    hubs = _existing_hubs()

    if slugs:
        paths = [PP_DIR / s / "index.html" for s in slugs]
    else:
        paths = sorted(PP_DIR.glob("*/index.html"))
        paths = [p for p in paths if p.name == "index.html"]

    counts = {"rewrote_l3": 0, "dropped_l3": 0, "noop_already_valid": 0,
              "unchanged": 0}
    for p in paths:
        a = process(p, hubs, dry_run)
        counts[a] = counts.get(a, 0) + 1

    mode = "DRY RUN" if dry_run else "APPLIED"
    print(f"[{mode}] processed {len(paths)} files (existing hubs: {len(hubs)})")
    print(f"  rewrote level-3 (mapped to existing hub): {counts['rewrote_l3']}")
    print(f"  dropped level-3 (no hub exists):          {counts['dropped_l3']}")
    print(f"  noop (already pointing at real hub):      {counts['noop_already_valid']}")
    print(f"  unchanged (no 4-level breadcrumb):        {counts['unchanged']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
