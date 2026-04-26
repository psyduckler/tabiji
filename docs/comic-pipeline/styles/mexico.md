---
name: Mexico scam comic style block
description: Locked Nano Banana Pro style prompt for Mexican scam comics — Lotería card (Don Clemente tarjeta) folk-print. Paste verbatim into every Mexico scam generation.
type: project
---
Mexico scam comic style — locked 2026-04-21 (PR #353) on the iconic Mexican Lotería card style (Don Clemente tarjeta). Lotería chosen for its instant Mexican cultural recognition, naïve-folk figure proportions, ornamental card-frame composition that reads each panel as a small cautionary tarjeta, and saturated palette (chili red, marigold yellow, sky blue, cactus green) that distinguishes Mexico comics at a glance from neighbouring Costa Rica's tropical-deco travel-poster style.

**Locked STYLE block (paste verbatim at the top of every Mexico comic prompt):**

```
A single illustrated comic book page rendered in the iconic Mexican Lotería card (Don Clemente tarjeta) style — flat bright saturated colors (chili red, marigold yellow, sky blue, cactus green, and ivory white) with bold clean black outline, naive-folk figure proportions, centered iconic compositions on each panel, decorative thin black ornamental frame around every panel evoking the classic Lotería deck, each panel reading like a small cautionary Lotería tarjeta, warm cream paper background with a subtle printing-grain texture. Showing four sequential panels arranged in a 2x2 grid with small Lotería-style card numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{MEXICO_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Mexican landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Mexican cities: acapulco, cabo-san-lucas, cancun, cozumel, guadalajara, guanajuato, holbox, isla-mujeres, mazatlan, merida, mexico-city, oaxaca, playa-del-carmen, puebla, puerto-escondido, puerto-vallarta, san-cristobal-de-las-casas, san-miguel-de-allende, tulum

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/mx/style-tests/3-loteria-card-tarjeta.jpg` (Lotería tarjeta bake-off winner)
