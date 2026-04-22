---
name: Australia scam comic style block
description: Locked Nano Banana Pro style prompt for Australia scam comics — Percy Trompf / Gert Sellheim 1930s-50s "Come to Australia" art-deco travel poster. Paste verbatim into every Australia scam generation.
type: project
---
Australia scam comic style — locked 2026-04-22 after a 5-way bake-off at the Sydney Bondi Beach bag-theft anchor scam. Selection: **Percy Trompf / Gert Sellheim 1930s-50s Australian art-deco travel-poster** style, for the strongest travel-identity fit, clean mobile readability, and versatility across the 14-city range (coastal, outback, city, island).

**Bake-off candidates tested** (see `scam-comics/au/style-tests/`):

| # | Style | Outcome |
|---|---|---|
| 1 | Ken Done Sydney Harbour pop | Runner-up — bright and distinctly Sydney, but 1980s-souvenir flavour less versatile for Hobart/Canberra |
| 2 | Michael Leunig whimsical pen-and-ink | Warm/gentle, but understated against competing photo content |
| 3 | May Gibbs Australian bush watercolor | Beautiful flora borders, but risks reading as children's-book only |
| 4 | **Percy Trompf art-deco travel poster ← CHOSEN** | Strongest travel-identity anchor, clean mobile readability, works for coastal / outback / city / island |
| 5 | Pro Hart outback folk oil | Distinctly Australian painterly, but impasto texture loses at mobile thumbnail size |

**Locked STYLE block (paste verbatim at the top of every Australia comic prompt):**

```
A single illustrated comic book page in the bold Australian art-deco travel-poster style of Percy Trompf and Gert Sellheim (1930s-50s 'Come to Australia' / 'Australia — Land of Sunshine' posters) — bold flat simplified graphic shapes with crisp black outlines, streamlined modernist composition, sun-drenched saturated palette of sky blue, turquoise ocean, golden sand, warm red ochre, and cream, stylized 1930s travelers and local Australian scenery (Sydney Opera House, Harbour Bridge, Bondi crescent, Melbourne trams, Great Barrier Reef, Uluru red monolith, Tasmanian sandstone, outback scrub, kangaroo and kookaburra silhouettes, gum-leaf motifs — whichever fits the scam's actual location), confident hand-stenciled travel-poster typography, cheerful advertising optimism, clean legible layout. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in art-deco stencil-style black lettering — text must be legible, in English only, and correctly spelled. Do NOT add any footer or caption banner outside the four panels — the comic must be exactly the 2x2 grid with no additional text, tagline, or banner below. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{AUSTRALIA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from cast.md}

SCENE:
Panel 1: {setup, with location-accurate Australian landmark/scenery}. Speech bubble: "{short line}"
Panel 2: {scam mechanic happens}. Speech bubble: "{short line}"
Panel 3: {realization / pushback}. Speech bubble: "{short line}"
Panel 4: {lesson / safer alternative — usually at a safer venue, with Australian location cue}. Speech bubble: "{short line}"
```

**API call:**
- Subsequent comics: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback on failure: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Australian cities (14): sydney, melbourne, brisbane, perth, adelaide, hobart, darwin, canberra, cairns, gold-coast, byron-bay, alice-springs, whitsundays, port-douglas
- 6 scams per city → 84 comics total

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/au/style-tests/4-trompf-art-deco-travel-poster.jpg` (the approved bake-off winner — Sydney Bondi Beach bag-theft scam with Marcus)

**Location-accuracy requirement — why it's called out in the STYLE block:**
- Australia's 14 cities cover radically different landscapes — Sydney Harbour vs. Uluru red monolith vs. Tasmanian sandstone vs. tropical Port Douglas mangroves
- The STYLE block lists the location cues the model should use; Gemini's synthesized scene for each scam must name the specific local landmark (e.g. "Bondi crescent", "Flinders Street Station clocks", "Uluru silhouette", "Port Douglas marina") for the image to read as authentic
- The Indigenous Art Code mention in Alice Springs scams is respected — the travel-poster style is not Indigenous-art pastiche, so we avoid appropriation concerns

**Style-specific gotcha:**
- The bake-off winner image (pilot) has a decorative "BONDI BEACH — COME TO AUSTRALIA! VISIT THE LAND OF SUNSHINE" footer banner outside the 4 panels. This is a period-accurate travel-poster flourish but is NOT wanted on subsequent comics. The STYLE block explicitly instructs "Do NOT add any footer or caption banner outside the four panels" — watch for regressions on this in quality review.
