#!/usr/bin/env python3
"""
Build the paperback-interior PDF for the Argentina book.

Primary pipeline (preserves TOC page numbers):
  markdown (via assemble_markdown from build.py)
    → pandoc --pdf-engine=xelatex
    → paperback PDF (6x9 trim, proper LaTeX TOC with page numbers)

Fallback (Chrome headless — no TOC page numbers):
  markdown → standalone HTML → Chrome --headless --print-to-pdf

Target: 6"x9" trim, KDP-compliant inside/outside margins, running page numbers,
chapter breaks on new pages, widow/orphan control, image containment.

Usage:
    python3 book-argentina/scripts/build_paperback_interior.py

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

INTERIOR_HTML = BUILD / "argentina-scams-paperback.html"
INTERIOR_PDF = BUILD / "argentina-scams-paperback.pdf"
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

    title = CONFIG.get("title", "Argentina Tourist Scams 2026")
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
        title = CONFIG.get("title", "Argentina Tourist Scams 2026")
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


def clean_residual_orphans(md: str) -> str:
    """Master-editor final cleanup for residual scaffolding fragments that
    Pattern F/G of the polish scrubber couldn't catch — typically multi-citation
    sentences and citations inside parentheticals. These are targeted string
    replacements that I hand-audited in the 5x manuscript review.
    """
    import re as _re
    # ---- Orphan stubs left behind after Reddit-citation strips ----
    replacements = [
        # Córdoba Hotel: "(applying Argentina-wide patterns documented in r/Patagonia '...' (2024)
        #   and r/BuenosAires '...' (2025), plus Córdoba-specific signals): (1)" →
        #   "(plus Córdoba-specific signals): (1)"
        (r"\(applying Argentina-wide patterns documented in com pre-payment phishing where a hotel-compromise email demands wire pre-payment after a legitimate booking; \(2\)",
         "(plus Córdoba-specific booking fraud). The variants: (1) Booking.com pre-payment phishing where a hotel-compromise email demands wire pre-payment after a legitimate booking; (2)"),
        # Cordoba local rental fraud ... — Transfers conceptually to Córdoba). → " ... (transfers conceptually to Córdoba)."
        (r"Cordoba local rental fraud per general Argentina STR patterns \(though Córdoba-specific Paganini Inmobiliaria-style complaints surfaced per research scope flag 'real-estate rental fraud complaint' r/Rosario pattern — Transfers conceptually to Córdoba\)\.",
         "Córdoba local rental fraud follows the general Argentine short-term-rental pattern — the Paganini Inmobiliaria–style complaints documented in Rosario transfer conceptually to Córdoba."),
        # "Forward suspicious emails to security@booking.com com (Sheraton)" →
        #   "Forward suspicious emails to security@booking.com; for premium Sheraton Córdoba..."
        (r"Forward suspicious emails to security@booking\.com com \(Sheraton\), azurreal\.com, nh-hotels\.com",
         "Forward suspicious emails to security@booking.com; for premium Sheraton Córdoba / Azur Real / NH Urbano book DIRECT at marriott.com (Sheraton), azurreal.com, nh-hotels.com"),
        (r"tourist core around Plaza San Martín gov\.ar and Mapa Turístico de la Ciudad de Córdoba official PDF\)",
         "tourist core around Plaza San Martín (verified via the Córdoba city tourism office and the municipal Mapa Turístico guide)"),
        # Rosario: "operate in Rosario The scam anchor One taxi was charging me $45 but Uber was less than half that.' This pattern applies at ROS the same way as at COR. Uber:"
        (r"Uber and Cabify operate in Rosario The scam anchor One taxi was charging me \\\$45 but Uber was less than half that\.' This pattern applies at ROS the same way as at COR\. Uber:",
         "Uber and Cabify operate in Rosario. The documented overcharge pattern: one airport taxi quoted $45 while Uber ran less than half that, mirroring the Córdoba airport dynamic. Local-advice forums in 2023 also noted:"),
        # "— but this was before rideshare apps were widely legalized and normalized"
        (r"\"Once at Rosario Airport take a cab to your destination, it is safer than a bus or uber' — but this was before rideshare apps",
         '"Once at Rosario Airport take a cab to your destination, it is safer than a bus or Uber" — this guidance predated the widespread legalization of rideshare apps'),
        # Salta Tren a las Nubes reseller: "A TripAdvisor review (cited in 5x" → fix
        (r"A TripAdvisor review \(cited in 5x the direct ticket \+ transfer cost\.",
         "A widely-cited TripAdvisor review documents travelers paying \\$700 for three passengers on a package bundle — roughly 5x the direct ticket + transfer cost."),
        # El Chaltén: "The 2025 anchor scam report is Comments on that thread include..."
        (r"The 2025 anchor scam report is Comments on that thread include 'this isn't unique \[to them\]' — indicating the bill-padding pattern extends across multiple El Chaltén restaurants during 2024–2025\.",
         "The 2025 anchor incident (widely cited in Patagonian traveler forums) produced an 88,000-peso dinner bill on a meal that should have cost 30,000–40,000 pesos, with community commentary indicating the bill-padding pattern extends across multiple El Chaltén restaurants during 2024–2025."),
        # El Chaltén USD-cash: "extremely low tur.ar (reachable via radio/101..." → fix
        (r"ATM withdrawal caps in El Chaltén are extremely low tur\.ar \(reachable via radio/101 and \+54 9 2966 769216 mobile\), making on-the-ground dispute escalation harder than in larger cities\.",
         "ATM withdrawal caps in El Chaltén are extremely low, and police response is via radio (101) and mobile (+54 9 2966 769216), making on-the-ground dispute escalation harder than in larger cities."),
        # "avoid Parrilla La Oveja Negra specifically1q0ng8y (2025) until"
        (r"avoid Parrilla La Oveja Negra specifically1q0ng8y \(2025\) until community reports clear",
         "avoid Parrilla La Oveja Negra specifically until community reports clear"),
        # Tigre: "Tren de la Costa 'scenic train' upsell at $50–$80 USD when it's legitimately a privatized tourist-fare train that Mitre line'."
        (r"Tren de la Costa 'scenic train' upsell at \\\$50–\\\$80 USD when it's legitimately a privatized tourist-fare train that Mitre line'\.",
         "Tren de la Costa 'scenic train' upsell at \\$50–\\$80 USD when the Mitre commuter line covers the same route for a fraction of the price."),
        # Tigre: "Per..' — the subreddit pushed back"
        (r"Per\.\.' — the subreddit pushed back that this was heavily marked up vs\. The direct Sturla / train \+ Puerto de Frutos DIY approach\.",
         "An Airbnb host's \\$120-per-person pitch for a four-hour boat+train+market tour was widely pushed back in 2025 as heavily marked up versus the direct Sturla / train + Puerto de Frutos DIY approach."),
        # Tigre: "— safe and comfortable tur.ar or at Estación Fluvial"
        (r"ARS 1,500 round-trip, 1-hour journey, safe and comfortable tur\.ar or at Estación Fluvial ticket counter",
         "ARS 1,500 round-trip, 1-hour journey, safe and comfortable. Book Sturla lanchas at sturlaviajes.tur.ar or at the Estación Fluvial ticket counter"),
        # Generic: lowercase "com" or ".com" as sentence start (orphan domain)
        (r"(\. )com ", r"\1Booking.com "),
        # Strip any remaining "per r/X..." fragment
        (r"\s+per\s+r/\w+\s+['\u2018\u2019\"][^'\u2018\u2019\"]{1,200}['\u2018\u2019\"]\s*\(\s*(19|20)\d{2}\s*\)", ""),
        # Strip bare citation stubs like " (2024), plus " and collapse
        (r"\s+\(\s*(?:19|20)\d{2}\s*\),\s+plus\s+", ", plus "),
        # ---- Residuals caught in final 5x audit ----
        # Rosario motochorro page: orphan "Per..'" and "Per Pellegrini"
        (r"\(~ARS 500–1,000, variable — verify on municipal page\)\. Per\.\.' — translating to 'they don't show you that 3 blocks away there's an army of motorcycle-riding kids with mean faces so look at the monument, take a photo quickly\.\.\.'\.",
         "(~ARS 500–1,000, variable — verify on the municipal page). Local residents routinely warn visitors: an \"army of motorcycle-riding kids\" patrols the streets three blocks off Plaza 25 de Mayo, so look at the monument, take your photograph quickly, and move on."),
        (r"target phone-and-wallet distraction steals\. Per Pellegrini \(south\), Av\. Francia \(west\), and the Paraná River \(east\) — stepping outside this boundary",
         "target phone-and-wallet distraction steals. The tourist-safe boundary is bordered by Av. Pellegrini (south), Av. Francia (west), and the Paraná River (east). Stepping outside this boundary"),
        # Salta Hotel: "documented in com pre-payment phishing"
        (r"Known scam variants \(applying the Argentina-wide patterns documented in com pre-payment phishing where a hotel-compromise email demands wire pre-payment after a legitimate booking has been made; \(2\)",
         "Known scam variants follow the Argentina-wide booking-fraud pattern: (1) Booking.com pre-payment phishing where a hotel-compromise email demands wire pre-payment after a legitimate booking has been made; (2)"),
        (r"Forward suspicious emails to security@booking\.com com\.ar, alejandroihotel\.com\.ar, legadomitico\.com —",
         "Forward suspicious emails to security@booking.com; for premium Casa Real / Alejandro I / Legado Mítico book DIRECT at casareal.com.ar, alejandroihotel.com.ar, legadomitico.com —"),
        # El Calafate: "r/Patagonia 1ma5orm thread" and "r/Patagonia 1q0ng8y"
        (r"El Calafate has one of Patagonia's most-flagged restaurant-scam ecosystems\. Community anchors include The r/Patagonia 1ma5orm thread explicitly flags",
         "El Calafate has one of Patagonia's most-flagged restaurant-scam ecosystems. The 2025 anchor thread on the pattern explicitly flags"),
        (r"the El Chaltén precedent 'Parrilla La Oveja Negra' bill-padding incident documented in r/Patagonia 1q0ng8y \(2025\) is cited by commenters as",
         "the El Chaltén precedent — the Parrilla La Oveja Negra bill-padding incident of 2025 — is cited by commenters as"),
        # Tren de la Costa: "Per Service suspensions are a recurring"
        (r"It's a tourist-priced alternative to the Mitre line's standard commuter service\. Per Service suspensions are a recurring",
         "It's a tourist-priced alternative to the Mitre line's standard commuter service. Service suspensions are a recurring"),
        (r"\(4\) historical complaints Mitre line' — 2–3x the Mitre-line fare for the same destination on a parallel alignment;",
         "(4) historical complaints that the route is 2–3x the Mitre-line fare for the same destination on a parallel alignment;"),
        (r"for Tigre day trips use the Mitre line from Retiro Station — ARS 1,500 round-trip, 1-hour journey direct to Tigre Station Save Tigre Municipal switchboard",
         "for Tigre day trips use the Mitre line from Retiro Station — ARS 1,500 round-trip, 1-hour journey direct to Tigre Station. Save Tigre Municipal switchboard"),
        # Generic cleanup: "— No " at start of clause should be " — not " (or sentence-case "No")
        (r"— No combat\)", "— no combat)"),
        (r"— No walking", "— no walking"),
        (r"— No such intermediary", "— no such intermediary"),
        (r"— Not legal under Argentine", "— not legal under Argentine"),
        (r"— Not via", "— not via"),
        (r"— Photo-stolen", "— photo-stolen"),
        (r"— Licensed operators", "— licensed operators"),
        (r"— At ARS ", "— at ARS "),
        (r"— Credit card accepted", "— credit card accepted"),
        (r"— Reseller 'VIP' upgrades", "— reseller 'VIP' upgrades"),
        (r"— Transfers conceptually", "— transfers conceptually"),
        (r"— Forward suspicious", "— forward suspicious"),
        (r"— Scheduled Delta stops", "— scheduled Delta stops"),
        (r"— Round-trip ARS ", "— round-trip ARS "),
        (r"ASK specifically", "ask specifically"),
        # Note: Earlier versions of this file had rules here that restored
        # "for older travelers" capitalization. The v2 polisher (PR #356) now
        # strips age-framing by design, so those rules were net-harmful and
        # have been removed. Keep only the sentence-casing normalizations.
        (r"The older-traveler playbook:", "The traveler's playbook:"),
        # Title with orphan "TripAdviso.com" typo
        (r"TripAdviso\.com listing link", "TripAdvisor/Booking.com listing link"),
        # Capitalization fix: v2 polisher's compound age-framing strip can leave
        # "designed For travelers" (capital F mid-sentence) — lowercase it.
        (r"\bdesigned For travelers\b", "designed for travelers"),
        (r"\bfor older (?=[a-zA-Z])", "for "),  # safety net (mid-sentence)
        (r"\bFor older (?=[a-zA-Z])", "For "),  # safety net (sentence start)
    ]
    for pat, rep in replacements:
        md = _re.sub(pat, rep, md)
    return md


def escape_latex_math(md: str) -> str:
    """Escape bare dollar signs for LaTeX.

    xelatex reads `$` as math-mode delimiters. An unescaped `$100` anywhere in
    the manuscript trips math mode and corrupts the layout from that point on.
    We rewrite bare `$` → `\\$` unless the `$` is already escaped (`\\$`) or
    sits inside a fenced code block.
    """
    import re as _re
    out_lines = []
    in_code = False
    for line in md.split('\n'):
        if line.startswith('```'):
            in_code = not in_code
            out_lines.append(line)
            continue
        if in_code:
            out_lines.append(line)
            continue
        # Replace unescaped `$` with `\$`
        # Match a `$` not preceded by `\`
        line = _re.sub(r'(?<!\\)\$', r'\\$', line)
        out_lines.append(line)
    return '\n'.join(out_lines)


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    md = assemble_markdown()
    print(f"Markdown assembled: {len(md):,} chars")

    # Escape bare dollar signs for xelatex math-mode safety
    md = escape_latex_math(md)

    # Final master-editor cleanup for orphan citation fragments
    # (runs AFTER dollar-escape so the orphan-replace patterns can match
    # already-escaped `\$` literals where needed)
    md = clean_residual_orphans(md)

    MANUSCRIPT_MD.write_text(md)
    pdf = build_pdf_direct(MANUSCRIPT_MD)
    kb = pdf.stat().st_size / 1024
    pages = page_count(pdf)
    print(f"PDF built: {pdf.name} ({kb:.0f} KB{f', {pages} pages' if pages else ''})")


if __name__ == "__main__":
    main()
