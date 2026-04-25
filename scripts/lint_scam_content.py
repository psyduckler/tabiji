#!/usr/bin/env python3
"""Pre-generation lint for scam research JSON (scams/research/<cc>_batchN.json).

Implements the 17+2 rules defined in .claude/skills/scam-page-builder.md plus
3 additional post-render HTML rules (18-20) that operate on scams/<slug>/index.html.
REJECT rules block generation; WARN rules surface to the user.

Usage:
    python3 scripts/lint_scam_content.py scams/research/tw_batch1.json [--city Taipei]
    python3 scripts/lint_scam_content.py --all
    python3 scripts/lint_scam_content.py --report /tmp/scam-research/<slug>/lint-report.json
    python3 scripts/lint_scam_content.py --html
    python3 scripts/lint_scam_content.py --html-city tokyo
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Currency alternation — symbols + 3-letter codes used in scam prose.
_CCY = r"R\$|NT\$|US\$|HK\$|S\$|£|€|¥|RM|THB|JPY|EUR|USD|NTD|ARS|BRL|INR"

# ---- AmE/BrE drift (rule 1) ----
BRE_PATTERN = re.compile(
    r"\b("
    r"travellers?|favour(?:ite|ed|s)?|colour(?:ed|ful|s)?|centre[ds]?|"
    r"neighbour(?:hood|s)?|organis(?:e|ed|ation|ing)|authoris(?:e|ed|ing)|"
    r"recognis(?:e|ed|ing)|analys(?:e|ed|ing)|realis(?:e|ed|ing)|emphasis(?:e|ed|ing)|"
    r"apologis(?:e|ed|ing)|summaris(?:e|ed|ing)|theatre|jewellery|defence|"
    r"licence|aluminium|behaviour|programmes?|holidaymakers?|"
    r"whilst|amongst"
    r")\b",
    re.IGNORECASE,
)
# Specific proper-noun phrases where a BrE-looking word is legitimate.
# Keep tight — generic entries like "centre for" create false negatives.
PROPER_NOUN_ALLOWLIST = {
    "centre pompidou", "metropolitan centre for tropical medicine",
    "programme national", "national theatre", "covent garden theatre",
    "theatre royal", "royal albert",
}

# ---- Reddit-in-prose (rule 2) ----
REDDIT_IN_PROSE = re.compile(
    r"r/\w+\s*['\u2018\u2019\"]|comments/[a-z0-9]{6,8}\b"
)

# ---- Currency spacing + ranges (rules 3, 4) ----
CURRENCY_NOSPACE = re.compile(rf"\b(?:{_CCY})(?=\d)")
# "RM 50-RM 100" (hyphen) or "RM 50–100" (missing repeat symbol) — either rejects.
CURRENCY_RANGE_BAD = re.compile(rf"(?:{_CCY})\s?[\d,\.]+\s?[-\u2013]\s?\d")

# ---- Em-dash spacing (rule 5) ----
# An em-dash with no space on either side (but allow mid-word em-dash which is
# uncommon anyway).
EMDASH_NOSPACE = re.compile(r"\S\u2014\S")

# ---- Age gating (rule 9) ----
AGE_GATING = re.compile(
    r"\b(older travell?ers?|seniors?|pensioners?|retirees?|elderly travell?ers?)\b",
    re.IGNORECASE,
)

# ---- Alarmist / breezy (rule 10) ----
BAD_INTERJECTIONS = re.compile(
    r"\b(OMG|pro tip|literally|insane|crazy|sketchy af|legit)\b",
    re.IGNORECASE,
)

# ---- ALL-CAPS token (rule 8) ----
# Matches 3+ uppercase letters. Allowlist known acronyms that appear in
# legitimate scam-page prose (regulatory bodies, transport, card networks).
ALLCAPS_TOKEN = re.compile(r"\b[A-Z]{3,}\b")
ALLCAPS_ALLOWLIST = {
    "MDAC", "KLIA", "JPJ", "PDRM", "GIA", "AIGS", "AGL", "LRT", "MRT",
    "USD", "EUR", "THB", "JPY", "ATM", "QR", "SMS", "PSA",
    "TRA", "TPE", "AIT", "OCAC", "CIB", "GASA",
    "MLM", "PDF", "FAQ", "TLDR",
    "TOC", "CSS", "HTML", "CTA", "URL", "CTR", "SEO",
    "CNA", "AFP", "BBC", "SAR", "NYC",
    "BUDGET", "PREMIER", "DNS",
}

# ---- Fixed scam categories ----
VALID_CATEGORIES = {
    "transport", "counterfeit", "overcharging", "distraction",
    "gem", "fake-police", "digital", "rental", "temple-beg",
    "romance", "food-scam", "petty-theft",
}

VALID_DANGER = {"high", "moderate", "low"}

_YEAR_AT_END = re.compile(r",\s*(\d{4})\)\s*$")
_REDDIT_ID = re.compile(r"comments/([a-z0-9]+)")
_REDDIT_ID_SHAPE = re.compile(r"[a-z0-9]{4,10}")
_TRAILING_QUOTES = re.compile(r"['\"\u2019\u201d]+$")
_PUNCT_STRIP = re.compile(r"[^\w\s]")


def _sentences(text: str):
    """Rough sentence split on [.!?] followed by whitespace or end."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def _is_proper_noun_phrase(text: str, match_start: int, match_end: int) -> bool:
    # Title-case match against the original window — generic lowercase matches
    # like "centre for" would admit BrE prose as a false positive.
    window = text[max(0, match_start - 20): match_end + 20]
    return any(p in window for p in PROPER_NOUN_ALLOWLIST)


