#!/usr/bin/env python3
"""Roll out the new two-tier book CTA across every city scam page that has a
live country book on Amazon Kindle.

Replaces:
  1. The mid-scroll .mid-cta that pushes /plan/         → .book-mid-cta
  2. The end-of-article .cta-box that pushes /plan/     → .book-end-cta
  3. The existing small <!-- @book-cta:start -->…</aside> aside (now merged
     into the prominent end-CTA so we don't have two book CTAs stacked).

CSS for the new classes lives in assets/scams.css — already imported by every
scam page, so no per-page stylesheet work is needed.

Usage:
    python3 scripts/book-cta-rollout/apply_book_ctas.py            # apply
    python3 scripts/book-cta-rollout/apply_book_ctas.py --dry-run  # preview
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
        "cover_url": "/books/brazil-tourist-scams/covers/front-designed.svg",
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
        "cover_url": "/books/united-kingdom-tourist-scams/covers/front-designed.svg",
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
        "cover_url": "/books/germany-tourist-scams/covers/front-designed.svg",
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
# Replacement blocks.
# ----------------------------------------------------------------------------
def mid_cta_html(d: dict) -> str:
    return (
        f'    <a class="book-mid-cta" href="/books/{d["book_slug"]}/">\n'
        f'        <div class="book-mid-cta-cover">\n'
        f'            <img src="{d["cover_url"]}" alt="{d["cover_alt"]}" width="64" height="96" loading="lazy">\n'
        f'        </div>\n'
        f'        <div class="book-mid-cta-body">\n'
        f'            <div class="book-mid-cta-eyebrow">📖 tabiji.ai Travel Safety Series</div>\n'
        f'            <div class="book-mid-cta-headline">Heading beyond {{city}}? The full {d["name"]} book has {d["scam_count"]} scams across {d["city_count"]} cities — {d["top_scams_mid"]}.</div>\n'
        f'            <div class="book-mid-cta-meta">$4.99 on Kindle · Read in a single flight · Updated annually</div>\n'
        f'        </div>\n'
        f'        <span class="book-mid-cta-btn">See the book →</span>\n'
        f'    </a>'
    )


def end_cta_html(d: dict) -> str:
    return (
        f'    <!-- @book-cta:start -->\n'
        f'    <section class="book-end-cta" aria-label="{d["name"]}: Tourist Scams book">\n'
        f'        <a href="/books/{d["book_slug"]}/" class="book-end-cta-cover" aria-hidden="true">\n'
        f'            <img src="{d["cover_url"]}" alt="{d["cover_alt"]}" width="220" height="330" loading="lazy">\n'
        f'        </a>\n'
        f'        <div class="book-end-cta-body">\n'
        f'            <div class="book-end-cta-eyebrow">📖 {d["name"]}: Tourist Scams</div>\n'
        f'            <h2 class="book-end-cta-headline">You just read {{n_scams}} in {{city}}. The book has {{more}} more across {d["city_count"]} {d["place_adj"]} destinations.</h2>\n'
        f'            <p class="book-end-cta-sub">{d["top_scams_end"]} Drawn from {d["sourced_from"]}.</p>\n'
        f'            <ul class="book-end-cta-benefits">\n'
        f'                <li>{d["scam_count"]} documented scams across {d["cities_join"]}</li>\n'
        f'                <li>{d["article"]} {d["language_note"]} exit-phrase card you can screenshot to your phone</li>\n'
        f'                <li>Updated annually — buy once, re-download future editions free</li>\n'
        f'                <li>Readable in one flight — $4.99 on Amazon Kindle</li>\n'
        f'            </ul>\n'
        f'            <div class="book-end-cta-btns">\n'
        f'                <a href="/books/{d["book_slug"]}/" class="book-end-cta-primary">See what\'s inside →</a>\n'
        f'                <a href="{d["amazon_url"]}" target="_blank" rel="noopener" class="book-end-cta-secondary">Buy on Amazon · $4.99 →</a>\n'
        f'            </div>\n'
        f'        </div>\n'
        f'    </section>\n'
        f'    <!-- @book-cta:end -->'
    )


# ----------------------------------------------------------------------------
# Country hub → list of city slugs that actually exist.
# ----------------------------------------------------------------------------
def city_slugs_for(code: str) -> list[str]:
    hub = SCAMS / "country" / code / "index.html"
    if not hub.exists():
        return []
    text = hub.read_text()
    urls = re.findall(r'"url":"https://tabiji\.ai/scams/([a-z0-9-]+)/"', text)
    out = []
    seen = set()
    for slug in urls:
        if slug in ("country", code) or slug in seen:
            continue
        seen.add(slug)
        if (SCAMS / slug / "index.html").exists():
            out.append(slug)
    return out


# ----------------------------------------------------------------------------
# Per-page: extract display city name + scam count for copy interpolation.
# ----------------------------------------------------------------------------
def parse_page_meta(html: str, slug: str) -> tuple[str, int]:
    # City display name from <h1>N Tourist Scams in {City}</h1>
    m = re.search(r'<h1[^>]*>\s*(?:\d+\s+)?Tourist Scams in ([^<]+?)\s*</h1>', html)
    city = m.group(1).strip() if m else slug.replace("-", " ").title()
    # Scam count: id="scam-N" first, else fall back to "Scam #N" labels
    ids = set(re.findall(r'id="scam-(\d+)"', html))
    if ids:
        return city, len(ids)
    labels = set(re.findall(r'>Scam\s*#(\d+)<', html))
    return city, len(labels)


# ----------------------------------------------------------------------------
# Replacements.
# ----------------------------------------------------------------------------
MID_CTA_RE = re.compile(
    r'[ \t]*<div class="mid-cta">\s*<p>[^<]*(?:Like what you\'re reading|Enjoying this guide)[^<]*</p>\s*<a href="/plan/?">[^<]*</a>\s*</div>',
    re.DOTALL,
)
CTA_BOX_RE = re.compile(
    r'[ \t]*(?:<!--\s*CTA\s*-->\s*\n[ \t]*)?<div class="cta-box">\s*<h2>[^<]*</h2>\s*<p>[^<]*</p>\s*<a href="/plan/?"[^>]*>[^<]*</a>\s*</div>',
    re.DOTALL,
)
# Only match the legacy small <aside> — NOT the new <section class="book-end-cta">.
# Anchoring on `<aside ` means re-running this script is idempotent.
BOOK_ASIDE_RE = re.compile(
    r'[ \t]*<!--\s*@book-cta:start\s*-->\s*<aside\b.*?</aside>\s*<!--\s*@book-cta:end\s*-->',
    re.DOTALL,
)


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


def apply_to_page(html: str, country: dict, city_display: str, scam_count: int) -> tuple[str, dict]:
    """Return (new_html, stats)."""
    stats = {"mid": 0, "cta_box": 0, "old_book_aside": 0}
    mid = interpolate_mid(mid_cta_html(country), city_display)
    end = interpolate_end(end_cta_html(country), city_display, scam_count, country["scam_count"])

    new_html, n = MID_CTA_RE.subn(mid, html, count=1)
    stats["mid"] = n
    # Drop the old small book-cta aside — the end-CTA replaces it.
    new_html, n = BOOK_ASIDE_RE.subn("", new_html, count=1)
    stats["old_book_aside"] = n
    # Replace the itinerary cta-box with the book end-CTA.
    new_html, n = CTA_BOX_RE.subn(end, new_html, count=1)
    stats["cta_box"] = n
    return new_html, stats


# ----------------------------------------------------------------------------
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Print what would change; don't write")
    ap.add_argument("--only", nargs="*", help="Country slugs to restrict to (default: all)")
    args = ap.parse_args(argv)

    only = set(args.only) if args.only else None
    grand_total = 0
    grand_touched = 0
    grand_mid = grand_end = grand_aside = 0

    for country_slug, data in COUNTRIES.items():
        if only and country_slug not in only:
            continue
        cities = city_slugs_for(data["code"])
        print(f"\n== {data['name']:>16}  ({data['code']})  {len(cities)} cities ==")
        for slug in cities:
            grand_total += 1
            p = SCAMS / slug / "index.html"
            html = p.read_text()
            city_display, scam_count = parse_page_meta(html, slug)
            new_html, stats = apply_to_page(html, data, city_display, scam_count)
            changed = new_html != html
            if changed:
                grand_touched += 1
                grand_mid += stats["mid"]
                grand_end += stats["cta_box"]
                grand_aside += stats["old_book_aside"]
                flag = "[dry]" if args.dry_run else "[write]"
                print(f"  {flag} /scams/{slug:<22} city='{city_display}' scams={scam_count} "
                      f"mid={stats['mid']} cta_box={stats['cta_box']} "
                      f"old_aside={stats['old_book_aside']}")
                if not args.dry_run:
                    p.write_text(new_html)
            else:
                print(f"  [skip ] /scams/{slug:<22} no patterns matched")

    print(f"\n=== SUMMARY ===")
    print(f"Pages scanned:        {grand_total}")
    print(f"Pages touched:        {grand_touched}")
    print(f"mid-CTAs replaced:    {grand_mid}")
    print(f"cta-box → end-CTA:    {grand_end}")
    print(f"Old book-aside gone:  {grand_aside}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
