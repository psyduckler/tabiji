#!/usr/bin/env python3
"""Sync canonical kindle book covers from /Users/bjh/Documents/tabiji-books into
/Users/bjh/Documents/tabiji/books/{country}-tourist-scams/covers/front-designed.jpg.

Standardizes the naming so every country has a `front-designed.jpg` (the canonical name
referenced in atlas pages, books/ hub, and the cron routine prompt). Where Greece and
Thailand had `front.jpg` historically, we add `front-designed.jpg` alongside (without
removing the old file) for backward compatibility.

Generates books/_covers-manifest.json mapping country slug → canonical path + source.
"""
from pathlib import Path
import shutil
import json

REPO = Path("/Users/bjh/Documents/tabiji")
SRC = Path("/Users/bjh/Documents/tabiji-books")

# country slug (matching books/ dir name) → list of candidate source paths in priority order
SOURCES = {
    "argentina":      ["argentina-scams/KINDLE-cover-1600x2560.jpg"],
    "australia":      ["australia-scams/01-final-deliverables/australia-kindle-cover-1600x2560.jpg"],
    "brazil":         ["brazil-scams/front-cover-KDP-1600x2560.jpg"],
    "canada":         ["canada-scams/kindle/canada-kindle-cover.jpg"],
    "china":          ["china-scams/01-final-deliverables/China Tourist Scams 2026 — Cover.jpg"],
    "colombia":       ["colombia-scams/KINDLE-cover-1600x2560.jpg"],
    "costa-rica":     ["costa-rica-scams/cover-kindle-1600x2560.jpg"],
    "egypt":          ["egypt-scams/01-final-deliverables/egypt-scams-kindle-cover.jpg"],
    "france":         ["france-scams/01-final-deliverables/france-kindle-cover-1600x2560.jpg"],
    "germany":        ["germany-scams/01-final-deliverables/germany-kindle-cover-1600x2560.jpg"],
    "greece":         ["greece-scams/greece-scams-front-cover-2026.jpg"],
    "indonesia":      ["indonesia-scams/source/cover-front-raw.jpg"],
    "italy":          ["italy-scams/01-final-deliverables/italy-kindle-cover-1600x2560.jpg"],
    "japan":          ["japan-scams/01-final-deliverables/japan-kindle-cover-1600x2560.jpg"],
    "malaysia":       ["malaysia-scams/01-final-deliverables/malaysia-kindle-cover-1600x2560.jpg"],
    "mexico":         ["mexico-scams/01-final-deliverables/mexico-kindle-cover-1600x2560.jpg"],
    "morocco":        ["morocco-scams/01-final-deliverables/morocco-kindle-cover-1600x2560.jpg"],
    "portugal":       ["portugal-scams/cover-front-rasterized.jpg"],
    "spain":          ["spain-scams/01-final-deliverables/spain-kindle-cover-1600x2560.jpg"],
    "thailand":       ["thailand-scams/thailand-cover-final.jpg"],
    "turkey":         ["turkey-scams/01-final-deliverables/turkey-kindle-cover-1600x2560.jpg"],
    "united-kingdom": ["uk-scams/united-kingdom-kindle-cover-1600x2560.jpg"],
    "vietnam":        ["vietnam-scams/Vietnam-Tourist-Scams-2026-Kindle-Cover.jpg"],
}

manifest = {
    "$comment": "Canonical book-cover paths. Every entry has a front-designed.jpg under "
                "books/{country}-tourist-scams/covers/. Sources synced from tabiji-books master.",
    "convention": "books/{country}-tourist-scams/covers/front-designed.jpg",
    "covers": {},
}

print(f"syncing {len(SOURCES)} country covers from {SRC}")
copied = 0
skipped = 0
missing = 0

for country, candidates in SOURCES.items():
    target_dir = REPO / "books" / f"{country}-tourist-scams" / "covers"
    target = target_dir / "front-designed.jpg"

    src_path = None
    for c in candidates:
        p = SRC / c
        if p.exists():
            src_path = p
            break

    if src_path is None:
        print(f"  ✗ {country}: no source found in {candidates}")
        missing += 1
        manifest["covers"][country] = {"status": "MISSING", "tried": candidates}
        continue

    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)

    # Skip if target exists and is the same size (rough idempotency)
    if target.exists() and target.stat().st_size == src_path.stat().st_size:
        skipped += 1
        action = "·"
    else:
        shutil.copy2(src_path, target)
        copied += 1
        action = "✓"

    manifest["covers"][country] = {
        "status": "OK",
        "canonical_url": f"/books/{country}-tourist-scams/covers/front-designed.jpg",
        "source_relative": str(src_path.relative_to(SRC)),
        "size_bytes": target.stat().st_size,
    }
    print(f"  {action} {country}: {target.relative_to(REPO)} ({target.stat().st_size:,}B)")

(REPO / "books" / "_covers-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"\nsynced: {copied} copied, {skipped} unchanged, {missing} missing")
print(f"manifest: books/_covers-manifest.json")
