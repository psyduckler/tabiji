#!/usr/bin/env python3
"""Move a slug from Coming Soon → Live Guides on /scams/everywhere/index.html.

Reads display fields from corpus-mapping.json[<slug>].display, generates
the city-card markup, removes the matching <li> from Coming Soon list,
and inserts the card into the city-grid.

Usage:
    python3 helpers/update_hub.py <slug>
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SKILL_DIR = REPO / ".claude-skills" / "general-scams-article"
HUB_PATH = REPO / "scams" / "everywhere" / "index.html"


def card_markup(slug, display):
    return f'''        <a href="/scams/everywhere/{slug}/" class="city-card">
            <div class="flag">{display["emoji"]}</div>
            <div class="city-name">{display["name"]}</div>
            <div class="city-country">{display["subtitle"]}</div>
            <div class="scam-count">{display["headline_stat"]}</div>
            <div class="city-tagline">{display["tagline"]}</div>
            <div class="card-date" style="font-size:0.72rem;color:#9ca3af;margin-top:0.4rem;">Updated {_current_month_year()}</div>
            <div class="arrow">Read the guide →</div>
        </a>'''


def _current_month_year():
    from datetime import datetime
    return datetime.now().strftime("%b %Y")


def main():
    if len(sys.argv) < 2:
        print("Usage: update_hub.py <slug>", file=sys.stderr)
        sys.exit(1)
    slug = sys.argv[1]

    mapping = json.loads((SKILL_DIR / "corpus-mapping.json").read_text())
    if slug not in mapping:
        print(f"Slug '{slug}' not found in corpus-mapping.json", file=sys.stderr)
        sys.exit(1)
    display = mapping[slug]["display"]

    if not HUB_PATH.exists():
        print(f"Hub page not found at {HUB_PATH}", file=sys.stderr)
        sys.exit(1)

    html = HUB_PATH.read_text()

    # Step 1: insert card into the city-grid (before its closing </div>)
    card = card_markup(slug, display)
    grid_close_pattern = r'(<div class="city-grid">.*?)(\n\s*</div>\s*\n\s*</div>\s*\n\s*<div class="grid-section">\s*\n\s*<h2 class="grid-label">Coming Soon</h2>)'
    if not re.search(grid_close_pattern, html, re.DOTALL):
        print("⚠ Could not locate city-grid + Coming Soon boundary", file=sys.stderr)
        sys.exit(1)

    new_html = re.sub(
        grid_close_pattern,
        rf'\1\n{card}\2',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Step 2: remove the matching <li> from Coming Soon list
    # Match <li>...slug-relevant-name...</li> heuristically by display.name
    name_keywords = display["name"].lower().split()[0:2]  # first 2 words usually identify
    coming_soon_pattern_template = r'\n?\s*<li><strong>([^<]*({})[^<]*)</strong>[^<]*(<[^>]+>[^<]*)*</li>'
    pattern_strings = [
        re.escape(kw) for kw in name_keywords
    ]
    found_and_removed = False
    for pattern_str in pattern_strings:
        coming_soon_pattern = coming_soon_pattern_template.format(pattern_str)
        matches = list(re.finditer(coming_soon_pattern, new_html, re.IGNORECASE))
        if matches:
            new_html = new_html[: matches[0].start()] + new_html[matches[0].end() :]
            found_and_removed = True
            print(f"✓ Removed Coming-Soon entry matching '{matches[0].group(1)}'")
            break

    if not found_and_removed:
        print(
            f"⚠ Could not auto-remove Coming-Soon entry for '{display['name']}'. "
            f"Add it manually.",
            file=sys.stderr,
        )

    HUB_PATH.write_text(new_html)
    print(f"✓ Updated hub: {HUB_PATH}")
    print(f"  - Added card for '{display['name']}'")


if __name__ == "__main__":
    main()
