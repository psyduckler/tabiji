#!/usr/bin/env python3
"""Inject tasteful book-promo CTAs into country hubs + city scam pages,
and a sneak-peek comic section into book landing pages.

All injections are idempotent — each block is wrapped in HTML comment
markers (`<!-- @book-cta:start -->` / `<!-- @book-sneak-peek:start -->`)
so re-runs replace in place. Add a new country by extending COUNTRIES.

Run:
    python3 scripts/inject_book_promos.py
"""
from __future__ import annotations

import html as _html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Config: per-country book data + 2 sneak-peek comics
# ---------------------------------------------------------------------------
# Each entry describes the live book, the cities covered by the scam hub
# (used to place city-page CTAs), and the two comic examples shown on the
# book landing page as a sneak peek.
COUNTRIES = [
    {
        "slug": "japan",
        "name": "Japan",
        "hub_code": "jp",
        "scam_count": 60,
        "city_count": 9,
        "sources": "Japanese press and local police advisories",
        "hub_cities": [
            "tokyo", "kyoto", "osaka", "nara", "hiroshima",
            "fukuoka", "sapporo", "yokohama", "okinawa",
        ],
        "comics": [
            {
                "city": "Tokyo",
                "title": "The Bottakuri Bar Overcharge",
                "src": "https://img.tabiji.ai/scams/tokyo/scam-1.jpg?v=2",
            },
            {
                "city": "Kyoto",
                "title": "Fake Buddhist Monk Donation Request",
                "src": "https://img.tabiji.ai/scams/kyoto/scam-2.jpg?v=2",
            },
        ],
    },
    {
        "slug": "france",
        "name": "France",
        "hub_code": "fr",
        "scam_count": 191,
        "city_count": 16,
        "sources": "Le Parisien, Nice-Matin, and Gendarmerie arrest records",
        "hub_cities": [
            "paris", "nice", "cannes", "marseille", "lyon", "bordeaux",
            "toulouse", "strasbourg", "annecy", "avignon", "biarritz",
            "chamonix", "colmar", "mont-saint-michel", "montpellier",
            "st-tropez",
        ],
        "comics": [
            {
                "city": "Paris",
                "title": "The Gold Ring Trick",
                "src": "https://img.tabiji.ai/scams/paris/scam-1.jpg?v=2",
            },
            {
                "city": "Nice",
                "title": "Beach Grab / Swim-and-Steal",
                "src": "https://img.tabiji.ai/scams/nice/scam-1.jpg?v=2",
            },
        ],
    },
    {
        "slug": "italy",
        "name": "Italy",
        "hub_code": "it",
        "scam_count": 149,
        "city_count": 20,
        "sources": "Repubblica, Corriere, and Carabinieri arrest records",
        "hub_cities": [
            "rome", "venice", "florence", "milan", "naples", "bologna",
            "pisa", "siena", "verona", "palermo", "capri", "sardinia",
            "amalfi-coast", "cinque-terre", "lake-como", "lake-garda",
            "pompeii", "positano", "sorrento", "taormina",
        ],
        "comics": [
            {
                "city": "Rome",
                "title": "Gladiator Photo Extortion",
                "src": "https://img.tabiji.ai/scams/rome/scam-1.jpg",
            },
            {
                "city": "Venice",
                "title": "Fake Vaporetto Ticket",
                "src": "https://img.tabiji.ai/scams/venice/scam-1.jpg",
            },
        ],
    },
    {
        "slug": "thailand",
        "name": "Thailand",
        "hub_code": "th",
        "scam_count": 67,
        "city_count": 11,
        "sources": "Bangkok Post, Thai PBS, and Tourist Police (1155) records",
        "hub_cities": [
            "bangkok", "chiang-mai", "chiang-rai", "phuket", "pattaya",
            "krabi", "koh-samui", "koh-phangan", "pai",
        ],
        "comics": [
            {
                "city": "Bangkok",
                "title": "The \u201cGrand Palace Closed Today\u201d Tuk-Tuk",
                "src": "https://img.tabiji.ai/scams/bangkok/scam-1.jpg",
            },
            {
                "city": "Phuket",
                "title": "The Patong Jet-Ski Damage Deposit",
                "src": "https://img.tabiji.ai/scams/phuket/scam-1.jpg",
            },
        ],
    },
    {
        "slug": "greece",
        "name": "Greece",
        "hub_code": "gr",
        "scam_count": 65,
        "city_count": 10,
        "sources": "Kathimerini, Greek Reporter, and Tourist Police (171) records",
        "hub_cities": [
            "athens", "santorini", "mykonos", "rhodes", "corfu", "heraklion",
        ],
        "comics": [
            {
                "city": "Athens",
                "title": "Airport & Piraeus Taxi Overcharge",
                "src": "https://img.tabiji.ai/scams/athens/scam-1.jpg",
            },
            {
                "city": "Santorini",
                "title": "Oia Sunset Per-Kilo Fish Billing",
                "src": "https://img.tabiji.ai/scams/santorini/scam-2.jpg",
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# HTML block templates
# ---------------------------------------------------------------------------
BOOK_CTA_START = "<!-- @book-cta:start -->"
BOOK_CTA_END = "<!-- @book-cta:end -->"
SNEAK_PEEK_START = "<!-- @book-sneak-peek:start -->"
SNEAK_PEEK_END = "<!-- @book-sneak-peek:end -->"


def cta_card(headline: str, sub: str, slug: str) -> str:
    """A warm-cream card linking to the book landing page.

    Used on both country hubs and city scam pages. Inline styles keep it
    safe across shared-shell + per-page <style> blocks.
    """
    return f"""    {BOOK_CTA_START}
    <aside aria-label="tabiji.ai Travel Safety Series" style="margin:2.5rem 0;padding:1.5rem 1.75rem;background:var(--warm-cream,#F5F0E8);border:1px solid var(--sand,#E8DFD0);border-radius:14px;display:flex;flex-wrap:wrap;gap:1.25rem;align-items:center;justify-content:space-between;">
        <div style="flex:1 1 320px;min-width:0;">
            <div style="font-size:0.72rem;letter-spacing:3px;color:var(--earth,#8B7355);text-transform:uppercase;margin-bottom:0.4rem;font-weight:600;">\U0001F4D6 tabiji.ai Travel Safety Series</div>
            <div style="font-size:1.05rem;font-weight:700;color:var(--indigo,#2D3A5C);margin-bottom:0.3rem;line-height:1.35;">{headline}</div>
            <div style="font-size:0.9rem;color:var(--text-muted,#6B6258);line-height:1.45;">{sub}</div>
        </div>
        <a href="/books/{slug}-tourist-scams/" style="flex:0 0 auto;background:var(--terracotta,#C4704B);color:#fff;padding:0.8rem 1.5rem;border-radius:8px;font-weight:700;text-decoration:none;font-size:0.95rem;white-space:nowrap;">See the book \u2192</a>
    </aside>
    {BOOK_CTA_END}
"""


def country_hub_cta(c: dict) -> str:
    headline = f"{c['name']}: Tourist Scams \u2014 the full guide on Kindle"
    sub = (
        f"All {c['scam_count']} scams across {c['city_count']} "
        f"{'cities and islands' if c['slug'] in ('greece', 'thailand') else 'cities'}"
        f" in one offline pocket guide. Drawn from {c['sources']}. $4.99."
    )
    return cta_card(headline, sub, c["slug"])


def city_page_cta(c: dict, city_title: str) -> str:
    headline = (
        f"Heading beyond {city_title}? The full {c['name']} book covers "
        f"{c['scam_count']} scams across {c['city_count']} "
        f"{'cities and islands' if c['slug'] in ('greece', 'thailand') else 'cities'}."
    )
    sub = f"Drawn from {c['sources']}. Available on Kindle, $4.99."
    return cta_card(headline, sub, c["slug"])


def sneak_peek_section(c: dict) -> str:
    """Two-comic sneak peek, matched to the book page's existing .section style."""
    comic_a, comic_b = c["comics"]
    # HTML-escape user-visible text so titles with `&` render correctly.
    a_title_html = _html.escape(comic_a["title"])
    b_title_html = _html.escape(comic_b["title"])
    a_alt_html = _html.escape(f"{comic_a['title']} \u2014 comic illustration", quote=True)
    b_alt_html = _html.escape(f"{comic_b['title']} \u2014 comic illustration", quote=True)
    return f"""{SNEAK_PEEK_START}
<section class="section">
  <h2>A look inside</h2>
  <p class="section-sub">Every scam in the book gets a four-panel comic. A sneak peek of two of the {c['scam_count']}:</p>
  <div class="sneak-peek-grid" style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;max-width:980px;margin:2rem auto 0;">
    <figure style="margin:0;">
      <img src="{comic_a['src']}" alt="{a_alt_html}" loading="lazy" style="width:100%;height:auto;border-radius:12px;display:block;border:1px solid var(--sand,#E8DFD0);">
      <figcaption style="margin-top:0.8rem;font-size:0.88rem;color:var(--text-muted,#6B6258);text-align:center;line-height:1.4;"><strong style="color:var(--indigo,#2D3A5C);">{comic_a['city']}</strong> \u00b7 {a_title_html}</figcaption>
    </figure>
    <figure style="margin:0;">
      <img src="{comic_b['src']}" alt="{b_alt_html}" loading="lazy" style="width:100%;height:auto;border-radius:12px;display:block;border:1px solid var(--sand,#E8DFD0);">
      <figcaption style="margin-top:0.8rem;font-size:0.88rem;color:var(--text-muted,#6B6258);text-align:center;line-height:1.4;"><strong style="color:var(--indigo,#2D3A5C);">{comic_b['city']}</strong> \u00b7 {b_title_html}</figcaption>
    </figure>
  </div>
  <style>@media(max-width:720px){{.sneak-peek-grid{{grid-template-columns:1fr!important}}.sneak-peek-grid figure+figure{{margin-top:0!important}}}}</style>
</section>
{SNEAK_PEEK_END}
"""


# ---------------------------------------------------------------------------
# Idempotent injection helpers
# ---------------------------------------------------------------------------
def replace_or_insert(html: str, start: str, end: str, block: str,
                      anchor_pattern: str, *, before: bool) -> str:
    """Replace existing start..end block if present; else insert relative to anchor.

    Anchor pattern is a regex matched once. If `before` is True, the block is
    inserted immediately before the anchor; otherwise immediately after.
    """
    if start in html and end in html:
        # Consume any leading spaces/tabs on the start-marker line so the
        # replacement block's own indentation is authoritative (avoids
        # compounding indentation on re-runs).
        return re.sub(
            r"[ \t]*" + re.escape(start) + r".*?" + re.escape(end) + r"\n?",
            block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    m = re.search(anchor_pattern, html)
    if not m:
        raise RuntimeError(f"Anchor not found: {anchor_pattern!r}")
    idx = m.start() if before else m.end()
    return html[:idx] + block + html[idx:]


def extract_city_title(html: str, slug: str) -> str:
    """Pull the city's display title from its page. Falls back to slug titlecase.

    City titles vary in preposition ("Scams in X" vs "Scams at X" for lakes)
    and may contain hyphens (Mont-Saint-Michel), so the stop conditions are
    an open-paren or a space-flanked em-dash — never a bare hyphen.
    """
    m = re.search(
        r"<title>[^<]*?Scams (?:in|at) ([^<(]+?)(?:\s*\(|\s+\u2014|</title>)",
        html,
    )
    if m:
        return m.group(1).strip()
    return slug.replace("-", " ").title()


# ---------------------------------------------------------------------------
# Per-file processors
# ---------------------------------------------------------------------------
def process_country_hub(c: dict) -> bool:
    path = REPO / "scams" / "country" / c["hub_code"] / "index.html"
    html = path.read_text(encoding="utf-8")
    block = country_hub_cta(c)
    # Anchor: insert right before the cross-links row at the bottom of <main>.
    new_html = replace_or_insert(
        html, BOOK_CTA_START, BOOK_CTA_END, block,
        anchor_pattern=r'    <div class="cross-links">',
        before=True,
    )
    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        return True
    return False


def process_city_page(c: dict, slug: str) -> bool:
    path = REPO / "scams" / slug / "index.html"
    html = path.read_text(encoding="utf-8")
    city_title = extract_city_title(html, slug)
    block = city_page_cta(c, city_title)
    # Anchor: insert right after the existing .cta-box "Plan Your Trip" block.
    # The cta-box is always followed by `</div>` on its own line, then `</div>`
    # (the container). We insert after the cta-box closing `</div>`.
    cta_box_pattern = re.compile(
        r'<div class="cta-box">.*?</div>\s*\n',
        re.DOTALL,
    )
    if BOOK_CTA_START in html and BOOK_CTA_END in html:
        new_html = re.sub(
            r"[ \t]*" + re.escape(BOOK_CTA_START) + r".*?" + re.escape(BOOK_CTA_END) + r"\n?",
            block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        m = cta_box_pattern.search(html)
        if not m:
            raise RuntimeError(f"cta-box not found on {path}")
        idx = m.end()
        new_html = html[:idx] + block + html[idx:]
    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        return True
    return False


def process_book_landing(c: dict) -> bool:
    path = REPO / "books" / f"{c['slug']}-tourist-scams" / "index.html"
    html = path.read_text(encoding="utf-8")
    block = sneak_peek_section(c)
    # Anchor: between "Inside this book" section end and the following
    # `<section class="section-alt">` (cities covered).
    # The "Inside this book" section's teasers-grid closes with `</div>\n</section>\n`.
    # We insert after that closing </section> and before the next <section class="section-alt">.
    new_html = replace_or_insert(
        html, SNEAK_PEEK_START, SNEAK_PEEK_END, block,
        anchor_pattern=r'\n<section class="section-alt">',
        before=True,
    )
    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        return True
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    touched = 0
    for c in COUNTRIES:
        if process_country_hub(c):
            print(f"  hub       scams/country/{c['hub_code']}/")
            touched += 1
        for city in c["hub_cities"]:
            if process_city_page(c, city):
                print(f"  city      scams/{city}/")
                touched += 1
        if process_book_landing(c):
            print(f"  book      books/{c['slug']}-tourist-scams/")
            touched += 1
    print(f"\nUpdated {touched} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
