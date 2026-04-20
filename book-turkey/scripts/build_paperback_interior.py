#!/usr/bin/env python3
"""
Build the paperback-interior PDF for the Turkey book.

Primary pipeline (preserves TOC page numbers):
  markdown (via assemble_markdown from build.py)
    → pandoc --pdf-engine=xelatex
    → paperback PDF (6x9 trim, proper LaTeX TOC with page numbers)

Fallback (Chrome headless — no TOC page numbers):
  markdown → standalone HTML → Chrome --headless --print-to-pdf

Target: 6"x9" trim, KDP-compliant inside/outside margins, running page numbers,
chapter breaks on new pages, widow/orphan control, image containment.

Usage:
    python3 book-turkey/scripts/build_paperback_interior.py

Prerequisites:
    - pandoc (brew install pandoc)
    - A LaTeX engine for TOC page numbers: xelatex / lualatex / pdflatex
      (BasicTeX, TinyTeX, or MacTeX all work)
    - Google Chrome (fallback only, if no LaTeX engine is available)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
BUILD = BOOK / "build"

sys.path.insert(0, str(BOOK))
from build import assemble_markdown, CONFIG  # noqa: E402

INTERIOR_HTML = BUILD / "turkey-scams-paperback.html"
INTERIOR_PDF = BUILD / "turkey-scams-paperback.pdf"
MANUSCRIPT_MD = BUILD / "paperback-manuscript.md"
PRINT_CSS_FILE = BUILD / "paperback-print.css"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Make sure TinyTeX (~/Library/TinyTeX/bin/universal-darwin) is on PATH
# when present, so the "which xelatex" check below succeeds in all shells.
_TINYTEX = Path.home() / "Library" / "TinyTeX" / "bin" / "universal-darwin"
if _TINYTEX.exists():
    os.environ["PATH"] = f"{_TINYTEX}:{os.environ.get('PATH', '')}"


# ---------------------------------------------------------------------------
# Print CSS — KDP 6"x9" trim with professional paperback typography.
# Used only for the Chrome-headless fallback path; xelatex takes over styling
# for the primary path.
# ---------------------------------------------------------------------------
PRINT_CSS = r"""
@page {
  size: 6in 9in;
  margin-top: 0.75in;
  margin-bottom: 0.75in;
  margin-left: 0.75in;
  margin-right: 0.75in;
  @bottom-center {
    content: counter(page);
    font-family: Georgia, serif;
    font-size: 9pt;
    color: #555;
  }
}
@page :right { margin-left: 0.875in; margin-right: 0.5in; }
@page :left  { margin-left: 0.5in;   margin-right: 0.875in; }
@page :first { @bottom-center { content: none; } }

