#!/usr/bin/env python3
"""Strip fabrication patterns from built popular-picks/*/index.html pages:

  1. aggregateRating JSON-LD blocks (self-declared third-party restaurant ratings —
     a Google review-snippet manual-action trigger).
  2. <section class="methodology-section"> blocks claiming "We analyzed N Reddit
     posts..." (false research-methodology claims).
  3. Reddit-quote attribution: <span class="source">— r/X · YEAR</span>
     -> <span class="source">— Editor's note</span> (kills fabricated subreddit
     attribution while keeping the editorial commentary visible).
  4. "Reddit-Backed Guide" suffix in <title>, og:title, twitter:title.
  5. "Reddit-backed" / "Reddit-sourced" in meta descriptions / og / twitter
     / JSON-LD descriptions -> "Editor-curated".
  6. Intro <p> paragraphs that make Reddit / r/<sub> / subreddit sourcing claims.

Idempotent: safe to re-run.

Usage:
  python3 scripts/strip_popular_picks_fabrications.py            # all pages
  python3 scripts/strip_popular_picks_fabrications.py SLUG ...   # specific slugs
  python3 scripts/strip_popular_picks_fabrications.py --dry-run  # report only
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PP_DIR = REPO / "popular-picks"

# (1) aggregateRating JSON-LD block.  Restaurant-schema blocks have no nested
# braces inside aggregateRating value, so [^{}]* is sufficient.
AGGREGATE_RATING_RE = re.compile(
    r'\n\s*"aggregateRating":\s*\{[^{}]*?\},',
    re.DOTALL,
)

# (2) Methodology section.
METHODOLOGY_RE = re.compile(
    r'\n?\s*<section class="methodology-section">.*?</section>\n?',
    re.DOTALL,
)

# (3) Reddit-quote attribution span.  Forms include:
#   <span class="source">— r/adelaide · 2025</span>
#   <span class="source">&mdash; r/food</span>
SOURCE_SPAN_RE = re.compile(
    r'<span class="source">[^<]*?r/[^<]*?</span>',
)
REPLACEMENT_SOURCE_SPAN = "<span class=\"source\">&mdash; Editor's note</span>"

# (4) "— Reddit-Backed Guide" appears in title, og:title, twitter:title.
# Variants seen: " — Reddit-Backed Guide" with em-dash, sometimes after a year.
TITLE_REDDIT_SUFFIX_RE = re.compile(r'\s*[—–-]\s*Reddit-Backed Guide')

# (5) "Reddit-backed" / "Reddit-sourced" in description fields.
# Case-insensitive; preserve the descriptor structure ("Reddit-backed picks"
# -> "Editor-curated picks").
REDDIT_DESC_RE = re.compile(r'Reddit-(?:backed|sourced)', re.IGNORECASE)
REDDIT_DESC_REPLACEMENT = "Editor-curated"

# (6) Intro paragraphs claiming Reddit sourcing.  Detection trigger: any of
# "Reddit", "r/<lowercase-word>", or "subreddit" appears in the paragraph text.
INTRO_SECTION_RE = re.compile(
    r'(<section class="intro-section">)(.*?)(</section>)',
    re.DOTALL,
)
PARAGRAPH_RE = re.compile(r'<p\b[^>]*>.*?</p>', re.DOTALL)
REDDIT_TRIGGER_RE = re.compile(r'\bReddit\b|\br/[a-z]|\bsubreddit', re.IGNORECASE)


def _clean_intro(intro_inner: str) -> tuple[str, int]:
    """Remove <p> blocks within the intro section that make Reddit claims."""
    removed = 0

    def _drop(m: re.Match) -> str:
        nonlocal removed
        body = m.group(0)
        text_only = re.sub(r'<[^>]+>', ' ', body)
        if REDDIT_TRIGGER_RE.search(text_only):
            removed += 1
            return ''
        return body

    cleaned = PARAGRAPH_RE.sub(_drop, intro_inner)
    # Collapse blank-line runs left behind after removing paragraphs.
    cleaned = re.sub(r'\n[ \t]*\n[ \t]*\n+', '\n\n', cleaned)
    return cleaned, removed


def strip(html: str) -> tuple[str, dict]:
    counts = {
        "aggregateRating": 0,
        "methodology": 0,
        "source_span": 0,
        "title_suffix": 0,
        "desc_phrase": 0,
        "intro_paragraphs": 0,
    }

    new_html, counts["aggregateRating"] = AGGREGATE_RATING_RE.subn("", html)
    new_html, counts["methodology"] = METHODOLOGY_RE.subn("\n", new_html)
    new_html, counts["source_span"] = SOURCE_SPAN_RE.subn(REPLACEMENT_SOURCE_SPAN, new_html)
    new_html, counts["title_suffix"] = TITLE_REDDIT_SUFFIX_RE.subn("", new_html)
    new_html, counts["desc_phrase"] = REDDIT_DESC_RE.subn(REDDIT_DESC_REPLACEMENT, new_html)

    def _intro_sub(m: re.Match) -> str:
        inner_clean, n = _clean_intro(m.group(2))
        counts["intro_paragraphs"] += n
        return m.group(1) + inner_clean + m.group(3)

    new_html = INTRO_SECTION_RE.sub(_intro_sub, new_html)

    return new_html, counts


def process(path: Path, dry_run: bool) -> dict:
    html = path.read_text()
    new_html, counts = strip(html)
    changed = new_html != html
    if changed and not dry_run:
        path.write_text(new_html)
    counts["changed"] = changed
    return counts


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    slugs = [a for a in argv[1:] if not a.startswith("--")]

    if slugs:
        paths = [PP_DIR / s / "index.html" for s in slugs]
    else:
        paths = sorted(PP_DIR.glob("*/index.html"))
        paths = [p for p in paths if p.name == "index.html"]

    totals = {k: 0 for k in (
        "aggregateRating", "methodology", "source_span",
        "title_suffix", "desc_phrase", "intro_paragraphs",
    )}
    changed_files = 0
    for path in paths:
        counts = process(path, dry_run)
        for k in totals:
            totals[k] += counts[k]
        if counts["changed"]:
            changed_files += 1

    mode = "DRY RUN" if dry_run else "APPLIED"
    print(f"[{mode}] processed {len(paths)} files")
    print(f"  files changed:           {changed_files}")
    print(f"  aggregateRating cuts:    {totals['aggregateRating']}")
    print(f"  methodology cuts:        {totals['methodology']}")
    print(f"  source-span rewrites:    {totals['source_span']}")
    print(f"  title suffix strips:     {totals['title_suffix']}")
    print(f"  desc phrase rewrites:    {totals['desc_phrase']}")
    print(f"  intro paragraphs cut:    {totals['intro_paragraphs']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
