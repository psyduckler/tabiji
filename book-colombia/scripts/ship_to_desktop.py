#!/usr/bin/env python3
"""Ship the built Colombia book artifacts to ~/Desktop/colombia-kdp/ in the
flat KDP-upload layout, with a README that has page-count + size figures.

Mirrors the argentina-kdp pattern:
    INTERIOR-colombia-scams-paperback.pdf
    COVER-colombia-paperback-wraparound.pdf
    COVER-colombia-paperback-wraparound.svg
    COVER-front-editable.svg
    COVER-back-editable.svg
    KINDLE-colombia-scams.epub
    KINDLE-cover-1600x2560.jpg
    SOURCE-final-manuscript.md
    README.md

Run after build.py, build_paperback_interior.py, and build_paperback_cover.py.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
BUILD = BOOK / "build"
ASSETS = BOOK / "assets"
DEST = Path.home() / "Desktop" / "colombia-kdp"


def fmt_size(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f} MB"
    if n >= 1_000:
        return f"{n / 1_000:.0f} KB"
    return f"{n} B"


def pdf_pages(path: Path) -> int:
    """Return page count via mdls (macOS Spotlight metadata)."""
    try:
        out = subprocess.run(
            ["mdls", "-name", "kMDItemNumberOfPages", "-raw", str(path)],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return int(out) if out and out != "(null)" else 0
    except Exception:
        return 0


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)

    interior_pdf = BUILD / "colombia-scams-paperback.pdf"
    cover_pdf = BUILD / "colombia-paperback-cover.pdf"
    cover_svg = BUILD / "colombia-paperback-cover.svg"
    epub = BUILD / "colombia-scams.epub"
    kindle_cover = ASSETS / "cover.jpg"
    front_svg = ASSETS / "svg" / "front.svg"
    back_svg = ASSETS / "svg" / "back.svg"
    manuscript_md = BUILD / "manuscript.md"

    moves = [
        (interior_pdf, "INTERIOR-colombia-scams-paperback.pdf"),
        (cover_pdf,    "COVER-colombia-paperback-wraparound.pdf"),
        (cover_svg,    "COVER-colombia-paperback-wraparound.svg"),
        (epub,         "KINDLE-colombia-scams.epub"),
        (kindle_cover, "KINDLE-cover-1600x2560.jpg"),
        (front_svg,    "COVER-front-editable.svg"),
        (back_svg,     "COVER-back-editable.svg"),
        (manuscript_md,"SOURCE-final-manuscript.md"),
    ]

    missing = [src for src, _ in moves if not src.exists()]
    if missing:
        print("Missing inputs — run the build steps first:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        sys.exit(1)

    for src, name in moves:
        dest = DEST / name
        shutil.copy2(src, dest)
        print(f"  ✓ {name} ({fmt_size(dest.stat().st_size)})")

    # README with up-to-date sizes + page count.
    pages = pdf_pages(DEST / "INTERIOR-colombia-scams-paperback.pdf")
    interior_size = fmt_size((DEST / "INTERIOR-colombia-scams-paperback.pdf").stat().st_size)
    cover_size = fmt_size((DEST / "COVER-colombia-paperback-wraparound.pdf").stat().st_size)
    epub_size = fmt_size((DEST / "KINDLE-colombia-scams.epub").stat().st_size)
    k_cover_size = fmt_size((DEST / "KINDLE-cover-1600x2560.jpg").stat().st_size)
    ms_words = len((DEST / "SOURCE-final-manuscript.md").read_text().split())

    readme = f"""# Colombia: Tourist Scams — Amazon KDP Upload Package

**Tabiji Travel Safety Series · Volume 16**
**58 scams · 10 destinations · {pages or '≈488'} pages · 2026 Edition**

---

## What's in this folder

### Paperback upload (KDP → Paperback)

