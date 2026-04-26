---
name: Austria scam comic style block
description: Locked Nano Banana Pro style prompt for Austria country scam comics — Jean-Jacques Sempé pen-and-ink watercolor wash. Paste verbatim into every Austria scam generation.
type: project
---
Austria country-scam comic style — approved 2026-04-18 after 5-style side-by-side test (ligne claire, Klimt Secession, Schiele expressionist, Sempé, Moebius). Sempé chosen for its pen-and-ink + soft watercolor wash that matches Vienna's coffee-house intellectual sensibility and keeps tabiji's gentle observational voice over 8+ scams without feeling heavy (Schiele was too dark, Klimt too ornate at card size, ligne claire too generic-European, Moebius drifted toward #1 Tintin in the side-by-side).

**Locked STYLE block (paste verbatim at the top of every Austria comic prompt):**

```
A single illustrated comic book page in the pen-and-ink wash style of Jean-Jacques Sempé, showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin clean white gutters. Loose delicate pen linework with many fine lines and gentle cross-hatching, pale transparent watercolor washes adding soft color without overpowering the ink, tiny expressive figures set in expansive architectural settings, warm understated palette of cream, soft blue, pale rose, and muted ochre, gentle observational humor, quintessentially European coffee-house sensibility. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black lettering — text must be legible and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{AUSTRIA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens}. Speech bubble: "{short line, under ~8 words}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {realization / aftermath}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Pilot reference image:** `https://img.tabiji.ai/scams/vienna/scam-1.jpg` (Vienna Fake Mozart Ticket Sellers — bake-off winner from the 5-style side-by-side test, reused as scam-1)

**Vienna character rotation (applied 2026-04-18):**
- Scam 1 Fake Mozart Ticket Sellers → Margie (trust)
- Scam 2 Pickpockets U1 & Stephansplatz → Priya (transit)
- Scam 3 Airport Taxi Fixed-Price Shakedown → Priya (haggling)
- Scam 4 Fake Police ID Check → Harry (charm)
- Scam 5 Fake Apartment & Airbnb Listings → Margie (too trusting)
- Scam 6 Kärntner Strasse Cover Charge Creep → Harry (affable, charmed by waiter)
- Scam 7 Airport-Train Zone Trap 105-Euro Fine → Marcus (observant traveler with camera gear)
- Scam 8 Distraction Theft Flower/Bracelet/Munich → Margie (cheerful, too trusting)
- Distribution: Margie 3, Priya 2, Harry 2, Marcus 1 — Margie is headline per cast rules, all four cast members appear.

**Storage path (production):**
- R2 path: `scams/<city-slug>/scam-<N>.jpg` where N is the scam's 1-indexed position on the city page
- Public URL: `https://img.tabiji.ai/scams/<city-slug>/scam-<N>.jpg`
- HTML injection: `<img class="scam-comic" src="..." alt="<short title> — comic illustration" loading="lazy" style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;">` placed immediately after `<div class="scam-location">...</div>` inside each `<div class="scam-card">`

**Dialogue rules (same as Thailand):**
- Each bubble under ~8 words
- Use exclamation/question marks for reading rhythm
- Panel 4 is usually the realization
- Spell digits as words where it feels natural ("ten euros" > "10 euros") to avoid OCR-style mis-renders; spot-check each output

**How to apply:**
- Vienna comics generated 2026-04-18 using the Sempé block above
- For Salzburg (and any future Austrian city), use the same style block verbatim
- Pass 2–3 Vienna comic URLs as style anchors via `/edit` for Salzburg to keep Austria visually cohesive
