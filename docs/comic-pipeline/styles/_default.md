---
name: Default fallback scam comic style block
description: Locked Nano Banana Pro fallback style — warm soft watercolor-and-ink storybook (universal, no country-specific elements). Used by the v2 pipeline when a country has no specific lock in styles.py.
type: project
---
Default fallback comic style — locked 2026-04-26 after a 10-candidate bake-off (5 illustrative/painterly directions in batch A + 5 wider-range graphic/print directions in batch B), all anchored on the same generic airport-taxi scam scene with no country-specific landmarks. **Warm watercolor storybook selected** for its universal legibility (reads as "tabiji travel comic" without invoking any specific country's locked aesthetic), neutral palette of cream / sky-blue / warm-ochre / sage / dusty-rose (no dominant signal that would clash with an arbitrary country's location backgrounds), gentle storybook tone appropriate to global cautionary travel-warnings, and clean readability across mobile and print sizes.

This style is the **fallback used by `scripts/comic-pipeline/synthesize.py` whenever a country has no explicit STYLES/PILOTS entry** in `scripts/comic-pipeline/styles.py`. Locked countries (Argentina, Australia, Austria, Brazil, Canada, China, Colombia, Costa Rica, Croatia, Egypt, France, Germany, Greece, Hong Kong, India, Indonesia, Italy, Jamaica, Japan, Malaysia, Mexico, Morocco, Philippines, Portugal, Saudi Arabia, Spain, Switzerland, Tanzania, Thailand, Turkey, United Kingdom, United States, Vietnam) keep using their specific locks; everything else uses this default until a per-country bake-off happens.

**Locked STYLE block (paste verbatim at the top of every default-fallback comic prompt):**

```
A single illustrated comic book page in a warm soft watercolor-and-ink storybook style — confident fine black-ink contour drawing with light hand-painted watercolor washes, neutral universal palette of cream, sky blue, warm ochre, sage green, dusty rose, and pale terracotta, friendly cartoon character figures with simple expressive faces, generic-international travel-scene backgrounds (taxi rank, airport curb, modest sedan, streetlight, generic urban context — no country-specific landmarks), warm afternoon light, gentle storybook tone appropriate to global cautionary travel-warnings. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{DEFAULT_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with country-appropriate landmark IF the country has any well-known generic visual cue, otherwise generic international travel-scene}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson with safer-alternative app/official-channel}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/_default/style-tests/warm-watercolor-storybook.jpg` (generic airport-taxi scam × Priya — bake-off winner from the 10-candidate default-style trial)

**When this default kicks in:**
- A new country is added to `scams/country/<cc>/` and city pages, but no `STYLES["<country>"]` / `PILOTS["<country>"]` entry exists yet
- A typo or unrecognized country slug is passed to the v2 pipeline
- An emergency batch where a per-country bake-off hasn't been run yet

The fallback is intentionally generic — when the v2 pipeline produces a default-styled comic, the resulting visual won't look like Italy or Japan or anywhere specific. **For book-quality publication and visual consistency across a country's full city set, run a proper bake-off and lock a per-country style** (see `style-exploration.md`); the default is a coherent stopgap, not a long-term substitute.

**Bake-off gallery** (preserved for "why this default?" lookups):

| # | Style | URL |
|---|---|---|
| A1 | **Warm watercolor storybook ← CHOSEN** | `scam-comics/_default/style-tests/warm-watercolor-storybook.jpg` |
| A2 | Editorial Niemann sophisticated | `scam-comics/_default/style-tests/editorial-niemann-sophisticated.jpg` |
| A3 | Contemporary graphic novel | `scam-comics/_default/style-tests/contemporary-graphic-novel.jpg` |
| A4 | Travel journal sketch | `scam-comics/_default/style-tests/travel-journal-sketch.jpg` |
| A5 | Mid-century children's book | `scam-comics/_default/style-tests/midcentury-childrens-book.jpg` |
| B1 | Risograph 2-color zine | `scam-comics/_default/style-tests/risograph-2color-zine.jpg` |
| B2 | Steinberg pure-line | `scam-comics/_default/style-tests/steinberg-pure-line.jpg` |
| B3 | Charley Harper geometric | `scam-comics/_default/style-tests/charley-harper-geometric.jpg` |
| B4 | Vector flat app-illustration | `scam-comics/_default/style-tests/vector-flat-app-illustration.jpg` |
| B5 | Linocut hand-printed | `scam-comics/_default/style-tests/linocut-handprinted.jpg` |
