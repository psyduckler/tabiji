#!/usr/bin/env python3
"""
Generate country hub pages for tabiji.ai.

Usage:
    python3 scripts/generate_country_hubs.py

Generates:
    - /countries/{slug}/index.html  for each country
    - /countries/index.html         master index of all countries

To add a new country, add an entry to COUNTRIES below with the required fields.
"""

import json
import os
import glob
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()
YEAR = date.today().year

# ---------------------------------------------------------------------------
# Country definitions
# ---------------------------------------------------------------------------

COUNTRIES = [
    {
        "name": "Japan",
        "slug": "japan",
        "iso2": "JP",
        "flag": "\U0001F1EF\U0001F1F5",
        "continent": "Asia",
        "capital": "Tokyo",
        "currency": "\u00a5 (JPY)",
        "language": "Japanese",
        "best_time": "Mar\u2013May / Oct\u2013Nov",
        "budget": "$$\u2013$$$",
        "visa": "90-day visa-free for most",
        "advisory_level": 1,
        "advisory_color": "#16A34A",
        "advisory_bg": "#F0FDF4",
        "advisory_label": "Level 1 \u2014 Exercise Normal Precautions",
        "health_bullets": [
            "No required vaccines for most travelers",
            "Tap water is safe to drink nationwide",
            "Universal healthcare system \u2014 clinics widely available",
        ],
        "scam_cities": [
            {"city": "Tokyo", "slug": "tokyo", "count": 6},
            {"city": "Osaka", "slug": "osaka", "count": 6},
            {"city": "Kyoto", "slug": "kyoto", "count": 7},
        ],
        "itineraries": [
            {"title": "7-Day Classic Route", "slug": "7-day-japan-classic-route", "days": 7},
            {"title": "5-Day Tokyo Food & Nightlife", "slug": "5-day-tokyo-food-nightlife", "days": 5},
            {"title": "10-Day First Time", "slug": "10-day-japan-first-time", "days": 10},
            {"title": "14-Day Family", "slug": "14-day-japan-family", "days": 14},
            {"title": "7-Day Cherry Blossom", "slug": "7-day-japan-cherry-blossom", "days": 7},
        ],
        "picks_cities": [
            "tokyo", "osaka", "kyoto", "kobe", "nara", "hiroshima",
            "yokohama", "fukuoka", "sapporo", "nagoya", "sendai",
            "kanazawa", "hakone", "nikko", "kamakura", "takayama",
        ],
        "compare_keywords": [
            "japan", "tokyo", "osaka", "kyoto", "kobe", "nara",
            "hiroshima", "yokohama", "fukuoka", "sapporo", "nagoya",
            "sendai", "matsumoto", "kanazawa", "hakone", "nikko",
            "kamakura", "takayama", "nagano", "hakodate",
        ],
        "top_destinations": [
            {"name": "Tokyo", "slug": "tokyo", "photo": "https://img.tabiji.ai/find/img/tokyo.webp"},
            {"name": "Kyoto", "slug": "kyoto", "photo": "https://img.tabiji.ai/find/img/kyoto.webp"},
            {"name": "Osaka", "slug": "osaka", "photo": "https://img.tabiji.ai/find/img/osaka.webp"},
            {"name": "Sapporo", "slug": "sapporo", "photo": "https://img.tabiji.ai/find/img/sapporo.webp"},
            {"name": "Nagoya", "slug": "nagoya", "photo": "https://img.tabiji.ai/find/img/nagoya.webp"},
            {"name": "Kanazawa", "slug": "kanazawa", "photo": "https://img.tabiji.ai/find/img/kanazawa.webp"},
            {"name": "Hokkaido", "slug": "hokkaido", "photo": "https://img.tabiji.ai/find/img/hokkaido.webp"},
            {"name": "Hakuba", "slug": "hakuba", "photo": "https://img.tabiji.ai/find/img/hakuba.webp"},
            {"name": "Niseko", "slug": "niseko", "photo": "https://img.tabiji.ai/find/img/niseko.webp"},
            {"name": "Yokohama", "slug": "yokohama", "photo": "https://img.tabiji.ai/find/img/yokohama.webp"},
            {"name": "Japan Alps", "slug": "japan-alps", "photo": "https://img.tabiji.ai/find/img/japan-alps.webp"},
            {"name": "Lake Biwa", "slug": "lake-biwa", "photo": "https://img.tabiji.ai/find/img/lake-biwa.webp"},
        ],
    },
    {
        "name": "Mexico",
        "slug": "mexico",
        "iso2": "MX",
        "flag": "\U0001F1F2\U0001F1FD",
        "continent": "Americas",
        "capital": "Mexico City",
        "currency": "MXN",
        "language": "Spanish",
        "best_time": "Nov\u2013Apr",
        "budget": "$\u2013$$",
        "visa": "180-day visa-free for most",
        "advisory_level": 2,
        "advisory_color": "#F59E0B",
        "advisory_bg": "#FFFBEB",
        "advisory_label": "Level 2 \u2014 Exercise Increased Caution",
        "health_bullets": [
            "Hepatitis A vaccine recommended",
            "Tap water is NOT safe \u2014 drink bottled or filtered",
            "High altitude in Mexico City (2,240 m) \u2014 take it easy day one",
        ],
        "scam_cities": [
            {"city": "Canc\u00fan", "slug": "cancun", "count": 6},
            {"city": "Mexico City", "slug": "mexico-city", "count": 6},
            {"city": "Puerto Vallarta", "slug": "puerto-vallarta", "count": 7},
            {"city": "Cabo San Lucas", "slug": "cabo-san-lucas", "count": 7},
            {"city": "Guadalajara", "slug": "guadalajara", "count": 7},
            {"city": "Tulum", "slug": "tulum", "count": 7},
            {"city": "Playa del Carmen", "slug": "playa-del-carmen", "count": 7},
            {"city": "Cozumel", "slug": "cozumel", "count": 7},
            {"city": "Oaxaca", "slug": "oaxaca", "count": 7},
        ],
        "itineraries": [
            {"title": "5-Day Mexico City Food & Art", "slug": "5-day-mexico-city-food-art", "days": 5},
        ],
        "picks_cities": [
            "mexico-city", "cancun", "tulum", "cabo-san-lucas", "cozumel",
            "guadalajara", "oaxaca", "playa-del-carmen", "puerto-vallarta",
            "merida",
        ],
        "compare_keywords": [
            "mexico", "cancun", "tulum", "cabo", "cozumel", "guadalajara",
            "oaxaca", "playa", "puerto-vallarta",
        ],
        "top_destinations": [
            {"name": "Mexico City", "slug": "mexico-city", "photo": "https://img.tabiji.ai/find/img/mexico-city.webp"},
            {"name": "Tulum", "slug": "tulum", "photo": "https://img.tabiji.ai/find/img/tulum.webp"},
            {"name": "Oaxaca", "slug": "oaxaca", "photo": "https://img.tabiji.ai/find/img/oaxaca.webp"},
            {"name": "Cozumel", "slug": "cozumel", "photo": "https://img.tabiji.ai/find/img/cozumel.webp"},
            {"name": "Chich\u00e9n Itz\u00e1", "slug": "chichen-itza", "photo": "https://img.tabiji.ai/find/img/chichen-itza.webp"},
            {"name": "San Miguel de Allende", "slug": "san-miguel-de-allende", "photo": "https://img.tabiji.ai/find/img/san-miguel-de-allende.webp"},
            {"name": "Puerto Escondido", "slug": "puerto-escondido", "photo": "https://img.tabiji.ai/find/img/puerto-escondido.webp"},
            {"name": "Lake Chapala", "slug": "lake-chapala", "photo": "https://img.tabiji.ai/find/img/lake-chapala.webp"},
            {"name": "Canc\u00fan", "slug": "cancun", "photo": "https://img.tabiji.ai/owl-logo.png"},
            {"name": "Guadalajara", "slug": "guadalajara", "photo": "https://img.tabiji.ai/owl-logo.png"},
            {"name": "Puerto Vallarta", "slug": "puerto-vallarta", "photo": "https://img.tabiji.ai/owl-logo.png"},
            {"name": "Playa del Carmen", "slug": "playa-del-carmen", "photo": "https://img.tabiji.ai/owl-logo.png"},
        ],
    },
    {
        "name": "Italy",
        "slug": "italy",
        "iso2": "IT",
        "flag": "\U0001F1EE\U0001F1F9",
        "continent": "Europe",
        "capital": "Rome",
        "currency": "\u20ac (EUR)",
        "language": "Italian",
        "best_time": "Apr\u2013Jun / Sep\u2013Oct",
        "budget": "$$\u2013$$$",
        "visa": "90-day Schengen visa-free",
        "advisory_level": 1,
        "advisory_color": "#16A34A",
        "advisory_bg": "#F0FDF4",
        "advisory_label": "Level 1 \u2014 Exercise Normal Precautions",
        "health_bullets": [
            "No required vaccines for most travelers",
            "Tap water is safe to drink \u2014 even the street fountains in Rome",
            "EU Health Insurance Card (EHIC) accepted for EU/EEA citizens",
        ],
        "scam_cities": [
            {"city": "Rome", "slug": "rome", "count": 6},
            {"city": "Florence", "slug": "florence", "count": 6},
            {"city": "Venice", "slug": "venice", "count": 7},
            {"city": "Milan", "slug": "milan", "count": 6},
            {"city": "Naples", "slug": "naples", "count": 7},
        ],
        "itineraries": [
            {"title": "10-Day First Time Italy", "slug": "10-day-italy-first-time", "days": 10},
            {"title": "7-Day Amalfi Coast", "slug": "7-day-amalfi-coast", "days": 7},
            {"title": "5-Day Amalfi Coast", "slug": "5-day-amalfi-coast", "days": 5},
            {"title": "14-Day Amalfi & Southern Italy", "slug": "14-day-italy-amalfi-coast", "days": 14},
            {"title": "7-Day Rome & Southern Italy", "slug": "7-day-rome-southern-italy", "days": 7},
        ],
        "picks_cities": [
            "rome", "florence", "venice", "milan", "naples", "bologna",
            "turin", "palermo", "verona", "siena", "pisa", "lucca",
        ],
        "compare_keywords": [
            "italy", "rome", "florence", "venice", "milan", "naples",
            "bologna", "turin", "palermo", "sicily", "amalfi",
            "northern-italy", "southern-italy", "bari", "cinque-terre",
        ],
        "top_destinations": [
            {"name": "Rome", "slug": "rome", "photo": "https://img.tabiji.ai/find/img/rome.webp"},
            {"name": "Amalfi Coast", "slug": "amalfi-coast", "photo": "https://img.tabiji.ai/find/img/amalfi-coast.webp"},
            {"name": "Cinque Terre", "slug": "cinque-terre", "photo": "https://img.tabiji.ai/find/img/cinque-terre.webp"},
            {"name": "Lake Como", "slug": "lake-como", "photo": "https://img.tabiji.ai/find/img/lake-como.webp"},
            {"name": "Dolomites", "slug": "dolomites", "photo": "https://img.tabiji.ai/find/img/dolomites.webp"},
            {"name": "Tuscany", "slug": "tuscany", "photo": "https://img.tabiji.ai/find/img/tuscany.webp"},
            {"name": "Piedmont", "slug": "piedmont", "photo": "https://img.tabiji.ai/find/img/piedmont.webp"},
            {"name": "Palermo", "slug": "palermo-italy", "photo": "https://img.tabiji.ai/find/img/palermo-italy.webp"},
            {"name": "Cortina d'Ampezzo", "slug": "cortina-dampezzo", "photo": "https://img.tabiji.ai/find/img/cortina-dampezzo.webp"},
            {"name": "Alghero", "slug": "alghero-sardinia-italy", "photo": "https://img.tabiji.ai/find/img/alghero-sardinia-italy.webp"},
            {"name": "Cefal\u00f9", "slug": "cefalu-sicily-italy", "photo": "https://img.tabiji.ai/find/img/cefal-sicily-italy.webp"},
            {"name": "Lampedusa", "slug": "lampedusa-italy", "photo": "https://img.tabiji.ai/find/img/lampedusa-italy.webp"},
        ],
    },
]


