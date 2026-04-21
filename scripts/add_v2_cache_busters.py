#!/usr/bin/env python3
"""Add ?v=2 cache busters to US city scam comics that were just uploaded.

Reads the list of uploaded comics from tmp/*-new.jpg, then updates the
corresponding HTML pages to add ?v=2 to the matching img src attributes.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TMP = REPO / "tmp"
SCAMS = REPO / "scams"


def parse_filename(name: str) -> tuple[str, int] | None:
    m = re.match(r"^(.+)-scam-?(\d+)-new\.jpg$", name)
    if not m:
        return None
    city = m.group(1)
    scam_n = int(m.group(2))
    if city == "vegas":
        city = "las-vegas"
    elif city == "la":
        city = "los-angeles"
    return city, scam_n


def main():
    files = list(TMP.glob("*-new.jpg"))

    # Group by city
    city_scams: dict[str, list[int]] = {}
    for f in files:
        parsed = parse_filename(f.name)
        if not parsed:
            continue
        city, scam_n = parsed
        city_scams.setdefault(city, []).append(scam_n)

    print(f"Processing {len(city_scams)} cities")

    total_updates = 0
    for city, scam_nums in sorted(city_scams.items()):
        html_path = SCAMS / city / "index.html"
        if not html_path.exists():
            print(f"⚠ {city}: index.html not found")
            continue

        content = html_path.read_text()
        original = content
        updates = 0

        for scam_n in scam_nums:
            # Match: src="https://img.tabiji.ai/scams/{city}/scam-{N}.jpg" (without ?v=)
            pattern = rf'(src="https://img\.tabiji\.ai/scams/{re.escape(city)}/scam-{scam_n}\.jpg)(")'
            replacement = rf'\1?v=2\2'

            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                updates += count

        if content != original:
            html_path.write_text(content)
            print(f"✓ {city}: {updates} comics updated")
            total_updates += updates
        else:
            # Check if already has ?v=2
            already_v2 = sum(1 for n in scam_nums
                           if f"scam-{n}.jpg?v=2" in original or f"scam-{n}.jpg?v=" in original)
            if already_v2:
                print(f"  {city}: {already_v2} already have ?v=2")
            else:
                print(f"  {city}: no matches found for scams {scam_nums}")

    print(f"\nTotal: {total_updates} comic URLs updated with ?v=2")


if __name__ == "__main__":
    main()
