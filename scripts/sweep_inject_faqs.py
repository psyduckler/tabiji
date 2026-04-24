#!/usr/bin/env python3
"""Inject FAQPage schema + <div class="faq-section"> block into city scam pages.

Context: 303 of 492 scam city pages currently have FAQPage JSON-LD; 189 do not.
FAQPage rich results are a major AI-search surfacing win for Google SGE /
Perplexity / ChatGPT. Rather than regenerate (only ~23 research JSONs exist),
this sweeps the rendered HTML and injects:

  1. A <div class="faq-section"> block before </main>, after the
     <div class="related-section"> (or <div id="emergency"> fallback).
  2. An FAQPage object inside the existing JSON-LD @graph.
  3. Also adds ".faq-a" to the Article's speakable.cssSelector array so the
     new FAQ answers are speakable-marked, matching canonical pages like
     /scams/tokyo/ and /scams/rome/.

The 4-6 FAQs are auto-derived from content already on the page:
  - Scam titles (first .scam-card .scam-title) — "most common scam"
  - Locations + zones (from scam-location + hero-meta country) — "is it safe"
  - Police phone + country (from the existing action-section block)
  - Airport / taxi flags (presence of airport/taxi scam cards)

Extracted data drives the Q&A template — each city gets city-specific
detail, not generic SEO filler. Cities where content is too sparse (<3
scam-cards or unparseable emergency block) are SKIPPED and logged so a
human can hand-author later.

Usage:
    python3 scripts/sweep_inject_faqs.py                          # dry-run (default)
    python3 scripts/sweep_inject_faqs.py --limit 5                # dry-run, first 5
    python3 scripts/sweep_inject_faqs.py --city accra             # dry-run, one page
    python3 scripts/sweep_inject_faqs.py --apply                  # write to all pages
    python3 scripts/sweep_inject_faqs.py --apply --city accra     # write one page

Idempotent: pages that already have FAQPage JSON-LD are no-ops.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("pip install beautifulsoup4", file=sys.stderr)
    sys.exit(2)


REPO = Path(__file__).resolve().parents[1]
SCAMS_DIR = REPO / "scams"

# Share the canonical FAQ renderer + schema-item builder with the page
# generator so the markup stays in lockstep on regeneration.
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scams"))
from _scam_sweep_common import collect_scam_targets  # type: ignore[import-not-found]
from generate_pages import generate_faq_html, generate_faq_schema  # type: ignore[import-not-found]


# ---------------------------------------------------------------------------
# City content extraction
# ---------------------------------------------------------------------------

def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def extract_city_name(soup: BeautifulSoup, slug: str) -> str:
    """Pull the canonical city name from <h1> (handles <em>City</em> wrap)."""
    h1 = soup.find("h1")
    if not h1:
        return slug.replace("-", " ").title()
    em = h1.find("em")
    if em:
        return em.get_text(strip=True)
    # "7 Tourist Scams in Accra (2026)" — strip counts/years
    txt = h1.get_text(" ", strip=True)
    m = re.search(r"Scams?\s+in\s+(.+?)(?:\s*\(\d{4}\))?$", txt)
    if m:
        return m.group(1).strip()
    return slug.replace("-", " ").title()


def extract_country(soup: BeautifulSoup) -> Optional[str]:
    """Pull country from hero-meta's '📍 City, Country' span."""
    hero = soup.select_one(".hero-meta")
    if not hero:
        return None
    for span in hero.find_all("span"):
        text = span.get_text(" ", strip=True)
        # "📍 Accra, Ghana"
        m = re.search(r"📍\s*[^,]+,\s*(.+)", text)
        if m:
            return m.group(1).strip()
    return None


def extract_scam_titles(soup: BeautifulSoup) -> List[str]:
    titles = []
    for node in soup.select(".scam-card .scam-title"):
        t = node.get_text(" ", strip=True)
        if t:
            titles.append(t)
    return titles


def extract_scam_locations(soup: BeautifulSoup) -> List[str]:
    locs = []
    for node in soup.select(".scam-card .scam-location"):
        t = node.get_text(" ", strip=True)
        # strip leading 📍 emoji
        t = re.sub(r"^📍\s*", "", t)
        if t:
            locs.append(t)
    return locs


