#!/usr/bin/env python3
"""Roll out the two-tier book CTA across every scam page.

Three-way coverage:
  1. City pages with a dedicated country book (the 13 in ``COUNTRIES``) get the
     per-country ``book-end-cta`` positioned directly after the ``#emergency``
     recovery section and immediately before ``<div class="related-section">``.
     This is the peak-intent moment — the reader has just finished
     "What to Do If You Get Scammed" and their guard is highest.
  2. City pages in orphan countries (no dedicated Amazon title) get the
     ``SERIES_BUNDLE`` fallback CTA pointing to ``/books/`` so every scam page
     still earns its book slot.
  3. Country hubs at ``scams/country/<cc>/index.html`` get the same CTA
     treatment, inserted before ``<div class="cross-links">``.
  4. The master hub ``scams/index.html`` is left CTA-free. The script strips
     any stale ``book-end-cta`` block on the master hub but does not insert a
     new one — product decision (2026-04-24) to keep the stats-bar adjacent
     to the city-grid with no in-content CTA between them.

Inside a city page the script also replaces the legacy mid-scroll
``.mid-cta`` → ``.book-mid-cta`` in the per-country case only, and removes any
surviving legacy ``<div class="cta-box">`` / ``<aside>`` book-cta markup.

The script is idempotent: re-running on a fully-applied corpus produces zero
changes.

Usage:
    python3 scripts/book-cta-rollout/apply_book_ctas.py            # apply
    python3 scripts/book-cta-rollout/apply_book_ctas.py --dry-run  # preview
    python3 scripts/book-cta-rollout/apply_book_ctas.py --only japan thailand
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCAMS = REPO / "scams"

# ----------------------------------------------------------------------------
# Country data — one entry per live Amazon Kindle title.
# ----------------------------------------------------------------------------
COUNTRIES: dict[str, dict] = {
    "japan": {
        "code": "jp",
        "name": "Japan",
        "place_adj": "Japanese",
        "article": "A",
        "book_slug": "japan-tourist-scams",
        "amazon_url": "https://amzn.to/3OEVclV",
        "cover_url": "https://img.tabiji.ai/books/japan-tourist-scams/cover.jpg?v=3",
        "cover_alt": "Japan: Tourist Scams book cover — Mt. Fuji with cherry blossoms",
        "scam_count": 60,
        "city_count": 9,
        "cities_join": "Tokyo, Osaka, Kyoto, Nara &amp; 5 more cities",
        "top_scams_mid": "Tokyo's ¥130,000 bar trap and Nara's aggressive deer",
        "top_scams_end": "Tokyo's ¥130,000 Kabukichō bar trap. Osaka's \"friendly local\" tea-house honeypot. Nara's aggressive deer. Kyoto temple donations. Every documented Japan scam — with the exact scripts, red flags, and Japanese phrases that shut each one down.",
        "language_note": "Japanese",
        "sourced_from": "Japanese press, embassy advisories, and real traveler reports",
    },
    "italy": {
        "code": "it",
        "name": "Italy",
        "place_adj": "Italian",
        "article": "An",
        "book_slug": "italy-tourist-scams",
        "amazon_url": "https://amzn.to/4cFk4lH",
        "cover_url": "/books/italy-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "Italy: Tourist Scams book cover",
        "scam_count": 149,
        "city_count": 20,
        "cities_join": "Rome, Venice, Florence, Milan &amp; 16 more cities",
        "top_scams_mid": "Rome's tre-campanelle shell game and Venice's €2,500-a-day pickpocket ring",
        "top_scams_end": "Rome's tre-campanelle shell game. Venice's €2,500-a-day pickpocket ring. Florence's fake-leather trade. Capri's Blue Grotto fee-stack. Sardinia's €3,000 sand-in-your-luggage fine. Every documented Italy scam — with the exact scripts, red flags, and Italian phrases that shut each one down.",
        "language_note": "Italian",
        "sourced_from": "Repubblica, Corriere, Il Mattino, and Carabinieri arrest records",
    },
    "france": {
        "code": "fr",
        "name": "France",
        "place_adj": "French",
        "article": "A",
        "book_slug": "france-tourist-scams",
        "amazon_url": "https://amzn.to/4mHEZJk",
        "cover_url": "/books/france-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "France: Tourist Scams book cover",
        "scam_count": 191,
        "city_count": 16,
        "cities_join": "Paris, Nice, Cannes, Marseille &amp; 12 more cities",
        "top_scams_mid": "the Paris Hamidovic gang and Cannes's €7.7 million luxury-watch season",
        "top_scams_end": "The Paris Hamidovic gang. Cannes's 301-watches-in-a-year luxury-watch season. The Saint-Tropez beach-club racket the mayor himself called \"racketeering.\" Chamonix chalet-rental fraud. Every documented France scam — with the exact scripts, red flags, and French phrases that shut each one down.",
        "language_note": "French",
        "sourced_from": "Le Parisien, Nice-Matin, La Provence, Ouest-France, and gendarmerie arrest records",
    },
    "indonesia": {
        "code": "id",
        "name": "Indonesia",
        "place_adj": "Indonesian",
        "article": "A",
        "book_slug": "indonesia-tourist-scams",
        "amazon_url": "https://amzn.to/4u41gUj",
        "cover_url": "/books/indonesia-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "Indonesia: Tourist Scams book cover",
        "scam_count": 73,
        "city_count": 12,
        "cities_join": "Bali, Jakarta, Yogyakarta &amp; 9 more cities and regions",
        "top_scams_mid": "Bali's fake-Grab circuit and Jakarta's Blok M honeypot-bar 7-million-rupiah extortion",
        "top_scams_end": "Bali's Ngurah Rai Airport fake-Grab circuit. Jakarta's Blok M honeypot-bar 7-million-rupiah extortion. Yogyakarta's Malioboro batik kickback. The Mount Bromo jeep cartel. Ijen Crater's mandatory-guide shakedown. Every documented Indonesia scam — with the exact scripts, red flags, and Bahasa Indonesia phrases that shut each one down.",
        "language_note": "Bahasa Indonesia",
        "sourced_from": "Jakarta Post, Tempo, Kompas, Bali Post, and Ministry of Tourism records",
    },
    "brazil": {
        "code": "br",
        "name": "Brazil",
        "place_adj": "Brazilian",
        "article": "A",
        "book_slug": "brazil-tourist-scams",
        "amazon_url": "https://amzn.to/48Mib5s",
        "cover_url": "https://img.tabiji.ai/books/brazil-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "Brazil: Tourist Scams book cover",
        "scam_count": 72,
        "city_count": 12,
        "cities_join": "Rio, São Paulo, Salvador, Manaus &amp; 8 more cities",
        "top_scams_mid": "Rio's R$ 250 \"Special Taxi\" kiosk mafia and Lapa's R$ 10,000 caipirinha-bar honeypot",
        "top_scams_end": "Rio Galeão's R$ 250 \"Special Taxi\" kiosk mafia. Lapa's R$ 10,000 caipirinha-bar honeypot. Salvador Pelourinho's <em>fita do Senhor do Bonfim</em> ribbon-tying forced-tip. Manaus's PIX-irreversible jungle-lodge booking fraud. Every documented Brazil scam — with the exact scripts, red flags, and Brazilian Portuguese phrases that shut each one down.",
        "language_note": "Brazilian Portuguese",
        "sourced_from": "DEATUR tourist police, PROCON, IBAMA, and real r/Brazil traveler reports",
    },
    "portugal": {
        "code": "pt",
        "name": "Portugal",
        "place_adj": "Portuguese",
        "article": "A",
        "book_slug": "portugal-tourist-scams",
        "amazon_url": "https://amzn.to/4tnefAl",
        "cover_url": "https://img.tabiji.ai/books/portugal-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "Portugal: Tourist Scams book cover",
        "scam_count": 65,
        "city_count": 10,
        "cities_join": "Lisbon, Porto, the Algarve, Madeira &amp; 6 more destinations",
        "top_scams_mid": "Lisbon Tram 28's pickpocket team and Porto's €60–€150 port-cellar commission upsell",
        "top_scams_end": "Lisbon Tram 28's team-based pickpocket ring through Alfama. Porto's €60–€150 \"port cellar + river cruise + fado\" commission upsell. Faro Airport's duct-taped-rental-car scam. Albufeira's scratchcard-plus-bar-ushering scheme. Every documented Portugal scam — with the exact scripts, red flags, and European Portuguese phrases that shut each one down.",
        "language_note": "European Portuguese",
        "sourced_from": "PSP Turismo, ASAE, Turismo de Portugal, and real traveler reports",
    },
    "canada": {
        "code": "ca",
        "name": "Canada",
        "place_adj": "Canadian",
        "article": "An",
        "book_slug": "canada-tourist-scams",
        "amazon_url": "https://amzn.to/4sOJp2A",
        "cover_url": "/books/canada-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "Canada: Tourist Scams book cover",
        "scam_count": 75,
        "city_count": 12,
        "cities_join": "Toronto, Montreal, Vancouver, Banff &amp; 8 more Canadian cities",
        "top_scams_mid": "Toronto Pearson's Uber cancel-and-cash and Whistler's QR-sticker parking fraud",
        "top_scams_end": "Toronto Pearson's Uber cancel-and-cash. Montreal's winter parking-tow trap. Whistler's CBC-documented QR-sticker parking fraud. Calgary Stampede's ticket-scalper fakes. Banff's Pursuit Collection American-pricing overcharge. Every documented Canada scam — with the exact scripts, red flags, and English and French phrases that shut each one down.",
        "language_note": "English + French",
        "sourced_from": "Globe and Mail, Toronto Star, CBC News, CTV News, and Canadian Anti-Fraud Centre records",
    },
    "united-kingdom": {
        "code": "gb",
        "name": "United Kingdom",
        "place_adj": "UK",
        "article": "An",
        "book_slug": "united-kingdom-tourist-scams",
        "amazon_url": "https://amzn.to/4tqpMih",
        "cover_url": "https://img.tabiji.ai/books/united-kingdom-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "United Kingdom: Tourist Scams book cover",
        "scam_count": 94,
        "city_count": 16,
        "cities_join": "London, Edinburgh, Manchester, Liverpool &amp; 12 more UK cities",
        "top_scams_mid": "London's Westminster Bridge shell game and the Oxford Street moped phone-snatch network",
        "top_scams_end": "London's Westminster Bridge shell game. The Oxford Street moped phone-snatch network. Edinburgh's Royal Mile Fringe-ticket resellers. Bath's Roman Baths queue-jump racket. The Lake District holiday-let booking fraud season. Every documented UK scam — with the exact scripts, red flags, and calm English phrases that shut each one down.",
        "language_note": "English",
        "sourced_from": "The Guardian, The Times, BBC News, Evening Standard, and Action Fraud records",
    },
    "vietnam": {
        "code": "vn",
        "name": "Vietnam",
        "place_adj": "Vietnamese",
        "article": "A",
        "book_slug": "vietnam-tourist-scams",
        "amazon_url": "https://amzn.to/4cLjxPj",
        "cover_url": "/books/vietnam-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "Vietnam: Tourist Scams book cover",
        "scam_count": 66,
        "city_count": 11,
        "cities_join": "Hanoi, HCMC, Hoi An, Ha Long Bay &amp; 7 more destinations",
        "top_scams_mid": "Hanoi's fake-Grab driver at Noi Bai and Ho Chi Minh's Bui Vien 4-million-VND bar extortion",
        "top_scams_end": "Hanoi's Noi Bai Airport fake-Grab driver. Ho Chi Minh City's Bui Vien 4-million-VND bar extortion. Hoi An's tailor-shop markup and fake-monk lantern-boat circuit. Ha Long Bay's off-platform cruise-booking fraud. Every documented Vietnam scam — with the exact scripts, red flags, and Vietnamese phrases that shut each one down.",
        "language_note": "Vietnamese",
        "sourced_from": "Tuoi Tre, VnExpress, Thanh Nien, VietnamPlus, and VNAT tourist-assistance records",
    },
    "germany": {
        "code": "de",
        "name": "Germany",
        "place_adj": "German",
        "article": "An",
        "book_slug": "germany-tourist-scams",
        "amazon_url": "https://amzn.to/4vK73jh",
        "cover_url": "https://img.tabiji.ai/books/germany-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "Germany: Tourist Scams book cover",
        "scam_count": 88,
        "city_count": 16,
        "cities_join": "Berlin, Munich, Hamburg, Cologne &amp; 12 more German cities",
        "top_scams_mid": "Berlin's Brandenburger Tor clipboard-petition team and Munich's Oktoberfest bill-shock",
        "top_scams_end": "Berlin's Brandenburger Tor clipboard-petition pickpocket team. The U-Bahn fake-Kontrolleur €60 cash-fine script. Munich's Oktoberfest \"share my table\" bill-shock. Neuschwanstein's third-party ticket-resale QR fraud. Every documented Germany scam — with the exact scripts, red flags, and calm English and German phrases that shut each one down.",
        "language_note": "English and German",
        "sourced_from": "Der Spiegel, Süddeutsche Zeitung, Bild, Frankfurter Allgemeine, and Bundespolizei records",
    },
    "spain": {
        "code": "es",
        "name": "Spain",
        "place_adj": "Spanish",
        "article": "A",
        "book_slug": "spain-tourist-scams",
        "amazon_url": "https://amzn.to/4vKaDdt",
        "cover_url": "/books/spain-tourist-scams/covers/front-designed.jpg",
        "cover_alt": "Spain: Tourist Scams book cover",
        "scam_count": 103,
        "city_count": 16,
        "cities_join": "Barcelona, Madrid, Seville, Granada &amp; 12 more cities and islands",
        "top_scams_mid": "Barcelona's La Rambla rosemary-sprig circuit and Madrid's Puerta del Sol three-card trile",
        "top_scams_end": "Barcelona's La Rambla rosemary-sprig <em>clavel</em> circuit. Madrid's Puerta del Sol three-card <em>trile</em>. Seville's Plaza de España palm-reading gambit. Granada's Alhambra skip-the-line reseller industry. Ibiza and Mallorca scooter deposit-hold cycle. Every documented Spain scam — with the exact scripts, red flags, and Spanish phrases that shut each one down.",
        "language_note": "Spanish",
        "sourced_from": "El País, La Vanguardia, ABC, El Mundo, and Policía Nacional and Mossos d'Esquadra records",
    },
    "greece": {
        "code": "gr",
        "name": "Greece",
        "place_adj": "Greek",
        "article": "A",
        "book_slug": "greece-tourist-scams",
        "amazon_url": "https://amzn.to/4sLotJJ",
        "cover_url": "/books/greece-tourist-scams/covers/front.jpg",
        "cover_alt": "Greece: Tourist Scams book cover",
        "scam_count": 65,
        "city_count": 10,
        "cities_join": "Athens, Santorini, Mykonos, Crete &amp; 6 more cities and islands",
        "top_scams_mid": "Athens's Plaka clip-joint and Mykonos's DK Oyster €836 seafood bills",
        "top_scams_end": "Athens's Plaka \"friendly local bar\" clip-joint. Mykonos's DK Oyster €836 seafood bills. Santorini's \"meter is broken\" taxi overcharges. Crete's rental-car damage-deposit cycle. Every documented Greece scam — with the exact scripts, red flags, and Greek phrases that shut each one down.",
        "language_note": "Greek",
        "sourced_from": "Kathimerini, eKathimerini, Greek Reporter, Athens Voice, and Tourist Police (171) records",
    },
    "thailand": {
        "code": "th",
        "name": "Thailand",
        "place_adj": "Thai",
        "article": "A",
        "book_slug": "thailand-tourist-scams",
        "amazon_url": "https://amzn.to/4tY1KLr",
        "cover_url": "https://img.tabiji.ai/books/thailand-tourist-scams/cover.jpg",
        "cover_alt": "Thailand: Tourist Scams book cover",
        "scam_count": 67,
        "city_count": 11,
        "cities_join": "Bangkok, Phuket, Chiang Mai, Koh Samui &amp; 7 more cities and islands",
        "top_scams_mid": "Bangkok's \"Grand Palace closed today\" tuk-tuk and Phuket's Patong jet-ski damage-deposit cycle",
        "top_scams_end": "Bangkok's \"Grand Palace closed today\" tuk-tuk and gem-shop loop. Phuket's Patong jet-ski damage-deposit cycle. Chiang Mai's Doi Suthep kickback tours. Koh Tao's passport-hostage motorbike scratch racket. Every documented Thailand scam — with the exact scripts, red flags, and Thai phrases that shut each one down.",
        "language_note": "Thai",
        "sourced_from": "Bangkok Post, The Nation Thailand, Khaosod English, Thai PBS, and Tourist Police (1155) records",
    },
}


# ----------------------------------------------------------------------------
# Orphan-country fallback: the "Travel Safety Series" bundle CTA.
#
# Every city whose ``addressCountry`` is NOT in ``COUNTRIES`` gets this block
# instead. It links to the master books hub at ``/books/`` (not a per-country
# book) and intentionally omits the Amazon buy-button — users typically want
# to browse the series index before purchasing a single title.
# ----------------------------------------------------------------------------
SERIES_BUNDLE: dict = {
    "code": "",
    "name": "Travel Safety",
    "place_adj": "international",
    "article": "An",
    "book_slug": "",  # links to /books/ root
    "cover_alt": "tabiji.ai Travel Safety Series — every country covered",
    "scam_count": 780,
    "scam_count_display": "780+",
    "city_count": 110,
    "cities_join": "Tokyo, Rome, Paris, Bali, Bangkok, Rio &amp; 100+ more cities",
    "top_scams_mid": "the most-cited scams in 20+ destinations from Reddit, embassy advisories, and consumer-protection cases",
    "top_scams_end": "Tokyo's Kabukichō ¥130,000 bar trap. Rome's gladiator photo extortion. Paris's gold-ring trick. Bali's ATM skimmer scams. Bangkok's grand-palace closure ruse. Every documented scam across 20+ destinations — with the exact scripts, red flags, and local-language phrases that shut each one down.",
    "language_note": "country-by-country phrase",
    "sourced_from": "Reddit traveler reports, embassy advisories, and consumer-protection cases",
}


# Inline CSS-only cover block for the bundle. Replaces the broken
# series-bundle/cover.jpg asset; styled by `.bundle-cover` rules in scams.css.
def _bundle_cover_inner() -> str:
    return (
        '            <span class="bundle-cover-badge">20<small>covered</small></span>\n'
        '            <span class="bundle-cover-eyebrow">tabiji.ai</span>\n'
        '            <span class="bundle-cover-title">Travel<em>Safety</em></span>\n'
        '            <span class="bundle-cover-sub">Tourist scams &amp; defenses across 20+ countries — every named scam, every red flag, every script.</span>\n'
        '            <span class="bundle-cover-brand">The Series</span>\n'
    )


def is_bundle(d: dict) -> bool:
    """True iff ``d`` is the SERIES_BUNDLE fallback (vs. a per-country entry)."""
    return not d.get("book_slug")


def book_href(d: dict) -> str:
    """``/books/<slug>/`` for per-country, ``/books/`` for bundle.

    Guards against the ``/books//`` double-slash that naive f-string formatting
    would produce when ``book_slug`` is the empty string.
    """
    slug = d.get("book_slug", "")
    return f"/books/{slug}/" if slug else "/books/"


# ----------------------------------------------------------------------------
# Replacement blocks.
# ----------------------------------------------------------------------------
def _mid_cta_cover_block(d: dict) -> str:
    if is_bundle(d):
        return (
            f'        <div class="book-mid-cta-cover bundle-cover" aria-hidden="true">\n'
            f'{_bundle_cover_inner()}'
            f'        </div>\n'
        )
    return (
        f'        <div class="book-mid-cta-cover">\n'
        f'            <img src="{d["cover_url"]}" alt="{d["cover_alt"]}" width="64" height="96" loading="lazy">\n'
        f'        </div>\n'
    )


def mid_cta_html(d: dict) -> str:
    return (
        f'    <a class="book-mid-cta" href="{book_href(d)}">\n'
        f'{_mid_cta_cover_block(d)}'
        f'        <div class="book-mid-cta-body">\n'
        f'            <div class="book-mid-cta-eyebrow">📖 tabiji.ai Travel Safety Series</div>\n'
        f'            <div class="book-mid-cta-headline">Heading beyond {{city}}? The full {d["name"]} book has {d["scam_count"]} scams across {d["city_count"]} cities — {d["top_scams_mid"]}.</div>\n'
        f'            <div class="book-mid-cta-meta">$4.99 on Kindle · Read in a single flight · Updated annually</div>\n'
        f'        </div>\n'
        f'        <span class="book-mid-cta-btn">See the book →</span>\n'
        f'    </a>'
    )


def _end_cta_headline(d: dict) -> str:
    """Interpolation template for the headline on a *city* page.

    ``{n_scams}`` / ``{city}`` / ``{more}`` are filled by ``interpolate_end``.
    The bundle variant pivots off "destinations" / "countries" instead of the
    per-country ``place_adj`` phrasing.
    """
    if is_bundle(d):
        return (
            f'You just read {{n_scams}} in {{city}}. '
            f'The full Travel Safety Series has 780+ more across 20+ countries.'
        )
    return (
        f'You just read {{n_scams}} in {{city}}. '
        f'The book has {{more}} more across {d["city_count"]} {d["place_adj"]} destinations.'
    )


def _end_cta_eyebrow(d: dict) -> str:
    if is_bundle(d):
        return "📖 tabiji.ai Travel Safety Series"
    return f'📖 {d["name"]}: Tourist Scams'


def _end_cta_aria(d: dict) -> str:
    if is_bundle(d):
        return "tabiji.ai Travel Safety Series"
    return f'{d["name"]}: Tourist Scams book'


def _end_cta_benefits(d: dict) -> str:
    """Benefits bullets inside the end-CTA."""
    if is_bundle(d):
        return (
            f'                <li>780+ documented scams across {d["cities_join"]}</li>\n'
            f'                <li>20+ countries covered, with {d["language_note"]} cards for every destination</li>\n'
            f'                <li>Updated annually — buy once, re-download future editions free</li>\n'
            f'                <li>All titles $4.99 each on Amazon Kindle</li>\n'
        )
    return (
        f'                <li>{d["scam_count"]} documented scams across {d["cities_join"]}</li>\n'
        f'                <li>{d["article"]} {d["language_note"]} exit-phrase card you can screenshot to your phone</li>\n'
        f'                <li>Updated annually — buy once, re-download future editions free</li>\n'
        f'                <li>Readable in one flight — $4.99 on Amazon Kindle</li>\n'
    )


def _end_cta_primary_label(d: dict) -> str:
    if is_bundle(d):
        return "Browse the series →"
    return "See what's inside →"


def _end_cta_buttons(d: dict) -> str:
    """Primary+secondary button row.

    Bundle variant drops the Amazon button entirely (users browse before they
    buy); per-country variant keeps both.
    """
    primary = (
        f'                <a href="{book_href(d)}" class="book-end-cta-primary">'
        f'{_end_cta_primary_label(d)}</a>\n'
    )
    if is_bundle(d):
        # Single-button layout — deliberately no Amazon CTA yet.
        return primary
    secondary = (
        f'                <a href="{d["amazon_url"]}" target="_blank" rel="noopener" '
        f'class="book-end-cta-secondary">Buy on Amazon · $4.99 →</a>\n'
    )
    return primary + secondary


def _end_cta_cover_block(d: dict) -> str:
    if is_bundle(d):
        return (
            f'        <a href="{book_href(d)}" class="book-end-cta-cover bundle-cover" aria-hidden="true">\n'
            f'{_bundle_cover_inner()}'
            f'        </a>\n'
        )
    return (
        f'        <a href="{book_href(d)}" class="book-end-cta-cover" aria-hidden="true">\n'
        f'            <img src="{d["cover_url"]}" alt="{d["cover_alt"]}" width="220" height="330" loading="lazy">\n'
        f'        </a>\n'
    )


def end_cta_html(d: dict) -> str:
    """End-of-article CTA block for a *city* page.

    The returned string is already wrapped in the
    ``<!-- @book-cta:start -->`` / ``<!-- @book-cta:end -->`` markers used for
    idempotent detection; callers should NOT add their own markers.
    """
    return (
        f'    <!-- @book-cta:start -->\n'
        f'    <section class="book-end-cta" aria-label="{_end_cta_aria(d)}">\n'
        f'{_end_cta_cover_block(d)}'
        f'        <div class="book-end-cta-body">\n'
        f'            <div class="book-end-cta-eyebrow">{_end_cta_eyebrow(d)}</div>\n'
        f'            <h2 class="book-end-cta-headline">{_end_cta_headline(d)}</h2>\n'
        f'            <p class="book-end-cta-sub">{d["top_scams_end"]} Drawn from {d["sourced_from"]}.</p>\n'
        f'            <ul class="book-end-cta-benefits">\n'
        f'{_end_cta_benefits(d)}'
        f'            </ul>\n'
        f'            <div class="book-end-cta-btns">\n'
        f'{_end_cta_buttons(d)}'
        f'            </div>\n'
        f'        </div>\n'
        f'    </section>\n'
        f'    <!-- @book-cta:end -->'
    )


def hub_cta_html(d: dict) -> str:
    """End-of-hub CTA for a *country hub* (``scams/country/<cc>/index.html``).

    Same visual block as the city end-CTA but with hub-appropriate copy
    (there's no "you just read N scams" hook because hubs are index pages).
    """
    if is_bundle(d):
        headline = (
            "Every scam across 20+ countries, in one offline pocket guide."
        )
    else:
        headline = (
            f'The full {d["name"]} guide — {d["scam_count"]} scams across {d["city_count"]} destinations.'
        )
    return (
        f'    <!-- @book-cta:start -->\n'
        f'    <section class="book-end-cta" aria-label="{_end_cta_aria(d)}">\n'
        f'{_end_cta_cover_block(d)}'
        f'        <div class="book-end-cta-body">\n'
        f'            <div class="book-end-cta-eyebrow">{_end_cta_eyebrow(d)}</div>\n'
        f'            <h2 class="book-end-cta-headline">{headline}</h2>\n'
        f'            <p class="book-end-cta-sub">{d["top_scams_end"]} Drawn from {d["sourced_from"]}.</p>\n'
        f'            <ul class="book-end-cta-benefits">\n'
        f'{_end_cta_benefits(d)}'
        f'            </ul>\n'
        f'            <div class="book-end-cta-btns">\n'
        f'{_end_cta_buttons(d)}'
        f'            </div>\n'
        f'        </div>\n'
        f'    </section>\n'
        f'    <!-- @book-cta:end -->'
    )


# ----------------------------------------------------------------------------
# Per-page: extract city display name, scam count, and addressCountry.
# ----------------------------------------------------------------------------
ADDRESS_COUNTRY_RE = re.compile(r'"addressCountry"\s*:\s*"([A-Za-z]{2})"')
# Fallback: ~25 pages (Australia + Thailand, older templates) have no
# schema.org Place block but DO carry a breadcrumb link to
# ``/scams/country/<cc>/``. Match a two-letter segment there as a last-resort.
BREADCRUMB_COUNTRY_RE = re.compile(r'href="/scams/country/([a-z]{2})/"')


def parse_page_meta(html: str, slug: str) -> tuple[str, int]:
    """Return ``(display_city, scam_count)`` for a city page."""
    m = re.search(r'<h1[^>]*>\s*(?:\d+\s+)?Tourist Scams in ([^<]+?)\s*</h1>', html)
    city = m.group(1).strip() if m else slug.replace("-", " ").title()
    ids = set(re.findall(r'id="scam-(\d+)"', html))
    if ids:
        return city, len(ids)
    labels = set(re.findall(r'>Scam\s*#(\d+)<', html))
    return city, len(labels)


def extract_country_code(html: str) -> str | None:
    """Lowercase ISO-2 country code for a city page.

    Tries schema.org ``addressCountry`` first; falls back to the breadcrumb
    ``<a href="/scams/country/<cc>/">Country</a>`` link for ~25 pages on an
    older template that omit the Place block.

    Returns None when neither source is present (e.g. the master hub or an
    unrelated sub-page).
    """
    m = ADDRESS_COUNTRY_RE.search(html)
    if m:
        return m.group(1).lower()
    m = BREADCRUMB_COUNTRY_RE.search(html)
    if m:
        return m.group(1).lower()
    return None


# ----------------------------------------------------------------------------
# Legacy scrubs + anchor insertion.
# ----------------------------------------------------------------------------
MID_CTA_RE = re.compile(
    r'[ \t]*<div class="mid-cta">\s*<p>[^<]*(?:Like what you\'re reading|Enjoying this guide)[^<]*</p>\s*<a href="/plan/?">[^<]*</a>\s*</div>',
    re.DOTALL,
)
# Legacy free-trip-planner CTA — kept as a scrub pattern so re-runs clean it up
# even though we no longer *replace* it; the new book-CTA now anchors on
# related-section, not on this cta-box.
CTA_BOX_RE = re.compile(
    # Matches both attribute orderings (href-first or class-first), with or
    # without a trailing slash on /plan, and an optional "<!-- CTA -->" hint
    # comment on the preceding line. Trailing ``\n?`` keeps re-runs tidy.
    r'[ \t]*(?:<!--\s*CTA\s*-->\s*\n[ \t]*)?<div class="cta-box">\s*<h2>[^<]*</h2>\s*<p>[^<]*</p>\s*<a [^>]*href="/plan/?"[^>]*>[^<]*</a>\s*</div>\n?',
    re.DOTALL,
)
# Legacy tiny <aside> book-cta (the one before the full two-tier rollout).
# Kept as a scrub so repeated runs clean it up without double-injecting.
# Trailing ``\n?`` absorbs the block's own newline so we don't leave an extra
# blank line when re-running.
BOOK_ASIDE_RE = re.compile(
    r'[ \t]*<!--\s*@book-cta:start\s*-->\s*<aside\b.*?</aside>\s*<!--\s*@book-cta:end\s*-->\n?',
    re.DOTALL,
)
# Any existing two-tier book-cta block (marker-wrapped section). Matches the
# CURRENT idiom, so we can detect + remove it to re-insert at the correct
# anchor point. ``re.DOTALL`` so it spans newlines. Trailing ``\n?`` keeps
# re-runs idempotent (see BOOK_ASIDE_RE comment).
BOOK_END_BLOCK_RE = re.compile(
    r'[ \t]*<!--\s*@book-cta:start\s*-->\s*<section\b[^>]*class="[^"]*book-end-cta[^"]*"[^>]*>.*?</section>\s*<!--\s*@book-cta:end\s*-->\n?',
    re.DOTALL,
)
RELATED_SECTION_RE = re.compile(r'(?P<indent>[ \t]*)<div class="related-section">')
CROSS_LINKS_RE = re.compile(r'(?P<indent>[ \t]*)<div class="cross-links">')


def interpolate_mid(template: str, city: str) -> str:
    return template.replace("{city}", city)


def interpolate_end(template: str, city: str, scam_count_on_page: int, country_total: int) -> str:
    n = max(scam_count_on_page, 1)
    more = max(country_total - n, 1)
    scam_word = "scam" if n == 1 else "scams"
    return (template.replace("{city}", city)
                    .replace("{n_scams}", f"{n} {scam_word}")
                    .replace("{n}", str(n))
                    .replace("{more}", str(more))
                    .replace("{destinations}", "destinations"))


# ----------------------------------------------------------------------------
# City-page application.
# ----------------------------------------------------------------------------
def _insert_before_anchor(html: str, anchor_re: re.Pattern, cta_block: str) -> tuple[str, bool]:
    """Insert ``cta_block`` immediately before the first anchor match.

    The anchor's own leading whitespace is preserved, so the CTA is separated
    from the anchor by exactly one newline. Returns ``(new_html, inserted?)``.
    """
    m = anchor_re.search(html)
    if not m:
        return html, False
    start = m.start()
    # Walk back to the start of the line that contains the anchor so we keep
    # the anchor's own leading whitespace untouched.
    line_start = html.rfind("\n", 0, start) + 1  # 0 if no \n found → start
    insertion = cta_block.rstrip() + "\n"
    new_html = html[:line_start] + insertion + html[line_start:]
    return new_html, True


def apply_to_city_page(html: str, country: dict, city_display: str, scam_count: int) -> tuple[str, dict]:
    """Apply the book-CTA rollout to a single city page.

    Steps:
      1. Mid-CTA: replace legacy ``.mid-cta`` with the new ``.book-mid-cta``
         (per-country pages only — bundle pages skip the mid-CTA to avoid
         cluttering an orphan page with two bundle CTAs).
      2. Scrub legacy ``<aside>`` book-cta.
      3. Strip any *current* book-end-cta section so re-runs cleanly re-anchor.
      4. Scrub the legacy ``<div class="cta-box">`` free-trip-planner block.
      5. Insert the new ``<section class="book-end-cta">`` directly before
         ``<div class="related-section">``; if the page has no
         related-section, fall back to the previous position by appending
         before ``</main>``.
    """
    stats = {"mid": 0, "cta_box": 0, "old_book_aside": 0, "end_stripped": 0,
             "end_inserted": 0, "end_fallback": 0}
    new_html = html

    # Step 1: mid-CTA (per-country only).
    if not is_bundle(country):
        mid = interpolate_mid(mid_cta_html(country), city_display)
        new_html, n = MID_CTA_RE.subn(mid, new_html, count=1)
        stats["mid"] = n

    # Steps 2+3: scrub any existing book-cta marker-wrapped block.
    new_html, n_before = BOOK_ASIDE_RE.subn("", new_html, count=1)
    stats["old_book_aside"] = n_before
    new_html, n_end = BOOK_END_BLOCK_RE.subn("", new_html, count=1)
    stats["end_stripped"] = n_end

    # Step 4: scrub the legacy free-trip-planner box. No replacement — the new
    # book-CTA now anchors on related-section, not on this box.
    new_html, n_cta = CTA_BOX_RE.subn("", new_html, count=1)
    stats["cta_box"] = n_cta

    # Step 5: insert the new end-CTA.
    end = interpolate_end(end_cta_html(country), city_display, scam_count, country["scam_count"])
    new_html, inserted = _insert_before_anchor(new_html, RELATED_SECTION_RE, end)
    if inserted:
        stats["end_inserted"] = 1
    else:
        # Fallback chain for pages without a related-section:
        #   1. Insert just before </main> (Bangkok-style template).
        #   2. Insert just before <!-- @include:footer:start --> (older
        #      Thailand/Australia templates that don't use <main> at all).
        fallback_anchors = (
            re.compile(r'(?P<indent>[ \t]*)</main>'),
            re.compile(r'(?P<indent>[ \t]*)<!--\s*@include:footer:start\s*-->'),
        )
        for pat in fallback_anchors:
            m = pat.search(new_html)
            if m:
                line_start = new_html.rfind("\n", 0, m.start()) + 1
                insertion = end.rstrip() + "\n"
                new_html = new_html[:line_start] + insertion + new_html[line_start:]
                stats["end_fallback"] = 1
                break
        # else: page has none — leave as-is (the scrubs already fired).

    return new_html, stats


# ----------------------------------------------------------------------------
# Country-hub application.
# ----------------------------------------------------------------------------
def apply_to_country_hub(html: str, country: dict) -> tuple[str, dict]:
    """Apply a book CTA to a country-hub page (``/scams/country/<cc>/``).

    Inserts before ``<div class="cross-links">`` (the nav-breadcrumb strip at
    the bottom of every hub). If the hub has an older ``<aside>`` book-cta or
    a current section block, strip it first for idempotency.
    """
    stats = {"old_book_aside": 0, "end_stripped": 0, "hub_inserted": 0}
    new_html, n_aside = BOOK_ASIDE_RE.subn("", html, count=1)
    stats["old_book_aside"] = n_aside
    new_html, n_end = BOOK_END_BLOCK_RE.subn("", new_html, count=1)
    stats["end_stripped"] = n_end

    cta = hub_cta_html(country)
    new_html, inserted = _insert_before_anchor(new_html, CROSS_LINKS_RE, cta)
    if inserted:
        stats["hub_inserted"] = 1
    return new_html, stats


# ----------------------------------------------------------------------------
# Country-code → COUNTRIES entry index.
# ----------------------------------------------------------------------------
def country_by_code() -> dict[str, dict]:
    return {d["code"]: d for d in COUNTRIES.values()}


# ----------------------------------------------------------------------------
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Print what would change; don't write")
    ap.add_argument("--only", nargs="*",
                    help="Country slugs (matching COUNTRIES keys) to restrict to. "
                         "Default: all. Bundle/orphan pages are always included.")
    args = ap.parse_args(argv)

    by_code = country_by_code()
    # Restrict set of country codes to apply to.
    only = set(args.only) if args.only else None
    if only:
        allowed_codes: set[str] | None = {COUNTRIES[s]["code"] for s in only if s in COUNTRIES}
    else:
        allowed_codes = None  # all

    n_city_per_country = 0
    n_city_bundle = 0
    n_city_unchanged = 0
    n_city_repositioned = 0   # already had a book-cta, now moved to new anchor
    n_city_fallback = 0       # no related-section — inserted before </main>
    n_city_no_anchor = 0      # no related-section AND no </main> — shouldn't happen
    n_hub_per_country = 0
    n_hub_bundle = 0
    n_hub_unchanged = 0
    n_master = 0

    # --- City pages --------------------------------------------------------
    city_dirs = sorted(p for p in SCAMS.iterdir() if p.is_dir() and p.name != "country")
    for cdir in city_dirs:
        p = cdir / "index.html"
        if not p.exists():
            continue
        html = p.read_text()
        cc = extract_country_code(html)
        if not cc:
            # Probably a sub-hub like /scams/research — skip silently.
            continue
        country = by_code.get(cc)
        kind = "bundle" if country is None else "per-country"
        if country is None:
            country = SERIES_BUNDLE
        if allowed_codes is not None and cc not in allowed_codes and kind == "per-country":
            continue
        city_display, scam_count = parse_page_meta(html, cdir.name)
        new_html, stats = apply_to_city_page(html, country, city_display, scam_count)
        changed = new_html != html
        if changed:
            if kind == "per-country":
                n_city_per_country += 1
            else:
                n_city_bundle += 1
            if stats["end_stripped"]:
                n_city_repositioned += 1
            if stats["end_fallback"]:
                n_city_fallback += 1
            if stats["end_inserted"] == 0 and stats["end_fallback"] == 0:
                n_city_no_anchor += 1
            flag = "[dry]" if args.dry_run else "[write]"
            if not args.dry_run:
                p.write_text(new_html)
            print(f"  {flag} /scams/{cdir.name:<30} [{kind}] cc={cc} "
                  f"mid={stats['mid']} cta_box={stats['cta_box']} "
                  f"old_aside={stats['old_book_aside']} "
                  f"end_stripped={stats['end_stripped']} "
                  f"inserted={stats['end_inserted']} "
                  f"fallback={stats['end_fallback']}")
        else:
            n_city_unchanged += 1

    # --- Country hubs ------------------------------------------------------
    hub_dir = SCAMS / "country"
    if hub_dir.exists():
        for hdir in sorted(p for p in hub_dir.iterdir() if p.is_dir()):
            p = hdir / "index.html"
            if not p.exists():
                continue
            html = p.read_text()
            cc = hdir.name.lower()
            country = by_code.get(cc)
            kind = "bundle" if country is None else "per-country"
            if country is None:
                country = SERIES_BUNDLE
            if allowed_codes is not None and cc not in allowed_codes and kind == "per-country":
                continue
            new_html, stats = apply_to_country_hub(html, country)
            changed = new_html != html
            if changed:
                if kind == "per-country":
                    n_hub_per_country += 1
                else:
                    n_hub_bundle += 1
                flag = "[dry]" if args.dry_run else "[write]"
                if not args.dry_run:
                    p.write_text(new_html)
                print(f"  {flag} /scams/country/{cc:<4} [{kind}] "
                      f"old_aside={stats['old_book_aside']} "
                      f"end_stripped={stats['end_stripped']} "
                      f"inserted={stats['hub_inserted']}")
            else:
                n_hub_unchanged += 1

    # --- Master hub --------------------------------------------------------
    # Strip-only path: the master hub at /scams/ used to receive a bundle CTA,
    # but product reverted that decision (the hub stats area should stay clean
    # so the city-grid is the next thing visible). We still strip any existing
    # block to keep the script idempotent if a stray CTA gets re-introduced.
    master_path = SCAMS / "index.html"
    if master_path.exists() and allowed_codes is None:
        html = master_path.read_text()
        new_html, n = BOOK_END_BLOCK_RE.subn("", html, count=1)
        if new_html != html:
            n_master = 1
            flag = "[dry]" if args.dry_run else "[write]"
            if not args.dry_run:
                master_path.write_text(new_html)
            print(f"  {flag} /scams/ (master hub) end_stripped={n}")

    print("\n=== SUMMARY ===")
    print(f"City pages:   {n_city_per_country} per-country, "
          f"{n_city_bundle} bundle, {n_city_unchanged} unchanged")
    print(f"              {n_city_repositioned} repositioned (stripped old CTA first), "
          f"{n_city_fallback} fallback (no related-section)")
    if n_city_no_anchor:
        print(f"              ! {n_city_no_anchor} pages had NO usable anchor — inspect")
    print(f"Country hubs: {n_hub_per_country} per-country, "
          f"{n_hub_bundle} bundle, {n_hub_unchanged} unchanged")
    print(f"Master hub:   {'touched' if n_master else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
