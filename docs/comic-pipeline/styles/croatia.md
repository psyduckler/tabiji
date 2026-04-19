---
name: Croatia scam comic style block
description: Locked Nano Banana Pro style prompt for Croatia country scam comics — Ivan Generalić / Hlebine School Croatian naïve-art classic period. Paste verbatim into every Croatia generation.
type: project
originSessionId: f4c6802a-d6fc-404e-b964-ffce1f0271c0
---
Croatia country-scam comic style — approved 2026-04-18 after a 3-variation test of Ivan Generalić periods (classic Hlebine oil-on-glass, earthy 1930s-50s, dramatic 1960s-70s). The classic Hlebine variant was chosen for best readability at web-card size while retaining the unmistakable Croatian folk-art DNA of Ivan Generalić (1914-1992), the most internationally-known Croatian naïve artist and co-founder of the Hlebine School.

**Locked STYLE block (paste verbatim at the top of every Croatia comic prompt):**

```
A single illustrated comic book page in the classic Hlebine School naïve-art style of Ivan Generalić (Croatia, 1914-1992), showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin clean white gutters. Painted in the traditional oil-on-glass technique — vivid saturated jewel-tone colors (crimson red, emerald green, cobalt blue, warm ochre, cream), flat folk-art perspective with all objects shown frontally, stylized figures with rounded blocky bodies and simplified faces, patiently detailed Croatian village setting with red-roofed stone houses and cypress trees, expressive folk-art sky with stylised scalloped clouds, quiet storybook mood, every surface filled with careful hand-painted pattern. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black lettering — text must be legible and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{CROATIA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from project_scam_comics_cast.md}

SCENE:
Panel 1: {what happens}. Speech bubble: "{short line, under ~8 words}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {realization / aftermath}. Speech bubble: "{short line}"
```

**API call — same Wavespeed Nano Banana Pro pipeline as Thailand / Austria / HK:**
- First comic in a city: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image` with `{prompt, aspect_ratio: "1:1", resolution: "2k", output_format: "jpeg"}`
- Later comics in the same city (for tighter consistency): `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` passing 2–3 prior approved comics as style anchors in the `images` array; `/edit` supports `aspect_ratio: "1:1"`
- Poll: `GET https://api.wavespeed.ai/api/v3/predictions/{id}/result` until `status=="completed"`
- Credential: `wavespeed-api-key` in macOS keychain

**Character rotation — Dubrovnik (applied 2026-04-18):**
- Scam 1 Port Gruž Cruise-Taxi Overcharge → Priya (transit/haggle)
- Scam 2 Old Town Menu Bait-and-Switch → Margie (trust, restaurant)
- Scam 3 Fake Apartment & Booking.com Hijack → Margie (too trusting)
- Scam 4 City Walls & Dubrovnik Pass Ticket Resellers → Harry (charm, easily charmed by a tout)
- Scam 5 Fake-QR-Code Parking Meter → Marcus (observer, has a rental car)
- Scam 6 Unlicensed Elafiti / Game of Thrones Tours → Harry (affable, follows tour pitch)
- Scam 7 Stradun Euronet ATM DCC Markup → Priya (haggling, would push back on DCC screen)
- Scam 8 Stradun & City Walls Pickpocket → Margie (cheerful in cruise crowd)

**Character rotation — Split (applied 2026-04-18):**
- Scam 1 Ferry Port 'Predator' Taxi → Priya (transit/haggle)
- Scam 2 SPU Airport & Kaštela Taxi → Priya (transit)
- Scam 3 Riva & Old Town Menu Trap → Margie (trust, restaurant)
- Scam 4 Bacvice 'Gentlemen's Club' Bill Trap → Harry (charm, follows promoter offer)
- Scam 5 Diocletian's Palace 'Legionary' Photo Fee → Marcus (DSLR camera, photo-fee scene)
- Scam 6 Jadrolinija & Krilo Ferry Ticket Tout → Harry (charmed by tout at kiosk)
- Scam 7 Old Town & Ferry Terminal Pickpocket → Margie (cheerful in ferry crowd)
- Scam 8 Split Apartment Booking.com Fraud → Margie (too trusting online)

**Total Croatia distribution**: Margie 6, Priya 4, Harry 4, Marcus 2 — all four cast members appear, Margie is headline across both cities.

**Storage path (production):**
- R2 path: `scams/<city-slug>/scam-<N>.jpg` where N is the scam's 1-indexed position on the city page
- Public URL: `https://img.tabiji.ai/scams/<city-slug>/scam-<N>.jpg`
- HTML injection: `<img class="scam-comic" src="..." alt="<short title> — comic illustration" loading="lazy" style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;">` placed immediately after `<div class="scam-location">...</div>` inside each `<div class="scam-card">`

**Dialogue rules (same as Thailand / Austria / HK):**
- Each bubble under ~8 words
- Use exclamation/question marks for reading rhythm
- Panel 4 is usually the realization
- Spell EUR amounts as words or use "€" prefix consistently ("sixty euros" over "60 euros" for the folk-art lettering); spot-check every output

**How to apply:**
- Dubrovnik comics generated 2026-04-18 using the classic Generalić block; scam-1 reused from the 3-variation test
- Split comics generated in parallel via `/edit` anchored to approved Dubrovnik comics for visual cohesion across the Croatia set
- For future Croatian cities (Hvar, Zagreb, Rovinj, Zadar, Pula), use the same style block verbatim and anchor to 2–3 existing Dubrovnik/Split comics via `/edit`
