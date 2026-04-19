---
name: Indonesia scam comic style block
description: Locked Nano Banana Pro style prompt for Indonesian scam comics — Balinese Lontar palm-leaf manuscript illustration. Paste verbatim into every Indonesia scam generation.
type: project
originSessionId: 6e1b60d6-8114-4bf8-83d3-25c3a4635638
---
Indonesia scam comic style — chosen 2026-04-18 after a 5-way Indonesian illustration bake-off (Wayang Kulit shadow-puppet, Kamasan Balinese narrative painting, Batik wax-resist motifs, R.A. Kosasih classic komik, Lontar palm-leaf manuscript). Lontar palm-leaf chosen for its quiet mature heritage-anchor tone — fine brown linework on cream palm-leaf with visible fiber texture and punched binding-hole motifs, quiet literati-like feeling appropriate for the cautionary scam narrative at our demographic.

**Locked STYLE block (paste verbatim at the top of every Indonesia comic prompt):**

```
A single illustrated comic book page rendered as a Balinese Lontar palm-leaf manuscript illustration — fine dark-brown line drawings on pale cream palm-leaf background with visible leaf-fiber texture, intricate decorative linework, stylized classical Balinese figures in formal profile, sparse minimalist ink with tiny architectural and costume details, subtle ochre-brown accents, ancient manuscript aesthetic with occasional punched binding-hole motifs at panel edges. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{INDONESIA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from project_scam_comics_cast.md}

SCENE:
Panel 1: {what happens, with Indonesian landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson}. Speech bubble: "{short line}"
```

**API call:**
- First Indonesia comic: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Subsequent: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with pilot as anchor
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- Indonesian cities: bali, batam, gili-islands, ijen-crater, jakarta, labuan-bajo, lombok, mount-bromo, nusa-penida, seminyak, ubud, yogyakarta

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/id/style-tests/5-lontar-palm-leaf-manuscript.jpg` (Harry + Bali money changer)

**Why Lontar over the other 4 candidates:**
- **Wayang Kulit** — visually striking puppet silhouettes but protagonist-as-realistic + scammer-as-puppet hybrid fights cast consistency across 73 comics
- **Kamasan Balinese** — reads more "generic Bali tourist illustration" than strictly Kamasan in practice
- **Batik wax-resist** — strong heritage anchor but the ornate margin patterns compete visually with the comic narrative
- **Kosasih classic komik** — most narratively fluid but looks close to R.A. Kosasih's European/adventure-comic influence — less uniquely Indonesian
- **Lontar palm-leaf** — economy of line + fiber texture + heritage anchor = best fit for mature cautionary-tale narrative at our demographic. Closest aesthetic kin is the China Feng Zikai brush style but readable as a distinct Balinese manuscript tradition.