| File | Purpose | Size |
|---|---|---|
| `INTERIOR-colombia-scams-paperback.pdf` | **Upload as the book interior.** {pages or '≈488'} pp, 6″×9″ trim, cream paper, xelatex-rendered, KDP-compliant margins. | {interior_size} |
| `COVER-colombia-paperback-wraparound.pdf` | **Upload as the paperback cover.** Full wraparound (back + spine + front) with 0.125″ bleed. | {cover_size} |

### Kindle upload (KDP → Kindle eBook)

| File | Purpose | Size |
|---|---|---|
| `KINDLE-colombia-scams.epub` | **Upload as the eBook manuscript.** EPUB 3 format, chapters split at H1, embedded 58 scam comics + 10 city illustrations + front cover. | {epub_size} |
| `KINDLE-cover-1600x2560.jpg` | **Upload as the eBook cover.** 1600×2560 JPEG (KDP's 1.6:1 aspect spec at ~300 DPI). | {k_cover_size} |

### Editable source

| File | Purpose |
|---|---|
| `COVER-colombia-paperback-wraparound.svg` | Editable wraparound SVG — adjust spine width or content here, then re-render to PDF with `rsvg-convert --format=pdf`. |
| `COVER-front-editable.svg` | Front cover SVG (portrait 500×800 viewBox). Paired with `assets/svg/front.jpg` as the Macondo-watercolor raster background. |
| `COVER-back-editable.svg` | Back cover SVG (portrait 500×800 viewBox). Paired with `assets/svg/back.jpg` as the raster background. |
| `SOURCE-final-manuscript.md` | The final master-editor-audited Markdown manuscript ({ms_words:,} words) that Pandoc → xelatex converted into the PDF. |

---

## KDP upload checklist

### Paperback

- [ ] **Title:** `Colombia Tourist Scams 2026`
- [ ] **Subtitle:** `58 Real Scams Across 10 Colombian Destinations — From Paseo Millonario to Scopolamine, the Exact Phrases That End the Con`
- [ ] **Series:** `Tabiji Travel Safety Series`
- [ ] **Volume:** `16`
- [ ] **Author:** `The Tabiji Team`
- [ ] **Language:** `English`
- [ ] **Interior:** upload `INTERIOR-colombia-scams-paperback.pdf`
- [ ] **Cover:** upload `COVER-colombia-paperback-wraparound.pdf`
- [ ] **Trim size:** 6″ × 9″
- [ ] **Paper:** Cream
- [ ] **Bleed:** Yes (0.125″)
- [ ] **Margins:** Standard

### Kindle

- [ ] **Title / subtitle / series / volume / author / language:** same as paperback above.
- [ ] **eBook manuscript:** upload `KINDLE-colombia-scams.epub`
- [ ] **eBook cover:** upload `KINDLE-cover-1600x2560.jpg`
- [ ] **Categories:** `Travel > Reference`; `Travel > South America > Colombia`; `Travel > Travel Safety`
- [ ] **Keywords:** `Colombia travel safety`, `tourist scams Colombia`, `Bogota safety`, `Medellin safety`, `Cartagena safety`, `paseo millonario`, `scopolamine Colombia`

---

## Cities included (build order)

1. **Bogotá** (Andean capital, *paseo millonario*)
2. **Medellín** (paisa hub, scopolamine ecosystem)
3. **Cartagena** (Caribbean walled city, restaurant overcharge)
4. **Cali** (salsa capital, Granada nightlife)
5. **Santa Marta** (Caribbean gateway, bill-switch + Lost City)
6. **Guatapé** (painted-zócalos pueblo, La Piedra del Peñol)
7. **Salento** (Eje Cafetero coffee axis, Cocora wax palms)
8. **Parque Tayrona** (Caribbean park, El Zaino "park closed" redirect)
9. **San Andrés** (Caribbean island, Tarjeta de Turismo resale)
10. **Villa de Leyva** (Boyacá colonial weekend town)
"""
    (DEST / "README.md").write_text(readme)
    print(f"  ✓ README.md")
    print(f"\n→ shipped to {DEST}")


if __name__ == "__main__":
    main()
