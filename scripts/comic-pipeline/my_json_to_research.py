#!/usr/bin/env python3
"""Convert the 10 Malaysia api/v1 scam JSONs into research-batch format
that scams/generate_pages.py can consume.

Reads:  api/v1/scams/<city>.json (our deep book-ready format)
Writes: scams/research/my_batch1.json (the list-of-city-dicts research format)

Each scam's deep description gets decomposed into:
  - story:     the opening/context portion (first ~1500 chars, Reddit scaffolding stripped by polish later)
  - red_flags: 5 items extracted from the "(a)(b)(c)..." mechanic enumeration
  - how_to_avoid: 5 items extracted from the "For travelers: (1)(2)(3)..." defense list
  - reddit_sources: 5 citations extracted from `r/<sub> 'title' (comments/<hash>, YEAR)` patterns
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
API_DIR = REPO / "api" / "v1" / "scams"
OUT = REPO / "scams" / "research" / "my_batch1.json"

CITIES_IN_ORDER = [
    "kuala-lumpur", "melaka", "johor-bahru", "genting-highlands",
    "cameron-highlands", "ipoh", "penang", "langkawi",
    "kuching", "kota-kinabalu",
]

CITY_DISPLAY = {
    "kuala-lumpur": "Kuala Lumpur",
    "melaka": "Melaka",
    "johor-bahru": "Johor Bahru",
    "genting-highlands": "Genting Highlands",
    "cameron-highlands": "Cameron Highlands",
    "ipoh": "Ipoh",
    "penang": "Penang",
    "langkawi": "Langkawi",
    "kuching": "Kuching",
    "kota-kinabalu": "Kota Kinabalu",
}

# Regex patterns for extraction
RE_REDDIT = re.compile(
    r"r/[\w-]+\s+['\u2018\u2019\"][^'\u2018\u2019\"]{5,200}['\u2018\u2019\"]\s*\(comments/[a-z0-9]{5,12},\s*\d{4}\)",
    re.DOTALL,
)

# Find the "(a) … (b) … (c) …" mechanic block. Letters a–j.
RE_MECHANIC = re.compile(
    r"\(([a-j])\)\s*([^;]+?)(?=;\s*\([a-j]\)|\.\s*For travelers:|$)",
    re.DOTALL,
)

# Find the "For travelers: (1) … (2) … (3) …" defense block. Numbers 1–12.
RE_DEFENSE = re.compile(
    r"\((\d{1,2})\)\s*([^;]+?)(?=;\s*\(\d{1,2}\)|\.\s*$|$)",
    re.DOTALL,
)


def extract_reddit_sources(text: str, max_n: int = 5) -> list[str]:
    """Extract unique r/sub 'title' (comments/hash, YEAR) citations."""
    seen: set[str] = set()
    out: list[str] = []
    for m in RE_REDDIT.finditer(text):
        norm = re.sub(r"\s+", " ", m.group(0)).strip()
        key = norm.lower()
        if key in seen:
            continue
        seen.add(key)
        # Normalize quotes to ASCII single quotes for research format
        norm = norm.replace("\u2018", "'").replace("\u2019", "'").replace('"', "'")
        out.append(norm)
        if len(out) >= max_n:
            break
    return out


def clean_item(text: str) -> str:
    """Tidy a single bullet-list item."""
    t = text.strip().rstrip(".;,")
    t = re.sub(r"\s+", " ", t)
    # strip trailing parenthetical citations that leaked in
    t = re.sub(r"\s+per\s+r/[\w-]+\s+['\u2018\u2019\"][^'\u2018\u2019\"]+['\u2018\u2019\"](\s*\(comments/[a-z0-9]+,?\s*\d{4}\))?\.?", "", t)
    t = re.sub(r"\s+r/[\w-]+\s+['\u2018\u2019\"][^'\u2018\u2019\"]+['\u2018\u2019\"](\s*\(comments/[a-z0-9]+,?\s*\d{4}\))?\.?", "", t)
    return t.strip()


def extract_red_flags(desc: str, max_n: int = 5) -> list[str]:
    """Extract 5 red-flag items from the (a)(b)(c)… mechanic enumeration.

    Looks for the chunk after 'The 2025 scam pattern:' / 'The 2025 scams:' /
    'The scams:' and splits on lettered bullets."""
    # find the start of the mechanic block
    m = re.search(
        r"(?:The\s+(?:20\d{2}\s+)?scam\s+pattern[s]?|The\s+(?:20\d{2}\s+)?scams?)[:\s]",
        desc, re.IGNORECASE,
    )
    if not m:
        # Fallback: look for the first "(a)"
        m = re.search(r"\(a\)", desc)
        if not m:
            return []
    chunk = desc[m.end():]
    # cut off at "For travelers:" / "For older travelers:" OR the first "(1)" of
    # the numbered defense list — whichever comes first — so we don't bleed
    # the mechanic match into the defense section
    cut_positions = []
    for cutpat in [r"\bFor\s+(?:older\s+)?travelers[:,]", r"\(1\)\s"]:
        cm = re.search(cutpat, chunk, re.IGNORECASE)
        if cm:
            cut_positions.append(cm.start())
    if cut_positions:
        chunk = chunk[: min(cut_positions)]

    out: list[str] = []
    for mm in RE_MECHANIC.finditer(chunk):
        item = clean_item(mm.group(2))
        if len(item) < 10:
            continue
        # trim to ~140 chars for a chip — cut at last sentence-ish break
        if len(item) > 160:
            cut2 = item.rfind(",", 0, 160)
            if cut2 < 80:
                cut2 = 160
            item = item[:cut2].rstrip(", ")
        out.append(item)
        if len(out) >= max_n:
            break
    return out


def extract_how_to_avoid(desc: str, max_n: int = 5) -> list[str]:
    """Extract 5 defense steps from 'For travelers: (1)(2)(3)…' — or, if that
    marker is missing, from the first `(1)` that appears AFTER the lettered
    mechanic block."""
    m = re.search(r"For\s+(?:older\s+)?travelers[:,]", desc, re.IGNORECASE)
    if m:
        chunk = desc[m.end():]
    else:
        # Fallback: find the first "(1)" after any "(d)" or later mechanic
        # letters — that's where the defense list begins.
        one = re.search(r"\(1\)\s", desc)
        if not one:
            return []
        chunk = desc[one.start():]

    out: list[str] = []
    for mm in RE_DEFENSE.finditer(chunk):
        item = clean_item(mm.group(2))
        if len(item) < 10:
            continue
        if len(item) > 160:
            cut = item.rfind(",", 0, 160)
            if cut < 80:
                cut = 160
            item = item[:cut].rstrip(", ")
        out.append(item)
        if len(out) >= max_n:
            break
    return out


def story_preamble(desc: str) -> str:
    """Short story = description with the two big blocks removed, trimmed.
    The generate_pages.py story field is rendered as prose, so we keep the
    opening context + strip the explicit list markers."""
    # Find where the mechanic block starts; cut everything after.
    cut = re.search(
        r"(?:The\s+(?:20\d{2}\s+)?scam\s+pattern[s]?|The\s+(?:20\d{2}\s+)?scams?)[:\s]",
        desc, re.IGNORECASE,
    )
    story = desc[: cut.start()].strip() if cut else desc[:1400]
    if len(story) > 1400:
        story = story[:1400].rsplit(".", 1)[0] + "."
    return story


def convert_city(slug: str) -> dict:
    src = json.loads((API_DIR / f"{slug}.json").read_text())
    out_scams = []
    for s in src["scams"]:
        desc = s["description"]
        out_scams.append({
            "scam_name": s["name"],
            "danger_level": s["severity"],
            "category": s.get("category", "general"),
            "location": s.get("location", ""),
            "story": story_preamble(desc),
            "red_flags": extract_red_flags(desc, 5),
            "how_to_avoid": extract_how_to_avoid(desc, 5),
            "reddit_sources": extract_reddit_sources(desc, 5),
        })
    return {
        "city": CITY_DISPLAY[slug],
        "country": "Malaysia",
        "country_code": "MY",
        "flag": "\U0001F1F2\U0001F1FE",  # 🇲🇾
        "scams": out_scams,
    }


def main() -> None:
    # scams/generate_pages.py does `all_cities.extend(data)` — so the batch
    # file must be a flat list of city dicts at the top level, not wrapped.
    batch_list = [convert_city(c) for c in CITIES_IN_ORDER]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(batch_list, ensure_ascii=False, indent=2))

    # Sanity report
    print(f"Wrote {OUT}")
    for c in batch_list:
        slug = c["city"]
        print(f"\n  {slug}: {len(c['scams'])} scams")
        for s in c["scams"]:
            n_rf = len(s["red_flags"])
            n_ha = len(s["how_to_avoid"])
            n_rs = len(s["reddit_sources"])
            warn = []
            if n_rf < 5: warn.append(f"red_flags={n_rf}")
            if n_ha < 5: warn.append(f"how_to_avoid={n_ha}")
            if n_rs < 5: warn.append(f"reddit={n_rs}")
            flag = f"  [UNDER 5: {', '.join(warn)}]" if warn else ""
            print(f"    - {s['scam_name'][:50]:<50s} rf={n_rf} ha={n_ha} rs={n_rs}{flag}")


if __name__ == "__main__":
    main()
