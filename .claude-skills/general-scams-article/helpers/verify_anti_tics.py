#!/usr/bin/env python3
"""Pass 8 — automated AI-tic detection.

Greps the body text of /scams/everywhere/<slug>/index.html for the
banned phrases, banned constructions, and ratio violations defined in
audit-checklists/pass-8-ai-tics.md.

Returns exit 0 if all checks pass; exit 1 if any hard-fail.

Usage:
    python3 helpers/verify_anti_tics.py <slug>
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]


# --- Hard-banned phrases (any occurrence = hard fail) ---
BANNED_PHRASES = [
    "It's worth noting",
    "It's important to remember",
    "At the end of the day",
    "In today's world",
    "In the digital age",
    "In this day and age",
    "Rest assured",
    "The bottom line",
    "The simple truth",
    "It's a testament to",
    "Navigate the complexities",
    "Tapestry",
    "Delve",
    "Delving",
    "Let me be clear",
    # Cross-page formula tics (added 2026-04-29 corpus audit) — appearing
    # verbatim across multiple /scams/everywhere/ pages was the worst
    # editorial smell in the audit. These hard-fail to keep them out.
    "The script is one. The",
]

# --- Soft-capped phrases (caps per 5,000 words) ---
SOFT_CAPS = {
    "essentially": 2,
    "ultimately": 2,
    "Furthermore,": 2,
    "Moreover,": 2,
    "However,": 4,
    "Indeed,": 2,
    # Cross-page formula tics (2026-04-29 corpus audit). These were the
    # paragraph-3 / paragraph-close formulas that appeared in every variant
    # of every page until the audit caught them. Allow ≤1 per page so the
    # phrase can still appear as language but not as the cross-variant formula.
    "The defense is ": 1,
    "The single decision rule": 1,
    "The single sentence": 1,
}

# --- Banned constructions (regex) ---
BANNED_REGEXES = [
    (r"\bX is not Y[,.]? but Z\b", "balanced-clause AI tic"),
    (r"on (the )?one hand[,.]?.+?on (the )?other hand", "balanced 'on one hand' construction"),
    (r"\bmyriad\b", "diction over-reach: 'myriad'"),
    (r"\bplethora\b", "diction over-reach: 'plethora'"),
    (r"\bshowcase[ds]?\b", "diction over-reach: 'showcase'"),
    (r"\bleverage[sd]?\b", "diction over-reach: 'leverage'"),
]

# --- Diction trio cap ---
DICTION_TRIO = ["calibrated", "engineered", "industrial"]
DICTION_TRIO_CAP = 4


def extract_body_text(html: str) -> str:
    """Extract text from <body> minus <script> and <style> blocks."""
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
    if not body_match:
        return ""
    body = body_match.group(1)
    body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.DOTALL)
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"&[a-z]+;", " ", body)
    body = re.sub(r"\s+", " ", body)
    return body.strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: verify_anti_tics.py <slug>", file=sys.stderr)
        sys.exit(2)
    slug = sys.argv[1]
    page_path = REPO / "scams" / "everywhere" / slug / "index.html"
    if not page_path.exists():
        print(f"Page not found: {page_path}", file=sys.stderr)
        sys.exit(2)

    html = page_path.read_text()
    body = extract_body_text(html)
    word_count = len(body.split())
    sentence_count = max(1, len(re.findall(r"[.!?]+", body)))
    em_dash_count = body.count("—")

    print(f"Auditing {page_path}")
    print(f"Body word count: {word_count}")
    print(f"Sentence count: {sentence_count}")
    print(f"Em-dash count: {em_dash_count}")
    print()

    fails = []
    warns = []

    # Em-dash density
    em_dash_density = em_dash_count / (word_count / 100) if word_count else 0
    if em_dash_density > 1.5:
        fails.append(f"Em-dash density {em_dash_density:.2f}/100w > 1.5")
    em_dash_per_sentence = em_dash_count / sentence_count
    if em_dash_per_sentence > 0.4:
        fails.append(f"Em-dash:sentence ratio {em_dash_per_sentence:.2f} > 0.4")

    # Banned phrases (case-insensitive)
    body_lower = body.lower()
    for phrase in BANNED_PHRASES:
        count = body_lower.count(phrase.lower())
        if count:
            fails.append(f"Banned phrase '{phrase}' appears {count}x")

    # Soft caps (per 5,000 words; scale)
    scale_factor = max(1, word_count / 5000)
    for phrase, cap in SOFT_CAPS.items():
        count = body_lower.count(phrase.lower())
        scaled_cap = int(cap * scale_factor)
        if count > scaled_cap:
            warns.append(f"Soft-cap '{phrase}' appears {count}x (cap {scaled_cap})")

    # Banned regexes
    for pattern, label in BANNED_REGEXES:
        matches = re.findall(pattern, body, re.IGNORECASE)
        if matches:
            fails.append(f"Banned construction ({label}): {len(matches)} match(es)")

    # Diction trio cap
    trio_count = sum(body_lower.count(w.lower()) for w in DICTION_TRIO)
    if trio_count > DICTION_TRIO_CAP:
        fails.append(
            f"Diction trio (calibrated/engineered/industrial): {trio_count}x > cap {DICTION_TRIO_CAP}"
        )

    # Reading level (rough Flesch Reading Ease approximation)
    syllables = sum(_count_syllables(w) for w in body.split())
    if word_count and sentence_count:
        flesch = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (
            syllables / word_count
        )
        if flesch < 50:
            warns.append(f"Flesch Reading Ease {flesch:.1f} < 50 (heavy reading)")
        else:
            print(f"Flesch Reading Ease: {flesch:.1f}")

    # Report
    print()
    if fails:
        print(f"❌ {len(fails)} HARD FAILS:")
        for f in fails:
            print(f"  - {f}")
    if warns:
        print(f"⚠ {len(warns)} WARNINGS:")
        for w in warns:
            print(f"  - {w}")
    if not fails and not warns:
        print("✓ All anti-tic checks pass")

    sys.exit(1 if fails else 0)


_VOWELS = "aeiouy"


def _count_syllables(word: str) -> int:
    word = word.lower().strip(".,;:!?\"'()[]")
    if not word:
        return 0
    count = 0
    prev_was_vowel = False
    for ch in word:
        is_vowel = ch in _VOWELS
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


if __name__ == "__main__":
    main()
