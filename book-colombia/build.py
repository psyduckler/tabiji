#!/usr/bin/env python3
"""
Build Kindle EPUB from JSON scam data + manuscript markdown.

Usage:
    python3 book-colombia/build.py

Produces: book-colombia/build/colombia-scams.epub
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

sys.path.insert(0, str(HERE / "scripts"))
from polish_scam_prose import polish_description, polish_avoidance, polish_location, polish_markdown  # noqa: E402

# Rich alt text for Colombian city chapter openers (screen-reader friendly).
CITY_ALT_TEXT: dict[str, str] = {
    "bogota": "Bogotá — La Candelaria's painted balconies and Cerro Monserrate above the Andean skyline",
    "medellin": "Medellín — the Comuna 13 hillside escalators and brick-red barrios in the Aburrá Valley",
    "cartagena": "Cartagena — the Walled City's bougainvillea balconies above Plaza Santo Domingo",
    "cali": "Cali — the Cristo Rey statue and Río Cali bridges with palm-lined San Antonio rooftops",
    "santa-marta": "Santa Marta — the colonial cathedral and Tayrona ridgeline above Rodadero beach",
    "guatape": "Guatapé — the painted zócalos of Plaza de los Zócalos and La Piedra del Peñol monolith",
    "salento": "Salento — Cocora Valley wax-palm silhouettes above coffee-axis hillsides",
    "tayrona": "Tayrona — Cabo San Juan's twin coves and jungle-fringed Caribbean palms",
    "san-andres": "San Andrés — the seven-color Caribbean shallows around Johnny Cay",
    "villa-de-leyva": "Villa de Leyva — Plaza Mayor's whitewashed facades under Boyacá's high-altitude sky",
}


def load_city(slug: str) -> dict:
    path = DATA_DIR / f"{slug}.json"
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")
    return json.loads(path.read_text())


def _normalize_scam(scam: dict) -> dict:
    """Adapt newer api/v1 scams (howToAvoid array, no frequency, no tags) onto
    the legacy shape this builder was written against. All 10 Colombia cities
    are currently legacy-shaped, but keep the adapter for forward-compat."""
    if "howToAvoid" in scam and not scam.get("avoidance"):
        v = scam["howToAvoid"]
        scam["avoidance"] = " ".join(v) if isinstance(v, list) else str(v)
    scam.setdefault("frequency", "common")
    scam.setdefault("tags", [])
    return scam


def scam_md(scam: dict, image_path: Path | None = None) -> str:
    scam = _normalize_scam(scam)
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
    # Render tldr (when present) as an italic lead-in. Many Colombia scam
    # descriptions begin with a sentence that references the tldr, so dropping
    # it would leave the first paragraph reading like a sequel. Italy V2 uses
    # the same pattern.
    tldr = scam.get("tldr", "").strip()
    if tldr:
        parts.append(f"*{tldr}*\n\n")
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


def city_chapter_md(data: dict) -> str:
    slug = data["slug"]
    city = data.get("city", slug.title())
    parts = [f"\n\n# {city}\n\n"]
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
            f"nearest Policía de Turismo, one safe recommendation.\n\n"
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
    return polish_markdown("".join(parts))


def build_epub(md: str) -> Path:
    md_path = BUILD / "manuscript.md"
    md_path.write_text(md)

    out_name = CONFIG.get("output_filename", "colombia-scams")
    epub_path = BUILD / f"{out_name}.epub"
    cover = ASSETS / "cover.jpg"
    css = TEMPLATES / "style.css"

    cmd = [
        "pandoc",
        str(md_path),
        "-o",
        str(epub_path),
        # Disable LaTeX math-dollar parsing — prose uses "$10–20" / "20,000 COP"
        # paired with another "$N" elsewhere in paragraphs, which pandoc
        # otherwise interprets as math and mangles.
        "--from", "markdown-tex_math_dollars-tex_math_single_backslash-tex_math_double_backslash-raw_tex-raw_attribute",
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