def lint_scam(scam: dict, scam_idx: int):
    """Return list of (level, rule, message) tuples."""
    issues = []

    def add(level, rule, msg):
        issues.append((level, rule, f"scam #{scam_idx} ({scam.get('scam_name','?')[:40]}): {msg}"))

    # ---- structural ----
    if "scam_name" not in scam or not scam["scam_name"]:
        add("REJECT", "structural", "missing scam_name")
        return issues
    if len(scam["scam_name"]) > 60:
        add("REJECT", "13", f"scam_name too long ({len(scam['scam_name'])} chars)")

    if scam.get("danger_level", "").lower() not in VALID_DANGER:
        add("REJECT", "structural", f"invalid danger_level: {scam.get('danger_level')!r}")

    if scam.get("category") not in VALID_CATEGORIES:
        add("REJECT", "structural", f"invalid category: {scam.get('category')!r}")

    loc_count = len([s for s in scam.get("location","").split(",") if s.strip()])
    if loc_count > 5:
        add("WARN", "14", f"location has {loc_count} entries (>5)")

    rf = scam.get("red_flags", [])
    av = scam.get("how_to_avoid", [])
    rs = scam.get("reddit_sources", [])
    if len(rf) != 5:
        add("REJECT", "17", f"red_flags count {len(rf)} != 5")
    if len(av) != 5:
        add("REJECT", "17", f"how_to_avoid count {len(av)} != 5")
    if len(rs) != 5:
        add("REJECT", "16", f"reddit_sources count {len(rs)} != 5")

    story = scam.get("story", "")

    # ---- 7b: paragraph count — 3-beat narrative is the floor ----
    # The 3-paragraph compact format (setup → pivot → mechanism) is the
    # canonical post-2026-04-25 shape — see /scams/new-york-city/ for the
    # reference implementation. Longer scams may extend Beat 3 across
    # 2–3 extra paragraphs but should not re-introduce defense steps the
    # how_to_avoid list already covers.
    paragraphs = [p.strip() for p in story.split("\n\n") if p.strip()]
    if len(paragraphs) < 3:
        add("REJECT", "7b", f"story has {len(paragraphs)} paragraphs (< 3)")
    elif len(paragraphs) > 5:
        add("WARN", "7b", f"story has {len(paragraphs)} paragraphs (> 5)")

    # ---- 7: paragraph length ----
    for pi, p in enumerate(paragraphs, 1):
        wc = len(p.split())
        if wc > 120:
            add("REJECT", "7", f"paragraph {pi} is {wc} words (>120)")
        elif wc > 100:
            add("WARN", "7", f"paragraph {pi} is {wc} words (>100)")

    # ---- 6: sentence length ----
    for pi, p in enumerate(paragraphs, 1):
        for sent in _sentences(p):
            wc = len(sent.split())
            if wc > 70:
                add("REJECT", "6", f"sentence in paragraph {pi} is {wc} words (>70)")
            elif wc > 50:
                add("WARN", "6", f"sentence in paragraph {pi} is {wc} words (>50)")

    # ---- 8: ALL-CAPS budget ----
    caps_tokens = [t for t in ALLCAPS_TOKEN.findall(story) if t not in ALLCAPS_ALLOWLIST]
    if len(caps_tokens) > 18:
        add("REJECT", "8", f"ALL-CAPS token count {len(caps_tokens)} (>18): {caps_tokens[:8]}")
    elif len(caps_tokens) > 12:
        add("WARN", "8", f"ALL-CAPS token count {len(caps_tokens)} (>12): {caps_tokens[:8]}")

    # ---- Combined prose fields for rules 1, 2, 3, 4, 5, 9, 10 ----
    prose_fields = {
        "story": story,
        **{f"red_flags[{i}]": rf[i] for i in range(len(rf))},
        **{f"how_to_avoid[{i}]": av[i] for i in range(len(av))},
    }

    for fname, text in prose_fields.items():
        if not text:
            continue

        # Rule 1: AmE/BrE drift (reddit_sources[] is excluded upstream — not in prose_fields)
        for m in BRE_PATTERN.finditer(text):
            if _is_proper_noun_phrase(text, m.start(), m.end()):
                continue
            add("REJECT", "1", f"BrE form {m.group()!r} in {fname}")

        # Rule 2: Reddit citation in prose
        for m in REDDIT_IN_PROSE.finditer(text):
            add("REJECT", "2", f"Reddit citation {m.group()!r} in {fname} (use reddit_sources[] only)")

        # Rule 3: Currency no-space
        for m in CURRENCY_NOSPACE.finditer(text):
            add("REJECT", "3", f"currency no-space at {m.group()!r} in {fname}")

        # Rule 4: Currency range missing the repeated symbol on the second amount
        for m in CURRENCY_RANGE_BAD.finditer(text):
            add("REJECT", "4", f"bad currency range {m.group()!r} in {fname}")

        # Rule 5: Em-dash no-space
        for m in EMDASH_NOSPACE.finditer(text):
            add("REJECT", "5", f"em-dash without space {m.group()!r} in {fname}")

        # Rule 9: Age-gating
        for m in AGE_GATING.finditer(text):
            add("REJECT", "9", f"age-gating phrase {m.group()!r} in {fname}")

        # Rule 10: Bad interjections
        for m in BAD_INTERJECTIONS.finditer(text):
            add("REJECT", "10", f"alarmist/breezy interjection {m.group()!r} in {fname}")

    # ---- 12: bullet completeness ----
    for i, item in enumerate(rf):
        if len(item.split()) < 4:
            add("REJECT", "12", f"red_flags[{i}] has < 4 words: {item!r}")
    for i, item in enumerate(av):
        stripped = _TRAILING_QUOTES.sub("", item.strip())
        if not stripped or stripped[-1] not in ".?!":
            add("REJECT", "12", f"how_to_avoid[{i}] doesn't end in .?!: {item!r}")

    # ---- 15: reddit year mix ----
    years = []
    for src in rs:
        m = _YEAR_AT_END.search(src)
        if m:
            years.append(int(m.group(1)))
    if years:
        modern = sum(1 for y in years if y >= 2025)
        pct = 100 * modern / len(years)
        if pct < 80:
            add("WARN", "15", f"reddit_sources year mix {modern}/{len(years)} from 2025/2026 ({pct:.0f}% < 80%)")

    # ---- reddit id shape (4-10 chars covers legacy + modern base36 IDs) ----
    for src in rs:
        m = _REDDIT_ID.search(src)
        if not m:
            add("REJECT", "16", f"reddit_sources missing comments/<id>: {src!r}")
        elif not _REDDIT_ID_SHAPE.fullmatch(m.group(1)):
            add("REJECT", "16", f"reddit thread id wrong shape: {m.group(1)!r}")

    return issues


