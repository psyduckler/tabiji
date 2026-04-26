---
name: United Kingdom scam comic style block
description: Locked Nano Banana Pro style prompt for UK scam comics — Quentin Blake loose pen-and-watercolor (Roald Dahl illustrator). Paste verbatim into every UK scam generation.
type: project
---
United Kingdom scam comic style — locked 2026-04-20 (PR #334) on the loose scratchy pen-and-watercolor style of Quentin Blake, the beloved British illustrator of Roald Dahl's children's books ('Matilda', 'The BFG', 'James and the Giant Peach'). Quentin Blake chosen for its unmistakable British cultural signal, energetic hand-drawn linework with deliberate wobble, warm wry storybook tone that adults love, and bright loose watercolor washes that distinguish the UK set visually from France's clean Tintin ligne claire and Germany's Zille pen-and-ink wash on the same European hub.

**Locked STYLE block (paste verbatim at the top of every UK comic prompt):**

```
A single illustrated comic book page in the loose scratchy pen-and-watercolor style of Quentin Blake — the beloved British illustrator of Roald Dahl's children's books ('Matilda', 'The BFG', 'James and the Giant Peach') — energetic scratchy cross-hatched black-ink linework with deliberate hand-drawn wobble and exaggerated expressive body language, bright loose watercolor washes in cheerful buttery yellow, ink-blue, crimson, and forest-green that run beyond the line-drawing edges, whimsically-caricatured British characters with oversized hands and feet, playful storybook composition, warm and wry British children's-book tone that adults love. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin hand-drawn black panel borders with narrow warm-white gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black hand-lettered text — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{UNITED_KINGDOM_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with UK landmark}. Speech bubble: "{short line}"
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
- UK cities (16): bath, belfast, birmingham, cambridge, edinburgh, glasgow, inverness, lake-district, liverpool, london, manchester, oxford, stonehenge, stratford-upon-avon, windsor, york

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/gb/style-tests/quentin-blake-v1.jpg` (Quentin Blake bake-off winner)
