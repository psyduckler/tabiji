---
name: Japan scam comic style block
description: Locked Nano Banana Pro style prompt for Japan scam comics — contemporary illustrated travel-comic (neon night + warm day). Paste verbatim into every Japan scam generation.
type: project
---
Japan scam comic style — locked 2026-04-21 to match the visual aesthetic of the 49 in-spec v1 Japan comics already live across 9 cities. The 2026-04-21 audit of `/scams/country/jp/` flagged 5 of 54 comics as problematic (see `scripts/comic-pipeline/regen_japan.py`): the Japan damage was dominated by location-tag drift on the bar-tout template (Roppongi signage leaking into Fukuoka/Sapporo scenes, Shibuya signage into Kabukicho scenes) plus one pixel-identical duplicate across two cities (fukuoka-1 ≡ sapporo-1) and one wrong-mechanism comic (sapporo-6). The remaining 49 were on-scam and share a consistent warm contemporary illustrated-travel-comic look, so we lock that verbatim rather than run a fresh manga/ukiyo-e bake-off — new regens need to blend into the existing set, not replace it.

**Locked STYLE block (paste verbatim at the top of every Japan comic prompt):**

```
A single illustrated comic book page in a warm contemporary illustrated-travel-comic style: confident fine black ink outlines with richly digital-painted watercolor-and-gouache fills, realistic character proportions and expressive faces, visible painterly texture, detailed Japanese location backgrounds — neon-lit nightlife alleys (Shinjuku, Dotonbori, Susukino, Nakasu) rendered in vivid magenta, cyan, warm amber, and reflected-puddle cobalt against dark wet pavement; daytime exteriors (Kyoto temple streets, Nara Park, Miyajima torii, suburban train stations, Koban police boxes, Japanese convenience-store and vending-machine signage) rendered in warm natural light with soft blues, cherry pink, lantern red, and cream. Traveler figures in modern casual clothing alongside Japanese characters — salarymen in dark suits, bar touts in slim black suits, kimono-clad hostesses and temple visitors, uniformed Koban police, ramen cooks, deer-feeding visitors, monks — each drawn with everyday realism. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin clean black panel borders with narrow white gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Japanese neon and signage in the background must be location-accurate for the scam's specific district (no Roppongi signage on Fukuoka/Sapporo scenes, no Shibuya signage on Kabukicho scenes). Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{JAPAN_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from cast.md}

SCENE:
Panel 1: {what happens, with location-accurate Japanese landmark/signage}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson at a Koban or with a lesson banner}. Speech bubble: "{short line}"
```

**API call:**
- Subsequent comics: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback on failure: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Japanese cities: fukuoka, hiroshima, kyoto, nara, okinawa, osaka, sapporo, tokyo, yokohama

**Pilot reference image:** `https://img.tabiji.ai/scams/tokyo/scam-3.jpg` (Tokyo English Conversation / Student Scam — an on-spec v1 Japan comic that cleanly exhibits the warm daytime illustration style with multi-character interaction and a Koban lesson panel)

**Location-accuracy requirement — why it's called out in the STYLE block:**
- The v1 bar-tout template mis-rendered district signage (Roppongi neon appeared on Fukuoka Nakasu + Sapporo Susukino scenes; Shibuya neon on Tokyo Kabukicho scenes). v2 must keep district-specific signage true to the scam's actual location.

**Why lock the existing v1 look rather than bake off a new Japanese-illustration style:**
- Only 5/54 comics (≈9%) need regen — the other 49 are on-scam and aesthetically coherent
- Swapping style for the whole country would require re-doing 49 already-good comics
- The contemporary-travel-comic look is neutral and location-specific (neon nightlife / temple daytime) — culturally anchored without imposing a named-artist interpretation
- If we ever want to re-do the whole country with a named-artist style (manga, Yoshitomo Nara, ukiyo-e, Shuji Terayama-era poster aesthetic), that's a separate style-exploration exercise