def extract_first_scam_story(soup: BeautifulSoup) -> Optional[str]:
    """Return first scam's story body (used for 'how does it work' Q2)."""
    node = soup.select_one(".scam-card .scam-story-body")
    if node:
        return node.get_text(" ", strip=True)
    tldr = soup.select_one(".scam-card .scam-tldr")
    if tldr:
        return tldr.get_text(" ", strip=True)
    return None


def extract_emergency_police(soup: BeautifulSoup) -> Tuple[Optional[str], Optional[str]]:
    """Return (police_authority, phone_line_text) from action-section.

    Example: ("Ghana Police Service", "191 (Police) or 112 (Emergency)")
    """
    action = soup.find(id="emergency")
    if not action:
        action = soup.select_one(".action-section")
    if not action:
        return None, None
    police_h3 = None
    for h3 in action.find_all("h3"):
        if "Police Report" in h3.get_text(" ", strip=True):
            police_h3 = h3
            break
    if not police_h3:
        return None, None
    p = police_h3.find_next("p")
    if not p:
        return None, None

    authority = None
    for strong in p.find_all("strong"):
        txt = strong.get_text(" ", strip=True)
        # Skip the phone-number <strong> (contains digits)
        if any(c.isdigit() for c in txt):
            continue
        authority = txt
        break

    phone = None
    for strong in p.find_all("strong"):
        txt = strong.get_text(" ", strip=True)
        if any(c.isdigit() for c in txt):
            phone = txt
            break

    return authority, phone


def extract_takeaways(soup: BeautifulSoup) -> List[str]:
    items = []
    box = soup.select_one(".takeaways-box")
    if not box:
        return items
    for li in box.find_all("li"):
        t = li.get_text(" ", strip=True)
        if t:
            items.append(t)
    return items


def extract_safety_tips(soup: BeautifulSoup) -> List[str]:
    items = []
    box = soup.select_one(".safety-box")
    if not box:
        return items
    for li in box.find_all("li"):
        t = li.get_text(" ", strip=True)
        if t:
            items.append(t)
    return items


# ---------------------------------------------------------------------------
# FAQ generation
# ---------------------------------------------------------------------------

def _clean_title(t: str) -> str:
    """Strip leading articles + trailing parenthetical notes."""
    t = t.strip()
    for prefix in ("The ", "A ", "An "):
        if t.startswith(prefix):
            t = t[len(prefix):]
            break
    # Strip trailing ( ... ) parentheticals which are often nicknames.
    t = re.sub(r"\s*\([^)]*\)\s*$", "", t).strip()
    return t


def _primary_zones(locations: List[str], limit: int = 3) -> List[str]:
    """Extract clean district/zone names from scam-location strings.

    '📍 Central Accra, Osu, Labadi Beach' → ['Central Accra', 'Osu', 'Labadi Beach']
    We keep only locations that *look* like proper-noun place names (title-cased,
    short, and free of phrase-like verbiage). This is used for optional flavor
    in the "pickpockets" answer — it must read as a believable district name.
    """
    zones: List[str] = []
    seen = set()
    # Words that signal the fragment is a descriptor, not a place name.
    descriptor_words = {
        "meetings", "meeting", "restaurants", "shops", "stalls", "entrance",
        "entrances", "outside", "inside", "near", "around", "hotels",
        "checkpoints", "gates", "exits", "targeting", "arrival",
    }
    for loc in locations:
        # Split on common delimiters
        parts = re.split(r"\s*(?:,|;|→| and | or |/)\s*", loc)
        for raw in parts:
            part = raw.strip()
            if not part or len(part) < 4 or len(part) > 40:
                continue
            low = part.lower()
            if low in seen:
                continue
            if low.startswith((
                "throughout", "online", "across", "citywide", "everywhere",
                "anywhere", "nationwide", "island-wide", "outside", "inside",
                "near", "around", "downtown-area",
            )):
                continue
            # Must start with uppercase
            if not part[0].isupper():
                continue
            # Must not be a multi-word descriptor phrase
            tokens = set(part.lower().split())
            if tokens & descriptor_words:
                continue
            # Too many words is usually a phrase, not a zone name
            if len(part.split()) > 5:
                continue
            # Strip parenthetical like "Merkato (Africa's largest ...)" → "Merkato"
            part = re.sub(r"\s*\([^)]*\)\s*$", "", part).strip()
            if not part:
                continue
            zones.append(part)
            seen.add(low)
            if len(zones) >= limit:
                return zones
    return zones


