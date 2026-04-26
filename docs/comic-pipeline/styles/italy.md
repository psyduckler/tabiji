---
name: Italy scam comic style block
description: Locked Nano Banana Pro style prompt for Italy scam comics — warm hand-drawn travel-sketchbook cartoon (pencil + watercolor wash). Paste verbatim into every Italy scam generation.
type: project
---
Italy scam comic style — locked 2026-04-26 to match the visual aesthetic of the 107 in-spec v1 Italy comics already live across 20 cities (the 2026-04-26 sampling of `/scams/country/it/` found a consistent dominant style across pompeii, verona, venice, taormina, siena, pisa, palermo, naples, lake-garda, capri, sardinia, rome, milan, florence — soft pencil + warm watercolor wash with a recurring straw-hat protagonist and yellow title banner). One outlier (rome scam-1, slightly more saturated bold-comic look) exists; new regens follow the dominant pencil-watercolor style rather than the outlier. We lock that aesthetic verbatim rather than run a fresh bake-off — new regens need to blend into the existing set, not replace it.

**Locked STYLE block (paste verbatim at the top of every Italy comic prompt):**

```
A single illustrated comic book page in a warm hand-drawn travel-sketchbook cartoon style: soft pencil linework with subtle cross-hatching and gentle shading, light watercolor washes in a muted Italian palette of cream, terracotta, sandstone, sky blue, warm ochre, and pale rose, friendly cartoon character figures with simple expressive faces, recurring traveler protagonist (light-blue polo shirt, beige shorts, white straw hat with brown band, backpack, camera) drawn with consistent everyday realism, detailed Italian location backgrounds (Colosseum, Duomo di Milano, Leaning Tower of Pisa, Trevi Fountain, Vesuvius silhouette, Florence Duomo, Pompeii ruins, Venetian canals and gondolas — whichever fits the scam's actual location), warm Mediterranean sunlight. The page is topped by a horizontal yellow title banner spanning the full width, holding the scam name in all-caps brown serif lettering; a small location label appears in the corner of panel 1 (e.g. 'ROME, ITALY:' or 'FLORENCE, ITALY - Piazza del Duomo'); the final panel contains a small yellow PRO TIP callout box in the lower corner with one line of safety advice. Showing four sequential panels arranged in a 2x2 grid separated by thin black panel borders with narrow white gutters. Each panel contains one clean white rectangular speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{ITALY_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with location-accurate Italian landmark/scenery}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson, with PRO TIP callout}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Italian cities (20): amalfi-coast, bologna, capri, cinque-terre, florence, lake-como, lake-garda, milan, naples, palermo, pisa, pompeii, positano, rome, sardinia, siena, sorrento, taormina, venice, verona

**Pilot reference image:** `https://img.tabiji.ai/scams/pisa/scam-1.jpg` (Pisa Campo dei Miracoli Bracelet & Rose Ambush — an on-spec v1 Italy comic that cleanly exhibits the soft pencil + warm watercolor look with a recognizable Italian landmark, the recurring straw-hat protagonist, the yellow title banner, and the lower-corner PRO TIP callout)

**Why lock the existing v1 look rather than bake off a fresh Italian-illustration style:**
- All 107 Italy comics are aesthetically coherent (one outlier at rome scam-1) — fresh-baking would require redoing 106 already-good images
- The hand-drawn travel-sketchbook look reads unmistakably as a tabiji travel-comic without imposing a named-artist style
- If we ever want a named-artist Italian style (e.g. Hugo Pratt Corto Maltese, Milo Manara, fumetti, Alberto Sordi-era poster aesthetic), that's a separate style-exploration exercise

**Style-specific notes:**
- The yellow horizontal title banner across the top is distinctive to Italy and absent from every other country. Future regens must include it.
- The lower-corner PRO TIP callout in panel 4 is also distinctive — keep it.
- Panel numbers are NOT used (unlike most countries) — the title banner and natural reading order convey sequence.
- The recurring straw-hat protagonist appears in nearly every existing Italy comic regardless of which canonical cast member the scam pairs with. New regens should keep this visual continuity unless the cast pairing rule explicitly demands a different protagonist.
