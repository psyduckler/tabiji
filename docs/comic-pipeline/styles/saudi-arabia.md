---
name: Saudi Arabia scam comic style block
description: Locked Nano Banana Pro style prompt for Saudi Arabia scam comics — contemporary illustrated Gulf travel-comic with Najd-pink heritage accents. Paste verbatim into every Saudi Arabia scam generation.
type: project
---
Saudi Arabia scam comic style — locked 2026-04-26 after a 3-way Saudi illustration bake-off (Najdi mud-architecture heritage, 1960s ARAMCO-era travel-poster modernism, contemporary illustrated Gulf travel-comic) at the Riyadh Broken-Meter Taxi anchor scam. **Contemporary illustrated Gulf travel-comic selected** for its modern realism (essential for depicting Riyadh's Kingdom Tower and contemporary taxi/Careem scam mechanics), warm sand/cobalt/terracotta palette that reads identifiably as Saudi without leaning on either heritage-pastiche or 1960s-poster nostalgia, restrained tasteful composition appropriate to Saudi cultural sensibilities, and the visual flexibility to span Riyadh modern-skyline + Diriyah heritage-pink + Jeddah coastal scenes across the existing 3-city set.

**Locked STYLE block (paste verbatim at the top of every Saudi Arabia comic prompt):**

```
A single illustrated comic book page in a contemporary illustrated Gulf travel-comic style: confident fine black ink outlines with richly digital-painted gouache fills, realistic character proportions and expressive faces, visible painterly texture, detailed Saudi Arabian location backgrounds — Riyadh Kingdom Tower silhouette at dusk, King Khalid International Airport curved white roofs, beige modernist taxi ranks, Riyadh palm-lined boulevards, Najd-style salmon-pink heritage neighborhoods — palette of warm sand, golden cream, deep cobalt night sky, terracotta, and accent palm-green. Saudi figures in white thobes and red-checkered shemaghs and women in modest abayas alongside modern international travelers, restrained tasteful composition appropriate to Saudi cultural sensibilities. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin clean black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{SAUDI_ARABIA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Saudi landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson with Careem app or official rank}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Saudi cities: jeddah, mecca, riyadh

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/sa/style-tests/contemporary-gulf-illustrated.jpg` (Riyadh Broken-Meter Taxi × Priya — bake-off winner)

**Why contemporary Gulf illustrated over the other 2 candidates:**
- **Najdi mud-architecture heritage** — strongest cultural-heritage anchor but the salmon-pink earth-tone palette and traditional-architecture detail didn't render Riyadh's modern airport-and-Kingdom-Tower scam locations clearly; better suited to Diriyah-only scenes
- **ARAMCO 1960s travel-poster** — handsome mid-century deco but the period nostalgia clashed with depicting modern Careem-app and contemporary scam mechanics
- **Contemporary Gulf illustrated (LOCKED)** — modern realism + Saudi-coded palette + scales across modern Riyadh + Mecca + Jeddah + heritage-Najd accents + culturally tasteful composition