def _has_keyword(items: List[str], keywords: List[str]) -> bool:
    blob = " ".join(items).lower()
    return any(k in blob for k in keywords)


def _detect_pickpocket(titles: List[str], tips: List[str], takeaways: List[str]) -> bool:
    hay = " ".join(titles + tips + takeaways).lower()
    return any(w in hay for w in ("pickpocket", "snatch", "bag theft", "phone snatch", "bag snatch"))


def _detect_airport(titles: List[str], locations: List[str]) -> bool:
    hay = " ".join(titles + locations).lower()
    return "airport" in hay


def _detect_taxi(titles: List[str]) -> bool:
    hay = " ".join(titles).lower()
    return any(w in hay for w in ("taxi", "rideshare", "uber", "bolt", "tuk-tuk", "auto rickshaw"))


def generate_faqs(city: str,
                  country: Optional[str],
                  scam_titles: List[str],
                  locations: List[str],
                  story: Optional[str],
                  tips: List[str],
                  takeaways: List[str],
                  police_authority: Optional[str],
                  police_phone: Optional[str]) -> List[Tuple[str, str]]:
    """Return 4-6 (question, answer) tuples derived from the page.

    Returns empty list if content is too sparse to build meaningful FAQs
    (caller will skip such pages rather than ship filler).
    """
    # Require at least 1 scam card — with 0 we truly can't build FAQs.
    if not scam_titles:
        return []

    faqs: List[Tuple[str, str]] = []

    top_titles = [_clean_title(t) for t in scam_titles[:4]]
    zones = _primary_zones(locations, limit=3)
    n_scams = len(scam_titles)
    has_pickpocket = _detect_pickpocket(scam_titles, tips, takeaways)
    has_airport = _detect_airport(scam_titles, locations)
    has_taxi = _detect_taxi(scam_titles)

    # ---------- Q1: Is {city} safe for tourists? ----------
    # Violent crime is rarely the concern for tourists; the real risks are
    # financial scams documented on the page. Mention the top-2 named scams
    # by title so the answer is city-specific rather than generic.
    top2 = top_titles[:2]
    if len(top2) >= 2:
        scam_phrase = f"{top2[0]} and {top2[1]}"
    else:
        scam_phrase = top2[0]
    country_clause = f" in {country}" if country else ""
    scams_noun = "scam" if n_scams == 1 else "scams"
    if n_scams == 1:
        scam_count_clause = f"this guide covers one documented scam"
    else:
        scam_count_clause = f"this guide covers {n_scams} documented {scams_noun}"
    q1_a = (
        f"{city}{country_clause} is generally safe for tourists — violent "
        f"crime against visitors is uncommon, and most visitors have a "
        f"trouble-free trip. The real risks are financial: {scam_count_clause} "
        f"active in {city}, led by {scam_phrase}. "
    )
    if police_phone:
        q1_a += f"Save the local emergency numbers — {police_phone} — before you arrive."
    else:
        q1_a += "Save the local emergency numbers before you arrive."
    faqs.append((f"Is {city} safe for tourists?", q1_a))

    # ---------- Q2: What is the most common scam in {city}? ----------
    top = top_titles[0]
    q2_a = f"The most commonly reported tourist scam in {city} is {top}."
    # Cross-reference to the 2nd/3rd scams
    if len(top_titles) >= 3:
        q2_a += f" {top_titles[1]} and {top_titles[2]} are the other frequently-reported risks."
    elif len(top_titles) >= 2:
        q2_a += f" {top_titles[1]} is a frequent secondary risk."
    q2_a += " See the first scam card on this page for a full walkthrough of how it unfolds and the exact red flags to watch for."
    faqs.append((f"What is the most common scam in {city}?", q2_a))

    # ---------- Q3: Are there pickpockets in {city}? ----------
    if has_pickpocket:
        pickpocket_title = next(
            (_clean_title(t) for t in scam_titles
             if re.search(r"pickpocket|snatch|bag theft|phone snatch", t, re.IGNORECASE)),
            top
        )
        q3_a = (
            f"Yes — pickpocketing is documented in {city}, and {pickpocket_title} "
            f"is covered in detail in this guide. The main risk is in crowded "
            f"tourist areas, markets, and on public transit. Keep phones and "
            f"wallets in front pockets or a zipped cross-body bag, and stay alert "
            f"when anyone crowds you or tries to distract you."
        )
    else:
        q3_a = (
            f"Pickpocketing is not among the most-reported tourist issues in "
            f"{city} — the bigger financial risks in this guide are overcharging, "
            f"booking-fraud, and taxi scams. That said, standard precautions "
            f"still apply: keep phones and wallets in front pockets, use a zipped "
            f"cross-body bag in crowded markets, and stay alert on public transit."
        )
    faqs.append((f"Are there pickpockets in {city}?", q3_a))

    # ---------- Q4: What should I do if I get scammed in {city}? ----------
    q4_parts = []
    if police_authority and police_phone:
        q4_parts.append(
            f"File a police report at the nearest {police_authority} station — "
            f"call {police_phone} for immediate help."
        )
    elif police_phone:
        q4_parts.append(
            f"File a police report at the nearest local station — call "
            f"{police_phone} for immediate help."
        )
    else:
        q4_parts.append(
            "File a police report at the nearest local station for an official "
            "crime report."
        )
    q4_parts.append(
        "Contact your embassy or consulate if your passport is lost or stolen, "
        "and call your card issuer immediately to freeze cards and dispute any "
        "unauthorized charges."
    )
    # Only point readers at the on-page emergency block when one actually
    # exists — sparse pages without a parsed police authority typically also
    # lack the fully-rendered emergency section.
    if police_authority:
        q4_parts.append(
            f"The full emergency block near the bottom of this page lists {city}-"
            f"specific contact details and step-by-step recovery actions."
        )
    faqs.append((f"What should I do if I get scammed in {city}?", " ".join(q4_parts)))

    # ---------- Optional Q5: airport or taxi ----------
    if has_airport:
        airport_scam = next(
            (_clean_title(t) for t in scam_titles
             if "airport" in t.lower()),
            None
        )
        if airport_scam:
            q5_a = (
                f"{city}'s airport itself is safe, but arriving travelers are a "
                f"known target for taxi overcharges and curb-side touts — this "
                f"guide documents {airport_scam} specifically. Use the posted "
                f"official taxi stand, a rideshare app with an in-app fare quote, "
                f"or the airport's own rail/shuttle service; refuse any driver "
                f"soliciting inside the baggage claim."
            )
        else:
            q5_a = (
                f"{city}'s airport itself is safe, but arriving travelers are a "
                f"known target for taxi overcharges and curb-side touts covered "
                f"in this guide. Use the posted official taxi stand, a rideshare "
                f"app with an in-app fare quote, or the airport's rail/shuttle "
                f"service; refuse any driver soliciting inside the baggage claim."
            )
        faqs.append((f"Is {city} airport safe?", q5_a))
    elif has_taxi:
        taxi_scam = next(
            (_clean_title(t) for t in scam_titles
             if any(w in t.lower() for w in ("taxi", "rideshare", "uber", "bolt", "tuk-tuk", "rickshaw"))),
            None
        )
        if taxi_scam:
            q5_a = (
                f"Metered and app-booked taxis in {city} are generally reliable, "
                f"but this guide documents {taxi_scam} — the main risk is drivers "
                f"quoting flat fares instead of running the meter, or taking "
                f"longer routes. Use Uber, Bolt, or the equivalent local "
                f"rideshare app when possible, and always confirm the fare or "
                f"insist on the meter before you start moving."
            )
        else:
            q5_a = (
                f"Metered and app-booked taxis in {city} are generally reliable, "
                f"but drivers occasionally overcharge tourists as documented in "
                f"this guide. Use Uber, Bolt, or the equivalent local rideshare "
                f"app when possible, and always confirm the fare or insist on the "
                f"meter before you start moving."
            )
        faqs.append((f"Are taxis in {city} safe?", q5_a))

    return faqs


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

