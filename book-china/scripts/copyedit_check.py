#!/usr/bin/env python3
"""5-pass copyedit diagnostic for book-china manuscript."""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANUSCRIPT = HERE.parent / "manuscript"

AI_ISMS = [
    "delve", "delving", "navigating the landscape", "in today's world",
    "it's important to note", "in the realm of", "embark on", "unveil",
    "plethora", "tapestry", "myriad", "kaleidoscope", "in essence",
    "moreover", "furthermore", "ultimately", "in conclusion",
    "seamless", "bustling", "nestled", "enchanting", "vibrant",
    "culturally rich", "hidden gem", "treasure trove",
]
BR_TO_US = {
    "realise": "realize", "realised": "realized", "realising": "realizing",
    "organise": "organize", "organised": "organized", "organisation": "organization",
    "colour": "color", "favour": "favor", "neighbour": "neighbor",
    "behaviour": "behavior", "defence": "defense", "centre": "center",
    "metre": "meter", "travelling": "traveling", "cancelled": "canceled",
    "whilst": "while", "amongst": "among", "towards": "toward", "learnt": "learned",
}

# Words where -our endings are valid in American English (do not flag)
US_OUR_OK = {"hour", "hourly", "tour", "tourist", "your", "yours", "yourself",
             "four", "fourth", "labour-", "armour-", "sour", "pour", "flour"}

findings: list[tuple[str, int, str, str]] = []  # (file, line, pass, msg)


def add(p: Path, lineno: int, pass_name: str, msg: str):
    findings.append((p.name, lineno, pass_name, msg))


def check_typography(p: Path, text: str):
    for i, line in enumerate(text.splitlines(), 1):
        if "  " in line and not line.startswith("  ") and not line.startswith("|"):
            # Allow markdown table column padding; flag mid-prose double-spaces
            stripped = line.strip()
            if stripped and not stripped.startswith("|"):
                if re.search(r"[^\s]  [^\s]", line):
                    add(p, i, "typography", "double-space in prose")
        if "\t" in line:
            add(p, i, "typography", "tab character (use spaces)")
        if "--" in line and not re.search(r"^\s*<!--|-->\s*$", line):
            # Flag --, but not HTML comments
            for m in re.finditer(r"--", line):
                # Allow --pdf-engine= etc. inside code spans
                pre = line[:m.start()]
                if pre.count("`") % 2 == 1:
                    continue
                add(p, i, "typography", f"-- (use em-dash —): ...{line[max(0,m.start()-20):m.end()+20]}...")
                break
        # Bare hyphen between digits (need en-dash for ranges)
        for m in re.finditer(r"(\d)-(\d)", line):
            pre = line[:m.start()]
            if pre.count("`") % 2 == 1:
                continue
            # Allow N-N inside URLs / IDs
            ctx = line[max(0,m.start()-3):m.end()+3]
            if re.search(r"[a-zA-Z]/[\d-]|[\d]/[\d]|@|http", ctx):
                continue
            # Allow phone-number hyphenation (e.g. +86 21 8011-2400)
            if re.search(r"\+\d{1,3}\s|\b\d{4,}-\d{3,}\b", line):
                continue
            # Allow date ranges like 2024-2025 (should they be en-dashed? typically yes but accept)
            if re.search(r"\b(19|20)\d{2}-(19|20)\d{2}\b", line):
                continue
            add(p, i, "typography", f"hyphen between digits (consider en-dash): ...{ctx}...")
            break


def check_aiisms(p: Path, text: str):
    for i, line in enumerate(text.splitlines(), 1):
        for term in AI_ISMS:
            if re.search(rf"\b{re.escape(term)}\b", line, re.IGNORECASE):
                add(p, i, "ai-isms", f"'{term}' present")


def check_british(p: Path, text: str):
    for i, line in enumerate(text.splitlines(), 1):
        for br, us in BR_TO_US.items():
            if re.search(rf"\b{re.escape(br)}\b", line, re.IGNORECASE):
                add(p, i, "british", f"'{br}' → '{us}'")
        # Generic -our ending words that are British (color/colour, etc.) are mostly covered
        # by the explicit map. Only flag 'organis' stem and 'behaviour' stem.
        # (The map is exhaustive enough for our manuscript.)


def check_terminology(p: Path, text: str):
    # Place-name spellings to verify
    if "Beijing" in text or "Shanghai" in text:
        # Check Türkiye spelling consistency (CTA mentions it)
        if "Turkey" in text and "Türkiye" in text:
            add(p, 0, "terminology", "both 'Turkey' and 'Türkiye' used — check consistency")
    # Italics convention: foreign-language terms should be italicized on first mention
    # We rely on visual inspection; this script just notes presence
    # No flag generated — informational only


def check_structural(p: Path, text: str):
    lines = text.splitlines()
    name = p.name
    if not lines:
        add(p, 0, "structural", "empty file")
        return
    if name.startswith("cities-") and name.endswith("-intro.md"):
        # City intros should NOT have a top-level # heading
        for i, line in enumerate(lines, 1):
            if re.match(r"^#\s+[^#]", line):
                add(p, i, "structural", "city intro should not have its own # heading (build.py adds it)")
                break
    elif re.match(r"^\d{2}-", name) or name in ("95-about.md", "99-cta.md"):
        # Front/back matter must have a top-level # heading
        has_h1 = any(re.match(r"^#\s+[^#]", l) for l in lines)
        if not has_h1:
            add(p, 0, "structural", "missing top-level # heading")
        # Front/back-matter should use {-}
        if name not in ("04-cities-section.md",):
            unmarked = []
            for i, line in enumerate(lines, 1):
                m = re.match(r"^#+\s+(.+?)$", line)
                if m and "{-}" not in line and "<!--" not in line:
                    unmarked.append((i, line.strip()))
            if unmarked and name in ("01-copyright.md", "02-introduction.md", "03-red-flag-patterns.md",
                                      "90-appendix-phrase-card.md", "91-appendix-recovery.md",
                                      "92-appendix-contacts.md", "95-about.md", "99-cta.md"):
                # Sub-headings (## and below) inside front/back-matter don't need {-}
                # Only the H1 needs {-}
                top = [(i, l) for i, l in unmarked if re.match(r"^#\s", l)]
                if top:
                    for i, line in top:
                        add(p, i, "structural", f"front/back-matter H1 missing {{-}}: {line}")
    if name == "04-cities-section.md":
        if "<!-- CITIES -->" not in text:
            add(p, 0, "structural", "missing <!-- CITIES --> marker")


def main():
    files = sorted(MANUSCRIPT.glob("*.md"))
    print(f"Scanning {len(files)} manuscript files...\n")
    for p in files:
        text = p.read_text(encoding="utf-8")
        check_typography(p, text)
        check_aiisms(p, text)
        check_british(p, text)
        check_terminology(p, text)
        check_structural(p, text)

    by_pass: dict[str, list[tuple[str, int, str]]] = {}
    for fname, lineno, pass_name, msg in findings:
        by_pass.setdefault(pass_name, []).append((fname, lineno, msg))

    for pass_name in ["structural", "typography", "ai-isms", "british", "terminology"]:
        rows = by_pass.get(pass_name, [])
        print(f"=== Pass: {pass_name} ({len(rows)} findings) ===")
        for fname, lineno, msg in rows:
            print(f"  {fname}:{lineno}: {msg}")
        print()
    print(f"TOTAL findings: {len(findings)}")


if __name__ == "__main__":
    main()
