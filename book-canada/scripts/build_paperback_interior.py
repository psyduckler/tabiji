#!/usr/bin/env python3
"""
Build the paperback-interior PDF for the Indonesia book (V6).

Pipeline:
  markdown (via assemble_markdown from build.py)
    → standalone HTML (pandoc, with embedded images)
    → print-CSS applied
    → paperback PDF (WeasyPrint, respecting @page rules + target-counter())

Target: 6"x9" trim, KDP-compliant inside/outside margins, running page numbers,
chapter breaks on new pages, widow/orphan control, image containment,
**TOC with real page numbers via CSS Paged Media target-counter()**.

V6 note: we moved off Chrome headless because Chrome doesn't implement
target-counter() — so the TOC dotted leaders had no page numbers. WeasyPrint
fully implements CSS Paged Media and renders the same HTML/CSS with proper
leaders. Fallback to Chrome only if WeasyPrint isn't importable.

Usage:
    python3 book-canada/scripts/build_paperback_interior.py

Prerequisites:
    - pandoc (brew install pandoc)
    - WeasyPrint (pip install weasyprint; depends on Homebrew pango/cairo)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
BUILD = BOOK / "build"

# Reuse the canonical markdown assembler from build.py so the paperback
# interior and the EPUB always derive from the same source text.
sys.path.insert(0, str(BOOK))
from build import assemble_markdown, CONFIG  # noqa: E402

INTERIOR_HTML = BUILD / "canada-scams-paperback.html"
INTERIOR_PDF = BUILD / "canada-scams-paperback.pdf"
MANUSCRIPT_MD = BUILD / "paperback-manuscript.md"
PRINT_CSS_FILE = BUILD / "paperback-print.css"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


# ---------------------------------------------------------------------------
# Print CSS — KDP 6"x9" trim with professional paperback typography.
# ---------------------------------------------------------------------------
PRINT_CSS = r"""
/* ===== @page: KDP 6"x9" trim with asymmetric inside/outside margins ===== */
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

