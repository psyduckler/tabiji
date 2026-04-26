---
name: Greece scam comic style block
description: Locked Nano Banana Pro style prompt for Greek scam comics — ancient red-figure pottery storytelling, modern 2x2 grid, English speech bubbles. Paste verbatim into every Greece scam generation.
type: project
---
Greek country-scam comic style — chosen 2026-04-18 after 5-way European style bake-off (Asterix, red-figure pottery, Mattotti gouache, Corto Maltese, Loustal). Red-figure pottery chosen for its instant Greek-heritage recognition and visual differentiation from France (Tintin), Thailand (watercolor), Austria (Sempé), Hong Kong (Shaw Brothers).

**Locked STYLE block (paste verbatim at the top of every Greece comic prompt):**

```
A single illustrated comic book page drawn as ancient Greek red-figure pottery storytelling — figures rendered as flat orange-red silhouettes on a deep matte terracotta background with fine black painted details on the figures, classical profile poses, and geometric border motifs of meanders (Greek key) and laurel leaves framing each panel, a modern sequential-comic layout merged with ancient vase-painting aesthetics. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin white gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{GREECE_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens in the scene, with Greek landmark}. Speech bubble: "{short line}"
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
- Greek cities: athens, corfu, heraklion, mykonos, rhodes, santorini

**Why:** The red-figure pottery style gives every Greek scam page a distinctive "this is Greece" visual identity that no other country has — heritage-locked, unmistakable, and differentiated from the France Tintin set on the same tabiji hub. Dialogue is still in modern English (legibility for readers) but the figurative style is 5th-century BC.

**How to apply:** Use this style block verbatim for every Greek scam comic. Do not adapt to modern color palettes — the terracotta + red-figure limitation is what makes it recognizably Greek.
