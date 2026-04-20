"""
Shared prose-polish helpers for every book in the Tabiji Travel Safety Series.

Applied at build time in `assemble_markdown()` (or directly in `scam_md()`) to
turn the JSON source data — which carries Reddit-URL fragments, mid-word
apostrophe breaks, and single-paragraph walls of text — into book-ready prose.

Transformations:

  1. strip_reddit_fragments(md)
     - `(comments/<hash>[, <year>])` URL fragments → removed
     - `r/<sub> 'thread title' documents/captures/reports/...:` scaffolding → removed
     - `r/<sub> 'thread title'` orphan citations → removed
     - `word' fragment` mid-word apostrophe-break → fused back (e.g., `gr' ab` → `grab`)
     - Orphan trailing single-quote marks → dropped
     - Dangling whitespace/punctuation → cleaned

  2. break_description_paragraphs(desc)
     Insert paragraph breaks before strong signal phrases that indicate a
     new sub-pattern in a scam description. Turns a 2,000-char single-block
     description into 2-4 readable paragraphs.

  3. linearize_numbered_list(desc)
     Turn trailing inline `(1) ... (2) ... (3) ...` protocol lists at the end
     of a description into proper markdown bullets.

  4. bulletize_avoidance(avoid)
     Split a run-on avoidance string into a markdown bullet list using a
     curated list of imperative / conditional / topic-lead starter words,
     with a post-validation pass that rejoins splits where the preceding
     word is a capitalized proper-noun fragment (preventing `Ocean / Park`,
     `Tang Dynasty / Show`, `WeChat / Pay` false splits).

  5. fix_alt_text_double_the(md)
     Repair `depicting the The X scam` → `depicting the X scam` in image
     alt text (scam names beginning with "The" produce "the The" under the
     default alt-text template).
"""
from __future__ import annotations

import re


# ---------------------------------------------------------------------------
# 1. Reddit URL fragment + scaffolding stripper
# ---------------------------------------------------------------------------


# Reddit-scaffolding preamble verbs. When a `r/SUB 'title'` citation is
# immediately followed by one of these verbs + colon, the whole construct is
# stripped. Example: "r/travelchina 'thread title' documents: ..." — the whole
# preamble up to and including the colon is removed.
_CITATION_VERBS = (
    r"documents?|captures?|reports?|notes?|says?|observes?|details?|confirms?|"
    r"catalogs?|corroborates?|describes?|frames?|warns?(?:\s+directly)?|"
    r"records?|mentions?|recounts?|explains?|complains?|shows?|"
    r"walks?\s+through|applies|is|are|was|were|gives?|adds?|"
    r"has\s+\w+|have\s+\w+|"
    r"gives?\s+the\s+[\w-]+(?:\s+\w+)*\s*(?:rule|pattern|warning|advice|fix|defence|defense|protocol|lesson)|"
    r"names?\s+the\s+\w+\s+pattern\s+as|"
    r"calls?\s+out|"
    r"lists?"
)


