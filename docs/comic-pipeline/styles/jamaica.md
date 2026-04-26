---
name: Jamaica scam comic style block
description: Locked Nano Banana Pro style prompt for Jamaica scam comics — 1970s Bob-Marley-era reggae poster (red/gold/green Rastafari palette, hand-painted). Paste verbatim into every Jamaica scam generation.
type: project
---
Jamaica scam comic style — locked 2026-04-26 after a 3-way Jamaican illustration bake-off (1970s reggae album-cover/poster, contemporary Jamaican mural/dancehall, Caribbean storybook watercolor) at the Montego Bay Hip Strip Aggressive Vendor anchor scam. **1970s reggae poster selected** for its globally-iconic Jamaican visual signal (Bob Marley reggae aesthetic is universally read as Jamaica), saturated Rastafari palette (red, gold-yellow, forest-green) that distinguishes the Jamaica set from any neighboring country, sun-drenched Caribbean warmth that suits the Hip Strip beach-town tone, and retro hand-painted poster lettering that scales beautifully from mobile thumbnail to print.

**Locked STYLE block (paste verbatim at the top of every Jamaica comic prompt):**

```
A single illustrated comic book page in the 1970s Jamaican reggae album-cover / Bob Marley poster aesthetic — bold hand-painted figures with confident black outline, saturated Rastafari palette (deep red, gold-yellow, forest-green, black, plus tropical turquoise and palm-leaf green), sun-drenched Caribbean warmth, retro 1970s reggae visual vocabulary (palm fronds, sun-rays, mountains, dreadlock silhouettes, hand-painted poster lettering), Montego Bay coastal backgrounds (Hip Strip palm-lined avenue, turquoise Caribbean, craft-market stalls, colonial colorful storefronts), warm Jamaican sun. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{JAMAICA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Jamaican landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson, polite-but-firm departure}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Jamaican cities: kingston, montego-bay, negril, ocho-rios, port-antonio

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/jm/style-tests/reggae-poster-1970s.jpg` (Montego Bay Hip Strip Aggressive Vendor × Margie — bake-off winner)

**Why 1970s reggae poster over the other 2 candidates:**
- **Jamaican mural / dancehall** — bold contemporary energy and authentic street-art Jamaica, but the electric-pink + neon-yellow palette read more aggressive than the gentle-but-firm vendor-warning tone needed
- **Caribbean storybook watercolor** — warm and friendly but generic-tropical; could read as Bahamas, Barbados, or any Caribbean island — not distinctively Jamaican
- **1970s reggae poster (LOCKED)** — globally-iconic Jamaican visual + Rastafari palette anchor + sun-drenched warmth + scales across all 5 Jamaican cities (Hip Strip MoBay, Negril beaches, Ocho Rios cruise port, Kingston urban, Port Antonio jungle)