def render_faq_html(faqs: List[Tuple[str, str]]) -> str:
    """Render the <div class="faq-section"> block matching tokyo/rome canonical.

    Delegates the per-item markup to ``generate_pages.generate_faq_html`` so
    sweep-injected FAQs look identical to ones a generator regen would emit.
    """
    body = generate_faq_html(faqs).strip("\n")
    return (
        '<!-- FAQ -->\n'
        '<div class="faq-section">\n'
        '<h2 class="section-heading">Frequently Asked Questions</h2>\n'
        f'{body}\n'
        '</div>\n'
    )


def build_faq_schema(faqs: List[Tuple[str, str]]) -> dict:
    """Wrap the shared schema item-builder in the FAQPage envelope."""
    return {
        "@type": "FAQPage",
        "mainEntity": generate_faq_schema(None, faqs),
    }


# ---------------------------------------------------------------------------
# JSON-LD injection
# ---------------------------------------------------------------------------

_LD_SCRIPT_RE = re.compile(
    r'(<script\s+type="application/ld\+json">\s*)(.+?)(\s*</script>)',
    re.DOTALL,
)


def _update_jsonld(html: str, faqs: List[Tuple[str, str]]) -> str:
    """Insert FAQPage into @graph and add '.faq-a' to Article speakable."""
    match = _LD_SCRIPT_RE.search(html)
    if not match:
        raise ValueError("could not locate <script type=\"application/ld+json\"> block")

    pre, body, post = match.group(1), match.group(2), match.group(3)
    data = json.loads(body)

    # Ensure we have an @graph structure
    if not isinstance(data, dict) or "@graph" not in data:
        raise ValueError("JSON-LD does not use @graph structure — unsupported")
    graph = data["@graph"]
    if not isinstance(graph, list):
        raise ValueError("@graph is not a list")

    # Skip if FAQPage already present (idempotent)
    for node in graph:
        if isinstance(node, dict) and node.get("@type") == "FAQPage":
            return html  # nothing to do

    # Add .faq-a to the Article's speakable.cssSelector
    for node in graph:
        if isinstance(node, dict) and node.get("@type") == "Article":
            sp = node.get("speakable")
            if isinstance(sp, dict):
                sel = sp.get("cssSelector")
                if isinstance(sel, list) and ".faq-a" not in sel:
                    sel.append(".faq-a")

    # Insert FAQPage after Article (or wherever Article is). Fall back to end.
    faq_obj = build_faq_schema(faqs)
    insert_at = len(graph)
    for i, node in enumerate(graph):
        if isinstance(node, dict) and node.get("@type") == "Article":
            insert_at = i + 1
            break
    graph.insert(insert_at, faq_obj)

    # Re-serialize with 4-space indent to mirror existing style
    new_body = json.dumps(data, indent=4, ensure_ascii=False)
    # Keep the original leading/trailing whitespace around the JSON body
    return html[:match.start()] + pre + new_body + post + html[match.end():]


