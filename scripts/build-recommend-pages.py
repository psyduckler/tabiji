#!/usr/bin/env python3
"""
Build recommendation landing pages from api/v1/recommend.json.
Generates:
  recommend/{id}/index.html  — one page per preset (top 25 results)
  recommend/index.html       — hub page listing all presets
"""

import json
import os
import html
from pathlib import Path

ROOT = Path(__file__).parent.parent
RECOMMEND_JSON = ROOT / "api/v1/recommend.json"
FILTER_JSON = ROOT / "api/v1/filter.json"
OUT_DIR = ROOT / "recommend"

# Destination pages that have real HTML detail pages at /destinations/{slug}/
FEATURED_SLUGS = {
    "bali", "bangkok", "barcelona", "london",
    "mexico-city", "paris", "rome", "tokyo"
}

NAV_HTML = """<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">☰</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/compare/">🆚 Compare Destinations</a>
                <a href="/find/">🔍 Destination Finder</a>
                <a href="/spin/">🌎 Spin the Globe</a>
                <a href="/resources/">📚 Resources</a>
                <a href="/trends/">📊 Travel Trends</a>
                <a href="/alerts/">🚨 Travel Alerts</a>
                <a href="/scams/">🚨 Tourist Scams</a>
                <a href="/credit-cards/">💳 Credit Card Benefits</a>
                <a href="/health/">🏥 Travel Health Tips</a>
                <a href="/api/">🔌 API</a>
            </div>
        </div>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/itineraries/">Itineraries</a>
        <a href="/about/">About</a>
        <a href="/plan" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>"""

FOOTER_HTML = """<footer>
    <p>© 2026 tabiji.ai · <a href="/terms/">Terms of Service</a> · <a href="/privacy/">Privacy Policy</a> · <a href="/delete-data/">Delete My Data</a> · <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener">YouTube</a> · <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener">Pinterest</a> · <a href="https://x.com/tabijiai" target="_blank" rel="noopener">X</a> · <a href="/media/">Media Studio</a> · <a href="/api/">API</a></p>
</footer>"""

SHARED_CSS = """
:root{--indigo:#2D3A5C;--terracotta:#C4704B;--warm-cream:#F5F0E8;--sand:#E8DFD0;--earth:#8B7355;--sage:#7A8B6F;--white:#FEFCF9;--text:#2C2419;--text-muted:#6B5D4F}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:var(--warm-cream);color:var(--text);min-height:100vh;-webkit-font-smoothing:antialiased}
.logo{position:relative;padding-left:38px}.logo .owl-default,.logo .owl-fly{position:absolute;left:0;top:50%;transform:translateY(-50%);transition:opacity .15s}.logo .owl-fly{opacity:0}.logo:hover .owl-default{opacity:0}.logo:hover .owl-fly{opacity:1}
footer{padding:2.5rem 2rem;text-align:center;border-top:1px solid var(--sand);color:var(--text-muted);font-size:0.82rem}
footer a{color:var(--terracotta);text-decoration:none}footer a:hover{text-decoration:underline}
.hero{text-align:center;padding:7rem 2rem 3rem;max-width:800px;margin:0 auto}
.hero-badge{display:inline-block;background:var(--sand);color:var(--earth);padding:0.3rem 1rem;border-radius:100px;font-size:0.85rem;font-weight:500;margin-bottom:1.25rem}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(1.8rem,5vw,2.8rem);color:var(--indigo);margin-bottom:0.75rem;line-height:1.2}
.hero p{color:var(--text-muted);font-size:1.05rem;max-width:580px;margin:0 auto}
.grid{max-width:1080px;margin:0 auto 60px;padding:0 20px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.07);transition:transform .2s,box-shadow .2s;text-decoration:none;color:var(--text);display:block;animation:fadeUp .4s ease both}
.card:hover{transform:translateY(-4px);box-shadow:0 8px 32px rgba(0,0,0,.12)}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
.card-img-wrap{position:relative;height:180px;overflow:hidden;background:var(--sand)}
.card-img-wrap img{width:100%;height:100%;object-fit:cover}
.card-body{padding:16px 18px 20px}
.card-body h2{font-family:'Playfair Display',serif;font-size:1.15rem;color:var(--indigo);margin-bottom:2px}
.card-country{color:var(--text-muted);font-size:0.8rem;margin-bottom:10px}
.tags{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px}
.tag{padding:3px 8px;border-radius:14px;font-size:0.7rem;font-weight:600}
.tag.vibe{background:#eef2ff;color:var(--indigo)}
.card-meta{display:flex;gap:8px;font-size:0.78rem;color:var(--text-muted);align-items:center;flex-wrap:wrap}
.safety-badge{display:inline-flex;align-items:center;padding:2px 8px;border-radius:8px;font-size:0.7rem;font-weight:700;white-space:nowrap}
.sb-1{background:#f0fdf4;color:#16a34a}.sb-2{background:#fefce8;color:#a16207}
.sb-3{background:#fff7ed;color:#ea580c}.sb-4{background:#fef2f2;color:#dc2626}
.reasons{margin-top:8px;font-size:0.77rem;color:var(--text-muted);list-style:none}
.reasons li::before{content:'✓ ';color:var(--sage)}
.score-bar{height:3px;border-radius:2px;background:var(--sand);margin-top:10px;overflow:hidden}
.score-fill{height:100%;background:var(--terracotta);border-radius:2px}
@media(max-width:768px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.grid{grid-template-columns:1fr}}
"""

