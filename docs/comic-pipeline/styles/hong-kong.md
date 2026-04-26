---
name: Hong Kong scam comic style block
description: Locked Nano Banana Pro style prompt for Hong Kong / China country scam comics — 1960s-70s Shaw Brothers painted cinema-poster style. Paste verbatim into every HK generation.
type: project
---
Hong Kong country-scam comic style — approved 2026-04-18 after a 5-style side-by-side test (Tony Wong manhua, Tsai Chih Chung ink-wash, Wong Kar-Wai neon-cinematic, Shaw Brothers poster, Old Master Q). Shaw Brothers chosen for its painterly gouache texture, jade/crimson/gold palette, and unmistakably Hong Kong cinematic feel — distinct from both Thailand watercolor and a future Japan manga lock. Reusable for other Chinese cities (Beijing, Shanghai, Chengdu, etc.) since the Shaw Brothers visual is pan-Chinese rather than strictly Cantonese.

**Locked STYLE block (paste verbatim at the top of every Hong Kong / China comic prompt):**

```
A single illustrated comic book page in the bold painted-poster style of 1960s-1970s Shaw Brothers Hong Kong cinema posters, showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin clean white gutters. Painted gouache-on-board technique with confident brushed edges, high-contrast saturated color fields of jade green, crimson red, golden yellow, and royal blue, dramatic low-angle compositions with characters leaning into the frame, stylized cinematic framing as if every panel is a movie-poster still, warm retro paper grain. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black lettering — text must be legible and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{HONG_KONG_STYLE_BLOCK}

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

**Hong Kong character rotation (applied 2026-04-18):**
- Scam 1 Airport & Peak Tram Taxi Overcharge → Priya (transit/haggle)
- Scam 2 Peninsula Centre Fake-Watch-Repair Shop → Harry (elder, brings luxury piece for service)
- Scam 3 Tsim Sha Tsui & CWB Fake Monks → Margie (trust/bracelet)
- Scam 4 Mong Kok & Ladies' Market Counterfeit Run → Marcus (observer with camera)
- Scam 5 Mong Kok 'Massage' Wallet Theft → Harry (chatty / follows offer upstairs)
- Scam 6 MTR Pickpocket Ring → Priya (transit)
- Scam 7 Peak Tram Phishing Website → Margie (trusts online deal)
- Scam 8 Tsim Sha Tsui Tailor Deposit → Margie (trusts rush tailor)
- Distribution: Margie 3, Priya 2, Harry 2, Marcus 1 — Margie is headline per cast rules, all four cast members appear.

**Storage path (production):**
- R2 path: `scams/<city-slug>/scam-<N>.jpg` where N is the scam's 1-indexed position on the city page
- Public URL: `https://img.tabiji.ai/scams/<city-slug>/scam-<N>.jpg`
- HTML injection: `<img class="scam-comic" src="..." alt="<short title> — comic illustration" loading="lazy" style="width:100%;height:auto;border-radius:12px;margin:1rem 0 1.25rem;display:block;">` placed immediately after `<div class="scam-location">...</div>` inside each `<div class="scam-card">`

**Dialogue rules (same as Thailand / Austria):**
- Each bubble under ~8 words
- Use exclamation/question marks for reading rhythm
- Panel 4 is usually the realization
- Spell HKD amounts as words or use "HK$" prefix consistently ("six hundred" > "600" for legibility); spot-check every output

**How to apply:**
- Hong Kong comics generated 2026-04-18 using the Shaw Brothers block above; scam-1 reused from the 5-style test
- For future Chinese cities (Macau, Beijing, Shanghai, Chengdu, Xi'an), use the same style block verbatim
- Pass 2–3 Hong Kong comic URLs as style anchors via `/edit` for the next Chinese city to keep the regional look cohesive
