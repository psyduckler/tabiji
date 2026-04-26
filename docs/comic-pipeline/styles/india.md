---
name: India scam comic style block
description: Locked Nano Banana Pro style prompt for India scam comics — classical Mughal miniature painting (jewel-tone court ateliers). Paste verbatim into every India scam generation.
type: project
---
India scam comic style — locked 2026-04-26 after a 3-way Indian illustration bake-off (Mughal miniature, Madhubani folk-art, 1970s-80s Bollywood movie-poster) at the Delhi Fake Government Tourist Office anchor scam. **Mughal miniature selected** for its instant heritage-recognition (Indo-Islamic Mughal court painting is a globally-known Indian visual idiom), refined jewel-tone palette that distinguishes the India set from neighboring China (Feng Zikai brush) and Indonesia (Lontar palm-leaf), meticulous architectural detail (Mughal red-sandstone arches and jharokha balconies render Indian landmarks beautifully), and the dignified courtly tone appropriate for a 49-page Indian set across 10+ cities.

**Locked STYLE block (paste verbatim at the top of every India comic prompt):**

```
A single illustrated comic book page in the classical Mughal miniature painting style of the Akbar/Jahangir court ateliers — meticulous fine black-ink outline drawing with bright opaque jewel-tone gouache fills (deep crimson, peacock-blue, emerald, saffron yellow, lapis blue, gold leaf accents), classical Indian profile poses with elongated almond eyes and refined gestures, intricately patterned textiles and architectural detail (Mughal red sandstone arches, jharokha balconies, marble inlay), decorative geometric and floral borders framing each panel in red and gold, ornate calligraphic flourishes, courtly Indo-Islamic painting tradition. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin gold borders with cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{INDIA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Indian landmark}. Speech bubble: "{short line}"
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
- Indian cities: agra, bangalore, chennai, delhi, goa, hyderabad, jaipur, kolkata, mumbai, rishikesh

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/in/style-tests/mughal-miniature.jpg` (Delhi Fake Government Tourist Office × Margie — bake-off winner)

**Why Mughal miniature over the other 2 candidates:**
- **Madhubani folk-art** — strong heritage-anchor and bold visual punch, but the doubled-outline + dense-pattern aesthetic competes with the comic narrative at panel-thumbnail size; better suited to single illustrations than multi-panel sequential storytelling
- **Bollywood movie-poster** — vivid and unmistakably Indian, but the 1970s-cinema melodrama tone fights the cautionary scam-alert voice; reads as entertainment rather than warning
- **Mughal miniature (LOCKED)** — refined jewel-tone palette + careful architectural detail + dignified courtly tone + best at small print sizes