PRESET_LABELS = {
    "solo-female-safe-budget": ("👩‍💼", "Solo Female Travel"),
    "warm-beach-budget": ("🏖️", "Budget Beach Trips"),
    "cultural-europe": ("🏛️", "Cultural Europe"),
    "foodie-asia": ("🍜", "Foodie Asia"),
    "adventure-south-america": ("🧗", "South America Adventure"),
    "family-safe": ("👨‍👩‍👧‍👦", "Family-Friendly"),
    "digital-nomad-budget": ("💻", "Digital Nomad"),
    "romantic-europe": ("💕", "Romantic Europe"),
    "nature-wildlife": ("🦁", "Nature & Wildlife"),
    "off-beaten-path": ("🗺️", "Off the Beaten Path"),
}

PHOTO_POOL = [
    "photo-1488646953014-85cb44e25828", "photo-1476514525535-07fb3b4ae5f1",
    "photo-1530521954074-e64f6810b32d", "photo-1501854140801-50d01698950b",
    "photo-1507525428034-b723cf961d3e", "photo-1469474968028-56623f02e42e",
    "photo-1476673160081-cf065607f449", "photo-1500534314209-a25ddb2bd429",
    "photo-1485470733090-0aae1788d5af", "photo-1464822759023-fed622ff2c3b",
    "photo-1528360983277-13d401cdc186", "photo-1499678329028-101435549a4e",
    "photo-1504214208698-ea1916a2195a", "photo-1518998053901-5348d3961a04",
    "photo-1506905925346-21bda4d32df4", "photo-1542314831-068cd1dbfeeb",
    "photo-1539037116277-4db20889f2d4", "photo-1533105079780-92b9be482077",
    "photo-1502301103665-0b95cc738daf", "photo-1580639569904-7a4b27cfb6e3",
]


def photo_for_slug(slug, w=600, q=80):
    h = 5381
    for c in (slug or ""):
        h = ((h << 5) + h + ord(c)) & 0xFFFFFFFF
    photo = PHOTO_POOL[h % len(PHOTO_POOL)]
    return f"https://images.unsplash.com/{photo}?w={w}&q={q}&fit=crop&auto=format"


def safety_badge(level):
    if not level:
        return ""
    labels = {1: "L1 Normal", 2: "L2 Caution", 3: "L3 Reconsider", 4: "L4 Avoid"}
    return f'<span class="safety-badge sb-{level}">{labels.get(level, f"L{level}")}</span>'


def dest_link(slug):
    if slug in FEATURED_SLUGS:
        return f"/destinations/{slug}/"
    return f"/find/?q={slug}"


