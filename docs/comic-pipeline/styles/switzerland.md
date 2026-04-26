---
name: Switzerland scam comic style block
description: Locked Nano Banana Pro style prompt for Switzerland scam comics — Müller-Brockmann Swiss modernist grid (white/black/Swiss-red, Helvetica sans-serif). Paste verbatim into every Switzerland scam generation.
type: project
---
Switzerland scam comic style — locked 2026-04-26 after a 3-way Swiss illustration bake-off (alpine Bauernmalerei folk-painting, Müller-Brockmann Swiss modernist grid, Albert Anker 19th-century genre-painting) at the Zurich Altstadt Fake Police Officer anchor scam. **Swiss modernist grid selected** for its uniquely Swiss design heritage (the International Typographic Style is one of Switzerland's globally-recognized cultural exports), sharp visual differentiation from every other locked country (no other lock uses pure modernist grid + Helvetica), restrained tasteful palette (white / black / Swiss-flag red / ink-blue) that suits the calm Swiss-precision tone of the scam-warning narrative, and effortless mobile readability via the modernist grid's signature clarity.

**Locked STYLE block (paste verbatim at the top of every Switzerland comic prompt):**

```
A single illustrated comic book page in the Swiss modernist design style of Josef Müller-Brockmann and the 1950s-60s Swiss International Typographic Style — clean precise geometric linework, restrained palette of pure white, deep black, single accent of Swiss-flag red and crisp ink-blue, perfect modernist grid composition with generous white space, Helvetica-style sans-serif typography, minimalist flat figure rendering with confident geometric shapes, Zurich Altstadt and Bahnhofstrasse rendered as clean architectural silhouettes, Swiss design's signature objectivity and clarity. Showing four sequential panels arranged in a perfect 2x2 grid with bold sans-serif numerals 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin sharp black panel borders with narrow white gutters. Each panel contains one clean white rectangular speech bubble (no rounded corners) with a small pointer tail, holding short printed English dialogue in clean Helvetica-style sans-serif lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{SWITZERLAND_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Swiss landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson with Stadtpolizei or 117 emergency line}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Swiss cities: bern, geneva, interlaken, lucerne, zermatt, zurich

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/ch/style-tests/swiss-modernist-grid.jpg` (Zurich Altstadt Fake Police Officer × Harry — bake-off winner)

**Why Swiss modernist grid over the other 2 candidates:**
- **Alpine Bauernmalerei** — strong heritage anchor but the rustic decorative-cattle-procession-border aesthetic read as "Switzerland the tourist-postcard" rather than "Switzerland the precise modern country"; better suited to alpine-village scenes than urban scam settings
- **Albert Anker 19th-century genre-painting** — beautifully dignified humanist tone but visually overlapped too closely with neighboring Germany's Heinrich Zille observational pen-and-ink-wash style on the same European hub
- **Swiss modernist grid (LOCKED)** — uniquely Swiss design heritage + maximum visual differentiation from neighbors + clean readability + suits the Swiss-precision calm-warning tone

**Style-specific notes:**
- The modernist grid is the most rule-bound style in the locked set. Future regens must respect: pure white background, Helvetica-only typography, single red/blue accent (no other colors), generous white space, sharp rectangular speech bubbles (NOT rounded).
- Swiss-flag red is the only saturated color permitted as an accent; everything else is white/black/ink-blue.
