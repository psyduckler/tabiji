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

# (5) "Reddit-backed" / "Reddit-sourced" / "Reddit-Approved" in description fields.
# Case-insensitive; preserve the descriptor structure ("Reddit-backed picks"
# -> "Editor-curated picks").
REDDIT_DESC_RE = re.compile(r'Reddit-(?:backed|sourced|approved)', re.IGNORECASE)
REDDIT_DESC_REPLACEMENT = "Editor-curated"

# (5b) Country-hub & per-card Reddit-sourcing prose patterns left over after
# pass 5.  Order matters: handle the longer phrases first so substrings don't
# half-match.
EXTRA_REDDIT_SUBS = [
    # Country-hub meta/JSON-LD descriptions:
    (re.compile(r' — researched from thousands of real Reddit reviews\.?', re.IGNORECASE), '.'),
    (re.compile(r' — researched from real Reddit reviews\.?', re.IGNORECASE), '.'),
    (re.compile(r'\.+\s*$', re.MULTILINE), '.'),  # collapse the ".." we may produce
    # Per-card descriptions on hubs ("curated from Reddit reviews and local
    # recommendations." / "curated from Reddit reviews. Stalls...").  Keep the
    # rest of the sentence/paragraph intact.
    (re.compile(r'curated from Reddit reviews and local recommendations', re.IGNORECASE),
     'editor-curated'),
    (re.compile(r'curated from Reddit reviews', re.IGNORECASE),
     'editor-curated'),
    (re.compile(r'powered by Reddit insights and traveler reviews', re.IGNORECASE),
     'editor-curated'),
    (re.compile(r'powered by Reddit insights', re.IGNORECASE),
     'editor-curated'),
    # Catch-all for prose patterns of the shape "curated from [...]Reddit[...]"
    # or "powered by [...]Reddit[...]" — the AI generator produces many
    # variants ("curated from Reddit threads, local reviews, and food
    # critics.", "powered by Reddit reviews and local critics,", etc.).
    # Match through to the next sentence boundary or HTML tag and replace with
    # neutral "editor-curated".  Bounded length keeps it from running away.
    (re.compile(r'curated from (?:real )?Reddit[^.<]{0,200}', re.IGNORECASE),
     'editor-curated'),
    (re.compile(r'powered by (?:real )?Reddit[^.<]{0,200}', re.IGNORECASE),
     'editor-curated'),
    (re.compile(r'backed by (?:real )?Reddit reviews[^.<]{0,200}', re.IGNORECASE),
     'editor-curated'),
    (re.compile(r'verified with (?:[^.<]{0,40})?real Reddit reviews', re.IGNORECASE),
     'verified with traveler reviews'),
    # FAQ JSON-LD answer prose patterns ("Based on Reddit consensus and local
    # rankings, Lou Malnati's...") — render in Google's PAA box.  Replace the
    # Reddit framing with a neutral source claim.
    (re.compile(r'Based on Reddit consensus and (?:local rankings|local recommendations|local reviews|critic rankings|critic picks|critic reviews)', re.IGNORECASE),
     'Based on local consensus'),
    (re.compile(r'Based on Reddit consensus(?:,| from| across)([^.<]{0,80})', re.IGNORECASE),
     r'Based on local consensus\1'),
    (re.compile(r'\bBased on Reddit consensus\b', re.IGNORECASE), 'Based on local consensus'),
    (re.compile(r'\bAccording to Reddit (?:consensus|expats(?: and residents)?|threads)\b', re.IGNORECASE),
     'According to local consensus'),
    (re.compile(r'\bAccording to Redditors(?:[^.<]{0,40})?\b', re.IGNORECASE),
     'According to locals'),
    (re.compile(r'\bReddit consistently calls\b', re.IGNORECASE), 'Locals consistently call'),
    (re.compile(r'"servesCuisine":\s*"Reddit\'s #1"', re.IGNORECASE),
     '"servesCuisine": "Local favorite"'),
    # Hub FAQ:
    (re.compile(r'researched from thousands of Reddit posts(?:[^.<]{0,80})?', re.IGNORECASE),
     'editor-curated from research across travel forums and local-knowledge sources'),
    (re.compile(r'built from real Reddit discussions and traveler recommendations', re.IGNORECASE),
     'built from editorial research and traveler discussion patterns'),
    # Visible-prose phrasings: drop the false sourcing chrome but keep the
    # surrounding sentence intact.
    (re.compile(r'\bReddit users\b', re.IGNORECASE), 'travelers'),
    (re.compile(r'\bReddit locals\b', re.IGNORECASE), 'locals'),
    (re.compile(r'\bReddit-vetted\b', re.IGNORECASE), 'editor-vetted'),
    (re.compile(r'\bReddit (?:consensus|recommendations|insights|threads)\b', re.IGNORECASE),
     'local consensus'),
    (re.compile(r'\s*[—–-]\s*The Reddit Guide', re.IGNORECASE), ''),
    (re.compile(r'researched from real Reddit reviews', re.IGNORECASE), 'editor-curated'),
    (re.compile(r'across Reddit and (?:food|travel) blogs', re.IGNORECASE),
     'across travel forums'),
    (re.compile(r'(?:hand-picked|ranked|backed|vetted)(?: from| by| with)? (?:hundreds of|100\+|thousands of)? ?Reddit (?:reviews|recommendations|threads|insights|posts)[^.<]{0,80}', re.IGNORECASE),
     'editor-curated'),
    (re.compile(r'highly rated by Reddit (?:users|locals)? ?and (?:local )?critics', re.IGNORECASE),
     'highly rated by locals and critics'),
    # "curated from <quantity> Reddit reviews" variants the earlier rule missed.
    (re.compile(r'curated from (?:hundreds of|thousands of|\d+\+?) Reddit (?:reviews|recommendations)', re.IGNORECASE),
     'editor-curated'),
    # "backed by Reddit and <something>" — Reddit is followed by an "and"
    # conjunction, so the earlier `Reddit (?:reviews|...)` pattern doesn't fit.
    (re.compile(r'(?:backed|curated|powered) by Reddit and [^.<]{0,80}', re.IGNORECASE),
     'editor-curated'),
    # Internal QA debug string ("Source quality: 1 sources · reddit, legacy-html
    # · low confidence") rendered visibly on ~2,500 pages — drop the entire
    # string + any leading whitespace and trailing punctuation/separator.
    (re.compile(r'\s*Source quality:\s*\d+\s*sources?\s*·\s*reddit[^<]*?(?:low|medium|high)?\s*confidence\s*', re.IGNORECASE),
     ''),
    # Anchor IDs / data attributes derived from the now-fixed "Reddit's #1"
    # servesCuisine — strip the few remaining slug fragments.
    (re.compile(r"reddit(?:'|&#39;)?s-#?1", re.IGNORECASE), 'local-favorite'),
    # Cleanup: prior runs of (5) "Reddit-backed -> Editor-curated" produced
    # "Editor-curated curated lists" when the source said "Reddit-backed
    # curated lists".  Collapse the duplicate adjacent "curated" word.
    (re.compile(r'\bEditor-curated curated\b', re.IGNORECASE), 'Editor-curated'),
]

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
        "extra_phrase": 0,
    }

    new_html, counts["aggregateRating"] = AGGREGATE_RATING_RE.subn("", html)
    new_html, counts["methodology"] = METHODOLOGY_RE.subn("\n", new_html)
    new_html, counts["source_span"] = SOURCE_SPAN_RE.subn(REPLACEMENT_SOURCE_SPAN, new_html)
    new_html, counts["title_suffix"] = TITLE_REDDIT_SUFFIX_RE.subn("", new_html)
    new_html, counts["desc_phrase"] = REDDIT_DESC_RE.subn(REDDIT_DESC_REPLACEMENT, new_html)

    for pattern, replacement in EXTRA_REDDIT_SUBS:
        new_html, n = pattern.subn(replacement, new_html)
        counts["extra_phrase"] += n

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
        # Include the popular-picks/index.html hub (not matched by the */ glob).
        if (PP_DIR / "index.html").exists():
            paths.insert(0, PP_DIR / "index.html")

    totals = {k: 0 for k in (
        "aggregateRating", "methodology", "source_span",
        "title_suffix", "desc_phrase", "intro_paragraphs", "extra_phrase",
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
    print(f"  extra phrase rewrites:   {totals['extra_phrase']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
