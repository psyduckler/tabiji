#!/usr/bin/env python3
"""Targeted regen for the 3 still-broken Australia scam comics surfaced in the
2026-04-28 book-readiness audit.

After the 2026-04-27 regen pass, three issues persisted:
- whitsundays-4: panel 1 background still shows Sydney Opera House + Harbour
  Bridge despite the Whitsundays/Airlie Beach setting (WRONG-CITY)
- darwin-5: stray "AUSTRALIA — LAND OF SUNSHINE" travel-poster banner top + bottom
  with kangaroo/bird leaf border (BANNER + decorative-frame regression)
- melbourne-2: stray "MELBOURNE AIRPORT — SIXT" header + "MELBOURNE CAR RENTAL —
  BE PREPARED, AVOID SCAMS!" footer banner with kangaroo/bird leaf border
  (BANNER + decorative-frame regression)

Per the 2026-04-27 session learning: Wavespeed is more reliable at avoidance
than at producing specific landmarks, so we inject explicit "BACKDROP REQUIREMENT"
text into the scam's location field before calling synthesize_prompt.

Usage:
    python3 scripts/comic-pipeline/regen_australia_book_audit_2026_04_28.py --force
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

COUNTRY = "australia"

TARGETS: dict[str, list[int]] = {
    "whitsundays": [4],
    "darwin":      [5],
    "melbourne":   [2],
}

# Inject explicit BACKDROP REQUIREMENT into the scam's location to constrain
# the Gemini prompt synthesis against the previously-observed regressions.
LOCATION_SUFFIX: dict[tuple[str, int], str] = {
    ("whitsundays", 4): (
        " — BACKDROP REQUIREMENT: this scene is set in Airlie Beach / Whitsundays. "
        "STRICTLY NO Sydney Opera House, NO Sydney Harbour Bridge, NO Sydney landmarks "
        "anywhere in any panel. Background must be Coral Sea, palm trees, marina with "
        "yachts, Whitsunday Sailing Club signage, or Airlie Beach lagoon — never Sydney."
    ),
    ("darwin", 5): (
        " — BACKDROP REQUIREMENT: NO decorative travel-poster top or bottom banners. "
        "NO 'AUSTRALIA — LAND OF SUNSHINE' or any framing slogan. NO kangaroo or bird "
        "border art. NO leaf-vine ornamental border. The image is four plain comic "
        "panels in a 2×2 grid with NO surrounding frame, NO header, NO footer text."
    ),
    ("melbourne", 2): (
        " — BACKDROP REQUIREMENT: NO decorative travel-poster top or bottom banners. "
        "NO 'MELBOURNE AIRPORT — SIXT' header. NO 'MELBOURNE CAR RENTAL — BE PREPARED, "
        "AVOID SCAMS!' footer. NO kangaroo, bird, or leaf-vine ornamental border. "
        "The image is four plain comic panels in a 2×2 grid with NO surrounding frame, "
        "NO header, NO footer text."
    ),
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--batch-size", type=int, default=3)
    p.add_argument("--force", action="store_true",
                   help="re-generate even if local /tmp cache exists")
    args = p.parse_args()

    out_dir = Path(f"/tmp/{COUNTRY}-comics-v3")
    out_dir.mkdir(parents=True, exist_ok=True)
    audit_log = Path(f"/tmp/{COUNTRY}-audit-v3.jsonl")
    audit_log.write_text("")
    flagged_log = Path(f"/tmp/{COUNTRY}-flagged-v3.log")
    flagged_log.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    targeted = []
    total_expected = sum(len(v) for v in TARGETS.values())
    for city, wanted in TARGETS.items():
        city_scams = {s["n"]: s for s in extract_scams(city)}
        for n in wanted:
            if n not in city_scams:
                print(f"WARN {city}/scam-{n}: not found in index.html", flush=True)
                continue
            scam = city_scams[n]
            suffix = LOCATION_SUFFIX.get((city, n), "")
            if suffix:
                scam["location"] = scam["location"] + suffix
            targeted.append(scam)

    print(f"[{COUNTRY}] targeted {len(targeted)}/{total_expected} scams "
          f"across {len(TARGETS)} cities (batch size {args.batch_size})", flush=True)

    ok = retried = flagged = 0
    for i in range(0, len(targeted), args.batch_size):
        batch = targeted[i:i + args.batch_size]
        print(f"\n=== batch {i // args.batch_size + 1} ({len(batch)} items) ===", flush=True)
        with ThreadPoolExecutor(max_workers=args.batch_size) as ex:
            futures = [ex.submit(generate_one, COUNTRY, s, out_dir, ws_token, r2_token, args.force)
                       for s in batch]
            for s, f in zip(batch, futures):
                res = f.result()
                label = f"{s['city']}/scam-{s['n']}"
                line = f"{label}: {res['status']} char={res['character']} ({res['note']})"
                print(f"  {line}", flush=True)
                audit_log.open("a").write(json.dumps({
                    "city": s["city"], "n": s["n"], "title": s["title"], **res,
                }) + "\n")
                if res["status"] in ("ok", "ok-cached"):
                    ok += 1
                elif res["status"] == "ok-retried":
                    retried += 1
                    ok += 1
                else:
                    flagged += 1
                    flagged_log.open("a").write(line + "\n")

    summary = {
        "country": COUNTRY, "total": len(targeted),
        "ok": ok, "retried": retried, "flagged": flagged,
        "audit_log": str(audit_log), "flagged_log": str(flagged_log),
    }
    print(f"\n[{COUNTRY}] FINAL: {json.dumps(summary)}", flush=True)
    return 0 if flagged == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
