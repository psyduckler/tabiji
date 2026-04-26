#!/usr/bin/env python3
"""Style bake-off — batch 2: Philippines, Tanzania, Jamaica, Switzerland.

Same shape as batch 1. 3 candidates per country × 4 countries = 12 images.

Run: python3 scripts/comic-pipeline/bakeoff_2026_04_26_batch2.py
"""
from __future__ import annotations

import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import (  # noqa: E402
    submit_nbp, poll_nbp, download_verify, upload_r2, _keychain, T2I_EP,
)
from cast import CHARACTERS  # noqa: E402

OUT_DIR = Path("/tmp/bakeoff-2026-04-26-batch2")
OUT_DIR.mkdir(exist_ok=True)

SCENES = {
    "ph": {
        "city": "Manila",
        "character_key": "priya",
        "scene": (
            "SCENE:\n"
            "Panel 1: Priya stands at the Ninoy Aquino International Airport (NAIA) Manila taxi rank, "
            "tropical evening light, her hiking backpack at her feet, as a Filipino taxi driver in a "
            "blue polo shirt loads her bag into a beige sedan. The terminal sign reads 'NAIA TERMINAL "
            "3'. Speech bubble (driver): \"Makati hotel? Four thousand pesos!\"\n"
            "Panel 2: Inside the taxi, Priya looks at her phone showing the Grab app with a ₱280 fare "
            "estimate, while the driver gestures dismissively at the meter. Speech bubble (driver): "
            "\"Meter broken — fixed price four thousand!\"\n"
            "Panel 3: The taxi is parked under bright Manila streetlights; Priya holds her phone up "
            "showing the Grab map and price. Speech bubble (Priya): \"Grab says two hundred eighty.\"\n"
            "Panel 4: Priya climbs into a clearly-marked Grab car (white sedan with Grab logo), calmly "
            "waving off the first taxi. Speech bubble (Priya): \"Always book Grab — never broken meters.\""
        ),
    },
    "tz": {
        "city": "Zanzibar (Stone Town)",
        "character_key": "marcus",
        "scene": (
            "SCENE:\n"
            "Panel 1: Marcus has just stepped off the Dar es Salaam ferry at Zanzibar Stone Town's "
            "harbour, his DSLR around his neck, his rolling suitcase beside him on the dock. A "
            "Tanzanian porter in a green polo grabs the suitcase handle without asking and starts "
            "walking. Speech bubble (porter): \"I take your bag — this way, friend!\"\n"
            "Panel 2: Marcus jogs after the porter through the crowded dockside, past dhow boats and "
            "Stone Town's coral-stone buildings, calling out. Speech bubble (Marcus): \"Hey — wait, I "
            "didn't ask!\"\n"
            "Panel 3: The porter has stopped at the taxi rank twenty meters away with Marcus's bag, "
            "now demanding payment with an outstretched hand. Speech bubble (porter): \"Twenty dollars "
            "service — you pay now!\"\n"
            "Panel 4: Marcus stands by an officially-uniformed porter wearing a Zanzibar Port "
            "Authority ID badge, who is loading his bag into a marked taxi at a respectful distance. "
            "Speech bubble (Marcus): \"Only use ID-badged porters — agree price first.\""
        ),
    },
    "jm": {
        "city": "Montego Bay",
        "character_key": "margie",
        "scene": (
            "SCENE:\n"
            "Panel 1: Margie strolls down Gloucester Avenue (Montego Bay's Hip Strip), tropical "
            "afternoon sun, palm trees and turquoise Caribbean visible behind colorful craft stalls. A "
            "Jamaican vendor in a bright headwrap calls out from a stall doorway. Speech bubble "
            "(vendor): \"Come look — best prices, lady!\"\n"
            "Panel 2: A second vendor steps in front of Margie and gently ties a colorful red-gold-"
            "green braided bracelet onto her wrist. Margie smiles politely, looking uncertain. Speech "
            "bubble (vendor): \"Free gift for a beautiful friend!\"\n"
            "Panel 3: The vendor now holds out a hand demanding payment. A thought bubble over Margie "
            "shows a US ten-dollar bill. Speech bubble (vendor): \"Ten dollars for the bracelet, "
            "darling!\"\n"
            "Panel 4: Margie has politely removed the bracelet and handed it back, walking firmly away "
            "down the Hip Strip with hands tucked in her pockets. Speech bubble (Margie): \"Polite but "
            "firm — keep walking.\""
        ),
    },
    "ch": {
        "city": "Zurich",
        "character_key": "harry",
        "scene": (
            "SCENE:\n"
            "Panel 1: Harry stands in Zurich's Altstadt (old town), cobbled lane with limestone "
            "facades and Grossmünster cathedral spires visible behind, looking puzzled at a man in a "
            "dark suit who is showing him a metallic badge. Speech bubble (man): \"Zurich Police — I "
            "need to inspect your wallet.\"\n"
            "Panel 2: The 'officer' is reaching for Harry's wallet with one hand, holding the badge "
            "in the other. Harry hesitates, his hand on his sling-bag. Speech bubble (officer): "
            "\"Counterfeit-currency check — only takes a moment.\"\n"
            "Panel 3: Harry has stepped back and is dialing 117 (Swiss police emergency) on his "
            "phone, looking firm. The fake officer's expression is uncomfortable. Speech bubble "
            "(Harry): \"I'll call 117 to confirm — please wait.\"\n"
            "Panel 4: Harry stands speaking with two clearly-uniformed real Stadtpolizei Zürich "
            "officers in dark navy uniforms with embroidered Zurich shields. The fake officer is "
            "gone. Speech bubble (Harry): \"Real Swiss police never inspect wallets on the street.\""
        ),
    },
}

