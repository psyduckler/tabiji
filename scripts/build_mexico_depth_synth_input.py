#!/usr/bin/env python3
"""Build /tmp/mexico-depth-synth-input.json — input for synth subagent.

For each under-depth scam card (depth=2), capture:
  - city, n
  - title, location
  - tldr
  - existing 2 body paragraphs (as plain text)
  - red_flags (5 bullets — gives mechanic vocabulary)
  - how_to_avoid (5 bullets — same)

Subagent will read this file and output one new body paragraph per card
that fits the NYC narrative style (3rd para typically ends with bold CTA).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

UNDER_DEPTH = [
    ("cabo-san-lucas", 1),
    ("cabo-san-lucas", 3),
    ("cabo-san-lucas", 5),
    ("cozumel", 1),
    ("cozumel", 3),
    ("guanajuato", 1),
    ("guanajuato", 5),
    ("holbox", 1),
    ("holbox", 2),
    ("holbox", 4),
    ("holbox", 5),
    ("isla-mujeres", 1),
    ("isla-mujeres", 2),
    ("isla-mujeres", 3),
    ("isla-mujeres", 4),
    ("mazatlan", 5),
    ("san-cristobal-de-las-casas", 4),
    ("san-miguel-de-allende", 1),
    ("san-miguel-de-allende", 4),
    ("san-miguel-de-allende", 6),
]

CARD_RE = re.compile(
    r'<div class="scam-card"[^>]*id="scam-(\d+)"[^>]*>(.*?)(?=<div class="scam-card"|<div class="mid-cta"|<!-- What to do)',
    re.DOTALL,
)


def text_only(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def extract_card(city: str, target_n: int) -> dict | None:
    h = (REPO / f"scams/{city}/index.html").read_text()
    for n_str, body in CARD_RE.findall(h):
        if int(n_str) != target_n:
            continue
        title = text_only(re.search(r'<div class="scam-title">([^<]+)</div>', body).group(1))
        loc_m = re.search(r'<div class="scam-location">([^<]+)</div>', body)
        location = text_only(loc_m.group(1)) if loc_m else ""
        tldr_m = re.search(r'<p class="scam-tldr">(.*?)</p>', body, re.DOTALL)
        tldr = text_only(tldr_m.group(1)) if tldr_m else ""
        bodies = [
            text_only(m.group(1))
            for m in re.finditer(r'<p class="scam-story-body">(.*?)</p>', body, re.DOTALL)
        ]
        red = re.search(r'red-flags">.*?<ul>(.*?)</ul>', body, re.DOTALL)
        avoid = re.search(r'avoid">.*?<ul>(.*?)</ul>', body, re.DOTALL)
        red_bullets = [text_only(li) for li in re.findall(r'<li>(.*?)</li>', red.group(1) if red else '', re.DOTALL)]
        avoid_bullets = [text_only(li) for li in re.findall(r'<li>(.*?)</li>', avoid.group(1) if avoid else '', re.DOTALL)]
        return {
            "city": city,
            "n": target_n,
            "title": title,
            "location": location,
            "tldr": tldr,
            "existing_body_paragraphs": bodies,
            "red_flags": red_bullets,
            "how_to_avoid": avoid_bullets,
        }
    return None


def main():
    cards = []
    for city, n in UNDER_DEPTH:
        card = extract_card(city, n)
        if card is None:
            print(f"  WARN: missing {city}/scam-{n}")
            continue
        cards.append(card)
    out = Path("/tmp/mexico-depth-synth-input.json")
    out.write_text(json.dumps(cards, indent=2, ensure_ascii=False))
    print(f"  Wrote {len(cards)} cards to {out}")
    print(f"  Total existing body paragraphs: "
          f"{sum(len(c['existing_body_paragraphs']) for c in cards)}")
    print(f"  Each will get +1 = {len(cards)} new paragraphs to generate.")


if __name__ == "__main__":
    main()
