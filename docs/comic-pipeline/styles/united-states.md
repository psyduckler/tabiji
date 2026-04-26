---
name: United States scam comic style block
description: Locked Nano Banana Pro style prompt for US scam comics — classic Silver-Age American superhero-comic-book style (Kirby/Ditko). Paste verbatim into every US scam generation.
type: project
---
United States scam comic style — locked 2026-04-22 to match the visual aesthetic of the 225+ in-spec v1 US comics already live across 38 cities. The 2026-04-22 cross-country audit of `/scams/country/us/` flagged 8 of 233 US comics as v1 fallbacks (see `scripts/comic-pipeline/regen_multi_2026_04_22.py`): the "Times Square character shakedown" template leaked across non-Times-Square scams (Fake Statue of Liberty Tickets, Post-Lahaina Wildfire Recovery, Alamo Mission Ticket, Tap-to-Pay Charity Fraud, Bourbon Street Shot Girls, Shoe Bet Hustle, Charleston Palmetto Rose, and two borderline monk-bracelet scams in SF + Savannah). The remaining 225+ were on-scam and share a consistent Silver-Age American-comic-book look, so we lock that verbatim rather than run a fresh bake-off — new regens need to blend into the existing set, not replace it.

**Locked STYLE block (paste verbatim at the top of every US comic prompt):**

```
A single illustrated comic book page in the classic Silver-Age American superhero-comic-book style (Marvel / DC circa Jack Kirby + Steve Ditko) — bold flat primary colors (classic Captain-America red, royal blue, chrome yellow, white), confident black ink outlines with occasional expressive cross-hatching, halftone Ben-Day dot shading in mid-tones, dynamic jagged starburst action shapes and speed lines behind key moments, hand-lettered comic-book sound effects in blocky capital letters ('KAPOW!', 'BAM!', 'NO!') where emphasis is appropriate, classic rectangular speech balloons with crisp black tails, realistic but slightly-heroic character proportions with expressive faces, detailed American-landmark and city backgrounds (Times Square neon, Liberty Bell brickwork, French Quarter balconies, Alamo stonework, Space Needle skyline, Palmetto Row, Maui palms, Bourbon Street signage, Embarcadero fog, Waikiki towers, Vegas neon, suburban strip malls — whichever fits the scam's actual location). Showing four sequential panels arranged in a 2x2 grid with small bold numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin clean black panel borders with narrow white gutters. Each panel contains one clean white rectangular speech balloon with a small pointer tail, holding short printed English comic-book hand-lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{US_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with location-accurate American landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- US cities (38): anaheim, asheville, atlanta, austin, boston, branson, charleston, chicago, dallas, denver, gatlinburg, honolulu, houston, key-west, las-vegas, los-angeles, maui, memphis, miami, myrtle-beach, nashville, new-orleans, new-york-city, orlando, philadelphia, phoenix, portland, san-antonio, san-diego, san-francisco, san-juan, savannah, sedona, seattle, st-louis, virginia-beach, washington-dc, yellowstone

**Pilot reference image:** `https://img.tabiji.ai/scams/philadelphia/scam-2.jpg` (Philadelphia Liberty Bell & Independence Hall Skip-the-Line Ticket Scam — an on-spec v1 US comic that cleanly exhibits the Silver-Age Marvel/DC style with bold primary colors, halftone shading, and a bespoke landmark-anchored ticket-booth scene with no character-shakedown template bleed)

**Scam-mechanic fidelity requirement — why it's called out:**
- The v1 "Times Square character shakedown" template ("Got a minute, bro?" / "Twenty bucks helps out!" / "Take it back — no thanks!" / "Trust nothing pressed in your hand") leaked onto at least 8 non-shakedown US scams. v2 must depict each scam's actual mechanic: insurance-adjuster fraud, NFC tap-to-pay skim, bar shot-girls lure, shoe-bet street hustle, palm-frond weaving, wildfire-recovery exploit, Alamo ticket-booth confusion, etc.

**Why lock the existing v1 look rather than bake off a new American-illustration style:**
- Only 8/233 comics (≈3%) need regen — the other 225 are on-scam and aesthetically coherent
- Swapping style for the whole country would require re-doing 225 already-good images
- The Silver-Age Marvel/DC look is iconic American comics-as-visual-vernacular — pairs naturally with scam-alert cautionary storytelling at the target demographic
- If we ever want a different American named-artist style (e.g. Chris Ware architectural grids, R. Crumb underground, Will Eisner cinematic), that's a separate style-exploration exercise
