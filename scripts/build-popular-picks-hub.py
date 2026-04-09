#!/usr/bin/env python3
"""
build-popular-picks-hub.py — rebuild /popular-picks/index.html as a card-driven hub.

Reads popular-picks-hub-data/*.json (one per country) and writes a clean,
visually rich hub page modeled on /destinations/ and /popular-picks/{country}/.

Layers:
  1. Hero with real stats (guides / countries / cities)
  2. Featured picks — auto-picked from leaf cards with country diversity,
     overridable via popular-picks/featured.json (a list of slugs)
  3. Compact "Browse by country" chip bar (so all 1.5k+ guides remain reachable)

Usage:
  python3 scripts/build-popular-picks-hub.py
"""

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB_DATA_DIR = ROOT / "popular-picks-hub-data"
OVERRIDE_FILE = ROOT / "popular-picks" / "featured.json"
OUT_FILE = ROOT / "popular-picks" / "index.html"

NUM_FEATURED = 12


def esc(s):
    return html.escape(s or "", quote=True)


# ---------- read country hubs ----------
def load_countries():
    countries = []
    for path in sorted(HUB_DATA_DIR.glob("*.json")):
        if " 2.json" in path.name:
            continue
        try:
            with path.open() as f:
                data = json.load(f)
        except Exception as e:
            print(f"WARN: failed to read {path.name}: {e}", file=sys.stderr)
            continue
        slug = data.get("slug")
        hero = data.get("hero", {}) or {}
        label = hero.get("title") or ""
        if not slug or not label:
            continue

        sections = data.get("sections", []) or []
        cards = []
        cities = []
        for s in sections:
            city = s.get("title")
            if city:
                cities.append(city)
            for c in s.get("cards", []) or []:
                cards.append(
                    {
                        "slug": c.get("slug"),
                        "href": c.get("href"),
                        "title": c.get("title"),
                        "description": c.get("description"),
                        "badge": c.get("badge"),
                        "meta": c.get("meta") or [],
                        "image": c.get("image"),
                        "imageAlt": c.get("imageAlt"),
                        "city": city,
                        "country_slug": slug,
                        "country_label": label,
                    }
                )

        countries.append(
            {
                "slug": slug,
                "label": label,
                "cards": cards,
                "guide_count": len(cards),
                "city_count": len(set(cities)),
            }
        )
    return countries


# ---------- score a card for "featured" worthiness ----------
def score_card(card):
    title = card.get("title") or ""
    desc = card.get("description") or ""
    image = card.get("image") or ""
    meta = card.get("meta") or []

    # Required: real hero image hosted on our CDN under the leaf slug
    if not image or "img.tabiji.ai/popular-picks/" not in image:
        return -1

    # Required: title in a sane length range
    tlen = len(title)
    if tlen < 14 or tlen > 80:
        return -1

    # Filter the "12 Best paddle a kayak through hidden..." pattern where the
    # title was assembled from a sentence rather than a category — heuristic:
    # third token starts lowercase right after a leading "<n> Best".
    parts = title.split()
    if (
        len(parts) >= 3
        and parts[0].rstrip(".,").isdigit()
        and parts[1].lower() == "best"
        and parts[2]
        and parts[2][0].islower()
    ):
        return -1

    # Required: substantial description
    dlen = len(desc)
    if dlen < 60 or dlen > 220:
        return -1

    # Required: spots/places count present in meta
    spots_meta = next(
        (m for m in meta if "spot" in m.lower() or "place" in m.lower()), None
    )
    if not spots_meta:
        return -1

    score = 50
    if 22 <= tlen <= 60:
        score += 15
    if 80 <= dlen <= 180:
        score += 10

    # Reward higher pick counts
    digits = "".join(ch for ch in spots_meta if ch.isdigit())
    if digits:
        n = int(digits)
        if n >= 15:
            score += 15
        elif n >= 10:
            score += 10
        elif n >= 6:
            score += 5

    return score


