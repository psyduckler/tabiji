#!/usr/bin/env python3
"""Integrate comics + pattern icons + hero illustrations into the manuscript.

Steps:
  1. Download all 40 images from R2 (30 atlas comics + 7 pattern icons + 3 heroes)
  2. Compress + resize for ePub-friendly size (max 1200px, JPG q85)
  3. Save to book-atlas/build/images/
  4. Insert markdown image references into each manuscript file at the right spot:
     - atlas-*.md: after the front-matter blockquote, before first ##
     - 05-patterns.md: after each "## N. <Pattern Name>" heading
     - 02-introduction.md / 06-pre-trip-checklist.md / 07-first-24-hours.md:
       after H1 with the corresponding hero illustration

Usage:
    python3 scripts/integrate_comics.py
"""
from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from io import BytesIO

ROOT = Path("/Users/bjh/Documents/tabiji/.claude/worktrees/eloquent-boyd-7e72e8/book-atlas")
MS = ROOT / "manuscript"
IMG_DIR = ROOT / "build" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

R2_BASE = "https://img.tabiji.ai/scam-comics"

# 30 atlas chapter comics (chapter slug → R2 path)
ATLAS_COMICS = {
    "atlas-aggressive-street-vendor": "italy/book-2026/aggressive-street-vendor.png",
    "atlas-airbnb-off-platform-fraud": "argentina/book-2026/airbnb-off-platform-fraud.png",
    "atlas-airport-arrival-scams": "egypt/book-2026/airport-arrival-scams.png",
    "atlas-atm-currency-conversion-trap": "italy/book-2026/atm-currency-conversion-trap.png",
    "atlas-atm-skimming": "france/book-2026/atm-skimming.png",
    "atlas-beach-chair-lounger-hustle": "greece/book-2026/beach-chair-lounger-hustle.png",
    "atlas-bus-train-station-scams": "italy/book-2026/bus-train-station-scams.png",
    "atlas-carpet-shop-pressure-sale": "turkey/book-2026/carpet-shop-pressure-sale.png",
    "atlas-closed-attraction-redirect": "india/book-2026/closed-attraction-redirect.png",
    "atlas-counterfeit-currency-returns": "argentina/book-2026/counterfeit-currency-returns.png",
    "atlas-cover-charge-coperto-otoshi": "italy/book-2026/cover-charge-coperto-otoshi.png",
    "atlas-currency-exchange-cambio": "argentina/book-2026/currency-exchange-cambio.png",
    "atlas-distraction-theft-pickpocket-team": "spain/book-2026/distraction-theft-pickpocket-team.png",
    "atlas-drink-spiking-bar-bill-trap": "thailand/book-2026/drink-spiking-bar-bill-trap.png",
    "atlas-express-kidnapping-taxi": "mexico/book-2026/express-kidnapping-taxi.png",
    "atlas-fake-antique-souvenir-markup": "australia/book-2026/fake-antique-souvenir-markup.png",
    "atlas-fake-booking-website": "portugal/book-2026/fake-booking-website.png",
    "atlas-fake-drug-search-police-sting": "egypt/book-2026/fake-drug-search-police-sting.png",
    "atlas-fake-government-tourist-office": "thailand/book-2026/fake-government-tourist-office.png",
    "atlas-fake-skip-the-line-tickets": "italy/book-2026/fake-skip-the-line-tickets.png",
    "atlas-fake-tour-guide": "egypt/book-2026/fake-tour-guide.png",
    "atlas-friendship-bracelet-trap": "france/book-2026/friendship-bracelet-trap.png",
    "atlas-gem-jewelry-shop-pressure": "india/book-2026/gem-jewelry-shop-pressure.png",
    "atlas-gold-ring-trick": "france/book-2026/gold-ring-trick.png",
    "atlas-henna-tattoo-ambush": "morocco/book-2026/henna-tattoo-ambush.png",
    "atlas-phone-snatch-motorcycle": "brazil/book-2026/phone-snatch-motorcycle.png",
    "atlas-qr-code-quishing": "germany/book-2026/qr-code-quishing.png",
    "atlas-restaurant-bill-padding": "italy/book-2026/restaurant-bill-padding.png",
    "atlas-tea-house-invitation": "china/book-2026/tea-house-invitation.png",
    "atlas-three-card-monte": "united-states/book-2026/three-card-monte.png",
}