def strip_reddit_fragments(md: str) -> str:
    """Strip Reddit URL fragments, citation scaffolding, and word-break artifacts.

    Order matters:
      1. URL fragments (`(comments/hash)`) — must run first
      2. Reddit scaffolding (`r/SUB 'title' verb:`) — must run BEFORE mid-word
         repair, because mid-word repair corrupts the closing quote + space
         between title and verb (e.g., `Jakarta' documents` → `Jakartadocuments`
         destroys the citation pattern).
      3. Mid-word apostrophe-break repair — runs LAST on prose that's already
         had citations stripped.
    """
    # ---- PASS 1: URL fragment stripping ----
    md = re.sub(r"\s*\(comments/[a-z0-9]+(?:,\s*\d{4})?\)", "", md)
    md = re.sub(r"\s*comments/[a-z0-9]+", "", md)

    # ---- PASS 2: Reddit citation scaffolding — MUST RUN BEFORE mid-word repair ----
    # Strategy: strip the ENTIRE citation sentence, not just the preamble.
    # Citations in the source follow the pattern:
    #   `r/SUB 'title' (comments/hash) documents the pattern and X.`
    # After Pass 1 removes (comments/hash), the sentence becomes:
    #   `r/SUB 'title' documents the pattern and X.`
    # Stripping just `r/SUB 'title' documents` leaves an orphan `the pattern
    # and X.` that reads as a subject-less fragment. So we strip through the
    # next sentence terminator.
    #
    # Pattern A: citation + verb + colon + quoted evidence + period
    #   `r/SUB 'title' documents: 'the quoted evidence.' `
    # Uses `.+?` (non-greedy any-char) for title/evidence so that titles
    # containing internal apostrophes (e.g., `'I'm going to Barcelona'`)
    # still match. The trailing verb anchors the title boundary.
    md = re.sub(
        r"\s*r/\w+\s+['\u2018\u2019\"].+?['\u2018\u2019\"]"
        r"\s*(?:" + _CITATION_VERBS + r")\s*:\s*"
        r"['\u2018\u2019\"].+?['\u2018\u2019\"]\s*\.?",
        " ",
        md,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # Pattern B: citation + verb + continues through next period
    #   `r/SUB 'title' shows how fresh the concern still is.`
    md = re.sub(
        r"\s*r/\w+\s+['\u2018\u2019\"].+?['\u2018\u2019\"]"
        r"\s*(?:" + _CITATION_VERBS + r")\b[^.\n]{0,500}\.",
        " ",
        md,
        flags=re.IGNORECASE,
    )

    # Pattern C: standalone `r/SUB 'title'` citation (no verb), possibly
    # with leading "per"/"from"/"via". Strip through next period.
    md = re.sub(
        r"\s*(?:per\s+|from\s+|via\s+)?r/\w+\s+['\u2018\u2019\"].+?['\u2018\u2019\"]"
        r"[^.\n]{0,400}\.",
        " ",
        md,
    )

    # Pattern D: bare `r/SUB 'title'` not followed by anything structured —
    # just strip the citation, leave surrounding prose.
    md = re.sub(
        r"\s*(?:per\s+|from\s+|via\s+)?r/\w+\s+['\u2018\u2019\"].+?['\u2018\u2019\"]",
        " ",
        md,
    )

    # Pattern E: malformed `r/SUB (...` with no closing paren — strip to EOL
    md = re.sub(r"\s*r/\w+\s+\([^)\n]*$", "", md, flags=re.MULTILINE)

    # Pattern F: bare `r/SUB` left after stripping
    md = re.sub(r"\s*(?:per\s+|from\s+|via\s+)?r/\w+\b(?=\s*[.,;:!?\n])", "", md)

    # ---- PASS 3: Mid-word apostrophe-break repair (AFTER scaffolding is stripped) ----
    # e.g., "gr' ab" → "grab", "sc' am" → "scam"
    # Must exclude `s'\s+` (plural-possessives: "girls' room").
    # Valid contractions like "don't X" never match because the apostrophe
    # is followed by a letter, not whitespace.
    #
    # Also exclude when the following word is a common connective/preposition/
    # pronoun — these are strong signals that we're looking at a legitimate
    # closing quote followed by the sentence continuing, e.g.:
    #   `'photo-with-cannon' and 'Dutch uniform rental' where` — KEEP as-is
    # rather than fusing to `cannonand` / `rentalwhere`.
    md = re.sub(
        r"(?<=[a-rt-z])['\u2019]\s+"
        r"(?!(?:and|or|but|where|when|while|which|that|then|until|how|why|"
        r"not|all|the|as|at|to|for|in|on|by|of|from|with|about|into|onto|"
        r"upon|you|we|they|he|she|it|i|is|are|was|were|be|been|do|does|"
        r"did|can|could|will|would|should|may|might|must|have|has|had|a|"
        r"an|any|some|this|these|those|no|so|if|than|because)\b)"
        r"(?=[a-z])",
        "",
        md,
    )

    # ---- PASS 4: Whitespace + punctuation cleanup ----
    md = re.sub(r" +([,.;:!?])", r"\1", md)   # space-before-punct → drop space
    md = re.sub(r"  +", " ", md)              # collapse double-space → single
    md = re.sub(r"\n +", "\n", md)            # leading whitespace on line → strip
    md = re.sub(r"\n{3,}", "\n\n", md)        # 3+ newlines → 2
    # Orphan sentence-start caused by removing a citation at sentence start:
    # " . The next scam..." → ". The next scam..."
    md = re.sub(r"\s+\.\s+", ". ", md)

    return md.strip() if len(md) < 50 else md


# ---------------------------------------------------------------------------
# 2. Description paragraph-breaker
# ---------------------------------------------------------------------------

_DESCRIPTION_PARA_BREAKS = [
    r"A separate variant",
    r"A related variant",
    r"A 20\d{2}-surging variant",
    r"A 20\d{2}-documented variant",
    r"A 20\d{2} variant",
    r"A common variant",
    r"Another 20\d{2} version",
    r"Another variant",
    r"Another version",
    r"The variant targeting",
    r"The specific [A-Za-z][A-Za-z0-9 '\-]{2,40} pattern:",
    r"The variant specifically",
    r"The critical variant",
    r"The most-surging",
    r"The most-documented",
    r"Crucially[,:]",
    r"Notably[,:]",
    r"Importantly[,:]",
    r"For older travellers?, the (?:defensive protocol|practical defence|practical defense|defence|defense):",
    r"For older travelers?, the (?:defensive protocol|practical defence|practical defense|defence|defense):",
    r"For the traveller?, the (?:defensive protocol|practical defence|practical defense|defence|defense):",
    r"For travellers?, the (?:defensive protocol|practical defence|practical defense|defence|defense):",
    r"The defence is",
    r"The defense is",
    r"The practical defence",
    r"The practical defense",
    r"The defensive protocol",
    r"Recent reports",
]


def break_description_paragraphs(desc: str) -> str:
    """Insert `\\n\\n` before strong signal phrases inside a scam description."""
    for sig in _DESCRIPTION_PARA_BREAKS:
        desc = re.sub(
            r"(?<=[a-z0-9\)'])\.\s+(?=" + sig + r")",
            ".\n\n",
            desc,
        )
    return desc


# ---------------------------------------------------------------------------
# 3. Numbered-list linearizer
# ---------------------------------------------------------------------------


def linearize_numbered_list(desc: str) -> str:
    """Convert inline `(1) ... (2) ... (3) ...` protocols into markdown bullets."""
    preamble_re = re.compile(
        r"((?:defensive protocol|practical defence|practical defense|defence|defense)):"
        r"\s*(?=\(1\))",
    )
    match = preamble_re.search(desc)
    if not match:
        return desc
    start = match.end()
    end_match = re.search(r"\n\n", desc[start:])
    end = start + end_match.start() if end_match else len(desc)
    body = desc[start:end].strip()
    parts = re.split(r"\s*\(\d+\)\s*", body)
    parts = [p.strip().rstrip(".").rstrip(";").strip() for p in parts if p.strip()]
    if len(parts) < 2:
        return desc
    bullets = "\n".join(f"- {b}" for b in parts)
    return desc[:match.start(1) + len(match.group(1)) + 1] + "\n\n" + bullets + desc[end:]


# ---------------------------------------------------------------------------
# 4. Avoidance bulletizer
# ---------------------------------------------------------------------------

# Curated list of imperative / conditional / topic-lead starters that mark a
# new bullet boundary. Ambiguous noun-starters (Park, Return, Hide, Load,
# Leave, Change, Move) have been REMOVED — they false-split proper nouns like
# "Ocean Park" / "Teide National Park" / "Tang Dynasty Show". The post-split
# validation pass also catches capitalized-word false-positives.
_AVOIDANCE_BULLET_STARTERS = [
    # Imperatives — unambiguous verbs
    "Use", "Book", "Verify", "Keep", "Remove", "Stay", "Ask", "Rent",
    "Install", "Download", "Pay", "Check", "Confirm", "Get", "Take", "Request",
    "Report", "Call", "Dial", "Ensure", "Insist", "Carry", "Bring", "Wear",
    "Walk", "Avoid", "Accept", "Decline", "Refuse", "Never", "Always",
    "Photograph", "Buy", "Scan", "Choose", "Show", "Swap", "Open", "Close",
    "Test", "Pre-book", "Drink", "Eat", "Arrange", "Travel",
    "Plan", "Prepare", "Put", "Make", "Set", "Hand", "Lock", "Unlock",
    "Cancel", "Reject", "Ignore", "Apply", "File", "Screenshot",
    "Cross-reference", "Say", "Expect", "Share", "Demand", "Research",
    "Opt", "Beware", "Order", "Attend", "Prefer", "Skip", "Understand",
    "Email", "Text", "Message", "Freeze", "Split", "Follow", "Confirm",
    "Allow", "Allot", "Visit", "Stand", "Sit", "Wait",
    # ALL CAPS emphasis bullets
    "NEVER", "ALWAYS", "AVOID", "REFUSE", "IGNORE", "DECLINE", "USE", "BOOK",
    "SKIP", "STOP",
    # Conditional / topic lead
    "If", "For", "When", "After", "Before", "During", "While", "Unless",
    "Once", "Upon", "Without", "Do not", "Don't",
    # Adjectives / nouns leading bullets
    "Typical", "Standard", "Safe", "Safer", "Alternative", "Legitimate",
    "Regulated", "Authentic", "Real", "Genuine", "Licensed", "Official",
    "Proper", "Correct", "Known", "Community-recommended",
    "Community-verified", "Community-vetted",
    # Compound lead phrases
    "Make sure", "In case", "On arrival", "At the", "If in doubt",
    "On the", "At night", "In advance", "Before boarding", "Before entering",
    "Older travellers", "Older travelers",
]

# Sentence-boundary starters (applied in strict mode first). Any of the above
# preceded by a sentence terminator is a strong split signal.

_STARTERS_SORTED = sorted(_AVOIDANCE_BULLET_STARTERS, key=len, reverse=True)
_STARTERS_ALT = "|".join(re.escape(s) for s in _STARTERS_SORTED)

# Strict: sentence-terminator + whitespace + starter
_AVOIDANCE_SPLIT_STRICT_RE = re.compile(
    r"(?<=[a-z0-9\)'])[.;:]\s+(?=(?:" + _STARTERS_ALT + r")\b)"
)

# Lenient: just lowercase-letter + whitespace + starter (no preceding punct).
# This catches period-less run-ons but has more false-positive risk, so we
# post-validate and rejoin splits where the preceding word is a capitalized
# proper-noun fragment.
_AVOIDANCE_SPLIT_LENIENT_RE = re.compile(
    r"(?<=[a-z0-9\)'])\s+(?=(?:" + _STARTERS_ALT + r")\b)"
)


def _is_proper_noun_boundary(prev_text: str) -> bool:
    """Return True if `prev_text` ends in a capitalized-word sequence.

    Used to rejoin lenient splits that would otherwise break a proper noun
    (e.g., `Ocean` [split] `Park` — the `Ocean` ends in a capitalized word,
    so it's almost certainly a proper-noun phrase and the split was bogus).
    """
    if not prev_text:
        return False
    # Look at the last whitespace-delimited token
    last_word = prev_text.rstrip().rsplit(None, 1)[-1] if prev_text.strip() else ""
    # Capitalized word = starts with uppercase + has at least one lowercase after
    # (to exclude ALL-CAPS abbreviations like "USE" which are in our starter list)
    return bool(re.match(r"^[A-Z][a-z]", last_word))


def bulletize_avoidance(avoid: str) -> str:
    """Split a run-on avoidance string into a markdown bullet list.

    Returns the original string if fewer than 2 plausible bullets can be
    detected (safer to leave ugly prose than to mangle a single-sentence
    instruction).
    """
    if not avoid or not avoid.strip():
        return avoid
    text = avoid.strip()

    # Pass A: apply the STRICT splitter (sentence-boundary required).
    strict_items = _AVOIDANCE_SPLIT_STRICT_RE.split(text)

    # Pass B: on each piece, apply the LENIENT splitter, then merge back any
    # splits where the preceding token is a capitalized proper-noun.
    final_items: list[str] = []
    for piece in strict_items:
        raw_parts = _AVOIDANCE_SPLIT_LENIENT_RE.split(piece)
        if len(raw_parts) <= 1:
            final_items.append(piece)
            continue
        # Walk through parts, merging back capitalized-boundary false-positives
        merged: list[str] = [raw_parts[0]]
        for part in raw_parts[1:]:
            if _is_proper_noun_boundary(merged[-1]):
                merged[-1] = merged[-1].rstrip() + " " + part.lstrip()
            else:
                merged.append(part)
        final_items.extend(merged)

    # Clean + filter
    items = [i.strip().rstrip(".").rstrip(";").strip() for i in final_items if i and i.strip()]
    if len(items) < 2:
        return avoid
    return "\n".join(f"- {item}" for item in items)


# ---------------------------------------------------------------------------
# 5. Image alt-text "the The X" repair
# ---------------------------------------------------------------------------


def fix_alt_text_double_the(md: str) -> str:
    """Repair `depicting the The Scam Name` → `depicting the Scam Name`.

    Scam names that start with "The" produce doubled-article alt text under
    the default alt-text template. Fix them at build time so screen-reader
    users hear a natural phrase.
    """
    return re.sub(
        r"(depicting\s+the)\s+The\s+",
        r"\1 ",
        md,
    )


def fix_alt_text_scam_scam(md: str) -> str:
    """Repair `... Scam scam — a Y scam rated ...` → `... Scam — a Y scam rated ...`.

    Scam names that END with "Scam" produce doubled " scam" under the default
    alt-text template (`{name} scam`). Strip the redundant lowercase "scam"
    after the name when the name already ends with "Scam".
    """
    return re.sub(
        r"(\bScam)\s+scam\s+—",
        r"\1 —",
        md,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def polish_description(desc: str) -> str:
    """Apply all description transformations in order."""
    desc = strip_reddit_fragments(desc)
    desc = break_description_paragraphs(desc)
    desc = linearize_numbered_list(desc)
    return desc


def polish_avoidance(avoid: str) -> str:
    """Apply all avoidance transformations."""
    avoid = strip_reddit_fragments(avoid)
    avoid = bulletize_avoidance(avoid)
    return avoid


def polish_location(loc: str) -> str:
    """Lightweight location-field polish: just strip Reddit fragments."""
    return strip_reddit_fragments(loc)


def polish_markdown(md: str) -> str:
    """Whole-document polish — applied to the final assembled markdown.

    Use this in `assemble_markdown()` as a final pass for fixes that need to
    see the fully-assembled document (alt-text repair, etc.).
    """
    md = fix_alt_text_double_the(md)
    md = fix_alt_text_scam_scam(md)
    return md
