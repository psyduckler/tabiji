---
name: Colombia scam comic style block
description: Locked Nano Banana Pro style prompt for Colombian scam comics — "Macondo" magical-realism watercolor inspired by Gabriel García Márquez's literary imagination, 2x2 grid, English speech bubbles. Paste verbatim into every Colombia scam generation.
type: project
---
Colombia country-scam comic style — chosen 2026-04-22 after a 5-way Colombian illustration bake-off (Fernando Botero voluminous-folk, "Macondo" magical-realism watercolor, Débora Arango social-realism, Alejandro Obregón expressionist-modernist, Museo del Oro pre-Columbian flat vector). **Macondo magical-realism watercolor selected** for its authentically Colombian cultural signal (Gabriel García Márquez is universally synonymous with Colombian literary imagination), warm tropical palette that distinguishes Colombia comics from neighboring Argentine/Brazilian books, lush blooming watercolor texture that reads beautifully at both screen and 258pp paperback print sizes, and flexible Caribbean-to-Andean regional adaptability across the five existing Colombian city pages.

**Locked STYLE block (paste verbatim at the top of every Colombia comic prompt):**

```
A single illustrated comic book page in the dreamlike magical-realism watercolor style evoking Gabriel García Márquez's 'Macondo' and the Caribbean-coastal Colombian literary imagination — delicate ink outlines with lush layered watercolor washes in a saturated tropical palette of papaya orange, Caribbean teal, mango yellow, hibiscus pink, and deep jungle green, soft blooming pigment edges, expressive dreamy faces, hints of butterflies and tropical foliage at panel edges, Macondo-era mid-20th-century nostalgia, literary storybook sensibility, warm humid Caribbean atmosphere adapted to the scam's actual Colombian setting (highland Bogotá colonial Candelaria, Medellín paisa hillsides, Cartagena walled-city colonial balconies, Cali salsa-city streets, Santa Marta Caribbean coastline — whichever fits). Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin cream gutters with subtle watercolor bleed. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black handwritten-looking lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{COLOMBIA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens in the scene, with Colombian landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson/CAI Turístico}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Pilot reference:** `https://img.tabiji.ai/scam-comics/co/style-tests/2-macondo-magical-realism-watercolor.jpg` (Bogotá Paseo Millonario express-taxi kidnapping × Harry)

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Colombian cities (existing): bogota, medellin, cartagena, cali, santa-marta
- Colombian cities (planned enrichment tier): guatape, salento, tayrona, san-andres, barranquilla (or san-gil)
- Typical: ~6 scams per city; generated via `scripts/comic-pipeline/generate.py colombia <city>...`