# ---------------------------------------------------------------------------
# Data scanning helpers
# ---------------------------------------------------------------------------

def scan_popular_picks(country):
    """Find popular-picks pages that belong to this country's cities."""
    picks_dir = os.path.join(BASE_DIR, "popular-picks")
    matches = []
    for city_prefix in country["picks_cities"]:
        pattern = os.path.join(picks_dir, f"{city_prefix}*")
        for path in sorted(glob.glob(pattern)):
            slug = os.path.basename(path)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, "index.html")):
                # Convert slug to title: kyoto-ramen -> Kyoto Ramen
                title = slug.replace("-", " ").title()
                matches.append({"slug": slug, "title": title})
    # Also check for country-level picks like "best-pizza-naples"
    special_patterns = {
        "Italy": ["best-pizza-naples"],
        "Mexico": ["mexico"],
        "Japan": [],
    }
    for extra in special_patterns.get(country["name"], []):
        path = os.path.join(picks_dir, extra)
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "index.html")):
            title = extra.replace("-", " ").title()
            matches.append({"slug": extra, "title": title})
    return matches


def scan_comparisons(country):
    """Find compare pages that match this country's cities/keywords."""
    compare_dir = os.path.join(BASE_DIR, "compare")
    matches = []
    seen = set()
    for kw in country["compare_keywords"]:
        for entry in sorted(os.listdir(compare_dir)):
            if entry in seen:
                continue
            path = os.path.join(compare_dir, entry)
            if not os.path.isdir(path):
                continue
            # Match if keyword appears in the slug
            parts = entry.split("-vs-")
            if len(parts) == 2:
                if kw in entry.split("-"):
                    # Check it's a real match (not partial word match)
                    if kw in parts[0].split("-") or kw in parts[1].split("-"):
                        title = entry.replace("-vs-", " vs ").replace("-", " ").title()
                        matches.append({"slug": entry, "title": title})
                        seen.add(entry)
            elif entry == kw:
                # Hub page like "japan", "italy", "mexico"
                title = entry.replace("-", " ").title()
                matches.append({"slug": entry, "title": title})
                seen.add(entry)
    return matches


