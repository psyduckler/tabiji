# US scam-comic pipeline hardening + Tier-1 blocker regeneration (2026-06)

## Why

An audit of all **241 US scam-page comics** (41 cities, `/scams/country/us/`) found **102 not book-ready (42%)** for a planned *United States: Tourist Scams* KDP paperback. The dominant defects:

- **Leaked art-direction baked into the art** (~60): character bios ("SOUTH ASIAN WOMAN, 34"), scene/location descriptions as caption bands, even the style reference "Jack Kirby" — all rendered as visible text by Nano Banana Pro.
- **Trademark / IP** (~48 not-ready; 112 with any brand reference): Disney characters & castle, Marvel/DC characters, Airbnb/Ticketmaster/Gucci/Uber/Mastercard logos.
- **Half-resolution masters** (83 of 241 at 1024px instead of 2048px).
- **Garbled text on dense props**, stray banners, and 7 wrong-scam depictions.

Root cause of the leaks: `synthesize.build_full_prompt()` fed the `CHARACTER` bio and per-panel `scene` descriptions to the image model with nothing telling it those were *drawing directions, not copy to letter*. Root cause of the half-res: `submit_nbp` only set `resolution:"2k"` on the `/text-to-image` retry, so first-pass `/edit` renders defaulted to 1024px.

## Pipeline fixes (this PR)

- **`synthesize.py` — prompt hardening.** `build_full_prompt()` now appends a strict **text contract** (CHARACTER/SCENE are art direction, not text; only speech-balloon dialogue + minimal natural signage may be lettered; no narration/caption/location/title banners, names, ages, "Panel", or artist names; minimize prop text — show only the 1–2 key items on receipts/menus/screens; no placeholders like `X`/`HUGE PRICE`; no duplicated text) and an **IP contract** (no real logos, copyrighted characters/mascots, brand colors, or trademarked architecture — use generic stand-ins). Also sets `resolution:"2k"` so `/edit` renders 2048px masters.
- **`cachebust.py`** now matches the `.webp` web variant (US `<img>` tags load `.webp`; it previously matched only `.jpg`, a silent no-op on those pages).
- **`regen_local.py`** (new) — generate one comic to a local file with **no R2 upload**, so nothing unverified reaches production; used by the audited regeneration loop.
- **`r2_push_comic.py`** (new) — push an approved comic to R2 as the 2048px `.jpg` master **and** a derived 1024px `.webp` (generate.py only uploaded `.jpg`, which is why webp variants drifted).

## Regeneration results (42 Tier-1 blockers)

Two audited rounds (generate → view/audit → retry ≤3, every image opened and judged). Trademark policy: **Balanced** — named real venues and depicted landmarks are acceptable; copyrighted characters and brand logos are not.

**27 fixed & book-ready** (staged in `~/Documents/tabiji-us-comic-regen-staging/`, pending R2 push):
anaheim/5, asheville/3, atlanta/2, austin/7, branson/1, charleston/6, chicago/4, chicago/5, dallas/3, fort-lauderdale/2, gatlinburg/1, gatlinburg/4, key-west/2, key-west/6, memphis/6, miami/6, miami/7, myrtle-beach/3, myrtle-beach/6, napa-valley/2, philadelphia/3, portland/3, san-antonio/4, san-diego/4, seattle/3, sedona/4, washington-dc/1.

**15 deferred** — hit the limits of automated generation after up to 6 attempts:

| Comic | Reason (deferred) |
|---|---|
| anaheim/1 | Copyrighted character (Goofy) + garbled badge |
| anaheim/6 | Disney castle + "DISNEY" on props + stray time-banner |
| atlanta/5 | Stray "ATLANTA" location banner |
| chicago/2 | Garbled highway signage |
| dallas/4 | Ticketmaster / Facebook Marketplace logos + placeholder |
| galveston/2 | "CRUZE" misspelling + Honda logo |
| key-west/5 | Garbled receipt fine-print |
| las-vegas/1 | Copyrighted character (Superman / DC shield) |
| las-vegas/3 | Garbled polo + receipt values |
| las-vegas/5 | Duplicated balloon + garbled signage |
| los-angeles/6 | Hyundai logo (Hollywood Sign itself OK under Balanced) |
| napa-valley/1 | Real reseller brand "Platypus Wine Tours" + mascot |
| nashville/3 | Mastercard logo + garbled bank statement |
| san-diego/7 | City of San Diego seal + garbled fine-print |
| san-francisco/5 | Garbled clipboard / URL fine-print |

Recommendation for the deferred set: hand-edit (paint out the logo/character/banner) or use region inpainting — full-image regeneration won't reliably avoid IP the scam is intrinsically about, nor settle dense prop text.

## Deployed

- **R2 push + cachebust — DONE.** All 27 fixed comics pushed to R2 (2048px `.jpg` + 1024px `.webp`); the 22 pages cache-busted (`?v=` bump) in this PR; verified live from `img.tabiji.ai`. The stale `cloudflare-r2-secret-access-key` was bypassed by deriving S3 creds from a Cloudflare API token (access-key-id = token id via `/user/tokens/verify`; secret = `sha256(token value)`). The token is R2-scoped (no cache-purge), so the bare `.jpg` masters used by the book build refresh on CDN TTL; the live site is fresh now via `?v=`.

## Remaining follow-ups (not in this PR)

- **15 deferred comics** still serve their original defective versions live (garbled prop-text; a few copyrighted characters/logos) — need hand-edit/inpainting per the table above.
- **savannah + st-louis content desync** — page HTML and `api/v1` JSON disagree on the scam list (different scams; HTML shows fewer). 6 "wrong-scam" audit findings stem from this, and savannah/5–6 + st-louis/5 are orphan comics not referenced on the live pages. Needs a content reconciliation decision, not a comic fix — **excluded from this regeneration.**
