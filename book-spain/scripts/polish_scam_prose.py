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
    # Strategy: strip the ENTIRE citation + any quoted evidence it introduces.
    # Citations follow several patterns after Pass 1 removes the URL fragment:
    #   `r/SUB 'title' documents: 'evidence.'`
    #   `r/SUB 'title' is a named 2025 first-person anchor: 'evidence.'`
    #   `r/SUB 'title' documents the pattern and X.`
    #   `r/SUB 'title' shows how fresh the concern still is.`
    #   `per r/SUB 'title'` (bare reference)
    #
    # Pattern A: citation + any-introductory-clause + colon + quoted evidence
    # Allows modifier text between the title-closing-quote and the colon, so
    # "r/sub 'title' is a named 2025 anchor: 'quote'" is caught.
    #
    # CRITICAL: the closing quotes (title AND evidence) must be followed by
    # whitespace / paren / end-of-line — otherwise non-greedy `.+?` stops at
    # the FIRST internal apostrophe in contractions like `won't` / `I'd` /
    # `it's`, leaving the rest of the quote orphaned in the output as
    # fragments like ". t take it back.'"
    # NOTE: evidence uses `[^.\n]{5,400}?` not `.+?` — prevents over-matching
    # when the evidence quote is never properly closed within its own sentence
    # (common when Reddit scraping leaves unclosed single-quotes with internal
    # contractions like 'It's...' ). Without this, Pattern A extends evidence
    # across multiple sentences to the next bare `'` (often the SECOND quoted
    # scam-term in a later sentence like 'cleaning'), leaving an orphan tail
    # like "even if no work was actually done." in the output.
    #
    # Trailing `[^.\n]{0,200}\.` — scrubs any trailing clause after the closing
    # evidence quote up to the next period. Fixes orphan fragments like
    # "after the victim tried to dispute." / "for tourists specifically."
    # / "leverages emotional sympathy..." that were left behind when the
    # source sentence was a single long clause with the evidence quote in
    # the middle.
    md = re.sub(
        r"\s*r/\w+\s+['\u2018\u2019\"][^.\n]{1,200}?['\u2018\u2019\"](?=[\s(,;])"  # r/sub 'title'
        r"[^.\n]{0,200}?:\s*"                                                     # any modifier + :
        r"['\u2018\u2019\"][^.\n]{5,400}?['\u2018\u2019\"](?=[\s.,;!?)]|$)"       # 'evidence'
        r"[^.\n]{0,200}\.",                                                       # trailing clause.
        " ",
        md,
        flags=re.IGNORECASE,
    )

    # Pattern B: citation + verb + continues through next period (NO colon)
    md = re.sub(
        r"\s*r/\w+\s+['\u2018\u2019\"].+?['\u2018\u2019\"](?=[\s(,;])"
        r"\s*(?:" + _CITATION_VERBS + r")\b[^.\n]{0,500}\.",
        " ",
        md,
        flags=re.IGNORECASE,
    )

    # Pattern C: standalone `r/SUB 'title'` citation (no verb) through next period
    md = re.sub(
        r"\s*(?:per\s+|from\s+|via\s+)?r/\w+\s+['\u2018\u2019\"].+?['\u2018\u2019\"](?=[\s(,;])"
        r"[^.\n]{0,400}\.",
        " ",
        md,
    )

    # Pattern D: bare `r/SUB 'title'` not followed by anything structured
    md = re.sub(
        r"\s*(?:per\s+|from\s+|via\s+)?r/\w+\s+['\u2018\u2019\"].+?['\u2018\u2019\"](?=[\s(]|$)",
        " ",
        md,
    )

    # Pattern E: malformed `r/SUB (...` with no closing paren
    md = re.sub(r"\s*r/\w+\s+\([^)\n]*$", "", md, flags=re.MULTILINE)

    # Pattern F: bare `r/SUB` left after stripping
    md = re.sub(r"\s*(?:per\s+|from\s+|via\s+)?r/\w+\b(?=\s*[.,;:!?\n])", "", md)

    # ---- PASS 3: Mid-word apostrophe-break repair — DISABLED ----
    # The historical use case was truncated Reddit quotes like `gr' ab` that
    # needed to be fused back into `grab`. But those truncations only existed
    # INSIDE Reddit citation scaffolding (`r/SUB 'title' documents: '...gr' ab...'`)
    # — and Pass 2 now strips the entire citation sentence including the quote
    # body, so the truncations are removed wholesale.
    #
    # Running a mid-word-apostrophe-repair pass on the remaining prose is NET
    # HARMFUL because it can't distinguish truncations (rare) from legitimate
    # quoted phrases followed by a lowercase continuation word (common):
    #   `'Blue Bird Taxi' stickers`     → WRONG: `Taxistickers`
    #   `'photo-with-cannon' and X`     → WRONG: `cannonand`
    #   `'Dutch uniform rental' where`  → WRONG: `rentalwhere`
    #   `'my favourite bar' pattern`    → WRONG: `barpattern`
    #
    # So this pass is intentionally a no-op. If a future change reintroduces
    # truncation patterns in the prose, re-enable with a dictionary-aware
    # word-fusion heuristic rather than a blanket regex.

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
# 6. US English + inclusive-framing normalizer
# ---------------------------------------------------------------------------

