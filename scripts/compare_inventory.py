#!/usr/bin/env python3
"""Build and validate compare inventory artifacts.

Commands:
  extract   - backfill compare/inventory.json from the current live compare index + per-page APIs
  build     - render compare/index.html and api/v1/compare.json from compare/inventory.json
  validate  - verify compare leaf dirs, compare index, aggregate API, per-page APIs, and sitemap are in sync

This is intentionally inventory-focused phase 1 infrastructure:
- one structured source of truth for live compare cards/order/metadata
- deterministic regeneration of compare/index.html + api/v1/compare.json
- drift detection against leaf pages and sitemap
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPARE_DIR = REPO_ROOT / "compare"
API_DIR = REPO_ROOT / "api" / "v1"
INVENTORY_PATH = COMPARE_DIR / "inventory.json"
COMPARE_INDEX_PATH = COMPARE_DIR / "index.html"
COMPARE_AGG_PATH = API_DIR / "compare.json"
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"
BASE_URL = "https://tabiji.ai"

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <script async src=\"https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ\"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
    <link rel=\"icon\" type=\"image/x-icon\" href=\"/favicon.ico\">
    <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"https://img.tabiji.ai/apple-touch-icon.png\">
    <link rel=\"icon\" type=\"image/png\" sizes=\"192x192\" href=\"https://img.tabiji.ai/icon-192.png\">
    <title>Compare Destinations — Which Should You Visit? | tabiji.ai</title>
    <meta name=\"description\" content=\"{meta_description}\">
    <meta property=\"og:title\" content=\"Compare Destinations — tabiji.ai\">
    <meta property=\"og:description\" content=\"Side-by-side destination comparisons backed by real traveler data from Reddit.\">
    <meta property=\"og:type\" content=\"website\">
    <meta property=\"og:url\" content=\"https://tabiji.ai/compare/\">
    <meta name=\"robots\" content=\"index, follow, max-image-preview:large\">

    <link rel=\"canonical\" href=\"https://tabiji.ai/compare/\">

    <script type=\"application/ld+json\">
    {{
        \"@context\": \"https://schema.org\",
        \"@type\": \"CollectionPage\",
        \"name\": \"Compare Destinations\",
        \"description\": \"Data-backed destination comparisons built from Reddit discussions, real costs, and traveler preferences.\",
        \"url\": \"https://tabiji.ai/compare/\",
        \"publisher\": {{\"@type\": \"Organization\", \"name\": \"tabiji.ai\", \"url\": \"https://tabiji.ai\"}}
    }}
    </script>

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
        nav {{
            position: fixed; top: 0; width: 100%; z-index: 100;
            background: rgba(254, 252, 249, 0.92);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--sand);
            padding: 1rem 2rem;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .logo {{ font-size: 1.4rem; font-weight: 700; color: var(--indigo); text-decoration: none; letter-spacing: -0.02em; }}
        .logo span {{ color: var(--terracotta); }}
        .logo{{position:relative}}.logo .owl-fly{{display:none}}.logo:hover .owl-default{{display:none}}.logo:hover .owl-fly{{display:inline}}
        nav a.cta-nav {{
            background: var(--terracotta); color: white;
            padding: 0.5rem 1.2rem; border-radius: 8px;
            text-decoration: none; font-size: 0.9rem; font-weight: 500;
            transition: background 0.2s;
        }}
        nav a.cta-nav:hover {{ background: #b5633f; }}
        .nav-links {{ display: flex; align-items: center; gap: 1.5rem; }}
        .nav-links a {{ color: var(--indigo); text-decoration: none; font-size: 0.9rem; font-weight: 500; }}
        .nav-dropdown {{ position: relative; }}
        .nav-dropdown-toggle {{
            background: none; border: none; cursor: pointer;
            color: var(--indigo); font-size: 0.9rem; font-weight: 500; font-family: inherit;
        }}
        .nav-dropdown-toggle::after {{ content: ' ▾'; font-size: 0.7em; }}
        .nav-dropdown-menu {{
            display: none; position: absolute; top: 100%; left: 0;
            background: var(--white); border: 1px solid var(--sand); border-radius: 8px;
            padding: 0.5rem 0; min-width: 200px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        .nav-dropdown.open .nav-dropdown-menu {{ display: block; }}
        .nav-dropdown-menu a {{
            display: block; padding: 0.5rem 1rem; color: var(--text);
            text-decoration: none; font-size: 0.85rem;
        }}
        .nav-dropdown-menu a:hover {{ background: var(--warm-cream); }}
        .hamburger {{ display: none; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--indigo); }}
        @media (max-width: 768px) {{
            .hamburger {{ display: block; }}
            .nav-links {{
                display: none; flex-direction: column; position: absolute;
                top: 100%; left: 0; right: 0; background: var(--white);
                border-bottom: 1px solid var(--sand); padding: 1rem 2rem; gap: 0.8rem;
            }}
            .nav-links.open {{ display: flex; }}
            .nav-dropdown-menu {{
                position: static; box-shadow: none; border: none;
                padding-left: 1rem; margin-top: 0.3rem;
            }}
            .nav-dropdown-menu a {{ font-size: 0.85rem; padding: 0.3rem 0; }}
        }}
        .hero {{
            position: relative;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            text-align: center;
            padding: 8rem 2rem 4rem;
            background: linear-gradient(rgba(45,58,92,0.75), rgba(45,58,92,0.8)),
                        url('https://img.tabiji.ai/compare/hero-bg.webp') center/cover no-repeat;
        }}
        .hero h1 {{
            font-size: clamp(2.2rem, 5vw, 3rem);
            line-height: 1.15; font-weight: 800;
            color: #fff; margin-bottom: 1rem;
        }}
        .hero p {{
            font-size: 1.1rem; color: rgba(255,255,255,0.8);
            max-width: 600px; margin-bottom: 1.5rem;
        }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 0 2rem; }}
        .section-label {{
            display: inline-block;
            background: var(--warm-cream); color: var(--earth);
            padding: 0.3rem 0.8rem; border-radius: 100px;
            font-size: 0.8rem; font-weight: 600;
            text-transform: uppercase; letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }}
        .compare-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        .compare-card {{
            background: var(--white);
            border: 1px solid var(--sand);
            border-radius: 12px;
            overflow: hidden;
            text-decoration: none;
            color: var(--text);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .compare-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }}
        .compare-card-image {{
            height: 200px;
            background-size: cover;
            background-position: center;
            position: relative;
        }}
        .compare-card-vs {{
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            background: var(--terracotta);
            color: white;
            font-weight: 800;
            font-size: 1.1rem;
            width: 48px; height: 48px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 2;
        }}
        .compare-card-body {{ padding: 1.2rem; }}
        .compare-card-body h2 {{
            font-size: 1.2rem; font-weight: 700;
            margin-bottom: 0.5rem; color: var(--indigo);
        }}
        .compare-card-body p {{
            font-size: 0.9rem; color: var(--text-muted);
            margin-bottom: 0.8rem;
        }}
        .compare-card-tags {{
            display: flex; gap: 0.5rem; flex-wrap: wrap;
        }}
        .compare-card-tags span {{
            background: var(--warm-cream);
            color: var(--earth);
            padding: 0.2rem 0.6rem;
            border-radius: 100px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        footer {{
            margin-top: 4rem; padding: 2rem;
            border-top: 1px solid var(--sand);
            text-align: center;
            color: var(--text-muted); font-size: 0.85rem;
        }}
        footer a {{ color: var(--earth); text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
        section {{ padding: 3rem 0; }}
    </style>
<!-- @include:shared-head:start -->
<link rel=\"stylesheet\" href=\"/assets/shared-shell.css\">
<script defer src=\"/assets/shared-shell.js\"></script>
<!-- @include:shared-head:end -->
</head>
<body>
<!-- @include:nav:start -->
<nav>
    <a href=\"/\" class=\"logo\"><img class=\"owl-default\" src=\"https://img.tabiji.ai/tabiji-owl-logo.png\" alt=\"tabiji.ai\" style=\"height:32px;vertical-align:middle;margin-right:6px;\" loading=\"lazy\"><img class=\"owl-fly\" src=\"https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2\" alt=\"tabiji.ai\" style=\"height:32px;vertical-align:middle;margin-right:6px;\" loading=\"lazy\">tabiji<span>.ai</span></a>
    <button class=\"hamburger\" onclick=\"document.querySelector('.nav-links').classList.toggle('open')\" aria-label=\"Menu\">☰</button>
    <div class=\"nav-links\">
        <div class=\"nav-dropdown\">
            <button class=\"nav-dropdown-toggle\" onclick=\"this.parentElement.classList.toggle('open')\">Explore</button>
            <div class=\"nav-dropdown-menu\">
                <a href=\"/compare/\">🆚 Compare Destinations</a>
                <a href=\"/find/\">🔍 Destination Finder</a>
                <a href=\"/resources/\">📚 Resources</a>
                <a href=\"/alerts/\">🚨 Travel Alerts</a>
                <a href=\"/api/\">🔌 API</a>
            </div>
        </div>
        <a href=\"/popular-picks/\">Popular Picks</a>
        <a href="/countries/">Country Guides</a>
        <a href=\"/about/\">About</a>
        <a href=\"/plan\" class=\"cta-nav\">Get a Free Itinerary</a>
    </div>
</nav>
<!-- @include:nav:end -->

<section class=\"hero\">
    <h1>Compare Destinations</h1>
    <p>{hero_dek}</p>
</section>

<section>
    <div class=\"container\">
        <div class=\"section-label\">Live Comparisons</div>

        <div class=\"compare-grid\">
{cards}
        </div>
    </div>
</section>

<!-- @include:footer:start -->
<footer>
    <p>© 2026 tabiji.ai · <a href=\"/terms/\" style=\"color: inherit; text-decoration: underline;\">Terms of Service</a> · <a href=\"/privacy/\" style=\"color: inherit; text-decoration: underline;\">Privacy Policy</a> · <a href=\"/delete-data/\" style=\"color: inherit; text-decoration: underline;\">Delete My Data</a> · <a href=\"https://www.instagram.com/tabiji.ai/\" target=\"_blank\" rel=\"noopener\" style=\"color: inherit; text-decoration: underline;\">Instagram</a> · <a href=\"https://www.youtube.com/@tabijiai\" target=\"_blank\" rel=\"noopener\" style=\"color: inherit; text-decoration: underline;\">YouTube</a> · <a href=\"https://www.pinterest.com/tabijiai/\" target=\"_blank\" rel=\"noopener\" style=\"color: inherit; text-decoration: underline;\">Pinterest</a> · <a href=\"https://x.com/tabijiai\" target=\"_blank\" rel=\"noopener\" style=\"color: inherit; text-decoration: underline;\">X</a> · <a href=\"/media/\" style=\"color: inherit; text-decoration: underline;\">Media Studio</a> · <a href=\"/api/\" style=\"color: inherit; text-decoration: underline;\">API</a></p>
</footer>
<!-- @include:footer:end -->

<script>document.addEventListener('click',function(e){{document.querySelectorAll('.nav-dropdown.open').forEach(function(d){{if(!d.contains(e.target))d.classList.remove('open')}})}});</script>
</body>
</html>
"""

