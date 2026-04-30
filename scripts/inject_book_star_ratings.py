#!/usr/bin/env python3
"""Inject per-book star ratings:
  - Hub cards in books/index.html: under the "Buy on Amazon" CTA.
  - Country pages: inline next to "$4.99 on Kindle".

Pulls rating data from scripts/inject_book_reviews.REVIEWS so the two
scripts stay in sync. Idempotent: skips countries already injected.

Usage: python3 scripts/inject_book_star_ratings.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
from inject_book_reviews import REVIEWS  # noqa: E402

HUB = REPO / "books" / "index.html"


def fmt_rating(country: str) -> str | None:
    data = REVIEWS.get(country)
    if not data:
        return None
    avg = data["avg"]
    count = data["count"]
    val = f"{avg:.1f}"
    word = "review" if count == 1 else "reviews"
    return val, count, word


def inject_hub_cards(dry_run: bool) -> int:
    """For every book card on the hub, add a rating row after the buy CTA."""
    html = HUB.read_text()
    before = html
    updated = 0

    # The book-card-footer wraps the price + Buy-on-Amazon button.
    # Insert <div class="book-card-rating"> right after </div> closing book-card-footer.
    # We need the country slug to look up the rating — find it from the buy URL or earlier comment.
    #
    # Strategy: walk article-by-article using the comment markers (<!-- ========== JAPAN ========== -->)
    # which the hub already uses for grouping.
    pattern = re.compile(
        r'<!-- =+\s*([A-Z][A-Z\- ]+?)\s*=+ -->'  # marker comment, e.g. <!-- ========== JAPAN ========== -->
        r'(.*?)'                                  # card body (non-greedy)
        r'(?=<!-- =+\s*[A-Z]|</div>\s*</section>)',  # next marker or end of grid
        re.DOTALL,
    )

    def replace_card(m: re.Match) -> str:
        marker = m.group(0).split(m.group(2))[0]  # the marker comment line
        body = m.group(2)
        slug_raw = m.group(1).strip().lower()
        # Map display name → slug used in REVIEWS dict.
        slug_map = {
            "japan": "japan", "italy": "italy", "france": "france",
            "thailand": "thailand", "greece": "greece", "vietnam": "vietnam",
            "spain": "spain", "indonesia": "indonesia", "china": "china",
            "canada": "canada", "mexico": "mexico", "turkey": "turkey",
            "germany": "germany", "brazil": "brazil", "portugal": "portugal",
            "united kingdom": "united-kingdom", "uk": "united-kingdom",
            "morocco": "morocco", "australia": "australia", "colombia": "colombia",
            "costa rica": "costa-rica", "egypt": "egypt", "argentina": "argentina",
            "malaysia": "malaysia",
        }
        slug = slug_map.get(slug_raw)
        if not slug:
            return m.group(0)

        rating = fmt_rating(slug)
        if not rating:
            return m.group(0)
        if 'class="book-card-rating"' in body:
            return m.group(0)  # already injected

        val, count, word = rating
        rating_html = (
            f'\n            <div class="book-card-rating" aria-label="Rated {val} out of 5, {count} {word}">'
            f'<span class="star" aria-hidden="true">★</span>'
            f'{val} <span class="rating-count">· {count} {word}</span>'
            f'</div>'
        )

        # Insert immediately after the </div> that closes class="book-card-footer".
        # Anchor on the CTA's closing </a> + the footer's closing </div> (deterministic).
        footer_close_re = re.compile(
            r'(<a[^>]*class="book-card-cta"[^>]*>[^<]*</a>\s*</div>)',
            re.DOTALL,
        )
        new_body, n = footer_close_re.subn(lambda fm: fm.group(1) + rating_html, body, count=1)
        if n == 0:
            return m.group(0)
        return marker + new_body

    new_html, n = pattern.subn(replace_card, html)
    # Count actual changes by searching for new class
    diff_count = new_html.count('class="book-card-rating"') - before.count('class="book-card-rating"')

    if diff_count and not dry_run:
        HUB.write_text(new_html)
    return diff_count


def inject_country_pages(dry_run: bool) -> dict[str, str]:
    """For each country with reviews, inject .cta-rating next to .cta-price."""
    results: dict[str, str] = {}
    for country in REVIEWS:
        page = REPO / "books" / f"{country}-tourist-scams" / "index.html"
        if not page.exists():
            results[country] = "no page"
            continue
        html = page.read_text()
        if 'class="cta-rating"' in html:
            results[country] = "already injected"
            continue

        rating = fmt_rating(country)
        if not rating:
            results[country] = "no rating data"
            continue
        val, count, word = rating

        rating_html = (
            f'<span class="cta-rating" aria-label="Rated {val} out of 5, {count} {word}">'
            f'<span class="star" aria-hidden="true">★</span>'
            f'{val} <span class="rating-count">· {count} {word}</span>'
            f'</span>'
        )

        # Match the cta-price span (one line). Insert rating directly after it.
        target = re.compile(r'(<span class="cta-price"><strong>\$4\.99</strong> on Kindle</span>)')
        new_html, n = target.subn(r'\1 ' + rating_html, html, count=1)
        if n == 0:
            results[country] = "no cta-price anchor"
            continue
        if not dry_run:
            page.write_text(new_html)
        results[country] = f"+{len(new_html) - len(html)} chars"
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    print("=== HUB CARDS ===")
    n = inject_hub_cards(args.dry_run)
    mode = " (dry-run)" if args.dry_run else ""
    print(f"  {n} cards updated{mode}")

    print("\n=== COUNTRY PAGES ===")
    results = inject_country_pages(args.dry_run)
    ok = 0
    for country, msg in results.items():
        marker = "✓" if msg.startswith("+") else "·"
        print(f"  {marker} {country:18s}  {msg}")
        if marker == "✓":
            ok += 1
    print(f"\n{ok} country pages updated{mode}")


if __name__ == "__main__":
    main()