def lint_city(data: dict):
    """Lint one city object."""
    city = data.get("city", "?")
    scams = data.get("scams", [])
    all_issues = []

    # Scam count
    if not (3 <= len(scams) <= 6):
        all_issues.append(("REJECT", "count", f"{city}: {len(scams)} scams (need 3-6)"))

    # Opening-repetition (rule 11): first 2 words of first sentence, punctuation-stripped
    openings = []
    for s in scams:
        story = s.get("story", "")
        first_para = story.split("\n\n")[0] if story else ""
        sents = _sentences(first_para)
        first_sent = sents[0] if sents else ""
        words = [_PUNCT_STRIP.sub("", w).lower() for w in first_sent.split()[:2]]
        words = [w for w in words if w]
        if len(words) == 2:
            openings.append(" ".join(words))
    for op, c in Counter(openings).items():
        if c >= 3:
            all_issues.append(("WARN", "11", f"{city}: {c} scams share 2-word opening {op!r}"))

    for i, scam in enumerate(scams, 1):
        all_issues.extend(lint_scam(scam, i))

    return all_issues


# ---- Rule 18/19/20: rendered-HTML lint ----
from _scam_sweep_common import is_tldr_complete, collect_scam_targets  # noqa: E402

_H1_SCAM_COUNT = re.compile(r"^(?:(?:Don[\u2019']t Fall for These\s+)?)?(\d+)\s+Tourist\s+Scams", re.IGNORECASE)
_HERO_SCAMS_DOCUMENTED = re.compile(r"(\d+)\s+scams\s+documented", re.IGNORECASE)
_HERO_UPDATED = re.compile(
    r"Updated\s+(January|February|March|April|May|June|July|August|"
    r"September|October|November|December)\s+(\d{4})",
    re.IGNORECASE,
)
_MONTH_TO_NUM = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12",
}


