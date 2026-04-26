#!/usr/bin/env python3
"""
Build Kindle EPUB from JSON scam data + manuscript markdown.

Usage:
    python3 book-france/build.py

Produces: book-france/build/france-scams.epub
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

# Rich alt text for French city chapter openers (screen-reader friendly).
CITY_ALT_TEXT: dict[str, str] = {
    "paris": "Paris — the Eiffel Tower above the Trocadéro plaza at golden hour",
    "nice": "Nice — the Promenade des Anglais curving along the Baie des Anges at dusk",
    "cannes": "Cannes — the Croisette palm-line promenade and Palais des Festivals at sunset",
    "st-tropez": "Saint-Tropez — the old harbor with bell tower and pastel quayside houses",
    "marseille": "Marseille — the Vieux-Port basin and Notre-Dame de la Garde basilica on the hill",
    "avignon": "Avignon — the Pont d'Avignon and Palais des Papes ramparts above the Rhône",
    "montpellier": "Montpellier — the Place de la Comédie fountain and Opéra Comédie facade",
    "toulouse": "Toulouse — the pink-brick Capitole de Toulouse and Garonne riverbank at golden hour",
    "lyon": "Lyon — the Saône river curving past the Fourvière basilica on the hill",
    "chamonix": "Chamonix — the Mont Blanc summit rising above the alpine valley village",
    "annecy": "Annecy — the Palais de l'Île on the canal with Lake Annecy beyond",
    "bordeaux": "Bordeaux — the Place de la Bourse mirror-pool reflecting the 18th-century facade",
    "biarritz": "Biarritz — the Hôtel du Palais and surf beach at dusk above the Bay of Biscay",
    "strasbourg": "Strasbourg — the Cathédrale Notre-Dame spire above the Petite France canal quarter",
    "colmar": "Colmar — the half-timbered houses of the Petite Venise quarter along the canal",
    "mont-saint-michel": "Mont-Saint-Michel — the abbey island silhouette rising from the tidal flats at dawn",
}


# Prose-polish helpers live in scripts/polish_scam_prose.py.
# They strip Reddit-URL fragments, split run-on descriptions into paragraphs,
# and bulletize run-on avoidance strings into markdown lists.
sys.path.insert(0, str(HERE / "scripts"))
from polish_scam_prose import polish_description, polish_avoidance, polish_location  # noqa: E402


def load_city(slug: str) -> dict:
    path = DATA_DIR / f"{slug}.json"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    return json.loads(path.read_text())


# Per-image downsize cache: keep raw 2K assets in /assets/images/<slug>/NN.jpg
# untouched (those go into the desktop bundle), and write 1000px-wide
# quality-85 EPUB-bound copies to /build/images/<slug>/NN.jpg. Without this,
# 191 raw 2K comics balloon the EPUB to ~95 MB and destroy KDP delivery margins
# at $0.15/MB above 10 MB.
def _resize_for_epub(src: Path) -> Path:
    rel = src.relative_to(ASSETS / "images")
    dest = BUILD / "images" / rel
    if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    # 800px wide @ quality 78 with Pillow: ~60-90 KB/comic for 191 comics
    # ≈ 14 MB EPUB, which keeps KDP delivery fees minimal at the 70% royalty
    # tier without visibly degrading the watercolor illustrations.
    from PIL import Image
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        if max(w, h) > 800:
            scale = 800 / max(w, h)
            im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        im.save(dest, format="JPEG", quality=78, optimize=True, progressive=True)
    return dest


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
        epub_img = _resize_for_epub(image_path)
        parts.append(f"![{alt}]({epub_img.resolve()})\n\n")
    # Polish the raw JSON prose before rendering: strip Reddit URL fragments,
    # insert paragraph breaks at signal phrases, bulletize the avoidance list.
    description = polish_description(scam["description"])
    avoidance = polish_avoidance(scam["avoidance"])
    location = polish_location(scam["location"])
    parts.extend([
        f'### How this scam works\n\n{description}\n\n',
        f'### How to avoid it\n\n{avoidance}\n\n',
        f'**Where it happens:** {location}\n\n',
    ])
    if scam.get("tags"):
        parts.append(f'*{" · ".join(scam["tags"])}*\n\n')
    return "".join(parts)


def city_display_name(slug: str, data: dict) -> str:
    """Return the preferred display name for a city.

    Map slug → display-name so the book prints Saint-Tropez, Mont Saint-Michel,
    etc. consistently in chapter headings and the TOC, regardless of how the
    upstream JSON stores the city field.
    """
    DISPLAY = {
        "paris": "Paris",
        "nice": "Nice",
        "cannes": "Cannes",
        "st-tropez": "Saint-Tropez",
        "marseille": "Marseille",
        "avignon": "Avignon",
        "montpellier": "Montpellier",
        "toulouse": "Toulouse",
        "lyon": "Lyon",
        "chamonix": "Chamonix",
        "annecy": "Annecy",
        "bordeaux": "Bordeaux",
        "biarritz": "Biarritz",
        "strasbourg": "Strasbourg",
        "colmar": "Colmar",
        "mont-saint-michel": "Mont-Saint-Michel",
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
        # Resize 2K city covers to 1200px for EPUB embedding (originals stay
        # 2K in the desktop bundle).
        dest_dir = BUILD / "cities"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{slug}.jpg"
        if not dest.exists() or dest.stat().st_mtime < city_img.stat().st_mtime:
            subprocess.run(
                ["sips", "-Z", "1200", "-s", "format", "jpeg",
                 "-s", "formatOptions", "85", str(city_img), "--out", str(dest)],
                check=True, capture_output=True,
            )
        parts.append(f"![{alt}]({dest.resolve()})\n\n")
    intro_path = MANUSCRIPT / f"cities-{slug}-intro.md"
    if intro_path.exists():
        parts.append(intro_path.read_text().strip() + "\n\n")
    else:
        parts.append(
            f"> **TODO** — write a 1-page intro for {city}: "
            f"overall risk level, top 3 neighborhoods to watch, "
            f"nearest Police nationale commissariat, one safe recommendation.\n\n"
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


def _normalize_currency(md: str) -> str:
    """Convert hyphens in numeric currency ranges to en-dashes.

    Pandoc +smart converts -- to em-dash but leaves single hyphens between
    digits as-is. The euro symbol € is well-supported in Arial Unicode MS,
    so no symbol substitution is needed for France.
    """
    # Convert hyphens in numeric ranges followed by a currency token.
    md = re.sub(
        r"(\b[\d,.]+)-([\d,.]+\s*(?:euros?|EUR|€|\$))",
        r"\1–\2",
        md,
    )
    # Range: €N-€N or €N-N
    md = re.sub(r"(€[\d,.]+)\s*-\s*€?([\d,.]+)", r"\1–\2", md)
    # Range: $N-$N
    md = re.sub(r"(\$[\d,.]+)-(\$?[\d,.]+)", r"\1–\2", md)
    return md


def _rewrite_gallery_thumbnails(md: str) -> str:
    """Rewrite manuscript inline `(assets/cities/<slug>.jpg)` gallery refs to
    point at the resized BUILD/cities/<slug>.jpg copy. Without this the front
    16-city glance in 04-cities-section.md doubles the EPUB size by embedding
    the 2K originals."""
    def repl(m: re.Match) -> str:
        slug = m.group(1)
        src = ASSETS / "cities" / f"{slug}.jpg"
        if not src.exists():
            return m.group(0)
        dest_dir = BUILD / "cities"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{slug}.jpg"
        if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
            subprocess.run(
                ["sips", "-Z", "1200", "-s", "format", "jpeg",
                 "-s", "formatOptions", "85", str(src), "--out", str(dest)],
                check=True, capture_output=True,
            )
        return f"]({dest.resolve()})"
    return re.sub(r"\]\(assets/cities/([a-z0-9\-]+)\.jpg\)", repl, md)


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
    return _normalize_currency(_rewrite_gallery_thumbnails("".join(parts)))


def build_epub(md: str) -> Path:
    md_path = BUILD / "manuscript.md"
    md_path.write_text(md)

    out_name = CONFIG.get("output_filename", "france-scams")
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
