---
name: Morocco scam comic style block
description: Locked Nano Banana Pro style prompt for Morocco scam comics — Matisse Tangier-period vibrant watercolor (fauve color-as-emotion). Paste verbatim into every Morocco scam generation.
type: project
---
Morocco scam comic style — locked 2026-04-26 after a 3-way Moroccan illustration bake-off (zellige tile-border, Matisse Tangier watercolor, Hassan Hajjaj contemporary pop) at the Marrakech "That Way's Closed" Fake Guide anchor scam. **Matisse Tangier watercolor selected** for its painterly vibrancy that captures Marrakech's sun-drenched warmth, the historical resonance of Matisse's 1912-13 Tangier period (a Moroccan-anchored European-art lineage that reads as Moroccan without being decorative-tile pastiche), saturated North African palette (Moroccan blue, terracotta, moss green, deep magenta), and clean readability at thumbnail size that the more ornate zellige border didn't have.

**Locked STYLE block (paste verbatim at the top of every Morocco comic prompt):**

```
A single illustrated comic book page in the loose vibrant watercolor style of Matisse's 1912 Tangier paintings — bold expressive brushed shapes with confident dark ink contour drawing, saturated North African palette (Moroccan blue, terracotta orange, moss green, deep magenta, warm cream, gold), painterly watercolor washes with visible edges and bleeding pigment, simplified flattened forms with decorative pattern, sun-drenched Moroccan light, Marrakech medina backdrops (Koutoubia minaret, ochre walls, souks with hanging textiles, palm-shaded courtyards), modern fauve-influenced color-as-emotion approach. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{MOROCCO_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Moroccan landmark}. Speech bubble: "{short line}"
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
- Moroccan cities: agadir, casablanca, chefchaouen, essaouira, fez, marrakech, ouarzazate, tangier

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/ma/style-tests/matisse-tangier-watercolor.jpg` (Marrakech "That Way's Closed" Fake Guide × Harry — bake-off winner)

**Why Matisse Tangier watercolor over the other 2 candidates:**
- **Zellige tile-border** — strongest Moroccan cultural signal but the ornate mosaic borders compete with the panel narrative at thumbnail size; risks "decorative postcard" rather than "narrative comic"
- **Hassan Hajjaj pop-art** — bold and contemporary, but the photo-realistic-leaning portraiture didn't render as cleanly as the looser fauve watercolor; the consumer-product-pattern frames also competed with panel content
- **Matisse Tangier watercolor (LOCKED)** — painterly + readable + Moroccan-anchored color palette + scales beautifully across the medina/Atlas/coast variety in the 8-city set
