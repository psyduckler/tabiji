#!/usr/bin/env python3
"""
One-off audit fix pass — 2026-04-16.

Fixes identified in the compare/ quality audit:

  1. Remove invalid </img> closing tags on canonical pages (~1,410 pages)
  2. Smart-truncate meta descriptions over 160 chars (~501 pages)
  3. De-dup hub "popular" row + fix "destination" -> "destinations" typo
  4. Smart-truncate hub card descriptions that cut mid-word (~72 cards)
  5. Add reverse-slug 301 block to /_redirects
  6. Remove reverse-slug entries from /sitemap.xml
  7. Country cluster hub: rewrite boilerplate meta + remove double brand + double CTA

Idempotent: safe to re-run. Each step checks before writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
COMPARE = REPO / "compare"


# ---------------------------------------------------------------------------
# 1. Remove </img> in canonical pages
# ---------------------------------------------------------------------------
def fix_img_closing_tags() -> int:
    """Strip invalid </img> closing tags from every compare page."""
    fixed = 0
    for idx in COMPARE.rglob("index.html"):
        txt = idx.read_text(encoding="utf-8")
        if "</img>" not in txt:
            continue
        idx.write_text(txt.replace("</img>", ""), encoding="utf-8")
        fixed += 1
    return fixed


# ---------------------------------------------------------------------------
# 2. Smart-truncate meta descriptions > 160 chars
# ---------------------------------------------------------------------------
META_DESC_RE = re.compile(r'(<meta\s+content=")([^"]{161,})("\s+name="description"\s*/?>)', re.I)
MAX_DESC = 155  # leave a 5-char safety buffer under Google's 160-char display cap


def smart_truncate(text: str, limit: int) -> str:
    """Truncate to <=limit chars on a word boundary, ending with a period if possible."""
    if len(text) <= limit:
        return text
    # Prefer cutting at a sentence-end (. ! ?) close to the limit
    cut = text[:limit]
    # find the last sentence terminator
    for terminator in (". ", "! ", "? "):
        idx = cut.rfind(terminator)
        if idx >= limit - 40:  # close enough to the limit to be worth using
            return cut[: idx + 1].rstrip()
    # fall back to the last word boundary
    space = cut.rfind(" ")
    if space > 0:
        return cut[:space].rstrip().rstrip(",.;:!?-") + "."
    return cut.rstrip() + "."


def fix_long_meta_descriptions() -> int:
    fixed = 0
    for idx in COMPARE.rglob("index.html"):
        txt = idx.read_text(encoding="utf-8")
        m = META_DESC_RE.search(txt)
        if not m:
            continue
        original = m.group(2)
        new = smart_truncate(original, MAX_DESC)
        if new == original:
            continue
        txt = txt[: m.start(2)] + new + txt[m.end(2) :]
        idx.write_text(txt, encoding="utf-8")
        fixed += 1
    return fixed


# ---------------------------------------------------------------------------
# 3. Dedup hub popular row + fix "destination" typo
# ---------------------------------------------------------------------------
def fix_hub_dedup_and_typo() -> tuple[int, bool]:
    hub = COMPARE / "index.html"
    txt = hub.read_text(encoding="utf-8")
    before = txt

    # Typo: "Compare destination head-to-head" -> "destinations"
    typo_fixed = "Compare destination head-to-head" in txt
    txt = txt.replace(
        "Compare destination head-to-head",
        "Compare destinations head-to-head",
    )

    # Dedup: the <a class="compare-card" href="..."> blocks. Keep first occurrence.
    # Match each card block so we can remove later duplicates by href.
    card_re = re.compile(
        r'<a href="(/compare/[a-z0-9-]+/)" class="compare-card">.*?</a>',
        re.S,
    )
    seen: set[str] = set()
    removed = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal removed
        href = match.group(1)
        if href in seen:
            removed += 1
            return ""
        seen.add(href)
        return match.group(0)

    txt = card_re.sub(replace, txt)

    # Clean up any double blank lines from removals
    txt = re.sub(r"\n{3,}", "\n\n", txt)

    if txt != before:
        hub.write_text(txt, encoding="utf-8")
    return removed, typo_fixed


# ---------------------------------------------------------------------------
# 4. Smart-truncate hub card descriptions (the mid-word cutoffs)
# ---------------------------------------------------------------------------
# Hub cards look like: <p>Xxx vs Yyy — ... traveler preferences. Honest</p>
# We smart-truncate any <p> inside a compare-card that ends with a trailing
# word-boundary artifact.
TRAILING_BAD_SUFFIX_RE = re.compile(
    r"(<p>)([^<]{80,})(</p>)"
)


def clean_card_desc(original: str) -> str:
    """Normalize card descriptions so they end on a sentence boundary."""
    text = original.strip()
    # Cases we've seen in hub:
    #   "... traveler preferences. Honest"      -> "... traveler preferences."
    #   "... traveler preferences. Budget br"   -> "... traveler preferences."
    #   "... traveler preferences. B"           -> "... traveler preferences."
    # Rule: if the text ends with a clear trailing fragment (1-3 Capitalized words
    # without terminal punctuation), strip it back to the last '.', '?' or '!'.
    if text.endswith((".", "?", "!", '"', "”")):
        return text  # already clean
    # Find the last sentence terminator
    for term in (".", "?", "!"):
        idx = text.rfind(term)
        if idx > len(text) * 0.5:  # cut only if we keep most of the content
            return text[: idx + 1]
    # No clean boundary — cut at the last word and add a period
    space = text.rfind(" ")
    if space > 0:
        trimmed = text[:space].rstrip().rstrip(",.;:!?-")
        return trimmed + "."
    return text + "."


def fix_hub_card_descriptions() -> int:
    hub = COMPARE / "index.html"
    txt = hub.read_text(encoding="utf-8")

    # Only touch <p> tags that are INSIDE a compare-card-body block.
    # Find every compare-card-body and rewrite its <p>.
    body_re = re.compile(
        r'(<div class="compare-card-body">\s*<h2>[^<]+</h2>\s*<p>)([^<]+)(</p>)',
        re.S,
    )
    fixed = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal fixed
        original = match.group(2)
        cleaned = clean_card_desc(original)
        if cleaned == original:
            return match.group(0)
        fixed += 1
        return match.group(1) + cleaned + match.group(3)

    new_txt = body_re.sub(replace, txt)
    if new_txt != txt:
        hub.write_text(new_txt, encoding="utf-8")
    return fixed


# ---------------------------------------------------------------------------
# 5. Add 301 redirects to _redirects for reverse-slug pages
# ---------------------------------------------------------------------------
REDIRECT_MARKER_START = "# >>> compare reverse-slug redirects (auto-managed) >>>"
REDIRECT_MARKER_END = "# <<< compare reverse-slug redirects (auto-managed) <<<"

REFRESH_URL_RE = re.compile(
    r'meta\s+http-equiv="refresh"\s+content="0;\s*url=(/compare/[^"/]+/)"',
    re.I,
)


def collect_reverse_slug_redirects() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for idx in sorted(COMPARE.rglob("index.html")):
        # only direct children of /compare/ (canonical or redirect leaves)
        if idx.parent.parent.name != "compare":
            continue
        txt = idx.read_text(encoding="utf-8", errors="replace")
        m = REFRESH_URL_RE.search(txt)
        if not m:
            continue
        src = f"/compare/{idx.parent.name}/"
        tgt = m.group(1)
        if src == tgt:
            continue
        pairs.append((src, tgt))
    return pairs


def update_redirects_file(pairs: list[tuple[str, str]]) -> int:
    redirects_path = REPO / "_redirects"
    current = redirects_path.read_text(encoding="utf-8") if redirects_path.exists() else ""

    block_lines = [REDIRECT_MARKER_START]
    for src, tgt in pairs:
        block_lines.append(f"{src} {tgt} 301")
    block_lines.append(REDIRECT_MARKER_END)
    block = "\n".join(block_lines)

    if REDIRECT_MARKER_START in current and REDIRECT_MARKER_END in current:
        # replace the existing block
        new = re.sub(
            re.escape(REDIRECT_MARKER_START) + r".*?" + re.escape(REDIRECT_MARKER_END),
            block,
            current,
            flags=re.S,
        )
    else:
        # append
        sep = "" if current.endswith("\n") or not current else "\n"
        new = current + sep + "\n" + block + "\n"

    if new != current:
        redirects_path.write_text(new, encoding="utf-8")
    return len(pairs)


# ---------------------------------------------------------------------------
# 6. Strip reverse-slug entries from sitemap.xml
# ---------------------------------------------------------------------------
def strip_sitemap_reverse_slugs(pairs: list[tuple[str, str]]) -> int:
    sitemap = REPO / "sitemap.xml"
    if not sitemap.exists():
        return 0
    txt = sitemap.read_text(encoding="utf-8")
    removed = 0
    slugs = {src for src, _ in pairs}
    # <url>...<loc>https://tabiji.ai/compare/paris-vs-london/</loc>...</url>
    url_re = re.compile(r"\s*<url>\s*<loc>([^<]+)</loc>.*?</url>\s*", re.S)

    def replace(match: re.Match[str]) -> str:
        nonlocal removed
        loc = match.group(1).strip()
        # Normalize: accept with or without domain
        path = loc
        for prefix in ("https://tabiji.ai", "http://tabiji.ai"):
            if path.startswith(prefix):
                path = path[len(prefix) :]
                break
        if path in slugs:
            removed += 1
            return "\n"
        return match.group(0)

    new_txt = url_re.sub(replace, txt)
    # Tidy up any runs of blank lines
    new_txt = re.sub(r"\n{3,}", "\n\n", new_txt)
    if new_txt != txt:
        sitemap.write_text(new_txt, encoding="utf-8")
    return removed


# ---------------------------------------------------------------------------
# 7. Country cluster hubs — fix boilerplate + double brand + double CTA
# ---------------------------------------------------------------------------
# Country-specific hubs all have the same meta description template.
GENERIC_BOILERPLATE_RE = re.compile(
    r'Browse (?P<name>[^"]+?) destination comparisons with related reads and explicit ranking signals\.'
)

# A "country" cluster is a hub whose hero-card eyebrow says
#   "Destination cluster hub" AND whose title is "<Place> comparisons".
# We know the 33 hub slugs from the audit.
CLUSTER_HUB_SLUGS = [
    "asia", "australia", "bali", "cities", "colombia", "countries", "croatia",
    "culture", "egypt", "europe", "global-mixed", "greece", "hawaii", "iceland",
    "islands", "italy", "japan", "latin-america", "luxury", "maldives", "mexico",
    "middle-east-africa", "morocco", "nature", "new-zealand", "north-america",
    "oceania", "portugal", "spain", "taiwan", "thailand", "trip-style-guides",
    "vietnam",
]

# Curated replacement descriptions for country/place hubs that currently use
# the boilerplate. Thematic hubs (asia, europe, luxury, culture, cities,
# countries, islands, nature, trip-style-guides, global-mixed, oceania,
# latin-america, north-america, middle-east-africa) are already custom, skip.
CURATED_DESCRIPTIONS: dict[str, str] = {
    "australia": "Compare Sydney, Melbourne, the Outback, and the reef — the best Australia head-to-head travel decisions, ranked by real traveler data.",
    "bali": "Bali vs the rest of Southeast Asia. Compare Ubud, Canggu, Nusa islands, and nearby alternatives with honest cost and vibe breakdowns.",
    "colombia": "Cartagena, Medellín, the coffee region, and beyond — Colombia destination comparisons with honest cost, safety, and vibe verdicts.",
    "croatia": "Dubrovnik, Split, Hvar, Istria — compare Croatia coast and island options with real cost data and day-by-day tradeoffs.",
    "egypt": "Cairo, Luxor, the Red Sea, and more — Egypt destination comparisons with costs, logistics, and honest traveler tradeoffs.",
    "greece": "Santorini, Mykonos, Crete, Athens, and the lesser-known islands — Greece comparisons with costs and honest vibe tradeoffs.",
    "hawaii": "Maui, Oahu, Big Island, Kauai — Hawaii island-by-island comparisons with costs, beaches, and honest first-timer picks.",
    "iceland": "Iceland ring road vs south coast vs Reykjavik day trips — compare Iceland trip options with real cost and season data.",
    "italy": "Rome, Venice, Tuscany, Amalfi, and the north-vs-south debate — Italy destination comparisons with honest cost and vibe tradeoffs.",
    "japan": "Tokyo, Kyoto, Osaka, Hokkaido, Kyushu — Japan destination comparisons ranked by real traveler demand and updated for 2026.",
    "maldives": "Maldives vs the rest of the Indian Ocean. Compare atolls, resort tiers, and alternatives like Seychelles or Zanzibar.",
    "mexico": "Cancún, Tulum, Mexico City, Oaxaca, and beyond — Mexico destination comparisons with honest cost and safety tradeoffs.",
    "morocco": "Marrakech, Fes, Chefchaouen, the Sahara, and the coast — Morocco destination comparisons with costs and vibe verdicts.",
    "new-zealand": "North Island vs South Island, Queenstown vs Milford — compare New Zealand trip options with real cost and season data.",
    "portugal": "Lisbon, Porto, the Algarve, Madeira, the Azores — Portugal destination comparisons with costs and honest tradeoffs.",
    "spain": "Madrid, Barcelona, Andalusia, the Basque Country, and the islands — Spain destination comparisons, ranked by traveler demand.",
    "taiwan": "Taipei, Taroko, Alishan, Tainan, and the outer islands — Taiwan destination comparisons with costs and vibe verdicts.",
    "thailand": "Bangkok, Chiang Mai, Phuket, Krabi, and the islands — Thailand destination comparisons with real cost and season data.",
    "vietnam": "Hanoi, Ho Chi Minh, Hoi An, Ha Long, the Mekong — Vietnam destination comparisons with honest cost and route tradeoffs.",
}


def fix_cluster_hubs() -> tuple[int, int, int]:
    rewrote_desc = 0
    removed_double_brand = 0
    removed_double_cta = 0
    for slug in CLUSTER_HUB_SLUGS:
        path = COMPARE / slug / "index.html"
        if not path.exists():
            continue
        txt = path.read_text(encoding="utf-8")
        before = txt

        # --- meta description rewrite ---
        if slug in CURATED_DESCRIPTIONS:
            new_desc = CURATED_DESCRIPTIONS[slug]
            # Replace all 4 places the description can appear: meta[name=description],
            # og:description, twitter:description, JSON-LD "description":"..." of the
            # CollectionPage (NOT the nested comparison items).
            # Use a targeted regex that only matches the hub's boilerplate phrase.
            def sub_desc(match: re.Match[str]) -> str:
                return new_desc
            txt = GENERIC_BOILERPLATE_RE.sub(sub_desc, txt)

        # --- double-brand: strip the extra <a class="brand"> in the topbar ---
        # Pattern: <div class="shell"><a class="brand" href="/">tabi<span>ji</span></a><!-- @include:nav:start -->
        txt, n_brand = re.subn(
            r'<a class="brand" href="/">tabi<span>ji</span></a>',
            "",
            txt,
        )
        removed_double_brand += n_brand

        # --- double CTA: remove the injected .cta-plan-box at the bottom, keep the
        # in-template "Need help choosing?" section ---
        # The injected block lives between <section class="section" id="cta">...</section>
        # and </main>. It's the <div class="cta-plan-box" ...>...</div> block.
        cta_re = re.compile(
            r'\s*<div class="cta-plan-box"[^>]*>.*?</div>\s*',
            re.S,
        )
        txt, n_cta = cta_re.subn("", txt)
        removed_double_cta += n_cta

        if txt != before:
            path.write_text(txt, encoding="utf-8")
            rewrote_desc += 1 if slug in CURATED_DESCRIPTIONS else 0
    return rewrote_desc, removed_double_brand, removed_double_cta


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
def main() -> int:
    print("Compare audit-fix pass (2026-04-16)\n")

    print("Step 1: strip </img> closing tags ...", flush=True)
    n = fix_img_closing_tags()
    print(f"  fixed {n} pages")

    print("Step 2: truncate meta descriptions > 160 chars ...", flush=True)
    n = fix_long_meta_descriptions()
    print(f"  fixed {n} pages")

    print("Step 3: hub popular-row dedup + typo ...", flush=True)
    removed, typo_fixed = fix_hub_dedup_and_typo()
    print(f"  removed {removed} duplicate cards, typo fixed: {typo_fixed}")

    print("Step 4: hub card description smart-truncation ...", flush=True)
    n = fix_hub_card_descriptions()
    print(f"  cleaned {n} cards")

    print("Step 5: collecting reverse-slug redirects ...", flush=True)
    pairs = collect_reverse_slug_redirects()
    print(f"  found {len(pairs)} reverse-slug redirect targets")

    print("Step 6: writing _redirects ...", flush=True)
    n = update_redirects_file(pairs)
    print(f"  wrote {n} 301 rules")

    print("Step 7: stripping reverse slugs from sitemap.xml ...", flush=True)
    n = strip_sitemap_reverse_slugs(pairs)
    print(f"  removed {n} sitemap entries")

    print("Step 8: cluster hub fixes (boilerplate + double brand + double CTA) ...", flush=True)
    rewrote, brand_removed, cta_removed = fix_cluster_hubs()
    print(f"  rewrote {rewrote} descriptions, removed {brand_removed} double-brand, removed {cta_removed} duplicate CTAs")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
