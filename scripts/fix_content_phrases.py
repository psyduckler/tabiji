#!/usr/bin/env python3
"""Two content-quality fixes from the audit P1 set:

  #25 Reduce verbatim "data-backed comparison based on Reddit discussions"
      template fingerprint. Two surfaces:
      a) Body-intro boilerplate sentence: removed entirely.
         "A data-backed comparison based on Reddit discussions, real costs,
          and traveler preferences — not generic AI filler. (Also searching
          for Y vs X? You're in the right place.)"
         The rest of the body intro keeps the "Also searching..." hint.
      b) Related-card descriptions: rotated through 4 variants, picked
         deterministically from hash(source-slug + target-slug) so the
         four phrasings distribute evenly across the corpus. Replaces
         the static "X vs Y — a data-backed comparison based on Reddit
         discussions, real costs, and traveler preferences. Honest
         verdicts for your next trip." pattern.

  #26 / #28 Drop fabrication-risk Reddit-thread counts.
      "Reviewed 50+ Reddit threads from r/travel..." style claims have
      no source. Replace "<N>+ Reddit threads" with "Reddit threads"
      (no number). Keeps the qualitative claim, drops the unverifiable
      quantity.

Idempotent. --dry-run reports without writing.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COMPARE = REPO / "compare"
HUBS = {
    "asia", "australia", "bali", "cities", "colombia", "countries", "croatia",
    "culture", "egypt", "europe", "global-mixed", "greece", "hawaii", "iceland",
    "islands", "italy", "japan", "latin-america", "luxury", "maldives", "mexico",
    "middle-east-africa", "morocco", "nature", "new-zealand", "north-america",
    "oceania", "portugal", "spain", "taiwan", "thailand", "trip-style-guides",
    "vietnam",
}

# 4 phrasings used for related-card descriptions, rotated by hash.
RELATED_VARIANTS = [
    "{pair} — costs, weather, food, and travelers' honest takes for picking your next trip.",
    "{pair} — head-to-head: budgets, transit, food, and what travelers actually prefer.",
    "{pair} — a side-by-side decision built from real prices and traveler chatter.",
    "{pair} — the practical comparison: budgets, climate, food scene, and ground-truth verdicts.",
]


# Body-intro sentence — match the four variants seen in the corpus
# (em-dash literal/&#x2014;/&mdash; + "preferences"/"experiences").
BODY_INTRO_PATTERNS = [
    re.compile(
        r"(<p>)A data-backed comparison based on Reddit discussions, "
        r"real costs, and traveler (?:preferences|experiences)\s*"
        r"(?:[—-]|&#x2014;|&mdash;)\s*not generic AI filler\.\s*"
    ),
    re.compile(
        r"(<p>)A data-backed comparison based on Reddit discussions, "
        r"real costs, and traveler (?:preferences|experiences)\.\s*"
    ),
]

# Related-card description: <a class="related-card" href="/compare/<slug>/">
#   <h3>{pair}</h3>
#   <p>{pair} — a data-backed comparison based on Reddit discussions, real costs,
#      and traveler preferences. Honest verdicts for your next trip.</p>
# Match the <p> body and replace.
RELATED_CARD_RE = re.compile(
    r'(<a class="related-card" href="/compare/([a-z0-9-]+)/"[^>]*>'
    r'<h3>([^<]+)</h3>'
    r'<p>)'
    r'(?:[^<]+? — a )?data-backed comparison based on Reddit discussions, '
    r'real costs,? and traveler preferences\.\s*'
    r'(?:Honest verdicts for your next trip\.\s*)?'
    r'([^<]*)</p>',
    re.DOTALL,
)

# Reddit thread count patterns, e.g. "50+ Reddit threads", "500+ Reddit threads"
REDDIT_COUNT_RE = re.compile(r"\b\d+\+? Reddit threads\b")


def variant_for(source_slug: str, target_slug: str) -> str:
    """Pick one of 4 variants deterministically based on slug pair hash."""
    h = hashlib.sha1(f"{source_slug}|{target_slug}".encode()).digest()
    return RELATED_VARIANTS[h[0] % len(RELATED_VARIANTS)]


def fix_leaf(path: Path, dry_run: bool) -> dict[str, int]:
    """Apply the three transformations. Returns counts per fix."""
    txt = path.read_text(errors="replace")
    orig = txt
    counts = {"body_intro": 0, "related_card": 0, "reddit_count": 0}
    source_slug = path.parent.name

    # Body-intro: remove the boilerplate sentence(s)
    for pat in BODY_INTRO_PATTERNS:
        new, n = pat.subn(r"\1", txt)
        if n:
            counts["body_intro"] += n
            txt = new

    # Related-card descriptions: rotate variant
    def rcb(m: re.Match) -> str:
        target = m.group(2)
        pair = m.group(3)
        tail = m.group(4) or ""
        variant = variant_for(source_slug, target).format(pair=pair)
        counts["related_card"] += 1
        return f"{m.group(1)}{variant} {tail.strip()}</p>".rstrip(" ").replace(" </p>", "</p>")

    txt = RELATED_CARD_RE.sub(rcb, txt)

    # Reddit thread counts: drop the number
    new, n = REDDIT_COUNT_RE.subn("Reddit threads", txt)
    if n:
        counts["reddit_count"] += n
        txt = new

    if txt != orig and not dry_run:
        path.write_text(txt)
    return counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    leaves = sorted(p for p in COMPARE.glob("*/index.html") if p.parent.name not in HUBS)
    totals = {"body_intro": 0, "related_card": 0, "reddit_count": 0}
    leaves_touched = 0

    for leaf in leaves:
        counts = fix_leaf(leaf, args.dry_run)
        if any(counts.values()):
            leaves_touched += 1
        for k, v in counts.items():
            totals[k] += v

    print(f"Leaves processed:    {len(leaves)}")
    print(f"Leaves touched:      {leaves_touched}")
    print(f"  Body-intro removals:    {totals['body_intro']}")
    print(f"  Related-card variants:  {totals['related_card']}")
    print(f"  Reddit-count drops:     {totals['reddit_count']}")
    if args.dry_run:
        print("\n[dry-run — no files modified]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
