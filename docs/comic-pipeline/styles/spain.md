---
name: Spain scam comic style block
description: Locked Nano Banana Pro style prompt for Spanish scam comics — Paco Roca contemporary graphic novel, 2x2 grid, English speech bubbles. Paste verbatim into every Spain scam generation.
type: project
originSessionId: 6e1b60d6-8114-4bf8-83d3-25c3a4635638
---
Spain country-scam comic style — chosen 2026-04-18 after a 5-way Spanish illustration bake-off (Sorolla impressionism, Paco Roca contemporary, Miguelanxo Prado painted BD, Azulejo ceramic tile, Mariscal Mediterráneo). Paco Roca selected for its modern Spanish indie-comic tone — humanist, quiet, warm pastel palette that suits the cautionary-scam narrative at readable comic pace.

**Locked STYLE block (paste verbatim at the top of every Spain comic prompt):**

```
A single illustrated comic book page in the contemporary Spanish graphic-novel style of Paco Roca (author of 'Arrugas' and 'La Casa') — clean precise dark ink outlines with warm pastel gouache fills, muted palette of cream, soft orange, dusty rose, and gentle blue, sensitive humanist rendering of everyday life, quiet storytelling tone of modern Spanish indie comics, visible soft shading. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow white gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic-book lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{SPAIN_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from project_scam_comics_cast.md}

SCENE:
Panel 1: {what happens in the scene, with Spanish landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson}. Speech bubble: "{short line}"
```

**API call:**
- First comic in Spain: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Subsequent comics: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with 2-3 approved Spanish comics as style anchors (`images` array)
- Body: `{"prompt": "...", "aspect_ratio": "1:1", "resolution": "2k", "output_format": "jpeg"}` (t2i) or `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}` (edit)
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Spanish cities: barcelona, bilbao, cordoba, gran-canaria, granada-spain, ibiza, lanzarote, madrid, malaga, palma-de-mallorca, san-sebastian, santiago-de-compostela, seville, tenerife, toledo, valencia
