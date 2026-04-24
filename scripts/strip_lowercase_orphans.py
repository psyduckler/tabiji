#!/usr/bin/env python3
"""Detect + strip lowercase-opener orphan sentences.

The existing scripts/strip_orphan_phrases.py catches "is the 2025 anchor"-style
orphans (verb + determiner + signal-noun), but leaves behind editorial tags
that happen to start with a lowercase verb / determiner after `. `. Examples
auditor flagged:
    "... . is the cross-posted 2025 variant."
    "... . for a specific company."
    "... . cover cruise-day and visit landscape."

Root cause: the Reddit-shard sanitizer strips citation bodies but leaves
tags that were syntactically attached to the citation.

Natural English prose never starts a sentence with a lowercase letter
(outside of rare technical openers: iOS, iPhone, eBay, etc.), so
`\\.\\s+[a-z]` after a sentence boundary is a strong signal of an orphan.

This script has three modes:
  --detect-only   Print every match with 60-char context before + after.
                  Useful for human review before any write.
  --dry-run       Same detection + preview of the strip action.
  (write)         Apply strips and log per-file counts.

Targets for HTML: text inside `.scam-story-body`, `.scam-tldr`, and
top-level prose paragraphs (excluding navigation, TOC, footer, cards).

Targets for research JSON: the `story` string, and `red_flags[]` /
`how_to_avoid[]` entries.

A small ALLOWLIST skips legitimate lowercase-opener tokens (iOS, iPhone,
iPad, iMac, iCloud, eBay, iMessage, iBooks). Extend as false positives
appear.

Usage:
    python3 scripts/strip_lowercase_orphans.py --detect-only
    python3 scripts/strip_lowercase_orphans.py --dry-run
    python3 scripts/strip_lowercase_orphans.py
    python3 scripts/strip_lowercase_orphans.py --detect-only --limit 10
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets

REPO = Path(__file__).resolve().parents[1]

# Lowercase-opener technical terms that are NOT orphans.
ALLOWLIST = {
    "iOS",
    "iPhone",
    "iPad",
    "iMac",
    "iCloud",
    "iMessage",
    "iBooks",
    "eBay",
    "pH",
    "mRNA",
}

# Coordinating conjunctions that occasionally open a sentence in informal
# prose ("And we walked away."). Skip these — too ambiguous.
_CONJUNCTIONS = {"and", "but", "or", "so", "for", "yet", "nor"}

# Any quote-like character. If the matched sentence contains a quote, the
# detector likely truncated mid-quoted-title; stripping would corrupt the
# surrounding prose. Flag for human review via --detect-only; don't auto-strip.
_QUOTE_CHARS = set("'\"\u2018\u2019\u201c\u201d")

# HTML entity forms of the same quote characters — we scan raw HTML source
# in the stripper (not decoded text), so these need to be recognized too.
_QUOTE_ENTITIES = (
    "&apos;",
    "&quot;",
    "&#x27;",
    "&#X27;",
    "&#39;",
    "&#x22;",
    "&#X22;",
    "&#34;",
    "&#x2018;",
    "&#x2019;",
    "&#x201c;",
    "&#x201d;",
    "&lsquo;",
    "&rsquo;",
    "&ldquo;",
    "&rdquo;",
)

# Common abbreviations whose trailing `.` is not a sentence boundary.
# If the preceding word matches one of these (case-insensitive), the match
# is a continuation of an address/title, not an orphan sentence.
_ABBREVIATIONS = {
    "av",
    "ave",
    "blvd",
    "rd",
    "st",
    "dr",
    "mr",
    "mrs",
    "ms",
    "jr",
    "sr",
    "no",
    "vs",
    "etc",
    "eg",
    "ie",
    "e.g",
    "i.e",
    "approx",
    "inc",
    "ltd",
    "co",
    "corp",
    "u.s",
    "u.k",
    "u.s.a",
    "u.k.a",
}

# Sentence starting with a single lowercase letter after . ! or ?
# Bounded by the next sentence terminator, HTML open/close, or newline.
_DETECTOR = re.compile(r"(?<=[.!?])\s+([a-z][^.!?<>\n]{3,300}?[.!?])")


def _first_token(match_text: str) -> str:
    stripped = match_text.lstrip()
    m = re.match(r"\S+", stripped)
    return m.group(0).rstrip(".,;:!?") if m else ""


def _match_is_allowlisted(match_text: str) -> bool:
    """Return True if the matched sentence starts with an allowlisted
    technical term (iOS, iPhone, eBay), a Reddit handle (u/xxx or r/xxx),
    or a coordinating conjunction (and/but/or/...)."""
    token = _first_token(match_text)
    if token in ALLOWLIST:
        return True
    if token.lower() in _CONJUNCTIONS:
        return True
    if re.match(r"^[ur]/\S+$", token):
        return True
    return False


def _match_is_risky(match_text: str) -> bool:
    """Return True if the match contains quote chars — the detector likely
    truncated mid-quoted-title. Don't auto-strip; let a human review via
    --detect-only. Treats both literal quotes and HTML entity encodings
    (&apos;, &#x27;, etc.) as risky markers, since we scan raw HTML source
    in the stripper."""
    if any(c in match_text for c in _QUOTE_CHARS):
        return True
    if any(ent in match_text for ent in _QUOTE_ENTITIES):
        return True
    return False


_PRECEDING_WORD_RE = re.compile(r"([A-Za-z][A-Za-z.]*)[.!?]\s*$")


def _preceded_by_abbreviation(text: str, sentence_end_idx: int) -> bool:
    """True if the `.!?` char at `sentence_end_idx - 1` is part of a known
    abbreviation (Av., Mr., etc.) rather than a real sentence terminator."""
    # Look up to 12 chars back before the terminator to capture the word.
    look_start = max(0, sentence_end_idx - 12)
    prefix = text[look_start:sentence_end_idx]
    m = _PRECEDING_WORD_RE.search(prefix)
    if not m:
        return False
    word = m.group(1).lower().rstrip(".")
    return word in _ABBREVIATIONS


def _scan_text(text: str, *, include_risky: bool = True) -> list[tuple[int, int, str, str, str, bool]]:
    """Find orphan candidates in a plain-text blob. Returns a list of
    (start, end, before_ctx, match_text, after_ctx, is_risky) tuples.

    If include_risky=False, quote-containing matches are excluded
    (same as what the stripper will touch). For --detect-only we include
    them so humans see the full picture."""
    out = []
    for m in _DETECTOR.finditer(text):
        raw = m.group(0)
        orphan = m.group(1)
        if _match_is_allowlisted(orphan):
            continue
        # Skip when preceded by a known abbreviation (Av., Mr., etc.)
        if _preceded_by_abbreviation(text, m.start()):
            continue
        risky = _match_is_risky(orphan)
        if risky and not include_risky:
            continue
        start = m.start()
        end = m.end()
        ctx_before = text[max(0, start - 60) : start]
        ctx_after = text[end : min(len(text), end + 60)]
        out.append((start, end, ctx_before, raw.strip(), ctx_after, risky))
    return out


def _strip_orphans_from_text(text: str) -> tuple[str, int]:
    """Iteratively strip non-risky orphan sentences from a plain-text blob.
    Quote-containing matches and matches preceded by a common abbreviation
    are LEFT IN PLACE. Returns (new_text, count)."""
    count = 0

    # Closure that captures the surrounding text for abbreviation-aware checks.
    current_text = text

    def _should_strip(m: re.Match) -> str:
        orphan = m.group(1)
        if _match_is_allowlisted(orphan):
            return m.group(0)
        if _match_is_risky(orphan):
            return m.group(0)
        if _preceded_by_abbreviation(current_text, m.start()):
            return m.group(0)
        return ""

    for _ in range(6):  # iterate — chained orphans can stack
        current_text = text
        before_nonrisky = len(_scan_text(text, include_risky=False))
        new = _DETECTOR.sub(_should_strip, text)
        after_nonrisky = len(_scan_text(new, include_risky=False))
        if new == text:
            break
        removed = before_nonrisky - after_nonrisky
        count += max(1, removed) if new != text else 0
        text = new
    # Whitespace cleanup identical to v1
    text = re.sub(r" +([.?!,;])", r"\1", text)
    text = re.sub(r"([.?!]) +(?=[.?!])", r"\1", text)
    return text, count


# --- HTML handling -----------------------------------------------------------

# Classes whose text content is prose we should scan for orphans.
_PROSE_SELECTORS = (".scam-story-body", ".scam-tldr")


def _scan_html(path: Path, *, include_risky: bool = True) -> list[tuple[str, str, str, bool]]:
    """Scan an HTML file. Returns a list of (before_ctx, match, after_ctx,
    is_risky) tuples — byte offsets are not preserved because we scan
    per-element."""
    html = path.read_text()
    soup = BeautifulSoup(html, "html.parser")
    findings = []
    for sel in _PROSE_SELECTORS:
        for el in soup.select(sel):
            txt = el.get_text()
            for _s, _e, before, match, after, risky in _scan_text(txt, include_risky=include_risky):
                findings.append((before, match, after, risky))
    return findings


def _strip_html_file(text: str) -> tuple[str, int]:
    """Strip orphans from HTML by operating on each target element's raw
    source substring. Uses bs4 sourceline/sourcepos to locate elements,
    then does surgical string splicing. Idempotent."""
    soup = BeautifulSoup(text, "html.parser")

    # Collect (sourceline, sourcepos, tag_name) of target prose elements.
    targets: list[tuple[int, int, str]] = []
    for sel in _PROSE_SELECTORS:
        for el in soup.select(sel):
            if el.sourceline is None or el.sourcepos is None:
                continue
            targets.append((el.sourceline, el.sourcepos, el.name))

    if not targets:
        return text, 0

    # Compute line start offsets
    line_starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            line_starts.append(i + 1)

    # Compute byte offsets and process in reverse order.
    spans: list[tuple[int, int]] = []  # (start, end_of_close_tag)
    for line, col, name in targets:
        if not (1 <= line <= len(line_starts)):
            continue
        start = line_starts[line - 1] + col
        # Find end of this element: naive search for the matching close tag.
        # These prose elements don't nest with themselves in practice.
        close_tag = f"</{name}>"
        close = text.find(close_tag, start)
        if close < 0:
            continue
        spans.append((start, close + len(close_tag)))
    spans.sort(reverse=True)

    total = 0
    for start, end in spans:
        block = text[start:end]
        # Find the boundary between open tag and interior
        open_end = block.find(">")
        if open_end < 0:
            continue
        close_start = block.rfind("<")
        if close_start <= open_end:
            continue
        interior = block[open_end + 1 : close_start]
        new_interior, n = _strip_orphans_from_text(interior)
        if n > 0 and new_interior != interior:
            total += n
            new_block = block[: open_end + 1] + new_interior + block[close_start:]
            text = text[:start] + new_block + text[end:]
    return text, total


# --- Research JSON handling --------------------------------------------------


def _scan_research_json(path: Path, *, include_risky: bool = True) -> list[tuple[str, str, str, bool]]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return []
    if not isinstance(data, dict) or "cities" not in data:
        return []
    findings = []
    for city in data.get("cities", []) or []:
        for scam in (city or {}).get("scams", []) or []:
            for key in ("story",):
                val = scam.get(key)
                if isinstance(val, str):
                    for _s, _e, before, match, after, risky in _scan_text(val, include_risky=include_risky):
                        findings.append((before, match, after, risky))
            for key in ("red_flags", "how_to_avoid"):
                arr = scam.get(key)
                if isinstance(arr, list):
                    for item in arr:
                        if isinstance(item, str):
                            for _s, _e, before, match, after, risky in _scan_text(item, include_risky=include_risky):
                                findings.append((before, match, after, risky))
    return findings


def _strip_research_json(path: Path) -> tuple[str | None, int]:
    text = path.read_text()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None, 0
    if not isinstance(data, dict) or "cities" not in data:
        return None, 0

    count = 0
    for city in data.get("cities", []) or []:
        for scam in (city or {}).get("scams", []) or []:
            val = scam.get("story")
            if isinstance(val, str):
                new, n = _strip_orphans_from_text(val)
                if n > 0:
                    scam["story"] = new
                    count += n
            for key in ("red_flags", "how_to_avoid"):
                arr = scam.get(key)
                if isinstance(arr, list):
                    for i, item in enumerate(arr):
                        if isinstance(item, str):
                            new, n = _strip_orphans_from_text(item)
                            if n > 0:
                                arr[i] = new
                                count += n

    if count == 0:
        return None, 0
    new_text = json.dumps(data, ensure_ascii=False, indent=2) + ("\n" if text.endswith("\n") else "")
    return new_text, count


def _print_finding(path: Path, before: str, match: str, after: str, risky: bool) -> None:
    label = str(path.relative_to(REPO))
    tag = " [RISKY: contains quote — will NOT auto-strip]" if risky else ""
    print(f"[{label}]{tag}")
    print(f"  before: ...{before!r}")
    print(f"  match : {match!r}")
    print(f"  after : {after!r}...")
    print()


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--detect-only", action="store_true", help="Print matches with context; no edits.")
    mode.add_argument("--dry-run", action="store_true", help="Print matches and would-strip counts; no edits.")
    ap.add_argument("--limit", type=int, help="Stop after N files (for testing)")
    args = ap.parse_args()

    targets = collect_scam_targets(
        city_pages=True,
        country_hubs=True,
        master_hub=True,
        research_json=True,
        api_json=True,
    )
    if args.limit:
        targets = targets[: args.limit]

    if args.detect_only:
        all_findings: list[tuple[Path, str, str, str, bool]] = []
        for path in targets:
            if not path.exists():
                continue
            if path.suffix == ".html":
                findings = _scan_html(path)
            elif path.suffix == ".json" and "research" in path.parts:
                findings = _scan_research_json(path)
            else:
                continue
            for f in findings:
                all_findings.append((path,) + f)
        # Print first 10 as sanity check
        print("=== FIRST 10 EXAMPLES ===\n")
        for path, before, match, after, risky in all_findings[:10]:
            _print_finding(path, before, match, after, risky)
        files_with = len({p for p, *_ in all_findings})
        risky_count = sum(1 for *_, r in all_findings if r)
        safe_count = len(all_findings) - risky_count
        print(f"=== TOTAL: {len(all_findings)} orphan candidates across {files_with} files ===")
        print(f"=== {safe_count} safe (will auto-strip) + {risky_count} risky (human review only) ===")
        return

    total_stripped = 0
    files_changed = 0
    for path in targets:
        if not path.exists():
            continue
        if path.suffix == ".html":
            original = path.read_text()
            fixed, n = _strip_html_file(original)
            if n > 0 and fixed != original:
                files_changed += 1
                total_stripped += n
                label = str(path.relative_to(REPO))
                print(f"  {label:60} — {n} orphans stripped")
                if args.dry_run:
                    # Show first 3 non-risky findings for this file
                    safe = [f for f in _scan_html(path) if not f[3]]
                    for before, match, after, _risky in safe[:3]:
                        print(f"      match: {match!r}")
                else:
                    path.write_text(fixed)
        elif path.suffix == ".json" and "research" in path.parts:
            fixed, n = _strip_research_json(path)
            if fixed is not None and n > 0:
                files_changed += 1
                total_stripped += n
                label = str(path.relative_to(REPO))
                print(f"  {label:60} — {n} orphans stripped")
                if args.dry_run:
                    safe = [f for f in _scan_research_json(path) if not f[3]]
                    for before, match, after, _risky in safe[:3]:
                        print(f"      match: {match!r}")
                else:
                    path.write_text(fixed)

    action = "would strip" if args.dry_run else "stripped"
    print(f"\n{action} {total_stripped} orphans across {files_changed} files")


if __name__ == "__main__":
    main()