CANDIDATES = {
    "ph": [
        ("jeepney-folk-art", (
            "A single illustrated comic book page in the vibrant Filipino jeepney folk-art style — "
            "bold hand-painted decorative panels with rainbow-saturated colors (hot pink, marigold "
            "yellow, sky blue, lime green, fire-engine red, bright cyan), confident black "
            "outline brushwork, ornamental hand-painted Filipino jeepney lettering and decorative "
            "swirls, colorful tassels, mirror-and-chrome accents at panel borders, sun-rays and "
            "religious iconography flourishes, cheerful working-class Filipino visual energy, "
            "Manila urban backgrounds (jeepneys, sari-sari stores, NAIA terminals, Makati "
            "skyline). Showing four sequential panels arranged in a 2x2 grid with small numbers "
            "1, 2, 3, 4 in the upper-left corner of each panel, separated by decorative jeepney-"
            "style ornamental borders. Each panel contains one clean white rounded speech bubble "
            "with a small pointer tail, holding short printed English dialogue in simple black "
            "comic lettering — text must be legible, in English only, and correctly spelled. "
            "Square 1:1 composition, 2K resolution."
        )),
        ("bencab-figurative", (
            "A single illustrated comic book page in the contemporary Filipino figurative style "
            "of Benedicto 'BenCab' Cabrera — confident dark ink-and-charcoal linework with "
            "expressive hand-drawn shading, muted earth-tone palette of warm sepia, ochre, deep "
            "indigo, cream, and accents of crimson, sensitive humanist rendering of Filipino "
            "everyday people, restrained painterly tone, refined Filipino contemporary-art "
            "sensibility, Manila urban-tropical backgrounds (NAIA terminal, palm-fringed taxi "
            "rank, Makati high-rises in the distance). Showing four sequential panels arranged in "
            "a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
            "separated by thin black panel borders with narrow cream gutters. Each panel contains "
            "one clean white rounded speech bubble with a small pointer tail, holding short "
            "printed English dialogue in simple black lettering — text must be legible, in "
            "English only, and correctly spelled. Square 1:1 composition, 2K resolution."
        )),
        ("kenkoy-pinoy-komiks", (
            "A single illustrated comic book page in the classic 1930s-50s Filipino 'Kenkoy' "
            "Pinoy-komiks style of Tony Velasquez and the golden age of Filipino comic books — "
            "clean confident black ink outlines with halftone dot shading and occasional "
            "cross-hatching, warm cream newsprint paper background, simplified expressive cartoon "
            "faces with big eyes and slapstick gestures, bold flat color fills in classic four-"
            "color Filipino-komiks palette (red, blue, yellow, black on cream), classic Filipino "
            "humor-comic narrative pacing, Manila tropical-urban setting (street vendors, "
            "jeepney silhouettes, palm trees, NAIA airport). Showing four sequential panels "
            "arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of "
            "each panel, separated by thin black panel borders with narrow cream gutters. Each "
            "panel contains one clean white rectangular speech bubble with a small pointer tail, "
            "holding short printed English dialogue in classic comic-book hand-lettering — text "
            "must be legible, in English only, and correctly spelled. Square 1:1 composition, "
            "2K resolution."
        )),
    ],
    "tz": [
        ("tingatinga", (
            "A single illustrated comic book page in the Tanzanian Tingatinga folk-painting style "
            "of Edward Saidi Tingatinga (Dar es Salaam, mid-20th century) — bold flat saturated "
            "color blocks with confident black outline drawing, classic Tingatinga palette "
            "(intense yellow, electric blue, vermillion red, emerald green, deep black "
            "background), stylized naive figures and animals (giraffes, elephants, dhow boats) "
            "as decorative motifs, repeating decorative pattern fills, distinctively flat "
            "perspective, vibrant East African folk-painting energy. Showing four sequential "
            "panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left "
            "corner of each panel, separated by thin black panel borders with narrow cream "
            "gutters. Each panel contains one clean white rounded speech bubble with a small "
            "pointer tail, holding short printed English dialogue in simple black lettering — "
            "text must be legible, in English only, and correctly spelled. Square 1:1 "
            "composition, 2K resolution."
        )),
        ("zanzibar-swahili-coastal", (
            "A single illustrated comic book page in a warm Zanzibar Swahili-coast travel-"
            "illustration style — confident fine black ink linework with rich watercolor washes, "
            "warm coastal palette of coral-stone cream, deep Indian Ocean turquoise, palm "
            "green, sunset orange, and saffron, detailed Stone Town backgrounds (carved-wood "
            "Zanzibari doors with brass studs, coral-stone facades with hanging laundry, dhow "
            "sailing boats with triangular sails, palm-fringed harbour, narrow Swahili alleys), "
            "Tanzanian figures in vibrant kanga and kitenge fabrics alongside modern travelers, "
            "warm equatorial sunlight. Showing four sequential panels arranged in a 2x2 grid "
            "with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by "
            "thin black panel borders with narrow cream gutters. Each panel contains one clean "
            "white rounded speech bubble with a small pointer tail, holding short printed "
            "English dialogue in simple black comic lettering — text must be legible, in "
            "English only, and correctly spelled. Square 1:1 composition, 2K resolution."
        )),
        ("east-african-modern", (
            "A single illustrated comic book page in a contemporary East African illustrated "
            "travel-comic style with kanga-textile pattern accents at panel corners — confident "
            "fine black ink outlines with painterly gouache fills, warm African palette of "
            "terracotta, ochre, baobab brown, savanna gold, deep cobalt, and accent kanga-red, "
            "decorative kanga-textile geometric and floral pattern flourishes at panel corners "
            "(no figurative ornament), Tanzanian location backgrounds (Stone Town coral-stone "
            "facades, dhow harbour, palm-lined streets, ferry terminal, official porter ID-"
            "badge stations), modern-realistic figure rendering, Tanzanian figures in everyday "
            "modern dress with occasional kanga and kitenge accents. Showing four sequential "
            "panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left "
            "corner of each panel, separated by thin black panel borders with narrow cream "
            "gutters. Each panel contains one clean white rounded speech bubble with a small "
            "pointer tail, holding short printed English dialogue in simple black comic "
            "lettering — text must be legible, in English only, and correctly spelled. Square "
            "1:1 composition, 2K resolution."
        )),
    ],
    "jm": [
        ("reggae-poster-1970s", (
            "A single illustrated comic book page in the 1970s Jamaican reggae album-cover / "
            "Bob Marley poster aesthetic — bold hand-painted figures with confident black "
            "outline, saturated Rastafari palette (deep red, gold-yellow, forest-green, "
            "black, plus tropical turquoise and palm-leaf green), sun-drenched Caribbean "
            "warmth, retro 1970s reggae visual vocabulary (palm fronds, sun-rays, mountains, "
            "dreadlock silhouettes, hand-painted poster lettering), Montego Bay coastal "
            "backgrounds (Hip Strip palm-lined avenue, turquoise Caribbean, craft-market "
            "stalls, colonial colorful storefronts), warm Jamaican sun. Showing four "
            "sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the "
            "upper-left corner of each panel, separated by thin black panel borders with "
            "narrow cream gutters. Each panel contains one clean white rounded speech "
            "bubble with a small pointer tail, holding short printed English dialogue in "
            "simple black comic lettering — text must be legible, in English only, and "
            "correctly spelled. Square 1:1 composition, 2K resolution."
        )),
        ("jamaican-mural-dancehall", (
            "A single illustrated comic book page in the bold contemporary Jamaican street-"
            "mural / dancehall-poster style — confident hand-painted shapes with thick "
            "black outlines, vibrant Caribbean palette (electric pink, neon yellow, hot "
            "turquoise, lime green, deep red, royal purple), graffiti-inflected hand-"
            "lettering, energetic dancehall-poster composition with characters leaning "
            "into the frame, decorative tropical-flora flourishes (hibiscus, palm fronds), "
            "Montego Bay coastal-urban backdrops (Hip Strip storefronts, Caribbean ocean, "
            "craft-market awnings), brash confident dancehall energy. Showing four "
            "sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in "
            "the upper-left corner of each panel, separated by thin black panel borders "
            "with narrow cream gutters. Each panel contains one clean white rounded "
            "speech bubble with a small pointer tail, holding short printed English "
            "dialogue in simple black comic lettering — text must be legible, in English "
            "only, and correctly spelled. Square 1:1 composition, 2K resolution."
        )),
        ("caribbean-storybook-watercolor", (
            "A single illustrated comic book page in a warm Caribbean storybook-watercolor "
            "illustration style — soft pencil linework with light watercolor washes, sun-"
            "drenched palette of cream, turquoise sea, sand gold, palm green, hibiscus "
            "pink, and warm coral, friendly cartoon character figures with simple expressive "
            "faces, detailed Jamaican location backgrounds (Hip Strip palm-lined avenue, "
            "colorful colonial storefronts, craft-market stalls with hanging textiles, "
            "Caribbean turquoise water in the distance, Doctor's Cave Beach), Jamaican "
            "vendors in colorful dress alongside travelers, warm tropical afternoon "
            "light. Showing four sequential panels arranged in a 2x2 grid with small "
            "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by "
            "thin black panel borders with narrow cream gutters. Each panel contains one "
            "clean white rounded speech bubble with a small pointer tail, holding short "
            "printed English dialogue in simple black comic lettering — text must be "
            "legible, in English only, and correctly spelled. Square 1:1 composition, "
            "2K resolution."
        )),
    ],
    "ch": [
        ("alpine-bauernmalerei", (
            "A single illustrated comic book page in the traditional Swiss alpine "
            "Bauernmalerei (peasant-painting) folk-art style — decorative hand-painted "
            "panels in classic alpine palette (cream paper background, alpine red, "
            "leaf green, sky blue, sunflower yellow, deep umber), folk-art Sennen-"
            "Streifen procession decorative borders with stylized cattle, pine trees, "
            "and Edelweiss flowers framing each panel, naive flat perspective, careful "
            "hand-painted decorative ornament filling negative space, characteristic "
            "Swiss alpine farmhouse-art warmth, Zurich Altstadt cobbled-lane backdrops "
            "with Grossmünster spires. Showing four sequential panels arranged in a 2x2 "
            "grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
            "separated by Bauernmalerei-style decorative borders. Each panel contains "
            "one clean white rounded speech bubble with a small pointer tail, holding "
            "short printed English dialogue in simple black lettering — text must be "
            "legible, in English only, and correctly spelled. Square 1:1 composition, "
            "2K resolution."
        )),
        ("swiss-modernist-grid", (
            "A single illustrated comic book page in the Swiss modernist design style of "
            "Josef Müller-Brockmann and the 1950s-60s Swiss International Typographic "
            "Style — clean precise geometric linework, restrained palette of pure white, "
            "deep black, single accent of Swiss-flag red and crisp ink-blue, perfect "
            "modernist grid composition with generous white space, Helvetica-style sans-"
            "serif typography, minimalist flat figure rendering with confident geometric "
            "shapes, Zurich Altstadt and Bahnhofstrasse rendered as clean architectural "
            "silhouettes, Swiss design's signature objectivity and clarity. Showing four "
            "sequential panels arranged in a perfect 2x2 grid with bold sans-serif "
            "numerals 1, 2, 3, 4 in the upper-left corner of each panel, separated by "
            "thin sharp black panel borders with narrow white gutters. Each panel contains "
            "one clean white rectangular speech bubble (no rounded corners) with a small "
            "pointer tail, holding short printed English dialogue in clean Helvetica-"
            "style sans-serif lettering — text must be legible, in English only, and "
            "correctly spelled. Square 1:1 composition, 2K resolution."
        )),
        ("anker-genre-painting", (
            "A single illustrated comic book page in the warm 19th-century Swiss genre-"
            "painting style of Albert Anker — sensitive realistic oil-painting rendering "
            "of everyday people, warm restrained palette of cream, soft ochre, dusty "
            "rose, slate blue, and umber, careful painterly observation of light and "
            "fabric, dignified humanist tone, detailed Swiss Altstadt architectural "
            "backgrounds (cobbled lanes, limestone facades, Grossmünster spires, "
            "Bahnhofstrasse storefronts), Swiss figures in restrained modern dress "
            "alongside travelers, the quiet moral seriousness of 19th-century Swiss "
            "academic painting. Showing four sequential panels arranged in a 2x2 grid "
            "with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
            "separated by thin black panel borders with narrow cream gutters. Each panel "
            "contains one clean white rounded speech bubble with a small pointer tail, "
            "holding short printed English dialogue in simple black comic lettering — "
            "text must be legible, in English only, and correctly spelled. Square 1:1 "
            "composition, 2K resolution."
        )),
    ],
}


