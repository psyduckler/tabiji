---
name: Germany scam comic style block
description: Locked Nano Banana Pro style prompt for German scam comics — Heinrich Zille "Berlin Milljöh" turn-of-the-century observational pen-and-ink-wash. Paste verbatim into every Germany scam generation.
type: project
originSessionId: 6e1b60d6-8114-4bf8-83d3-25c3a4635638
---
Germany scam comic style — chosen 2026-04-20 after a 5-way German illustration bake-off (Wilhelm Busch, E.O. Plauen Vater und Sohn, Bauhaus modernist poster, Heinrich Zille Berlin Milljöh, Reinhard Kleist graphic novel). Zille chosen for his warm observational everyday-life humanism, turn-of-the-20th-century Berliner illustrated-newspaper aesthetic, and rich narrative-comic texture well-suited to cautionary scam stories.

**Locked STYLE block (paste verbatim at the top of every Germany comic prompt):**

```
A single illustrated comic book page in the warm observational style of Heinrich Zille (Berlin Milljöh) — rich pen-and-ink cross-hatching with muted warm watercolor wash of grey-brown, rust-red, and dust-yellow, expressive working-class German street figures with sympathetic humanist detail, turn-of-the-20th-century Berliner illustrated-newspaper aesthetic, everyday-life observational tone. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin black panel borders with narrow cream gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black comic lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{GERMANY_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from project_scam_comics_cast.md}

SCENE:
Panel 1: {what happens, with German landmark}. Speech bubble: "{short line}"
Panel 2: {what happens}. Speech bubble: "{short line}"
Panel 3: {what happens}. Speech bubble: "{short line}"
Panel 4: {what happens — usually realization/lesson}. Speech bubble: "{short line}"
```

**API call:**
- First Germany comic: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image`
- Subsequent: `POST https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit` with pilot as anchor
- Body: `{"prompt":"...","images":[...],"aspect_ratio":"1:1","output_format":"jpeg"}`
- Credential: `wavespeed-api-key` in macOS keychain

**Cities / Production path:**
- R2: `scams/<city>/scam-<N>.jpg` → public `https://img.tabiji.ai/scams/<city>/scam-<N>.jpg`
- German cities: baden-baden, berlin, bremen, cologne, dresden, dusseldorf, frankfurt, fussen, hamburg, heidelberg, leipzig, munich, nuremberg, potsdam, rothenburg, stuttgart

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/de/style-tests/4-heinrich-zille-berlin-milljoh.jpg` (Marcus + Berlin shell game)
