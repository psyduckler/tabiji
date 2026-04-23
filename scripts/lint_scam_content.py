#!/usr/bin/env python3
"""Pre-generation lint for scam research JSON (scams/research/<cc>_batchN.json).

Implements the 17+2 rules defined in .claude/skills/scam-page-builder.md.
REJECT rules block generation; WARN rules surface to the user.

Usage:
    python3 scripts/lint_scam_content.py scams/research/tw_batch1.json [--city Taipei]
    python3 scripts/lint_scam_content.py --all
    python3 scripts/lint_scam_content.py --report /tmp/scam-research/<slug>/lint-report.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---- AmE/BrE drift (rule 1) ----
# Forbidden BrE forms; allowlist any match inside a proper-noun phrase or
# inside a single-quoted Reddit title in reddit_sources[].
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
PROPER_NOUN_ALLOWLIST = {
    "centre pompidou", "theatre district", "metropolitan centre",
    "programme national", "centre for", "national theatre",
    "london theatre", "covent garden theatre",
}

# ---- Reddit-in-prose (rule 2) ----
REDDIT_IN_PROSE = re.compile(
    r"r/\w+\s*['\u2018\u2019\"]|comments/[a-z0-9]{6,8}\b"
)

# ---- Currency spacing (rule 3) ----
# A currency symbol or 1-3-letter code directly adjacent to a digit.
CURRENCY_NOSPACE = re.compile(
    r"\b(?:R\$|NT\$|US\$|HK\$|S\$|£|€|¥|RM|THB|JPY|EUR|USD|NTD|ARS|BRL|INR)(?=\d)"
)

# ---- Currency range (rule 4) ----
# "RM 50-RM 100" (hyphen) or "RM 50–100" (missing repeat symbol).
CURRENCY_RANGE_BAD = re.compile(
    r"(?:R\$|NT\$|US\$|HK\$|S\$|£|€|¥|RM|THB|JPY|EUR|USD|NTD)\s?[\d,\.]+\s?[-\u2013]\s?\d"
)
CURRENCY_RANGE_GOOD = re.compile(
    r"(?:R\$|NT\$|US\$|HK\$|S\$|£|€|¥|RM|THB|JPY|EUR|USD|NTD)\s[\d,\.]+\s?\u2013\s?(?:R\$|NT\$|US\$|HK\$|S\$|£|€|¥|RM|THB|JPY|EUR|USD|NTD)\s"
)

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
ALLCAPS_TOKEN = re.compile(r"\b[A-Z]{3,}\b")
# Acronyms we expect to see repeatedly that shouldn't count as "emphasis":
ALLCAPS_ALLOWLIST = {
    "MDAC", "KLIA", "JPJ", "PDRM", "GIA", "AIGS", "AGL", "LRT", "MRT",
    "USD", "EUR", "THB", "JPY", "NT", "RM", "ATM", "QR", "SMS", "PSA",
    "TRA", "TPE", "AIT", "OCAC", "CIB", "GASA", "NT$", "HK$", "US$",
    "MLM", "ID", "PDF", "FAQ", "TL;DR", "TLDR", "WhatsApp",
    "TOC", "CSS", "HTML", "CTA", "URL", "CTR", "SEO", "T1", "T2", "T3",
    "CNA", "AFP", "AP", "BBC", "SAR", "NYC", "UK", "US", "EU",
    "BUDGET", "PREMIER",  # from existing corpus
    "DNS", "AI",
}

# ---- Fixed scam categories ----
VALID_CATEGORIES = {
    "transport", "counterfeit", "overcharging", "distraction",
    "gem", "fake-police", "digital", "rental", "temple-beg",
    "romance", "food-scam", "petty-theft",
}

VALID_DANGER = {"high", "moderate", "low"}


def _sentences(text: str):
    """Rough sentence split on [.!?] followed by whitespace or end."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def _is_in_reddit_title(text: str, match_start: int) -> bool:
    """Heuristic: if the match is between two single quotes, it's a citation."""
    before = text[:match_start]
    after = text[match_start:]
    # Find nearest single-quote boundaries
    last_open = max(before.rfind("'"), before.rfind("\u2018"))
    last_close = max(before.rfind("'"), before.rfind("\u2019"))
    if last_open > last_close:
        # We're inside a quoted span
        return True
    return False