# British → American spelling conversions. Lowercase-keyed; preserves
# capitalization of matched text via case-matching replacement helper below.
#
# PROPER-NOUN SAFETY: we only match lowercase-initial words with `\b` so
# proper nouns like "HarbourFront Centre", "Singapore Cruise Centre",
# "Trawangan Dive Centre" stay intact (their "Centre" is capital-C).
_BRITISH_TO_AMERICAN = [
    # (british, american) — order matters for overlapping matches (longer first)
    ("travellers", "travelers"),
    ("traveller", "traveler"),
    ("defence", "defense"),
    ("offence", "offense"),
    ("pretence", "pretense"),
    ("licence", "license"),
    ("practised", "practiced"),
    ("organised", "organized"),
    ("organising", "organizing"),
    ("organisation", "organization"),
    ("recognised", "recognized"),
    ("recognising", "recognizing"),
    ("recognise", "recognize"),
    ("realised", "realized"),
    ("realising", "realizing"),
    ("realise", "realize"),
    ("specialised", "specialized"),
    ("specialising", "specializing"),
    ("specialise", "specialize"),
    ("apologised", "apologized"),
    ("apologise", "apologize"),
    ("prioritising", "prioritizing"),
    ("prioritised", "prioritized"),
    ("prioritise", "prioritize"),
    ("analysed", "analyzed"),
    ("analyse", "analyze"),
    ("centre", "center"),
    ("centres", "centers"),
    ("centred", "centered"),
    ("colour", "color"),
    ("colours", "colors"),
    ("coloured", "colored"),
    ("colouring", "coloring"),
    ("favour", "favor"),
    ("favours", "favors"),
    ("favourite", "favorite"),
    ("favouring", "favoring"),
    ("honour", "honor"),
    ("honours", "honors"),
    ("honoured", "honored"),
    ("humour", "humor"),
    ("labour", "labor"),
    ("labours", "labors"),
    ("labouring", "laboring"),
    ("behaviour", "behavior"),
    ("behaviours", "behaviors"),
    ("flavour", "flavor"),
    ("flavours", "flavors"),
    ("neighbour", "neighbor"),
    ("neighbours", "neighbors"),
    ("neighbouring", "neighboring"),
    ("neighbourhood", "neighborhood"),
    ("neighbourhoods", "neighborhoods"),
    ("colourful", "colorful"),
    ("colourfully", "colorfully"),
    ("kilometre", "kilometer"),
    ("kilometres", "kilometers"),
    ("cancelled", "canceled"),
    ("cancelling", "canceling"),
    ("pedestrianise", "pedestrianize"),
    ("pedestrianised", "pedestrianized"),
    ("pedestrianising", "pedestrianizing"),
    ("finalise", "finalize"),
    ("finalised", "finalized"),
    ("finalising", "finalizing"),
    ("monetise", "monetize"),
    ("monetised", "monetized"),
    ("monetising", "monetizing"),
    ("commercialise", "commercialize"),
    ("commercialised", "commercialized"),
    ("commercialising", "commercializing"),
    ("commercialisation", "commercialization"),
    ("rationalise", "rationalize"),
    ("rationalised", "rationalized"),
    ("rationalising", "rationalizing"),
    ("materialise", "materialize"),
    ("materialised", "materialized"),
    ("materialising", "materializing"),
    ("funnelled", "funneled"),
    ("funnelling", "funneling"),
    ("labelled", "labeled"),
    ("labelling", "labeling"),
    ("snorkelled", "snorkeled"),
    ("snorkelling", "snorkeling"),
    ("travelled", "traveled"),
    ("travelling", "traveling"),
    ("cancelling", "canceling"),
    ("signalled", "signaled"),
    ("signalling", "signaling"),
    ("modelled", "modeled"),
    ("modelling", "modeling"),
    ("prioritising", "prioritizing"),
    ("prioritised", "prioritized"),
    ("rumour", "rumor"),
    ("rumours", "rumors"),
    ("jewellery", "jewelry"),
    ("tyres", "tires"),
    ("tyre", "tire"),
    ("kerb", "curb"),
    ("kerbs", "curbs"),
    ("kerbside", "curbside"),
    ("aluminium", "aluminum"),
    ("catalogue", "catalog"),
    ("catalogues", "catalogs"),
    ("dialogue", "dialog"),
    ("dialogues", "dialogs"),
    ("storeys", "stories"),
    ("storey", "story"),
    ("whilst", "while"),
    ("amongst", "among"),
    ("grey", "gray"),
    ("manoeuvre", "maneuver"),
    ("manoeuvres", "maneuvers"),
    ("metre", "meter"),
    ("metres", "meters"),
    ("litre", "liter"),
    ("litres", "liters"),
    ("theatre", "theater"),
    ("theatres", "theaters"),
    ("fibre", "fiber"),
    ("fibres", "fibers"),
    ("cheque", "check"),
    ("cheques", "checks"),
    ("programme", "program"),
    ("programmes", "programs"),
    ("enquiry", "inquiry"),
    ("enquiries", "inquiries"),
    ("enquire", "inquire"),
    # Additional coverage caught by Round 1 copyedit audit
    ("acclimatise", "acclimatize"),
    ("acclimatised", "acclimatized"),
    ("acclimatises", "acclimatizes"),
    ("mechanised", "mechanized"),
    ("mechanise", "mechanize"),
    ("flavouring", "flavoring"),
    ("flavoured", "flavored"),
    ("unauthorised", "unauthorized"),
    ("authorised", "authorized"),
    ("authorisation", "authorization"),
    ("recognisable", "recognizable"),
    ("recognised", "recognized"),
    ("parlour", "parlor"),
    ("parlours", "parlors"),
    ("stabilise", "stabilize"),
    ("stabilised", "stabilized"),
    ("criticise", "criticize"),
    ("criticised", "criticized"),
    ("utilise", "utilize"),
    ("utilised", "utilized"),
    ("summarise", "summarize"),
    ("summarised", "summarized"),
    ("emphasise", "emphasize"),
    ("emphasised", "emphasized"),
    ("maximise", "maximize"),
    ("minimise", "minimize"),
    ("mobilise", "mobilize"),
    ("legalise", "legalize"),
    ("civilise", "civilize"),
    ("capitalise", "capitalize"),
    ("categorise", "categorize"),
]


