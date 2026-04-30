#!/usr/bin/env python3
"""Generate the hero comic for one Scam Atlas page using comic pipeline v2 + default style.

Atlas pages live at /scams/atlas/<slug>/ and span 65+ countries by definition.
That makes country-specific styles (Hergé France, Studio Ghibli Japan, Feng Zikai
China, etc.) wrong for these pages — atlas comics use the locked _default warm
watercolor storybook style so they read as "tabiji travel comic" without invoking
any one country's aesthetic.

Pipeline (one comic per atlas entry):
  1. Read entries.json for the slug → pull name + primaryQueryTarget + subTypes
  2. Synthesize a generic-international 4-panel script via Gemini using
     synthesize.synthesize_prompt(country="_default", scam=...)
  3. Submit to Wavespeed /edit with the _default pilot as style anchor
  4. Poll until completed (≤ 600s)
  5. Download + verify (JPEG header + ≥ 120 KB)
  6. On verification failure, retry once via /text-to-image (more permissive filter)
  7. Upload to R2 at scams/atlas/<slug>/hero.jpg
  8. Print the public URL

Usage:
    python3 scripts/comic-pipeline/generate_atlas.py taxi-meter-manipulation
    python3 scripts/comic-pipeline/generate_atlas.py the-gold-ring-trick --force
    python3 scripts/comic-pipeline/generate_atlas.py atm-skimming --dry-run

Requires keychain entries:
    wavespeed-api-key       — Nano Banana Pro
    cloudflare-api-token    — R2-scoped token (PUT to tabiji-media bucket)
    gemini-api-key          — Gemini 2.5 Pro for scene synthesis

See:
    docs/comic-pipeline/styles/_default.md  — locked default style block + bake-off rationale
    docs/comic-pipeline/cast.md             — 4 canonical protagonists + scam-type pairing
    docs/comic-pipeline/prompt-synthesis.md — v2 pipeline overview
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from synthesize import synthesize_prompt  # noqa: E402
import generate as _g  # noqa: E402  reuse submit_nbp, poll_nbp, download_verify, upload_r2, _keychain

REPO = _HERE.parent.parent
ENTRIES_PATH = REPO / "generators" / "scam-atlas" / "data" / "entries.json"

R2_KEY_TEMPLATE = "scams/atlas/{slug}/hero.jpg"
PUBLIC_URL_TEMPLATE = "https://img.tabiji.ai/scams/atlas/{slug}/hero.jpg"


def load_entry(slug: str) -> dict:
    """Find the atlas entry in entries.json. Raises if absent."""
    doc = json.loads(ENTRIES_PATH.read_text())
    for e in doc["entries"]:
        if e.get("slug") == slug:
            return e
    raise SystemExit(f"❌ slug '{slug}' not found in {ENTRIES_PATH}")


def build_synthetic_scam(entry: dict) -> dict:
    """Convert an atlas entry into a 'scam' dict that synthesize_prompt() can consume.

    The synthesizer expects: city, title, location, story.
    For atlas (cross-country) pages, we synthesize:
      - city: "" (intentional — no country-specific landmarks in default style)
      - title: the entry name
      - location: a generic-international hint based on subTypes / parentEntry
      - story: a 2-3 sentence universal mechanic description
    """
    name = entry["name"]
    style = entry.get("entryStyle", "broad")
    subs = entry.get("subTypes", [])
    parent = entry.get("parentEntry", "")
    target = entry.get("primaryQueryTarget", "")

    # Scene location — generic-international per default style
    location_blurbs = {
        "taxi-meter-manipulation":     "tourist taxi rank, generic urban hotel curb, modest sedan, streetlight",
        "rideshare-fare-inflation":    "airport rideshare zone, generic-international airport curb, smartphone with app fare",
        "tuk-tuk-rickshaw-detour":     "tourist street with auto-rickshaw, market alley, generic Asian-city storefront",
        "airport-arrival-scams":       "generic-international airport arrivals hall, luggage trolley, taxi sign",
        "atm-skimming":                "generic urban ATM in tourist area, evening light, small huddle of people",
        "currency-exchange-cambio":    "tourist street pedestrian zone, currency exchange storefront, calculator",
        "counterfeit-currency-returns":"generic café cash register, banknote held to light, change in hands",
        "qr-code-quishing":            "parking meter or restaurant table with QR code, smartphone scanning",
        "restaurant-bill-padding":     "tourist-zone restaurant table with menu and bill, café terrace lighting",
        "tourist-trap-restaurants":    "tourist-zone restaurant with chalkboard menu, no posted prices",
        "pickpocketing-tactics":       "crowded generic tourist street, market pedestrians, tourist with bag",
        "distraction-theft-pickpocket-team": "generic tourist plaza, pedestrian flow, tourist with daypack",
        "fake-police-shakedown":       "generic urban sidewalk, two men in plain clothes, tourist holding wallet",
        "fake-tour-guide":             "generic tourist landmark exterior, freelance guide approaches with brochure",
        "airbnb-off-platform-fraud":   "smartphone showing booking app message, suitcase in hotel-style apartment lobby",
        "fake-skip-the-line-tickets":  "tourist landmark queue, ticket reseller with paper tickets",
        "fake-charity-petition":       "tourist plaza, person with clipboard approaching pedestrian",
        "gem-jewelry-shop-pressure":   "souvenir shop interior, gemstones on velvet display, tea set on table",
        "aggressive-street-vendor":    "generic tourist street market, vendor with souvenirs and bracelet",
        "fake-antique-souvenir-markup":"souvenir-shop counter with framed art and ceramics, price tag obscured",
        "drink-spiking-bar-bill-trap": "dim lounge bar interior, two cocktails on counter, hostess in shadow",
    }
    location = location_blurbs.get(
        entry["slug"],
        f"generic-international tourist street, anonymous urban backdrop, no country-specific landmarks (atlas comic — {name} runs across many countries)",
    )

    # Compose a universal-mechanic story for Gemini to dramatize
    if style == "broad" and subs:
        sub_list = ", ".join(s.replace("-", " ") for s in subs[:5])
        story = (
            f"{name} is a tourist-fraud family documented across many countries with multiple sub-variants: "
            f"{sub_list}. The universal mechanic is: scammer initiates contact (rather than the tourist), "
            f"locks in commitment before friction shows up, lets the route or pricing or product drift, "
            f"applies pressure at the destination or counter, and then evades the paper trail. "
            f"This atlas comic should illustrate the universal pattern using a generic-international "
            f"setting — no country-specific landmarks. Panel 4 should show the lesson: skip the scam "
            f"channel entirely and use a verified app, official counter, or licensed alternative."
        )
    else:
        story = (
            f"{name} is the tourist scam where {target}. The mechanic plays out in 4 stages: "
            f"setup (the approach), bait (the offer or distraction), pressure (the demand at the moment of commitment), "
            f"and aftermath (the lesson — what the tourist could have done instead). "
            f"This atlas comic should use a generic-international setting and end Panel 4 with the safer "
            f"alternative or refusal phrase."
        )

    return {
        "city": "",
        "n": 0,
        "title": name,
        "location": location,
        "story": story,
    }


def generate(slug: str, force: bool = False, dry_run: bool = False) -> int:
    entry = load_entry(slug)
    print(f"📋 atlas entry: {entry['name']} ({entry['entryStyle']})")
    print(f"   parent: {entry.get('parentEntry', '—')}")
    print(f"   query target: {entry.get('primaryQueryTarget', '—')}")
    print(f"   primary book funnels: {entry.get('primaryBookFunnels', [])}")

    scam = build_synthetic_scam(entry)
    print(f"\n🎬 synthesizing scene via Gemini (country=_default)...")

    try:
        body = synthesize_prompt("_default", scam)
    except Exception as e:
        print(f"❌ Gemini synthesis failed: {e}", file=sys.stderr)
        return 1

    print(f"   character chosen: {body['_character']}")
    print(f"   pilot anchor: {body['images'][0]}")

    if dry_run:
        print("\n--- PROMPT PREVIEW (dry-run) ---")
        print(body["prompt"])
        print("\n--- 4 PANELS ---")
        for i, p in enumerate(body["_scene"]["panels"], 1):
            print(f"  Panel {i}: {p['scene']}")
            print(f"    Dialogue: \"{p['dialogue']}\"")
        print("\n[dry-run] not submitting to Wavespeed.")
        return 0

    # R2 path + idempotency check
    r2_key = R2_KEY_TEMPLATE.format(slug=slug)
    public_url = PUBLIC_URL_TEMPLATE.format(slug=slug)
    out_dir = REPO / "tmp" / "atlas-comics"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}_hero.jpg"

    if out_path.exists() and out_path.stat().st_size >= _g.MIN_IMAGE_BYTES and not force:
        print(f"\n📂 cached locally at {out_path} ({out_path.stat().st_size:,}B). Use --force to regenerate.")
        # Still re-upload in case R2 was cleared
        r2_token = _g._keychain("cloudflare-api-token")
        if upload_to_r2(out_path, r2_key, r2_token):
            print(f"✅ uploaded cached file to {public_url}")
        return 0

    ws_token = _g._keychain("wavespeed-api-key")
    r2_token = _g._keychain("cloudflare-api-token")

    # Step 1: submit to /edit with _default pilot anchor
    print("\n📤 submitting to Wavespeed /edit (Nano Banana Pro)...")
    task_id = _g.submit_nbp(body, _g.EDIT_EP, ws_token)
    if not task_id:
        # Fallback to text-to-image
        print("   /edit failed; falling back to /text-to-image...")
        task_id = _g.submit_nbp(body, _g.T2I_EP, ws_token)
        if not task_id:
            print("❌ both /edit and /text-to-image failed at submit. Flag for manual review.", file=sys.stderr)
            return 2

    print(f"   task id: {task_id}")
    print("⏱  polling (up to 10 min)...")

    output_url = _g.poll_nbp(task_id, ws_token, timeout=600)
    if not output_url:
        # Try text-to-image once
        print("   poll timed out or failed; retrying via /text-to-image...")
        task_id_2 = _g.submit_nbp(body, _g.T2I_EP, ws_token)
        if task_id_2:
            output_url = _g.poll_nbp(task_id_2, ws_token, timeout=600)
        if not output_url:
            print("❌ polling failed twice. Flag for manual review.", file=sys.stderr)
            return 3

    print(f"✅ generation completed: {output_url}")

    # Step 2: download + verify
    ok, note = _g.download_verify(output_url, out_path)
    if not ok:
        # One more retry via text-to-image
        print(f"⚠ verification failed ({note}); retrying once via /text-to-image...")
        task_id_3 = _g.submit_nbp(body, _g.T2I_EP, ws_token)
        if task_id_3:
            output_url_3 = _g.poll_nbp(task_id_3, ws_token, timeout=600)
            if output_url_3:
                ok, note = _g.download_verify(output_url_3, out_path)
        if not ok:
            print(f"❌ download/verify failed twice ({note}). Flag for manual review.", file=sys.stderr)
            return 4

    print(f"✅ verified ({out_path.stat().st_size:,}B)")

    # Step 3: upload to R2
    if upload_to_r2(out_path, r2_key, r2_token):
        print(f"\n🚀 uploaded to R2: {public_url}")
        print("\n💡 If first fetch returns 404, wait ~60 seconds for CDN negative-cache to expire,")
        print("   or append ?v=1 to the <img src> on the atlas page.")
        return 0
    else:
        print(f"❌ R2 upload failed. Local file at {out_path}", file=sys.stderr)
        return 5


def upload_to_r2(src: Path, r2_key: str, r2_token: str) -> bool:
    print(f"\n☁  uploading to R2: {r2_key}")
    return _g.upload_r2(src, r2_key, r2_token)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="Atlas entry slug from entries.json (e.g., taxi-meter-manipulation)")
    parser.add_argument("--force", action="store_true",
                        help="Regenerate even if local cache exists")
    parser.add_argument("--dry-run", action="store_true",
                        help="Synthesize the prompt via Gemini and print it, but don't submit to Wavespeed")
    args = parser.parse_args()

    sys.exit(generate(args.slug, force=args.force, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