def scan_destinations_count(country_name):
    """Count destinations for a country from the API data."""
    api_path = os.path.join(BASE_DIR, "api", "v1", "destinations.json")
    try:
        with open(api_path) as f:
            data = json.load(f)
        return sum(1 for d in data["destinations"] if d.get("country") == country_name)
    except Exception:
        return 0


def scan_picks_from_api(country_name):
    """Count picks from the API directory."""
    picks_dir = os.path.join(BASE_DIR, "api", "v1", "picks")
    count = 0
    for path in glob.glob(os.path.join(picks_dir, "*.json")):
        try:
            with open(path) as f:
                data = json.load(f)
            if data.get("country") == country_name:
                count += 1
        except Exception:
            pass
    return count


# ---------------------------------------------------------------------------
# HTML generation helpers
# ---------------------------------------------------------------------------

def h(text):
    """HTML-escape text."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def pl(n, singular, plural=None):
    """Simple pluralization."""
    if plural is None:
        plural = singular + "s"
    return f"{n} {singular}" if n == 1 else f"{n} {plural}"


def nav_html():
    return """<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">\u2630</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/compare/">\U0001F19A Compare Destinations</a>
                <a href="/find/">\U0001F50D Destination Finder</a>
                <a href="/resources/">\U0001F4DA Resources</a>
                <a href="/trends/">\U0001F4CA Travel Trends</a>
                <a href="/alerts/">\U0001F6A8 Travel Alerts</a>
                <a href="/scams/">\U0001F6A8 Tourist Scams</a>
                <a href="/credit-cards/">\U0001F4B3 Credit Card Benefits</a>
                <a href="/health/">\U0001F3E5 Travel Health Tips</a>
                <a href="/api/">\U0001F50C API</a>
            </div>
        </div>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/itineraries/">Itineraries</a>
        <a href="/about/">About</a>
        <a href="/plan" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>"""


def footer_html():
    return f"""<footer>
    <p>&copy; {YEAR} tabiji.ai &middot; <a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a> &middot; <a href="/privacy/" style="color: inherit; text-decoration: underline;">Privacy Policy</a> &middot; <a href="/delete-data/" style="color: inherit; text-decoration: underline;">Delete My Data</a> &middot; <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Instagram</a> &middot; <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">YouTube</a> &middot; <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Pinterest</a> &middot; <a href="https://x.com/tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">X</a> &middot; <a href="/media/" style="color: inherit; text-decoration: underline;">Media Studio</a> &middot; <a href="/api/" style="color: inherit; text-decoration: underline;">API</a></p>
