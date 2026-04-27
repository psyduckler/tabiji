#!/usr/bin/env python3
"""
Build Kindle EPUB from JSON scam data + manuscript markdown.

Usage:
    python3 book-morocco/build.py

Produces: book-morocco/build/morocco-scams.epub
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

# Rich alt text for Moroccan city chapter openers (screen-reader friendly).
CITY_ALT_TEXT: dict[str, str] = {
    "marrakech": "Marrakech — Djemaa el-Fna at dusk with the Koutoubia Mosque minaret silhouetted against the Atlas Mountains",
    "fez": "Fez — the leather tanneries of Chouara from a rooftop at golden hour, with the medina of Fez al-Bali behind",
    "casablanca": "Casablanca — the Hassan II Mosque rising over the Atlantic at sunset, silhouetted against the city skyline",
    "rabat": "Rabat — the Kasbah des Oudayas ramparts overlooking the Bouregreg river and the Atlantic",
    "tangier": "Tangier — the Bay of Tangier from the kasbah, with the medina above and the Mediterranean meeting the Atlantic",
    "chefchaouen": "Chefchaouen — the blue-washed medina alleys at golden hour with the Rif Mountains rising behind",
    "essaouira": "Essaouira — the white-and-blue medina ramparts and Atlantic surf at sunset, seagulls overhead",
    "agadir": "Agadir — the long curve of Agadir Bay with palm-lined corniche and the Atlantic at golden hour",
    "merzouga": "Merzouga — the Erg Chebbi sand dunes at sunrise with a camel caravan silhouette and ochre sky",
    "ouarzazate": "Ouarzazate — the red-earth ksar of Aït Benhaddou at golden hour with the Atlas Mountains behind",
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

    Map slug → display-name so the book prints Xi'an, Chongqing,
    Zhangjiajie, etc. consistently in chapter headings and the TOC,
    regardless of how the upstream JSON stores the city field.
    """
    DISPLAY = {
        "marrakech": "Marrakech",
        "fez": "Fez",
        "casablanca": "Casablanca",
        "rabat": "Rabat",
        "tangier": "Tangier",
        "chefchaouen": "Chefchaouen",
        "essaouira": "Essaouira",
        "agadir": "Agadir",
        "merzouga": "Merzouga",
        "ouarzazate": "Ouarzazate",
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
            f"nearest Sûreté Nationale or Brigade Touristique post, one safe default.\n\n"
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

    The Moroccan dirham (MAD) is plain ASCII and renders fine in every font,
    so no symbol substitution is needed. But Pandoc +smart leaves bare hyphens
    between digits as-is — gotcha #5 — so a hyphen in `100-200 MAD` would render
    as a hyphen rather than the typographically correct `100–200 MAD`.
    """
    # (digits)-(digits) followed by Moroccan or shared currency words → en-dash
    md = re.sub(
        r"(\b[\d,.]+)-([\d,.]+\s*(?:MAD|DH|dirhams?|euro|euros|€|\$))",
        r"\1–\2",
        md,
    )
    # `$N-$N` or `$N-N` ranges
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
    return _normalize_currency("".join(parts))


def build_epub(md: str) -> Path:
    md_path = BUILD / "manuscript.md"
    md_path.write_text(md)

    out_name = CONFIG.get("output_filename", "morocco-scams")
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
    Produces a 1600x2560 JPG (KDP spec, 1.6:1 aspect, ~300 DPI).

    rsvg-convert 2.62+ silently drops images referenced by relative or
    absolute href in the source SVG (gotcha #3 in book-generator skill).
    Inline every <image href> as a base64 data URI before rendering.
    """
    import base64
    import mimetypes
    import re
    svg = ASSETS / "svg" / "front.svg"
    jpg = ASSETS / "cover.jpg"
    if not svg.exists():
        return
    svg_text = svg.read_text()

    def _inline(match: re.Match) -> str:
        attr, quote, href = match.group(1), match.group(2), match.group(3)
        if href.startswith(("http://", "https://", "data:", "file://")):
            return match.group(0)
        # Resolve in this order: absolute path; next to the SVG; assets/covers/.
        # gen_comics.py writes the underlying art to assets/covers/, but the SVG
        # references it as a bare filename (relative).
        candidates: list[Path] = []
        if href.startswith("/"):
            candidates.append(Path(href))
        else:
            candidates.append(svg.parent / href)
            candidates.append(ASSETS / "covers" / href)
        src = next((p for p in candidates if p.exists()), None)
        if src is None:
            return match.group(0)
        mime = mimetypes.guess_type(src.name)[0] or "image/jpeg"
        encoded = base64.b64encode(src.read_bytes()).decode("ascii")
        return f"{attr}={quote}data:{mime};base64,{encoded}{quote}"

    svg_inlined = re.sub(
        r"(xlink:href|href)=(['\"])([^'\"]+)\2",
        _inline,
        svg_text,
    )
    inlined_svg = BUILD / "cover_tmp.svg"
    inlined_svg.write_text(svg_inlined)

    # If inlining changed nothing AND jpg is current, skip; otherwise re-render.
    if jpg.exists() and svg_inlined == svg_text and jpg.stat().st_mtime >= svg.stat().st_mtime:
        inlined_svg.unlink(missing_ok=True)
        return

    png_tmp = BUILD / "cover_tmp.png"
    subprocess.run(
        ["rsvg-convert", "-w", "1600", "-h", "2560", str(inlined_svg), "-o", str(png_tmp)],
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
    inlined_svg.unlink(missing_ok=True)


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
