---
name: Tanzania scam comic style block
description: Locked Nano Banana Pro style prompt for Tanzania scam comics — Zanzibar Swahili coastal travel-illustration (carved-wood doors + dhow + coral-stone, painterly watercolor). Paste verbatim into every Tanzania scam generation.
type: project
---
Tanzania scam comic style — locked 2026-04-26 after a 3-way Tanzanian illustration bake-off (Tingatinga folk-painting, Zanzibar Swahili coastal travel-illustration, contemporary East African modern with kanga-textile accents) at the Zanzibar Stone Town Ferry Porter anchor scam. **Zanzibar Swahili coastal selected** for its painterly travel-illustration warmth that captures Tanzania's Swahili coast, distinctive coral-stone-cream and Indian-Ocean-turquoise palette, detailed Stone Town backdrops (carved Zanzibari doors with brass studs, dhow sailing boats, narrow Swahili alleys), and visual flexibility to span Stone Town heritage + Serengeti wildlife + Kilimanjaro foothills + Dar es Salaam scenes for future Tanzanian cities.

**Locked STYLE block (paste verbatim at the top of every Tanzania comic prompt):**

```
A single illustrated comic book page in a warm Zanzibar Swahili-coast travel-illustration style — confident fine black ink linework with rich watercolor washes, warm coastal palette of coral-stone cream, deep Indian Ocean turquoise, palm green, sunset orange, and saffron, detailed Stone Town backgrounds (carved-wood Zanzibari doors with brass studs, coral-stone facades with hanging laundry, dhow sailing boats with triangular sails, palm-fringed harbour, narrow Swahili alleys), Tanzanian figures in vibrant kanga and kitenge fabrics alongside modern travelers, warm equatorial sunlight. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{TANZANIA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Tanzanian landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson with ID-badged porter or official channel}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Tanzanian cities: arusha, dar-es-salaam, ngorongoro, serengeti, zanzibar

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/tz/style-tests/zanzibar-swahili-coastal.jpg` (Zanzibar Stone Town Ferry Porter × Marcus — bake-off winner)

**Why Zanzibar Swahili coastal over the other 2 candidates:**
- **Tingatinga folk-painting** — strongest Tanzanian-folk heritage anchor and beautifully saturated, but the dark-background flat-figure aesthetic struggled to render the porter-grabs-bag intimidation moment with everyday-realism urgency the scam-warning needs
- **East African modern with kanga corner accents** — clean modern realism but the kanga-pattern corners read as "decorative travel-blog" more than "Swahili-coast-anchored"; less distinctive
- **Zanzibar Swahili coastal (LOCKED)** — painterly warmth + culturally anchored without folk-pastiche + readable scam-mechanic depiction + scales across the Stone Town + Serengeti + Kilimanjaro + Dar es Salaam range
