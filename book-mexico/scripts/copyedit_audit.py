#!/usr/bin/env python3
"""5-pass copyedit audit for Mexico book manuscript."""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
MS = BOOK / "manuscript"

# Pass 1 — Typography
P1_PATTERNS = [
    ("double-hyphen-in-words", re.compile(r"\w--\w")),
    ("triple-dots", re.compile(r"[^\.]\.\.\.[^\.]")),
    ("double-space-in-prose", re.compile(r"(?<=[a-z])  (?=[A-Za-z])")),
    ("tab-character", re.compile(r"\t")),
    # Bare hyphens between numbers immediately followed by currency symbols/words
    ("hyphen-in-currency-range", re.compile(r"\b\d[\d,.]*-\d[\d,.]*\s*(?:MX\$|US\$|\$|MXN|USD|pesos|peso|dollars|dollar)")),
    # Bare hyphens between two USD/MX$ amounts (should be en-dash)
    ("hyphen-between-currency", re.compile(r"(?:MX\$|US\$|\$)\d[\d,.]*-\$?\d[\d,.]*")),
]

# Pass 2 — AI-isms
P2_TERMS = [
    "delve", "delving", "navigating the landscape", "in today's world",
    "it's important to note", "in the realm of", "embark on", "unveil",
    "plethora", "tapestry", "myriad", "kaleidoscope", "in essence",
    "moreover", "furthermore", "ultimately", "in conclusion",
    "seamless", "bustling", "nestled", "enchanting", "vibrant",
    "culturally rich", "hidden gem",
]

# Pass 3 — British → American English
P3_PAIRS = [
    ("realise", "realize"), ("organis", "organiz"),
    ("colour", "color"), ("favour", "favor"),
    ("neighbour", "neighbor"), ("behaviour", "behavior"),
    ("defence", "defense"),
    ("metre", "meter"),
    ("travelling", "traveling"), ("travelled", "traveled"),
    ("cancelled", "canceled"), ("cancelling", "canceling"),
    ("whilst", "while"), ("amongst", "among"),
    ("towards", "toward"), ("learnt", "learned"),
    ("stylised", "stylized"),  # we use "stylized" in alts elsewhere
]
# NOTE: "centre" left out because Centro Histórico contains "ntr" but never "centre"; check manually if needed.

# Pass 4 — Mexico-specific
P4_RULES = [
    # Place names that need accents
    (re.compile(r"\bMerida\b"), "Mérida"),
    (re.compile(r"\bCancun\b(?!-)"), "Cancún"),
    (re.compile(r"\bYucatan\b"), "Yucatán"),
    (re.compile(r"\bMexico\s+city\b"), "Mexico City"),
    (re.compile(r"\bMazatlan\b(?!-)"), "Mazatlán"),
    (re.compile(r"\bSan\s+Cristobal\b"), "San Cristóbal"),
    (re.compile(r"\bZocalo\b"), "Zócalo"),
    (re.compile(r"\bTeotihuacan\b"), "Teotihuacán"),
    (re.compile(r"\bPopocatepetl\b"), "Popocatépetl"),
    (re.compile(r"\bJuarez\b"), "Juárez"),
    (re.compile(r"\bChichen\s+Itza\b"), "Chichén Itzá"),
    # Currency consistency
    (re.compile(r"\bMX\s+\$"), "MX$ (with stray space)"),
]

# Pass 5 — structural
def pass5_check(path: Path, content: str) -> list[str]:
    issues = []
    name = path.name
    is_numbered = re.match(r"\d{2}-", name)
    is_city_intro = name.startswith("cities-")
    is_back_matter = name.startswith(("90-", "91-", "92-", "95-", "99-"))
    is_front_matter = name.startswith(("01-", "02-", "03-", "04-"))

    first = content.lstrip().split("\n", 1)[0] if content.strip() else ""

    if is_numbered:
        if not first.startswith("# "):
            issues.append(f"missing top-level # heading in {name}")
        # Front/back-matter must use {-} on the H1
        if (is_front_matter or is_back_matter) and "{-}" not in first:
            issues.append(f"missing {{-}} on H1 in {name}")
    if is_city_intro and first.startswith("# "):
        issues.append(f"city intro should NOT have a top-level # (build.py adds it): {name}")
    if name == "04-cities-section.md" and "<!-- CITIES -->" not in content:
        issues.append(f"04-cities-section.md missing <!-- CITIES --> marker")
    return issues


def run() -> None:
    files = sorted(MS.glob("*.md"))
    print(f"Auditing {len(files)} manuscript files...\n")

    p1_total = 0
    print("=== PASS 1 — Typography ===")
    for f in files:
        text = f.read_text()
        for label, pat in P1_PATTERNS:
            for m in pat.finditer(text):
                line = text[:m.start()].count("\n") + 1
                snippet = text[max(0, m.start()-30):m.end()+30].replace("\n", " ")
                print(f"  {f.name}:{line}  [{label}]  ...{snippet}...")
                p1_total += 1
    print(f"  Pass 1 hits: {p1_total}\n")

    p2_total = 0
    print("=== PASS 2 — AI-isms + content padding ===")
    for f in files:
        text = f.read_text().lower()
        for term in P2_TERMS:
            for m in re.finditer(rf"\b{re.escape(term)}\b", text):
                line = text[:m.start()].count("\n") + 1
                snippet = text[max(0, m.start()-30):m.end()+30].replace("\n", " ")
                print(f"  {f.name}:{line}  [{term!r}]  ...{snippet}...")
                p2_total += 1
    print(f"  Pass 2 hits: {p2_total}\n")

    p3_total = 0
    print("=== PASS 3 — British → American English ===")
    for f in files:
        text = f.read_text()
        for br, am in P3_PAIRS:
            for m in re.finditer(rf"\b{re.escape(br)}\w*", text):
                line = text[:m.start()].count("\n") + 1
                w = m.group(0)
                print(f"  {f.name}:{line}  '{w}' → '{w.replace(br, am, 1)}'")
                p3_total += 1
    print(f"  Pass 3 hits: {p3_total}\n")

    p4_total = 0
    print("=== PASS 4 — Mexico-specific ===")
    for f in files:
        text = f.read_text()
        for pat, fix in P4_RULES:
            for m in pat.finditer(text):
                # Skip obvious slug references (lowercase) and dictionary keys
                line = text[:m.start()].count("\n") + 1
                snippet = text[max(0, m.start()-40):m.end()+40].replace("\n", " ")
                print(f"  {f.name}:{line}  [{m.group(0)!r} → {fix!r}]  ...{snippet}...")
                p4_total += 1
    print(f"  Pass 4 hits: {p4_total}\n")

    p5_total = 0
    print("=== PASS 5 — Structural ===")
    for f in files:
        for issue in pass5_check(f, f.read_text()):
            print(f"  {issue}")
            p5_total += 1
    print(f"  Pass 5 hits: {p5_total}\n")

    print(f"\n=== TOTAL: {p1_total + p2_total + p3_total + p4_total + p5_total} hits across 5 passes ===")


if __name__ == "__main__":
    run()
