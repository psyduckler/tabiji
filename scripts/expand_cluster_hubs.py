#!/usr/bin/env python3
"""
Expand /compare/{cluster}/ hubs to show ALL cards for their cluster,
not just the top 12.

Context: cluster hubs like /compare/japan/ had 84 comparisons in scope
but only rendered 12 in the hub grid. The remaining 72+ pages got no
internal-link juice from the hub, contributing to the 213 orphaned
canonical pages identified in the 2026-04-16 audit.

This script:
  1. Reads compare/inventory.json for per-cluster card data.
  2. For each existing cluster hub, rebuilds the <section id="popular">
     grid with ALL cards in that cluster, sorted by popularityScore desc
     then slug asc (matching the original sort).
  3. Renames the section heading from "Top comparisons" to
     "All {label} comparisons" to match the expanded content.
  4. Preserves curated meta descriptions and other edits from the
     2026-04-16 audit — the CollectionPage schema's numberOfItems was
     already correct at cluster-size.

Idempotent: re-running produces the same output.
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

# label text used in the hero "{label} comparisons" — copied from
# scripts/build_compare_phase4.mjs clusterDefinitions
CLUSTER_LABELS: dict[str, str] = {
    "japan": "Japan",
    "italy": "Italy",
    "thailand": "Thailand",
    "bali": "Bali",
    "greece": "Greece",
    "spain": "Spain",
    "portugal": "Portugal",
    "croatia": "Croatia",
    "vietnam": "Vietnam",
    "mexico": "Mexico",
    "iceland": "Iceland",
    "maldives": "Maldives",
    "morocco": "Morocco",
    "egypt": "Egypt",
    "australia": "Australia",
    "new-zealand": "New Zealand",
    "taiwan": "Taiwan",
    "sri-lanka": "Sri Lanka",
    "hawaii": "Hawaii",
    "colombia": "Colombia",
}

# Thematic hubs drive off region/tripType rather than the card.cluster
# field. Each is defined by a filter predicate against the inventory.
def _thematic_cards(inventory: list[dict], cluster_slug: str) -> list[dict]:
    def region_match(region: str):
        return lambda c: (c.get("region") or "") == region

    def trip_match(trip: str):
        return lambda c: (c.get("tripType") or "") == trip

    def intent_match(intent: str):
        return lambda c: intent in (c.get("intents") or [])

    predicates = {
        "asia": region_match("Asia"),
        "europe": region_match("Europe"),
        "north-america": region_match("North America"),
        "latin-america": region_match("Latin America"),
        "middle-east-africa": region_match("Middle East & Africa"),
        "oceania": region_match("Oceania"),
        "global-mixed": region_match("Global & Mixed"),
        "cities": trip_match("City breaks"),
        "islands": trip_match("Islands & beaches"),
        "nature": trip_match("Nature & outdoors"),
        "culture": trip_match("Food & culture"),
        "luxury": trip_match("Luxury & honeymoon"),
        "countries": trip_match("Countries"),
        "trip-style-guides": lambda c: (c.get("tripType") or "") in (
            "City breaks", "Islands & beaches", "Nature & outdoors",
            "Food & culture", "Luxury & honeymoon", "Countries",
        ),
    }
    pred = predicates.get(cluster_slug)
    if not pred:
        return []
    return [c for c in inventory if pred(c)]


def safe(s: str | None) -> str:
    return html.escape(s or "", quote=True)


def render_card(card: dict) -> str:
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


def cards_for_cluster(inventory: list[dict], cluster_slug: str) -> list[dict]:
    if cluster_slug in CLUSTER_LABELS:
        cards = [c for c in inventory if (c.get("cluster") or "") == cluster_slug]
    else:
        cards = _thematic_cards(inventory, cluster_slug)
    # Sort by popularity desc, then slug asc (matches build_compare_phase4.mjs)
    return sorted(
        cards,
        key=lambda c: (-(c.get("popularityScore") or 0), c.get("slug") or ""),
    )


def cluster_label(cluster_slug: str, fallback_heading: str) -> str:
    if cluster_slug in CLUSTER_LABELS:
        return CLUSTER_LABELS[cluster_slug]
    # Derive from existing H1 (e.g. "Europe comparisons" -> "Europe")
    return fallback_heading.rsplit(" ", 1)[0] if fallback_heading else cluster_slug


# Regexes scoped to the existing cluster-hub layout (written by
# build_compare_phase4.mjs).
SECTION_RE = re.compile(
    r'(<section class="section" id="popular"><div class="shell">)'
    r'<div class="section-head">.*?</div>'            # existing head
    r'(<div class="grid">).*?(</div></div></section>)',
    re.S,
)
H1_RE = re.compile(r"<h1>([^<]+)</h1>")
STATGRID_COUNT_RE = re.compile(
    r'<div class="statgrid"><div><strong>\d+</strong>'
)
NUMBEROFITEMS_RE = re.compile(
    r'"mainEntity":\{"@type":"ItemList","numberOfItems":\d+\}'
)


ARCHIVE_LIST_RE = re.compile(
    r'(<div id="archiveList" class="archive-list">)(\s*)(</div>)'
)
JS_CARDS_RE = re.compile(r"const cards = (\[[\s\S]+?\]);")


def render_archive_row(card: dict) -> str:
    slug = card["slug"]
    url = card.get("url") or f"/compare/{slug}/"
    d1 = card.get("destination1", "")
    d2 = card.get("destination2", "")
    desc = (card.get("description") or "").strip()
    region = card.get("region") or ""
    trip = card.get("tripType") or ""
    inbound = card.get("inboundLinks") or 0
    return (
        f'<a class="archive-row" href="{safe(url)}">'
        f'<div><h3>{safe(d1)} vs {safe(d2)}</h3><p>{safe(desc)}</p></div>'
        f'<div class="archive-label"><strong>Region</strong><br>{safe(region)}</div>'
        f'<div class="archive-label"><strong>Type</strong><br>{safe(trip)}</div>'
        f'<div class="archive-label"><strong>Signals</strong><br>{inbound} links</div>'
        f'</a>'
    )


def process_country_hub(path: Path, inventory: list[dict]) -> tuple[int, int] | None:
    """Country-cluster layout: <section id="popular"> with <div class="grid">.
    Returns (old_count, new_count) or None if unchanged."""
    cluster_slug = path.parent.name
    cards = cards_for_cluster(inventory, cluster_slug)
    if not cards:
        return None
    txt = path.read_text(encoding="utf-8")

    h1 = H1_RE.search(txt)
    label = cluster_label(cluster_slug, h1.group(1) if h1 else "")

    section_m = SECTION_RE.search(txt)
    if not section_m:
        return None  # thematic hubs have a different layout
    old_section = section_m.group(0)
    old_count = old_section.count('<a class="row"')
    if len(cards) <= old_count:
        return None

    new_head = (
        '<div class="section-head">'
        f'<h2>All {safe(label)} comparisons</h2>'
        f'<p>Every comparison in this cluster, ranked by popularity.</p>'
        '</div>'
    )
    new_grid_inner = "".join(render_card(c) for c in cards)
    new_section = (
        section_m.group(1)
        + new_head
        + section_m.group(2)
        + new_grid_inner
        + section_m.group(3)
    )
    txt = txt[: section_m.start()] + new_section + txt[section_m.end() :]
    txt = NUMBEROFITEMS_RE.sub(
        f'"mainEntity":{{"@type":"ItemList","numberOfItems":{len(cards)}}}',
        txt,
    )
    path.write_text(txt, encoding="utf-8")
    return old_count, len(cards)


def process_thematic_hub(path: Path) -> tuple[int, int] | None:
    """Thematic-hub layout: <div id="archiveList"> populated by JS at runtime.
    Pre-renders the same contents server-side so bots see the anchors in
    raw HTML. JS still runs on top for filtering/sort — it overwrites
    archiveList.innerHTML, so there's no user-visible duplication."""
    txt = path.read_text(encoding="utf-8")
    archive_m = ARCHIVE_LIST_RE.search(txt)
    if not archive_m:
        return None
    # Skip if already pre-rendered (idempotency check)
    if 'class="archive-row"' in archive_m.group(0):
        return None
    cards_m = JS_CARDS_RE.search(txt)
    if not cards_m:
        return None
    try:
        cards = json.loads(cards_m.group(1))
    except json.JSONDecodeError:
        return None
    if not cards:
        return None
    rendered = "".join(render_archive_row(c) for c in cards)
    new_block = archive_m.group(1) + rendered + archive_m.group(3)
    txt = txt[: archive_m.start()] + new_block + txt[archive_m.end() :]
    path.write_text(txt, encoding="utf-8")
    return 0, len(cards)


def process_hub(path: Path, inventory: list[dict]) -> tuple[int, int, str] | None:
    """Route to the correct handler based on layout. Returns
    (old_count, new_count, kind) or None."""
    result = process_country_hub(path, inventory)
    if result is not None:
        return result[0], result[1], "country"
    result = process_thematic_hub(path)
    if result is not None:
        return result[0], result[1], "thematic"
    return None


def main() -> int:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))["cards"]
    hubs = sorted(
        p for p in COMPARE.iterdir()
        if p.is_dir()
        and (p / "index.html").exists()
        and "-vs-" not in p.name  # skip canonical/reverse comparison pages
    )
    total_added = 0
    expanded = 0
    skipped = 0
    for hub in hubs:
        result = process_hub(hub / "index.html", inventory)
        if result is None:
            skipped += 1
            continue
        old, new, kind = result
        expanded += 1
        total_added += new - old
        print(f"  {hub.name:25} [{kind:<8}] {old:>3} → {new:>3}  (+{new - old})")
    print(f"\nExpanded {expanded} hubs, added {total_added} card links. {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
