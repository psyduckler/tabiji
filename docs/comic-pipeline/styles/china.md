---
name: China (mainland) scam comic style block
description: Locked Nano Banana Pro style prompt for mainland China scam comics — Feng Zikai poetic brush cartoon. Paste verbatim into every China scam generation.
type: project
---
Mainland China scam comic style — chosen 2026-04-18 after a 5-way Chinese illustration bake-off (Gongbi court painting, Lianhuanhua pocket comic, paper-cut jianzhi, Nianhua folk woodblock, Feng Zikai brush cartoon). Feng Zikai chosen for its mature philosophical tone, clear narrative pacing at small brush-economy, and quiet literati sensibility that suits the cautionary scam narrative for the older-female demographic.

Note: distinct from the **Hong Kong / China** style file (`styles/hong-kong.md`) which locks Hong Kong SAR to Shaw Brothers cinema-poster style. Mainland PRC cities use Feng Zikai. Macau (PRC SAR with Portuguese heritage) uses Feng Zikai with this pipeline for consistency with its neighbors on the China country hub.

**Locked STYLE block (paste verbatim at the top of every China comic prompt):**

```
A single illustrated comic book page in the poetic simple-brush cartoon style of Feng Zikai (丰子恺), the beloved 20th-century Chinese essayist-cartoonist — economical black-ink brushstrokes on cream paper, a few confident strokes suggesting figures and setting, soft pale color washes in muted tea-green and terracotta, gentle quietly-humorous tone, Chinese literati sensibility, mature and philosophical feeling, wide margins. Showing four sequential panels arranged in a 2x2 grid with small numbers 1, 2, 3, 4 in the upper-left corner of each panel, separated by thin gray gutters. Each panel contains one clean white rounded speech bubble with a small pointer tail, holding short printed English dialogue in simple black lettering — text must be legible, in English only, and correctly spelled. Square 1:1 composition, 2K resolution.
```

**Full prompt template:**

```
{CHINA_STYLE_BLOCK}

CHARACTER: {paste one of the 4 canonical cast paragraphs verbatim from scripts/comic-pipeline/cast.py}

SCENE:
Panel 1: {what happens, with Chinese landmark}. Speech bubble: "{short line}"
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
- Chinese cities: beijing, chengdu, chongqing, guangzhou, guilin, hangzhou, harbin, kunming, lijiang, macau, pingyao, shanghai, shenzhen, suzhou, xian, yangshuo, zhangjiajie

**Why Feng Zikai over the other 4 candidates:**
- **Gongbi court painting** — elegant but rendered as generic Chinese illustration, lost the silk-scroll formality
- **Lianhuanhua pocket comic** — strong authentic nostalgia and good narrative pacing; second-choice
- **Paper-cut jianzhi** — most visually distinctive (heritage-anchor like Greek red-figure), but red-on-cream is visually intense at full page
- **Nianhua folk woodblock** — cheerful but the festive decorative borders fight the Tourist Police / modern scam context
- **Feng Zikai** — economy of line + quietly humorous tone + mature literati sensibility = best fit for cautionary scam narrative at the demographic

**Pilot reference image:** `https://img.tabiji.ai/scam-comics/cn/style-tests/5-feng-zikai-brush-cartoon.jpg` (Margie + Beijing Wangfujing tea-house scam)