# Pattern icons (display name → R2 slug)
PATTERN_ICONS = {
    "Captive-Position Lever": "icon-captive-position-lever",
    "Authority Costume": "icon-authority-costume",
    "Sub-Market Quote": "icon-sub-market-quote",
    "Commission Detour": "icon-commission-detour",
    "Made-Up Closure": "icon-made-up-closure",
    "Brand-Mimicry Storefront": "icon-brand-mimicry-storefront",
    "Manufactured Reciprocity": "icon-manufactured-reciprocity",
}

# Hero illustrations
HEROES = {
    "02-introduction": "hero-introduction-four-travelers",
    "06-pre-trip-checklist": "hero-pre-trip-checklist-margie",
    "07-first-24-hours": "hero-first-24-hours-arrival",
}

# Marker for inserted images so re-runs are idempotent
INSERT_MARKER = "<!-- comic-insert -->"


def download_and_compress(url: str, out_path: Path,
                          max_dim: int = 1200, quality: int = 85) -> bool:
    """Download an image from URL, resize to max_dim, save as JPG."""
    if out_path.exists() and out_path.stat().st_size > 0:
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except Exception as e:
        print(f"  FAIL download {url}: {e}", flush=True)
        return False
    try:
        img = Image.open(BytesIO(data)).convert("RGB")
        # Resize: max_dim on longest side
        w, h = img.size
        if max(w, h) > max_dim:
            scale = max_dim / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        img.save(out_path, format="JPEG", quality=quality, optimize=True,
                 progressive=True)
        return True
    except Exception as e:
        print(f"  FAIL compress {url}: {e}", flush=True)
        return False


def download_all() -> dict[str, Path]:
    """Download all 40 images. Returns mapping of slug → local path."""
    tasks: list[tuple[str, str, Path]] = []  # (slug, url, out_path)

    for chapter, r2_path in ATLAS_COMICS.items():
        slug = chapter
        url = f"{R2_BASE}/{r2_path}"
        out = IMG_DIR / f"{slug}.jpg"
        tasks.append((slug, url, out))

    for pattern_name, slug in PATTERN_ICONS.items():
        url = f"{R2_BASE}/book-frontmatter/{slug}.png"
        out = IMG_DIR / f"{slug}.jpg"
        tasks.append((slug, url, out))

    for ms_slug, slug in HEROES.items():
        url = f"{R2_BASE}/book-frontmatter/{slug}.png"
        out = IMG_DIR / f"{slug}.jpg"
        tasks.append((slug, url, out))

    print(f"Downloading + compressing {len(tasks)} images...", flush=True)
    paths: dict[str, Path] = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(download_and_compress, url, out): (slug, out)
                for slug, url, out in tasks}
        for i, fut in enumerate(as_completed(futs), 1):
            slug, out = futs[fut]
            try:
                ok = fut.result()
            except Exception as e:
                ok = False
                print(f"  EXC {slug}: {e}", flush=True)
            if ok:
                paths[slug] = out
                if i % 10 == 0 or i == len(tasks):
                    print(f"  [{i}/{len(tasks)}] OK", flush=True)
    print(f"Downloaded {len(paths)}/{len(tasks)} images, "
          f"total {sum(p.stat().st_size for p in paths.values())//1024} KB",
          flush=True)
    return paths


def insert_atlas_image(file_path: Path, image_path: Path):
    """Insert image markdown into atlas chapter after front-matter blockquote."""
    content = file_path.read_text(encoding="utf-8")
    if INSERT_MARKER in content:
        return False  # already inserted (idempotent)

    lines = content.split("\n")
    # Find the front-matter blockquote (starts with `> **Pattern:` typically)
    # and find first blank line after it, then first `##` heading
    insert_idx = None
    in_blockquote = False
    blockquote_ended_at = None
    for i, line in enumerate(lines):
        if line.startswith(">"):
            in_blockquote = True
        elif in_blockquote and line.strip() == "":
            blockquote_ended_at = i
            in_blockquote = False
            # don't break — keep looking for `##`
        if blockquote_ended_at is not None and line.startswith("## "):
            insert_idx = blockquote_ended_at + 1
            break

    if insert_idx is None:
        # Fallback: insert after H1
        for i, line in enumerate(lines):
            if line.startswith("# "):
                insert_idx = i + 2  # blank line + image
                break

    if insert_idx is None:
        print(f"  SKIP {file_path.name} — no insertion point found")
        return False

    # Build relative image path (from manuscript/ to build/images/)
    rel_path = "../build/images/" + image_path.name
    chapter_label = file_path.stem.replace("atlas-", "").replace("-", " ").title()
    image_md = (
        f"{INSERT_MARKER}\n"
        f"![Comic illustration of {chapter_label}]({rel_path}){{ width=100% }}\n"
    )

    new_lines = lines[:insert_idx] + [image_md] + lines[insert_idx:]
    file_path.write_text("\n".join(new_lines), encoding="utf-8")
    return True