</footer>"""


# ---------------------------------------------------------------------------
# Country page generator
# ---------------------------------------------------------------------------

def generate_country_page(country):
    """Generate the full HTML for a country hub page."""
    name = country["name"]
    slug = country["slug"]
    flag = country["flag"]
    iso2 = country["iso2"]

    # Scan live data
    picks = scan_popular_picks(country)
    comparisons = scan_comparisons(country)
    dest_count = scan_destinations_count(name)

    scam_count = len(country["scam_cities"])
    compare_count = len(comparisons)
    itin_count = len(country["itineraries"])
    picks_count = len(picks)

    subtitle_parts = []
    if dest_count:
        subtitle_parts.append(pl(dest_count, "destination"))
    if scam_count:
        subtitle_parts.append(pl(scam_count, "scam guide"))
    if compare_count:
        subtitle_parts.append(pl(compare_count, "comparison"))
    if itin_count:
        subtitle_parts.append(pl(itin_count, "itinerary", "itineraries"))
    if picks_count:
        subtitle_parts.append(pl(picks_count, "popular pick"))
    subtitle = " &middot; ".join(subtitle_parts)

    meta_desc = (
        f"Your complete {name} travel guide for {YEAR}. "
        f"Explore {dest_count} destinations, scam alerts, health tips, "
        f"itineraries, and curated local picks \u2014 all backed by real traveler data."
    )

    # Compare cards (top 12)
    compare_top = comparisons[:12]
    compare_remaining = len(comparisons) - 12

    # Picks cards (top 12)
    picks_top = picks[:12]
    picks_remaining = len(picks) - 12

    # JSON-LD
    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                    {"@type": "ListItem", "position": 2, "name": "Countries", "item": "https://tabiji.ai/countries/"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": f"https://tabiji.ai/countries/{slug}/"},
                ],
            },
            {
                "@type": "TouristDestination",
                "name": name,
                "description": meta_desc,
                "url": f"https://tabiji.ai/countries/{slug}/",
                "touristType": "International travelers",
                "containedInPlace": {
                    "@type": "Country",
                    "name": name,
                },
            },
        ]
    }, indent=4)

    # Build sections

    # --- Quick Facts ---
    quick_facts_html = f"""
    <section class="section">
        <h2 class="section-title">Quick Facts</h2>
        <div class="facts-grid">
            <div class="fact-item">
                <div class="fact-label">Capital</div>
                <div class="fact-value">{h(country['capital'])}</div>
            </div>
            <div class="fact-item">
                <div class="fact-label">Currency</div>
                <div class="fact-value">{h(country['currency'])}</div>
            </div>
            <div class="fact-item">
                <div class="fact-label">Language</div>
                <div class="fact-value">{h(country['language'])}</div>
            </div>
            <div class="fact-item">
                <div class="fact-label">Best Time to Visit</div>
                <div class="fact-value">{h(country['best_time'])}</div>
            </div>
            <div class="fact-item">
                <div class="fact-label">Budget Level</div>
                <div class="fact-value">{h(country['budget'])}</div>
            </div>
            <div class="fact-item">
                <div class="fact-label">Visa</div>
                <div class="fact-value">{h(country['visa'])}</div>
            </div>
        </div>
    </section>"""

    # --- Travel Advisory ---
    advisory_html = f"""
    <section class="section">
        <h2 class="section-title">Travel Advisory</h2>
        <a href="/alerts/{slug}/" class="advisory-card" style="border-left: 4px solid {country['advisory_color']};">
            <div class="advisory-badge" style="background: {country['advisory_bg']}; color: {country['advisory_color']};">
                {h(country['advisory_label'])}
            </div>
            <p class="advisory-desc">View the full {name} travel advisory, entry requirements, and safety updates.</p>
            <span class="advisory-link">Read full advisory &rarr;</span>
        </a>
    </section>"""

    # --- Health ---
    health_bullets = "\n".join(
        f'                <li>{h(b)}</li>' for b in country["health_bullets"]
    )
    health_html = f"""
    <section class="section">
        <h2 class="section-title">Health &amp; Safety</h2>
        <div class="health-card">
            <ul class="health-list">
{health_bullets}
            </ul>
            <a href="/health/{slug}/" class="section-link">Full health guide for {name} &rarr;</a>
        </div>
    </section>"""

    # --- Scam Guides ---
    scam_cards = ""
    for sc in country["scam_cities"]:
        scam_cards += f"""
            <a href="/scams/{sc['slug']}/" class="card">
                <div class="card-body">
                    <h3 class="card-title">{h(sc['city'])}</h3>
                    <p class="card-meta">{sc['count']} scams documented</p>
                </div>
            </a>"""
    scam_html = f"""
    <section class="section">
        <h2 class="section-title">Scam Guides</h2>
        <p class="section-desc">Real tourist scams reported by Reddit travelers. Know what to watch for before you arrive.</p>
        <div class="card-grid">{scam_cards}
        </div>
    </section>"""

    # --- Popular Picks ---
    picks_cards = ""
    for pk in picks_top:
        picks_cards += f"""
            <a href="/popular-picks/{pk['slug']}/" class="card">
                <div class="card-body">
                    <h3 class="card-title">{h(pk['title'])}</h3>
                </div>
            </a>"""
    picks_view_all = ""
    if picks_remaining > 0:
        picks_view_all = f'\n        <div class="view-all-wrap"><a href="/popular-picks/" class="view-all-link">View all {picks_count} popular picks &rarr;</a></div>'
    picks_html = f"""
    <section class="section">
        <h2 class="section-title">Popular Picks</h2>
        <p class="section-desc">Curated lists of the best restaurants, bars, and experiences \u2014 backed by real reviews.</p>
        <div class="card-grid">{picks_cards}
        </div>{picks_view_all}
    </section>""" if picks else ""

    # --- Compare ---
    compare_cards = ""
    for cp in compare_top:
        compare_cards += f"""
            <a href="/compare/{cp['slug']}/" class="card">
                <div class="card-body">
                    <h3 class="card-title">{h(cp['title'])}</h3>
                </div>
            </a>"""
    compare_view_all = ""
    if compare_remaining > 0:
        compare_view_all = f'\n        <div class="view-all-wrap"><a href="/compare/" class="view-all-link">View all {compare_count} comparisons &rarr;</a></div>'
    compare_html = f"""
    <section class="section">
        <h2 class="section-title">Destination Comparisons</h2>
        <p class="section-desc">Side-by-side breakdowns to help you choose the right destination.</p>
        <div class="card-grid">{compare_cards}
        </div>{compare_view_all}
    </section>""" if comparisons else ""

    # --- Itineraries ---
    itin_cards = ""
    for it in country["itineraries"]:
        itin_cards += f"""
            <a href="/itineraries/{it['slug']}/" class="card">
                <div class="card-body">
                    <h3 class="card-title">{h(it['title'])}</h3>
                    <p class="card-meta">{it['days']} days</p>
                </div>
            </a>"""
    itin_html = f"""
    <section class="section">
        <h2 class="section-title">Sample Itineraries</h2>
        <p class="section-desc">Day-by-day itineraries built from thousands of real traveler recommendations.</p>
        <div class="card-grid">{itin_cards}
        </div>
    </section>""" if country["itineraries"] else ""

    # --- Top Destinations ---
    dest_cards = ""
    for td in country["top_destinations"]:
        dest_cards += f"""
            <a href="/destinations/{td['slug']}/" class="dest-card">
                <img src="{h(td['photo'])}" alt="{h(td['name'])}" loading="lazy" width="400" height="260">
                <div class="dest-overlay">
                    <h3>{h(td['name'])}</h3>
                </div>
            </a>"""
    dest_html = f"""
    <section class="section">
        <h2 class="section-title">Top Destinations</h2>
        <div class="dest-grid">{dest_cards}
        </div>
        <div class="view-all-wrap"><a href="/find/?continent={h(country['continent'])}" class="view-all-link">Explore all {name} destinations &rarr;</a></div>
    </section>"""

    # --- CTA ---
    cta_html = f"""
    <section class="cta-box">
        <h2>Ready to plan your {name} trip?</h2>
        <p>Get a personalized, day-by-day itinerary built from real traveler recommendations.</p>
        <a href="/plan/?destination={h(name)}" class="cta-btn">Plan My {name} Trip &rarr;</a>
    </section>"""

    # --- Full page ---
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <title>{h(name)} Travel Guide {YEAR} | tabiji.ai</title>
    <meta name="description" content="{h(meta_desc)}">
    <meta property="og:title" content="{h(name)} Travel Guide {YEAR} | tabiji.ai">
    <meta property="og:description" content="{h(meta_desc)}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai/countries/{slug}/">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{h(name)} Travel Guide {YEAR} | tabiji.ai">
    <meta name="twitter:description" content="{h(meta_desc)}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://tabiji.ai/countries/{slug}/">
    <link rel="stylesheet" href="/assets/shared-shell.css">
    <link rel="stylesheet" href="/assets/countries.css">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#2D3A5C">
    <script defer src="/assets/shared-shell.js"></script>
    <script defer src="/assets/offline-download.js"></script>

    <script type="application/ld+json">
{breadcrumb_json}
    </script>
</head>
<body>

{nav_html()}

<main>
    <div class="breadcrumb">
        <a href="/">Home</a> <span class="sep">/</span>
        <a href="/countries/">Countries</a> <span class="sep">/</span>
        <span>{h(name)}</span>
    </div>

    <section class="hero">
        <div class="hero-inner">
            <span class="hero-flag">{flag}</span>
            <h1>{h(name)} Travel Guide</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
    </section>
{quick_facts_html}
{advisory_html}
{health_html}
{scam_html}
{picks_html}
{compare_html}
{itin_html}
{dest_html}
{cta_html}
</main>

{footer_html()}

</body>
</html>"""

    return html


