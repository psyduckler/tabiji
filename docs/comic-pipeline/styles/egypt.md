---
name: Egypt scam comic style block
description: Locked Nano Banana Pro style prompt for Egypt scam comics — contemporary illustrated Egyptian travel-comic (warm watercolor + gouache). Paste verbatim into every Egypt scam generation.
type: project
---
Egypt scam comic style — locked 2026-04-26 after a 3-way Egyptian illustration bake-off (ancient Egyptian tomb-painting, 1920s Art Deco Egyptian-revival travel-poster, contemporary illustrated Egyptian travel-comic) at the Giza Camel-Hostage anchor scam. **Contemporary illustrated travel-comic selected** for its realistic character proportions and expressive faces (essential for showing the hostage-on-camel scam mechanic clearly), warm sand-gold/terracotta/Nile-blue palette that reads instantly as Egypt without leaning on either ancient-tomb pastiche or 1920s-deco nostalgia, painterly painterly visible texture that scales well from mobile thumbnail to print, and modern legibility for safety-warning signage (Tourist Police uniforms, hieroglyph-etched stelae as background detail).

**Locked STYLE block (paste verbatim at the top of every Egypt comic prompt):**

```
A single illustrated comic book page in a contemporary illustrated Egyptian travel-comic style: confident fine black ink outlines with richly digital-painted watercolor-and-gouache fills, realistic character proportions and expressive faces, visible painterly texture, detailed Egyptian location backgrounds — golden Giza desert plateau with the pyramids of Khufu, Khafre, and Menkaure rendered in warm sandstone, the Sphinx in soft afternoon light, decorative camels with red-and-orange tasseled saddles, Tourist Police kiosks with the distinctive teal-and-white Egyptian uniform, hieroglyph-etched stelae as background details — palette of sand-gold, terracotta, Nile-blue, and cream. Egyptian figures in light galabeyas alongside modern travelers. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin clean black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{EGYPT_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Egyptian landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson at Tourist Police kiosk}. Speech bubble: "{short line}"
```

**API call:**
- Primary: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with the pilot URL below as style anchor
- Fallback: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Egyptian cities: alexandria, aswan, cairo, hurghada, luxor, sharm-el-sheikh

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/eg/style-tests/modern-cairo-illustrated.jpg` (Giza Camel-Hostage × Marcus — bake-off winner)

**Why contemporary illustrated over the other 2 candidates:**
- **Hieroglyphic tomb-painting** — strongest heritage-anchor but the flat-profile-figure ancient-tomb aesthetic struggled to depict the hostage-on-camel intimidation moment with the urgency the scam-warning narrative needs
- **Art Deco Egyptian-revival 1920s travel-poster** — beautiful gold/turquoise palette but the streamlined deco simplification flattened character expression too much; reads as "vintage travel romance" rather than "modern safety warning"
- **Contemporary illustrated (LOCKED)** — modern realism + warm Egyptian palette + clear scam-mechanic depiction + readable Tourist Police signage + scales across all 6 Egypt cities (Cairo/Giza, Alexandria, Luxor, Aswan, Hurghada, Sharm el-Sheikh)
