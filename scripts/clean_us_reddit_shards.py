#!/usr/bin/env python3
"""Strip Reddit URL shards and editorial workflow artifacts from US city scam pages.

The US scam-page data (generated from SAFETY_TIPS + scam stories + FAQs)
contains research-workflow shards that were never meant to be reader-facing:

    r/savannah 'Airport taxi scam' (comments/1grpmor) is the 2025 named anchor...
    r/savannah 'What's up with the monk?' comments/1kmjc3m is the NAMED anchor
    r/memphis (comments/1i2p0sb + 1l43gh2, 2025) 2025 NAMED anchors

These patterns need to be cleaned out of visible prose. Shapes handled:

1.  `(r/<sub> '<title>' comments/xxx[, 2025])` — outer-parens citation block.
2.  `r/<sub> '<title>' (comments/xxx[, 2025])` — standard citation.
3.  `r/<sub> '<title>' comments/xxx[, 2025]` — bare-comments citation (no parens).
4.  `r/<sub> (comments/xxx[ + yyy][, 2025])` — no-title citation.
5.  Any of the above followed by "is/are/documents/captures/tracks the
    [YEAR] [CANONICAL] [NAMED] <kind> anchor[ documenting ...]" editorial tag.
6.  Leading connectors: "per ", "and ", "+ ", "; ", ", ", "— ".
7.  Leftover standalone `(comments/xxx, 2025)` fragments.
8.  Leftover standalone `, 2025)` fragments and empty parens.

The cleaner then runs grammar-fixup passes: collapse double spaces, drop
orphan semicolons, dangling connectors, empty parens, repeated punctuation.
It's idempotent — re-running on a clean file produces no change.

Operates on the 38 US city pages listed below. Does not touch non-US cities.

Usage:
    python3 scripts/clean_us_reddit_shards.py [--dry-run] [--city slug] [--test]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"

US_CITIES = [
    "anaheim", "asheville", "atlanta", "austin", "boston", "branson",
    "carmel", "charleston", "chicago", "denver", "fort-lauderdale",
    "galveston", "gatlinburg", "honolulu", "key-west", "las-vegas",
    "los-angeles", "maui", "memphis", "miami", "myrtle-beach",
    "napa-valley", "nashville", "new-orleans", "new-york-city", "orlando",
    "philadelphia", "phoenix", "portland", "san-antonio", "san-diego",
    "san-francisco", "san-juan", "savannah", "seattle", "sedona",
    "st-louis", "washington-dc",
]


# --------- regex toolkit --------- #

# A Reddit title — we can't use greedy single-quote capture because titles
# frequently contain apostrophes ("What's up with the monk?") or nested
# quotes ('Will Savannah ever "ban" STRs like Tybee?'). The reliable
# terminator is the closing quote immediately followed by ` (comments` or
# ` comments` (the citation tail). We therefore match content lazily up
# to that anchor using a lookahead.
TITLE_BODY = r"[^'\n][^\n]{0,200}?"  # any title content, bounded
# TITLE = quote + body + quote, with terminator lookahead
TITLE = (
    r"'"                 # opening quote
    r"" + TITLE_BODY +   # lazy content (may contain apostrophes)
    r"'"                 # closing quote
    r"(?=\s*\(?\s*comments/)"   # tail must start with comments/ (maybe in parens)
)

# comments ID: alphanumeric, may compound with " + other_id", optional year
COMMENTS_ID = (
    r"comments/[A-Za-z0-9_]+"          # primary id
    r"(?:\s*\+\s*[A-Za-z0-9_]+)*"      # optional " + id2 + id3"
    r"(?:,\s*(?:late\s+|early\s+)?\d{4})?"   # optional ", 2025" or ", late 2025"
)

# Parenthesized or bare comments tail (after a title or a subreddit).
COMMENTS_TAIL = (
    r"(?:"
    r"\(\s*" + COMMENTS_ID + r"\s*\)"  # (comments/xxx[, 2025])
    r"|"
    r"" + COMMENTS_ID +                # bare comments/xxx[, 2025]
    r")"
)

# The editorial "named anchor" descriptor phrase that often trails a
# citation. Caps vary (NAMED, named, Named). Kinds: anchor, follow-up,
# anchors, companion anchor, specific-operator anchor, complementary
# anchor, avoid-list anchor, trade-show variant, gold-chain anchor,
# Beale Street anchor, phone-sale anchor, cross-reference, community
# view/consensus/awareness, etc. We greedily swallow an optional
# "documenting …" / "captures …" trailing clause up to the next
# sentence-terminator (period, semicolon, or close-bracket).
ANCHOR_KIND = (
    r"(?:"
    r"[A-Za-z][A-Za-z0-9-]{0,40}\s+"          # optional qualifier (Beale, gold-chain, etc.)
    r"){0,3}?"
    # Longer alternatives first so regex prefers "anchors" over "anchor"
    r"(?:anchors|anchor|follow-ups|follow-up|variants|variant|"
    r"cross-references|cross-reference|consensus|awareness|views|view)"
)
NAMED_DESCRIPTOR = (
    r"\s+(?:is|are|was|were|remains?|captures?|covers?|tracks?|"
    r"documents?|frames?|provides?)\s+"
    r"(?:the\s+|a\s+|an\s+)?"
    r"(?:\d{4}\s+)?"
    r"(?:CANONICAL\s+|canonical\s+|direct\s+|recent\s+|cross-region\s+|broader\s+|ongoing\s+)?"
    r"(?:\d{4}\s+)?"
    r"(?:NAMED|named|Named)\s+"
    r"" + ANCHOR_KIND +
    # optional trailing "documenting/covering/tracking ... " clause.
    # Consume content up to the sentence terminator. If the terminator
    # is a period-plus-closing-quote pair like "is 'broken.'" we
    # consume the inner phrase including the period-quote, but we'll
    # reinsert a `.` in the replacement (see phase-3 fix below).
    r"(?:\s+(?:documenting|covering|tracking|on)\s+[^.;<>]*?(?=[.]))?"
)
# Also the "… 2025 NAMED anchor" tag without a leading verb, used after a
# closing paren (e.g., "(comments/xxx, 2025) 2025 NAMED anchor").
# We deliberately NOT optional-ize the ANCHOR_KIND so a bare "NAMED "
# without a kind word isn't swallowed (unless it's followed by
# punctuation/sentence-end, which LOOSE_NAMED_BARE handles).
TAG_DESCRIPTOR = (
    r"\s+(?:\d{4}\s+)?(?:NAMED|named|Named)"
    r"(?:\s+" + ANCHOR_KIND + r")?"
)

# Full citation block, optionally preceded by a connector.
CONNECTOR = r"(?:^|(?<=\s)|(?<=[;,:]\s))(?:per\s+|and\s+|\+\s+|;\s+|,\s+|—\s+|-\s+)?"

CITATION_WITH_TITLE = re.compile(
    CONNECTOR +
    r"r/[A-Za-z0-9_]+"                 # subreddit
    r"\s+" + TITLE +                   # quoted title
    r"\s*" + COMMENTS_TAIL +           # comments tail
    r"(?:" + NAMED_DESCRIPTOR + r")?"  # optional "is the … anchor" tag
    r"(?:" + TAG_DESCRIPTOR + r")?",   # or trailing tag
    re.VERBOSE | re.IGNORECASE,
)

# No-title citation: "r/memphis (comments/141rhlm)" / "per r/memphis (…)"
CITATION_NO_TITLE = re.compile(
    CONNECTOR +
    r"r/[A-Za-z0-9_]+"
    r"\s+" + COMMENTS_TAIL +
    r"(?:" + NAMED_DESCRIPTOR + r")?"
    r"(?:" + TAG_DESCRIPTOR + r")?",
    re.VERBOSE | re.IGNORECASE,
)

# Orphan-title citation after a compound: the shape
# "... r/memphis '…' (comments/…) + 'New Scam | TN DMV' (comments/…) are 2025 NAMED anchors"
# — after the first strip, we have leftover "+ 'New Scam | TN DMV' (comments/…) are 2025 NAMED anchors".
# This matches a `+` or `and`/`,`-introduced `'title' (comments/xxx[, 2025])` with
# optional trailing NAMED descriptor. It's restricted to compound-list
# context (a leading `+`, `and`, or `;` connector) so we never strip
# legitimate `'quoted text' (parenthetical explanation)` prose.
CITATION_ORPHAN_TITLE = re.compile(
    r"\s*(?:\+|and|,|;)\s+"                 # compound connector
    + TITLE +
    r"\s*" + COMMENTS_TAIL +
    r"(?:" + NAMED_DESCRIPTOR + r")?"
    r"(?:" + TAG_DESCRIPTOR + r")?",
    re.VERBOSE | re.IGNORECASE,
)

# Leadup editorial phrase that wraps a citation, e.g.
# "The 2025 NAMED anchor for this pattern is r/X 'Y' (comments/xyz, 2025)."
# The citation itself will already be gone from the passes above; we
# still need to strip the wrapper sentence. Match from "The …" through the
# end of the sentence when the sentence is now empty-stub after strip.
LEADUP_ANCHOR_SENTENCE = re.compile(
    r"(?:^|(?<=\s)|(?<=[;>]))\s*The\s+"
    r"(?:\d{4}\s+)?(?:CANONICAL\s+|canonical\s+|direct\s+)?"
    r"(?:NAMED|named)\s+" + ANCHOR_KIND +
    r"\s+(?:for\s+this\s+pattern\s+is|documenting\s+this[^.]*?is|is)\s*[.]",
    re.VERBOSE | re.IGNORECASE,
)

# Outer-parens variant: "(r/savannah 'Airport taxi scam' comments/1grpmor, 2025)"
CITATION_OUTER_PARENS = re.compile(
    r"\(\s*r/[A-Za-z0-9_]+\s+" + TITLE + r"\s*" + COMMENTS_TAIL + r"\s*\)",
    re.VERBOSE | re.IGNORECASE,
)
CITATION_OUTER_PARENS_NOTITLE = re.compile(
    r"\(\s*r/[A-Za-z0-9_]+\s+" + COMMENTS_TAIL + r"\s*\)",
    re.VERBOSE | re.IGNORECASE,
)

# Leftover bare comments tails after the main strip (defensive).
BARE_COMMENTS_TAIL = re.compile(
    r"\s*\(\s*" + COMMENTS_ID + r"\s*\)",
    re.VERBOSE | re.IGNORECASE,
)

# TLDR-specific shape: when `make_tldr` cut the story at the first "."
# and landed INSIDE a parenthesized citation that hadn't closed yet:
#   `r/DisneyPlanning 'title' (comments/1jdymmp, ...`
# The TLDR becomes the entire citation-fragment with `, ...` at end.
# Since a TLDR that's just a citation is useless, we replace the whole
# thing with `...` — the reader will see the story body below anyway.
TLDR_CITATION_ONLY = re.compile(
    r"^\s*r/[A-Za-z0-9_]+\s+'[^']*?(?:'[a-z])?[^']*?'\s*"
    r"\(\s*comments/[A-Za-z0-9_]+"
    r"(?:\s*\+\s*[A-Za-z0-9_]+)*"
    r"(?:,\s*(?:\.{3}|[a-z0-9 ]+))?\s*\)?\s*(?:\.{3})?\s*$",
    re.IGNORECASE,
)

# Standalone "is the [2025] [NAMED] anchor" leftover (no preceding citation).
STANDALONE_NAMED = re.compile(
    r"\s+(?:is|are|remains?)\s+(?:the\s+|a\s+)?"
    r"(?:\d{4}\s+)?"
    r"(?:CANONICAL\s+|canonical\s+|direct\s+)?"
    r"(?:\d{4}\s+)?"
    r"(?:NAMED|named)\s+" + ANCHOR_KIND +
    r"(?:\s+(?:documenting|covering|tracking|on)\s+[^.;<>]{0,250}?)?"
    r"(?=[.;<])",
    re.VERBOSE,
)

# Loose "2025 NAMED anchor" or "NAMED" leftover (defensive pass).
LOOSE_NAMED_ANCHOR = re.compile(
    r"\s*(?:\d{4}\s+)?(?:NAMED|named)\s+"
    r"(?:[A-Za-z][A-Za-z0-9-]{0,40}\s+){0,3}?"
    r"(?:anchor|anchors|follow-up|variant)\b"
    r"(?:\s+(?:documenting|covering|tracking|on)\s+[^.;<>]{0,250}?(?=[.;<]))?",
)
LOOSE_NAMED_BARE = re.compile(r"\s*\b2025\s+NAMED\b(?=[.;,<])")

# Orphan verb phrases after citation strip. When a citation was the subject
# of a sentence whose verb wasn't part of the NAMED_DESCRIPTOR pattern,
# stripping leaves a dangling verb fragment like:
#   " cab. documents the 'flat …' patterns"
#   "; tracks regulation changes;"
#   ". confirms Uber/Lyft is the reliable default."
# These always start right after `.` `;` or `>` with a lowercase third-
# person verb and run to the next sentence terminator.
ORPHAN_VERB_PHRASE = re.compile(
    # Use 3rd-person-singular forms only to avoid matching imperative
    # mood (e.g. "confirm the $28.50 rate" in a safety-tip).
    r"(?<=[.;>\)])\s+"
    r"(?:documents|tracks|confirms|captures|covers|provides|"
    r"frames|reports|notes|describes|details|documented|tracked|"
    r"confirmed|captured|covered|provided|framed|reported|noted|"
    r"described|detailed)\s+"
    r"[^.;<>]{0,300}?"
    r"(?=[.;<])",
)

# Collapse residual ". . " / "'. " / ".' " / "'.' " created when a citation
# clause ended mid-sentence and we preserved a boundary period that now
# butts up against an existing sentence-end period.
DOUBLE_PERIOD = re.compile(r"[.]\s*'?\s*[.]")
QUOTE_BEFORE_PERIOD_SPACE = re.compile(r"(?<=[a-z'\"])[.]'\s+(?=[A-Z])")

# Grammar fixups.
DOUBLE_SPACE = re.compile(r"  +")
# Collapse whitespace before non-period punctuation.
SPACE_BEFORE_PUNCT = re.compile(r" +([,;:!?])")
# Collapse `word + SPACE + period + SPACE + Uppercase` to `word. Upper`
# — only when the preceding char is a word character (alphanumeric/'/")
# and the following context is clearly a new sentence. This avoids
# touching `.gov` / `.com` / ellipsis cases.
SPACE_BEFORE_SENTENCE_PERIOD = re.compile(
    r"(?<=[a-zA-Z0-9'\"])\s+\.(?=\s+[A-Z])"
)
SPACE_BEFORE_CLOSE = re.compile(r" +\)")
SPACE_AFTER_OPEN = re.compile(r"\( +")
# Double-punctuation collapse, but NOT an ellipsis (`...`).
# Matches a punct followed by one or more DIFFERENT punct chars, or by the
# same char provided it's not `.` (which would indicate an ellipsis).
DOUBLE_PUNCT = re.compile(r"([,;:])[.,;:]+|([.])[,;:]+")
EMPTY_PARENS = re.compile(r"\(\s*(?:,\s*\d{4})?\s*\)")
# A list like "A, B, , and C" → "A, B, and C"
DANGLING_COMMA = re.compile(r",\s*,")
DANGLING_SEMI = re.compile(r";\s*;")
# Orphan "; and" / "; + " / "; ;" / " —;" at start of phrase fragments.
# We deliberately avoid matching before `...` (an ellipsis) or before a
# single `.` that's the start of `...`.
ORPHAN_CONNECTOR = re.compile(
    r"(?:\s*[;,:]\s*)+(?=\s*(?:and\s+|or\s+|[;,:](?!\.)|\.(?!\.\.)))"
)
# "… and .", "… and ;", "and )", "+ ," etc. → strip the connector.
# We deliberately exclude `(?=,)` so we don't swallow a legit "and" in
# "sophisticated and, in some areas, aggressive" — that reads as real
# prose. We also exclude `\s+\.\.\.` so we don't eat the "and" in
# "plaza and ..." (TLDR truncation ellipsis).
DANGLING_TRAIL = re.compile(
    r"\s+(?:and|or|plus|per|also|\+)\s*(?=[;:)]|<|\.(?!\.))"
)
# "— ;" / " — ." → drop the em-dash.
DANGLING_DASH = re.compile(r"\s+[—–-]\s*(?=[.,;:)<])")
# "documenting the pattern —" hanging with nothing after. We drop only
# the `documenting`/`covering`/`tracking` variants — NOT "on the" (which
# would wrongly eat "on the ..." TLDR ellipses).
DANGLING_DOC = re.compile(r"\s+(?:documenting|covering|tracking)\s+(?=[.,;:)<])")
# "A; ." → "A."
SEMI_BEFORE_PUNCT = re.compile(r";\s*(?=[.,)])")
# "… pattern —  <next>" — leading em-dash on a sentence after strip.
# Collapse " . " → ". " etc.
# "pattern.  Individuals wearing" → "pattern. Individuals"
# (handled by DOUBLE_SPACE already)


def clean_text(text: str) -> str:
    """Apply all cleaning passes to a chunk of text. Idempotent."""
    before = None
    passes = 0
    while before != text and passes < 6:
        before = text
        passes += 1

        # Phase 1: strip full citation blocks.
        # Order matters — outer-parens variants first so we don't leave
        # stray parens when the inner form strips.
        text = CITATION_OUTER_PARENS.sub("", text)
        text = CITATION_OUTER_PARENS_NOTITLE.sub("", text)
        text = CITATION_WITH_TITLE.sub("", text)
        text = CITATION_NO_TITLE.sub("", text)
        text = CITATION_ORPHAN_TITLE.sub("", text)

        # Phase 2: standalone leftovers.
        text = LEADUP_ANCHOR_SENTENCE.sub("", text)
        text = BARE_COMMENTS_TAIL.sub("", text)
        text = STANDALONE_NAMED.sub("", text)
        text = LOOSE_NAMED_ANCHOR.sub("", text)
        text = LOOSE_NAMED_BARE.sub("", text)
        text = ORPHAN_VERB_PHRASE.sub("", text)

        # Phase 3: grammar fixups.
        # Empty parens "( , 2025)" / "()"
        text = re.sub(r"\(\s*,\s*(?:late\s+|early\s+)?\d{4}\s*\)", "", text)
        text = re.sub(r"\(\s*\)", "", text)
        text = EMPTY_PARENS.sub("", text)

        # Dangling punctuation/connector cleanup.
        text = DANGLING_DOC.sub(" ", text)
        text = DANGLING_TRAIL.sub("", text)
        text = DANGLING_DASH.sub("", text)
        text = DANGLING_COMMA.sub(",", text)
        text = DANGLING_SEMI.sub(";", text)
        text = SEMI_BEFORE_PUNCT.sub("", text)

        # Whitespace + punctuation normalization.
        text = SPACE_BEFORE_CLOSE.sub(")", text)
        text = SPACE_AFTER_OPEN.sub("(", text)
        text = SPACE_BEFORE_PUNCT.sub(r"\1", text)
        text = SPACE_BEFORE_SENTENCE_PERIOD.sub(".", text)
        text = DOUBLE_PUNCT.sub(lambda m: m.group(1) or m.group(2), text)
        text = DOUBLE_SPACE.sub(" ", text)

        # "(per )" / "(and )" / "( )" at sentence end.
        text = re.sub(r"\((?:per|and|or|plus)\s*\)", "", text)

        # Stranded leading punctuation (". Foo" / "; Foo" / "— Foo" at start
        # of a text cell after HTML-tag like '>').
        text = re.sub(r">\s*[.;,—–-]\s+", ">", text)
        # Strand at very start of string.
        text = re.sub(r"^\s*[.;,—–-]\s+", "", text)

        # Orphan numbered-list prefix left over when the ONLY content of a
        # list item "(N) …" was a citation that got stripped. Shapes:
        #   "; (5) r/foo 'bar' (comments/xxx, 2025) tracks …" → strip
        #   leaves "; (5). Next sentence" OR "; (5) Next sentence"
        # If "(N)" is followed directly by "." or by end-of-string with
        # no content of its own, remove the orphan prefix plus its
        # preceding "; "/", ".
        text = re.sub(r"\s*;\s*\(\d+\)\s*(?=[.]|$)", "", text)
        text = re.sub(r"\s*,\s*\(\d+\)\s*(?=[.]|$)", "", text)

        # Double period collapse: ".  ." → "." (happens when descriptor
        # preserves a boundary period and the prose already ended in one).
        # Also handle ".'." (quoted-phrase-end immediately followed by a
        # boundary period) and "..". We are careful NOT to touch
        # ellipses ("...") which appear in TLDR truncation.
        text = re.sub(r"[.](?!\.)\s+[.](?!\.)", ".", text)
        text = re.sub(r"[.]'[.](?!\.)", ".'", text)
        text = re.sub(r"(?<!\.)[.][.](?!\.)", ".", text)

        # Targeted stray-quote fix: when a citation descriptor-strip
        # leaves residue like `).' Upper` — a `)` immediately followed
        # by `.` and a stray closing `'`, there was no opener for the
        # quote (the prior content was structural with `)`, not a
        # quoted phrase). Drop the `'`. This shape is only seen after
        # a descriptor strip.
        text = re.sub(r"\)\.'\s+(?=[A-Z])", "). ", text)

        # Don't restore space after punct-followed-by-uppercase — that
        # rule destroys legitimate compounds like "AllEars.Net",
        # "e.g.X", etc. The DOUBLE_SPACE collapse below handles any
        # gap left behind by a strip.

        # Sentence-join artifacts: "; — Individuals" → "; Individuals"
        text = re.sub(r"([;,])\s*[—–-]\s+", r"\1 ", text)

        # " — ." dangle
        text = re.sub(r"\s+[—–-]\s*(?=\.)", "", text)

        # Phase 4: bare r/X references (no comments/ ID) that survive Phase 1.
        # Quote char class: single, double, curly variants.
        _Q = r"['\u2018\u2019\"\u201c\u201d]"
        _TITLE = rf"{_Q}[^'\u2018\u2019\"\u201c\u201d]{{2,120}}{_Q}"

        # STRIP FULL SCAFFOLDING FIRST: shard + attribution phrase as one unit,
        # so we don't leave an orphan verb (e.g. " is the 2025 anchor:").

        # "r/X 'title' (YYYY) is the named YYYY anchor: 'quote'" → "One traveler wrote: 'quote'"
        text = re.sub(
            rf"r/\w+\s+{_TITLE}(?:\s+\([^)]{{0,40}}\))?\s+is\s+(?:the|a)\s+(?:canonical\s+)?(?:\d{{4}}\s+)?(?:named\s+)?(?:first-person\s+)?(?:community\s+)?anchor:",
            "One traveler wrote:",
            text,
        )
        # "r/X 'title' (YYYY) is blunt: 'quote'" → "Travelers are blunt: 'quote'"
        text = re.sub(
            rf"r/\w+\s+{_TITLE}(?:\s+\([^)]{{0,40}}\))?\s+is\s+blunt:",
            "Travelers are blunt:",
            text,
        )
        # "r/X 'title' (YYYY) documents/describes/confirms/frames/places/captures/applies/warns/notes [more]"
        text = re.sub(
            rf"r/\w+\s+{_TITLE}(?:\s+\([^)]{{0,40}}\))?\s+(documents?|describes?|confirms?|frames?|places?|captures?|applies|warns?|notes?)\b",
            r"Community reports \1",
            text,
        )
        # "r/X 'title' (YYYY) and" / " and r/X 'title' ..." trailing conjunctions → drop
        text = re.sub(
            rf"\s+and\s+r/\w+\s+{_TITLE}(?:\s+\([^)]{{0,40}}\))?",
            "",
            text,
        )
        # "per r/X 'title' [maybe documented anchor]"
        text = re.sub(
            rf"per\s+r/\w+\s+{_TITLE}(?:\s+documented\s+anchor)?",
            "per community reports",
            text,
        )
        # "r/X 'title' (YYYY)" standalone (sentence-fragment citation)
        text = re.sub(
            rf"r/\w+\s+{_TITLE}\s+\(\s*(?:late\s+|early\s+)?\d{{4}}(?:\s*,\s*\d{{4}})?\s*\)",
            "",
            text,
        )
        # Bare "r/X 'title'" (no year, no verb)
        text = re.sub(
            rf"r/\w+\s+{_TITLE}",
            "",
            text,
        )
        # "(r/X)" in parentheses
        text = re.sub(r"\(\s*r/\w+\s*\)", "", text)
        # "(comments/xxx, YYYY description)" — parenthetical containing comments ID + sentence
        text = re.sub(
            r"\(\s*comments/[a-z0-9]+,?\s*(?:late\s+|early\s+)?\d{4}\s+[^)]+\)",
            "",
            text,
        )
        # "(comments/xxx)" / "(comments/xxx, YYYY)" standalone parenthetical
        text = re.sub(
            r"\(\s*comments/[a-z0-9]+(?:\s*,\s*(?:late\s+|early\s+)?\d{4})?\s*\)",
            "",
            text,
        )
        # Bare "comments/xxx" without parens
        text = re.sub(r"\bcomments/[a-z0-9]{4,}\b", "", text)
        # "per the r/X community" / "per r/X community"
        text = re.sub(r"per\s+(?:the\s+)?r/\w+\s+community\b", "per Reddit", text)
        # "the r/X community"
        text = re.sub(r"\bthe\s+r/\w+\s+community\b", "Reddit", text)
        # "r/X community"
        text = re.sub(r"\br/\w+\s+community\b", "Reddit", text)
        # "per r/X"
        text = re.sub(r"\bper\s+r/\w+\b", "per Reddit", text)
        # "r/X threads?"
        text = re.sub(r"\br/\w+\s+threads?\b", "Reddit threads", text)
        # "r/X traveler reports?"
        text = re.sub(r"\br/\w+\s+traveler\s+reports?\b", "Reddit reports", text)
        # "r/X users?"
        text = re.sub(r"\br/\w+\s+users?\b", "Redditors", text)
        # Catch-all: bare r/X remaining → "Reddit"
        text = re.sub(r"\br/[A-Za-z][A-Za-z0-9_]*\b", "Reddit", text)

        # Dangling "— is a YYYY report" / "— documents" / "— describes" etc.
        # after em-dash where shard was stripped.
        text = re.sub(
            r"\s+[—–-]\s+is\s+(?:the|a)\s+(?:canonical\s+)?(?:\d{4}\s+)?(?:named\s+|first-person\s+)*(?:report|anchor|thread|post)\b[^.;]*",
            "",
            text,
        )
        text = re.sub(
            r"\s+[—–-]\s+(documents?|describes?|confirms?|frames?|places?|captures?|warns?|notes?)\b[^.;]*",
            "",
            text,
        )
        # Orphan verb phrases left after shard strip (no subject)
        # "^ is the named 2025 anchor: 'quote'" → "One traveler wrote: 'quote'"
        text = re.sub(
            r"^\s*is\s+(?:the|a)\s+(?:(?:canonical|named|first-person|community|2\d{3})\s+){0,4}anchor:\s*",
            "One traveler wrote: ",
            text,
        )
        # "[.;] is the named 2025 anchor:" mid-text
        text = re.sub(
            r"([.;])\s+is\s+(?:the|a)\s+(?:(?:canonical|named|first-person|community|2\d{3})\s+){0,4}anchor:\s*",
            r"\1 One traveler wrote: ",
            text,
        )
        # ". is [the|a] X anchor." — no quote follows — drop entirely
        text = re.sub(
            r"([.;])\s+is\s+(?:the|a)\s+(?:(?:canonical|named|first-person|community|2\d{3})\s+){0,4}anchor\.\s*",
            r"\1 ",
            text,
        )
        # "^is blunt: 'quote'" → "Travelers are blunt: 'quote'"
        text = re.sub(r"^\s*is\s+blunt:\s*", "Travelers are blunt: ", text)
        text = re.sub(r"([.;])\s+is\s+blunt:\s*", r"\1 Travelers are blunt: ", text)
        # "^ applies the X rule at Y" → "The same rule applies at Y"
        text = re.sub(r"^\s*applies\s+the\s+\w[\w\s-]*?\s+rule\s+", "The same rule applies ", text)
        text = re.sub(r"([.;])\s+applies\s+the\s+\w[\w\s-]*?\s+rule\s+", r"\1 The same rule applies ", text)
        # "^ documents" → "Community reports document"
        text = re.sub(r"^\s*documents?\s+", "Community reports document ", text)
        text = re.sub(r"([.;])\s+documents?\s+", r"\1 Community reports document ", text)
        # Orphan describe/confirm/frame/place/capture/warn/note verbs at start
        text = re.sub(
            r"^\s*(describes?|confirms?|frames?|places?|captures?|warns?|notes?)\s+",
            r"Community reports \1 ",
            text,
        )
        text = re.sub(
            r"([.;])\s+(describes?|confirms?|frames?|places?|captures?|warns?|notes?)\s+",
            r"\1 Community reports \2 ",
            text,
        )
        # Semi-colon + orphan verb ("; documents ¥300+ scams" → "; community reports document ¥300+ scams")
        # Already handled above.

        # Re-apply grammar fixups after Phase 4
        text = DOUBLE_SPACE.sub(" ", text)
        text = re.sub(r"\s+([,.;:])", r"\1", text)
        text = re.sub(r"\(\s*\)", "", text)
        text = re.sub(r",\s*,", ",", text)
        text = re.sub(r",\s*\.", ".", text)
        # Double period from shard-before-period removal
        text = re.sub(r"(?<!\.)\.{2}(?!\.)", ".", text)

    return text


# --------- HTML-surgical application --------- #
#
# The cleaner is prose-focused — applying it to raw HTML would break
# indentation, JS, JSON-LD keys, etc. Instead we target the specific
# regions where generate_pages.py interpolates user-facing prose:
#
#   * JSON-LD FAQPage `"text": "..."`           — structured data
#   * `<p class="scam-tldr">...</p>`              — TL;DR above each scam card
#   * `<p class="scam-story-body">...</p>`        — main story paragraphs
#   * `<li>...</li>`   (safety-tips list items)  — top-of-page bullets
#   * `<div class="faq-a">...</div>`              — visible FAQ answers
#
# For each of these we pull out the inner content, run clean_text on it,
# and splice it back. Everything else in the HTML (DOCTYPE, scripts,
# CSS, comic <img>, breadcrumb schema, etc.) is left byte-for-byte intact.

TARGETS = [
    # name, compiled pattern with ONE capture group for the inner content
    (
        "jsonld_text",
        re.compile(r'("text":\s*")((?:\\.|[^"\\])*)(")', re.DOTALL),
    ),
    (
        "scam-tldr",
        re.compile(r'(<p class="scam-tldr">)(.*?)(</p>)', re.DOTALL),
    ),
    (
        "scam-story-body",
        re.compile(r'(<p class="scam-story-body">)(.*?)(</p>)', re.DOTALL),
    ),
    (
        "safety-tips-li",
        re.compile(r'(^\s*<li>)([^<]*?)(</li>)', re.DOTALL | re.MULTILINE),
    ),
    (
        "faq-a",
        re.compile(r'(<div class="faq-a">)(.*?)(</div>)', re.DOTALL),
    ),
    (
        "faq-q",
        re.compile(r'(<button class="faq-q"[^>]*>)(.*?)(</button>)', re.DOTALL),
    ),
    (
        "scam-story",
        re.compile(r'(<p class="scam-story">)(.*?)(</p>)', re.DOTALL),
    ),
    (
        "scam-location",
        re.compile(r'(<div class="scam-location">)(.*?)(</div>)', re.DOTALL),
    ),
    (
        "scam-title",
        re.compile(r'(<div class="scam-title">)(.*?)(</div>)', re.DOTALL),
    ),
    (
        "book-end-cta-sub",
        re.compile(r'(<p class="book-end-cta-sub">)(.*?)(</p>)', re.DOTALL),
    ),
    (
        "meta-desc",
        re.compile(r'(<meta\s+(?:name|property)="(?:description|og:description|twitter:description)"\s+content=")((?:[^"\\]|\\.)*)(")', re.DOTALL),
    ),
    (
        "jsonld_description",
        re.compile(r'("description":\s*")((?:\\.|[^"\\])*)(")', re.DOTALL),
    ),
    (
        "jsonld_headline",
        re.compile(r'("headline":\s*")((?:\\.|[^"\\])*)(")', re.DOTALL),
    ),
    (
        "plain-p",
        re.compile(r'(<p>)([^<]*?)(</p>)', re.DOTALL),
    ),
]


def _unescape_json(s: str) -> str:
    """Turn JSON-escaped text into raw text (just `\\"` → `"`, `\\\\` → `\\`).

    The FAQPage `"text": "..."` values escape double quotes as `\"`. We
    don't do full JSON decoding — we preserve all other escape sequences
    (Unicode, newlines) verbatim so the file stays byte-clean outside
    the shard region."""
    return s.replace('\\"', '"').replace("\\\\", "\\")


def _reescape_json(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def clean_file(path: Path, dry_run: bool = False) -> tuple[int, int]:
    """Clean a single HTML file. Returns (changed_flag, bytes_stripped)."""
    if not path.exists():
        return 0, 0
    original = path.read_text(encoding="utf-8")
    cleaned = original

    for _name, pattern in TARGETS:
        def _sub(match: re.Match, _name=_name) -> str:
            opening, inner, closing = match.group(1), match.group(2), match.group(3)
            if _name == "jsonld_text":
                raw = _unescape_json(inner)
                new = clean_text(raw)
                return opening + _reescape_json(new) + closing
            new_inner = clean_text(inner)
            if _name == "scam-tldr":
                # A TLDR that consists ONLY of a citation-fragment
                # (no prose) is useless. Happens when make_tldr cut
                # at a period inside a parenthesized citation, e.g.
                # "r/DisneyPlanning 'Got sent…' (comments/1jdymmp, ...".
                # Replace with a simple placeholder.
                if TLDR_CITATION_ONLY.match(new_inner.strip()):
                    new_inner = "..."
            return opening + new_inner + closing

        cleaned = pattern.sub(_sub, cleaned)

    if cleaned == original:
        return 0, 0
    diff_size = len(original) - len(cleaned)
    if dry_run:
        print(f"  [dry-run] {path.parent.name}/{path.name}: would strip {diff_size} chars")
    else:
        path.write_text(cleaned, encoding="utf-8")
        print(f"  + {path.parent.name}/{path.name}: stripped {diff_size} chars")
    return 1, diff_size


# --------- self-test --------- #

TESTS = [
    # (input, expected_substring_absent, description)
    (
        "Drivers quote a 'flat $45–$60' to downtown per r/savannah 'Airport taxi scam' "
        "comments/1grpmor is the 2025 named anchor documenting a pattern where drivers "
        "insist the meter is 'broken.' Legitimate Uber/Lyft runs $20–$32.",
        ["comments/", "named anchor", "NAMED"],
        "apostrophe-inside-title + bare comments",
    ),
    (
        "r/savannah 'What's up with the monk on River Street?' (comments/1kmjc3m, 2025) "
        "is the 2025 named anchor. Individuals wearing orange robes approach tourists.",
        ["comments/", "named anchor", "r/savannah"],
        "apostrophe + parenthesized comments",
    ),
    (
        "The 2025 NAMED anchor for this pattern is r/Something 'Title Here' "
        "(comments/abc123, 2025). The rest continues here.",
        ["comments/", "NAMED anchor", "r/Something"],
        "leading-the-NAMED-anchor + citation",
    ),
    (
        "r/A 'B' + r/C 'D' (comments/xyz, 2025) are the 2025 NAMED anchors. "
        "Content continues.",
        ["comments/", "NAMED anchors", "r/A", "r/C"],
        "compound r/A + r/C citation",
    ),
    (
        "Verify any mailed ticket at memphistn.gov — r/memphis 'Have you RECENTLY received a fine/ticket from a red light' "
        "(comments/1i2p0sb, 2025) + 'New Scam | TN DMV' (comments/1l43gh2, 2025) are 2025 NAMED anchors; "
        "legitimate red-light tickets are $50 (not $150–$300 with 'late fees')",
        ["comments/", "NAMED anchors"],
        "compound-with-plus citation",
    ),
    (
        "Graceland upsells per r/memphis (comments/141rhlm); aggressive panhandling follows.",
        ["comments/", "r/memphis"],
        "no-title subreddit citation",
    ),
    (
        "fake mailed 'red-light camera tickets' and TN DMV phishing per r/memphis "
        "(comments/1i2p0sb + 1l43gh2, 2025) 2025 NAMED anchors; Beale-adjacent parking scams",
        ["comments/", "NAMED anchors"],
        "compound-id + tag-descriptor",
    ),
    (
        "Downtown Memphis caution per r/memphis (comments/1ezvkth, 2024) — walk in pairs.",
        ["comments/"],
        "simple citation mid-sentence",
    ),
]


def run_tests() -> bool:
    """Run self-tests; return True iff all pass."""
    all_pass = True
    for idx, (inp, must_absent, desc) in enumerate(TESTS, 1):
        out = clean_text(inp)
        ok = all(m not in out for m in must_absent)
        flag = "PASS" if ok else "FAIL"
        print(f"[{flag}] Test {idx}: {desc}")
        if not ok:
            print(f"  IN : {inp!r}")
            print(f"  OUT: {out!r}")
            print(f"  still contains: {[m for m in must_absent if m in out]}")
            all_pass = False
        else:
            print(f"  OUT: {out!r}")
    return all_pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    ap.add_argument("--city", help="Only clean a specific city slug (e.g. savannah)")
    ap.add_argument("--test", action="store_true", help="Run self-tests and exit")
    args = ap.parse_args()

    if args.test:
        ok = run_tests()
        sys.exit(0 if ok else 1)

    cities = [args.city] if args.city else US_CITIES

    total_files = 0
    total_bytes = 0
    for city in cities:
        path = SCAMS / city / "index.html"
        if not path.exists():
            print(f"  SKIP: {city} (not found)")
            continue
        changed, stripped = clean_file(path, dry_run=args.dry_run)
        total_files += changed
        total_bytes += stripped

    verb = "would strip" if args.dry_run else "stripped"
    print(f"\nDone. {total_files} file(s) modified; {verb} {total_bytes} chars total.")


if __name__ == "__main__":
    main()
