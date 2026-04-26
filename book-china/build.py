#!/usr/bin/env python3
"""
Build Kindle EPUB from JSON scam data + manuscript markdown.

Usage:
    python3 book-china/build.py

Produces: book-china/build/china-scams.epub
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

# Rich alt text for Chinese city chapter openers (screen-reader friendly).
CITY_ALT_TEXT: dict[str, str] = {
    "beijing": "Beijing — the Forbidden City rooftops and the Jingshan Park pavilion silhouette",
    "shanghai": "Shanghai — the Bund waterfront and the Pudong skyline at dusk",
    "xian": "Xi'an — the medieval city wall with bicycles at golden hour",
    "chengdu": "Chengdu — a giant panda in a bamboo grove at the Chengdu Research Base",
    "chongqing": "Chongqing — the Hongya Cave stilt houses illuminated along the Yangtze",
    "guangzhou": "Guangzhou — the Canton Tower and Pearl River at blue hour",
    "shenzhen": "Shenzhen — the Ping An Finance Center above Shenzhen Bay",
    "hangzhou": "Hangzhou — the Leifeng Pagoda above West Lake at golden hour",
    "suzhou": "Suzhou — a moon-gate and willow along a Humble Administrator's Garden canal",
    "guilin": "Guilin — karst peaks rising from the Li River at dawn mist",
    "yangshuo": "Yangshuo — a cormorant fisherman on a bamboo raft below karst peaks",
    "lijiang": "Lijiang — a stone bridge and canal through the Old Town at twilight",
    "kunming": "Kunming — the Stone Forest limestone pinnacles at golden hour",
    "pingyao": "Pingyao — the Ming-dynasty city wall and courtyard roofs at sunset",
    "harbin": "Harbin — the Saint Sophia Cathedral in winter snow",
    "zhangjiajie": "Zhangjiajie — towering sandstone pillars above a sea of clouds",
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
    """Return the preferred display name for a city.

    Map slug → display-name so the book prints Xi'an, Chongqing,
    Zhangjiajie, etc. consistently in chapter headings and the TOC,
    regardless of how the upstream JSON stores the city field.
    """
    DISPLAY = {
        "beijing": "Beijing",
        "shanghai": "Shanghai",
        "xian": "Xi'an",
        "chengdu": "Chengdu",
        "chongqing": "Chongqing",
        "guangzhou": "Guangzhou",
        "shenzhen": "Shenzhen",
        "hangzhou": "Hangzhou",
        "suzhou": "Suzhou",
        "guilin": "Guilin",
        "yangshuo": "Yangshuo",
        "lijiang": "Lijiang",
        "kunming": "Kunming",
        "pingyao": "Pingyao",
        "harbin": "Harbin",
        "zhangjiajie": "Zhangjiajie",
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
            f"nearest Public Security Bureau (公安局) station, one safe recommendation.\n\n"
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


_RANGE_RE = re.compile(r"(?<![\w\-\d])(\d[\d,.]*)-(\d[\d,.]*)(?=[\s%×)]|g\b|kg\b|m\b|km\b)")


def _normalize_ranges(md: str) -> str:
    """Convert digit ranges like '300-400 RMB' to en-dash '300–400 RMB'.

    Skips 1-800 toll-free numbers (preserved verbatim in the recovery /
    contacts appendices). Skips inside fenced code blocks and URLs.
    """
    def replace(m: re.Match) -> str:
        a, b = m.group(1), m.group(2)
        if a == "1" and b == "800":
            return m.group(0)
        return f"{a}–{b}"

    out_lines: list[str] = []
    in_code = False
    for line in md.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code or "http://" in line or "https://" in line:
            out_lines.append(line)
            continue
        out_lines.append(_RANGE_RE.sub(replace, line))
    return "".join(out_lines)


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
    return _normalize_ranges(polish_markdown("".join(parts)))


def build_epub(md: str) -> Path:
    md_path = BUILD / "manuscript.md"
    md_path.write_text(md)

    out_name = CONFIG.get("output_filename", "china-scams")
    epub_path = BUILD / f"{out_name}.epub"
    cover = ASSETS / "cover.jpg"
    css = TEMPLATES / "style.css"

    cmd = [
        "pandoc",
        str(md_path),
        "-o",
        str(epub_path),
        # Disable LaTeX math-dollar syntax: prose contains currency like "$10-20"
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


def _inline_svg_images(svg_text: str, svg_dir: Path) -> str:
    """Replace relative <image href="X.jpg"> refs with base64 data URIs.

    rsvg-convert 2.62+ silently drops images it can't resolve (gotcha #3).
    The cover SVGs reference `front.jpg` relative to the SVG's directory,
    but gen_comics.py writes the artwork to `assets/covers/`. Without
    inlining, the rendered Kindle cover ends up as just the gradient
    overlay + text — no illustration. Look in the SVG dir first, then
    fall back to a sibling `covers/` directory.
    """
    import base64, mimetypes

    def to_data_uri(m: re.Match) -> str:
        attr, quote, href = m.group(1), m.group(2), m.group(3)
        if href.startswith(("http://", "https://", "data:", "file://")):
            return m.group(0)
        candidates = []
        if href.startswith("/"):
            candidates.append(Path(href))
        else:
            candidates.append(svg_dir / href)
            candidates.append(svg_dir.parent / "covers" / Path(href).name)
        src = next((p for p in candidates if p.exists()), None)
        if src is None:
            return m.group(0)
        mime = mimetypes.guess_type(src.name)[0] or "application/octet-stream"
        encoded = base64.b64encode(src.read_bytes()).decode("ascii")
        return f"{attr}={quote}data:{mime};base64,{encoded}{quote}"

    return re.sub(r'(xlink:href|href)=(["\'])([^"\']+)\2', to_data_uri, svg_text)


def render_cover() -> None:
    """Rebuild cover.jpg from the SVG source if the SVG is newer.
    Produces a 1600x2560 JPG (KDP spec, 1.6:1 aspect, ~300 DPI)."""
    svg = ASSETS / "svg" / "front.svg"
    jpg = ASSETS / "cover.jpg"
    if not svg.exists():
        return
    if jpg.exists() and jpg.stat().st_mtime >= svg.stat().st_mtime:
        return
    inlined = _inline_svg_images(svg.read_text(), svg.parent)
    inlined_svg = BUILD / "cover_inlined.svg"
    inlined_svg.write_text(inlined)
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
