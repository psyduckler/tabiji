---
name: France scam comic style block
description: Locked Nano Banana Pro style prompt for France country scam comics — Hergé ligne claire (Tintin), 2x2 grid, English speech bubbles. Paste verbatim into every France scam generation.
type: project
---
France country-scam comic style — piloted 2026-04-18 on Paris Gold Ring Trick. Classic European ligne claire (Tintin / Hergé) chosen to evoke French/Belgian bande dessinée heritage and to feel distinct from the existing scattered multi-style French-language comics we're replacing.

**Locked STYLE block (paste verbatim at the top of every France comic prompt):**

```
A single illustrated comic book page in the classic European ligne claire style of Hergé and Tintin: clean uniform-weight black ink outlines with no hatching, bright flat colors with no gradient or painterly texture, minimal shading, careful architectural detail, clear geometric composition, cheerful bande dessinée tone. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin crisp black panel borders with narrow white gutters. Each panel contains one clean white oval speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic-book lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{FRANCE_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens in the scene}. Speech bubble: "{short English line, under ~8 words}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually the "realization" or "lesson" moment}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Storage path (production):**
- R2 path: `scams/<city-slug>/scam-<N>.jpg`
- Public URL: `https://img.tabiji.ai/scams/<city-slug>/scam-<N>.jpg`
- HTML injection: `<img class="scam-comic" src="..." alt="<short title> — comic illustration" loading="lazy" style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;">` immediately after `<div class="scam-location">...</div>`

**Migration note:** The existing France comic set (Paris, Nice, Marseille, Cannes, etc. — originally added in commit `2931b5192e`) is scattered across multiple inconsistent styles and mostly in French dialogue. Replacing the whole set with this locked Tintin style + English dialogue + canonical cast is the plan; scale-up happens after the Paris Gold Ring pilot is approved.

**Dialogue rules:**
- Keep each line under ~8 words — Tintin-style lettering reads cleaner with short phrases anyway.
- All dialogue in English — the prior French dialogue is part of what's being fixed.
- Panel 4 dialogue is usually the protagonist's realization or the "lesson" line.