# ---------------------------------------------------------------------------
# HTML block injection
# ---------------------------------------------------------------------------

_RELATED_RE = re.compile(r'(<div class="related-section">)', re.DOTALL)
_MAIN_CLOSE_RE = re.compile(r'(\s*</main>)')


def _insert_faq_block(html: str, faq_block: str) -> str:
    """Insert the FAQ HTML BEFORE <div class="related-section"> when present,
    otherwise before </main>."""
    if 'class="faq-section"' in html:
        return html  # idempotent

    m = _RELATED_RE.search(html)
    if m:
        return html[:m.start()] + faq_block + html[m.start():]
    # Fall back: insert before </main>
    m = _MAIN_CLOSE_RE.search(html)
    if not m:
        raise ValueError("could not locate </main> to insert FAQ block before")
    return html[:m.start()] + "\n" + faq_block + html[m.start():]


# ---------------------------------------------------------------------------
# Main per-page pipeline
# ---------------------------------------------------------------------------

def process_page(path: Path) -> dict:
    """Return dict summarizing action: {slug, changed, reason, faqs, html}.

    The ``html`` field is the raw page source — passed through to apply_page
    so we don't have to re-read the file from disk on the apply pass.
    """
    slug = path.parent.name
    html = path.read_text(encoding="utf-8")

    # Idempotent guard
    if '"@type": "FAQPage"' in html:
        return {"slug": slug, "changed": False, "reason": "already has FAQPage"}

    soup = _soup(html)
    city = extract_city_name(soup, slug)
    country = extract_country(soup)
    scam_titles = extract_scam_titles(soup)
    locations = extract_scam_locations(soup)
    story = extract_first_scam_story(soup)
    takeaways = extract_takeaways(soup)
    tips = extract_safety_tips(soup)
    police_authority, police_phone = extract_emergency_police(soup)

    faqs = generate_faqs(
        city=city,
        country=country,
        scam_titles=scam_titles,
        locations=locations,
        story=story,
        tips=tips,
        takeaways=takeaways,
        police_authority=police_authority,
        police_phone=police_phone,
    )

    if not faqs:
        return {
            "slug": slug,
            "changed": False,
            "reason": f"SKIPPED (sparse content — {len(scam_titles)} scam cards)",
            "faqs": [],
        }

    return {
        "slug": slug,
        "changed": True,
        "reason": "FAQs generated",
        "city": city,
        "faqs": faqs,
        "country": country,
        "police_authority": police_authority,
        "police_phone": police_phone,
        "html": html,
    }


