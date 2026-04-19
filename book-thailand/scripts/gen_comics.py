#!/usr/bin/env python3
"""
Generate the Thailand book comic assets via Wavespeed (Nano Banana Pro):
 - front cover (single dramatic panel, 2:3 aspect)
 - back cover (single scene with empty upper third for text overlay, 2:3)
 - 20 missing per-scam comics (2x2 grid watercolor-storybook, 1:1) for
   Ayutthaya / Hua Hin / Koh Tao / Koh Phi Phi.

Style is anchored to the existing Bangkok / Chiang Mai / etc. scam comics
on R2: watercolor storybook, pastel palette, soft hand-painted lines,
English speech bubbles, numbered panels in circles (1-4).

Usage:
    python3 book-thailand/scripts/gen_comics.py              # all assets
    python3 book-thailand/scripts/gen_comics.py --covers-only
    python3 book-thailand/scripts/gen_comics.py --scams-only
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


STYLE_COMIC = (
    "Watercolor-storybook illustration in soft hand-painted lines, pastel "
    "palette with cream and sage-green background, gentle shading. Matches a "
    "travel-safety book interior illustration style. English text in speech "
    "bubbles must be clear, grammatically correct, and legible. No logos, "
    "no watermarks, no signatures."
)

STYLE_2X2 = (
    "Four-panel 2x2 comic grid. Each panel is a clean square with a thin "
    "off-white gutter between panels. Panels numbered 1-4 in small circles "
    "in the corner of each panel. "
)

# --- COVER PROMPTS --------------------------------------------------------

COVERS = [
    (
        "front",
        (
            "A single dramatic watercolor-storybook scene, portrait 2:3 "
            "aspect, depicting a Thailand tourist scam in action: a female "
            "tourist wearing a sun hat stands in front of the Grand Palace "
            "ornate golden gates, looking slightly worried, while a friendly "
            "smiling Thai man in a white polo shirt with an ID lanyard points "
            "at the gate and says 'Palace closed today for royal ceremony!' "
            "in a white speech bubble. A red-and-white tuk-tuk waits in the "
            "middle distance with its driver waving. Sky is warm peachy "
            "golden-hour. Composition leaves generous empty sky in the upper "
            "third of the frame for a book-cover title to be overlaid. "
            "No book title, no watermark, no logo — just the illustration. "
        ),
        "2:3",
    ),
    (
        "back",
        (
            "A single watercolor-storybook scene, portrait 2:3 aspect, "
            "depicting a bustling Thai night market from a three-quarter "
            "overhead view: street food stalls with hanging lanterns, tuk-tuks "
            "passing in the distance, a temple silhouette against the twilight "
            "sky, and a small group of tourists walking among the crowd. "
            "Composition is atmospheric and calm, with substantial empty dark-"
            "teal sky in the upper two-thirds of the frame to leave space for "
            "back-cover copy to be overlaid. Palette: pastel watercolor, warm "
            "lantern glow, hints of saffron and sage. No text, no watermark, "
            "no book title. "
        ),
        "2:3",
    ),
]


# --- MISSING SCAM COMICS --------------------------------------------------
# Four cities had no comics on R2. Prompts below are scam-specific and follow
# the existing cast convention (Margie / Priya / Harry / Marcus) — we rotate
# fairly and pick the protagonist closest to the scam demographic.

# Each prompt describes a 4-panel arc with dialogue. The watercolor style and
# 2x2 grid are appended by the formatter.

SCAM_COMICS: list[tuple[str, int, str]] = [
    # AYUTTHAYA (5 scams)
    ("ayutthaya", 1,
     "Panel 1: A female tourist in a sun hat arrives at Ayutthaya Historical "
     "Park entrance; a smiling man in a fake uniform says 'Foreign price: 500 "
     "baht per temple!' Panel 2: She looks confused, pointing at the official "
     "sign that reads 'Wat Mahathat admission: 50 baht'. Panel 3: The man is "
     "walking away quickly; her friend in the background says 'That's a "
     "scam!' Panel 4: The tourist is at a real park ticket booth paying 50 "
     "baht, smiling."),
    ("ayutthaya", 2,
     "Panel 1: A female tourist near Wat Phra Si Sanphet in Ayutthaya; a "
     "young Thai man on a motorbike says 'Private guided tour of all temples, "
     "only 200 baht!' Panel 2: They ride through the park, passing major "
     "temples without stopping. Panel 3: The bike pulls up at a gem shop; the "
     "man says 'Special stop — best prices!' Panel 4: Tourist frowning, "
     "thinking 'That wasn't a temple tour at all.'"),
    ("ayutthaya", 3,
     "Panel 1: A couple of tourists asking a tuk-tuk driver how much to see "
     "the ruins; driver says '800 baht, very cheap!' Panel 2: Nearby sign "
     "shows '200 baht standard rate for Ayutthaya tuk-tuk day rental.' "
     "Panel 3: The tourists walk away; driver shouts 'Okay okay 250!' "
     "Panel 4: They ride off happily at the fair rate, driver smiles."),
    ("ayutthaya", 4,
     "Panel 1: A male tourist with a backpack at Ayutthaya train station; a "
     "local offers 'I rent you bicycle, 300 baht one day.' Panel 2: Tourist "
     "pedals around the park, a wheel wobbles. Panel 3: Returning, the "
     "renter demands '2000 baht! You broke it!' Panel 4: Tourist showing a "
     "pre-rental photo of the bike on his phone: 'Already wobbly when I "
     "took it.'"),
    ("ayutthaya", 5,
     "Panel 1: A tourist buying a bottle of water from a vendor near Wat "
     "Chaiwatthanaram; vendor charges '100 baht.' Panel 2: Tourist looking "
     "at a nearby 7-Eleven sign showing water at 15 baht. Panel 3: Tourist "
     "politely declining and walking to the 7-Eleven. Panel 4: Tourist "
     "smiling, drinking water from the 7-Eleven, having saved 85 baht."),

    # HUA HIN (5 scams)
    ("hua-hin", 1,
     "Panel 1: A male tourist on Hua Hin beach; a smiling jet-ski operator "
     "says 'Jet ski rental, 2000 baht one hour!' Panel 2: Tourist riding the "
     "jet ski happily on the water. Panel 3: On return, the operator points "
     "at a pre-existing scratch and shouts '20,000 baht damage!' Panel 4: "
     "Tourist showing a time-stamped phone photo of the scratch from "
     "before the ride."),
    ("hua-hin", 2,
     "Panel 1: A female tourist at Hua Hin Railway Station; a taxi driver "
     "says '500 baht to your hotel.' Panel 2: A Grab-taxi app on her phone "
     "shows the fare is 120 baht. Panel 3: She declines and walks 50 meters "
     "to the Grab pickup point. Panel 4: Smiling in the Grab car, paying the "
     "metered fare."),
    ("hua-hin", 3,
     "Panel 1: A couple walking the Hua Hin night market; a vendor pulls them "
     "to a jewelry stall saying 'Special discount, just for you!' Panel 2: "
     "A ring being held up, the vendor says 'Real gold, 8000 baht!' Panel 3: "
     "The tourist scratches the surface with a coin; the gold-colored paint "
     "flakes off. Panel 4: Walking away empty-handed, vendor looking "
     "embarrassed."),
    ("hua-hin", 4,
     "Panel 1: A tourist at Hua Hin Beach; a beach chair vendor says '200 "
     "baht per chair, all day!' Panel 2: Tourist settles in with a book. "
     "Panel 3: At sunset the vendor returns: '800 baht! You were here five "
     "hours!' Panel 4: Tourist showing a written receipt for 200 baht; "
     "vendor reluctantly accepts."),
    ("hua-hin", 5,
     "Panel 1: A male tourist at a Hua Hin seafood restaurant studying the "
     "menu: prawns '200 baht per 100g.' Panel 2: The tourist asks for 'one "
     "plate of prawns.' Panel 3: The bill arrives with '1500 grams of "
     "prawns, 3000 baht.' Panel 4: Tourist pointing at the menu, asking the "
     "kitchen to show the scale and the actual weight."),

    # KOH TAO (5 scams)
    ("koh-tao", 1,
     "Panel 1: Two tourists at a Koh Tao dive shop; instructor says 'Open "
     "Water certification, 8000 baht.' Panel 2: On the pier, they're told "
     "'Rental equipment extra, 2000 baht per day.' Panel 3: After the course, "
     "the certification card never arrives. Panel 4: Tourists researching "
     "PADI online: 'Book only with shops listed on padi.com.'"),
    ("koh-tao", 2,
     "Panel 1: A male tourist rents a motorbike at Koh Tao; owner says '300 "
     "baht per day, easy!' Panel 2: Tourist hands over his passport as "
     "'deposit.' Panel 3: On return, a small scratch is pointed out: "
     "'15,000 baht to fix!' Panel 4: Tourist refusing, calling Tourist "
     "Police 1155 from his phone."),
    ("koh-tao", 3,
     "Panel 1: A female tourist on Sairee Beach; a beach-boy masseuse offers "
     "'Thai massage on the beach, 400 baht.' Panel 2: After the massage, "
     "'Tip is separate, 300 baht.' Panel 3: Tourist politely: 'No thank you, "
     "400 was the total.' Panel 4: She walks off to her bungalow, massage "
     "paid, no tip forced."),
    ("koh-tao", 4,
     "Panel 1: A couple at the Mae Haad pier buying ferry tickets; seller "
     "says '1200 baht each for Koh Phangan.' Panel 2: Sign above the booth "
     "reads 'Lomprayah ferry: 600 baht.' Panel 3: The couple turns to the "
     "Lomprayah counter a few meters away. Panel 4: Boarding the real ferry "
     "at the official price."),
    ("koh-tao", 5,
     "Panel 1: A tourist at a Koh Tao convenience store; the clerk rings "
     "up water, sunscreen, and snacks at '500 baht.' Panel 2: Tourist pays "
     "with a 1000-baht note, gets 300 back. Panel 3: Checking the receipt: "
     "total was 480, change should have been 520. Panel 4: Tourist pointing "
     "at receipt; clerk hands over the correct 220 baht with an apology."),

    # KOH PHI PHI (5 scams)
    ("koh-phi-phi", 1,
     "Panel 1: A female tourist at Tonsai pier arriving on Koh Phi Phi; a "
     "longtail boat driver offers 'Maya Bay tour, 2000 baht, just you!' "
     "Panel 2: Sign nearby reads 'Group Maya Bay tour: 600 baht, includes "
     "national park fee.' Panel 3: Tourist politely declining and heading to "
     "the tour-agent booth. Panel 4: Boarding the group tour, smiling at "
     "the much better price."),
    ("koh-phi-phi", 2,
     "Panel 1: A male tourist at a Koh Phi Phi bar; bartender says 'Happy "
     "hour buckets, 150 baht each!' Panel 2: The tab after four buckets "
     "arrives: '1800 baht.' Panel 3: Tourist asking for an itemized receipt. "
     "Panel 4: Bartender sheepishly correcting to 600 baht."),
    ("koh-phi-phi", 3,
     "Panel 1: Two tourists renting snorkeling gear; shop says '300 baht per "
     "set, deposit 3000 baht.' Panel 2: They return at sunset; shop insists "
     "'Mask strap broken, deposit kept.' Panel 3: Tourist showing a "
     "time-stamped rental photo on her phone. Panel 4: Shop returning the "
     "full deposit, promising 'sorry, mistake.'"),
    ("koh-phi-phi", 4,
     "Panel 1: A tourist at a Koh Phi Phi beach restaurant studying the "
     "menu; waiter says 'Fresh fish, 200 baht per 100g.' Panel 2: Tourist "
     "ordering a whole fish 'maybe half a kilo.' Panel 3: The bill arrives "
     "as '1.8 kg of fish, 3600 baht.' Panel 4: Tourist asking the kitchen "
     "to weigh the fish bones on a visible scale."),
    ("koh-phi-phi", 5,
     "Panel 1: A couple on Long Beach; a local with a camera offers 'Photos "
     "with parrots, 100 baht!' Panel 2: They pose; the local now adds "
     "'Each photo is 100 — that's seven photos, 700 baht!' Panel 3: Couple "
     "politely disputing: 'We agreed to 100 for the session.' Panel 4: "
     "They pay 100 and walk off, the local moves on to another tourist."),
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
            prompt = f"{subject}\n\n{STYLE_COMIC}"
            tasks.append((prompt, dest, aspect))

    if not args.covers_only:
        for city, n, subject in SCAM_COMICS:
            dest = SCAMS_DIR / city / f"{n}.jpg"
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                print(f"· {city}/{n}.jpg exists — skipping (delete to regen)")
                continue
            prompt = (
                f"{STYLE_2X2}"
                f"Scene: {subject}\n\n{STYLE_COMIC}"
            )
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
