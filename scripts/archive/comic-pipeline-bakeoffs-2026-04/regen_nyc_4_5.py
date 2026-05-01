#!/usr/bin/env python3
"""Regenerate NYC scams 4 (character photo shake-down) and 5 (subway swipe).

Existing comics for these two depict a generic "got a minute, boss" street
handout — visually identical to scam 1 (CD hustle) and not matching the actual
scam mechanics on the page. This script runs only those two through the v2
pipeline (Gemini synthesis + Nano Banana Pro edit) without touching the other
four NYC comics.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

TARGETS = (4, 5)
COUNTRY = "united-states"
CITY = "new-york-city"
OUT_DIR = Path("/tmp/usa-comics-v2")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    scams = [s for s in extract_scams(CITY) if s["n"] in TARGETS]
    if len(scams) != len(TARGETS):
        sys.exit(f"expected {len(TARGETS)} scams, found {len(scams)}")

    for scam in scams:
        print(f"\n→ regenerating {scam['city']}/scam-{scam['n']}: {scam['title']}")
        print(f"  location: {scam['location']}")
        print(f"  story: {scam['story'][:200]}...")
        res = generate_one(COUNTRY, scam, OUT_DIR, ws_token, r2_token, force=True)
        print(f"  result: {res['status']}  character={res['character']}  ({res['note']})")
        if res.get("prompt"):
            print(f"  prompt[:300]: {res['prompt']}")


if __name__ == "__main__":
    main()
