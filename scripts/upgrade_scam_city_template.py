#!/usr/bin/env python3
"""Upgrade city scam pages with template improvements.

Six idempotent changes per city page (skips work already applied):

1. Tighten <title> from "...— Real Stories & How to Avoid Them | tabiji.ai"
   (~85 chars) to "...— How to Avoid" (~50 chars). The suffix truncates in
   SERPs at ~60 chars; tightening reclaims the slot.
2. Tighten name="description" + og:description to <=150 chars when they
   exceed 150, truncating at the last fitting sentence boundary.
3. Add wordCount + articleSection to Article JSON-LD schema (was 0% coverage).
4. Add HowTo JSON-LD schema with one HowToStep per scam card, derived from
   each card's <div class="scam-title"> + the bullets in its
   <div class="detail-block avoid"><ul>. AI Overviews and Perplexity weight
   HowTo for "how to avoid X" queries; was 0% on city pages.
5. Add geo (GeoCoordinates) to Place schema using lat/lng from
   api/v1/destinations.json. If the page has no Place schema (UTF-8 template
   like Bangkok), create one with name + addressLocality + addressCountry +
   geo.
6. On the ~16 city pages whose Article schema author is Organization rather
   than Person, replace the author with the canonical Bernard Huang Person
   schema for E-E-A-T consistency.

Run from repo root: python3 scripts/upgrade_scam_city_template.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"
DESTINATIONS_JSON = REPO / "api" / "v1" / "destinations.json"
SKIP_DIRS = {"atlas", "everywhere", "country", "research"}

BERNARD_AUTHOR = {
    "@type": "Person",
    "name": "Bernard Huang",
    "jobTitle": "Editor",
    "image": "https://img.tabiji.ai/authors/bernard-huang.jpg",
    "url": "https://tabiji.ai/about/",
    "worksFor": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
}

JSONLD_RE = re.compile(
    r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',
    re.DOTALL,
)


def load_dest_lookup() -> dict[str, dict]:
    with open(DESTINATIONS_JSON) as f:
        data = json.load(f)
    out: dict[str, dict] = {}
    for d in data["destinations"]:
        coords = d.get("coordinates") or {}
        if "lat" in coords and "lng" in coords:
            out[d["slug"]] = {
                "name": d["name"],
                "lat": coords["lat"],
                "lng": coords["lng"],
                "country": d.get("countryCode", ""),
            }
    return out


def slug_to_name(slug: str, dest_lookup: dict[str, dict]) -> str:
    if slug in dest_lookup:
        return dest_lookup[slug]["name"]
    return slug.replace("-", " ").title()


def truncate_to_sentence(s: str, max_len: int) -> str:
    """Trim s to <=max_len at a sentence boundary. If no clean sentence
    boundary fits (e.g., long single-sentence descriptions or list-style
    em-dash structures), return s unchanged rather than cutting mid-clause —
    Google's natural SERP truncation is cleaner than a mid-list chop.
    """
    if len(s) <= max_len:
        return s
    parts = re.split(r"(?<=[.!?])\s+", s)
    out = ""
    for p in parts:
        candidate = (out + " " + p).strip() if out else p
        if len(candidate) <= max_len:
            out = candidate
        else:
            break
    if len(out) >= 100:
        return out
    return s


def tighten_title(text: str) -> str:
    return re.sub(
        r"(<title>[^<]*?)\s*—\s*[^<|]+\|\s*tabiji\.ai(</title>)",
        r"\1 — How to Avoid\2",
        text,
    )


def tighten_meta_desc(text: str, max_len: int = 150) -> str:
    def replacer(m: re.Match) -> str:
        prefix, current, suffix = m.group(1), m.group(2), m.group(3)
        if len(current) <= max_len:
            return m.group(0)
        return prefix + truncate_to_sentence(current, max_len) + suffix

    patterns = [
        # name="description" content="..."
        r'(<meta[^>]*?name="description"\s+content=")([^"]+)(")',
        # content="..." name="description"
        r'(<meta[^>]*?content=")([^"]+)("\s+name="description")',
        # og:description (both attribute orders)
        r'(<meta[^>]*?property="og:description"\s+content=")([^"]+)(")',
        r'(<meta[^>]*?content=")([^"]+)("\s+property="og:description")',
    ]
    for pat in patterns:
        text = re.sub(pat, replacer, text)
    return text


def extract_scam_cards(soup: BeautifulSoup) -> list[dict]:
    cards: list[dict] = []
    for card in soup.select(".scam-card"):
        title_el = card.select_one(".scam-title")
        avoid_ul = card.select_one(".detail-block.avoid ul")
        if not title_el or not avoid_ul:
            continue
        title = title_el.get_text(" ", strip=True)
        bullets = [li.get_text(" ", strip=True) for li in avoid_ul.find_all("li")]
        bullets = [b for b in bullets if b]
        if title and bullets:
            cards.append({"title": title, "bullets": bullets})
    return cards


def count_body_words(soup: BeautifulSoup) -> int:
    main = soup.find("div", id="main") or soup.find("main") or soup.find("body")
    if main is None:
        return 0
    return len(main.get_text(" ", strip=True).split())


def build_howto(slug: str, dest_lookup: dict[str, dict], scam_cards: list[dict]) -> dict:
    name = slug_to_name(slug, dest_lookup)
    return {
        "@type": "HowTo",
        "name": f"How to avoid tourist scams in {name}",
        "description": f"Step-by-step defenses for {len(scam_cards)} documented scams in {name}, drawn from each scam's red-flag list and avoidance script.",
        "step": [
            {
                "@type": "HowToStep",
                "position": i + 1,
                "name": f"Avoid {card['title']}",
                "text": " ".join(card["bullets"]),
            }
            for i, card in enumerate(scam_cards)
        ],
    }


def build_place(slug: str, dest_lookup: dict[str, dict]) -> dict | None:
    info = dest_lookup.get(slug)
    if not info:
        return None
    name = info["name"]
    return {
        "@type": "Place",
        "name": name,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": name,
            "addressCountry": info["country"] or "US",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": info["lat"],
            "longitude": info["lng"],
        },
    }


def upgrade_jsonld(
    text: str,
    slug: str,
    dest_lookup: dict[str, dict],
    scam_cards: list[dict],
    word_count: int,
) -> tuple[str, dict]:
    """Returns (new_text, stats_dict)."""
    stats = {
        "added_wordcount": False,
        "added_articlesection": False,
        "added_howto": False,
        "added_place_geo": False,
        "created_place": False,
        "fixed_bernard": False,
    }

    m = JSONLD_RE.search(text)
    if not m:
        return text, stats

    open_tag, body_str, close_tag = m.groups()
    try:
        data = json.loads(body_str)
    except json.JSONDecodeError as e:
        print(f"  [{slug}] JSON parse error: {e}")
        return text, stats

    if not isinstance(data, dict) or "@graph" not in data or not isinstance(data["@graph"], list):
        return text, stats

    graph = data["@graph"]

    # 3. wordCount + articleSection
    article = next((b for b in graph if isinstance(b, dict) and b.get("@type") == "Article"), None)
    if article:
        if "wordCount" not in article:
            article["wordCount"] = word_count
            stats["added_wordcount"] = True
        if "articleSection" not in article:
            article["articleSection"] = "Tourist Scams"
            stats["added_articlesection"] = True
        # 6. Bernard Person fix
        author = article.get("author")
        is_person = isinstance(author, dict) and author.get("@type") == "Person"
        if not is_person:
            article["author"] = BERNARD_AUTHOR
            stats["fixed_bernard"] = True

    # 4. HowTo
    has_howto = any(isinstance(b, dict) and b.get("@type") == "HowTo" for b in graph)
    if not has_howto and scam_cards:
        howto = build_howto(slug, dest_lookup, scam_cards)
        # Insert before FAQPage if present
        faq_idx = next(
            (i for i, b in enumerate(graph) if isinstance(b, dict) and b.get("@type") == "FAQPage"),
            None,
        )
        if faq_idx is not None:
            graph.insert(faq_idx, howto)
        else:
            graph.append(howto)
        stats["added_howto"] = True

    # 5. Place + geo
    place = next((b for b in graph if isinstance(b, dict) and b.get("@type") == "Place"), None)
    info = dest_lookup.get(slug)
    if info:
        if place is not None:
            if "geo" not in place:
                place["geo"] = {
                    "@type": "GeoCoordinates",
                    "latitude": info["lat"],
                    "longitude": info["lng"],
                }
                stats["added_place_geo"] = True
        else:
            new_place = build_place(slug, dest_lookup)
            if new_place is not None:
                graph.append(new_place)
                stats["created_place"] = True

    new_body = json.dumps(data, indent=4, ensure_ascii=False)
    new_text = text[: m.start(2)] + new_body + text[m.end(2) :]
    return new_text, stats


def upgrade_page(path: Path, slug: str, dest_lookup: dict[str, dict]) -> dict:
    text = path.read_text()
    soup = BeautifulSoup(text, "html.parser")

    scam_cards = extract_scam_cards(soup)
    word_count = count_body_words(soup)

    text = tighten_title(text)
    text = tighten_meta_desc(text)
    text, stats = upgrade_jsonld(text, slug, dest_lookup, scam_cards, word_count)

    if text != path.read_text():
        path.write_text(text)
    stats["scam_card_count"] = len(scam_cards)
    return stats


def main() -> int:
    if not DESTINATIONS_JSON.exists():
        print(f"missing: {DESTINATIONS_JSON}", file=sys.stderr)
        return 1

    dest_lookup = load_dest_lookup()
    print(f"Loaded {len(dest_lookup)} destinations with coordinates")

    totals: dict[str, int] = {}
    pages = 0
    no_dest = []

    for child in sorted(SCAMS.iterdir()):
        if not child.is_dir() or child.name in SKIP_DIRS:
            continue
        index = child / "index.html"
        if not index.exists():
            continue

        slug = child.name
        if slug not in dest_lookup:
            no_dest.append(slug)

        stats = upgrade_page(index, slug, dest_lookup)
        pages += 1
        for k, v in stats.items():
            if isinstance(v, bool) and v:
                totals[k] = totals.get(k, 0) + 1

    print(f"\nProcessed {pages} city pages")
    for k, v in sorted(totals.items()):
        print(f"  {k}: {v}")
    if no_dest:
        print(f"\n{len(no_dest)} cities not in destinations.json (no geo added):")
        for s in no_dest[:10]:
            print(f"  {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