html { font-family: Georgia, "Times New Roman", serif; font-size: 11pt; color: #111; }
body { line-height: 1.38; text-align: justify; hyphens: auto;
       -webkit-hyphens: auto; widows: 3; orphans: 3;
       font-kerning: normal; font-variant-ligatures: common-ligatures; }

h1 {
  break-before: right;
  page-break-before: right;
  break-after: avoid;
  page-break-after: avoid;
  font-size: 26pt;
  font-weight: 700;
  text-align: center;
  margin: 1in 0 0.5in 0;
  line-height: 1.15;
  letter-spacing: -0.02em;
}
h1:first-of-type { page-break-before: avoid; break-before: avoid; margin-top: 1.25in; }
h2 { page-break-after: avoid; break-after: avoid; font-size: 14pt; font-weight: 700;
     margin-top: 1.5em; margin-bottom: 0.5em; letter-spacing: -0.01em; }
h2 + p { break-after: avoid; page-break-after: avoid; }
h2 + p + figure, h2 + p + p, h2 + p + p > img { break-before: avoid; page-break-before: avoid; }
h3 { page-break-after: avoid; break-after: avoid; font-size: 12pt; font-weight: 700;
     margin-top: 1em; margin-bottom: 0.25em; }
h4 { page-break-after: avoid; break-after: avoid; font-size: 11pt; font-weight: 600;
     font-style: italic; margin-top: 0.75em; margin-bottom: 0.25em; }

p { margin: 0 0 0.25em 0; text-indent: 1.2em; }
h1 + p, h2 + p, h3 + p, h4 + p, blockquote + p { text-indent: 0; }
h1 + p:first-of-type { text-indent: 0; }
p > em:only-child { text-indent: 0; }
p:has(> em:only-child) { text-indent: 0; font-size: 9.5pt; color: #555; margin-top: 0.25em; }

ul, ol { margin: 0.5em 0 0.75em 1.5em; }
li { margin-bottom: 0.2em; page-break-inside: avoid; break-inside: avoid; }

img { max-width: 100%; height: auto; display: block; margin: 1em auto;
      page-break-inside: avoid; break-inside: avoid; }
h1 + p > img:only-child,
h1 + figure img { max-width: 3.5in; margin: 0.25in auto 0.5em auto; }

figure { page-break-inside: avoid; break-inside: avoid;
         margin: 0.25in auto; text-align: center; }
figure figcaption { font-size: 9.5pt; color: #444; margin-top: 0.25em;
                    font-style: italic; page-break-before: avoid; break-before: avoid; }
h1 + figure { page-break-before: avoid; break-before: avoid; }

blockquote { margin: 1em 1.5em; padding-left: 1em; border-left: 2pt solid #888;
             font-style: italic; color: #333; page-break-inside: avoid;
             break-inside: avoid; }

table { border-collapse: collapse; margin: 1em auto; page-break-inside: avoid;
        break-inside: avoid; font-size: 10pt; }
th, td { padding: 4pt 8pt; border-bottom: 0.5pt solid #ccc; text-align: left;
         vertical-align: top; }
th { font-weight: 700; border-bottom: 1pt solid #333; }

#TOC { page-break-before: right; page-break-after: right; }
#TOC h1, #TOC h2 { page-break-before: avoid; }
#TOC ul { list-style: none; margin-left: 0; }
#TOC li { margin: 0.15em 0; }
#TOC a { text-decoration: none; color: inherit; }

code, pre { font-family: "Courier New", Courier, monospace; font-size: 10pt; }
pre { background: #f4f4f4; padding: 0.75em; overflow-x: auto; page-break-inside: avoid; }

hr { border: none; text-align: center; margin: 1.5em 0; }
hr::after { content: "· · ·"; letter-spacing: 0.5em; color: #888; }

a, a:link, a:visited, a:hover, a:active {
  color: #111 !important;
  text-decoration: none !important;
  font-weight: inherit !important;
  border-bottom: 0 !important;
  background: none !important;
}
@media print {
  a, a:link, a:visited { color: #000 !important; text-decoration: none !important; }
}

h1, h2, h3, h4, h5, h6 { break-inside: avoid; page-break-inside: avoid; }
h2 + p, h3 + p, h4 + p { page-break-before: avoid; break-before: avoid; }

h1 + p img, h1 + p + p img { max-width: 4.25in; margin: 0.4in auto 0.6em auto; }
h1 + p:has(img) { text-align: center; }
p:has(img) { text-indent: 0; text-align: center; margin: 0.5em 0; }
p:has(img) + p em { font-size: 9.5pt; color: #444; }

h1 + p { text-indent: 0; }

#TOC { page-break-before: right; }
#TOC h1 { margin-top: 1.5in; margin-bottom: 0.75in; }
#TOC > ul { font-size: 11pt; line-height: 1.9; list-style: none; margin-left: 0; padding-left: 0; }
#TOC > ul > li { list-style: none; margin: 0 0 4pt 0; padding: 0; }
/* The <a> is a flex container with three items:
     1. Chapter-title text (flex: 0 1 auto)
     2. ::before dotted leader (order: 2, flex: 1 1 auto)
     3. ::after page number (order: 3, flex: 0 0 auto)
   This is the only layout that gives WeasyPrint a right-aligned page
   number with proper dot leaders between title and number. */
#TOC > ul > li > a {
  display: flex;
  align-items: flex-end;
  text-decoration: none;
  border-bottom: none;
  color: inherit;
}
#TOC > ul > li > a::before {
  content: "";
  order: 2;
  flex: 1 1 auto;
  margin: 0 0.35em 0.32em;
  border-bottom: 0.5pt dotted #777;
  min-width: 1em;
  align-self: flex-end;
}
#TOC > ul > li > a::after {
  content: target-counter(attr(href), page);
  order: 3;
  flex: 0 0 auto;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}
@supports not (content: target-counter(attr(href), page)) {
  #TOC > ul > li > a::after { content: ""; }
}

p, li { widows: 2; orphans: 2; }
em, i { font-style: italic; }
strong, b { font-weight: 700; }
"""


def build_html(md: str) -> Path:
    MANUSCRIPT_MD.write_text(md)
    PRINT_CSS_FILE.write_text(PRINT_CSS)

    title = CONFIG.get("title", "Turkey Tourist Scams 2026")
    author = CONFIG.get("author", "The Tabiji Team")

    cmd = [
        "pandoc",
        str(MANUSCRIPT_MD),
        "-o", str(INTERIOR_HTML),
        "--standalone",
        "--embed-resources",
        "--toc",
        "--toc-depth=1",
        "--metadata", "toc-title=Contents",
        "--css", str(PRINT_CSS_FILE),
        "--metadata", f"title={title}",
        "--metadata", f"author={author}",
        "--resource-path", str(BOOK),
        "--from", "markdown+smart",
    ]
    subprocess.run(cmd, check=True)
    return INTERIOR_HTML


def build_pdf_direct(md_path: Path) -> Path:
    """Build PDF directly from markdown using pandoc with a LaTeX engine.
    This is the primary path — produces proper TOC with page numbers."""
    from shutil import which

    engine = None
    for eng in ("xelatex", "lualatex", "pdflatex"):
        if which(eng):
            engine = eng
            break

    if engine:
        title = CONFIG.get("title", "Turkey Tourist Scams 2026")
        author = CONFIG.get("author", "The Tabiji Team")

        header_tex = BOOK / "templates" / "header-includes.tex"
        cmd = [
            "pandoc",
            str(md_path),
            "-o", str(INTERIOR_PDF),
            f"--pdf-engine={engine}",
            "--toc",
            "--toc-depth=1",
            "-V", "geometry:paperwidth=6in",
            "-V", "geometry:paperheight=9in",
            # KDP-compliant twoside geometry for 6"×9" trim.
            # For 151-400 pages, KDP requires ≥0.625" gutter (inside);
            # outside/top/bottom need only ≥0.25". We use:
            #   inside (gutter) = 0.875"  — comfortable above KDP 0.625" min
            #   outside         = 0.5"    — 2x KDP 0.25" min, keeps line lengths comfortable
            #   top             = 0.75"   — room for running head
            #   bottom          = 0.75"   — room for page number
            # Text block width: 6 - 0.875 - 0.5 = 4.625" at 11pt ≈ ~62 chars,
            # which is in the 60-75 char optimal readability range.
            "-V", "geometry:inner=0.875in",
            "-V", "geometry:outer=0.5in",
            "-V", "geometry:top=0.75in",
            "-V", "geometry:bottom=0.75in",
            "-V", "classoption=twoside",
            "-V", "documentclass=book",
            "-V", f"title={title}",
            "-V", f"author={author}",
            "-V", "fontsize=11pt",
            # Arial Unicode MS covers Latin + Spanish accents cleanly and
            # matches the Thailand volume's font choice for series consistency.
            "-V", "mainfont=Arial Unicode MS",
            "--resource-path", str(BOOK),
        ]
        # Inject the header fixes (running-head reset for unnumbered chapters,
        # long-heading protection) if the template file exists.
        if header_tex.exists():
            cmd.extend(["-H", str(header_tex)])
        subprocess.run(cmd, check=True)
    else:
        # Fall back to Chrome headless (TOC will render but without page numbers)
        print("Warning: No LaTeX engine found. TOC will not have page numbers.")
        html = build_html(MANUSCRIPT_MD.read_text())
        cmd = [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--disable-extensions",
            "--virtual-time-budget=10000",
            f"--print-to-pdf={INTERIOR_PDF}",
            f"file://{html.resolve()}",
        ]
        subprocess.run(cmd, check=True, capture_output=True)
    return INTERIOR_PDF


def page_count(pdf: Path) -> int | None:
    try:
        r = subprocess.run(
            ["/opt/homebrew/bin/pdfinfo", str(pdf)],
            capture_output=True, text=True, check=True,
        )
        for line in r.stdout.splitlines():
            if line.startswith("Pages:"):
                return int(line.split()[-1])
    except Exception:
        return None
    return None


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    md = assemble_markdown()
    print(f"Markdown assembled: {len(md):,} chars")

    MANUSCRIPT_MD.write_text(md)
    pdf = build_pdf_direct(MANUSCRIPT_MD)
    kb = pdf.stat().st_size / 1024
    pages = page_count(pdf)
    print(f"PDF built: {pdf.name} ({kb:.0f} KB{f', {pages} pages' if pages else ''})")


if __name__ == "__main__":
    main()
