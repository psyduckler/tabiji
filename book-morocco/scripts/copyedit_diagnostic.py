#!/usr/bin/env python3
"""
5-pass copyedit diagnostic for book-morocco manuscript.

Pass 1 — Typography (double hyphens, triple dots, double spaces, tabs, hyphen ranges)
Pass 2 — AI-isms + content padding
Pass 3 — British → American English
Pass 4 — Country-specific terminology (Morocco diacritics + italics)
Pass 5 — Structural (heading conventions, CITIES marker, file naming)

Run from repo root:
    python3 book-morocco/scripts/copyedit_diagnostic.py
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
MANU = BOOK / "manuscript"


def find_in_files(pattern, label, files=None, flags=0):
    files = files or sorted(MANU.glob("*.md"))
    hits = []
    rx = re.compile(pattern, flags)
    for f in files:
        text = f.read_text()
        for m in rx.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            line = text.splitlines()[line_no - 1]
            hits.append((f.name, line_no, m.group(0), line.strip()[:120]))
    return label, hits


def main():
    findings = []

    # PASS 1 — Typography
    findings.append(find_in_files(r"\w--\w", "P1: double-hyphen inside word"))
    findings.append(find_in_files(r"\.\.\.[^\.]", "P1: triple dots"))
    # Double spaces only in prose (skip tables, allow trailing spaces for hard breaks)
    findings.append(find_in_files(r"(?<![\n|])  +(?![\n*\-])", "P1: double-space in prose"))
    findings.append(find_in_files(r"\t", "P1: tab character"))
    # Hyphens in numeric currency ranges (these get fixed at build time but flag for review)
    findings.append(find_in_files(
        r"\b\d[\d,.]*-\d[\d,.]*\s*(?:MAD|DH|dirhams?|euro|euros|€|\$|MAD|USD)",
        "P1: hyphen in currency range (build.py normalizes — informational)"
    ))

    # PASS 2 — AI-isms + content padding
    AI_ISMS = [
        "delve", "delving", "navigating the landscape", "in today's world",
        "it's important to note", "in the realm of", "embark on", "unveil",
        "plethora", "tapestry", "myriad", "kaleidoscope", "in essence",
        "moreover", "furthermore", "ultimately", "in conclusion",
        "seamless", "bustling", "nestled", "enchanting", "vibrant",
        "culturally rich", "hidden gem",
    ]
    for ai in AI_ISMS:
        findings.append(find_in_files(rf"\b{re.escape(ai)}\b", f"P2: AI-ism '{ai}'", flags=re.IGNORECASE))

    # PASS 3 — British → American English
    BRIT_AM = [
        ("realise", "realize"),
        ("organis", "organiz"),
        ("colour", "color"),
        ("favour", "favor"),
        ("neighbour", "neighbor"),
        ("behaviour", "behavior"),
        ("defence", "defense"),
        ("centre", "center"),
        ("metre", "meter"),
        ("travelling", "traveling"),
        ("cancelled", "canceled"),
        ("whilst", "while"),
        ("amongst", "among"),
        ("towards", "toward"),
        ("learnt", "learned"),
    ]
    for brit, am in BRIT_AM:
        findings.append(find_in_files(rf"\b{brit}\w*", f"P3: British '{brit}' → American '{am}'", flags=re.IGNORECASE))

    # PASS 4 — Morocco-specific terminology
    # Place-name forms preferred in this book: Marrakech (not Marrakesh), Fez (not Fès in body), Tangier (not Tanger)
    findings.append(find_in_files(r"\bMarrakesh\b", "P4: 'Marrakesh' — book uses 'Marrakech'"))
    findings.append(find_in_files(r"\bFès\b", "P4: 'Fès' — book uses 'Fez'"))
    findings.append(find_in_files(r"\bTanger\b", "P4: 'Tanger' — book uses 'Tangier'"))
    # Currency abbreviations
    findings.append(find_in_files(r"\bMAD\b", "P4: 'MAD' usage (informational — confirm context)"))

    # PASS 5 — Structural
    structural_issues = []
    # Numbered front/back-matter must start with `#` heading
    for f in sorted(MANU.glob("[0-9][0-9]-*.md")):
        first = f.read_text().lstrip().splitlines()[0] if f.read_text().strip() else ""
        if not first.startswith("# "):
            structural_issues.append((f.name, 1, "no leading H1", first[:80]))
        # Front/back-matter must use `{-}` for unnumbered chapters
        if not first.endswith("{-}"):
            structural_issues.append((f.name, 1, "front/back-matter H1 missing {-}", first[:80]))
    # 04-cities-section.md must have <!-- CITIES --> marker
    cs = (MANU / "04-cities-section.md")
    if cs.exists() and "<!-- CITIES -->" not in cs.read_text():
        structural_issues.append((cs.name, 0, "missing <!-- CITIES --> marker", ""))
    # cities-*-intro.md must NOT start with H1
    for f in sorted(MANU.glob("cities-*-intro.md")):
        first = f.read_text().lstrip().splitlines()[0] if f.read_text().strip() else ""
        if first.startswith("#"):
            structural_issues.append((f.name, 1, "city intro must NOT start with H1", first[:80]))
    findings.append(("P5: structural", structural_issues))

    # Report
    total_hits = 0
    for label, hits in findings:
        if hits:
            print(f"\n=== {label} ({len(hits)} hits) ===")
            for h in hits[:10]:
                fname, ln, match, ctx = h
                print(f"  {fname}:{ln}  '{match}'   {ctx!r}")
            if len(hits) > 10:
                print(f"  ... and {len(hits) - 10} more")
            total_hits += len(hits)

    print(f"\n=== SUMMARY ===")
    print(f"Total findings across 5 passes: {total_hits}")


if __name__ == "__main__":
    main()