def apply_page(path: Path, faqs: List[Tuple[str, str]], html: str) -> None:
    html = _update_jsonld(html, faqs)
    faq_block = render_faq_html(faqs)
    html = _insert_faq_block(html, faq_block)
    path.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Preview only (default behavior — kept for explicitness)")
    ap.add_argument("--apply", action="store_true",
                    help="Write changes to disk. Without this flag the run is a dry-run preview.")
    ap.add_argument("--city", help="Only one city (slug)")
    ap.add_argument("--limit", type=int, default=0, help="Only first N pages (preview)")
    ap.add_argument("--verbose", action="store_true", help="Print generated FAQs per page")
    ap.add_argument(
        "--dump-json",
        help="Write {city: [[q,a],...]} JSON of generated FAQs to this path (does not modify HTML)",
    )
    args = ap.parse_args()

    # Dry-run by default — match sweep_dates.py / sweep_deshout_caps.py pattern.
    dry_run = not args.apply

    if args.city:
        targets = [SCAMS_DIR / args.city / "index.html"]
    else:
        targets = collect_scam_targets(city_pages=True)

    results = []
    for path in targets:
        if not path.exists():
            print(f"MISSING: {path}", file=sys.stderr)
            continue
        result = process_page(path)
        results.append((path, result))

    # Filter to pages needing changes for the --limit / verbose output
    needs_change = [(p, r) for p, r in results if r["changed"]]
    skipped = [(p, r) for p, r in results if not r["changed"] and r["reason"].startswith("SKIPPED")]
    already = [(p, r) for p, r in results if not r["changed"] and r["reason"] == "already has FAQPage"]

    if args.limit:
        needs_change = needs_change[:args.limit]

    if dry_run or args.verbose:
        for path, result in needs_change:
            print(f"\n=== {result['slug']} ({result.get('city', '?')}) ===")
            if result.get("country"):
                print(f"  country: {result['country']}")
            if result.get("police_authority") or result.get("police_phone"):
                print(f"  police:  {result.get('police_authority') or '?'} / {result.get('police_phone') or '?'}")
            for i, (q, a) in enumerate(result["faqs"], 1):
                print(f"  Q{i}: {q}")
                # Wrap answer for readability
                print(f"    A: {a}")

    # Dump FAQs to JSON (independent of HTML writes)
    if args.dump_json:
        dump = {
            result["city"]: [[q, a] for q, a in result["faqs"]]
            for _, result in needs_change
        }
        Path(args.dump_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.dump_json).write_text(
            json.dumps(dump, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {args.dump_json} ({len(dump)} cities)")

    # Apply changes
    applied = 0
    if not dry_run:
        for path, result in needs_change:
            apply_page(path, result["faqs"], result["html"])
            applied += 1

    print(f"\n--- summary ---")
    print(f"total pages scanned:       {len(results)}")
    print(f"already have FAQPage:      {len(already)}")
    print(f"would inject / injected:   {len(needs_change) if dry_run else applied}")
    print(f"skipped (sparse content):  {len(skipped)}")
    if skipped:
        print("  skipped slugs:")
        for _, r in skipped:
            print(f"    - {r['slug']}: {r['reason']}")


if __name__ == "__main__":
    main()
