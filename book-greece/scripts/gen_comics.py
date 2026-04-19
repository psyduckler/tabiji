#!/usr/bin/env python3
"""
Generate the Greece book comic assets via Wavespeed (Nano Banana Pro):
 - front cover (single dramatic panel, 2:3 aspect)
 - back cover (single scene with empty upper third for text overlay, 2:3)
 - 24 missing per-scam comics (2x2 grid red-figure pottery, 1:1) for
   Chania / Thessaloniki / Paros / Naxos.

Style is ancient Greek red-figure pottery — figures rendered as flat orange-red
silhouettes on deep matte terracotta background with fine black painted details,
classical profile poses, and geometric border motifs (meanders/laurel).

Usage:
    python3 book-greece/scripts/gen_comics.py              # all assets
    python3 book-greece/scripts/gen_comics.py --covers-only
    python3 book-greece/scripts/gen_comics.py --scams-only
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import requests


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
COVERS_DIR = BOOK / "assets" / "covers"
SCAMS_DIR = BOOK / "assets" / "scam-comics"
COVERS_DIR.mkdir(parents=True, exist_ok=True)
SCAMS_DIR.mkdir(parents=True, exist_ok=True)


STYLE_GREECE = (
    "A single illustrated comic book page drawn as ancient Greek red-figure "
    "pottery storytelling — figures rendered as flat orange-red silhouettes on "
    "a deep matte terracotta background with fine black painted details on the "
    "figures, classical profile poses, and geometric border motifs of meanders "
    "(Greek key) and laurel leaves framing each panel, a modern sequential-comic "
    "layout merged with ancient vase-painting aesthetics. Showing four sequential "
    "panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left "
    "corner of each panel, separated by thin white gutters. Each panel contains "
    "one clean white rounded speech bubble with a small pointer tail, holding "
    "short printed English dialogue in simple black comic lettering — text must "
    "be legible, in English only, and correctly spelled. Square 1:1 composition, "
    "2K resolution."
)

# Cast characters (paste verbatim into prompts)
MARGIE = (
    "A 62-year-old Western woman with shoulder-length silver-gray hair worn under "
    "a woven straw sun hat with a cream ribbon, warm blue eyes behind tortoiseshell "
    "reading glasses often perched on her head, light olive complexion with gentle "
    "laugh lines and a friendly curious expression. She wears a cream linen blouse, "
    "tan wide-leg travel pants, and white canvas sneakers, with a small tan leather "
    "crossbody bag and a coral scarf. Gracious, cheerful, a little too trusting."
)

PRIYA = (
    "A 34-year-old South Asian woman with long dark wavy hair pulled into a low "
    "ponytail under a wide-brim navy sun hat, warm brown eyes, clear brown skin, "
    "athletic build and confident posture. She wears olive utility shorts and a "
    "terracotta cotton t-shirt, white running sneakers, and carries a charcoal "
    "compact hiking backpack with a reusable water bottle clipped to the side. "
    "Sunglasses pushed up on her head. Capable, lightly skeptical, a prepared traveler."
)

HARRY = (
    "A 64-year-old Western man with close-cropped silver-white hair and a neatly-"
    "trimmed salt-and-pepper beard, warm hazel eyes with kind wrinkles, light tan "
    "complexion. He wears a pale-blue short-sleeve button-down, beige chinos, brown "
    "leather loafers, and a soft navy baseball cap, with a small brown leather sling "
    "bag and a simple silver watch. Often holds a folded paper map or pocket guidebook. "
    "Affable, chatty, easily charmed."
)

MARCUS = (
    "A 34-year-old man of mixed heritage with short dark-brown hair and light stubble, "
    "warm medium-brown skin, athletic build. He wears an olive-green polo shirt, dark "
    "khaki slim travel trousers, and brown trail sneakers, with a black sling bag and "
    "a DSLR camera on a woven strap around his neck, sunglasses hooked at his collar. "
    "Observant, curious, slightly guarded but warm."
)


# --- COVER PROMPTS --------------------------------------------------------

COVERS = [
    (
        "front",
        (
            "A single dramatic ancient Greek red-figure pottery scene, portrait 2:3 "
            "aspect, depicting a Greece tourist scam in action: a female tourist "
            "wearing a sun hat stands in front of the Parthenon columns on the "
            "Acropolis, looking slightly worried, while a friendly smiling Greek man "
            "in a casual shirt points at the temple and says 'Acropolis closed today!' "
            "in a white speech bubble. Figures rendered as flat orange-red silhouettes "
            "on deep matte terracotta with fine black details, classical profile poses, "
            "geometric meander border. Composition leaves generous empty sky in the "
            "upper third for a book-cover title. No book title, no watermark, no logo."
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single ancient Greek red-figure pottery scene, portrait 2:3 aspect, "
            "depicting a peaceful Greek island harbour at twilight: a whitewashed "
            "village with blue-domed churches climbing a hill, fishing boats in the "
            "harbour, and a small group of tourists walking the waterfront promenade. "
            "Figures rendered as flat orange-red silhouettes on deep matte terracotta "
            "with fine black details, classical profile poses, geometric meander and "
            "laurel border. Composition has substantial empty dark-teal sky in the "
            "upper two-thirds for back-cover copy overlay. No text, no watermark."
        ),
        "2:3",
    ),
]


# --- MISSING SCAM COMICS --------------------------------------------------
# Chania, Thessaloniki, Paros, Naxos need comics. We rotate cast members.

SCAM_COMICS: list[tuple[str, int, str, str]] = [
    # CHANIA (6 scams)
    ("chania", 1, MARGIE,
     "Panel 1: Margie sits at a waterfront café in Chania's Old Venetian Harbour; "
     "waiter brings bread and olives without asking. Speech bubble: 'Compliments!' "
     "Panel 2: She enjoys the harbour view with coffee; bill arrives. "
     "Panel 3: Bill shows '€8 cappuccino, €6 bread cover, €4 cutlery'. Speech bubble: "
     "'But I didn't order these!' Panel 4: She walks inland to a local taverna; sign "
     "reads '€2.50 coffee'. Speech bubble: 'Much better!'"),

    ("chania", 2, PRIYA,
     "Panel 1: Priya at Chania Airport taxi rank; driver says 'Meter broken, €50 to "
     "Old Town!' Panel 2: She checks her phone showing '€25-35 metered fare'. "
     "Panel 3: She walks to the KTEL bus stop. Speech bubble: '€2.50 bus, no scam.' "
     "Panel 4: Arriving in Chania Old Town by bus, smiling. Speech bubble: 'Saved €45!'"),

    ("chania", 3, HARRY,
     "Panel 1: Harry at a Chania tour desk; agent says 'Balos lagoon tour €90!' "
     "Panel 2: He researches on phone: 'Direct ferry from Kissamos: €35'. "
     "Panel 3: He drives to Kissamos Port himself. Speech bubble: 'Much cheaper.' "
     "Panel 4: At turquoise Balos lagoon, happy. Speech bubble: 'Worth the effort!'"),

    ("chania", 4, MARCUS,
     "Panel 1: Marcus at Chania rental shop; agent says 'Sign here, €300 deposit.' "
     "Panel 2: He photographs every scratch on the car with his phone. "
     "Panel 3: On return, agent points at scratch: 'That's new, €500!' "
     "Panel 4: Marcus shows timestamped photo. Speech bubble: 'Already there.' Agent backs down."),

    ("chania", 5, MARGIE,
     "Panel 1: Margie at Souda petrol station; attendant pumps fuel. Speech bubble: "
     "'€50 total.' Panel 2: She hands over €100 note, states loudly: 'One hundred!' "
     "Panel 3: Attendant gives €40 change. Speech bubble: 'That's €10 short.' "
     "Panel 4: She counts change in front of attendant; he hands over correct amount."),

    ("chania", 6, HARRY,
     "Panel 1: Harry on Leather Lane in Chania; vendor says 'Handmade Cretan sandals, "
     "€80!' Panel 2: He examines the sandals closely; label says 'Made in Turkey'. "
     "Panel 3: He walks to Manolis workshop; sign says 'Authentic since 1960s'. "
     "Panel 4: Buying real handmade sandals. Speech bubble: 'Now these are genuine!'"),

    # THESSALONIKI (6 scams)
    ("thessaloniki", 1, PRIYA,
     "Panel 1: Priya books Uber at Thessaloniki Airport; estimate shows €14. "
     "Panel 2: Ride ends; app charges €24. Speech bubble: 'Wait, that's wrong!' "
     "Panel 3: She opens dispute in FreeNow app. Speech bubble: 'Filing complaint.' "
     "Panel 4: Next time, takes 01X bus for €2. Speech bubble: 'Lesson learned!'"),

    ("thessaloniki", 2, MARGIE,
     "Panel 1: Margie at Ladadika restaurant; waiter brings bread and tzatziki. "
     "Speech bubble: 'Welcome gift!' Panel 2: Bill arrives with €15 cover charge. "
     "Panel 3: She points at Greek law sign: 'Unlisted covers illegal!' "
     "Panel 4: Walking to Mourga taverna. Speech bubble: 'Posted prices, honest food.'"),

    ("thessaloniki", 3, MARCUS,
     "Panel 1: Marcus at Aristotelous Square; man approaches with bracelet. Speech "
     "bubble: 'Gift for you, friend!' Panel 2: Bracelet slipped on wrist; man demands "
     "'€20!' Panel 3: Marcus crosses arms, steps back. Speech bubble: 'No thank you.' "
     "Panel 4: Walking away, bracelet cut off at café. Speech bubble: 'Worth nothing.'"),

    ("thessaloniki", 4, HARRY,
     "Panel 1: Harry at tour desk; agent says 'Meteora day trip €55, 14 hours!' "
     "Panel 2: He calculates: '8 hours driving, 3 hours there, rushed lunch.' "
     "Panel 3: He books train to Kalambaka instead. Speech bubble: '€20, overnight stay.' "
     "Panel 4: At Meteora monasteries at sunrise. Speech bubble: 'So much better!'"),

    ("thessaloniki", 5, PRIYA,
     "Panel 1: Priya enters Valaoritou bar; host says 'VIP table this way!' "
     "Panel 2: Seated, menu appears: 'Minimum €80 per person.' Speech bubble: 'What?!' "
     "Panel 3: She asks for minimum before sitting next time. Speech bubble: 'How much?' "
     "Panel 4: At Canteen bar with posted prices. Speech bubble: 'Clear and fair.'"),

    ("thessaloniki", 6, MARGIE,
     "Panel 1: Margie gets Booking.com message: 'Pay deposit via this link.' "
     "Panel 2: She notices URL is 'booking-payment.com' not booking.com. "
     "Panel 3: She calls hotel directly via Google Maps number. Speech bubble: "
     "'Is this request real?' Panel 4: Hotel confirms: 'Scam! Never pay off-platform.'"),

    # PAROS (6 scams)
    ("paros", 1, HARRY,
     "Panel 1: Harry at Parikia ferry port with luggage; driver says '€40 to hotel!' "
     "Panel 2: Sign shows 'Greek minimum fare €5 + €1 port.' Speech bubble: 'That's 8x!' "
     "Panel 3: He takes KTEL bus. Speech bubble: '€1.80 to Naoussa.' "
     "Panel 4: Arriving at hotel by bus, relaxed. Speech bubble: 'Saved €38!'"),

    ("paros", 2, MARGIE,
     "Panel 1: Margie at Naoussa Old Port restaurant; menu has no prices. "
     "Panel 2: She asks for printed menu; waiter hesitates. Speech bubble: 'Prices please.' "
     "Panel 3: She walks 200m inland to Sigi Ikthios. Sign shows posted prices. "
     "Panel 4: Enjoying honest meal. Speech bubble: 'Same view, half the price!'"),

    ("paros", 3, PRIYA,
     "Panel 1: Priya at Parikia rental shop; agent says 'ATV €50/day, deposit €500 cash.' "
     "Panel 2: She insists: 'Credit card only.' Agent frowns. "
     "Panel 3: She rents from Europcar at airport with insurance. Speech bubble: 'Safer.' "
     "Panel 4: Driving Paros roads in proper car. Speech bubble: 'No damage scam risk!'"),

    ("paros", 4, MARCUS,
     "Panel 1: Marcus gets email: 'Complete payment via secure link before arrival.' "
     "Panel 2: He checks URL carefully: 'booking-secure-pay.gr' — not booking.com. "
     "Panel 3: He calls hotel via Google Maps. Speech bubble: 'Is this real?' "
     "Panel 4: Hotel confirms scam. Speech bubble: 'Never click email payment links!'"),

    ("paros", 5, HARRY,
     "Panel 1: Harry at tour desk; agent says 'Antiparos private yacht €500!' "
     "Panel 2: He checks ferry schedule. Speech bubble: '€2.50 each way to Antiparos.' "
     "Panel 3: He takes public ferry from Pounda. "
     "Panel 4: Exploring Antiparos Cave for €6 entry. Speech bubble: 'Total: €15 vs €500!'"),

    ("paros", 6, MARGIE,
     "Panel 1: Margie at Golden Beach; vendor says '€15 for two sunbeds, all day!' "
     "Panel 2: At 4pm, vendor returns: 'That's €60 — €15 per chair per HOUR.' "
     "Panel 3: She shows written receipt: '€15 total, full day.' "
     "Panel 4: Vendor accepts. Speech bubble: 'Always get it in writing!'"),

    # NAXOS (6 scams)
    ("naxos", 1, PRIYA,
     "Panel 1: Priya at Plaka Beach; vendor says '€5 per chair.' Speech bubble: 'Great!' "
     "Panel 2: After 4 hours, bill is €40. Speech bubble: '€5 per chair per HOUR?!' "
     "Panel 3: Next beach, she asks clearly: 'Total for full day, in writing?' "
     "Panel 4: Enjoying beach with written receipt. Speech bubble: '€15 total, sorted!'"),

    ("naxos", 2, MARCUS,
     "Panel 1: Marcus at Matha Rent a Car; clerk says 'Sign here, passport deposit.' "
     "Panel 2: He sees Reddit warning on phone: 'DO NOT RENT WITH MATHA.' "
     "Panel 3: He walks to Europcar at Naxos Airport. Speech bubble: 'Major brand only.' "
     "Panel 4: Driving safely, card ready to lock. Speech bubble: 'No damage scam today!'"),

    ("naxos", 3, HARRY,
     "Panel 1: Harry at Naxos Chora waterfront restaurant; waiter brings welcome bread. "
     "Panel 2: Bill shows €12 bread, €8 olives added. Speech bubble: 'I never ordered these!' "
     "Panel 3: He points at Greek law poster. Speech bubble: 'Unlisted covers: €500 fine.' "
     "Panel 4: Eating at Metaxi Mas with posted prices. Speech bubble: 'Locals eat here!'"),

    ("naxos", 4, MARGIE,
     "Panel 1: Margie at Naxos port; driver quotes '€20 to hotel.' Speech bubble: '1km walk!' "
     "Panel 2: She checks meter rate: '€4 base + €1 port = €5 minimum.' "
     "Panel 3: She takes KTEL bus. Speech bubble: '€1.80, comfortable.' "
     "Panel 4: Arriving at hotel by bus. Speech bubble: 'Why pay 4x the real price?'"),

    ("naxos", 5, PRIYA,
     "Panel 1: Priya gets email from 'Booking.com': 'Pay balance via secure link.' "
     "Panel 2: She logs into Booking.com directly — no payment request there. "
     "Panel 3: She screenshots the scam email for Tourist Police. "
     "Panel 4: At hotel, pays at check-in. Speech bubble: 'Never click email links!'"),

    ("naxos", 6, HARRY,
     "Panel 1: Harry at Chora tour desk; agent says 'Traditional village tour €85!' "
     "Panel 2: He checks KTEL: 'Bus to Apiranthos €4, Halki €2.50.' "
     "Panel 3: He rents car for €35/day and drives the villages himself. "
     "Panel 4: At Apiranthos marble streets, lunch at local taverna. Speech bubble: "
     "'Better pace, half the cost!'"),
]


def get_api_key() -> str:
    key = os.environ.get("WAVESPEED_API_KEY")
    if key:
        return key.strip()
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "wavespeed-api-key", "-w"],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        sys.exit("could not read WAVESPEED_API_KEY from keychain or env")
    return result.stdout.strip()


def submit(api_key: str, prompt: str, aspect_ratio: str = "1:1") -> str:
    url = "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image"
    r = requests.post(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }, json={
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": "2k",
        "output_format": "jpeg",
    }, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["data"]["id"] if "data" in data and "id" in data["data"] else data["id"]


def poll(api_key: str, task_id: str, timeout: int = 360) -> str:
    url = f"https://api.wavespeed.ai/api/v3/predictions/{task_id}/result"
    headers = {"Authorization": f"Bearer {api_key}"}
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        body = r.json()
        payload = body.get("data", body)
        status = payload.get("status")
        if status == "completed":
            outputs = payload.get("outputs") or payload.get("output") or []
            return outputs if isinstance(outputs, str) else outputs[0]
        if status == "failed":
            raise RuntimeError(f"task failed: {body}")
        time.sleep(3)
    raise TimeoutError(f"task {task_id} timed out")


def download(url: str, dest: Path) -> None:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)


def generate(api_key: str, prompt: str, dest: Path, aspect_ratio: str) -> bool:
    try:
        task = submit(api_key, prompt, aspect_ratio)
        out_url = poll(api_key, task)
        download(out_url, dest)
        return True
    except Exception as e:
        print(f"✗ {dest}: {e}", file=sys.stderr)
        return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--covers-only", action="store_true")
    ap.add_argument("--scams-only", action="store_true")
    args = ap.parse_args()

    api_key = get_api_key()

    tasks: list[tuple[str, Path, str]] = []  # (prompt, dest_path, aspect)
    if not args.scams_only:
        for name, subject, aspect in COVERS:
            dest = COVERS_DIR / f"{name}.jpg"
            if dest.exists():
                print(f"· {name}.jpg exists — skipping (delete to regen)")
                continue
            tasks.append((subject, dest, aspect))

    if not args.covers_only:
        for city, n, cast, scene in SCAM_COMICS:
            dest = SCAMS_DIR / city / f"{n}.jpg"
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                print(f"· {city}/{n}.jpg exists — skipping (delete to regen)")
                continue
            prompt = f"{STYLE_GREECE}\n\nCHARACTER: {cast}\n\nSCENE:\n{scene}"
            tasks.append((prompt, dest, "1:1"))

    print(f"→ Queuing {len(tasks)} generations…")
    ok = 0
    for prompt, dest, aspect in tasks:
        print(f"  → {dest.relative_to(BOOK)} ({aspect})…")
        if generate(api_key, prompt, dest, aspect):
            ok += 1
            size_kb = dest.stat().st_size / 1024
            print(f"  ✓ {dest.name} ({size_kb:.0f} KB)")
    print(f"\nDone: {ok} / {len(tasks)} succeeded")


if __name__ == "__main__":
    main()
