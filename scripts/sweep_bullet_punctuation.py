#!/usr/bin/env python3
"""Punctuate bullet items in scam-page how-to-avoid / safety-tips lists.

Editorial lint rule 12 (bullet completeness) REJECTs any `<li>` in an
avoidance / recovery / safety / takeaways block that does not end in
`.`, `!`, or `?`. 402 violations observed across the shipped corpus.

This script:
  1. Parses each HTML page with BeautifulSoup and finds every `<li>` whose
     ancestor has one of these classes: `avoid`, `how-to-avoid`,
     `recovery-steps`, `safety-tips`, `safety-box`, `takeaways-box`.
  2. For each target `<li>`, checks `get_text()` after stripping trailing
     whitespace and one trailing quote (`'`, `\u2019`, `"`, `\u201d`).
  3. If the final visible character isn't in `.!?`, performs a surgical
     source-text splice to append `.` — preserving the original file's
     indentation, inline HTML (<strong>/<a>/etc.), and trailing whitespace.
  4. For research JSON (scams/research/*.json), applies the same rule to
     string entries in each scam's `how_to_avoid` array.

Navigation lists, TOCs, related-cities, and hub card grids are left alone —
those `<li>`s aren't descendants of any target class.

API v1 scam JSON uses `avoidance: string` (run-on prose, not a bullet list),
so is not touched by this script.

Usage:
    python3 scripts/sweep_bullet_punctuation.py --dry-run
    python3 scripts/sweep_bullet_punctuation.py
    python3 scripts/sweep_bullet_punctuation.py --dry-run --limit 5
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scam_sweep_common import collect_scam_targets

REPO = Path(__file__).resolve().parents[1]

# Classes whose <li> descendants are bullet-rule-bound
TARGET_CLASSES = {
    "avoid",
    "how-to-avoid",
    "recovery-steps",
    "safety-tips",
    "safety-box",
    "takeaways-box",
}

# Trailing characters we consider "closing-quote-like" when checking punctuation
_TRAILING_QUOTES = "'\"\u2019\u201d"
_WHITESPACE = " \t\n\r"


def _needs_period(text: str) -> bool:
    """True if `text` (a rendered <li> or bullet string) lacks trailing .!?"""
    # Strip trailing whitespace
    t = text.rstrip()
    # Strip one level of trailing quote + any whitespace inside it
    if t and t[-1] in _TRAILING_QUOTES:
        t = t[:-1].rstrip()
    if not t:
        return False
    return t[-1] not in ".!?"


def _punctuate_li_raw(raw: str) -> tuple[str, bool]:
    """Given a <li>...</li> source fragment, append `.` before </li> if the
    trailing visible char isn't .!?. Handles trailing whitespace + one
    closing quote. Idempotent. Returns (new_raw, changed)."""
    idx_close = raw.rfind("</li>")
    if idx_close < 0:
        return raw, False
    idx_open = raw.find("<li")
    if idx_open < 0:
        return raw, False
    idx_open_end = raw.find(">", idx_open) + 1
    interior = raw[idx_open_end:idx_close]
    if not interior.strip():
        return raw, False

    pos = len(interior)
    # Strip trailing whitespace
    while pos > 0 and interior[pos - 1] in _WHITESPACE:
        pos -= 1
    # Peel one trailing quote (the period goes INSIDE the quote, US style)
    if pos > 0 and interior[pos - 1] in _TRAILING_QUOTES:
        pos -= 1
        # Further strip whitespace inside the quote
        while pos > 0 and interior[pos - 1] in _WHITESPACE:
            pos -= 1
    if pos <= 0:
        return raw, False
    last = interior[pos - 1]
    if last in ".!?":
        return raw, False
    # If the content ends with a closing tag (e.g. "</strong>"), we'd need
    # to push the period INSIDE the tag. That case is rare here; skip to
    # avoid mangling. Lint will still flag these for manual review.
    if last == ">":
        return raw, False
    new_interior = interior[:pos] + "." + interior[pos:]
    return raw[:idx_open_end] + new_interior + raw[idx_close:], True


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def _fix_html(text: str) -> tuple[str, int]:
    """Parse, find target <li>s, splice periods into the source string.
    Returns (new_text, count)."""
    soup = BeautifulSoup(text, "html.parser")

    # Collect (sourceline, sourcepos, li) for every qualifying <li>
    targets: list[tuple[int, int]] = []
    for li in soup.find_all("li"):
        # Ancestor-class check
        has_target = False
        for anc in li.parents:
            cls = anc.get("class") or []
            if any(c in TARGET_CLASSES for c in cls):
                has_target = True
                break
        if not has_target:
            continue
        if not _needs_period(li.get_text()):
            continue
        if li.sourceline is None or li.sourcepos is None:
            continue
        targets.append((li.sourceline, li.sourcepos))

    if not targets:
        return text, 0

    line_starts = _line_starts(text)

    # Compute byte offsets of each target <li> start, then sort descending
    # so earlier edits don't shift later offsets.
    offsets: list[int] = []
    for line, col in targets:
        if 1 <= line <= len(line_starts):
            offsets.append(line_starts[line - 1] + col)
    offsets.sort(reverse=True)

    count = 0
    for start in offsets:
        close = text.find("</li>", start)
        if close < 0:
            continue
        raw = text[start : close + len("</li>")]
        new_raw, changed = _punctuate_li_raw(raw)
        if changed:
            text = text[:start] + new_raw + text[close + len("</li>") :]
            count += 1

    return text, count


def _fix_research_json(path: Path) -> tuple[str | None, int]:
    """Punctuate `how_to_avoid[]` entries in a research-batch JSON.
    Returns (new_text, count). Returns (None, 0) if file is not a research
    batch with the expected shape."""
    text = path.read_text()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None, 0
    if not isinstance(data, dict) or "cities" not in data:
        return None, 0

    count = 0
    for city in data.get("cities", []):
        for scam in (city or {}).get("scams", []) or []:
            avoid = scam.get("how_to_avoid")
            if not isinstance(avoid, list):
                continue
            for i, item in enumerate(avoid):
                if not isinstance(item, str):
                    continue
                if _needs_period(item):
                    # Append period to the visible content, preserving any
                    # trailing closing quote (period goes inside).
                    stripped = item.rstrip()
                    tail_ws = item[len(stripped) :]
                    if stripped and stripped[-1] in _TRAILING_QUOTES:
                        new_str = stripped[:-1].rstrip() + "." + stripped[-1] + tail_ws
                    else:
                        new_str = stripped + "." + tail_ws
                    avoid[i] = new_str
                    count += 1

    if count == 0:
        return None, 0
    # Re-serialize preserving ensure_ascii behaviour of the original
    # (these files contain Unicode; ensure_ascii=False keeps them readable).
    new_text = json.dumps(data, ensure_ascii=False, indent=2) + ("\n" if text.endswith("\n") else "")
    return new_text, count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
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

    total_fixed = 0
    files_changed = 0
    for path in targets:
        if not path.exists():
            continue
        if path.suffix == ".html":
            original = path.read_text()
            fixed, n = _fix_html(original)
            if n > 0 and fixed != original:
                files_changed += 1
                total_fixed += n
                label = str(path.relative_to(REPO))
                print(f"  {label:60} — {n} bullets punctuated")
                if not args.dry_run:
                    path.write_text(fixed)
        elif path.suffix == ".json":
            # Only research batches have how_to_avoid[] arrays
            if "research" not in path.parts:
                continue
            fixed, n = _fix_research_json(path)
            if fixed is not None and n > 0:
                files_changed += 1
                total_fixed += n
                label = str(path.relative_to(REPO))
                print(f"  {label:60} — {n} bullets punctuated")
                if not args.dry_run:
                    path.write_text(fixed)

    action = "would punctuate" if args.dry_run else "punctuated"
    print(f"\n{action} {total_fixed} bullets across {files_changed} files")


if __name__ == "__main__":
    main()
