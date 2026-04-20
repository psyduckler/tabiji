---
name: Argentina scam comic style block
description: Locked Nano Banana Pro style prompt for Argentine scam comics — Quino / Mafalda classic newspaper-strip, 2x2 grid, English speech bubbles. Paste verbatim into every Argentina scam generation.
type: project
---
Argentina country-scam comic style — chosen 2026-04-20 after a 5-way Argentine illustration bake-off (Quino/Mafalda classic strip, Liniers/Macanudo contemporary indie watercolor, Molina Campos gauchesco folk painting, Alberto Breccia warm porteño ink, 1930s tango-era travel poster). **Quino/Mafalda selected** for its authentically Argentine cultural signal (Mafalda is a universally-recognized mid-20th-century porteño icon), warm humanist humor that fits cautionary-scam narrative, and clean flat-color readability at small print sizes.

**Locked STYLE block (paste verbatim at the top of every Argentina comic prompt):**

```
A single illustrated comic book page in the classic Argentine newspaper-strip style of Quino (Joaquín Salvador Lavado, creator of 'Mafalda') — clean confident black ink outlines with occasional hatched shadow, simple expressive cartoon faces with oversized eyes and tiny gestures, warm flat-color fills in a muted palette of cream, soft mustard, dusty rose, and gentle sky blue, gently humorous social-observation tone, the beloved mid-20th-century Buenos Aires newspaper comic-strip aesthetic. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic-strip lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{ARGENTINA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens in the scene, with Argentine landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson}. Speech bubble: "{short line}"
```

**API call:**
- First comic in Argentina: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Subsequent comics: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot (`scam-comics/ar/style-tests/1-quino-mafalda.jpg`) as style anchor
- Body: `{"prompt": "...", "aspect_ratio": "1:1", "resolution": "2k", "output_format": "jpeg"}` (t2i) or `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}` (edit)
- Credential: `wavespeed-api-key` in macOS keychain

**Pilot reference:** `https://img.tabiji.ai/scam-comics/ar/style-tests/1-quino-mafalda.jpg` (Buenos Aires Florida Ave '¡Cambio!' Touts × Margie)

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Argentine cities: buenos-aires, mendoza, bariloche, puerto-iguazu, el-calafate, ushuaia, el-chalten, salta, cordoba-argentina, tigre, rosario
- 11 cities × 6 scams = 66 comics total
