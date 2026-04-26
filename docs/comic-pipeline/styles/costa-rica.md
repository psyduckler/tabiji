---
name: Costa Rica scam comic style block
description: Locked Nano Banana Pro style prompt for Costa Rica scam comics — 1950s Pan American Airways tropical-deco travel-poster. Paste verbatim into every Costa Rica scam generation.
type: project
---
Costa Rica scam comic style — locked 2026-04-22 after a 5-way bake-off (on both Nano Banana Pro and GPT Image 2) at the Manuel Antonio "Fake Park Ranger" Route 618 roadblock anchor scam. Selection: **1950s Pan American Airways tropical-deco Costa Rica travel-poster** style, for the strongest travel-identity fit, clean mobile readability, versatility across the 8-city range (Central Valley, Caribbean, North Pacific, Central Pacific, cloud forest), and distinctiveness from Australia's Percy Trompf deco (shared aesthetic lineage but tropical palette vs. Australia's coastal/outback).

**Bake-off candidates tested on both NBP and GPT Image 2** (see `scam-comics/cr/style-tests/`):

| # | Style | Outcome |
|---|---|---|
| 1 | Paco Amighetti woodcut modernism | Runner-up — deep CR art-heritage anchor, but B&W/terracotta palette reads colder than the warm travel-guide tone |
| 2 | Carreta típica folk-geometric | Most-instantly-Tico visual, but ornate carreta borders compete with panel content at mobile thumbnail size |
| 3 | Henri Rousseau tropical-jungle primitivist | Beautiful biodiversity rendering, but French (not Tico) heritage and dreamlike tone reads quieter than needed |
| 4 | Francisco Zúñiga humanist modernism | Warm character-forward CR-born artist, but earth-tone palette gets lost against photo content |
| 5 | **1950s Pan-Am tropical-deco travel poster ← CHOSEN** | Strongest travel-identity anchor, clean mobile readability, tropical palette clearly distinct from Australia Trompf |

**Engine:** the CR batch uses the same production **Nano Banana Pro via Wavespeed** pipeline as every other country. GPT Image 2 was tested during bake-off for comparison only — it produced competent renders at ~6.6× cost per image and no multi-image `edit` anchoring, so NBP stays the production engine.

**Locked STYLE block (paste verbatim at the top of every Costa Rica comic prompt):**

```
A single illustrated comic book page in the vivid 1950s tropical art-deco travel-poster style used by Pan American Airways for Central America routes — bold flat simplified graphic shapes with crisp black outlines, streamlined modernist composition, sun-drenched tropical palette of deep turquoise Pacific, emerald jungle, volcano red-orange, banana yellow, tropical magenta, and cream, stylized 1950s travelers and location-accurate Costa Rican scenery (Arenal volcano cone, Manuel Antonio beach coves, palm silhouettes, SINAC ranger stations, carreta oxcart wheels, toucans and sloths — whichever fits the scam's actual location), confident hand-stenciled travel-poster typography, cheerful mid-century advertising optimism, clean legible layout. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in art-deco stencil-style black lettering — text must be legible, in English only, and correctly spelled. Do NOT add any footer or caption banner outside the four panels — the comic must be exactly the 2x2 grid with no additional text, tagline, or banner below. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{COSTA_RICA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {setup, with location-accurate Costa Rican landmark/scenery}. Speech bubble: "{short line}"
Panel 2: {scam mechanic happens}. Speech bubble: "{short line}"
Panel 3: {realization / pushback}. Speech bubble: "{short line}"
Panel 4: {lesson / safer alternative — usually at a Fuerza Pública / SINAC / ICT-certified operator / Caribe Shuttle / Interbus / hotel safe, with CR location cue}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Costa Rican cities (8): san-jose-costa-rica, tamarindo, manuel-antonio, la-fortuna, puerto-viejo-costa-rica, liberia-costa-rica, jaco-costa-rica, monteverde
- 5–7 scams per city → 54 comics total (7 × 7 cities + 5 Monteverde)

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/cr/style-tests/nbp-5-tropical-deco-travel-poster.jpg` (the approved bake-off winner — Manuel Antonio "Fake Park Ranger" scam with Harry)

**Bake-off gallery** (preserved for "why this style?" lookups):

| # | Engine | Style | URL |
|---|---|---|---|
| 1 | NBP | Amighetti woodcut | `scam-comics/cr/style-tests/nbp-1-amighetti-woodcut.jpg` |
| 2 | NBP | Carreta folk-geometric | `scam-comics/cr/style-tests/nbp-2-carreta-folk-geometric.jpg` |
| 3 | NBP | Rousseau tropical | `scam-comics/cr/style-tests/nbp-3-rousseau-tropical-primitivist.jpg` |
| 4 | NBP | Zúñiga humanist | `scam-comics/cr/style-tests/nbp-4-zuniga-humanist-mesoamerican.jpg` |
| 5 | NBP | **Tropical-deco travel poster ← CHOSEN** | `scam-comics/cr/style-tests/nbp-5-tropical-deco-travel-poster.jpg` |
| 1 | GPT2 | Amighetti woodcut | `scam-comics/cr/style-tests/gpt-1-amighetti-woodcut.jpg` |
| 2 | GPT2 | Carreta folk-geometric | `scam-comics/cr/style-tests/gpt-2-carreta-folk-geometric.jpg` |
| 3 | GPT2 | Rousseau tropical | `scam-comics/cr/style-tests/gpt-3-rousseau-tropical-primitivist.jpg` |
| 4 | GPT2 | Zúñiga humanist | `scam-comics/cr/style-tests/gpt-4-zuniga-humanist-mesoamerican.jpg` |
| 5 | GPT2 | Tropical-deco travel poster | `scam-comics/cr/style-tests/gpt-5-tropical-deco-travel-poster.jpg` |

**Location-accuracy requirement — why it's called out in the STYLE block:**
- Costa Rica's 8 cities span radically different landscapes — Central Valley colonial urban vs. Caribbean sandy coast vs. Guanacaste dry-tropics airport vs. Manuel Antonio jungle-beach vs. Monteverde cloud-forest
- The STYLE block lists the location cues the model should use; Gemini's synthesized scene for each scam must name the specific local landmark (e.g. "Arenal volcano cone", "Manuel Antonio SINAC ranger station", "Puerto Viejo palm-lined beach", "LIR Daniel Oduber airport", "Monteverde cloud-forest canopy") for the image to read as authentic
- CR's biodiversity (sloths, toucans, macaws) and carreta oxcart heritage are explicitly named so the model can sprinkle them into appropriate panels without being forced everywhere

**Style-specific gotchas:**
- The style block explicitly forbids footer/caption banners outside the 2x2 grid. The pilot image has no footer — watch for regressions on this in quality review.
- Do NOT conflate with Australia's Trompf deco — palettes are intentionally different (Australia: ochre/sky-blue desert-coastal; Costa Rica: turquoise/emerald/volcano-red tropical). Both are period-accurate travel-poster aesthetics but target different tropical/desert territories.
