---
name: Vietnam scam comic style block
description: Locked Nano Banana Pro style prompt for Vietnam scam comics — contemporary Vietnamese travel-comic with red lotus/cloud folk-art corner motifs. Paste verbatim into every Vietnam scam generation.
type: project
---
Vietnam scam comic style — locked 2026-04-26 to match the visual aesthetic of the 72 in-spec v1 Vietnam comics already live across all 12 cities (the 2026-04-26 sampling of `/scams/country/vn/` found remarkably consistent style across hanoi, ho-chi-minh-city, ha-long-bay, hoi-an, sapa, nha-trang, phu-quoc, with a single recurring female traveler protagonist, decorative red lotus/cloud corner motifs, and a saturated warm palette on cream-yellow paper). All 72 comics share one illustrator's hand, so we lock that aesthetic verbatim rather than run a fresh bake-off — new regens need to blend into the existing set, not replace it.

**Locked STYLE block (paste verbatim at the top of every Vietnam comic prompt):**

```
A single illustrated comic book page in a contemporary Vietnamese travel-comic style with decorative folk-art accents: bold confident black ink outlines with light cross-hatching, saturated warm palette of rust-red, mustard-yellow, ocean-teal, deep navy blue, and forest-green on a warm cream-yellow paper background, decorative red lotus-blossom and Vietnamese cloud-motif corner flourishes at panel edges, small red circle with white numeral 1, 2, 3, 4 in the corner of each panel, recurring female traveler protagonist (olive-green cargo shorts, rust-red short-sleeved shirt, dark navy wide-brim sun hat with sunglasses tucked into the band, backpack, smartphone) drawn with consistent everyday realism, detailed Vietnamese location backgrounds (Hanoi Old Quarter, Tan Son Nhat / Noi Bai airport gates, Halong Bay limestone karsts, Sapa rice terraces, Hoi An lantern-lit canals, Saigon Grab/Xanh SM rideshare cars, official ticket counters, rural rice paddies — whichever fits the scam's actual location), authentic Vietnamese-language signage where appropriate, warm tropical Vietnamese light. Showing four sequential panels arranged in a 2x2 grid separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rectangular speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{VIETNAM_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with location-accurate Vietnamese landmark/scenery}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson with safer-alternative app/official-counter}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Vietnamese cities (12): can-tho, da-nang, dalat, ha-long-bay, hanoi, ho-chi-minh-city, hoi-an, hue, nha-trang, ninh-binh, phu-quoc, sapa

**Pilot reference image:** `https://img.tabiji.ai/scams/ho-chi-minh-city/scam-1.jpg` (Ho Chi Minh City Tan Son Nhat Fake Grab Driver — an on-spec v1 Vietnam comic that cleanly exhibits the bold ink outlines, saturated cream-yellow palette, decorative red corner cloud motifs, and the recurring female traveler protagonist at an iconic Saigon airport setting)

**Why lock the existing v1 look rather than bake off a fresh Vietnamese-illustration style:**
- All 72 Vietnam comics are aesthetically coherent (one illustrator's hand) — fresh-baking would require redoing every image
- The contemporary travel-comic + folk-art-corner-motif look reads unmistakably as Vietnam without imposing a named-artist style
- If we ever want a named-artist Vietnamese style (e.g. lacquer-painting sơn mài, Đông Hồ folk-print woodblock, contemporary illustrators like Tạ Huy Long), that's a separate style-exploration exercise

**Style-specific notes:**
- The recurring female traveler protagonist appears in nearly every existing Vietnam comic. Per the cast pairing rules in `scripts/comic-pipeline/cast.py`, this character is closest to Priya (transit/haggle); some scams (trust, charm, observation) should use Margie/Harry/Marcus instead but should match the existing visual style.
- The decorative red lotus/cloud corner motifs are distinctive to Vietnam — keep them.
- Vietnamese-language signage (e.g. "TÂN SƠN NHẤT", "LÀO CAI TRAIN STATION", "NỘI BÀI ARRIVALS") is preferred over English-only signs for authenticity.
- Numbered red circles in panel corners (vs. plain numbers) are the Vietnam convention.
