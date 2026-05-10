# book-travel-scams-seniors

Build pipeline for *Travel Scams for Seniors* (Bernard Huang, 2026).

A standalone trade-nonfiction book, structurally simpler than the country-scams books in this repo. One long manuscript, 19 chapters, 17 chapter scene illustrations + 2 cover illustrations.

## Layout

```
book-travel-scams-seniors/
├── config.yaml                       Title, author, description, trim, spine
├── build.py                          Manuscript assembly + EPUB build
├── amazon-listing.md                 KDP metadata (title, subtitle, HTML description, 7 keywords)
├── manuscript/
│   └── manuscript-source.md          Copyedited manuscript (39 edits applied)
├── assets/
│   ├── covers/
│   │   ├── front.jpg                 Raw illustration (no text)
│   │   ├── back.jpg                  Raw illustration (no text)
│   │   ├── front-titled.jpg          Front with title + byline overlaid
│   │   └── back-titled.jpg           Back with sales copy + bio band overlaid
│   └── chapter-scenes/
│       ├── ch01-mustard-stain.jpg
│       ├── ch02-midnight-call.jpg
│       └── … (17 total, ch03 and ch18 deliberately have no scene)
├── scripts/
│   ├── build_kindle_cover.py         1600×2560 JPEG for KDP ebook upload
│   ├── build_paperback_interior.py   6×9 in PDF, 361 pages, KDP/IngramSpark ready
│   └── build_paperback_cover.py      Back+spine+front composite PDF, with bleeds
└── build/                            (gitignored) Generated outputs go here
```

## Build all artifacts

```bash
/opt/homebrew/bin/python3 book-travel-scams-seniors/build.py
/opt/homebrew/bin/python3 book-travel-scams-seniors/scripts/build_kindle_cover.py
/opt/homebrew/bin/python3 book-travel-scams-seniors/scripts/build_paperback_interior.py
/opt/homebrew/bin/python3 book-travel-scams-seniors/scripts/build_paperback_cover.py
```

Outputs end up in `build/` (gitignored). Runtime: ~30 seconds total.

## Regenerate illustrations

The covers and chapter scenes were generated via Wavespeed (Nano Banana Pro). The original prompts and runner are in `~/Desktop/Travel-Scams-Copyedit-2026-05-09/`:

- `13-comics-plan.md` — prompts and style block
- `14-gen-comics.py` — Wavespeed pipeline runner

Each generation incurs ~$0.50–$1.50 in Wavespeed API costs. Total cost for the 19-asset run was ~$15.

## Spine width formula

For KDP cream paper:

```
spine_inches = page_count * 0.0025
```

Current spine: `361 × 0.0025 = 0.9025"`. If you re-edit the manuscript and the page count changes, regenerate `build_paperback_interior.py` first to get the new page count, then re-run `build_paperback_cover.py` (it auto-reads page count from the interior PDF).

## Dependencies

- macOS Big Caslon, Baskerville, Hoefler Text, Optima system fonts (for cover and PDF typography)
- pandoc 3.x (`brew install pandoc`)
- WeasyPrint 68+ (`pip install weasyprint`; runs on /opt/homebrew/bin/python3)
- Pillow (`pip install pillow`)
- pypdf (`pip install pypdf`)
- pyyaml (`pip install pyyaml`)

## Open issues / before going live

See `/Users/bjh/Desktop/Travel-Scams-Final-Assets/README.md` and `/Users/bjh/Desktop/Travel-Scams-Copyedit-2026-05-09/05-query-list.md` for the full pre-launch checklist (legal review, sensitivity reader, ISBN, indexing, author bio).
