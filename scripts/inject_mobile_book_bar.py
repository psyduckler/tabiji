#!/usr/bin/env python3
"""Inject a mobile-only sticky bottom book-CTA bar into every scams/<slug>/index.html.

The bar is hidden on desktop via CSS media query (max-width: 899px). CSS for
`.mobile-book-bar*` lives in assets/scams.css. For the 13 covered countries we
link to the country book's Amazon URL (matching scripts/book-cta-rollout/
apply_book_ctas.py COUNTRIES). For orphan countries the bar points at /books/
and shows the generic Travel Safety Series bundle.

Inserts markup just BEFORE the existing `.emergency-fab` anchor so the FAB (and
its tooltip + back-to-top) stay where they are. The script is idempotent:
pages that already have `class="mobile-book-bar"` are skipped.

Usage:
    python3 scripts/inject_mobile_book_bar.py            # apply
    python3 scripts/inject_mobile_book_bar.py --dry-run  # preview
    python3 scripts/inject_mobile_book_bar.py --only tokyo dubai
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"

# Import shared sweep helper (collect_scam_targets) — keeps the target-set
# logic in one place across all scam-page sweeps.
sys.path.insert(0, str(REPO / "scripts"))
from _scam_sweep_common import collect_scam_targets  # type: ignore[import-not-found]

# Import COUNTRIES + extract_country_code + SERIES_BUNDLE from apply_book_ctas.py
# (same slug/code/amazon_url/cover_url data we use everywhere else). We import
# the helpers rather than reimplement them so future rollout changes there
# don't silently drift away from this script.
sys.path.insert(0, str(REPO / "scripts" / "book-cta-rollout"))
from apply_book_ctas import COUNTRIES, SERIES_BUNDLE, extract_country_code  # type: ignore[import-not-found]

BUNDLE_COVER = SERIES_BUNDLE["cover_url"]
BUNDLE_HREF = "/books/"  # apply_book_ctas.book_href() returns this for bundle
BUNDLE_LABEL = "Travel Safety Series"
BUNDLE_TAGLINE = "Every country's tourist scams, ready to travel"

# country-code -> (country-slug-in-COUNTRIES)
CODE_TO_SLUG: dict[str, str] = {data["code"]: slug for slug, data in COUNTRIES.items()}

# Friendly country-name -> country-code — fallback for the small set of pages
# whose hero-meta `📍 City, Country` is the only country signal (older
# Thailand/Australia templates that lack the JSON-LD Place block AND the
# breadcrumb). `extract_country_code` from apply_book_ctas covers JSON-LD +
# breadcrumb; this fallback covers the rest.
NAME_TO_CODE: dict[str, str] = {
    "Thailand": "th",
    "Australia": "au",
    # Other no-JSON-LD pages don't exist today; extend here if they appear.
}


def detect_country_code(html: str) -> str | None:
    """Return a 2–3 letter ISO country code (lower-case) or None.

    Layered: try `extract_country_code` (JSON-LD + breadcrumb) first, then
    fall back to the hero-meta's `📍 City, Country` span for older
    no-JSON-LD pages.
    """
    code = extract_country_code(html)
    if code:
        return code
    m = re.search(r'<div class="hero-meta">.*?📍[^,]+,\s*([A-Za-z][A-Za-z &]+?)\s*</span>', html, re.DOTALL)
    if m:
        name = m.group(1).strip()
        if name in NAME_TO_CODE:
            return NAME_TO_CODE[name]
    return None


def bar_html(cover_url: str, label: str, tagline: str, href: str, target_blank: bool) -> str:
    """Build the <aside> block. `script` below is a single, tiny, inline block."""
    target = ' target="_blank" rel="noopener"' if target_blank else ""
    return (
        '<aside class="mobile-book-bar" data-mobile-book-bar role="complementary" aria-label="Buy the book">\n'
        f'<img src="{cover_url}" alt="" loading="lazy" width="32" height="48">\n'
        '<div class="mobile-book-bar-text">\n'
        f'<strong>{label}</strong>\n'
        f'<span>{tagline}</span>\n'
        '</div>\n'
        f'<a href="{href}" class="mobile-book-bar-cta"{target}>Buy →</a>\n'
        '<button class="mobile-book-bar-dismiss" aria-label="Dismiss book CTA" data-mobile-book-bar-dismiss>×</button>\n'
        '</aside>\n'
        '<script>\n'
        '(function () {\n'
        '    var bar = document.querySelector(\'[data-mobile-book-bar]\');\n'
        '    if (!bar) return;\n'
        '    try { if (localStorage.getItem(\'book-bar-dismissed\') === \'1\') { bar.classList.add(\'dismissed\'); return; } } catch (e) {}\n'
        '    var dismiss = bar.querySelector(\'[data-mobile-book-bar-dismiss]\');\n'
        '    if (dismiss) dismiss.addEventListener(\'click\', function () {\n'
        '        bar.classList.add(\'dismissed\');\n'
        '        try { localStorage.setItem(\'book-bar-dismissed\', \'1\'); } catch (e) {}\n'
        '    });\n'
        '    var endCta = document.querySelector(\'.book-end-cta\');\n'
        '    if (endCta && \'IntersectionObserver\' in window) {\n'
        '        var io = new IntersectionObserver(function (entries) {\n'
        '            entries.forEach(function (e) { if (e.isIntersecting) bar.classList.add(\'dismissed\'); });\n'
        '        }, { rootMargin: \'0px 0px 600px 0px\' });\n'
        '        io.observe(endCta);\n'
        '    }\n'
        '})();\n'
        '</script>'
    )


def block_for_page(html: str) -> tuple[str, str, str | None]:
    """Return (bar_html, variant_label, country_code).

    variant_label is 'book' for country-book pages and 'bundle' for orphans
    (surfaced in the summary). country_code is whatever detect_country_code
    returned — passed back so the caller doesn't need to re-detect.
    """
    code = detect_country_code(html)
    if code and code in CODE_TO_SLUG:
        slug = CODE_TO_SLUG[code]
        d = COUNTRIES[slug]
        label = f"📖 {d['name']} Scams"
        tagline = f"$4.99 Kindle · {d['scam_count']} scams across {d['city_count']} cities"
        return bar_html(d["cover_url"], label, tagline, d["amazon_url"], target_blank=True), "book", code
    # Orphan: link to /books/ bundle
    return bar_html(BUNDLE_COVER, f"📖 {BUNDLE_LABEL}", BUNDLE_TAGLINE, BUNDLE_HREF, target_blank=False), "bundle", code


# We insert the bar *before* the existing `.emergency-fab` anchor so the FAB
# keeps its z-index-100 and stays above the bar when both are visible.
FAB_RE = re.compile(
    r'(<a[^>]*class="emergency-fab"[^>]*>.*?</a>\s*<span class="emergency-fab-tooltip">[^<]*</span>)',
    re.DOTALL,
)
# Fallback: if a page has no FAB, inject before </body>.
BODY_END_RE = re.compile(r'(\s*</body>)', re.IGNORECASE)

ALREADY_RE = re.compile(r'class="mobile-book-bar"')


def apply_to_page(html: str) -> tuple[str, str, str | None]:
    """Return (new_html, status, country_code).

    status in {'injected:book','injected:bundle','skip:existing','skip:no-anchor'}.
    country_code is the value from block_for_page (or None if we skipped before
    detection ran).
    """
    if ALREADY_RE.search(html):
        return html, "skip:existing", None
    block, variant, code = block_for_page(html)
    if FAB_RE.search(html):
        new_html = FAB_RE.sub(block + "\n" + r"\1", html, count=1)
        return new_html, f"injected:{variant}", code
    # No FAB on the page — insert before </body> as a safe fallback.
    if BODY_END_RE.search(html):
        new_html = BODY_END_RE.sub("\n" + block + r"\1", html, count=1)
        return new_html, f"injected:{variant}", code
    return html, "skip:no-anchor", code


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Preview; don't write")
    ap.add_argument("--only", nargs="*", help="Restrict to these city slugs")
    args = ap.parse_args(argv)

    only = set(args.only) if args.only else None
    totals = {"injected:book": 0, "injected:bundle": 0, "skip:existing": 0, "skip:no-anchor": 0}
    no_code_pages = []

    pages = collect_scam_targets(city_pages=True)
    for p in pages:
        slug = p.parent.name
        if only and slug not in only:
            continue
        html = p.read_text(encoding="utf-8")
        new_html, status, code = apply_to_page(html)
        totals[status] = totals.get(status, 0) + 1
        if status.startswith("injected:") and new_html != html:
            if status == "injected:bundle" and code is None:
                no_code_pages.append(slug)
            flag = "[dry]" if args.dry_run else "[write]"
            print(f"  {flag} {status:<18} /scams/{slug}")
            if not args.dry_run:
                p.write_text(new_html, encoding="utf-8")
        elif status == "skip:existing":
            # Quiet — this is the idempotent happy-path on re-runs.
            pass
        elif status == "skip:no-anchor":
            print(f"  [warn ] no FAB or </body> found on /scams/{slug}")

    print("\n=== SUMMARY ===")
    print(f"Pages scanned:           {sum(totals.values())}")
    print(f"Injected (country book): {totals['injected:book']}")
    print(f"Injected (bundle):       {totals['injected:bundle']}")
    print(f"Skipped (already has):   {totals['skip:existing']}")
    print(f"Skipped (no anchor):     {totals['skip:no-anchor']}")
    if no_code_pages:
        print(f"\nPages with no detectable country (defaulted to bundle): {len(no_code_pages)}")
        for s in no_code_pages:
            print(f"  {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
