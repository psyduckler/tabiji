#!/usr/bin/env python3
"""Regenerate 10 China scam comics flagged in the 2026-04-26 visual audit.

The 38-comic 2026-04-21 regen targeted v1 keyword-template fallbacks. This
follow-up audit caught a different failure mode in the v2 (bespoke Gemini
synthesis) outputs: the comic depicts the right *category* of scam but
omits the iconic visual element that defines the scam in its title — e.g.
the "Sichuan Hotpot" comic shows a generic restaurant menu with no hotpot;
the "Peking Duck Famous Restaurant" comic shows a chalkboard of noodles.

Fix: prepend a per-scam VISUAL REQUIREMENT block to the story that the
synthesizer already passes to Gemini. The prompt builder is unchanged;
the augmented story just biases Gemini toward depicting the iconic element.

Audit findings (1 hard mismatch + 9 partial mismatches):
  beijing/4    HARD: rickshaw scam → comic shows subway pickpocketing
  beijing/5    PARTIAL: Great Wall fake ticket → comic shows Forbidden City ticket
  beijing/6    PARTIAL: Peking Duck restaurant swap → comic shows generic noodles
  chengdu/5    PARTIAL: Sichuan Hotpot overcharge → no hotpot in comic
  shanghai/5   PARTIAL: Shanghai Disneyland fast pass → no Disney imagery
  shenzhen/2   PARTIAL: Huaqiangbei electronics → comic shows fake handbags
  guangzhou/6  PARTIAL: Dim Sum overcharge → no dim sum baskets
  yangshuo/4   PARTIAL: Yangshuo Beer Fish → no fish on the table
  harbin/4     PARTIAL: Russian dinner → menu shows Chinese Dongbei dishes
  chongqing/6  PARTIAL: Yangtze shore-excursion / 3 Gorges Dam → generic cruise booking

Run:
    python3 scripts/comic-pipeline/regen_china_audit_2026_04_26.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import extract_scams, generate_one, _keychain  # noqa: E402

# (city, n, must-depict hint appended to the scam's "story" before synthesis)
TARGETS = [
    ("beijing", 4,
     "at least 2 of the 4 panels MUST prominently depict a Beijing cycle rickshaw / "
     "trishaw / pedicab (three-wheeled cycle taxi pedalled by a driver) with the "
     "tourist sitting as the passenger; the price flip happens on arrival at the "
     "destination. Do NOT depict a subway, bus, or pickpocketing scene — this scam "
     "is a rickshaw price flip, not pickpocketing."),
    ("beijing", 5,
     "at least one panel MUST clearly show the Great Wall of China (the iconic "
     "stone wall snaking across mountain ridges with watchtowers — Badaling or "
     "Mutianyu section). At least one panel MUST show the tour bus stopping at a "
     "shopping detour ('jade museum', silk shop, or tea house). Do NOT depict the "
     "Forbidden City — this scam is specifically about bait-priced Great Wall day "
     "tours padded with commission shopping stops."),
    ("beijing", 6,
     "at least 2 panels MUST clearly depict roasted Peking duck — a whole "
     "lacquered golden-brown duck on a serving platter, ideally being sliced "
     "tableside by a chef (the classic carving-in-front-of-guests presentation), "
     "with thin pancakes, scallions, and hoisin sauce visible. Do NOT show a "
     "noodle bowl or noodle-only chalkboard menu — this scam is specifically "
     "about Peking duck restaurants, the iconic Beijing dish."),
    ("chengdu", 5,
     "at least 2 panels MUST clearly depict a Sichuan hotpot in use — a divided "
     "round pot in the centre of the table (yin-yang split, red spicy chili broth "
     "on one side and clear broth on the other), steam rising, with plates of raw "
     "meat slices, lotus root, vegetables, and tofu skin around it, and chopsticks "
     "dipping into the broth. Do NOT depict a generic restaurant table or noodle "
     "shop — Sichuan hotpot is the iconic Chengdu dish."),
    ("shanghai", 5,
     "at least 2 panels MUST clearly depict Shanghai Disneyland imagery — the "
     "Enchanted Storybook Castle (the tall fairy-tale castle with multiple turrets "
     "and a central spire that defines Shanghai Disney), Mickey Mouse silhouettes "
     "or balloons, the Disney park entrance arch with Disney lettering, or visible "
     "Disney park signage. Do NOT depict the Bund or any European-style "
     "architecture — this scam is specifically about Shanghai Disneyland in Pudong."),
    ("shenzhen", 2,
     "at least 2 panels MUST clearly depict consumer electronics on sale — glass "
     "display cases full of smartphones / iPhones, walls of AirPods or earbud "
     "boxes, drones, smartwatches, or laptops at Huaqiangbei market booths. The "
     "classic shot: a tourist holding a counterfeit AirPods box at a stall, or "
     "comparing a fake phone to a real one. Do NOT depict counterfeit handbags / "
     "Gucci / fashion — this scam is about FAKE ELECTRONICS at Huaqiangbei."),
    ("guangzhou", 6,
     "at least 2 panels MUST clearly depict Cantonese dim sum — bamboo steamer "
     "baskets stacked 2-3 high on the table, lids partially open to reveal har gow "
     "(translucent shrimp dumplings), siu mai (pork-and-shrimp dumplings), char "
     "siu bao (white steamed buns), or chicken feet, with chopsticks and tea cups. "
     "The classic dim-sum table is round and covered in round bamboo steamers. "
     "Do NOT depict a noodle bowl or noodle chalkboard menu — this scam is "
     "specifically about Cantonese dim sum."),
    ("yangshuo", 4,
     "at least 2 panels MUST clearly depict Yangshuo's signature 'Beer Fish' "
     "(啤酒鱼) — a whole freshwater fish (head and tail visible) stewed in a wide "
     "flat pot or claypot in a beer-and-chili broth, with green chili slices and "
     "an open beer bottle nearby on the table. Karst-mountain views through the "
     "window reinforce Yangshuo. Do NOT depict generic noodles, dumplings, or a "
     "noodle chalkboard — this scam is specifically about the Beer Fish dish."),
    ("harbin", 4,
     "at least 2 panels MUST clearly depict Russian cuisine on the table — "
     "borscht (deep-red beet soup in a bowl), pelmeni / Russian dumplings, dark "
     "rye bread, vodka glasses or a vodka bottle, perhaps beef stroganoff. "
     "Russian-style décor: matryoshka nesting dolls on a shelf, a samovar on the "
     "counter, Russian-Orthodox onion-domed church visible through the window. "
     "The posted-prices chalkboard in panel 4 must list Russian dishes (Borscht, "
     "Pelmeni, Stroganoff), NOT Chinese noodles. Do NOT depict Chinese Dongbei "
     "food — this scam is specifically about Russian-cuisine restaurants on "
     "Zhongyang Street."),
    ("chongqing", 6,
     "at least one panel MUST clearly depict the Three Gorges Dam (the massive "
     "concrete hydroelectric dam across the Yangtze, with its wide concrete "
     "spillway and a dramatic gorge backdrop) OR one of the named shore-excursion "
     "stops (Fengdu Ghost City's hillside temples and demon statues, the "
     "red-wooden Shibaozhai pagoda built into a cliff, or the White Emperor City "
     "pagoda). At least one panel should show a guide on a cruise-ship deck "
     "pitching an 'optional' shore excursion to seated passengers, with the "
     "Yangtze visible behind. Do NOT depict a generic dinner-cruise booking — "
     "this scam is specifically about ON-BOARD upsells of shore excursions."),
]

COUNTRY = "china"
BATCH_SIZE = 3

OUT_DIR = Path("/tmp/china-audit-2026-04-26-comics")
AUDIT_LOG = Path("/tmp/china-audit-2026-04-26.jsonl")
FLAG_LOG = Path("/tmp/china-audit-2026-04-26-flagged.log")


def collect_targets() -> list[dict]:
    """Build the list of 10 scam dicts with augmented stories."""
    by_city: dict[str, dict[int, str]] = {}
    for city, n, hint in TARGETS:
        by_city.setdefault(city, {})[n] = hint
    out = []
    for city, wanted in sorted(by_city.items()):
        scams = extract_scams(city)
        want_ns = set(wanted.keys())
        found_ns = {s["n"] for s in scams}
        missing = want_ns - found_ns
        if missing:
            raise RuntimeError(f"{city}: could not extract scams {sorted(missing)} from HTML")
        for s in scams:
            if s["n"] in want_ns:
                # Trim to leave headroom for the appended hint, then append.
                hint = wanted[s["n"]]
                base = s["story"][:1100].rstrip()
                s["story"] = (
                    base
                    + "\n\n---\nREQUIRED VISUAL ELEMENT: "
                    + hint
                )
                out.append(s)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_LOG.write_text("")
    FLAG_LOG.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    targets = collect_targets()
    hint_by_key = {(c, n): h for c, n, h in TARGETS}
    print(f"[{COUNTRY}] regenerating {len(targets)} flagged scams (batch={BATCH_SIZE})",
          flush=True)

    ok = retried = flagged = 0
    t0 = time.time()
    for i in range(0, len(targets), BATCH_SIZE):
        batch = targets[i:i + BATCH_SIZE]
        elapsed = int(time.time() - t0)
        print(f"\n=== batch {i // BATCH_SIZE + 1}  t={elapsed}s  ({len(batch)} items) ===",
              flush=True)
        with ThreadPoolExecutor(max_workers=BATCH_SIZE) as ex:
            futs = [
                ex.submit(generate_one, COUNTRY, s, OUT_DIR, ws_token, r2_token, True)
                for s in batch
            ]
            for s, f in zip(batch, futs):
                try:
                    res = f.result()
                except Exception as e:
                    res = {"status": "flagged", "note": f"unhandled err: {e}",
                           "character": "?", "prompt": None}
                key = (s["city"], s["n"])
                label = f"{s['city']}/scam-{s['n']}"
                line = (f"{label}: {res['status']}  char={res['character']}  "
                        f"({res['note']})")
                print(f"  {line}", flush=True)
                AUDIT_LOG.open("a").write(json.dumps({
                    "city": s["city"], "n": s["n"], "title": s["title"],
                    "hint": hint_by_key[key], **res,
                }) + "\n")
                if res["status"] in ("ok", "ok-cached"):
                    ok += 1
                elif res["status"] == "ok-retried":
                    retried += 1
                    ok += 1
                else:
                    flagged += 1
                    FLAG_LOG.open("a").write(line + "\n")

    summary = {
        "country": COUNTRY, "total": len(targets),
        "ok": ok, "retried": retried, "flagged": flagged,
        "elapsed_s": int(time.time() - t0),
        "audit_log": str(AUDIT_LOG), "flagged_log": str(FLAG_LOG),
    }
    print(f"\n[{COUNTRY}] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    main()
