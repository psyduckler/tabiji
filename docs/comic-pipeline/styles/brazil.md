---
name: Brazil scam comic style block
description: Locked Nano Banana Pro style prompt for Brazilian scam comics — Aldemir Martins folk-modernist painting. Paste verbatim into every Brazil scam generation.
type: project
---
Brazil scam comic style — Aldemir Martins (1950s-70s Ceará-born Brazilian painter of cangaceiros, cats, and nordestino folk figures) folk-modernist painting, chosen 2026-04-20 after a 4-way Brazilian illustration bake-off against (1) Literatura de Cordel xilogravura, (2) Tarsila do Amaral 1920s modernism, (3) J. Carlos carioca watercolour. Aldemir Martins chosen for its combination of visual punch (bold primary-colour blocks with decorative sun and star motifs), strong Brazilian cultural anchor (Ceará nordestino lineage, same regional root as Cordel but painted rather than carved), landmark-readability (Brazilian architecture, skylines, signage render clearly), and book-ready maturity appropriate for the 55+ demographic.

**Locked STYLE block (paste verbatim at the top of every Brazil comic prompt):**

```
A single illustrated comic book page in the folk-modernist painting style of Aldemir Martins (1950s-70s Brazilian painter of cangaceiros, cats, and Ceará folk figures) — bold flat primary-color blocks with confident black ink outlines, vibrant nordestino palette of scarlet red, royal blue, chrome yellow, bright green, and black, stylized folk figures with geometric simplification and expressive gesture, decorative background patterns of stars and sun motifs, strong graphic weight, Ceará-born Brazilian folk-modernism aesthetic. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow white gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English comic-book lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{BRAZIL_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from cast.py}

SCENE:
Panel 1: {what happens, with Brazilian landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson}. Speech bubble: "{short line}"
```

**API call:**
- First Brazil comic: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Subsequent: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with pilot as anchor
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Brazilian cities: rio-de-janeiro, buzios, paraty, sao-paulo, florianopolis, salvador, recife, fortaleza, manaus, foz-do-iguacu, brasilia, ouro-preto

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/br/style-tests/4-aldemir-martins-folk-modernist.jpg` (Priya + Salvador SSA airport taxi)

**Why Aldemir Martins over the other 3 candidates:**
- **Literatura de Cordel xilogravura (option 1)** — strongest nordestino print weight and closest analogue to the locked Indonesia Lontar style. Eliminated for being too austere (B&W woodcut) — the book-ready Brazilian reference set should show off Brazilian colour heritage, not suppress it
- **Tarsila do Amaral modernism (option 2)** — beautiful flat-colour 1920s Brazilian modernism with strong landmark rendering, but the stylised rounded figure geometry sacrifices some comic-panel narrative clarity
- **J. Carlos carioca watercolour (option 3)** — sophisticated 1920s-40s Rio magazine illustration with soft sepia/teal washes; loses Brazilian punch in favour of New Yorker-style restraint — didn't feel distinctively Brazilian enough
- **Aldemir Martins folk-modernist (option 4, LOCKED)** — bold primary-colour blocks + decorative sun/star motifs feel actively nordestino while remaining narratively clear and book-ready. Renders Brazilian landmarks (Salvador cathedral, São Paulo skyline, Pelourinho streets) with strong graphic punch. Matches the "mature cautionary-tale with cultural weight" bar set by the locked Indonesia Lontar and China Feng Zikai styles while contributing colour energy missing from those two