/* ===== Body typography ===== */
html { font-family: Georgia, "Times New Roman", serif; font-size: 11pt; color: #111; }
body { line-height: 1.38; text-align: justify; hyphens: auto;
       -webkit-hyphens: auto; widows: 3; orphans: 3;
       font-kerning: normal; font-variant-ligatures: common-ligatures; }

/* ===== Headings ===== */
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

/* ===== Paragraphs ===== */
p { margin: 0 0 0.25em 0; text-indent: 1.2em; }
h1 + p, h2 + p, h3 + p, h4 + p, blockquote + p { text-indent: 0; }
h1 + p:first-of-type { text-indent: 0; }
p > em:only-child { text-indent: 0; }

/* ===== Lists ===== */
ul, ol { margin: 0.5em 0 0.75em 1.5em; }
li { margin-bottom: 0.2em; page-break-inside: avoid; break-inside: avoid; }

/* ===== Images ===== */
img { max-width: 100%; height: auto; display: block; margin: 1em auto;
      page-break-inside: avoid; break-inside: avoid; }
h1 + p > img:only-child,
h1 + figure img { max-width: 3.5in; margin: 0.25in auto 0.5em auto; }

figure { page-break-inside: avoid; break-inside: avoid;
         margin: 0.25in auto; text-align: center; }
figure figcaption { font-size: 9.5pt; color: #444; margin-top: 0.25em;
                    font-style: italic; page-break-before: avoid; break-before: avoid; }
h1 + figure { page-break-before: avoid; break-before: avoid; }

/* ===== Blockquotes / sidebars ===== */
blockquote { margin: 1em 1.5em; padding-left: 1em; border-left: 2pt solid #888;
             font-style: italic; color: #333; page-break-inside: avoid;
             break-inside: avoid; }

/* ===== Tables ===== */
table { border-collapse: collapse; margin: 1em auto; page-break-inside: avoid;
        break-inside: avoid; font-size: 10pt; }
th, td { padding: 4pt 8pt; border-bottom: 0.5pt solid #ccc; text-align: left;
         vertical-align: top; }
th { font-weight: 700; border-bottom: 1pt solid #333; }

/* ===== TOC ===== */
#TOC { page-break-before: right; page-break-after: right; }
#TOC h1, #TOC h2 { page-break-before: avoid; }
#TOC ul { list-style: none; margin-left: 0; }
#TOC li { margin: 0.15em 0; }
#TOC a { text-decoration: none; color: inherit; }

/* ===== Code / monospace ===== */
code, pre { font-family: "Courier New", Courier, monospace; font-size: 10pt; }
pre { background: #f4f4f4; padding: 0.75em; overflow-x: auto; page-break-inside: avoid; }

/* ===== Horizontal rule (scene / pattern break) ===== */
hr { border: none; text-align: center; margin: 1.5em 0; }
hr::after { content: "· · ·"; letter-spacing: 0.5em; color: #888; }

/* ===== Links — print style (black, not underlined) ===== */
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

/* ===== Prevent awkward page breaks ===== */
h1, h2, h3, h4, h5, h6 { break-inside: avoid; page-break-inside: avoid; }
h2 + p, h3 + p, h4 + p { page-break-before: avoid; break-before: avoid; }

/* ===== Chapter-opening images ===== */
h1 + p img, h1 + p + p img { max-width: 4.25in; margin: 0.4in auto 0.6em auto; }
h1 + p:has(img) { text-align: center; }
p:has(img) { text-indent: 0; text-align: center; margin: 0.5em 0; }
p:has(img) + p em { font-size: 9.5pt; color: #444; }

h1 + p { text-indent: 0; }

/* ===== TOC refinements — target-counter(attr(href), page) is the key line here ===== */
#TOC { page-break-before: right; }
#TOC h1 { margin-top: 1.5in; margin-bottom: 0.75in; }
#TOC > ul { font-size: 11pt; line-height: 1.9; list-style: none; margin-left: 0; padding-left: 0; }
#TOC > ul > li { list-style: none; margin-left: 0;
                 border-bottom: 0.3pt dotted #aaa;
                 padding-bottom: 2pt; margin-bottom: 4pt;
                 display: flex; justify-content: space-between; align-items: baseline; }
#TOC > ul > li > a { border-bottom: 0; padding-right: 0.6em; background: #fff;
                     flex: 1; }
#TOC > ul > li > a::after {
  content: target-counter(attr(href), page);
  background: #fff; padding-left: 0.3em;
  font-variant-numeric: tabular-nums;
  margin-left: auto;
}

/* ===== Widows/orphans ===== */
p, li { widows: 2; orphans: 2; }

/* ===== Emphasis ===== */
em, i { font-style: italic; }
strong, b { font-weight: 700; }
"""


def build_html(md: str) -> Path:
    MANUSCRIPT_MD.write_text(md)
    PRINT_CSS_FILE.write_text(PRINT_CSS)

    title = CONFIG.get("title", "Canada Tourist Scams 2026")
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


def html_to_pdf(html: Path) -> Path:
    """Render HTML to PDF via WeasyPrint.

    WeasyPrint implements CSS Paged Media target-counter() properly, which is
    why we use it instead of Chrome headless — the TOC actually gets page
    numbers. If the weasyprint import fails (missing brew pango / cairo), we
    fall back to Chrome with a loud warning."""
    try:
        # Make sure Homebrew libs are findable for pango/cairo/gobject
        os.environ.setdefault("DYLD_FALLBACK_LIBRARY_PATH", "/opt/homebrew/lib")
        from weasyprint import HTML as WP_HTML
        WP_HTML(filename=str(html)).write_pdf(str(INTERIOR_PDF))
        return INTERIOR_PDF
    except ImportError as e:
        print(f"Warning: WeasyPrint unavailable ({e}); falling back to Chrome (TOC page numbers will be empty).")

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

    html = build_html(md)
    kb = html.stat().st_size / 1024
    print(f"HTML built: {html.name} ({kb:.0f} KB)")

    pdf = html_to_pdf(html)
    kb = pdf.stat().st_size / 1024
    pages = page_count(pdf)
    print(f"PDF built: {pdf.name} ({kb:.0f} KB{f', {pages} pages' if pages else ''})")


if __name__ == "__main__":
    main()
