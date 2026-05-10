#!/usr/bin/env python3
"""
Build the paperback-interior PDF for Travel Scams for Seniors.

Pipeline:
  manuscript-with-images.md (from build.py)
    → standalone HTML (pandoc)
    → print-CSS applied (KDP 6x9)
    → paperback PDF (WeasyPrint, with running page numbers)

Usage:
    python3 book-travel-scams-seniors/scripts/build_paperback_interior.py

Prerequisites:
    pandoc, WeasyPrint (homebrew Python 3.14)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
BUILD = BOOK / "build"
BUILD.mkdir(parents=True, exist_ok=True)

CONFIG = yaml.safe_load((BOOK / "config.yaml").read_text())
OUT_BASE = CONFIG.get("output_filename", "book")

ASSEMBLED_MD = BUILD / "manuscript-with-images.md"
INTERIOR_HTML = BUILD / f"{OUT_BASE}-paperback-interior.html"
INTERIOR_PDF = BUILD / f"{OUT_BASE}-paperback-interior.pdf"
PRINT_CSS_FILE = BUILD / "paperback-print.css"


# ---------------------------------------------------------------------------
# Print CSS — KDP 6x9 trim, professional paperback typography.
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
body { line-height: 1.42; text-align: justify; hyphens: auto;
       -webkit-hyphens: auto; widows: 3; orphans: 3;
       font-kerning: normal; font-variant-ligatures: common-ligatures; }

/* The book uses # for parts/conclusion/appendices and ## for chapters. We
   want chapters to break onto a new right-hand page, like trade nonfiction.
   Treat both h1 (parts) and h2 (chapters) as forced-page-break headings. */
h1 {
  break-before: right;
  page-break-before: right;
  break-after: avoid;
  page-break-after: avoid;
  font-size: 28pt;
  font-weight: 700;
  text-align: center;
  margin: 1.25in 0 0.5in 0;
  line-height: 1.15;
  letter-spacing: -0.02em;
}
h1:first-of-type { page-break-before: avoid; break-before: avoid; margin-top: 1.25in; }

h2 {
  break-before: right;
  page-break-before: right;
  break-after: avoid;
  page-break-after: avoid;
  font-size: 22pt;
  font-weight: 700;
  text-align: center;
  margin: 1in 0 0.4in 0;
  line-height: 1.18;
  letter-spacing: -0.01em;
}
h2 + p { break-after: avoid; page-break-after: avoid; text-indent: 0; }

h3 {
  page-break-after: avoid; break-after: avoid;
  font-size: 13pt; font-weight: 700;
  margin-top: 1.4em; margin-bottom: 0.3em;
  letter-spacing: -0.005em;
}
h3 + p { break-after: avoid; page-break-after: avoid; text-indent: 0; }

h4 {
  page-break-after: avoid; break-after: avoid;
  font-size: 11pt; font-weight: 600; font-style: italic;
  margin-top: 0.85em; margin-bottom: 0.25em;
}
h4 + p { text-indent: 0; }

p { margin: 0 0 0.25em 0; text-indent: 1.2em; }
h1 + p, h2 + p, h3 + p, h4 + p, blockquote + p { text-indent: 0; }
p > em:only-child { text-indent: 0; }

ul, ol { margin: 0.5em 0 0.75em 1.5em; }
li { margin-bottom: 0.18em; page-break-inside: avoid; break-inside: avoid; }

/* Chapter scene illustrations — full-width landscape, soft border */
img {
  max-width: 100%; height: auto; display: block;
  margin: 1em auto;
  page-break-inside: avoid; break-inside: avoid;
}

/* Quick Take / Red Flags / Scripts / Checklist boxed callouts.
   The manuscript uses blockquotes with bold labels for these. */
blockquote {
  background: #f5f1e8;
  border-left: 3pt solid #1c264e;
  padding: 0.55em 0.85em 0.55em 1em;
  margin: 0.9em 0.25in 1em 0.25in;
  font-style: normal;
  color: #1c1c1c;
  page-break-inside: avoid;
  break-inside: avoid;
}
blockquote strong:first-child { color: #1c264e; letter-spacing: 0.03em; text-transform: uppercase; font-size: 9.5pt; }
blockquote p { text-indent: 0; margin: 0.18em 0; }
blockquote ul, blockquote ol { margin: 0.3em 0 0.3em 1.2em; }

/* Footnotes — superscript markers, end-of-book by default in pandoc */
sup { font-size: 0.72em; vertical-align: super; line-height: 0; }
.footnotes { font-size: 9.5pt; line-height: 1.30; margin-top: 1.5em;
             border-top: 1pt solid #aaa; padding-top: 0.75em; color: #333; }
.footnotes p { text-indent: 0; }

/* Horizontal rules — soft chapter breaks where present */
hr { border: 0; border-top: 1pt solid #c8c4b6; margin: 1.5em auto; width: 60%; }

/* Author byline / dedication / first-page treatment */
.title { font-size: 32pt; font-weight: 700; text-align: center;
         margin-top: 2.5in; letter-spacing: -0.02em; }
.subtitle { font-size: 13pt; font-style: italic; text-align: center;
            color: #444; margin-top: 0.4in; }
.author { font-size: 14pt; text-align: center;
          margin-top: 1in; letter-spacing: 0.04em; text-transform: uppercase; }

/* TOC — pandoc emits a definition-list-like structure */
nav#TOC ul { list-style: none; margin: 0; padding: 0; }
nav#TOC li { margin: 0.3em 0; }
nav#TOC a { text-decoration: none; color: #111; }
"""


def assemble_html(md_path: Path) -> Path:
    if not md_path.exists():
        sys.exit(f"missing assembled markdown at {md_path}; run build.py first")

    cmd = [
        "pandoc",
        "--from=markdown+footnotes+pipe_tables+task_lists",
        "--to=html5",
        "--standalone",
        f"--metadata=title={CONFIG['title']}",
        f"--metadata=author={CONFIG['author']}",
        "--toc",
        "--toc-depth=2",
        "--resource-path", str(BOOK),
        f"--output={INTERIOR_HTML}",
        str(md_path),
    ]
    print(f"[paperback-interior] pandoc → {INTERIOR_HTML.name}")
    subprocess.run(cmd, check=True)
    return INTERIOR_HTML


def build_pdf(html_path: Path) -> Path:
    PRINT_CSS_FILE.write_text(PRINT_CSS)
    print(f"[paperback-interior] WeasyPrint → {INTERIOR_PDF.name}")
    from weasyprint import HTML, CSS  # type: ignore
    HTML(filename=str(html_path), base_url=str(BOOK)).write_pdf(
        target=str(INTERIOR_PDF),
        stylesheets=[CSS(filename=str(PRINT_CSS_FILE))],
    )
    return INTERIOR_PDF


def main() -> None:
    html = assemble_html(ASSEMBLED_MD)
    pdf = build_pdf(html)
    print(f"[paperback-interior] DONE → {pdf}")


if __name__ == "__main__":
    main()
