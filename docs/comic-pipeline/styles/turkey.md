---
name: Turkey scam comic style block
description: Locked Nano Banana Pro style prompt for Turkey scam comics — Ottoman Iznik-tile border + contemporary illustrated travel-comic interior. Paste verbatim into every Turkey scam generation.
type: project
---
Turkey scam comic style — locked 2026-04-21 to match the visual aesthetic of the 70 in-spec v1 Turkey comics already live across 13 cities. The 2026-04-21 audit of `/scams/country/tr/` flagged 8 of 78 comics as v1 keyword-template fallbacks (see `scripts/comic-pipeline/regen_turkey.py`). The remaining 70 were on-scam and share a consistent ornate-Iznik-border + warm illustrated-travel-comic interior look, so we lock that verbatim rather than run a fresh bake-off — new regens need to blend into the existing set, not replace it.

**Locked STYLE block (paste verbatim at the top of every Turkey comic prompt):**

```
A single illustrated comic book page framed inside an ornate Ottoman Iznik-tile border — rich decorative geometric-floral rim in cobalt blue, coral red, emerald green, saffron yellow, and cream white, with stylized tulip, carnation, and arabesque motifs drawn as flat stained-glass-like shapes. Interior of each panel rendered in a warm contemporary illustrated-travel-comic style: confident fine black ink outlines with richly-painted watercolor and gouache fills, a warm palette of parchment cream, terracotta, deep Ottoman blue, ochre, crimson, and gold-leaf accents, detailed Turkish architectural and landscape backgrounds (mosques, minarets, bazaar domes, ancient ruins, travertine terraces, gulet boats, fairy-chimneys depending on scene), traveler figures in modern casual clothing alongside Turkish characters in traditional vests, fezzes, and embroidered waistcoats, storybook-rich composition with visible painterly texture. Showing four sequential panels arranged in a 2x2 grid with small blue numerals 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin cream gutters inside the tiled border. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{TURKEY_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from cast.md}

SCENE:
Panel 1: {what happens, with Turkish landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson}. Speech bubble: "{short line}"
```

**API call:**
- Subsequent comics: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback on failure: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Turkish cities: alanya, antalya, bodrum, cappadocia, ephesus, fethiye, istanbul, izmir, konya, kusadasi, marmaris, pamukkale, side-turkey

**Pilot reference image:** `https://img.tabiji.ai/scams/istanbul/scam-1.jpg` (Istanbul Shoe Shine Drop Trick — a bespoke v1 Turkey comic that cleanly exhibits both the Iznik-tile border and the contemporary-travel-comic interior)

**Why lock the existing v1 look rather than bake off a new style:**
- Only 8/78 comics (≈10%) need regen — the other 70 are on-scam and aesthetically coherent
- Swapping style for the whole country would require re-doing 70 already-good images
- The "ornate Ottoman tile border" look is genuinely culturally anchored and scans as "Turkey" immediately — good enough to keep
- If we ever want to re-do the whole country with a single named-artist style (e.g. Nuri İyem figurative painting, Ottoman miniature à la Matrakçı Nasuh, or İbrahim Balaban folk-art), that's a separate style-exploration exercise