def insert_pattern_icons(file_path: Path, paths: dict[str, Path]):
    """Insert icons in 05-patterns.md after each ## N. <Pattern Name> heading."""
    content = file_path.read_text(encoding="utf-8")
    if INSERT_MARKER in content:
        return False

    lines = content.split("\n")
    new_lines = []
    inserted_count = 0
    for line in lines:
        new_lines.append(line)
        # Match: ## 1. Captive-Position Lever
        m = re.match(r"^## \d+\.\s+(.+?)\s*$", line)
        if m:
            pattern_name = m.group(1).strip()
            if pattern_name in PATTERN_ICONS:
                slug = PATTERN_ICONS[pattern_name]
                if slug in paths:
                    rel_path = "../build/images/" + paths[slug].name
                    new_lines.append("")
                    new_lines.append(
                        f"{INSERT_MARKER}\n"
                        f"![{pattern_name} pattern icon]"
                        f"({rel_path}){{ width=40% }}"
                    )
                    inserted_count += 1
    if inserted_count > 0:
        file_path.write_text("\n".join(new_lines), encoding="utf-8")
        print(f"  Inserted {inserted_count} pattern icons in {file_path.name}")
        return True
    return False


def insert_hero_illustration(file_path: Path, hero_slug: str,
                              paths: dict[str, Path]):
    """Insert hero illustration after H1 in introduction / pre-trip / first-24."""
    content = file_path.read_text(encoding="utf-8")
    if INSERT_MARKER in content:
        return False
    if hero_slug not in paths:
        print(f"  SKIP {file_path.name} — hero {hero_slug} not downloaded")
        return False

    lines = content.split("\n")
    insert_idx = None
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_idx = i + 2  # after H1 + blank line
            break

    if insert_idx is None:
        return False

    rel_path = "../build/images/" + paths[hero_slug].name
    chapter_label = file_path.stem.replace("-", " ").title()
    image_md = (
        f"{INSERT_MARKER}\n"
        f"![Hero illustration for {chapter_label}]({rel_path}){{ width=100% }}\n"
    )
    new_lines = lines[:insert_idx] + [image_md] + lines[insert_idx:]
    file_path.write_text("\n".join(new_lines), encoding="utf-8")
    return True


def main():
    paths = download_all()

    # 1. Insert atlas comics
    print("\nInserting atlas comics...")
    inserted = 0
    for chapter, r2_path in ATLAS_COMICS.items():
        ms_file = MS / f"{chapter}.md"
        if not ms_file.exists():
            print(f"  SKIP {chapter} — file missing")
            continue
        if chapter not in paths:
            print(f"  SKIP {chapter} — image not downloaded")
            continue
        if insert_atlas_image(ms_file, paths[chapter]):
            inserted += 1
    print(f"  inserted {inserted}/{len(ATLAS_COMICS)}")

    # 2. Insert pattern icons in 05-patterns.md
    print("\nInserting pattern icons...")
    insert_pattern_icons(MS / "05-patterns.md", paths)

    # 3. Insert hero illustrations
    print("\nInserting hero illustrations...")
    for ms_slug, hero_slug in HEROES.items():
        ms_file = MS / f"{ms_slug}.md"
        if not ms_file.exists():
            continue
        if insert_hero_illustration(ms_file, hero_slug, paths):
            print(f"  inserted hero in {ms_slug}.md")

    print("\nDone.")


if __name__ == "__main__":
    main()
