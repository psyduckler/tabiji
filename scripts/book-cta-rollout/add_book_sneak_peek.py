#!/usr/bin/env python3
"""Inject the "A look inside" four-panel-comic sneak-peek section into
book landing pages that don't have it yet.

Section is inserted between the 'Inside this book' teasers section and
the 'N cities covered' section-alt, mirroring Italy's structure.

Idempotent: skips pages that already contain @book-sneak-peek markers.

When you ship a new country book, add an entry to PAIRS + TOTALS below
and re-run. Every country book lander page should have this 2-comic
sample block (matches Japan/Italy/etc.).

Usage:
    python3 scripts/book-cta-rollout/add_book_sneak_peek.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BOOKS = REPO / "books"


# (slug, display_city, short_scam_title)
PAIRS: dict[str, list[tuple[str, str, str]]] = {
    "germany": [
        ("berlin",          "Berlin",          "Alexanderplatz Pickpocket Team"),
        ("munich",          "Munich",          "Hauptbahnhof 'Moldovan Woman' Cash Scam"),
    ],
    "united-kingdom": [
        ("london",          "London",          "Westminster Bridge Shell Game"),
        ("edinburgh",       "Edinburgh",       "Fringe Festival Ticket Fraud"),
    ],
    "brazil": [
        ("rio-de-janeiro",  "Rio de Janeiro",  "Galeão Airport Taxi Mafia"),
        ("salvador",        "Salvador",        "Pelourinho Ribbon-Tying Forced Tip"),
    ],
    "portugal": [
        ("lisbon",          "Lisbon",          "Tram 28 Pickpocket Teams"),
        ("porto",           "Porto",           "Port Cellar Commission Upsell"),
    ],
    "canada": [
        ("toronto",         "Toronto",         "Taxi Card-Swap Fraud"),
        ("montreal",        "Montreal",        "Winter Parking Tow Trap"),
    ],
    "spain": [
        ("barcelona",       "Barcelona",       "La Rambla Pickpocket Gangs"),
        ("madrid",          "Madrid",          "Barajas Airport Taxi Overcharge"),
    ],
    "indonesia": [
        ("bali",            "Bali",            "Ngurah Rai Fake-Grab Taxi Mafia"),
        ("jakarta",         "Jakarta",         "Soekarno-Hatta Airport Sharks"),
    ],
    "vietnam": [
        ("hanoi",           "Hanoi",           "Noi Bai Fake-Grab Driver"),
        ("ho-chi-minh-city","Ho Chi Minh City", "Tan Son Nhat Fake-Grab Driver"),
    ],
    "argentina": [
        ("buenos-aires",        "Buenos Aires",    "The Florida Avenue “¡Cambio!” Tout"),
        ("bariloche",           "Bariloche",       "The Bariloche Rental-Car Smash-and-Grab"),
    ],
    "australia": [
        ("sydney",              "Sydney",          "The Sydney Airport Taxi “Top-Up”"),
        ("gold-coast",          "Gold Coast",      "The Wyndham Timeshare Pitch"),
    ],
    "china": [
        ("beijing",             "Beijing",         "The Beijing Airport Black-Taxi Switch"),
        ("shanghai",            "Shanghai",        "The Nanjing Road Tea-House Scam"),
    ],
    "colombia": [
        ("bogota",              "Bogotá",     "The Bogotá Scopolamine Drink-Spiking"),
        ("medellin",            "Medellín",   "The El Poblado Scopolamine Setup"),
    ],
    "costa-rica": [
        ("manuel-antonio",      "Manuel Antonio",  "The “Park Closed” Fake-Ranger Shake-Down"),
        ("san-jose-costa-rica", "San José",   "The SJO Airport Pirate-Taxi Cartel"),
    ],
    "egypt": [
        ("cairo",               "Cairo",           "The Camel-Ride Hostage at Giza"),
        ("luxor",               "Luxor",           "The Caleche Bait-and-Switch"),
    ],
    "mexico": [
        ("mexico-city",         "Mexico City",     "The MEX “Authorized Taxi” Overcharge"),
        ("cancun",              "Cancún",     "The CUN Airport Fake-“Visitax” Shake-Down"),
    ],
    "morocco": [
        ("marrakech",           "Marrakech",       "The “That Way’s Closed” Fake Guide"),
        ("chefchaouen",         "Chefchaouen",     "The Hash-Tout Police Shakedown"),
    ],
    "turkey": [
        ("istanbul",            "Istanbul",        "The Sultanahmet Shoe-Shine Drop"),
        ("bodrum",              "Bodrum",          "The Cumhuriyet Caddesi Bar Trap"),
    ],
}

# Country totals for the "A sneak peek of two of the N" line.
TOTALS = {
    "germany": 88,
    "united-kingdom": 94,
    "brazil": 72,
    "portugal": 65,
    "canada": 75,
    "spain": 103,
    "indonesia": 73,
    "vietnam": 66,
    "argentina": 66,
    "australia": 84,
    "china": 98,
    "colombia": 58,
    "costa-rica": 69,
    "egypt": 43,
    "mexico": 114,
    "morocco": 61,
    "turkey": 78,
}


def build_section(country: str) -> str:
    total = TOTALS[country]
    pairs = PAIRS[country]
    (s1, c1, t1), (s2, c2, t2) = pairs

    return (
        '<!-- @book-sneak-peek:start -->\n'
        '<section class="section">\n'
        '  <h2>A look inside</h2>\n'
        f'  <p class="section-sub">Every scam in the book gets a four-panel comic. A sneak peek of two of the {total}:</p>\n'
        '  <div class="sneak-peek-grid" style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem;max-width:980px;margin:2rem auto 0;">\n'
        '    <figure style="margin:0;">\n'
        f'      <img src="https://img.tabiji.ai/scams/{s1}/scam-1.jpg" alt="{t1} — comic illustration" loading="lazy" style="width:100%;height:auto;border-radius:12px;display:block;border:1px solid var(--sand,#E8DFD0);">\n'
        f'      <figcaption style="margin-top:0.8rem;font-size:0.88rem;color:var(--text-muted,#6B6258);text-align:center;line-height:1.4;"><strong style="color:var(--indigo,#2D3A5C);">{c1}</strong> · {t1}</figcaption>\n'
        '    </figure>\n'
        '    <figure style="margin:0;">\n'
        f'      <img src="https://img.tabiji.ai/scams/{s2}/scam-1.jpg" alt="{t2} — comic illustration" loading="lazy" style="width:100%;height:auto;border-radius:12px;display:block;border:1px solid var(--sand,#E8DFD0);">\n'
        f'      <figcaption style="margin-top:0.8rem;font-size:0.88rem;color:var(--text-muted,#6B6258);text-align:center;line-height:1.4;"><strong style="color:var(--indigo,#2D3A5C);">{c2}</strong> · {t2}</figcaption>\n'
        '    </figure>\n'
        '  </div>\n'
        '  <style>@media(max-width:720px){.sneak-peek-grid{grid-template-columns:1fr!important}.sneak-peek-grid figure+figure{margin-top:0!important}}</style>\n'
        '</section>\n'
        '<!-- @book-sneak-peek:end -->\n'
    )


# Match the end of the "Inside this book" teasers section. That section has:
#   <section class="section">
#     <h2>Inside this book</h2>
#     ...
#     <div class="teasers-grid">…</div>
#   </section>
# followed by blank line + `<section class="section-alt">`.
#
# We insert the new section between `</section>\n\n<section class="section-alt">`
# — but the insertion must only be after the "Inside this book" section, not
# any random section-alt. Anchor on the inside-book marker.
PATTERN = re.compile(
    r'(<h2>Inside this book</h2>.*?</section>)\n\n(<section class="section-alt">)',
    re.DOTALL,
)


def apply_one(country: str) -> str:
    p = BOOKS / f"{country}-tourist-scams" / "index.html"
    if not p.exists():
        return f"{country}: NO PAGE"
    html = p.read_text()
    if "@book-sneak-peek:start" in html:
        return f"{country}: already has sneak-peek — skipped"
    if not PATTERN.search(html):
        return f"{country}: insertion anchor not found"
    new_section = build_section(country)
    new = PATTERN.sub(
        lambda m: f"{m.group(1)}\n{new_section}\n{m.group(2)}",
        html, count=1,
    )
    if new == html:
        return f"{country}: substitution failed"
    p.write_text(new)
    return f"{country}: ✓ inserted"


def main() -> int:
    for country in PAIRS:
        print(apply_one(country))
    return 0


if __name__ == "__main__":
    sys.exit(main())
