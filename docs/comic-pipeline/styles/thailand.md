---
name: Thailand scam comic style block
description: Locked Nano Banana Pro style prompt for Thailand country scam comics — warm watercolor storybook, 2x2 grid, English speech bubbles. Paste verbatim into every Thailand scam generation.
type: project
originSessionId: 6e1b60d6-8114-4bf8-83d3-25c3a4635638
---
Thailand country-scam comic style — approved 2026-04-18 during pilot test. Watercolor storybook chosen to match the older, slightly female-skewing audience and the soft Thai tropical-light aesthetic.

**Locked STYLE block (paste verbatim at the top of every Thailand comic prompt):**

```
A single illustrated comic book page in warm soft watercolor storybook style, showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin clean white gutters. Hand-painted watercolor textures with visible paper grain, muted pastel palette warmed by golden Thai sunlight, gentle expressive faces with soft pencil linework, delicate shadows, unhurried storybook pacing. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black lettering — text must be legible and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{THAILAND_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from project_scam_comics_cast.md}

SCENE:
Panel 1: {what happens in the scene}. Speech bubble: "{short line of dialogue, under ~8 words}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually the "realization" or "home" moment}. Speech bubble: "{short line}"
```

**API call — prefer `edit` endpoint with prior comics as style refs (tighter consistency than text-to-image):**
- Endpoint: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit`
- Body: `{"prompt": "<full prompt>", "images": [<2-3 prior comic URLs as style anchors>], "aspect_ratio": "1:1", "output_format": "jpeg"}`
- First comic in a country has no anchors → use `/text-to-image` endpoint with the same prompt shape.
- `edit-multi` does NOT support `aspect_ratio: "1:1"` (only 3:2, 2:3, 3:4, 4:3) — use plain `/edit` which does support 1:1 and accepts multiple images in the `images` array.
- Poll: `GET https://api.wavespeed.ai/api/v3/predictions/{id}/result` until `status=="completed"`
- Credential: `wavespeed-api-key` in macOS keychain.

**Storage path (production — matches existing France/Paris pattern):**
- R2 path: `scams/<city-slug>/scam-<N>.jpg` where N is the scam's 1-indexed position on the city page
- Public URL: `https://img.tabiji.ai/scams/<city-slug>/scam-<N>.jpg`
- HTML injection: `<img class="scam-comic" src="..." alt="<short title> — comic illustration" loading="lazy" style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;">` placed immediately after `<div class="scam-location">...</div>` inside each `<div class="scam-card">`. The `scam-comic` class has no CSS rule — styling is entirely inline.

**Dialogue rules:**
- Keep each line under ~8 words — longer text occasionally mis-spells.
- Use exclamation/question marks for urgency; comics read faster.
- Panel 4 dialogue is usually the protagonist realizing they were scammed.
- Avoid numbers-as-digits in some cases ("twenty baht" renders more reliably than "20 baht") — spot-check.

**Why:** Every country gets its own style block to feel culturally grounded — Thailand is watercolor storybook, Japan will be manga, USA will be American-style comic, Italy fumetti/BD, etc. This file pins Thailand so we never drift.

**How to apply:** Use this exact style block for every Thailand scam comic. When starting a new country, create a sibling `project_scam_comics_style_<country>.md` file with that country's locked style block, keeping the same template structure.