@dataclass
class CompareCard:
    slug: str
    title: str
    description: str
    tags: List[str]
    image1: str
    image2: str
    destination1: str
    destination2: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path):
    return json.loads(read_text(path))


def write_json(path: Path, data) -> None:
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def strip_html(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()


def find_all(pattern: str, text: str, flags=0):
    return list(re.finditer(pattern, text, flags))


def extract_cards_from_index(html: str) -> List[CompareCard]:
    cards = []
    pattern = re.compile(r'<a href="/compare/([^/]+)/" class="compare-card">(.*?)</a>', re.S)
    for match in pattern.finditer(html):
        slug = match.group(1)
        block = match.group(2)
        title = strip_html(re.search(r'<h2>(.*?)</h2>', block, re.S).group(1))
        description = strip_html(re.search(r'<p>(.*?)</p>', block, re.S).group(1))
        tags = [strip_html(m.group(1)) for m in re.finditer(r'<span>(.*?)</span>', block, re.S)]
        image_matches = re.findall(r"background:url\('([^']+)'\)", block)
        if len(image_matches) < 2:
            raise ValueError(f"Could not extract both images for {slug}")
        api_path = API_DIR / "compare" / f"{slug}.json"
        api_json = load_json(api_path)
        cards.append(CompareCard(
            slug=slug,
            title=title,
            description=description,
            tags=tags,
            image1=image_matches[0],
            image2=image_matches[1],
            destination1=api_json["destination1"],
            destination2=api_json["destination2"],
        ))
    return cards


def build_inventory_from_live() -> Dict:
    html = read_text(COMPARE_INDEX_PATH)
    cards = extract_cards_from_index(html)
    inventory = {
        "pageType": "compare-inventory",
        "status": "active",
        "metaDescription": "40 data-backed destination comparisons built from Reddit discussions, real costs, weather data, and traveler preferences. No fluff — just honest verdicts.",
        "heroDek": "Side-by-side comparisons backed by Reddit discussions, real costs, weather data, and traveler preferences. No fluff — just honest verdicts.",
        "cards": [card.__dict__ for card in cards],
    }
    return inventory


def render_card(card: Dict) -> str:
    tags = "\n".join(f"                        <span>{tag}</span>" for tag in card["tags"])
    return f"""
            <a href=\"/compare/{card['slug']}/\" class=\"compare-card\">
                <div class=\"compare-card-image\" style=\"background-color: var(--indigo);\">
                    <div style=\"position:absolute;inset:0;display:flex;\">
                        <div style=\"flex:1;background:url('{card['image1']}') center/cover;\"></div>
                        <div style=\"flex:1;background:url('{card['image2']}') center/cover;\"></div>
                    </div>
                    <div class=\"compare-card-vs\">VS</div>
                </div>
                <div class=\"compare-card-body\">
                    <h2>{card['destination1']} vs {card['destination2']}</h2>
                    <p>{card['description']}</p>
                    <div class=\"compare-card-tags\">
{tags}
                    </div>
                </div>
            </a>"""


def build_compare_index(inventory: Dict) -> str:
    cards_html = "\n".join(render_card(card) for card in inventory["cards"])
    meta_description = inventory.get(
        "metaDescription",
        "Compare destination head-to-head with data-backed verdicts, key differences, and honest tradeoffs.",
    )
    hero_dek = inventory.get(
        "heroDek",
        "Side-by-side destination comparisons backed by traveler data, real costs, and practical tradeoffs.",
    )
    return HEAD_TEMPLATE.format(
        meta_description=meta_description,
        hero_dek=hero_dek,
        cards=cards_html,
    )


def canonical_compare_url(url: str | None, slug: str) -> str:
    if not url:
        return f"{BASE_URL}/compare/{slug}/"
    if url.startswith("/compare/"):
        return f"{BASE_URL}{url}"
    return url


def build_compare_aggregate(inventory: Dict) -> Dict:
    comparisons = []
    for card in inventory["cards"]:
        api_path = API_DIR / "compare" / f"{card['slug']}.json"
        per_page = load_json(api_path) if api_path.exists() else {}
        category_count = per_page.get("categoryCount")
        if category_count is None:
            category_count = len(per_page.get("categories", []))
        comparisons.append({
            "slug": card["slug"],
            "title": per_page.get("title", card.get("title", f"{card.get('destination1', '')} vs {card.get('destination2', '')}")),
            "destination1": per_page.get("destination1", card.get("destination1")),
            "destination2": per_page.get("destination2", card.get("destination2")),
            "categoryCount": category_count,
            "url": canonical_compare_url(per_page.get("url"), card["slug"]),
        })
    return {"count": len(comparisons), "comparisons": comparisons}


def compare_leaf_slugs() -> List[str]:
    return sorted([p.name for p in COMPARE_DIR.iterdir() if p.is_dir() and (p / "index.html").exists()])


def sitemap_compare_slugs() -> List[str]:
    text = read_text(SITEMAP_PATH)
    return re.findall(r"<loc>https://tabiji.ai/compare/([^<]+)/</loc>", text)


def validate_leaf_page(slug: str) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    html = read_text(COMPARE_DIR / slug / "index.html")

    toc_targets = re.findall(r'href="#([^"]+)"', html)
    ids = set(re.findall(r'id="([^"]+)"', html))
    for target in sorted(set(toc_targets)):
        if target not in ids:
            errors.append(f"{slug}: anchor target missing #{target}")

    placeholder_patterns = {
        r"NT,": "unresolved NT currency placeholder",
        r"~ USD": "unresolved USD currency placeholder",
        r"/bin/zsh\\.": "shell output leaked into page copy",
    }
    for pattern, label in placeholder_patterns.items():
        if re.search(pattern, html):
            errors.append(f"{slug}: {label}")

    return errors, warnings


def validate_inventory(inventory: Dict) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    cards = inventory.get("cards", [])
    if not isinstance(cards, list) or not cards:
        errors.append("inventory.cards must be a non-empty array")
        return errors, warnings

    seen = set()
    leaf_slugs = compare_leaf_slugs()
    leaf_set = set(leaf_slugs)
    sitemap_set = set(sitemap_compare_slugs())

    agg = build_compare_aggregate(inventory)

    if agg["count"] != len(cards):
        errors.append(f"Aggregate count mismatch: {agg['count']} vs cards {len(cards)}")

    for index, card in enumerate(cards, start=1):
        slug = card.get("slug")
        if not slug or not re.fullmatch(r"[a-z0-9-]+", slug):
            errors.append(f"Card #{index} has invalid slug: {slug}")
            continue
        if slug in seen:
            errors.append(f"Duplicate slug in inventory: {slug}")
        seen.add(slug)
        for field in ["description", "image1", "image2", "destination1", "destination2"]:
            if not str(card.get(field, "")).strip():
                errors.append(f"{slug}: missing {field}")
        if not isinstance(card.get("tags"), list) or not card["tags"]:
            warnings.append(f"{slug}: tags missing or empty")
        if slug not in leaf_set:
            errors.append(f"{slug}: missing compare leaf HTML")
        else:
            leaf_errors, leaf_warnings = validate_leaf_page(slug)
            errors.extend(leaf_errors)
            warnings.extend(leaf_warnings)
        api_path = API_DIR / "compare" / f"{slug}.json"
        if not api_path.exists():
            errors.append(f"{slug}: missing per-page API JSON")
        else:
            api_json = load_json(api_path)
            if api_json.get("destination1") != card.get("destination1"):
                errors.append(f"{slug}: destination1 mismatch inventory={card.get('destination1')} api={api_json.get('destination1')}")
            if api_json.get("destination2") != card.get("destination2"):
                errors.append(f"{slug}: destination2 mismatch inventory={card.get('destination2')} api={api_json.get('destination2')}")
        if slug not in sitemap_set:
            errors.append(f"{slug}: missing from sitemap compare URLs")

    extra_leaves = sorted(leaf_set - seen)
    if extra_leaves:
        warnings.append(f"Compare leaf dirs not in inventory: {', '.join(extra_leaves)}")

    extra_sitemap = sorted(sitemap_set - seen)
    if extra_sitemap:
        warnings.append(f"Sitemap compare URLs not in inventory: {', '.join(extra_sitemap)}")

    for item in agg["comparisons"]:
        url = item.get("url")
        if not isinstance(url, str) or not url.startswith(f"{BASE_URL}/compare/"):
            errors.append(f"{item.get('slug')}: aggregate compare URL must be absolute and under /compare/ (got {url})")

    current_agg = load_json(COMPARE_AGG_PATH) if COMPARE_AGG_PATH.exists() else None
    if current_agg is not None and current_agg != agg:
        warnings.append("api/v1/compare.json differs from generated aggregate; run build")

    current_index = read_text(COMPARE_INDEX_PATH)
    generated_index = build_compare_index(inventory)
    if current_index != generated_index:
        warnings.append("compare/index.html differs from generated output; run build")

    return errors, warnings


def cmd_extract() -> int:
    inventory = build_inventory_from_live()
    write_json(INVENTORY_PATH, inventory)
    print(f"Wrote {INVENTORY_PATH.relative_to(REPO_ROOT)} with {len(inventory['cards'])} cards")
    return 0


def cmd_build() -> int:
    inventory = load_json(INVENTORY_PATH)
    index_html = build_compare_index(inventory)
    aggregate = build_compare_aggregate(inventory)
    write_text(COMPARE_INDEX_PATH, index_html)
    write_json(COMPARE_AGG_PATH, aggregate)
    print(f"Built {COMPARE_INDEX_PATH.relative_to(REPO_ROOT)}")
    print(f"Built {COMPARE_AGG_PATH.relative_to(REPO_ROOT)}")
    return 0


def cmd_validate() -> int:
    inventory = load_json(INVENTORY_PATH)
    errors, warnings = validate_inventory(inventory)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED with {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: compare inventory valid ({len(inventory['cards'])} cards, {len(warnings)} warning(s))")
    return 0


def main(argv: List[str]) -> int:
    if len(argv) < 2 or argv[1] not in {"extract", "build", "validate"}:
        print("Usage: compare_inventory.py <extract|build|validate>")
        return 1
    cmd = argv[1]
    if cmd == "extract":
        return cmd_extract()
    if cmd == "build":
        return cmd_build()
    return cmd_validate()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