def build_prompt(cc: str, style_block: str) -> str:
    scene = SCENES[cc]
    char = CHARACTERS[scene["character_key"]]
    return f"{style_block}\n\nCHARACTER: {char}\n\n{scene['scene']}"


def generate_one(cc: str, slug: str, prompt: str, ws: str, r2: str) -> tuple[str, str]:
    body = {"prompt": prompt, "aspect_ratio": "1:1", "resolution": "2k", "output_format": "jpeg"}
    tid = submit_nbp(body, T2I_EP, ws)
    if not tid:
        return slug, "FAIL: submit"
    raw_url = poll_nbp(tid, ws, timeout=600)
    if not raw_url:
        return slug, "FAIL: poll"
    out = OUT_DIR / f"{cc}-{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return slug, f"FAIL: dl {note}"
    r2_key = f"scam-comics/{cc}/style-tests/{slug}.jpg"
    if not upload_r2(out, r2_key, r2):
        return slug, "FAIL: r2"
    return slug, f"https://img.tabiji.ai/{r2_key}"


def main():
    ws = _keychain("wavespeed-api-key")
    r2 = _keychain("cloudflare-api-token")
    if not ws or not r2:
        print("ERROR: missing creds in keychain")
        sys.exit(1)

    jobs = []
    for cc, candidates in CANDIDATES.items():
        for slug, style_block in candidates:
            prompt = build_prompt(cc, style_block)
            jobs.append((cc, slug, prompt))

    print(f"Submitting {len(jobs)} bake-off generations...")
    results: dict[str, dict[str, str]] = {cc: {} for cc in CANDIDATES}
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(generate_one, cc, slug, prompt, ws, r2): (cc, slug)
                for cc, slug, prompt in jobs}
        for fut in as_completed(futs):
            cc, slug = futs[fut]
            try:
                _, result = fut.result()
            except Exception as e:
                result = f"FAIL: {e}"
            results[cc][slug] = result
            print(f"  {cc}/{slug}: {result}")

    print("\n=== RESULTS ===")
    for cc in CANDIDATES:
        print(f"\n{cc.upper()} ({SCENES[cc]['city']}):")
        for slug, _ in CANDIDATES[cc]:
            url = results[cc].get(slug, "missing")
            print(f"  {slug}: {url}")


if __name__ == "__main__":
    main()