def _is_proper_noun_phrase(text: str, match_start: int, match_end: int) -> bool:
    """Check if the BrE match is part of a known proper-noun phrase."""
    # Look at 30 chars around match
    window = text[max(0, match_start - 20): match_end + 10].lower()
    return any(p in window for p in PROPER_NOUN_ALLOWLIST)


def lint_scam(scam: dict, scam_idx: int, city: str):
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

    # ---- 7b: paragraph count ----
    paragraphs = [p.strip() for p in story.split("\n\n") if p.strip()]
    if len(paragraphs) < 4:
        add("REJECT", "7b", f"story has {len(paragraphs)} paragraphs (< 4)")
    elif len(paragraphs) > 6:
        add("WARN", "7b", f"story has {len(paragraphs)} paragraphs (> 6)")

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

        # Rule 1: AmE/BrE drift (skip reddit_sources by design: not in prose_fields)
        for m in BRE_PATTERN.finditer(text):
            if _is_in_reddit_title(text, m.start()):
                continue
            if _is_proper_noun_phrase(text, m.start(), m.end()):
                continue
            add("REJECT", "1", f"BrE form {m.group()!r} in {fname}")

        # Rule 2: Reddit citation in prose
        for m in REDDIT_IN_PROSE.finditer(text):
            add("REJECT", "2", f"Reddit citation {m.group()!r} in {fname} (use reddit_sources[] only)")

        # Rule 3: Currency no-space
        for m in CURRENCY_NOSPACE.finditer(text):
            # Ignore matches inside reddit_sources titles (we don't scan those here)
            add("REJECT", "3", f"currency no-space at {m.group()!r} in {fname}")

        # Rule 4: Currency range with hyphen or missing repeat symbol
        for m in CURRENCY_RANGE_BAD.finditer(text):
            # Only reject if it's actually missing the repeat (not already matching CURRENCY_RANGE_GOOD)
            if not CURRENCY_RANGE_GOOD.search(text[max(0,m.start()-2):m.end()+10]):
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
        stripped = item.strip().rstrip("'\"\u2019\u201d")
        if not stripped or stripped[-1] not in ".?!":
            add("REJECT", "12", f"how_to_avoid[{i}] doesn't end in .?!: {item!r}")

    # ---- 15: reddit year mix ----
    years = []
    for src in rs:
        m = re.search(r",\s*(\d{4})\)\s*$", src)
        if m:
            years.append(int(m.group(1)))
    if years:
        modern = sum(1 for y in years if y >= 2025)
        pct = 100 * modern / len(years)
        if pct < 80:
            add("WARN", "15", f"reddit_sources year mix {modern}/{len(years)} from 2025/2026 ({pct:.0f}% < 80%)")

    # ---- reddit id shape ----
    for src in rs:
        m = re.search(r"comments/([a-z0-9]+)", src)
        if not m:
            add("REJECT", "16", f"reddit_sources missing comments/<id>: {src!r}")
        elif not re.fullmatch(r"[a-z0-9]{5,8}", m.group(1)):
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

    # Opening-repetition (rule 11)
    openings = []
    for s in scams:
        story = s.get("story", "")
        # First 2 words of first paragraph's first sentence, case-folded
        first_para = story.split("\n\n")[0] if story else ""
        first_sent = _sentences(first_para)[0] if _sentences(first_para) else ""
        words = first_sent.split()[:2]
        if len(words) == 2:
            openings.append(" ".join(w.lower() for w in words))
    from collections import Counter
    opening_counts = Counter(openings)
    for op, c in opening_counts.items():
        if c >= 3:
            all_issues.append(("WARN", "11", f"{city}: {c} scams share 2-word opening {op!r}"))

    for i, scam in enumerate(scams, 1):
        all_issues.extend(lint_scam(scam, i, city))

    return all_issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", help="Path to research JSON (e.g. scams/research/tw_batch1.json)")
    ap.add_argument("--city", help="Only lint this city (if file has multiple)")
    ap.add_argument("--report", help="Write JSON report to path")
    ap.add_argument("--all", action="store_true", help="Lint every scams/research/*.json")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[1]
    targets = []
    if args.all:
        targets = sorted((repo / "scams" / "research").glob("*.json"))
    elif args.path:
        targets = [Path(args.path)]
    else:
        ap.error("need path or --all")

    all_issues = []
    for path in targets:
        try:
            data = json.load(open(path))
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
