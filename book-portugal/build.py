#!/usr/bin/env python3
"""
Build Kindle EPUB from JSON scam data + manuscript markdown.

Usage:
    python3 book/build.py

Produces: book/build/japan-scams.epub
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

# Rich alt text for city chapter openers (screen-reader friendly).
# Mirrors the landmark descriptions used in the front-matter gallery so the
# same image gets the same spoken description regardless of where it appears.
CITY_ALT_TEXT: dict[str, str] = {
    # Japan volume
    "tokyo": "Stylized illustration of Tokyo — Shibuya crossing and Tokyo Tower at dusk",
    "kyoto": "Stylized illustration of Kyoto — the Fushimi Inari torii-gate tunnel at dusk",
    "osaka": "Stylized illustration of Osaka — the Dotonbori canal and Glico running-man sign",
    "sapporo": "Stylized illustration of Sapporo — Sapporo TV Tower above Odori Park in ginkgo season",
    "fukuoka": "Stylized illustration of Fukuoka — a Hakata yatai food-stall row at dusk",
    "hiroshima": "Stylized illustration of Hiroshima — the Itsukushima Shrine floating torii at high tide",
    "nara": "Stylized illustration of Nara — the Todai-ji Great Buddha Hall with deer in the foreground",
    "okinawa": "Stylized illustration of Okinawa — the Shuri Castle gate above a turquoise sea",
    "yokohama": "Stylized illustration of Yokohama — Minato Mirai and the Cosmo Clock Ferris wheel at dusk",
    # France volume
    "paris": "Paris — Eiffel Tower and Haussmann rooftops at dusk",
    "nice": "Nice — Promenade des Anglais curve and Baie des Anges",
    "cannes": "Cannes — Croisette palms and Palais des Festivals",
    "st-tropez": "Saint-Tropez — Vieux Port yachts at golden hour",
    "marseille": "Marseille — Vieux-Port and Notre-Dame de la Garde",
    "avignon": "Avignon — Palais des Papes and Pont Saint-Bénézet",
    "montpellier": "Montpellier — Place de la Comédie and the Three Graces fountain",
    "toulouse": "Toulouse — Place du Capitole at blue hour",
    "lyon": "Lyon — Vieux Lyon and Fourvière Basilica above the Saône",
    "chamonix": "Chamonix — Mont Blanc and the Aiguille du Midi",
    "annecy": "Annecy — turquoise lake and Palais de l’Ile",
    "bordeaux": "Bordeaux — Place de la Bourse and the Miroir d’Eau",
    "biarritz": "Biarritz — Grande Plage and Rocher de la Vierge",
    "strasbourg": "Strasbourg — the Cathedral and Petite France half-timbered houses",
    "colmar": "Colmar — Petite Venise canal and half-timbered houses",
    "mont-saint-michel": "Mont-Saint-Michel — tidal causeway and Abbey silhouette",
    # Vietnam volume
    "hanoi": "Hanoi — Old Quarter lanterns and One Pillar Pagoda at golden hour",
    "ha-long-bay": "Ha Long Bay — karst limestone islands and traditional junk-boat sails",
    "sapa": "Sapa — terraced rice fields and Fansipan peak in mountain mist",
    "hue": "Hue — Perfume River and Thien Mu Pagoda at sunset",
    "hoi-an": "Hoi An — lanterns, canal boats, and the Japanese Covered Bridge at night",
    "da-nang": "Da Nang — Dragon Bridge at dusk over the Han River",
    "nha-trang": "Nha Trang — long crescent beach and Po Nagar Cham Towers",
    "dalat": "Dalat — misty highlands, pastel railway station, Xuan Huong lake",
    "ho-chi-minh-city": "Ho Chi Minh City — Notre-Dame spires and Saigon Central Post Office",
    "can-tho": "Can Tho — Cai Rang floating market at dawn on the Mekong Delta",
    "phu-quoc": "Phu Quoc — Sao Beach sunset and basket-boat silhouette",
    # Thailand volume
    "bangkok": "Bangkok — Wat Arun riverside temple at dusk over the Chao Phraya",
    "chiang-mai": "Chiang Mai — Doi Suthep temple stairs with the naga-balustrade ascent",
    "ayutthaya": "Ayutthaya — Wat Mahathat ruins and the Buddha head in banyan roots",
    "pattaya": "Pattaya — Beach Road palms and the neon Walking Street skyline",
    "hua-hin": "Hua Hin — the royal railway-station pavilion at golden hour",
    "phuket": "Phuket — Karon Beach longtail boats at sunset",
    "krabi": "Krabi — Railay peninsula karst cliffs and Andaman turquoise",
    "koh-samui": "Koh Samui — Chaweng palm-fringed beach at sunset",
    "koh-phangan": "Koh Phangan — Haad Rin headland at moonrise",
    "koh-tao": "Koh Tao — Nang Yuan twin-island sandbar view",
    "koh-phi-phi": "Koh Phi Phi — Maya Bay limestone cliffs at golden hour",
}


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
        # Descriptive alt text for screen readers and KDP accessibility compliance.
        # Category + name + severity is what a blind reader needs to know before
        # the heading that follows explains the scam in detail.
        alt = (
            f'Stylized illustration depicting the {scam["name"]} scam — '
            f'a {cat.lower()} scam rated {sev.lower()} severity'
        )
        # Absolute path; Pandoc will copy into the EPUB package
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


def city_chapter_md(data: dict) -> str:
    city = data["city"]
    slug = data["slug"]
    parts = [f"\n\n# {city}\n\n"]
    # Chapter-opening city illustration (flat-vector travel-poster style).
    # Lives at assets/cities/<slug>.jpg — generated by scripts/gen_city_illustrations.py.
    # Uses the same relative path form as the gallery so pandoc dedupes the
    # image inside the EPUB (otherwise each of the 9 cities ships twice).
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
            f"nearest koban, one safe recommendation.\n\n"
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

    out_name = CONFIG.get("output_filename", "japan-scams")
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
    # Prefer ImageMagick if available; fall back to macOS sips (built-in).
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
