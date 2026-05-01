#!/usr/bin/env python3
"""Style bake-off — batch 1: India, Morocco, Egypt, Saudi Arabia.

For each country: 3 culturally-distinct style candidates, anchored on the same
4-panel scene. Submits each via Nano Banana Pro text-to-image (no anchor),
uploads to R2 at scam-comics/<cc>/style-tests/<slug>.jpg.

Run: python3 scripts/comic-pipeline/bakeoff_2026_04_26.py
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

OUT_DIR = Path("/tmp/bakeoff-2026-04-26")
OUT_DIR.mkdir(exist_ok=True)

# --------- Per-country scene blocks (one bespoke 4-panel scene per country) ---------

SCENES = {
    "in": {
        "city": "Delhi",
        "character_key": "margie",
        "scene": (
            "SCENE:\n"
            "Panel 1: Margie has just stepped off a long-distance train at New Delhi Railway Station, "
            "standing on a crowded platform with her wheeled suitcase, looking lost as a man in a neat "
            "polo shirt approaches with a friendly smile. The platform sign reads 'NEW DELHI / नई दिल्ली'. "
            "Speech bubble: \"Need help finding your hotel?\"\n"
            "Panel 2: The man leads Margie outside through the chaotic Paharganj market crowds toward "
            "a professional-looking storefront with a hand-painted 'INDIA TOURISM' sign and maps in the "
            "window. He gestures grandly. Speech bubble (man): \"My office — official Delhi Tourism!\"\n"
            "Panel 3: Inside the fake office, a 'tour operator' behind a desk pushes a printed itinerary "
            "across to Margie. The price reads ₹85,000. Margie's eyes are wide with shock; a thought "
            "bubble shows the official India Tourism logo with a red X over the fake sign. Speech bubble "
            "(operator): \"Book today — last room in Agra!\"\n"
            "Panel 4: Margie stands outside the actual government India Tourism office (a clean modern "
            "building on Janpath with the official emblem), confidently walking away from the fake one. "
            "Speech bubble: \"I'll book through the real Tourism office.\""
        ),
    },
    "ma": {
        "city": "Marrakech",
        "character_key": "harry",
        "scene": (
            "SCENE:\n"
            "Panel 1: Harry stands at the bustling edge of Djemaa el-Fna square in Marrakech, golden "
            "afternoon light falling on the Koutoubia minaret in the distance. He's holding a paper map "
            "and looking puzzled at a medina alley entrance when a friendly Moroccan man taps his "
            "shoulder. Speech bubble (man): \"Sorry friend — that street, closed for festival!\"\n"
            "Panel 2: The man leads Harry through twisting narrow medina alleys with colorful spice "
            "stalls, copper lanterns, and glimpses of high pink walls overhead. Harry follows trustingly, "
            "the man chatting cheerfully. Speech bubble (man): \"This way much better — I show you!\"\n"
            "Panel 3: They arrive in a small carpet shop crammed with stacked Berber rugs in jewel tones. "
            "The 'guide' is now demanding payment with an outstretched hand; the shopkeeper waits in the "
            "background. A thought bubble over Harry's head shows a Moroccan dirham banknote with '200' "
            "on it. Speech bubble (guide): \"Two hundred dirhams — for my time, friend!\"\n"
            "Panel 4: Harry has firmly declined and is walking back toward Djemaa el-Fna with his phone "
            "out, navigating by maps.me. Speech bubble: \"No thanks — I'll use my own map.\""
        ),
    },
    "eg": {
        "city": "Cairo (Giza)",
        "character_key": "marcus",
        "scene": (
            "SCENE:\n"
            "Panel 1: Marcus stands on the sandy Giza plateau in front of the Pyramid of Khafre and the "
            "Sphinx, his DSLR around his neck, looking at a smiling camel handler in a brown galabeya "
            "robe leading a kneeling camel decorated with bright red and orange tassels. Speech bubble "
            "(handler): \"Quick photo ride — only 50 pounds!\"\n"
            "Panel 2: Marcus has climbed onto the camel's back; the handler urges the camel to stand and "
            "it rises tall. Marcus grips the saddle horn looking nervous, four meters off the ground "
            "with the pyramids towering behind. The handler holds the lead rope tightly. Speech bubble "
            "(handler): \"Now 500 pounds for ride down!\"\n"
            "Panel 3: Marcus is still trapped on the standing camel, gesturing toward the Tourist Police "
            "kiosk visible in the middle distance. The handler smirks, refusing to make the camel kneel. "
            "Speech bubble (Marcus): \"Tourist Police! Right there!\"\n"
            "Panel 4: Marcus stands safely on the ground next to a uniformed Egyptian Tourist Police "
            "officer who is firmly admonishing the camel handler. Marcus's bag and camera are intact. "
            "Speech bubble (Marcus): \"Negotiate the price BEFORE you mount.\""
        ),
    },
    "sa": {
        "city": "Riyadh",
        "character_key": "priya",
        "scene": (
            "SCENE:\n"
            "Panel 1: Priya stands at the King Khalid International Airport taxi rank in Riyadh, late "
            "afternoon, her hiking backpack at her feet, as a taxi driver in a white thobe loads her bag "
            "into the trunk of a beige sedan. Speech bubble (driver): \"To your hotel — meter is broken.\"\n"
            "Panel 2: Inside the taxi, Priya looks at her smartphone showing the Careem app with a "
            "₹50 SAR fare estimate, while the driver gestures dismissively at the meter. Speech bubble "
            "(driver): \"Fixed price 150 — meter no good!\"\n"
            "Panel 3: The taxi is driving through Riyadh's brightly lit streets at night past the "
            "Kingdom Tower silhouette; Priya holds her phone up showing the Careem map with the route. "
            "Speech bubble (Priya): \"Careem says fifty riyals.\"\n"
            "Panel 4: Priya climbs into a clearly-marked Careem rideshare car, calmly waving off the "
            "first taxi. Speech bubble (Priya): \"Always use the app — never broken meters.\""
        ),
    },
}

# --------- Per-country 3 style blocks (the bake-off candidates) ---------

CANDIDATES = {
    "in": [
        ("mughal-miniature", (
            "A single illustrated comic book page in the classical Mughal miniature painting style of "
            "the Akbar/Jahangir court ateliers — meticulous fine black-ink outline drawing with bright "
            "opaque jewel-tone gouache fills (deep crimson, peacock-blue, emerald, saffron yellow, "
            "lapis blue, gold leaf accents), classical Indian profile poses with elongated almond eyes "
            "and refined gestures, intricately patterned textiles and architectural detail (Mughal red "
            "sandstone arches, jharokha balconies, marble inlay), decorative geometric and floral "
            "borders framing each panel in red and gold, ornate calligraphic flourishes, courtly "
            "Indo-Islamic painting tradition. Showing four sequential panels arranged in a 2x2 grid "
            "with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin "
            "gold borders with cream gutters. Each panel contains one clean white rounded speech "
            "bubble with a small pointer tail, holding short printed English dialogue in simple black "
            "lettering — text must be legible, in English only, and correctly spelled. Square 1:1 "
            "composition, 2K resolution."
        )),
        ("madhubani-folk", (
            "A single illustrated comic book page in the Madhubani / Mithila folk-painting style of "
            "rural Bihar, India — bold confident black ink double-line outlines on cream paper, flat "
            "saturated color blocks of deep red, mustard yellow, emerald green, indigo blue, and "
            "vermillion, intricate decorative pattern fills (fish, peacocks, lotus blossoms, mandala "
            "rosettes, geometric chevrons) packed into every background space, stylized figures with "
            "large almond eyes and front-facing simplified faces, characteristic doubled-outline "
            "linework, no shading or gradient, vibrant ceremonial folk-painting energy. Showing four "
            "sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left "
            "corner of each panel, separated by thin black borders with narrow cream gutters. Each "
            "panel contains one clean white rounded speech bubble with a small pointer tail, holding "
            "short printed English dialogue in simple black lettering — text must be legible, in "
            "English only, and correctly spelled. Square 1:1 composition, 2K resolution."
        )),
        ("bollywood-poster", (
            "A single illustrated comic book page in the painted 1970s-80s Bollywood Hindi-cinema "
            "poster style — bold hand-painted gouache figures with melodramatic expressive faces, "
            "saturated cinema palette (vivid red, royal blue, mustard yellow, magenta, kohl black), "
            "dramatic dynamic compositions with characters leaning into the frame, retro Indian "
            "movie-poster typography in stylized Devanagari-and-Latin lettering, painted Bombay "
            "cinema-poster brushwork with visible texture, urban Indian backgrounds (Delhi street "
            "scenes, autorickshaws, neon hotel signs), warm sun-drenched palette. Showing four "
            "sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left "
            "corner of each panel, separated by thin black panel borders with narrow cream gutters. "
            "Each panel contains one clean white rounded speech bubble with a small pointer tail, "
            "holding short printed English dialogue in simple black comic lettering — text must be "
            "legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution."
        )),
    ],
    "ma": [
        ("zellige-tile-border", (
            "A single illustrated comic book page framed inside an ornate Moroccan zellige tile "
            "border — rich decorative geometric mosaic rim in cobalt blue, emerald green, saffron "
            "yellow, terracotta, and white, with stylized eight-pointed-star and arabesque motifs "
            "drawn as flat tile-shapes. Interior of each panel rendered in a warm hand-painted "
            "Moroccan illustration style: confident black ink outlines with rich gouache fills, warm "
            "palette of terracotta pink, ochre, deep cobalt, mint, and saffron, detailed Marrakech "
            "medina backgrounds (Djemaa el-Fna minaret silhouettes, copper lantern stalls, narrow "
            "medina alleys, carpet souks, riad courtyards with tile fountains), Moroccan figures in "
            "djellabas and babouches, traveler figures in modern clothing, warm North African "
            "afternoon light. Showing four sequential panels arranged in a 2x2 grid with small "
            "numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin cream "
            "gutters inside the tiled border. Each panel contains one clean white rounded speech "
            "bubble with a small pointer tail, holding short printed English dialogue in simple "
            "black comic lettering — text must be legible, in English only, and correctly spelled. "
            "Square 1:1 composition, 2K resolution."
        )),
        ("matisse-tangier-watercolor", (
            "A single illustrated comic book page in the loose vibrant watercolor style of "
            "Matisse's 1912 Tangier paintings — bold expressive brushed shapes with confident dark "
            "ink contour drawing, saturated North African palette (Moroccan blue, terracotta orange, "
            "moss green, deep magenta, warm cream, gold), painterly watercolor washes with visible "
            "edges and bleeding pigment, simplified flattened forms with decorative pattern, sun-"
            "drenched Moroccan light, Marrakech medina backdrops (Koutoubia minaret, ochre walls, "
            "souks with hanging textiles, palm-shaded courtyards), modern fauve-influenced "
            "color-as-emotion approach. Showing four sequential panels arranged in a 2x2 grid with "
            "small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin "
            "black panel borders with narrow cream gutters. Each panel contains one clean white "
            "rounded speech bubble with a small pointer tail, holding short printed English "
            "dialogue in simple black comic lettering — text must be legible, in English only, and "
            "correctly spelled. Square 1:1 composition, 2K resolution."
        )),
        ("hassan-hajjaj-pop", (
            "A single illustrated comic book page in the contemporary Moroccan pop-art style of "
            "Hassan Hajjaj — vibrant photo-realistic-leaning portraiture with saturated bold colors "
            "and confident black ink lines, decorative pattern frames around each panel built from "
            "Moroccan consumer-product motifs (aluminum tea-glass patterns, mint-tea-box graphics, "
            "stylized tagine outlines, Moroccan harissa-tin labels, cobalt-and-yellow tile riffs), "
            "saturated palette of cobalt blue, mint green, hot magenta, marigold yellow, and "
            "candy-stripe red, contemporary streetwear-meets-djellaba fashion sensibility, "
            "Marrakech medina backdrops, modern Moroccan-pop irreverent energy. Showing four "
            "sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-"
            "left corner of each panel, separated by patterned decorative borders. Each panel "
            "contains one clean white rounded speech bubble with a small pointer tail, holding "
            "short printed English dialogue in simple black comic lettering — text must be "
            "legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution."
        )),
    ],
    "eg": [
        ("hieroglyphic-tomb", (
            "A single illustrated comic book page rendered as ancient Egyptian tomb-painting / "
            "papyrus illustration — flat profile figures painted in classical Egyptian style with "
            "frontal eye and torso but profile head and limbs, palette of warm ochre, terracotta "
            "red, lapis blue, gold leaf, malachite green, and ivory white, hieroglyphic symbol "
            "borders framing each panel (ankh, eye of Horus, lotus, scarab, Nile reed glyphs), "
            "papyrus paper background with subtle weave texture, Egyptian pyramidal landmarks "
            "(Pyramids of Giza, Sphinx, Tourist Police kiosks rendered as flat painted shapes), "
            "ancient-Egyptian-tomb-painting aesthetic merged with modern sequential comic layout. "
            "Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 "
            "in the upper-left corner of each panel, separated by thin gold gutters. Each panel "
            "contains one clean white rounded speech bubble with a small pointer tail, holding "
            "short printed English dialogue in simple black comic lettering — text must be "
            "legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution."
        )),
        ("art-deco-egyptian-revival", (
            "A single illustrated comic book page in the bold 1920s-30s Egyptian-revival travel-"
            "poster art-deco style (post-Tutankhamun-discovery era) — bold flat simplified graphic "
            "shapes with crisp black outlines, streamlined modernist deco composition, palette of "
            "gold leaf, deep turquoise, lapis blue, papyrus cream, scarab green, and pyramid "
            "sandstone, stylized 1920s travelers in pith helmets alongside Egyptian figures in "
            "galabeyas, geometric lotus and papyrus-column ornament, hand-stenciled travel-poster "
            "typography, deco sun-rays and pyramidal silhouettes, Tutankhamun-revival decorative "
            "vocabulary, cheerful mid-century travel-advertising optimism. Showing four sequential "
            "panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner "
            "of each panel, separated by thin black panel borders with narrow cream gutters. Each "
            "panel contains one clean white rounded speech bubble with a small pointer tail, "
            "holding short printed English dialogue in art-deco stencil-style black lettering — "
            "text must be legible, in English only, and correctly spelled. Square 1:1 composition, "
            "2K resolution."
        )),
        ("modern-cairo-illustrated", (
            "A single illustrated comic book page in a contemporary illustrated Egyptian travel-"
            "comic style: confident fine black ink outlines with richly digital-painted watercolor-"
            "and-gouache fills, realistic character proportions and expressive faces, visible "
            "painterly texture, detailed Egyptian location backgrounds — golden Giza desert plateau "
            "with the pyramids of Khufu, Khafre, and Menkaure rendered in warm sandstone, the Sphinx "
            "in soft afternoon light, decorative camels with red-and-orange tasseled saddles, "
            "Tourist Police kiosks with the distinctive teal-and-white Egyptian uniform, hieroglyph-"
            "etched stelae as background details — palette of sand-gold, terracotta, Nile-blue, and "
            "cream. Egyptian figures in light galabeyas alongside modern travelers. Showing four "
            "sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-"
            "left corner of each panel, separated by thin clean black panel borders with narrow "
            "cream gutters. Each panel contains one clean white rounded speech bubble with a small "
            "pointer tail, holding short printed English dialogue in simple black comic lettering — "
            "text must be legible, in English only, and correctly spelled. Square 1:1 composition, "
            "2K resolution."
        )),
    ],
    "sa": [
        ("najdi-mud-architecture", (
            "A single illustrated comic book page in a warm Najdi heritage-illustration style "
            "centered on traditional salmon-pink mud-brick Najd architecture (Diriyah / Riyadh old "
            "town) — bold confident black ink outlines with rich gouache fills, warm earth-tone "
            "palette of salmon-mud-pink, terracotta, ochre, sandstone cream, deep cobalt, and "
            "saffron, traditional Najdi architectural details (stepped mud-brick parapets, "
            "triangular vent windows, palm-frond ceilings, intricate carved wooden doors), Saudi "
            "figures in white thobes and red-checkered shemaghs alongside modern travelers, warm "
            "Arabian peninsula afternoon light, restrained Islamic-arabesque pattern accents at "
            "panel corners (no figurative ornament). Showing four sequential panels arranged in a "
            "2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, "
            "separated by thin black panel borders with narrow cream gutters. Each panel contains "
            "one clean white rounded speech bubble with a small pointer tail, holding short printed "
            "English dialogue in simple black comic lettering — text must be legible, in English "
            "only, and correctly spelled. Square 1:1 composition, 2K resolution."
        )),
        ("aramco-1960s-poster", (
            "A single illustrated comic book page in the bold 1960s-70s Saudi/Gulf travel-poster "
            "modernist deco style (ARAMCO-era advertising aesthetic) — bold flat simplified graphic "
            "shapes with crisp black outlines, streamlined modernist composition, sun-bleached "
            "desert palette of sand amber, sky-cobalt, dune-shadow violet, palm-green, and ivory "
            "cream, stylized 1960s-modern travelers in modest dress alongside Saudi figures in "
            "thobes and shemaghs, Arabian peninsula scenery (Najd dune silhouettes, Riyadh Kingdom "
            "Tower, palm groves, modernist airport architecture, taxi rank), confident hand-"
            "stenciled travel-poster typography, mid-century Gulf advertising optimism. Showing "
            "four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the "
            "upper-left corner of each panel, separated by thin black panel borders with narrow "
            "cream gutters. Each panel contains one clean white rounded speech bubble with a small "
            "pointer tail, holding short printed English dialogue in modernist stencil-style black "
            "lettering — text must be legible, in English only, and correctly spelled. Square 1:1 "
            "composition, 2K resolution."
        )),
        ("contemporary-gulf-illustrated", (
            "A single illustrated comic book page in a contemporary illustrated Gulf travel-comic "
            "style: confident fine black ink outlines with richly digital-painted gouache fills, "
            "realistic character proportions and expressive faces, visible painterly texture, "
            "detailed Saudi Arabian location backgrounds — Riyadh Kingdom Tower silhouette at dusk, "
            "King Khalid International Airport curved white roofs, beige modernist taxi ranks, "
            "Riyadh palm-lined boulevards, Najd-style salmon-pink heritage neighborhoods — palette "
            "of warm sand, golden cream, deep cobalt night sky, terracotta, and accent palm-green. "
            "Saudi figures in white thobes and red-checkered shemaghs and women in modest abayas "
            "alongside modern international travelers, restrained tasteful composition appropriate "
            "to Saudi cultural sensibilities. Showing four sequential panels arranged in a 2x2 grid "
            "with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by "
            "thin clean black panel borders with narrow cream gutters. Each panel contains one "
            "clean white rounded speech bubble with a small pointer tail, holding short printed "
            "English dialogue in simple black comic lettering — text must be legible, in English "
            "only, and correctly spelled. Square 1:1 composition, 2K resolution."
        )),
    ],
}


def build_prompt(cc: str, style_block: str) -> str:
    scene = SCENES[cc]
    char = CHARACTERS[scene["character_key"]]
    return f"{style_block}\n\nCHARACTER: {char}\n\n{scene['scene']}"


def generate_one(cc: str, slug: str, prompt: str, ws: str, r2: str) -> tuple[str, str]:
    """Returns (slug, public_url-or-error)."""
    body = {"prompt": prompt, "aspect_ratio": "1:1", "resolution": "2k", "output_format": "jpeg"}
    tid = submit_nbp(body, T2I_EP, ws)
    if not tid:
        return slug, f"FAIL: submit"
    raw_url = poll_nbp(tid, ws, timeout=600)
    if not raw_url:
        return slug, f"FAIL: poll"
    out = OUT_DIR / f"{cc}-{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return slug, f"FAIL: dl {note}"
    r2_key = f"scam-comics/{cc}/style-tests/{slug}.jpg"
    if not upload_r2(out, r2_key, r2):
        return slug, f"FAIL: r2"
    return slug, f"https://img.tabiji.ai/{r2_key}"


def main():
    ws = _keychain("wavespeed-api-key")
    r2 = _keychain("cloudflare-api-token")
    if not ws or not r2:
        print("ERROR: missing wavespeed-api-key or cloudflare-r2-bjh in keychain")
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