def render_card(result, filter_item, i):
    slug = result["slug"]
    name = html.escape(result["name"])
    country = html.escape(result.get("country", ""))
    score = result.get("score", 0)
    reasons = result.get("reasons", [])

    # Enrich from filter.json if available
    vibes = []
    budget_raw = ""
    advisory_level = None
    if filter_item:
        vibes = filter_item.get("vibes", [])[:3]
        budget_raw = (filter_item.get("budget") or {}).get("raw", "")
        advisory_level = (filter_item.get("safety") or {}).get("advisoryLevel")

    badge = safety_badge(advisory_level)
    tags_html = "".join(f'<span class="tag vibe">{html.escape(v)}</span>' for v in vibes)
    meta_parts = []
    if budget_raw:
        meta_parts.append(html.escape(budget_raw))
    if badge:
        meta_parts.append(badge)
    meta_html = " · ".join(meta_parts) if meta_parts else ""

    reasons_html = ""
    if reasons:
        items_html = "".join(f"<li>{html.escape(r)}</li>" for r in reasons[:3])
        reasons_html = f'<ul class="reasons">{items_html}</ul>'

    score_pct = int(score * 100)
    link = dest_link(slug)
    img_src = photo_for_slug(slug)
    delay = round(min(i * 0.05, 0.5), 2)

    return f'''<a class="card" href="{link}" style="animation-delay:{delay}s">
  <div class="card-img-wrap">
    <img src="{img_src}" alt="{name}" loading="{'eager' if i < 6 else 'lazy'}">
  </div>
  <div class="card-body">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:6px;margin-bottom:2px">
      <h2>{name}</h2>
    </div>
    <div class="card-country">{country}</div>
    <div class="tags">{tags_html}</div>
    <div class="card-meta">{meta_html}</div>
    {reasons_html}
    <div class="score-bar"><div class="score-fill" style="width:{score_pct}%"></div></div>
  </div>
</a>'''


def build_preset_page(preset, filter_lookup):
    pid = preset["id"]
    query = preset["query"]
    filters = preset.get("filters", {})
    results = preset["results"][:25]

    emoji, label = PRESET_LABELS.get(pid, ("✈️", query.title()))

    # Build filter description
    filter_parts = []
    for k, v in filters.items():
        vlist = v if isinstance(v, list) else [v]
        filter_parts.append(f"{k.split('.')[-1]}: {', '.join(str(x) for x in vlist)}")
    filter_desc = " · ".join(filter_parts) if filter_parts else ""

    # Intro text
    intro = f"These {len(results)} destinations are handpicked for <strong>{html.escape(query)}</strong>. "
    if filter_desc:
        intro += f"Filtered by: {html.escape(filter_desc)}."

    cards_html = "\n".join(
        render_card(r, filter_lookup.get(r["slug"]), i)
        for i, r in enumerate(results)
    )

    canonical = f"https://tabiji.ai/recommend/{pid}/"
    title_esc = html.escape(f"{label} — {query.title()} | tabiji.ai")
    desc_esc = html.escape(f"Top {len(results)} destinations for {query}. Handpicked by tabiji.ai.")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title_esc}</title>
<meta name="description" content="{desc_esc}">
<meta property="og:title" content="{title_esc}">
<meta property="og:description" content="{desc_esc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{SHARED_CSS}
</style>
<!-- @include:shared-head:start -->
<link rel="stylesheet" href="/assets/shared-shell.css">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
<!-- @include:shared-head:end -->
</head>
<body>
<!-- @include:nav:start -->
{NAV_HTML}
<!-- @include:nav:end -->

<div class="hero">
  <div class="hero-badge">{emoji} Curated List</div>
  <h1>{html.escape(query.title())}</h1>
  <p>{intro}</p>
  <p style="margin-top:0.75rem"><a href="/recommend/" style="color:var(--terracotta);font-size:0.9rem;text-decoration:none">← All Recommendations</a></p>
</div>

<div style="max-width:1080px;margin:0 auto 16px;padding:0 20px;display:flex;align-items:center;justify-content:space-between">
  <span style="font-size:0.85rem;color:var(--text-muted)">{len(results)} destinations</span>
  <a href="/find/" style="font-size:0.85rem;color:var(--terracotta);text-decoration:none">🔍 Explore all destinations →</a>