def lint_html_page(path: Path):
    """Lint a rendered scam page (scams/<slug>/index.html).

    Returns a list of (level, rule, message) tuples, matching lint_scam()'s shape.
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise SystemExit(
            "BeautifulSoup4 is required for --html lint. Install with: pip install beautifulsoup4"
        ) from exc

    issues = []
    try:
        html = path.read_text(encoding="utf-8")
    except Exception as e:
        issues.append(("REJECT", "io", f"failed to read {path}: {e}"))
        return issues

    soup = BeautifulSoup(html, "html.parser")

    # ---- Rule 18: TLDR sentence-complete ----
    for idx, node in enumerate(soup.select(".scam-tldr"), 1):
        text = node.get_text(" ", strip=True)
        if not is_tldr_complete(text):
            preview = (text or "(empty)")[:60].replace("\n", " ")
            issues.append(("REJECT", "18", f"scam-tldr[{idx}]: \"{preview}...\""))

    # ---- Rule 19: count desync (h1 vs .scam-card vs hero-meta) ----
    h1 = soup.find("h1")
    h1_n = None
    if h1:
        h1_text = h1.get_text(" ", strip=True)
        m = _H1_SCAM_COUNT.match(h1_text)
        if m:
            h1_n = int(m.group(1))

    cards_n = len(soup.select(".scam-card"))

    hero_n = None
    hero_meta = soup.select_one(".hero-meta")
    if hero_meta:
        for span in hero_meta.find_all("span"):
            stext = span.get_text(" ", strip=True)
            m = _HERO_SCAMS_DOCUMENTED.search(stext)
            if m:
                hero_n = int(m.group(1))
                break

    if h1_n is None:
        issues.append(("REJECT", "19", "could not parse scam count from <h1>"))
    elif hero_n is None:
        issues.append(("REJECT", "19", "could not parse 'N scams documented' from .hero-meta"))
    elif not (h1_n == cards_n == hero_n):
        issues.append(("REJECT", "19", f"h1={h1_n} cards={cards_n} hero={hero_n}"))

    # ---- Rule 20: hero 'Updated {Month Year}' vs JSON-LD dateModified ----
    hero_updated = None
    if hero_meta:
        for span in hero_meta.find_all("span"):
            stext = span.get_text(" ", strip=True)
            m = _HERO_UPDATED.search(stext)
            if m:
                hero_updated = f"{m.group(2)}-{_MONTH_TO_NUM[m.group(1).lower()]}"
                break

    jsonld_modified = None
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            ld = json.loads(script.string or "")
        except Exception:
            continue
        # JSON-LD may be a single object, a graph, or an array.
        candidates = []
        if isinstance(ld, dict):
            if "@graph" in ld and isinstance(ld["@graph"], list):
                candidates.extend(ld["@graph"])
            else:
                candidates.append(ld)
        elif isinstance(ld, list):
            candidates.extend(ld)
        for obj in candidates:
            if isinstance(obj, dict) and obj.get("dateModified"):
                dm = str(obj["dateModified"])
                # Grab YYYY-MM from any ISO-ish date.
                if re.match(r"^\d{4}-\d{2}", dm):
                    jsonld_modified = dm[:7]
                    break
        if jsonld_modified:
            break

    if hero_updated and jsonld_modified and hero_updated != jsonld_modified:
        issues.append(
            ("WARN", "20", f"hero={hero_updated} vs jsonld={jsonld_modified}")
        )

    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", help="Path to research JSON (e.g. scams/research/tw_batch1.json)")
    ap.add_argument("--city", help="Only lint this city (if file has multiple)")
    ap.add_argument("--report", help="Write JSON report to path")
    ap.add_argument("--all", action="store_true", help="Lint every scams/research/*.json")
    ap.add_argument("--html", action="store_true", help="Lint every scams/<slug>/index.html (rules 18-20)")
    ap.add_argument("--html-city", help="Lint one scams/<slug>/index.html (rules 18-20)")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[1]

    # ---- HTML mode (rules 18-20) ----
    if args.html or args.html_city:
        if args.html_city:
            html_targets = [repo / "scams" / args.html_city / "index.html"]
        else:
            html_targets = collect_scam_targets(city_pages=True)

        all_issues = []
        for path in html_targets:
            if not path.exists():
                print(f"FAIL: {path} does not exist", file=sys.stderr)
                sys.exit(2)
            slug = path.parent.name
            issues = lint_html_page(path)
            for level, rule, msg in issues:
                all_issues.append({"file": str(path), "city": slug, "level": level, "rule": rule, "message": msg})

        rejects = [i for i in all_issues if i["level"] == "REJECT"]
        warns = [i for i in all_issues if i["level"] == "WARN"]

        if args.report:
            Path(args.report).parent.mkdir(parents=True, exist_ok=True)
            with open(args.report, "w") as f:
                json.dump({"rejects": rejects, "warns": warns}, f, indent=2)

        for i in all_issues:
            marker = "\u274c" if i["level"] == "REJECT" else "\u26a0\ufe0f"
            print(f"{marker} [{i['level']} rule {i['rule']}] {i['city']}: {i['message']}")
        print(f"\n{len(rejects)} REJECT  {len(warns)} WARN")
        sys.exit(1 if rejects else 0)

    # ---- JSON mode (rules 1-17) ----
    targets = []
    if args.all:
        targets = sorted((repo / "scams" / "research").glob("*.json"))
    elif args.path:
        targets = [Path(args.path)]
    else:
        ap.error("need path, --all, --html, or --html-city")

    all_issues = []
    for path in targets:
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:
            print(f"FAIL to load {path}: {e}", file=sys.stderr)
            sys.exit(2)
        cities = data if isinstance(data, list) else [data]
        for city_data in cities:
            if args.city and city_data.get("city") != args.city:
                continue
            issues = lint_city(city_data)
            for level, rule, msg in issues:
                all_issues.append({"file": str(path), "city": city_data.get("city"), "level": level, "rule": rule, "message": msg})

    rejects = [i for i in all_issues if i["level"] == "REJECT"]
    warns = [i for i in all_issues if i["level"] == "WARN"]

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        with open(args.report, "w") as f:
            json.dump({"rejects": rejects, "warns": warns}, f, indent=2)

    for i in all_issues:
        marker = "\u274c" if i["level"] == "REJECT" else "\u26a0\ufe0f"
        print(f"{marker} [{i['level']} rule {i['rule']}] {i['message']}")
    print(f"\n{len(rejects)} REJECT  {len(warns)} WARN")
    sys.exit(1 if rejects else 0)


if __name__ == "__main__":
    main()