def _case_match_replace(match_word: str, replacement: str) -> str:
    """Preserve the capitalization pattern of `match_word` on `replacement`.

    "Travellers" → "Travelers"    (initial cap)
    "TRAVELLERS" → "TRAVELERS"    (all caps)
    "travellers" → "travelers"    (lowercase)
    """
    if match_word.isupper():
        return replacement.upper()
    if match_word[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


# Proper-noun phrases that contain British-spelled words but must be preserved
# verbatim (e.g., because they are official brand/venue names registered with
# the British spelling). Extend this list whenever a new proper-noun leaks.
_PROPER_NOUN_EXCEPTIONS = [
    "HarbourFront Centre",          # Singapore shopping/mall
    "Singapore Cruise Centre",      # Singapore cruise terminal
    "Trawangan Dive Centre",        # Gili Islands dive operator
    "Centre Pompidou",              # Paris museum (if it ever appears)
    "Lincoln Centre",               # NYC (unlikely but safe)
    "Theatre District",             # NYC neighborhood
    "Rockefeller Centre",           # Safety in case it appears with British spelling
    "City Centre Deal",             # known retail brand
    "Queen's Park",                 # could trigger confusion
    "Covent Garden Theatre",        # London venue
]


def normalize_us_english(md: str) -> str:
    """Convert British spellings to American.

    Uses word-boundary matching + a proper-noun exception list so brand/venue
    names registered with British spelling (HarbourFront Centre, Singapore
    Cruise Centre, Trawangan Dive Centre) survive intact. All other British
    spellings — lowercase mid-sentence AND Title-Case sentence-starts — get
    normalized.

    Capitalization of matched text is preserved (Travellers → Travelers,
    TRAVELLERS → TRAVELERS).
    """
    # PHASE 1: protect proper-noun exceptions with NULL-char placeholders
    placeholders: dict[str, str] = {}
    for idx, phrase in enumerate(_PROPER_NOUN_EXCEPTIONS):
        if phrase in md:
            placeholder = f"\x00PROPN{idx:02d}\x00"
            md = md.replace(phrase, placeholder)
            placeholders[placeholder] = phrase

    # PHASE 2: British → American replacement with capitalization preservation
    def _replace(match: re.Match) -> str:
        word = match.group(0)
        british = word.lower()
        for uk, us in _BRITISH_TO_AMERICAN:
            if british == uk:
                return _case_match_replace(word, us)
        return word

    pattern = r"\b(?:" + "|".join(uk for uk, _ in _BRITISH_TO_AMERICAN) + r")\b"
    md = re.sub(pattern, _replace, md, flags=re.IGNORECASE)

    # Harbour special-case: strip unless immediately followed by "Front"
    # (protects the Singapore mall brand "HarbourFront" — though the full
    # phrase "HarbourFront Centre" is already protected via the exception list).
    md = re.sub(r"\bharbour\b(?!Front)", "harbor", md, flags=re.IGNORECASE)
    md = re.sub(r"\bharbours\b", "harbors", md, flags=re.IGNORECASE)

    # PHASE 3: restore proper-noun placeholders
    for placeholder, phrase in placeholders.items():
        md = md.replace(placeholder, phrase)

    return md


def remove_older_traveler_framing(md: str) -> str:
    """Replace age-specific "older travelers" framing with inclusive "travelers".

    The source JSON scam descriptions frame the "defensive playbook" sections
    as "For older travellers, the practical defence:" — this was originally
    intended to single out readers 60+ but has the side effect of making
    younger readers feel the advice isn't for them. Rewrite as generic
    "For travelers" so the guidance reads as universal.

    Handles the common patterns:
      "For older travelers, ..."       → "For travelers, ..."
      "For older travelers (X), ..."   → "For travelers (X), ..."
      "For older travelers and X, ..." → "For travelers and X, ..."
      "For older travelers AND X"      → "For travelers"
      "older travelers" (mid-sentence) → "travelers"
      "older traveler"                 → "traveler"

    Runs AFTER US-English normalization so it only needs to handle the
    American spelling.
    """
    # "For older travelers AND [modifier up to end-of-clause or newline]"
    # → "For travelers" (drops the AND-qualifier because "travelers" is
    # already inclusive of "anyone descending to blue flames," etc.)
    md = re.sub(
        r"For older travelers\s+AND\s+[^,.:;\n]*",
        "For travelers",
        md,
        flags=re.IGNORECASE,
    )
    # "For older travelers and [modifier]" → "For travelers"
    md = re.sub(
        r"For older travelers\s+and\s+(?:all\s+)?[^,.:;\n]*",
        "For travelers",
        md,
        flags=re.IGNORECASE,
    )
    # "For older travelers (parenthetical)" → "For travelers" (drops the
    # parenthetical because it usually repeats the age caveat)
    md = re.sub(
        r"For older travelers\s*\([^)]{0,120}\)",
        "For travelers",
        md,
        flags=re.IGNORECASE,
    )
    # Plain: "For older travelers" → "For travelers"
    md = re.sub(r"\bFor older travelers\b", "For travelers", md, flags=re.IGNORECASE)
    # Mid-sentence: "older travelers" → "travelers" — case-insensitive match,
    # but we preserve the capitalization pattern of the OPENING word ("Older"
    # → "Travelers", "older" → "travelers", "OLDER TRAVELERS" → "TRAVELERS").
    def _strip_older(match: re.Match) -> str:
        first = match.group(1)     # "older" / "Older" / "OLDER"
        second = match.group(2)    # "travelers" / "travelers" / "TRAVELERS"
        is_plural = second.lower().endswith("s")
        base = "travelers" if is_plural else "traveler"
        if first.isupper():
            return base.upper()
        if first[0].isupper():
            return base[0].upper() + base[1:]
        return base

    md = re.sub(
        r"\b(older|Older|OLDER) (travelers?|Travelers?|TRAVELERS?)\b",
        _strip_older,
        md,
    )

    # --- Age-specific numeric and descriptor phrases ---
    # Caught by Round 1 audit — these slip past the "older travelers" pattern.
    # Note: `\b` does not match between `+` and a following letter (both are
    # non-word-ish), so we use explicit `(?=\s)` or wordless lookahead where
    # `\b` is unreliable.
    age_pattern_replacements = [
        # Explicit "60+" / "65+" age markers — followed by whitespace
        (r"\bfit 60\+\s+travelers?", "fit walkers"),
        (r"\bfit 65\+\s+travelers?", "fit walkers"),
        (r"\bmoderately fit 60\+\s+travelers?", "moderately fit walkers"),
        (r"\bmoderately fit 65\+\s+travelers?", "moderately fit walkers"),
        (r"\btravelers 65\+\s+with\s+", "anyone with "),
        (r"\btravelers 60\+\s+with\s+", "anyone with "),
        (r"\bchildren and travelers 65\+\s+with\s+", "anyone with "),
        (r"\bchildren and travelers 60\+\s+with\s+", "anyone with "),
        (r"\bdivers 60\+(?=[\s;,.])", "divers with cardiovascular, respiratory, or ear-pressure concerns"),
        (r"\bdivers 65\+(?=[\s;,.])", "divers with cardiovascular, respiratory, or ear-pressure concerns"),
        # Sentence-terminal "... for 60+/65+"  (e.g., "not recommended for 65+;")
        (r"\s+for 60\+(?=[;,.)])", ""),
        (r"\s+for 65\+(?=[;,.)])", ""),
        (r"\s+recommended for 60\+(?=[;,.)])", " recommended for those who sleep well in rough conditions"),
        (r"\s+recommended for 65\+(?=[;,.)])", " recommended for those who sleep well in rough conditions"),
        # "if X 60+/65+ or ..."  (e.g., "DO NOT do 3D2N cram if 60+ or heart issues")
        (r"\s+if 60\+\s+or\s+", " if you have "),
        (r"\s+if 65\+\s+or\s+", " if you have "),
        # Over/above phrasings
        (r"\byou're over 60 or have\b", "you have"),
        (r"\byou're over 65 or have\b", "you have"),
        (r"\bif you're over 60\b", "if you have any cardiovascular concerns"),
        (r"\bif you're over 65\b", "if you have any cardiovascular concerns"),
        (r"\babove age 65\b", "with mobility limitations"),
        (r"\bskip above age 65 if\s+", "skip if "),
        (r"\babove 60 or\b", "or"),
        (r"\babove 65 or\b", "or"),
        (r"\bnot recommended above 65 or\s+", "not recommended "),
        (r"\bnot recommended above 60 or\s+", "not recommended "),
        # Older-traveler compound descriptors
        (r"\bthe older-traveler choice\b", "the quieter choice"),
        (r"\bolder-traveler choice\b", "quieter choice"),
        (r"\bfor older solo male travelers\b", "for solo travelers using dating apps"),
    ]
    for pattern, replacement in age_pattern_replacements:
        md = re.sub(pattern, replacement, md, flags=re.IGNORECASE)

    return md


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
    see the fully-assembled document (alt-text repair, US-English + inclusive
    framing normalization).

    Order matters:
      1. Alt-text repairs (work on raw markdown)
      2. US-English normalization (must run before inclusive-framing because
         inclusive-framing operates on 'travelers' in American spelling)
      3. Inclusive-framing removal ('older travelers' → 'travelers')
    """
    md = fix_alt_text_double_the(md)
    md = fix_alt_text_scam_scam(md)
    md = normalize_us_english(md)
    md = remove_older_traveler_framing(md)
    return md
