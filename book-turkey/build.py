#!/usr/bin/env python3
"""
Build Kindle EPUB from JSON scam data + manuscript markdown.

Usage:
    python3 book-turkey/build.py

Produces: book-turkey/build/turkey-scams.epub
Requires: pandoc, pyyaml
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is required: pip3 install pyyaml")

HERE = Path(__file__).parent
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
MANUSCRIPT = HERE / "manuscript"
ASSETS = HERE / "assets"
TEMPLATES = HERE / "templates"
BUILD = HERE / CONFIG.get("output_dir", "build")
BUILD.mkdir(exist_ok=True)

CITIES = CONFIG["cities"]
DATA_DIR = (HERE / CONFIG["scam_data_dir"]).resolve()

CITY_INSERTION_MARKER = "<!-- CITIES -->"

# Rich alt text for Turkish city chapter openers (screen-reader friendly).
CITY_ALT_TEXT: dict[str, str] = {
    "istanbul": "Istanbul — the Blue Mosque and Hagia Sophia silhouettes across Sultanahmet at dusk",
    "cappadocia": "Cappadocia — hot-air balloons rising over the Göreme fairy chimneys at sunrise",
    "izmir": "İzmir — the waterfront Konak Square clock tower at golden hour",
    "ephesus": "Ephesus — the two-story Library of Celsus facade at late afternoon",
    "kusadasi": "Kuşadası — Pigeon Island causeway and Aegean harbor at sunset",
    "bodrum": "Bodrum — the Castle of St Peter on the harbor peninsula at golden hour",
    "marmaris": "Marmaris — the crescent bay and forested peninsula at blue hour",
    "fethiye": "Fethiye — Ölüdeniz blue lagoon and the Babadağ paragliding ridge",
    "antalya": "Antalya — Kaleiçi old-town harbor and Taurus Mountains silhouette",
    "alanya": "Alanya — the Red Tower and castle rock above Cleopatra Beach",
    "side-turkey": "Side — the colonnaded Temple of Apollo columns at sunset",
    "pamukkale": "Pamukkale — the white travertine terraces pooling mineral water at dawn",
    "konya": "Konya — the turquoise dome of the Mevlana Museum at golden hour",
}


def load_city(slug: str) -> dict:
    path = DATA_DIR / f"{slug}.json"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    return json.loads(path.read_text())


def scam_md(scam: dict, image_path: Path | None = None) -> str:
    cat = scam["category"].title()
    sev = scam["severity"].title()
    freq = scam["frequency"].title()
    parts = [
        f'## {scam["name"]}\n\n',
        f"**{cat}** · Severity: {sev} · Frequency: {freq}\n\n",
    ]
    if image_path and image_path.exists():
        alt = (
            f'Stylized illustration depicting the {scam["name"]} scam — '
            f'a {cat.lower()} scam rated {sev.lower()} severity'
        )
        parts.append(f"![{alt}]({image_path.resolve()})\n\n")
    parts.extend([
        f'### How this scam works\n\n{scam["description"]}\n\n',
        f'### How to avoid it\n\n{scam["avoidance"]}\n\n',
        f'**Where it happens:** {scam["location"]}\n\n',
    ])
    if scam.get("tags"):
        parts.append(f'*{" · ".join(scam["tags"])}*\n\n')
    return "".join(parts)


def city_display_name(slug: str, data: dict) -> str:
    """Return the preferred display name for a city.

    Map slug → display-name so the book prints Xi'an, Chongqing,
    Zhangjiajie, etc. consistently in chapter headings and the TOC,
    regardless of how the upstream JSON stores the city field.
    """
    DISPLAY = {
        "istanbul": "Istanbul",
        "cappadocia": "Cappadocia",
        "izmir": "İzmir",
        "ephesus": "Ephesus",
        "kusadasi": "Kuşadası",
        "bodrum": "Bodrum",
        "marmaris": "Marmaris",
        "fethiye": "Fethiye",
        "antalya": "Antalya",
        "alanya": "Alanya",
        "side-turkey": "Side",
        "pamukkale": "Pamukkale",
        "konya": "Konya",
    }
    if slug in DISPLAY:
        return DISPLAY[slug]
    return data.get("city", slug.title()).strip()


def city_chapter_md(data: dict) -> str:
    slug = data["slug"]
    city = city_display_name(slug, data)
    parts = [f"\n\n# {city}\n\n"]
    # Chapter-opening city illustration (flat-vector travel-poster style).
    city_img = HERE / "assets" / "cities" / f"{slug}.jpg"
    if city_img.exists():
        alt = CITY_ALT_TEXT.get(slug, f"Stylized illustration of {city}")
        parts.append(f"![{alt}](assets/cities/{slug}.jpg)\n\n")
    intro_path = MANUSCRIPT / f"cities-{slug}-intro.md"
    if intro_path.exists():
        parts.append(intro_path.read_text().strip() + "\n\n")
    else:
        parts.append(
            f"> **TODO** — write a 1-page intro for {city}: "
            f"overall risk level, top 3 neighborhoods to watch, "
            f"nearest Turkish National Police (Polis) station, one safe recommendation.\n\n"
        )
    parts.append(
        f'This chapter documents {len(data["scams"])} scams reported in {city}.\n\n'
    )
    image_dir = HERE / "assets" / "images" / slug
    for idx, scam in enumerate(data["scams"], start=1):
        img = image_dir / f"{idx:02d}.jpg"
        parts.append(scam_md(scam, img if img.exists() else None))
    return "".join(parts)


def static_chapters() -> list[tuple[str, str]]:
    """Return numbered manuscript files sorted by filename."""
    files = sorted(MANUSCRIPT.glob("[0-9][0-9]-*.md"))
    return [(f.name, f.read_text()) for f in files]


def _normalize_turkish_currency(md: str) -> str:
    """Convert the Turkish lira symbol (₺, U+20BA) — absent from Arial Unicode
    MS and from many other common book fonts — into the "TL" abbreviation,
    preserving spacing and the surrounding numeric/range text.

    Patterns handled:
      ₺350          → 350 TL
      ₺1,800        → 1,800 TL
      350-₺500      → 350–500 TL
      ₺350-₺500     → 350–500 TL
      ₺350 – ₺500   → 350–500 TL

    Also sweeps bare hyphens between two numbers in currency contexts into
    en-dashes, which Pandoc +smart otherwise leaves alone.
    """
    # Range: ₺N1 - ₺N2 (with optional spaces around the dash)
    md = re.sub(
        r"₺([\d,.]+)\s*[–-]\s*₺([\d,.]+)",
        r"\1–\2 TL",
        md,
    )
    # Range: N1 - ₺N2
    md = re.sub(
        r"([\d,.]+)\s*[–-]\s*₺([\d,.]+)",
        r"\1–\2 TL",
        md,
    )
    # Range: ₺N1 - N2
    md = re.sub(
        r"₺([\d,.]+)\s*[–-]\s*([\d,.]+)",
        r"\1–\2 TL",
        md,
    )
    # Single: ₺N  (must run after all range replacements)
    md = re.sub(r"₺([\d,.]+)", r"\1 TL", md)
    # Any stray ₺ that escaped (e.g. in prose) → "TL"
    md = md.replace("₺", "TL")

    # Convert hyphens in numeric ranges inside currency contexts to en-dashes.
    # Only touch: (digits)-(digits) immediately followed by a currency word.
    md = re.sub(
        r"(\b[\d,.]+)-([\d,.]+\s*(?:TL|TRY|lira|euro|euros|€|\$))",
        r"\1–\2",
        md,
    )
    # Same for ranges inside "from $N-N" or "$N-N" style
    md = re.sub(r"(\$[\d,.]+)-(\$?[\d,.]+)", r"\1–\2", md)

    return md


def assemble_markdown() -> str:
    parts: list[str] = []
    for fname, content in static_chapters():
        if CITY_INSERTION_MARKER in content:
            parts.append(content.replace(CITY_INSERTION_MARKER, ""))
            for c in CITIES:
                try:
                    parts.append(city_chapter_md(load_city(c)))
                except FileNotFoundError:
                    parts.append(
                        f"\n# {c.title()}\n\n"
                        f"> **TODO** — data missing for {c}\n\n"
                    )
        else:
            parts.append(content)
        parts.append("\n\n")
    return _normalize_turkish_currency("".join(parts))


def build_epub(md: str) -> Path:
    md_path = BUILD / "manuscript.md"
    md_path.write_text(md)

    out_name = CONFIG.get("output_filename", "turkey-scams")
    epub_path = BUILD / f"{out_name}.epub"
    cover = ASSETS / "cover.jpg"
    css = TEMPLATES / "style.css"

    cmd = [
        "pandoc",
        str(md_path),
        "-o",
        str(epub_path),
        "--resource-path",
        str(HERE),
        "--metadata",
        f'title={CONFIG["title"]}',
        "--metadata",
        f'subtitle={CONFIG["subtitle"]}',
        "--metadata",
        f'author={CONFIG["author"]}',
        "--metadata",
        f'publisher={CONFIG["publisher"]}',
        "--metadata",
        f'lang={CONFIG["language"]}',
        "--metadata",
        f'rights={CONFIG["rights"]}',
        "--metadata",
        f'description={CONFIG["description"].strip()}',
        "--toc",
        "--toc-depth=2",
        "--split-level=1",
    ]
    if cover.exists():
        cmd.extend(["--epub-cover-image", str(cover)])
    if css.exists():
        cmd.extend(["--css", str(css)])

    subprocess.run(cmd, check=True)
    return epub_path


def stats(md: str) -> dict:
    words = len(re.findall(r"\b\w+\b", md))
    todos = len(re.findall(r"\*\*TODO\*\*", md, re.IGNORECASE))
    scam_count = sum(len(load_city(c).get("scams", [])) for c in CITIES if (DATA_DIR / f"{c}.json").exists())
    return {"words": words, "todos": todos, "scams": scam_count}


def render_cover() -> None:
    """Rebuild cover.jpg from the SVG source if the SVG is newer.
    Produces a 1600x2560 JPG (KDP spec, 1.6:1 aspect, ~300 DPI)."""
    svg = ASSETS / "svg" / "front.svg"
    jpg = ASSETS / "cover.jpg"
    if not svg.exists():
        return
    if jpg.exists() and jpg.stat().st_mtime >= svg.stat().st_mtime:
        return
    png_tmp = BUILD / "cover_tmp.png"
    subprocess.run(
        ["rsvg-convert", "-w", "1600", "-h", "2560", str(svg), "-o", str(png_tmp)],
        check=True,
    )
    from shutil import which as _which
    if _which("magick"):
        subprocess.run(["magick", str(png_tmp), "-quality", "90", str(jpg)], check=True)
    elif _which("sips"):
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "90",
             str(png_tmp), "--out", str(jpg)],
            check=True, capture_output=True,
        )
    else:
        raise RuntimeError("Need either ImageMagick (magick) or macOS sips to convert PNG→JPG")
    png_tmp.unlink(missing_ok=True)


def main() -> None:
    render_cover()
    md = assemble_markdown()
    epub_path = build_epub(md)
    s = stats(md)
    print(f"✓ Built: {epub_path}")
    print(f"  Size:  {epub_path.stat().st_size / 1024:.1f} KB")
    print(f"  Words: {s['words']:,}")
    print(f"  Scams: {s['scams']}")
    print(f"  TODOs remaining: {s['todos']}")


if __name__ == "__main__":
    main()