# ---------------------------------------------------------------------------
# Index page generator
# ---------------------------------------------------------------------------

def generate_index_page(countries_data):
    """Generate the /countries/index.html listing all countries."""
    meta_desc = (
        f"Browse travel guides by country. In-depth destination guides, scam alerts, "
        f"health tips, itineraries, and local picks for {len(countries_data)} countries."
    )

    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
            {"@type": "ListItem", "position": 2, "name": "Countries", "item": "https://tabiji.ai/countries/"},
        ],
    }, indent=4)

    country_cards = ""
    for c in countries_data:
        dest_count = scan_destinations_count(c["name"])
        scam_count = len(c["scam_cities"])
        itin_count = len(c["itineraries"])
        picks = scan_popular_picks(c)
        comparisons = scan_comparisons(c)

        stats_parts = []
        if dest_count:
            stats_parts.append(pl(dest_count, "destination"))
        if scam_count:
            stats_parts.append(pl(scam_count, "scam guide"))
        if len(comparisons):
            stats_parts.append(pl(len(comparisons), "comparison"))
        if itin_count:
            stats_parts.append(pl(itin_count, "itinerary", "itineraries"))
        stats = " &middot; ".join(stats_parts)

        country_cards += f"""
            <a href="/countries/{c['slug']}/" class="country-card">
                <span class="country-flag">{c['flag']}</span>
                <div class="country-info">
                    <h2 class="country-name">{h(c['name'])}</h2>
                    <p class="country-stats">{stats}</p>
                </div>
                <span class="country-arrow">&rarr;</span>
            </a>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <title>Travel Guides by Country | tabiji.ai</title>
    <meta name="description" content="{h(meta_desc)}">
    <meta property="og:title" content="Travel Guides by Country | tabiji.ai">
    <meta property="og:description" content="{h(meta_desc)}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai/countries/">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Travel Guides by Country | tabiji.ai">
    <meta name="twitter:description" content="{h(meta_desc)}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://tabiji.ai/countries/">
    <link rel="stylesheet" href="/assets/shared-shell.css">
    <link rel="stylesheet" href="/assets/countries.css">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#2D3A5C">
    <script defer src="/assets/shared-shell.js"></script>
    <script defer src="/assets/offline-download.js"></script>

    <script type="application/ld+json">
{breadcrumb_json}
    </script>
</head>
<body>

{nav_html()}

<main>
    <section class="hero">
        <div class="hero-inner">
            <h1>Travel Guides by Country</h1>
            <p class="hero-subtitle">In-depth guides with scam alerts, health tips, itineraries, and curated local picks</p>
        </div>
    </section>

    <section class="section">
        <div class="countries-list">{country_cards}
        </div>
    </section>
</main>

{footer_html()}

</body>
</html>"""

    return html