</div>

<div class="grid">
{cards_html}
</div>

<!-- @include:footer:start -->
{FOOTER_HTML}
<!-- @include:footer:end -->

<script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-D7QHNRXLHJ');</script>
</body>
</html>"""


def build_hub_page(presets):
    cards_html_parts = []
    for i, preset in enumerate(presets):
        pid = preset["id"]
        query = preset["query"]
        count = len(preset.get("results", []))
        emoji, label = PRESET_LABELS.get(pid, ("✈️", query.title()))
        img_src = photo_for_slug(pid)
        delay = round(min(i * 0.05, 0.3), 2)
        cards_html_parts.append(f'''<a class="card" href="/recommend/{pid}/" style="animation-delay:{delay}s">
  <div class="card-img-wrap">
    <img src="{img_src}" alt="{html.escape(label)}" loading="{'eager' if i < 6 else 'lazy'}">
  </div>
  <div class="card-body">
    <div class="hero-badge" style="font-size:0.72rem;padding:2px 10px;margin-bottom:8px">{emoji} {count} destinations</div>
    <h2>{html.escape(label)}</h2>
    <div class="card-country" style="margin-top:4px">{html.escape(query)}</div>
  </div>
</a>''')

    cards_html = "\n".join(cards_html_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Curated Destination Recommendations | tabiji.ai</title>
<meta name="description" content="Handpicked destination recommendations for every type of traveler — solo female, budget, romance, adventure, and more.">
<meta property="og:title" content="Curated Destination Recommendations | tabiji.ai">
<meta property="og:description" content="Handpicked destinations for every type of traveler.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://tabiji.ai/recommend/">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://tabiji.ai/recommend/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{SHARED_CSS}
</style>
<!-- @include:shared-head:start -->
<link rel="stylesheet" href="/assets/shared-shell.css">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#2D3A5C">
<script defer src="/assets/shared-shell.js"></script>
<!-- @include:shared-head:end -->
</head>
<body>
<!-- @include:nav:start -->
{NAV_HTML}
<!-- @include:nav:end -->

<div class="hero">
  <div class="hero-badge">✈️ Curated Lists</div>
  <h1>Destination Recommendations</h1>
  <p>Handpicked destinations for every type of traveler, filtered by safety, budget, vibes, and more.</p>
</div>

<div style="max-width:1080px;margin:0 auto 16px;padding:0 20px">
  <a href="/find/" style="font-size:0.9rem;color:var(--terracotta);text-decoration:none">🔍 Use the full Destination Finder →</a>
</div>

<div class="grid">
{cards_html}
</div>

<!-- @include:footer:start -->
{FOOTER_HTML}
<!-- @include:footer:end -->

<script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-D7QHNRXLHJ');</script>
</body>
</html>"""


def main():
    print("Loading data…")
    with open(RECOMMEND_JSON) as f:
        recommend = json.load(f)
    with open(FILTER_JSON) as f:
        filter_data = json.load(f)

    filter_lookup = {item["slug"]: item for item in filter_data.get("items", [])}
    print(f"  filter.json: {len(filter_lookup)} items")

    presets = recommend["presets"]
    print(f"  recommend.json: {len(presets)} presets")

    # Build individual preset pages
    for preset in presets:
        pid = preset["id"]
        out_dir = OUT_DIR / pid
        out_dir.mkdir(parents=True, exist_ok=True)
        page_html = build_preset_page(preset, filter_lookup)
        out_path = out_dir / "index.html"
        out_path.write_text(page_html + '\n', encoding="utf-8")
        print(f"  ✓ recommend/{pid}/index.html  ({len(preset['results'][:25])} cards)")

    # Build hub page
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    hub_html = build_hub_page(presets)
    (OUT_DIR / "index.html").write_text(hub_html + "\n", encoding="utf-8")
    print(f"  ✓ recommend/index.html  ({len(presets)} presets)")

    print("Done.")


if __name__ == "__main__":
    main()
