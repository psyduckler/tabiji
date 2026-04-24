#!/usr/bin/env python3
"""Fix truncated / broken ``.scam-tldr`` pull-quotes across shipped scam pages.

The italic pull-quote at the top of every scam-card (``<p class="scam-tldr">``)
should read as a complete sentence. Many were generated from upstream prose
that got cut mid-clause — they end in an ellipsis ``...``, em-dash ``—``,
comma ``,``, colon ``:``, or semicolon ``;`` — or the writer left a mid-word
truncation that looks like a software bug on the live page.

Fix strategy (per TLDR node):

1. Parse the page, find every ``.scam-tldr``.
2. If the text is "well-closed" (ends in ``.?!`` after stripping trailing
   quotes) AND not an ellipsis, leave alone.
3. If broken, derive a replacement from the card's first ``.scam-story-body``
   sibling: take the first sentence; if too short (< 40 chars) or too long
   (> 280 chars), take the first two sentences. Ensure it ends in ``.?!``.
4. If the broken TLDR text is a verbatim head-truncation of the body's first
   sentence (the "dupe bug"), remove the TLDR paragraph entirely — the body
   already leads with the same sentence.
5. If no ``.scam-story-body`` sibling exists, remove the broken TLDR so the
   page never ships a ``...`` or mid-clause dash to a reader.

Usage::

    python3 scripts/sweep_tldr_truncation.py --dry-run --limit 5
    python3 scripts/sweep_tldr_truncation.py --city tokyo --dry-run
    python3 scripts/sweep_tldr_truncation.py --report /tmp/tldr-sweep.json
    python3 scripts/sweep_tldr_truncation.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"

# Trailing quote characters stripped before inspecting the terminal punctuation.
_TRAILING_QUOTES = "'\"\u201c\u201d\u2018\u2019"

# Characters that make a TLDR "broken" when they land at the end of the text.
_BAD_TAILS = {",", ":", ";", "\u2014", "-"}

# Sentence split: split after .?! that is followed by whitespace.
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")

# Stop-words that, when they're the final token before the terminal ``.``,
# mean the generator truncated mid-phrase and then appended a period —
# "drew 115 upvotes after a." / "target you at the." / "cheap drinks. Inside.".
# These are prepositions, articles, auxiliaries, and conjunctions that are
# never a legitimate sentence-final word in English prose.
_TRUNCATED_TAIL_WORDS = frozenset(
    {
        "a", "an", "the",
        "of", "in", "on", "at", "to", "by", "for", "with", "from", "into",
        "onto", "upon", "over", "under", "about", "after", "before",
        "during", "between", "through", "per", "via",
        "and", "or", "but", "nor", "so", "yet",
        "is", "are", "was", "were", "be", "been", "being", "am",
        "has", "have", "had", "having",
        "do", "does", "did", "doing",
        "will", "would", "shall", "should", "can", "could", "may", "might",
        "must", "ought",
        "that", "which", "who", "whom", "whose", "whether", "if",
        "as", "than", "then", "because", "while", "whereas",
        "their", "there", "these", "those", "this", "his", "her", "our",
        "your", "my", "its",
    }
)


def _strip_trailing_quotes(s: str) -> str:
    return s.rstrip(_TRAILING_QUOTES).rstrip()


def _is_ellipsis(text: str) -> bool:
    """True if text ends in an ellipsis (literal ``...`` or ``\u2026``)."""
    stripped = _strip_trailing_quotes(text)
    if stripped.endswith("\u2026"):
        return True
    if stripped.endswith("..."):
        return True
    return False


def _breakage_shape(text: str) -> str | None:
    """Classify the kind of breakage. ``None`` means the text is well-formed."""
    text = text.strip()
    if not text:
        return "empty"
    if _is_ellipsis(text):
        return "ellipsis"
    stripped = _strip_trailing_quotes(text)
    if not stripped:
        return "empty"
    tail = stripped[-1]
    if tail in {".", "!", "?"}:
        # Trailing ``.`` can still mask a mid-phrase cut: "drew 115 upvotes
        # after a." — the generator appended a period after truncating. Look
        # at the final word before the period; if it's a preposition / article
        # / auxiliary, the sentence isn't really finished.
        # Strip the terminal punctuation, then pick the last word.
        body = stripped.rstrip(".!?").rstrip()
        if body:
            # Take the last whitespace-separated token, lowercase, strip
            # surrounding punctuation (quotes, commas).
            last_token = body.split()[-1].strip(",;:()[]'\"\u201c\u201d\u2018\u2019").lower()
            if last_token in _TRUNCATED_TAIL_WORDS:
                return "mid-phrase"
        # Well-closed. (Ellipsis was caught above.)
        return None
    if tail == ",":
        return "comma"
    if tail in {";", ":"}:
        return "semicolon" if tail == ";" else "colon"
    if tail in {"\u2014", "-"}:
        return "em-dash"
    # Anything else (a letter, digit, etc.) = mid-word cut.
    if tail.isalnum():
        return "mid-word"
    return "other"


def _first_story_body(tldr_tag) -> "object | None":
    """Return the first ``.scam-story-body`` sibling following the TLDR, or None."""
    for sib in tldr_tag.find_next_siblings():
        classes = sib.get("class") or []
        if "scam-story-body" in classes:
            return sib
        # If we hit scam-details / another card boundary, stop — no body found.
        if "scam-details" in classes or "scam-card" in classes:
            return None
    return None


def _ensure_terminal(text: str) -> str:
    """Append ``.`` if text does not already end in ``.?!`` (after quotes)."""
    text = text.rstrip()
    stripped = _strip_trailing_quotes(text)
    if stripped and stripped[-1] in {".", "!", "?"}:
        return text
    # Preserve trailing quote if present — insert ``.`` before it.
    if text and text[-1] in _TRAILING_QUOTES:
        return text[:-1].rstrip() + "." + text[-1]
    return text + "."


def _derive_replacement(body_text: str) -> str | None:
    """Pick one or two sentences from ``body_text`` to use as the new TLDR."""
    body_text = body_text.strip()
    if not body_text:
        return None
    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(body_text) if s.strip()]
    if not sentences:
        return None
    first = sentences[0]
    if 40 <= len(first) <= 280:
        return _ensure_terminal(first)
    # Too short or too long — try the first two concatenated.
    if len(sentences) >= 2:
        two = (sentences[0] + " " + sentences[1]).strip()
        return _ensure_terminal(two)
    # Only one sentence and it's out of range — take it anyway, clamped.
    return _ensure_terminal(first)


def _head_truncation_of(a: str, b: str) -> bool:
    """True if ``a`` is a head prefix of ``b`` (the TLDR-dupe-of-body bug).

    Allows trailing ellipsis / em-dash / punctuation on ``a``. Compares
    case-insensitively on the leading chars. Requires ``a`` to be at least
    20 chars to avoid false positives on very short openers.
    """
    a_clean = a.rstrip(".\u2026\u2014-,;:\u201d\u2019\"' ").strip().lower()
    if len(a_clean) < 20:
        return False
    b_clean = b.strip().lower()
    return b_clean.startswith(a_clean)


def _rewrite_tldr_text(tldr_tag, new_text: str) -> None:
    """Replace the tag's text contents while preserving any child HTML tags.

    Most TLDRs are plain-text so this is just ``tag.string = new_text``.
    If the tag contains child tags (``<em>``, ``<a>``, ...) we still have no
    reliable way to re-insert the replacement with the same child structure
    — so we fall back to replacing the whole contents with a plain-text
    NavigableString. The alternative (leaving broken TLDRs in place) is
    worse for the reader.
    """
    tldr_tag.clear()
    tldr_tag.append(NavigableString(new_text))


def _process_page(html: str) -> tuple[str, dict]:
    """Return (new_html, stats) for one page."""
    soup = BeautifulSoup(html, "html.parser")
    stats = {
        "fixed": 0,
        "removed_dupe": 0,
        "removed_orphan": 0,
        "total_tldr": 0,
        "shapes": Counter(),
        "warnings": [],
    }
    tldrs = soup.select(".scam-tldr")
    stats["total_tldr"] = len(tldrs)
    for tldr in tldrs:
        text = tldr.get_text()
        if not text.strip():
            # Whitespace-only — skip per spec.
            continue
        shape = _breakage_shape(text)
        if shape is None:
            continue
        stats["shapes"][shape] += 1

        body = _first_story_body(tldr)
        if body is None:
            # No body sibling — remove the node so no ``...`` ships.
            stats["warnings"].append(
                f"tldr without sibling body: {text.strip()[:80]!r}"
            )
            tldr.decompose()
            stats["removed_orphan"] += 1
            continue

        body_text = body.get_text()

        # Dupe-bug: TLDR is a head-truncation of the body's first sentence.
        body_first = _SENTENCE_SPLIT.split(body_text.strip(), maxsplit=1)[0].strip()
        if body_first and _head_truncation_of(text, body_first):
            tldr.decompose()
            stats["removed_dupe"] += 1
            continue

        replacement = _derive_replacement(body_text)
        if replacement is None:
            # Body had no usable prose — remove the broken TLDR.
            stats["warnings"].append(
                f"tldr without usable body sentence: {text.strip()[:80]!r}"
            )
            tldr.decompose()
            stats["removed_orphan"] += 1
            continue

        _rewrite_tldr_text(tldr, replacement)
        stats["fixed"] += 1

    return str(soup), stats


def _fmt_shapes(shapes: Counter) -> str:
    if not shapes:
        return ""
    return ", ".join(f"{k}:{v}" for k, v in shapes.most_common())


def _dry_run_preview(path: Path, limit_per_page: int = 3) -> None:
    """Print what WOULD change for up to ``limit_per_page`` TLDRs on one page."""
    html = path.read_text()
    soup = BeautifulSoup(html, "html.parser")
    label = str(path.relative_to(REPO))
    print(f"  [preview] {label}")
    shown = 0
    for tldr in soup.select(".scam-tldr"):
        if shown >= limit_per_page:
            break
        text = tldr.get_text()
        if not text.strip():
            continue
        shape = _breakage_shape(text)
        if shape is None:
            continue
        body = _first_story_body(tldr)
        body_text = body.get_text() if body is not None else ""
        before = text.strip()
        body_first = (
            _SENTENCE_SPLIT.split(body_text.strip(), maxsplit=1)[0].strip()
            if body_text
            else ""
        )
        if body is None:
            after = "[REMOVE — no body sibling]"
        elif body_first and _head_truncation_of(text, body_first):
            after = "[REMOVE — dupe of body opener]"
        else:
            replacement = _derive_replacement(body_text)
            after = replacement or "[REMOVE — no usable body]"
        print(f"    shape={shape}")
        print(f"      before: {before[:160]}")
        print(f"      after:  {after[:200] if isinstance(after, str) else after}")
        shown += 1
    if shown == 0:
        print("    (no broken TLDRs found on this page)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, help="Stop after N pages (for testing)")
    ap.add_argument("--city", help="Only sweep scams/<city>/index.html")
    ap.add_argument("--report", help="Write per-file JSON report to this path")
    args = ap.parse_args()

    if args.city:
        targets = [SCAMS / args.city / "index.html"]
    else:
        targets = collect_scam_targets(city_pages=True)
    if args.limit:
        targets = targets[: args.limit]

    # Self-test preview: in dry-run mode, show the 3-TLDR preview for any of
    # the canonical self-test cities that are among ``targets``. This fires
    # both for bare ``--dry-run`` (they're in the full corpus) and for
    # ``--city tokyo --dry-run`` / ``--city kaohsiung --dry-run``.
    if args.dry_run:
        for slug in ("tokyo", "kaohsiung"):
            p = SCAMS / slug / "index.html"
            if p in targets and p.exists():
                _dry_run_preview(p, limit_per_page=3)

    total_fixed = 0
    total_removed_dupe = 0
    total_removed_orphan = 0
    total_tldr = 0
    files_changed = 0
    corpus_shapes: Counter = Counter()
    per_file_report: list[dict] = []

    for path in targets:
        if not path.exists():
            continue
        original = path.read_text()
        new_html, stats = _process_page(original)
        total_tldr += stats["total_tldr"]
        corpus_shapes.update(stats["shapes"])
        changed = (
            stats["fixed"] > 0
            or stats["removed_dupe"] > 0
            or stats["removed_orphan"] > 0
        )
        if changed and new_html != original:
            files_changed += 1
            total_fixed += stats["fixed"]
            total_removed_dupe += stats["removed_dupe"]
            total_removed_orphan += stats["removed_orphan"]
            label = str(path.relative_to(REPO))
            dupes = stats["removed_dupe"]
            orphans = stats["removed_orphan"]
            suffix = ""
            if dupes:
                suffix += f" ({dupes} duplicates removed)"
            if orphans:
                suffix += f" ({orphans} orphans removed)"
            print(
                f"  {label} — fixed {stats['fixed']}/{stats['total_tldr']} tldrs"
                f"{suffix}"
            )
            if not args.dry_run:
                path.write_text(new_html)
        per_file_report.append(
            {
                "path": str(path.relative_to(REPO)),
                "total_tldr": stats["total_tldr"],
                "fixed": stats["fixed"],
                "removed_dupe": stats["removed_dupe"],
                "removed_orphan": stats["removed_orphan"],
                "shapes": dict(stats["shapes"]),
                "warnings": stats["warnings"],
            }
        )

    action = "would fix" if args.dry_run else "fixed"
    shape_summary = _fmt_shapes(corpus_shapes)
    print(
        f"\n{action} {total_fixed} tldrs"
        f" ({total_removed_dupe} duplicates removed, "
        f"{total_removed_orphan} orphans removed)"
        f" across {files_changed} files; {total_tldr} tldrs inspected"
    )
    if shape_summary:
        print(f"breakage shapes: {shape_summary}")

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(
                {
                    "totals": {
                        "fixed": total_fixed,
                        "removed_dupe": total_removed_dupe,
                        "removed_orphan": total_removed_orphan,
                        "total_tldr": total_tldr,
                        "files_changed": files_changed,
                    },
                    "shapes": dict(corpus_shapes),
                    "per_file": per_file_report,
                },
                indent=2,
            )
        )
        print(f"wrote report to {report_path}")


if __name__ == "__main__":
    main()
