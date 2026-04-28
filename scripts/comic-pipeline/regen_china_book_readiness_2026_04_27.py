#!/usr/bin/env python3
"""Regenerate 17 China scam comics flagged in the 2026-04-27 book-readiness audit.

Two failure modes:
  (A) Wrong-locale / wrong-mechanic comics where the backdrop or scene
      depicted doesn't match the scam's title or location — e.g. harbin/1
      shows Moscow's St. Basil's Cathedral instead of Harbin's Saint Sophia.
  (B) Prompt-leak / gibberish text artifacts visible in the panel — e.g.
      shanghai/4 has "tea-house scam" rendered literally; chengdu/6 has the
      caption "Declinery head."; menus in dollars with garbled food names.

Fix: prepend a per-scam VISUAL REQUIREMENT block to the scam story before
Gemini synthesis. Same pattern as regen_china_audit_2026_04_26.py.
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

COUNTRY = "china"
BATCH_SIZE = 4
OUT_DIR = _HERE.parent.parent / "tmp" / "china-book-readiness-regen-2026-04-27"
AUDIT_LOG = OUT_DIR / "audit.jsonl"
FLAG_LOG = OUT_DIR / "flagged.txt"

# (city, n, must-depict / must-NOT-depict hint)
TARGETS = [
    # ===== TIER 1A: HARD WRONG-LOCALE / WRONG-MECHANIC =====
    ("harbin", 1,
     "BACKDROP REQUIREMENT: at least 2 of the 4 panels MUST show Harbin's "
     "Saint Sophia Cathedral — the green-domed Russian Orthodox cathedral "
     "in Harbin (red brick, single large green onion dome, Byzantine cross). "
     "DO NOT depict Moscow's St. Basil's Cathedral (multi-colored swirl-domed "
     "cathedral on Red Square) — that is the wrong city in the wrong country. "
     "If snow / ice sculptures are shown, they should be the Harbin Ice and "
     "Snow World festival pieces (massive backlit ice palaces and cathedrals). "
     "The scam takes place in Harbin, China, NOT in Moscow, Russia."),

    ("macau", 6,
     "BACKDROP REQUIREMENT: panels MUST be set at Macau tourist landmarks: "
     "the Ruins of St. Paul's (Portuguese Baroque stone façade with rose "
     "window, top of a wide stone staircase) AND/OR A-Ma Temple (traditional "
     "Chinese temple with red columns and dragon roof tiles, smoking incense "
     "burners in courtyard), AND/OR Senado Square (wave-pattern Portuguese "
     "calçada paving, pastel colonial buildings). DO NOT depict a subway "
     "train, metro car, or rush-hour transit scene — this scam is about "
     "pickpockets at outdoor tourist landmarks, NOT public transit. The "
     "pickpocket action should happen on the steps of St. Paul's, in the "
     "incense-burning courtyard of A-Ma Temple, or at the Senado Square "
     "bus-tour disembark zone. Each panel must have a distinct numbered "
     "label (1, 2, 3, 4) without duplicates."),

    ("shenzhen", 4,
     "BACKDROP REQUIREMENT: panels MUST be set on Shenzhen's Dongmen "
     "Pedestrian Street or Huaqiang North pedestrian electronics street — "
     "outdoor crowded pedestrian shopping streets with Chinese shopfront "
     "signage, market stalls, hanging banners, dense daytime foot traffic. "
     "DO NOT depict a subway train, metro car, or any transit interior — "
     "this scam is specifically about opportunistic pickpocketing on outdoor "
     "pedestrian streets, NOT on public transit. The pickpocket action "
     "should occur in a sidewalk crowd at a stall."),

    ("beijing", 8,
     "BACKDROP REQUIREMENT: at least 2 panels MUST show the Temple of Heaven "
     "(天坛) — the iconic circular Hall of Prayer for Good Harvests with its "
     "three blue tiered roofs on a white circular marble platform — OR the "
     "Summer Palace (Kunming Lake with the Long Corridor, Marble Boat, or "
     "Longevity Hill pavilions). DO NOT depict the Forbidden City's red "
     "vermilion walls, golden tiled roofs, or any rectangular palace "
     "buildings — that is the wrong landmark for this scam. The fake guide "
     "should approach tourists in the Temple of Heaven gardens or Summer "
     "Palace lakeshore."),

    ("pingyao", 3,
     "CAST REQUIREMENT: the protagonist MUST be one of the 4 canonical tabiji "
     "characters: Margie (62-year-old white woman with gray hair often in a "
     "bun, sun hat or scarf, glasses, traveler outfit) OR Priya (34-year-old "
     "South Asian / Indian woman with long dark hair, sun hat, backpack) OR "
     "Marcus (34-year-old white man with short brown hair, beard, polo and "
     "khakis) OR Harry (64-year-old white man with gray hair, light jacket, "
     "camera bag). DO NOT depict an unidentified young East-Asian Chinese "
     "woman as the tourist — the protagonist must be a clearly foreign "
     "Western/South-Asian traveler from the canonical cast. Pick ONE of the "
     "4 canonical characters and use them consistently across all 4 panels. "
     "Backdrop should be Pingyao Ancient City (Ming-Qing era walled town "
     "with grey-brick courtyard houses, narrow stone-paved alleys, red "
     "lanterns, traditional wooden doorways)."),

    # ===== TIER 1B: PROMPT-LEAK / GIBBERISH TEXT ARTIFACTS =====
    ("shanghai", 4,
     "TEXT REQUIREMENT: panel speech bubbles must contain ONLY the dialogue "
     "lines — no meta-prompt text, no labels, no scene descriptions. DO NOT "
     "render the literal text 'tea-house scam' anywhere in any panel "
     "(including phones, books, signs, or speech). DO NOT include city-name "
     "labels like 'Beijing/Shanghai' as panel captions. Each panel must have "
     "exactly one speech bubble or thought bubble with natural in-character "
     "dialogue, plus a clean numeric panel label (1, 2, 3, 4)."),

    ("suzhou", 3,
     "TEXT REQUIREMENT: phones, signs, and any text shown in panels must "
     "render natural in-world content — DO NOT render the literal text "
     "'tea-house scam' on any phone screen, sign, or surface in any panel. "
     "If a phone is shown, it should display a Dianping or Trip.com app "
     "screen with restaurant listings or a map, NOT the meta-prompt label. "
     "Speech bubbles should contain natural dialogue only."),

    ("guangzhou", 3,
     "TEXT REQUIREMENT: panels must NOT contain any prompt-leak labels or "
     "scene-description captions. DO NOT render text like 'Margie, City "
     "shopping street.' or any character-and-setting description as visible "
     "text in the image. Speech bubbles contain natural dialogue only; "
     "panel labels are simple numbers 1-4."),

    ("guangzhou", 4,
     "TEXT REQUIREMENT: any handbag / luggage / fake-brand product visible "
     "in panels must show either no brand text at all, OR a clearly readable "
     "obvious-knockoff brand parody like 'Lous Vutton' or 'Gucchi' (recognizable "
     "as a knockoff). DO NOT render gibberish brand text like 'Choody mes' or "
     "'Choobby mes' — make the text either readable or absent. The Beijing "
     "Road / Shangxiajiu pedestrian shopping street backdrop should be "
     "preserved."),

    ("chengdu", 4,
     "TEXT REQUIREMENT: panel 4 must contain ONE clean, readable defensive "
     "tip in the speech bubble (e.g. 'Real tea houses post prices!' or "
     "similar). DO NOT render duplicated or broken variants like 'Real house "
     "post prices!' alongside the correct version. Each panel: one speech "
     "bubble, clean dialogue text, no duplicated phrases."),

    ("chengdu", 6,
     "TEXT REQUIREMENT: panel captions must be readable English dialogue. "
     "DO NOT render gibberish text like 'Declinery head.' as a caption. "
     "Each panel has ONE speech bubble with natural in-character dialogue, "
     "plus a numeric panel label (1, 2, 3, 4). The Chengdu jade / TCM / "
     "silk shopping-tour backdrop should be preserved."),

    ("pingyao", 4,
     "TEXT REQUIREMENT: any restaurant menu shown in panels MUST display "
     "Chinese yuan prices (¥18, ¥45, ¥80, etc.) — NOT US dollar prices. "
     "Menu items should be readable Chinese cuisine names like 'Dao xiao "
     "mian (knife-cut noodles) ¥18', 'Pingyao beef ¥45', 'Shanxi vinegar "
     "noodles ¥22' — NOT gibberish words like 'Chine $1.95', 'Mock $1.45', "
     "'Han nuct $2.00'. The setting is Pingyao Ancient City, China, with "
     "yuan pricing, NOT a US restaurant."),

    ("xian", 2,
     "TEXT REQUIREMENT: any restaurant menu shown in panels MUST display "
     "readable Shaanxi cuisine items in clean English with yuan pricing — "
     "e.g. 'Yangrou paomo (mutton stew) ¥45', 'Roujiamo (Chinese hamburger) "
     "¥15', 'Liangpi (cold noodles) ¥18', 'Sour Plum Soup ¥10'. DO NOT "
     "render gibberish items like 'Sungin Soup', 'Chiken Soup', 'Cooked "
     "Pany', 'Common Noodles', 'Sillilan Mualim Chinese'. Backdrop is the "
     "Xi'an Muslim Quarter with strings of red lanterns and food-stall signs."),

    ("zhangjiajie", 4,
     "TEXT REQUIREMENT: any restaurant menu shown in panels MUST display "
     "readable Hunan/Tujia cuisine items in clean English with yuan pricing "
     "— e.g. 'La rou (cured pork) ¥80', 'Liang fen (cold jelly noodles) "
     "¥18', 'Sour fish soup ¥75', 'Three-cup chicken ¥65'. DO NOT render "
     "gibberish like 'Chilsen choosee prices', 'Stewing spired dishes', "
     "'Tortoissone sherd dishes', 'Glass siwing column'. Backdrop is "
     "Wulingyuan town with karst-pillar mountains visible in panel 4."),

    ("guilin", 6,
     "TEXT REQUIREMENT: any restaurant menu shown in panels MUST display "
     "readable Guangxi / Guilin cuisine items in clean English with yuan "
     "pricing — e.g. 'Guilin rice noodles ¥15', 'Beer fish ¥85', 'Stir-fry "
     "vegetables ¥35', 'Steamed pork ribs ¥55'. DO NOT render gibberish "
     "like 'Chinee dishes', 'Frilled dishes', 'Chicenean dishes'. Backdrop "
     "is Zhengyang Pedestrian Street with karst peaks visible in the night-sky "
     "background."),

    ("xian", 4,
     "TEXT REQUIREMENT: each panel must have exactly ONE speech bubble. DO "
     "NOT render duplicate speech bubbles within the same panel — for "
     "example, panel 1 must NOT contain two copies of 'Rush hour squeeze!' "
     "stacked on top of each other. Each panel: one speech bubble, one "
     "panel label (1, 2, 3, 4), no duplicates."),

    ("chongqing", 4,
     "TEXT REQUIREMENT: each panel must have exactly ONE numeric label "
     "in the corner (1, 2, 3, 4 — one per panel). DO NOT render duplicate "
     "panel-number markers — for example, panel 3 must NOT contain two "
     "copies of the '3' marker. The Hongyadong / Jiefangbei photo-spot "
     "backdrop should be preserved with the cliffside Qiansimen Bridge "
     "viewpoint visible at night."),
]


def collect_targets() -> list[dict]:
    """Pull scam dicts from each city's HTML and merge with hints."""
    by_city: dict[str, list[dict]] = {}
    for c, n, _hint in TARGETS:
        by_city.setdefault(c, set()).add(n)
    out = []
    hint_map = {(c, n): h for c, n, h in TARGETS}
    for city, ns in by_city.items():
        for s in extract_scams(city):
            if s["n"] in ns:
                hint = hint_map[(city, s["n"])]
                # Prepend hint to the scam's story so Gemini synthesizer
                # gives it priority during prompt construction
                s["story"] = f"{hint}\n\n{s['story']}"
                out.append(s)
    out.sort(key=lambda s: (s["city"], s["n"]))
    return out


def main() -> dict:
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