# ---------- pick featured with diversity ----------
def pick_featured(countries, n=NUM_FEATURED):
    # Hand-curated override?
    if OVERRIDE_FILE.exists():
        try:
            override = json.loads(OVERRIDE_FILE.read_text())
            if isinstance(override, list) and override:
                index = {c["slug"]: c for cy in countries for c in cy["cards"]}
                picks = [index[s] for s in override if s in index]
                if picks:
                    print(
                        f"Using {len(picks)} hand-picked featured cards from "
                        f"{OVERRIDE_FILE.relative_to(ROOT)}"
                    )
                    return picks
        except Exception as e:
            print(
                f"WARN: failed to read {OVERRIDE_FILE}: {e} — falling back to auto",
                file=sys.stderr,
            )

    scored = []
    for cy in countries:
        for card in cy["cards"]:
            s = score_card(card)
            if s > 0:
                scored.append((s, card))
    scored.sort(key=lambda x: (-x[0], x[1].get("slug") or ""))

    picks = []
    seen_country = set()
    seen_city = set()

    # Round 1: max 1 per country, max 1 per city
    for _, card in scored:
        if len(picks) >= n:
            break
        if card["country_slug"] in seen_country:
            continue
        if card.get("city") and card["city"] in seen_city:
            continue
        picks.append(card)
        seen_country.add(card["country_slug"])
        if card.get("city"):
            seen_city.add(card["city"])

    # Round 2: allow 2 per country if we still need more
    if len(picks) < n:
        country_count = {}
        for p in picks:
            country_count[p["country_slug"]] = country_count.get(p["country_slug"], 0) + 1
        for _, card in scored:
            if len(picks) >= n:
                break
            if card in picks:
                continue
            if country_count.get(card["country_slug"], 0) >= 2:
                continue
            picks.append(card)
            country_count[card["country_slug"]] = country_count.get(card["country_slug"], 0) + 1

    return picks


