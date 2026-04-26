---
name: Malaysia scam comic style block
description: Locked Nano Banana Pro style prompt for Malaysian scam comics — Yusof Gajah vibrant naïve folk-art. Paste verbatim into every Malaysia scam generation.
type: project
---
Malaysia scam comic style — locked 2026-04-22 (PR #370) on the vibrant naïve folk-art style of Yusof Gajah, Malaysia's beloved children's-book illustrator. Yusof Gajah chosen for its bold saturated color palette, intricate dot-and-line patterning, and warm Malaysian-children's-book sensibility — distinct from neighbouring Indonesia's quiet Lontar palm-leaf and Thailand's pastel watercolor, while remaining culturally anchored to Malaysian visual heritage.

**Locked STYLE block (paste verbatim at the top of every Malaysia comic prompt):**

```
A single illustrated comic book page in the vibrant naive folk-art style of Yusof Gajah, Malaysia's beloved illustrator — bold flat saturated colors (hot pink, marigold, turquoise, emerald, violet, sunset orange) with confident black ink outlines, richly patterned clothing and backgrounds with intricate dot-and-line decoration and elephant and flora motifs, naive-folk figure proportions with oversized friendly eyes, decorative repeating motifs of lotus, tropical leaves, and batik flourishes, warm cream paper background with subtle grain, cheerful Malaysian-children's-book sensibility. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{MALAYSIA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Malaysian landmark}. Speech bubble: "{short line}"
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
- Malaysian cities (10): cameron-highlands, genting-highlands, ipoh, johor-bahru, kota-kinabalu, kuala-lumpur, kuching, langkawi, melaka, penang

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/my/style-tests/4-yusof-gajah-folk-naif-nb2.jpg` (Yusof Gajah folk-naïf bake-off winner)