# ---------------------------------------------------------------------------
# CSS generation
# ---------------------------------------------------------------------------

def generate_css():
    return """:root {
    --indigo: #2D3A5C;
    --indigo-light: #3D4E7A;
    --warm-cream: #F5F0E8;
    --sand: #E8DFD0;
    --earth: #8B7355;
    --terracotta: #C4704B;
    --white: #FEFCF9;
    --text: #2C2419;
    --text-muted: #6B5D4F;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    color: var(--text);
    background: var(--white);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
}

/* ── Breadcrumb ──────────────────────────────────────── */

.breadcrumb {
    max-width: 860px;
    margin: 0 auto;
    padding: 5rem 2rem 0;
    font-size: 0.82rem;
    color: var(--text-muted);
}

.breadcrumb a {
    color: var(--text-muted);
    text-decoration: none;
}

.breadcrumb a:hover {
    color: var(--indigo);
    text-decoration: underline;
}

.breadcrumb .sep {
    margin: 0 0.4rem;
    opacity: 0.5;
}

/* ── Hero ────────────────────────────────────────────── */

.hero {
    background: var(--indigo);
    color: #fff;
    padding: 3rem 2rem 3rem;
    text-align: center;
}

.breadcrumb + .hero {
    padding-top: 2.5rem;
}

.hero-inner {
    max-width: 860px;
    margin: 0 auto;
}

.hero-flag {
    font-size: 3.5rem;
    display: block;
    margin-bottom: 0.75rem;
}

.hero h1 {
    font-size: clamp(1.8rem, 5vw, 2.8rem);
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.75);
    max-width: 600px;
    margin: 0 auto;
}

/* ── Sections ────────────────────────────────────────── */

.section {
    max-width: 860px;
    margin: 0 auto;
    padding: 2.5rem 2rem 0;
}

.section-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--indigo);
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}

.section-desc {
    font-size: 0.92rem;
    color: var(--text-muted);
    margin-bottom: 1.25rem;
    line-height: 1.55;
}

.section-link {
    display: inline-block;
    margin-top: 1rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--terracotta);
    text-decoration: none;
}

.section-link:hover {
    text-decoration: underline;
}

/* ── Quick Facts ─────────────────────────────────────── */

.facts-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    background: var(--warm-cream);
    border: 1.5px solid var(--sand);
    border-radius: 14px;
    padding: 1.5rem;
}

.fact-item {
    text-align: center;
}

.fact-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.3rem;
}

.fact-value {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text);
}

/* ── Advisory ────────────────────────────────────────── */

.advisory-card {
    display: block;
    background: var(--white);
    border: 1.5px solid var(--sand);
    border-radius: 14px;
    padding: 1.5rem;
    text-decoration: none;
    color: var(--text);
    transition: border-color 0.2s, box-shadow 0.2s;
}

.advisory-card:hover {
    border-color: var(--indigo);
    box-shadow: 0 2px 12px rgba(45, 58, 92, 0.08);
}

.advisory-badge {
    display: inline-block;
    font-size: 0.82rem;
    font-weight: 700;
    padding: 0.35rem 0.85rem;
    border-radius: 99px;
    margin-bottom: 0.75rem;
}

.advisory-desc {
    font-size: 0.92rem;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    line-height: 1.55;
}

.advisory-link {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--terracotta);
}

/* ── Health ───────────────────────────────────────────── */

.health-card {
    background: var(--white);
    border: 1.5px solid var(--sand);
    border-radius: 14px;
    padding: 1.5rem;
}

.health-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
    margin-bottom: 0.5rem;
}

.health-list li {
    font-size: 0.92rem;
    color: var(--text);
    padding-left: 1.5rem;
    position: relative;
    line-height: 1.5;
}

.health-list li::before {
    content: "\\2713";
    position: absolute;
    left: 0;
    color: #16A34A;
    font-weight: 700;
}

/* ── Card Grid ───────────────────────────────────────── */

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.75rem;
}

.card {
    display: block;
    background: var(--white);
    border: 1.5px solid var(--sand);
    border-radius: 14px;
    padding: 1.15rem 1.25rem;
    text-decoration: none;
    color: var(--text);
    transition: border-color 0.2s, box-shadow 0.2s;
}

.card:hover {
    border-color: var(--indigo);
    box-shadow: 0 2px 10px rgba(45, 58, 92, 0.08);
}

.card-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--indigo);
    margin-bottom: 0.2rem;
}

.card-meta {
    font-size: 0.78rem;
    color: var(--text-muted);
}

.view-all-wrap {
    text-align: center;
    margin-top: 1.25rem;
}

.view-all-link {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--terracotta);
    text-decoration: none;
}

.view-all-link:hover {
    text-decoration: underline;
}

/* ── Destination Photo Grid ──────────────────────────── */

.dest-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
    gap: 0.75rem;
}

.dest-card {
    position: relative;
    display: block;
    border-radius: 14px;
    overflow: hidden;
    aspect-ratio: 3 / 2;
    text-decoration: none;
}

.dest-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.3s ease;
}

.dest-card:hover img {
    transform: scale(1.05);
}

.dest-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 0.75rem 1rem;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.65));
}

.dest-overlay h3 {
    color: #fff;
    font-size: 0.92rem;
    font-weight: 700;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

/* ── CTA Box ─────────────────────────────────────────── */

.cta-box {
    max-width: 860px;
    margin: 2.5rem auto;
    padding: 2.5rem 2rem;
    background: var(--warm-cream);
    border: 1.5px solid var(--sand);
    border-radius: 14px;
    text-align: center;
}

.cta-box h2 {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--indigo);
    margin-bottom: 0.5rem;
}

.cta-box p {
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-bottom: 1.25rem;
}

.cta-btn {
    display: inline-block;
    background: var(--terracotta);
    color: #fff;
    padding: 0.8rem 1.75rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.97rem;
    text-decoration: none;
    transition: opacity 0.2s;
}

.cta-btn:hover {
    opacity: 0.88;
}

/* ── Footer ──────────────────────────────────────────── */

footer {
    padding: 3rem 2rem;
    text-align: center;
    border-top: 1px solid var(--sand);
    color: var(--text-muted);
    font-size: 0.85rem;
}

/* ── Countries Index ─────────────────────────────────── */

.countries-list {
    max-width: 860px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.country-card {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    background: var(--white);
    border: 1.5px solid var(--sand);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    text-decoration: none;
    color: var(--text);
    transition: border-color 0.2s, box-shadow 0.2s;
}

.country-card:hover {
    border-color: var(--indigo);
    box-shadow: 0 2px 12px rgba(45, 58, 92, 0.08);
}

.country-flag {
    font-size: 2.5rem;
    flex-shrink: 0;
}

.country-info {
    flex: 1;
    min-width: 0;
}

.country-name {
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--indigo);
    margin-bottom: 0.15rem;
}

.country-stats {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.country-arrow {
    font-size: 1.2rem;
    color: var(--terracotta);
    flex-shrink: 0;
    font-weight: 700;
}

/* ── Responsive ──────────────────────────────────────── */

@media (max-width: 600px) {
    .facts-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .card-grid {
        grid-template-columns: 1fr;
    }

    .dest-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .hero-flag {
        font-size: 2.5rem;
    }

    .hero h1 {
        font-size: 1.6rem;
    }

    .breadcrumb {
        padding-top: 4.5rem;
    }
}

@media (max-width: 400px) {
    .dest-grid {
        grid-template-columns: 1fr;
    }

    .facts-grid {
        grid-template-columns: 1fr;
    }
}
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Generating country hub pages...")
    print(f"Base directory: {BASE_DIR}")

    # Create CSS
    css_path = os.path.join(BASE_DIR, "assets", "countries.css")
    css = generate_css()
    with open(css_path, "w") as f:
        f.write(css)
    print(f"  Wrote {css_path}")

    # Generate each country page
    for country in COUNTRIES:
        slug = country["slug"]
        out_dir = os.path.join(BASE_DIR, "countries", slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.html")
        html = generate_country_page(country)
        with open(out_path, "w") as f:
            f.write(html)

        # Print summary
        picks = scan_popular_picks(country)
        comparisons = scan_comparisons(country)
        dest_count = scan_destinations_count(country["name"])
        print(
            f"  {country['name']:8s} -> {out_path}"
            f"  ({dest_count} dests, {len(comparisons)} compares, {len(picks)} picks)"
        )

    # Generate index page
    index_dir = os.path.join(BASE_DIR, "countries")
    os.makedirs(index_dir, exist_ok=True)
    index_path = os.path.join(index_dir, "index.html")
    html = generate_index_page(COUNTRIES)
    with open(index_path, "w") as f:
        f.write(html)
    print(f"  Index  -> {index_path}")

    print("Done.")


if __name__ == "__main__":
    main()
