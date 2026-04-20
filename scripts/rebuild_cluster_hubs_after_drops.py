#!/usr/bin/env python3
"""
Rebuild the "All {X} comparisons" grid in each cluster hub (japan, italy, etc.)
using the current inventory.json. This is a shrink-tolerant version of
expand_cluster_hubs.py — runs after dropping pages so the grid matches the
pruned inventory instead of pointing at deleted compare pages.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMPARE = REPO / "compare"
INVENTORY = COMPARE / "inventory.json"

CLUSTER_LABELS = {
    "japan": "Japan", "italy": "Italy", "thailand": "Thailand", "bali": "Bali",
    "greece": "Greece", "spain": "Spain", "portugal": "Portugal",
    "croatia": "Croatia", "vietnam": "Vietnam", "mexico": "Mexico",
    "iceland": "Iceland", "maldives": "Maldives", "morocco": "Morocco",
    "egypt": "Egypt", "australia": "Australia", "new-zealand": "New Zealand",
    "taiwan": "Taiwan", "sri-lanka": "Sri Lanka", "hawaii": "Hawaii",
    "colombia": "Colombia",
}

SECTION_RE = re.compile(
    r'(<section class="section" id="popular"><div class="shell">)'
    r'<div class="section-head">.*?</div>'
    r'(<div class="grid">).*?(</div></div></section>)',
    re.S,
)
NUMBEROFITEMS_RE = re.compile(
    r'"mainEntity":\{"@type":"ItemList","numberOfItems":\d+\}'
)
STATGRID_COUNT_RE = re.compile(
    r'(<div class="statgrid"><div><strong>)\d+(</strong>)'
)


def safe(s):
    return html.escape(s or "", quote=True)


def render_card(card):
    slug = card["slug"]
    d1 = card.get("destination1", "")
    d2 = card.get("destination2", "")
    heading = f"{d1} vs {d2}".strip()
    desc = (card.get("description") or "").strip()
    trip = card.get("tripType") or ""
    inbound = card.get("inboundLinks") or 0
    score = card.get("popularityScore") or 0
    return (
        f'<a class="row" href="/compare/{slug}/">'
        f'<h3>{safe(heading)}</h3>'
        f'<p>{safe(desc)}</p>'
        f'<div class="meta">{safe(trip)} · {inbound} internal links · score {score}</div>'
        f'</a>'
    )


def rebuild_cluster(cluster_slug, inventory):
    path = COMPARE / cluster_slug / "index.html"
    if not path.exists():
        return None
    cards = [c for c in inventory if (c.get("cluster") or "") == cluster_slug]
    cards.sort(key=lambda c: (-(c.get("popularityScore") or 0), c.get("slug") or ""))

    txt = path.read_text(encoding="utf-8")
    m = SECTION_RE.search(txt)
    if not m:
        return None
    old_count = m.group(0).count('<a class="row"')
    label = CLUSTER_LABELS.get(cluster_slug, cluster_slug)

    new_head = (
        '<div class="section-head">'
        f'<h2>All {safe(label)} comparisons</h2>'
        f'<p>Every comparison in this cluster, ranked by popularity.</p>'
        '</div>'
    )
    new_grid_inner = "".join(render_card(c) for c in cards)
    new_section = m.group(1) + new_head + m.group(2) + new_grid_inner + m.group(3)
    txt = txt[: m.start()] + new_section + txt[m.end():]

    txt = NUMBEROFITEMS_RE.sub(
        f'"mainEntity":{{"@type":"ItemList","numberOfItems":{len(cards)}}}', txt
    )
    # Update the first statgrid count (comparisons)
    txt = STATGRID_COUNT_RE.sub(
        lambda mm: f"{mm.group(1)}{len(cards)}{mm.group(2)}", txt, count=1
    )

    path.write_text(txt, encoding="utf-8")
    return old_count, len(cards)


def main():
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))["cards"]
    total_before = 0
    total_after = 0
    for cluster_slug in sorted(CLUSTER_LABELS):
        result = rebuild_cluster(cluster_slug, inventory)
        if result is None:
            print(f"  {cluster_slug:20} (skipped — no section or missing hub)")
            continue
        old, new = result
        total_before += old
        total_after += new
        print(f"  {cluster_slug:20} {old:>3} → {new:>3}")
    print(f"\nCluster hubs rebuilt. Cards: {total_before} → {total_after} (delta {total_after - total_before})")


if __name__ == "__main__":
    sys.exit(main())