# ---------- HTML rendering ----------
def render_card(card, eager=False):
    title = esc(card.get("title"))
    desc = esc(card.get("description"))
    image = esc(card.get("image"))
    href = esc(card.get("href"))
    badge = esc(card.get("badge"))
    alt = esc(card.get("imageAlt") or card.get("title"))
    meta = card.get("meta") or []
    meta_html = "".join(f"<span>{esc(m)}</span>" for m in meta)
    img_attrs = (
        'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    )
    return (
        f'<a href="{href}" class="pick-card">\n'
        f'  <img src="{image}" alt="{alt}" {img_attrs}>\n'
        f'  <div class="pick-card-body">\n'
        f'    <span class="card-badge">{badge}</span>\n'
        f"    <h3>{title}</h3>\n"
        f"    <p>{desc}</p>\n"
        f'    <div class="card-meta">{meta_html}</div>\n'
        f"  </div>\n"
        f"</a>"
    )


def render_country_chip(c):
    label = esc(c["label"])
    return (
        f'<a href="/popular-picks/{esc(c["slug"])}/" class="country-chip">'
        f"{label}<span class=\"chip-count\">{c['guide_count']}</span></a>"
    )


def render_html(countries, featured):
    countries_with_guides = [c for c in countries if c["guide_count"] > 0]
    total_guides = sum(c["guide_count"] for c in countries_with_guides)
    total_countries = len(countries_with_guides)
    total_cities = sum(c["city_count"] for c in countries_with_guides)

    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Featured Popular Picks",
        "numberOfItems": len(featured),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": c.get("title"),
                "url": "https://tabiji.ai" + (c.get("href") or ""),
            }
            for i, c in enumerate(featured)
        ],
    }
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://tabiji.ai/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Popular Picks",
                "item": "https://tabiji.ai/popular-picks/",
            },
        ],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What are Popular Picks?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"Popular Picks are {total_guides:,} curated shortlists of the best "
                        f"restaurants, bars, cafés, and experiences across {total_countries} "
                        "countries — built from real Reddit discussions and traveler "
                        "recommendations rather than sponsored placements."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": "How are the picks chosen?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        "Each list is researched from thousands of Reddit posts, travel "
                        "forums, and local-knowledge threads. We surface the places people "
                        "actually keep recommending, not the ones with the biggest ad budgets."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": "Are these affiliate or sponsored picks?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        "No — none of the picks are paid placements. Every guide is editorial "
                        "and based on traveler discussion patterns. Some leaf pages link to "
                        "Google Maps for navigation, but no business pays to be listed."
                    ),
                },
            },
        ],
    }

    def chip_sort_key(c):
        # Strip leading flag emoji + whitespace so we sort by country name,
        # not by the regional indicator codepoint of the flag.
        label = c["label"]
        # remove non-ASCII (flag) chars from the front
        return "".join(ch for ch in label if ord(ch) < 128).strip().lower()

    # First row (3 cards on desktop) is above-the-fold — eager load for LCP.
    featured_html = "\n    ".join(
        render_card(c, eager=(i < 3)) for i, c in enumerate(featured)
    )
    chips_html = "\n    ".join(
        render_country_chip(c)
        for c in sorted(countries_with_guides, key=chip_sort_key)
    )

    title_text = (
        f"Popular Picks — {total_guides:,} Reddit-Backed Travel Guides | tabiji.ai"
    )
    meta_desc = (
        f"{total_guides:,} curated lists of the best restaurants, bars, cafés, "
        f"and experiences across {total_countries} countries — researched from real "
        "Reddit reviews and traveler recommendations."
    )

    return f"""<!DOCTYPE html>
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
    <title>{esc(title_text)}</title>
    <meta name="description" content="{esc(meta_desc)}">
    <meta property="og:title" content="Popular Picks — tabiji.ai">
    <meta property="og:description" content="{esc(f'{total_guides:,} Reddit-backed lists across {total_countries} countries. No sponsored picks, no fluff.')}">
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://img.tabiji.ai/popular-picks/hero-bg.jpg">
    <meta property="og:url" content="https://tabiji.ai/popular-picks/">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Popular Picks — tabiji.ai">
    <meta name="twitter:description" content="{esc(f'{total_guides:,} Reddit-backed lists across {total_countries} countries.')}">
    <meta name="twitter:image" content="https://img.tabiji.ai/popular-picks/hero-bg.jpg">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="https://tabiji.ai/popular-picks/">
    <script type="application/ld+json">{json.dumps(item_list, separators=(",", ":"))}</script>
    <script type="application/ld+json">{json.dumps(breadcrumbs, separators=(",", ":"))}</script>
    <script type="application/ld+json">{json.dumps(faq, separators=(",", ":"))}</script>
    <style>
        :root {{
            --indigo: #2D3A5C;
            --indigo-light: #3D4E7A;
            --warm-cream: #F5F0E8;
            --sand: #E8DFD0;
            --earth: #8B7355;
            --earth-light: #A6906F;
            --terracotta: #C4704B;
            --deep-brown: #3E2F23;
            --sage: #7A8B6F;
            --white: #FEFCF9;
            --text: #2C2419;
            --text-muted: #6B5D4F;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            color: var(--text); background: var(--white); line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }}
        a {{ color: inherit; text-decoration: none; }}

        /* hero */
        .hero {{
            position: relative;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            text-align: center;
            padding: 9rem 2rem 4rem;
            background: url('https://img.tabiji.ai/popular-picks/hero-bg.jpg') center center / cover no-repeat;
            color: #fff;
        }}
        .hero::before {{
            content: '';
            position: absolute; inset: 0;
            background: linear-gradient(180deg, rgba(20,20,35,0.55) 0%, rgba(20,20,35,0.45) 60%, rgba(20,20,35,0.7) 100%);
            z-index: 0;
        }}
        .hero-inner {{ position: relative; z-index: 1; max-width: 820px; }}
        .hero h1 {{
            font-size: clamp(2.4rem, 5.5vw, 3.4rem);
            line-height: 1.12; font-weight: 800;
            margin-bottom: 1rem;
            letter-spacing: -0.03em;
            text-shadow: 0 2px 20px rgba(0,0,0,0.3);
        }}
        .hero p {{
            font-size: clamp(1rem, 1.6vw, 1.2rem);
            color: rgba(255,255,255,0.92);
            max-width: 680px; margin: 0 auto 1.6rem;
            text-shadow: 0 1px 8px rgba(0,0,0,0.3);
        }}
        .hero-meta {{
            display: flex; flex-wrap: wrap; gap: 0.75rem 1.5rem;
            justify-content: center;
            font-size: 0.95rem;
            color: rgba(255,255,255,0.92);
        }}
        .hero-meta span {{
            background: rgba(255,255,255,0.12);
            padding: 0.4rem 0.95rem; border-radius: 100px;
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255,255,255,0.18);
        }}

        /* generic section wrapper */
        .section {{ max-width: 1180px; margin: 0 auto; padding: 4rem 2rem; }}
        .section h2 {{
            font-size: clamp(1.6rem, 3vw, 2rem);
            color: var(--indigo); font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
        }}
        .section-sub {{
            color: var(--text-muted);
            font-size: 1rem; max-width: 720px;
            margin-bottom: 2rem;
        }}

        /* picks grid (featured) */
        .picks-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }}
        @media (max-width: 900px) {{ .picks-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media (max-width: 560px) {{ .picks-grid {{ grid-template-columns: 1fr; }} }}
        .pick-card {{
            background: var(--white);
            border: 1px solid var(--sand);
            border-radius: 16px;
            overflow: hidden;
            display: block;
            color: inherit;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        }}
        .pick-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 32px rgba(0,0,0,0.10);
            border-color: var(--terracotta);
        }}
        .pick-card img {{
            width: 100%; height: 200px;
            object-fit: cover; display: block;
            background: var(--warm-cream);
        }}
        .pick-card-body {{ padding: 1.1rem 1.25rem 1.4rem; }}
        .card-badge {{
            display: inline-block;
            font-size: 0.8rem; color: var(--earth);
            margin-bottom: 0.5rem;
        }}
        .pick-card h3 {{
            font-size: 1.1rem; font-weight: 700;
            color: var(--indigo);
            margin-bottom: 0.5rem;
            line-height: 1.3;
        }}
        .pick-card p {{
            font-size: 0.9rem; color: var(--text-muted);
            margin-bottom: 0.85rem;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .card-meta {{
            display: flex; flex-wrap: wrap; gap: 0.4rem 1rem;
            font-size: 0.82rem; color: var(--earth);
        }}

        /* country chip bar */
        .countries-section {{ background: var(--warm-cream); }}
        .country-chips {{
            display: flex; flex-wrap: wrap; gap: 0.5rem 0.6rem;
        }}
        .country-chip {{
            display: inline-flex; align-items: center; gap: 0.45rem;
            background: var(--white);
            border: 1px solid var(--sand);
            border-radius: 100px;
            padding: 0.45rem 0.95rem;
            color: var(--indigo);
            font-size: 0.92rem; font-weight: 500;
            transition: border-color 0.15s, background 0.15s, transform 0.15s;
        }}
        .country-chip:hover {{
            border-color: var(--terracotta);
            background: #fff;
            transform: translateY(-1px);
        }}
        .chip-count {{
            font-size: 0.78rem; color: var(--text-muted);
            background: var(--warm-cream);
            border-radius: 100px;
            padding: 0.05rem 0.5rem;
            font-weight: 600;
        }}
        .country-chip:hover .chip-count {{ color: var(--earth); }}

        /* bottom CTA */
        .bottom-cta {{
            text-align: center;
            padding: 4rem 2rem 5rem;
            background: var(--white);
            border-top: 1px solid var(--sand);
        }}
        .bottom-cta h2 {{
            font-size: clamp(1.5rem, 3vw, 2rem);
            color: var(--indigo);
            font-weight: 800;
            margin-bottom: 0.6rem;
        }}
        .bottom-cta p {{
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            max-width: 540px;
            margin-left: auto; margin-right: auto;
        }}
        .bottom-cta .cta-btn {{
            display: inline-block;
            background: var(--terracotta);
            color: #fff;
            padding: 0.95rem 2.2rem;
            border-radius: 10px;
            font-size: 1rem; font-weight: 600;
            transition: background 0.2s;
        }}
        .bottom-cta .cta-btn:hover {{ background: #b5633f; }}

        footer {{
            padding: 2.5rem 2rem;
            text-align: center;
            border-top: 1px solid var(--sand);
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        @media (max-width: 768px) {{
            .hero {{ padding: 7rem 1.25rem 3rem; }}
            .section {{ padding: 3rem 1.25rem; }}
            .pick-card img {{ height: 180px; }}
        }}
    </style>
    <!-- @include:shared-head:start -->
    <link rel="stylesheet" href="/assets/shared-shell.css">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#2D3A5C">
    <script defer src="/assets/shared-shell.js"></script>
    <script defer src="/assets/offline-download.js"></script>
    <!-- @include:shared-head:end -->
</head>
<body>
<!-- @include:nav:start -->
<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">☰</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/api/">🔌 API</a>
                <a href="/compare/">🆚 Compare Destinations</a>
                <a href="/credit-cards/">💳 Credit Card Benefits</a>
                <a href="/find/">🔍 Destination Finder</a>
                <a href="/resources/">📚 Resources</a>
                <a href="/scams/">🚨 Tourist Scams</a>
                <a href="/health/">🏥 Travel Health Tips</a>
            </div>
        </div>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/countries/">Country Guides</a>
        <a href="/about/">About</a>
        <a href="/plan" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>
<!-- @include:nav:end -->

<section class="hero">
  <div class="hero-inner">
    <h1>Popular Picks</h1>
    <p>Curated lists of the best restaurants, bars, cafés, and experiences — researched from real Reddit reviews and traveler recommendations. No sponsored picks, no fluff.</p>
    <div class="hero-meta">
      <span>📋 {total_guides:,} curated guides</span>
      <span>🌍 {total_countries} countries</span>
      <span>🏙️ {total_cities:,} cities &amp; areas</span>
    </div>
  </div>
</section>

<section class="section featured-section">
  <h2>✨ Featured Picks</h2>
  <p class="section-sub">A curated set of standout guides — each one researched from real Reddit reviews, with photos, neighborhoods, insider tips, and an interactive map. Refreshed regularly.</p>
  <div class="picks-grid">
    {featured_html}
  </div>
</section>

<section class="section countries-section">
  <h2>Browse by country</h2>
  <p class="section-sub">Open any country for the full city-by-city set of guides. Numbers show how many picks live inside each country hub.</p>
  <div class="country-chips">
    {chips_html}
  </div>
</section>

<section class="bottom-cta">
  <h2>Don't see what you're looking for?</h2>
  <p>We build custom AI itineraries for any destination — drawn from the same Reddit-sourced traveler intel that powers every Popular Pick.</p>
  <a href="/plan" class="cta-btn">Get a Free Itinerary</a>
</section>

<!-- @include:footer:start -->
<footer>
    <p>© 2026 tabiji.ai · <a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a> · <a href="/privacy/" style="color: inherit; text-decoration: underline;">Privacy Policy</a> · <a href="/delete-data/" style="color: inherit; text-decoration: underline;">Delete My Data</a> · <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Instagram</a> · <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">YouTube</a> · <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Pinterest</a> · <a href="https://x.com/tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">X</a> · <a href="/media/" style="color: inherit; text-decoration: underline;">Media Studio</a> · <a href="/api/" style="color: inherit; text-decoration: underline;">API</a></p>
</footer>
<!-- @include:footer:end -->

<script>
// Close Explore dropdown when clicking outside
document.addEventListener('click', function(e) {{
    var dd = document.querySelector('.nav-dropdown');
    if (dd && !dd.contains(e.target)) dd.classList.remove('open');
}});
</script>
</body>
</html>
"""


def main():
    countries = load_countries()
    print(f"Loaded {len(countries)} countries from {HUB_DATA_DIR.relative_to(ROOT)}")
    featured = pick_featured(countries)
    print(f"\nPicked {len(featured)} featured cards:")
    for c in featured:
        print(f"  - {c['country_label']:30s} {c.get('city') or '':20s} {c['title']}")
    out = render_html(countries, featured)
    OUT_FILE.write_text(out)
    print(f"\nWrote {OUT_FILE.relative_to(ROOT)} ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
