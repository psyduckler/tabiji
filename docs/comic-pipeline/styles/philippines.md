---
name: Philippines scam comic style block
description: Locked Nano Banana Pro style prompt for Philippines scam comics — vibrant Filipino jeepney folk-art (rainbow-saturated hand-painted). Paste verbatim into every Philippines scam generation.
type: project
---
Philippines scam comic style — locked 2026-04-26 after a 3-way Filipino illustration bake-off (jeepney folk-art, BenCab figurative, Kenkoy/Pinoy komiks) at the Manila NAIA Airport Taxi Overcharge anchor scam. **Jeepney folk-art selected** for its instantly-recognizable Filipino visual signal (the painted jeepney is iconic Manila folk-art with no ambiguity), rainbow-saturated palette that distinguishes the Philippines set from neighboring Indonesia (quiet Lontar palm-leaf) and Thailand (pastel watercolor), cheerful working-class energy that suits the everyday-scam-warning tone, and ornamental hand-painted lettering that scales beautifully from mobile thumbnail to print.

**Locked STYLE block (paste verbatim at the top of every Philippines comic prompt):**

```
A single illustrated comic book page in the vibrant Filipino jeepney folk-art style — bold hand-painted decorative panels with rainbow-saturated colors (hot pink, marigold yellow, sky blue, lime green, fire-engine red, bright cyan), confident black outline brushwork, ornamental hand-painted Filipino jeepney lettering and decorative swirls, colorful tassels, mirror-and-chrome accents at panel borders, sun-rays and religious iconography flourishes, cheerful working-class Filipino visual energy, Manila urban backgrounds (jeepneys, sari-sari stores, NAIA terminals, Makati skyline). Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by decorative jeepney-style ornamental borders. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{PHILIPPINES_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Philippine landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson with Grab app or official rank}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Philippine cities: bohol, boracay, cebu, coron, davao, el-nido, manila, palawan, siargao, vigan

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/ph/style-tests/jeepney-folk-art.jpg` (Manila NAIA Airport Taxi Overcharge × Priya — bake-off winner)

**Why jeepney folk-art over the other 2 candidates:**
- **BenCab figurative** — refined contemporary-art tone but reads more "art-gallery solemn" than "warning comic"; muted earth-tone palette less distinctive against the Indonesia / Thailand neighbors on the same SE Asia hub
- **Kenkoy / Pinoy komiks** — strong Filipino comic-book heritage but the 1930s-50s sepia-and-cream four-color aesthetic gets visually-quiet next to the saturated neighbors; risks reading as generic mid-century-American komiks rather than uniquely Filipino
- **Jeepney folk-art (LOCKED)** — instant Filipino recognition + saturated visual punch + ornamental energy + scales across all 10 Philippine cities (urban Manila, beach Boracay/Palawan/Coron, heritage Vigan)
