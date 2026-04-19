#!/usr/bin/env python3
"""
Build the KDP paperback wraparound cover PDF for the France book.

Composes back.svg (left) + spine (middle, with vertical title) + front.svg (right)
into a single print-ready PDF at the exact dimensions KDP requires, including bleed.

Target trim: 6" x 9" (the KDP-standard non-fiction trade paperback size).
The source SVGs in assets/svg/ were designed for a 5"x8" viewBox (500x800 units);
they are uniformly scaled to fit the 9" trim height and centered horizontally
inside the 6" trim width — the side gap fills naturally with the navy bleed
gradient so the preserved 5:8 composition reads as an intentionally-generous
framed design rather than a letterbox.

Default --pages (287, cream) produces an output exactly 12.968" x 9.250",
which is what KDP's cover calculator expects for this title. Override with
--pages N if the final interior comes in at a different page count.

Usage:
    python3 book-france/scripts/build_paperback_cover.py                 # 287 pages, cream
    python3 book-france/scripts/build_paperback_cover.py --pages 268
    python3 book-france/scripts/build_paperback_cover.py --paper white
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
FRONT_SVG = BOOK / "assets" / "svg" / "front.svg"
BACK_SVG = BOOK / "assets" / "svg" / "back.svg"
OUT_SVG = BOOK / "build" / "thailand-paperback-cover.svg"
OUT_PDF = BOOK / "build" / "thailand-paperback-cover.pdf"

TRIM_W_IN = 6.0           # KDP trade-paperback 6x9 trim
TRIM_H_IN = 9.0
BLEED_IN = 0.125
UNITS_PER_IN = 100

# The source SVGs were designed for 5"x8" (500x800 viewBox units).
# Used to compute the nested-SVG scale factor when we embed them in the larger
# 6x9 trim regions of the paperback.
SOURCE_W = 500
SOURCE_H = 800


def extract_inner(svg_text: str, source_svg_dir: Path | None = None) -> str:
    """Strip the outer <svg ...> / </svg> tags; return everything between.

    If `source_svg_dir` is provided, rewrite any relative `xlink:href="..."` or
    `href="..."` image attributes to base64 data URIs so embedded `<image>` tags
    still resolve when composed into a combined SVG rendered elsewhere.
    (rsvg-convert 2.62 silently fails to load absolute-path images, so we inline
    the bytes.)
    """
    import base64
    import mimetypes

    m = re.match(r"<svg[^>]*>\s*", svg_text, re.DOTALL)
    if not m:
        raise ValueError("no opening <svg> tag")
    inner = svg_text[m.end():]
    inner = re.sub(r"</svg>\s*$", "", inner, flags=re.DOTALL)

    if source_svg_dir is not None:
        def to_data_uri(match: re.Match) -> str:
            attr, quote, href = match.group(1), match.group(2), match.group(3)
            # skip already-absolute-URL and data URIs
            if href.startswith(("http://", "https://", "data:", "file://")):
                return match.group(0)
            # resolve to a local file and inline
            src = source_svg_dir / href if not href.startswith("/") else Path(href)
            if not src.exists():
                return match.group(0)
            mime, _ = mimetypes.guess_type(src.name)
            mime = mime or "application/octet-stream"
            encoded = base64.b64encode(src.read_bytes()).decode("ascii")
            return f'{attr}={quote}data:{mime};base64,{encoded}{quote}'

        inner = re.sub(
            r'(xlink:href|href)=(["\'])([^"\']+)\2',
            to_data_uri,
            inner,
        )
    return inner.strip()


def paperback_back_content(back_inner: str) -> str:
    """Transform the eBook back-cover inner content for paperback print.

    - Removes the QR-code panel and the 'Scan for the full...' tagline so
      Amazon's auto-generated ISBN barcode has a clean area to live in.
    - Relabels the footer from KINDLE EDITION to PAPERBACK EDITION and
      bumps it up so it doesn't compete with the barcode zone (Amazon
      reserves the lower-right ~2\" × 1.2\" of the back cover).
    """
    # 1. Strip the QR-panel group — from the "QR CODE PANEL" comment through
    #    the matching </g></g> pair that closes the outer translate group.
    back_inner = re.sub(
        r"<!-- =+\s*QR CODE PANEL\s*=+ -->\s*"
        r"<!--[^>]*-->\s*"
        r"<g\s+transform=\"translate\(250 662\)\">.*?</g>\s*</g>",
        "",
        back_inner,
        flags=re.DOTALL,
    )

    # 2. Strip the 'Scan for the full Travel Safety Series...' tagline.
    back_inner = re.sub(
        r"<text[^>]*>\s*Scan for the full Travel Safety Series[^<]*</text>\s*",
        "",
        back_inner,
    )

    # 3. Relabel footer + move it up above Amazon's barcode zone (y < 680).
    back_inner = re.sub(
        r'(<text x="250" y=")770(" [^>]*>)KINDLE EDITION(\s*&#183;\s*2026)(</text>)',
        r'\g<1>618\g<2>PAPERBACK EDITION\g<3>\g<4>',
        back_inner,
    )

    return back_inner


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=287, help="Interior page count "
                    "(default 287 cream = 0.718\" spine, matching KDP's expected "
                    "12.968\"x9.250\" total for 6x9 trim)")
    ap.add_argument("--paper", choices=["cream", "white"], default="cream")
    args = ap.parse_args()

    per_page = 0.0025 if args.paper == "cream" else 0.002252
    spine_in = args.pages * per_page

    trim_w = TRIM_W_IN * UNITS_PER_IN       # 600
    trim_h = TRIM_H_IN * UNITS_PER_IN       # 900
    bleed = BLEED_IN * UNITS_PER_IN          # 12.5
    spine = spine_in * UNITS_PER_IN          # e.g., 71.8 at 287 pages cream

    # Source is 500x800; fit to trim height (9"). Uniform scale = 900/800 = 1.125.
    # Nested SVG is 562.5 wide × 900 tall, centered horizontally inside the 600-wide
    # trim region. The 18.75-unit side gap is filled by the navy bleed gradient.
    scale = trim_h / SOURCE_H
    nested_w = SOURCE_W * scale
    nested_h = trim_h
    side_pad = (trim_w - nested_w) / 2

    total_w = bleed + trim_w + spine + trim_w + bleed
    total_h = bleed + trim_h + bleed

    back_x = bleed + side_pad
    spine_x = bleed + trim_w
    front_x = bleed + trim_w + spine + side_pad
    spine_cx = spine_x + spine / 2
    cover_cy = total_h / 2

    print(f"Pages:     {args.pages} ({args.paper})")
    print(f"Spine:     {spine_in:.4f}\" ({spine:.2f} SVG units, {spine_in * 25.4:.2f} mm)")
    print(f"Trim:      {TRIM_W_IN}\" × {TRIM_H_IN}\" per cover side")
    print(f"Cover:     {total_w / UNITS_PER_IN:.3f}\" × {total_h / UNITS_PER_IN:.3f}\" "
          f"({total_w:.1f} × {total_h:.1f} units)")
    print(f"Nested:    {nested_w / UNITS_PER_IN:.3f}\" × {nested_h / UNITS_PER_IN:.3f}\" "
          f"per cover (side pad {side_pad / UNITS_PER_IN:.3f}\")")

    front_inner = extract_inner(FRONT_SVG.read_text(), source_svg_dir=FRONT_SVG.parent)
    back_inner = paperback_back_content(
        extract_inner(BACK_SVG.read_text(), source_svg_dir=BACK_SVG.parent)
    )

    # Declare the outer SVG with explicit physical units so rsvg-convert emits
    # a PDF whose MediaBox is exactly 12.968"x9.250" — not "12.968 pixels at 96 dpi".
    total_w_in = total_w / UNITS_PER_IN
    total_h_in = total_h / UNITS_PER_IN
    svg = f"""<svg width="{total_w_in}in" height="{total_h_in}in"
     viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg"
     preserveAspectRatio="xMidYMid meet" xmlns:xlink="http://www.w3.org/1999/xlink">
  <!-- ================================================================ -->
  <!-- FRANCE PAPERBACK WRAPAROUND COVER                               -->
  <!-- KDP spec: 5"x8" trim, cream paper, {args.pages} pages            -->
  <!-- Spine: {spine_in:.4f}"; total {total_w / UNITS_PER_IN:.3f}"x{total_h / UNITS_PER_IN:.3f}" incl 0.125" bleed -->
  <!-- Order (left→right): BACK | SPINE | FRONT                        -->
  <!-- ================================================================ -->

  <!-- Full-canvas navy bleed (matches cover palette so any trim drift
       still produces a clean navy edge, not a white stripe) -->
  <defs>
    <linearGradient id="fullBleed" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#0F1A2E"/>
      <stop offset="1" stop-color="#1E2F4D"/>
    </linearGradient>
  </defs>
  <rect width="{total_w}" height="{total_h}" fill="url(#fullBleed)"/>

  <!-- ========== BACK COVER (left) ========== -->
  <svg x="{back_x}" y="{bleed}" width="{nested_w}" height="{nested_h}" viewBox="0 0 {SOURCE_W} {SOURCE_H}">
{back_inner}
  </svg>

  <!-- ========== SPINE (middle) ========== -->
  <!-- Thin vertical gold rules along the spine-trim edges -->
  <line x1="{spine_x}" y1="{bleed + 40}" x2="{spine_x}" y2="{total_h - bleed - 40}"
        stroke="#D4A12E" stroke-width="0.4" opacity="0.6"/>
  <line x1="{spine_x + spine}" y1="{bleed + 40}" x2="{spine_x + spine}" y2="{total_h - bleed - 40}"
        stroke="#D4A12E" stroke-width="0.4" opacity="0.6"/>

  <!-- TABIJI mark near the top of the spine (European convention: text reads
       bottom-to-top when book is face-up on a table) -->
  <g transform="translate({spine_cx} {bleed + 110}) rotate(-90)">
    <text x="0" y="3" font-family="Georgia, serif" font-size="7" fill="#D4A12E"
          text-anchor="middle" letter-spacing="3" opacity="0.9">T A B I J I</text>
  </g>

  <!-- Main spine title: THAILAND + Tourist Scams, centered -->
  <g transform="translate({spine_cx} {cover_cy}) rotate(-90)">
    <text x="0" y="-4" font-family="Georgia, serif" font-weight="700" font-size="20"
          fill="#F5E9D3" text-anchor="middle" letter-spacing="3">THAILAND</text>
    <text x="0" y="14" font-family="Georgia, serif" font-style="italic" font-size="10"
          fill="#D4A12E" text-anchor="middle" letter-spacing="1">Tourist Scams</text>
  </g>

  <!-- Roman-numeral edition year near the bottom of the spine -->
  <g transform="translate({spine_cx} {total_h - bleed - 110}) rotate(-90)">
    <text x="0" y="3" font-family="Georgia, serif" font-size="7" fill="#D4A12E"
          text-anchor="middle" letter-spacing="3" opacity="0.9">M M X X V I</text>
  </g>

  <!-- ========== FRONT COVER (right) ========== -->
  <svg x="{front_x}" y="{bleed}" width="{nested_w}" height="{nested_h}" viewBox="0 0 {SOURCE_W} {SOURCE_H}">
{front_inner}
  </svg>
</svg>
"""

    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    OUT_SVG.write_text(svg)

    # Render to vector PDF. Physical dimensions come from the SVG's
    # width="..in" / height="..in" attributes (not --width/--height pixels),
    # so the PDF's MediaBox is exactly total_w_in x total_h_in.
    subprocess.run(
        ["rsvg-convert", "--format=pdf", str(OUT_SVG), "-o", str(OUT_PDF)],
        check=True,
    )

    kb = OUT_PDF.stat().st_size / 1024
    print(f"✓ Wrote {OUT_PDF} ({kb:.0f} KB)")
    print(f"✓ Source SVG: {OUT_SVG}")


if __name__ == "__main__":
    main()
