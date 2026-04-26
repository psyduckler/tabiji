#!/usr/bin/env python3
"""
Build Kindle EPUB from JSON scam data + manuscript markdown.

Usage:
    python3 book-mexico/build.py

Produces: book-mexico/build/mexico-scams.epub
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

# Rich alt text for Mexican city chapter openers (screen-reader friendly).
CITY_ALT_TEXT: dict[str, str] = {
    "mexico-city": "Mexico City — the Catedral Metropolitana and Zócalo flag at golden hour",
    "puebla": "Puebla — the Talavera-tiled facades and Popocatépetl volcano on the horizon",
    "oaxaca": "Oaxaca — the Templo de Santo Domingo cantera-stone facade above jacaranda trees",
    "guanajuato": "Guanajuato — the Callejón del Beso painted alley and pastel-tiered hillside houses",
    "san-miguel-de-allende": "San Miguel de Allende — the pink-spired Parroquia rising over the Jardín",
    "guadalajara": "Guadalajara — the twin yellow-tile spires of the Catedral above mariachi square",
    "merida": "Mérida — the white limestone Plaza Grande and Casa de Montejo at midday",
    "san-cristobal-de-las-casas": "San Cristóbal de las Casas — the yellow Templo de Santo Domingo and pine-clad Chiapas hills",
    "cancun": "Cancún — the turquoise Caribbean shoreline and Hotel Zone palm crescent",
    "playa-del-carmen": "Playa del Carmen — Quinta Avenida pedestrian street and ferry-terminal beach",
    "tulum": "Tulum — the cliffside El Castillo Mayan ruin above Caribbean blue water",
    "cozumel": "Cozumel — the San Miguel waterfront promenade and reef-edge ferry pier",
    "isla-mujeres": "Isla Mujeres — Playa Norte's shallow turquoise water and golf-cart boardwalk",
    "holbox": "Holbox — sandy unpaved streets, palm-thatched palapas and lagoon-side flamingos",
    "puerto-vallarta": "Puerto Vallarta — the Malecón seawall sculptures above Banderas Bay at sunset",
    "mazatlan": "Mazatlán — the Old Lighthouse cliff (El Faro) and the curve of Olas Altas at golden hour",
    "acapulco": "Acapulco — the La Quebrada cliff divers above the Pacific bay at dusk",
    "cabo-san-lucas": "Cabo San Lucas — El Arco rock arch and Land's End at the tip of Baja",
    "puerto-escondido": "Puerto Escondido — Zicatela Beach's Pipeline break and surfers at golden hour",
}


# Prose-polish helpers live in scripts/polish_scam_prose.py.
sys.path.insert(0, str(HERE / "scripts"))
from polish_scam_prose import polish_description, polish_avoidance, polish_location, polish_markdown  # noqa: E402


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
    """Return the preferred display name for a city, with proper diacritics."""
    DISPLAY = {
        "mexico-city": "Mexico City",
        "puebla": "Puebla",
        "oaxaca": "Oaxaca",
        "guanajuato": "Guanajuato",
        "san-miguel-de-allende": "San Miguel de Allende",
        "guadalajara": "Guadalajara",
        "merida": "Mérida",
        "san-cristobal-de-las-casas": "San Cristóbal de las Casas",
        "cancun": "Cancún",
        "playa-del-carmen": "Playa del Carmen",
        "tulum": "Tulum",
        "cozumel": "Cozumel",
        "isla-mujeres": "Isla Mujeres",
        "holbox": "Holbox",
        "puerto-vallarta": "Puerto Vallarta",
        "mazatlan": "Mazatlán",
        "acapulco": "Acapulco",
        "cabo-san-lucas": "Cabo San Lucas",
        "puerto-escondido": "Puerto Escondido",
    }
    if slug in DISPLAY:
        return DISPLAY[slug]
    return data.get("city", slug.title()).strip()


def city_chapter_md(data: dict) -> str:
    slug = data["slug"]
    city = city_display_name(slug, data)
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
            f"overall risk level, top 3 corridors to watch, "
            f"nearest *Ministerio Público* (MP) office for filing a *denuncia*, one safe recommendation.\n\n"
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


def _normalize_mexican_currency(md: str) -> str:
    """Mexican peso conventions — the source JSON uses `MX$` for pesos and bare
    `$` for USD. Both render natively in Arial Unicode MS, so no symbol-swap is
    needed (unlike Turkey's ₺).

    What we DO sweep:
      - Bare hyphens between two numbers immediately followed by a currency
        word (MX$, $, pesos, USD) — pandoc's +smart does NOT en-dash these.
      - Stray `MX $` (with space) → `MX$` (no space) for consistency.
      - Pseudo-USD markers like `US$` or `USD$` → `US$` canonical.
    """
    # Range: MX$N1 - MX$N2 (with optional spaces around dash)
    md = re.sub(
        r"MX\$([\d,.]+)\s*[–-]\s*MX\$([\d,.]+)",
        r"MX$\1–\2",
        md,
    )
    # Range: MX$N1 - $N2 → MX$N1–N2 (assume both pesos when first is MX$)
    md = re.sub(
        r"MX\$([\d,.]+)\s*[–-]\s*\$([\d,.]+)",
        r"MX$\1–\2",
        md,
    )
    # Range: bare $N1 - $N2 → $N1–N2 (USD or peso depending on context;
    # leave the symbol alone, fix the dash only)
    md = re.sub(
        r"(\$[\d,.]+)\s*[-]\s*(\$?[\d,.]+)",
        r"\1–\2",
        md,
    )
    # Range followed by currency word: 200-300 pesos → 200–300 pesos
    md = re.sub(
        r"(\b[\d,.]+)-([\d,.]+\s*(?:pesos|peso|MXN|USD))",
        r"\1–\2",
        md,
    )
    # Stray space inside MX$
    md = re.sub(r"MX\s+\$", "MX$", md)
    # USD$ or US $ → US$
    md = re.sub(r"USD\s*\$", "US$", md)
    md = re.sub(r"US\s+\$", "US$", md)

    # Collapse "US$ 50" / "MX$ 1,200" (currency-then-space-then-number) — the
    # bare space breaks LaTeX's math-delimiter heuristic and renders the rest of
    # the paragraph as italic-per-letter math gibberish in the paperback PDF.
    md = re.sub(r"\b(MX|US)\$\s+(\d)", r"\1$\2", md)
    # Same for bare `$ 50` (space) → `$50` when in numeric context
    md = re.sub(r"(?<![\\\w])\$\s+(\d)", r"$\1", md)

    # The `**$**` / `**US$**` bold markers in the intro produce a `\textbf{$}`
    # LaTeX output where the `$` re-enters math mode. Replace with non-bold
    # equivalents — the user-visible meaning ("we use $ for dollars") is preserved.
    md = md.replace("**$**", r"$").replace("**US$**", r"US$").replace("**MX$**", r"MX$")

    # Escape every remaining bare `$` to `\$`. In markdown, `\$` is a literal
    # dollar sign — pandoc renders it as `$` in HTML/EPUB and as `\$` in LaTeX
    # (preventing math-mode triggering, which would otherwise mangle paragraphs
    # containing multiple dollar tokens like `MX$5,000` and `$30 USD`).
    # Run last so all earlier regexes see plain `$`.
    md = re.sub(r"(?<!\\)\$", r"\\$", md)

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
    return polish_markdown(_normalize_mexican_currency("".join(parts)))


def build_epub(md: str) -> Path:
    md_path = BUILD / "manuscript.md"
    md_path.write_text(md)

    out_name = CONFIG.get("output_filename", "mexico-scams")
    epub_path = BUILD / f"{out_name}.epub"
    cover = ASSETS / "cover.jpg"
    css = TEMPLATES / "style.css"

    cmd = [
        "pandoc",
        str(md_path),
        "-o",
        str(epub_path),
        # Disable LaTeX math-dollar syntax: prose contains currency like "$30-50"
        # that pandoc otherwise treats as math delimiters, mangling paragraphs
        # into <em>-per-letter gibberish.
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
