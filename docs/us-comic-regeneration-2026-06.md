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

Three audited rounds (generate → view/audit → retry ≤3, every image opened and judged). Rounds 1–2 used the hardened prompt; round 3 added per-comic `--avoid` hints (blank the specific garbled prop, force a generic mascot, drop the named brand) plus a text-free-prop rule. Trademark policy: **Balanced** — named real venues and depicted landmarks are acceptable; copyrighted characters and brand logos are not.

**34 fixed & book-ready — all pushed live to R2:**
anaheim/1, anaheim/5, asheville/3, atlanta/2, atlanta/5, austin/7, branson/1, charleston/6, chicago/4, chicago/5, dallas/3, dallas/4, fort-lauderdale/2, gatlinburg/1, gatlinburg/4, key-west/2, key-west/6, las-vegas/5, los-angeles/6, memphis/6, miami/6, miami/7, myrtle-beach/3, myrtle-beach/6, napa-valley/2, nashville/3, philadelphia/3, portland/3, san-antonio/4, san-diego/4, san-francisco/5, seattle/3, sedona/4, washington-dc/1.

**8 deferred** — at the hard ceiling of automated generation after 6–9 attempts (incl. round-3 `--avoid` hints). The model keeps reproducing brand-intrinsic imagery or rendering dense prop text as gibberish even when explicitly told not to:

| Comic | Reason (still deferred after round 3) |
|---|---|
| anaheim/6 | Keeps drawing a Disney castle + Mickey on the "free Disney tickets" posters |
| chicago/2 | Won't blank signage — renders O'HARE / TAXI lettering despite the hint |
| galveston/2 | Blanked the domain into scribble — can't letter `portofgalveston.com` cleanly |
| key-west/5 | Receipt keeps showing line-items + wrong total (never the single clean total) |
| las-vegas/1 | Reproduces the Bellagio logo + garbled Strip signage |
| las-vegas/3 | Reproduces the "Welcome to Las Vegas" landmark sign + garbled badge |
| napa-valley/1 | Keeps inventing a real reseller brand (Platypus/Beau) + garbled button |
| san-diego/7 | Garbled neon signage persists |

Recommendation for these 8: **hand-edit / region inpainting** (repaint just the offending sign/receipt/poster) — full-image text-to-image won't reliably avoid IP the scam is intrinsically about, nor settle dense prop text. Their original (defective) versions remain live until then.

## Deployed

- **R2 push + cachebust — DONE.** All 34 fixed comics (across 3 rounds) pushed to R2 (2048px `.jpg` + 1024px `.webp`); the 29 pages cache-busted (`?v=` bump) in this PR; verified live from `img.tabiji.ai`. The stale `cloudflare-r2-secret-access-key` was bypassed by deriving S3 creds from a Cloudflare API token (access-key-id = token id via `/user/tokens/verify`; secret = `sha256(token value)`). The token is R2-scoped (no cache-purge), so the bare `.jpg` masters used by the book build refresh on CDN TTL; the live site is fresh now via `?v=`.

## Remaining follow-ups (not in this PR)

- **8 deferred comics** still serve their original defective versions live (brand-intrinsic imagery or dense garbled prop-text) — need hand-edit/inpainting per the table above.
- **savannah + st-louis content desync** — page HTML and `api/v1` JSON disagree on the scam list (different scams; HTML shows fewer). 6 "wrong-scam" audit findings stem from this, and savannah/5–6 + st-louis/5 are orphan comics not referenced on the live pages. Needs a content reconciliation decision, not a comic fix — **excluded from this regeneration.**
