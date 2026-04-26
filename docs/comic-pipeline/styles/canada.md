---
name: Canada scam comic style block
description: Locked Nano Banana Pro style prompt for Canadian scam comics — Drawn & Quarterly Toronto indie-comic style (Seth / Chester Brown / Michael DeForge). Paste verbatim into every Canada scam generation.
type: project
---
Canada scam comic style — chosen 2026-04-18 after a 5-way Canadian illustration bake-off (Group of Seven landscape, Drawn & Quarterly indie, Maud Lewis Maritime folk art, Charles Pachter pop Canadiana, Ted Harrison Yukon stripe). Drawn & Quarterly chosen for narrative-comic fluency, literary mature tone, Canadian indie-comic heritage, and the best character-consistency across the cast.

**Locked STYLE block (paste verbatim at the top of every Canada comic prompt):**

```
A single illustrated comic book page in the Toronto indie-comic style of Drawn & Quarterly artists (Seth, Chester Brown, Michael DeForge) — clean precise black ink outlines with quiet duotone pencil hatching, muted palette of cream paper and olive-teal wash, understated quietly-melancholic tone, nostalgic 1950s Canadian small-town sensibility, thoughtful sequential composition, subtle spot-blacks, refined comic-book-as-literature feel. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow white gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic-book lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{CANADA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Canadian landmark}. Speech bubble: "{short line}"
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
- Canadian cities: banff, calgary, halifax, jasper, montreal, niagara-falls, ottawa, quebec-city, toronto, vancouver, victoria-bc, whistler

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/ca/style-tests/2-drawn-and-quarterly-indie.jpg` (Priya + Toronto taxi card-swap)
