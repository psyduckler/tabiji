#!/usr/bin/env python3
"""Re-download all comics from R2 at higher resolution for KDP print quality.

Replaces build/images/*.jpg with 1800px-max-dim JPGs at quality 90.
At 300 DPI, that's 6 inches wide — comfortably above the 4-5 inch
typical print width on a 6x9 page.

Re-using the script means the ePub & HTML re-bundle automatically pick
up the higher-res versions on next build.
"""
from __future__ import annotations

import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path
from PIL import Image

ROOT = Path("/Users/bjh/Documents/tabiji/.claude/worktrees/eloquent-boyd-7e72e8/book-atlas")
IMG_DIR = ROOT / "build" / "images"
IMG_DIR.mkdir(parents=True, exist_ok=True)

R2_BASE = "https://img.tabiji.ai/scam-comics"

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

PATTERN_ICONS = {
    "icon-captive-position-lever",
    "icon-authority-costume",
    "icon-sub-market-quote",
    "icon-commission-detour",
    "icon-made-up-closure",
    "icon-brand-mimicry-storefront",
    "icon-manufactured-reciprocity",
}

HEROES = {
    "hero-introduction-four-travelers",
    "hero-pre-trip-checklist-margie",
    "hero-first-24-hours-arrival",
}


def download_and_save(url: str, out_path: Path,
                      max_dim: int = 1800, quality: int = 90) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=180) as r:
            data = r.read()
    except Exception as e:
        print(f"  FAIL {url}: {e}")
        return False
    try:
        img = Image.open(BytesIO(data)).convert("RGB")
        w, h = img.size
        if max(w, h) > max_dim:
            scale = max_dim / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        img.save(out_path, format="JPEG", quality=quality, optimize=True,
                 progressive=True)
        return True
    except Exception as e:
        print(f"  FAIL compress {url}: {e}")
        return False


def main():
    tasks = []
    for chapter, r2_path in ATLAS_COMICS.items():
        tasks.append((chapter,
                      f"{R2_BASE}/{r2_path}",
                      IMG_DIR / f"{chapter}.jpg"))
    for slug in PATTERN_ICONS:
        tasks.append((slug,
                      f"{R2_BASE}/book-frontmatter/{slug}.png",
                      IMG_DIR / f"{slug}.jpg"))
    for slug in HEROES:
        tasks.append((slug,
                      f"{R2_BASE}/book-frontmatter/{slug}.png",
                      IMG_DIR / f"{slug}.jpg"))

    print(f"Re-downloading {len(tasks)} images at 1800px / q90...")
    ok_count = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(download_and_save, url, out): slug
                for slug, url, out in tasks}
        for i, fut in enumerate(as_completed(futs), 1):
            slug = futs[fut]
            if fut.result():
                ok_count += 1
            if i % 10 == 0 or i == len(tasks):
                print(f"  [{i}/{len(tasks)}] cumulative OK: {ok_count}")

    total_kb = sum(p.stat().st_size for p in IMG_DIR.glob("*.jpg")) // 1024
    print(f"\nDone. {ok_count}/{len(tasks)} images, total {total_kb} KB "
          f"({total_kb/1024:.1f} MB)")


if __name__ == "__main__":
    main()
