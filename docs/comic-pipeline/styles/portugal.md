---
name: Portugal scam comic style block
description: Locked Nano Banana Pro style prompt for Portuguese scam comics — José de Guimarães folk-pop modernist, 2x2 grid, English speech bubbles. Paste verbatim into every Portugal scam generation.
type: project
---
Portugal country-scam comic style — chosen 2026-04-20 after a 3-way Portuguese illustration bake-off (1-azulejo blue-and-white tile, 2-Paula Rego magic-realist pastel, 3-José de Guimarães folk-pop modernist). José de Guimarães selected for its bold flat graphic energy, unmistakably Portuguese folk-art vocabulary (galo de Barcelos, azulejo geometric motifs, Bordalo Pinheiro ceramics reduced to primary-color shapes), and strong visual distinction from other country styles in the library.

**Locked STYLE block (paste verbatim at the top of every Portugal comic prompt):**

```
A single illustrated comic book page in the folk-pop modernist style of Portuguese contemporary artist José de Guimarães — bold flat hand-painted shapes with strong black outline, saturated primary color palette (Portuguese flag red + cobalt blue + mustard yellow + white + black), stylized figures drawn in a modernist reduction inspired by Portuguese folk art (galo de Barcelos cockerel, azulejo geometric motifs, Bordalo Pinheiro ceramics), playful graphic simplification, bright confident storytelling tone. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow white gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{PORTUGAL_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens in the scene, with Portuguese landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson}. Speech bubble: "{short line}"
```

**Cast rotation:**
Gemini 2.5 Pro synthesizes the character choice per scam via `synthesize.py`. The four canonical travelers (Margie, Priya, Harry, Marcus) rotate based on which fits the scam best — e.g., Harry for the drug-tout street scam, Margie for older-cruise-day pickpocket scenarios, Priya for the Booking.com phishing scam, Marcus for the Klass Wagen rental fraud.

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Pilot image (style anchor):**
`https://img.tabiji.ai/scam-comics/pt/style-tests/3-jose-de-guimaraes-folk-pop.jpg`

**Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Portuguese cities: lisbon, porto, sintra, funchal, faro, albufeira, lagos-portugal, cascais, coimbra, nazare
