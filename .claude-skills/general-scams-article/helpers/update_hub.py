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
    #
    # Anchor: city-grid close → grid-section close → </main>. The previous
    # anchor used the Coming Soon section as its boundary, but that section
    # was removed on 2026-04-30 once the live grid had enough cards (8) that
    # it didn't need a roadmap leak below it. The new anchor is stable as
    # long as the hub keeps a single .city-grid wrapped in a .grid-section
    # immediately before </main>.
    card = card_markup(slug, display)
    grid_close_pattern = r'(<div class="city-grid">.*?)(\n\s*</div>\s*\n\s*</div>\s*\n\s*</main>)'
    if not re.search(grid_close_pattern, html, re.DOTALL):
        print("⚠ Could not locate city-grid → </main> boundary", file=sys.stderr)
        sys.exit(1)

    new_html = re.sub(
        grid_close_pattern,
        rf'\1\n{card}\2',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Step 2: legacy Coming-Soon list cleanup.
    #
    # The Coming Soon section was removed on 2026-04-30. This step now only
    # runs if the section is somehow still present (e.g. on a forked or
    # older hub). Otherwise it silently no-ops — the absence is expected.
    if 'class="grid-label">Coming Soon</h2>' in new_html:
        name_keywords = display["name"].lower().split()[0:2]
        coming_soon_pattern_template = r'^[\s]*<li><strong>[^<\n]*?{}[^<\n]*?</strong>[^<\n]*?</li>\s*\n'
        pattern_strings = [re.escape(kw) for kw in name_keywords]
        for pattern_str in pattern_strings:
            coming_soon_pattern = coming_soon_pattern_template.format(pattern_str)
            matches = list(re.finditer(coming_soon_pattern, new_html, re.IGNORECASE | re.MULTILINE))
            if matches:
                new_html = new_html[: matches[0].start()] + new_html[matches[0].end() :]
                print(f"✓ Removed legacy Coming-Soon entry matching keyword '{pattern_str}'")
                break

    HUB_PATH.write_text(new_html)
    print(f"✓ Updated hub: {HUB_PATH}")
    print(f"  - Added card for '{display['name']}'")


if __name__ == "__main__":
    main()
