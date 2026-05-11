# book-cosmetic-surgery — The Cosmetic Surgery Field Guide

**Volume 2 of the Tabiji Field Guides series.** Sister volume to `book-dental/`.

**Status:** **Phase 0 — strategic brief drafted, awaiting sign-off.** No manuscript writing has begun. Read `BRIEF.md` first.

**Editor (proposed):** Bernard Huang
**Publisher:** Tabiji
**Companion site (planned):** [tabiji.ai/book/cosmetic-surgery](https://tabiji.ai/book/cosmetic-surgery)

---

## What this book is

A consumer-protection field guide for cost-shocked patients considering cosmetic surgery or hair restoration abroad. Same calm, protective editorial voice as Volume 1 (Dental). Same framework structure. Adapted for the higher stakes, higher legal exposure, and more medically complex environment of cosmetic surgery.

The market reality this book serves:
- **$7.4B cosmetic medical tourism market** (2025), growing to $62.78B by 2035
- **BBL has the highest mortality rate of any cosmetic procedure** — between 1 in 3,000 and 1 in 6,241
- **93 documented U.S. citizen deaths from cosmetic surgery in the Dominican Republic alone** (CDC MMWR, 2009–2022)
- A consumer-protection vacuum that influencer marketing currently fills

See `BRIEF.md` for full strategic positioning.

---

## Read this in order

1. **`BRIEF.md`** — Phase 0 strategic brief. The most important document in this directory. Locks scope, voice, title, framework adaptation, reviewer requirements, and timeline.
2. **`README.md`** — this file (orientation)
3. After Phase 0 sign-off: chapter outlines, then drafts, will populate `manuscript/`

---

## Directory layout

```
book-cosmetic-surgery/
├── BRIEF.md                       ← Phase 0 strategic brief (READ THIS FIRST)
├── README.md                      ← this file
├── DESIGNER-BRIEF.md              ← stub (will be created when typesetting begins)
├── amazon-listing.md              ← stub (will be drafted in production phase)
├── manuscript/
│   └── README.md                  ← outline placeholder; populates as drafting proceeds
├── assets/
│   ├── css/
│   │   ├── print-style.css        ← reused from book-dental (no changes needed)
│   │   └── epub-style.css         ← reused from book-dental (no changes needed)
│   └── svg/
│       ├── cover-front.svg        ← will be adapted in production phase
│       └── cover-wrap.svg         ← will be adapted in production phase
├── scripts/
│   ├── build.sh                   ← reused from book-dental, slug-substituted
│   └── preprocess.py              ← reused from book-dental
└── build/                         ← gitignored
```

---

## Differences from `book-dental/` worth noting

| Dimension | book-dental | book-cosmetic-surgery |
|---|---|---|
| Manuscript length target | ~52,000 words | ~55,000–60,000 words |
| Reviewer panel | clinical (dentist), copyedit, legal, proofread | clinical (plastic surgeon), **anesthesiologist**, copyedit, legal, **sensitivity reader**, proofread |
| Reviewer budget | $3,000–$5,000 | **$4,400–$8,800** |
| Editorial position | "ask better questions" | "ask better questions" + **explicit warnings against specific high-risk procedure-destination combinations** |
| Disclaimer language | strong | **stronger; legal review required, not optional** |
| Composite scenario weight | varying-stakes | **higher-stakes; some procedures discussed have killed patients** |
| Recovery chapter weight | one chapter | **multi-chapter section; surgical recovery is materially more complex** |

These are deliberate. See `BRIEF.md` §10 for the editorial-risk-management rationale.

---

## Build pipeline

Identical to `book-dental/` once a manuscript exists. From repo root:

```bash
bash book-cosmetic-surgery/scripts/build.sh
```

This will produce all KDP-ready files in `book-cosmetic-surgery/build/`:
- `the-cosmetic-surgery-field-guide.epub`
- `kindle-cover.jpg`
- `paperback-interior.pdf`
- `paperback-wrap-cover.pdf`

The build pipeline reuses the v2 elaborate CSS from book-dental (scenario callout boxes, pull quotes, color-coded green/yellow/red flag treatments, Decision Gate boxes, styled Journey Map). No CSS work is required for Volume 2.

---

## What needs human action right now

Before any further work proceeds, the following decisions in `BRIEF.md` §15 require sign-off:

- [ ] Title and subtitle confirmed
- [ ] Procedure scope confirmed (cosmetic + hair restoration only; bariatric/orthopedic deferred)
- [ ] Editorial position on high-risk procedures confirmed
- [ ] Reviewer budget confirmed ($4,400–$8,800)
- [ ] Cover design direction confirmed (continue Direction 2)
- [ ] Series accent color decision
- [ ] Launch sequencing (sequential after Volume 1, or parallel)
- [ ] Bernard Huang confirmed as editor
- [ ] Endorsement outreach commitment

Without these decisions, no manuscript writing proceeds.

---

## Series identity

This book is the second of a planned multi-volume series:

| Volume | Title | Status |
|---|---|---|
| 1 | The Dental Tourism Field Guide | In production (book-dental/) |
| 2 | The Cosmetic Surgery Field Guide | **Phase 0 brief — this directory** |
| 3 (planned) | The Bariatric Surgery Field Guide | Future |
| 4 (planned) | The Orthopedic Surgery Field Guide | Future |

The series shares: editorial voice, structural framework (Five Rules, Seven Leverage Points, 20-Minute Safety Pause), Direction 2 cover aesthetic, "Bernard Huang, Editor" byline, Tabiji publisher imprint, calm-protective editorial position, no-rankings/no-clinic-recommendation discipline.

---

## History

- **2026-05-10:** Phase 0 brief drafted. Skeleton directory created with adapted starter files from book-dental. Awaiting sign-off on strategic decisions.
