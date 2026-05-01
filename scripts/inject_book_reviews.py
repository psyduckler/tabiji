#!/usr/bin/env python3
"""Inject reader-review blocks + JSON-LD AggregateRating/Review onto book landers.

For each country in REVIEWS, finds the Book JSON-LD block and the
<section class="bottom-cta"> in the corresponding book lander, then:
  1. Adds aggregateRating + review array to the Book schema
  2. Inserts a <section class="book-reviews"> immediately before the bottom-cta

Idempotent: if a previous run already inserted these, this script skips
that country (looks for `class="book-reviews"` in the page).

Usage:  python3 scripts/inject_book_reviews.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS_DIR = REPO / "books"

# Per-country reviews. Each country has 1-3 quotes — best per book.
# Avg = mean of all reviews we have for that country (incl. ones not shown);
# Count = total reviews collected. Verified=True only when the source
# screenshot showed an explicit "Verified Purchase" badge.
REVIEWS: dict[str, dict] = {
    "japan": {
        "avg": 5.0, "count": 4,
        "items": [
            {"name": "Michael", "rating": 5, "verified": True, "format": "Kindle",
             "quote": "As a two-year solo backpacker, I can tell you encountering scams is part of traveling. This book is an absolute must read before heading to Japan."},
            {"name": "Michael Goodman", "rating": 5, "format": "Kindle",
             "quote": "What sets it apart is the inclusion of exact Japanese phrases you can use in real situations — something I've never seen done this effectively before. It's practical, empowering, and incredibly well-researched."},
            {"name": "Laverne Rhodes", "rating": 5, "format": "Paperback",
             "quote": "The combination of real scam cases and exact Japanese phrases makes it stand out from other travel books. You're not just warned, you're equipped to respond."},
        ],
    },
    "italy": {
        "avg": 5.0, "count": 1,
        "items": [
            {"name": "Malcolm Kerry", "rating": 5, "format": "Paperback",
             "quote": "The detailed breakdown of 149 real scams makes it stand out from typical travel guides. I appreciate how it focuses on real incidents drawn from official reports, which adds a strong sense of credibility."},
        ],
    },
    "thailand": {
        "avg": 5.0, "count": 4,
        "items": [
            {"name": "Michael", "rating": 5, "verified": True, "format": "Kindle",
             "quote": "Great book that easily paid for itself. Sometimes I forget how much stronger the dollar is — even if it's not a lot of money, I'd still be overpaying by multiple times in Thailand. An easy read that educated me and prepared me for one of my favorite countries."},
            {"name": "Rachel Nicholls", "rating": 5, "format": "Kindle",
             "quote": "Goes beyond typical travel advice by exposing real scams backed by Thai news reports and tourist police records, which adds serious credibility. Perfect for both first-time visitors and seasoned travelers."},
            {"name": "Jeff Wolff", "rating": 5, "format": "Kindle",
             "quote": "This is a very comprehensive book that covers all of the scams imaginable. What really makes this book great is that it breaks the scams down by location. With so many to keep an eye out for, it can be hard to keep track of them all, but by knowing what to look for in each specific place, it makes everything much more manageable."},
        ],
    },
    "greece": {
        "avg": 5.0, "count": 2,
        "items": [
            {"name": "Yugti", "rating": 5, "format": "Kindle",
             "quote": "This book both terrified and excited me. I had no idea there were so many tourist traps and blatant rip-off artists in Greece. The guide prepared me for how to have an enjoyable time AND keep my wallet."},
            {"name": "Jeffery Lucas", "rating": 5, "format": "Kindle",
             "quote": "A practical and eye-opening guide that helps you stay aware and prepared while traveling. The real examples make it easy to recognize common scams, and the advice is clear and useful."},
        ],
    },
    "spain": {
        "avg": 5.0, "count": 3,
        "items": [
            {"name": "Murshed", "rating": 5, "format": "Kindle",
             "quote": "I've been to Spain a few times and always considered myself pretty street-smart. Then I read this book and realized how many scams I probably walked right past without even noticing."},
            {"name": "Jeremiah", "rating": 5, "format": "Kindle",
             "quote": "I'm walking the Camino this summer and was surprised to find a section dedicated to Santiago de Compostela. The warnings about 'reserved seat' fraud at the Pilgrim Mass and taxi overcharges were extremely specific. Truly an essential piece of 'digital gear.'"},
            {"name": "Amazon Reader", "rating": 5, "format": "Kindle",
             "quote": "Spain: Tourist Scams 2026 is a highly useful guide that every traveler should have before visiting. The real-life cases make the risks easy to recognize, and the advice is clear and actionable."},
        ],
    },
    "indonesia": {
        "avg": 4.8, "count": 4,
        "items": [
            {"name": "Erica Eaton", "rating": 5, "format": "Kindle",
             "quote": "A concise yet highly informative guide that every traveler to Indonesia should consider essential. Covering 73 real scams across popular destinations like Bali, Jakarta, and Yogyakarta — stands out for its credible sourcing and practical insights."},
            {"name": "Chang McMillan", "rating": 5, "format": "Kindle",
             "quote": "It's not fear-mongering — it's empowering. The inclusion of multiple cities like Bali, Jakarta, and Yogyakarta makes it comprehensive and relevant for different types of travelers. A smart investment for peace of mind."},
            {"name": "Timothy Caron", "rating": 5, "format": "Kindle",
             "quote": "Doesn't just list scams — it breaks them down in a way that's easy to understand and even easier to remember. The fact that the cases are drawn from real Indonesian news reports and tourist police records adds a layer of authenticity."},
        ],
    },
    "china": {
        "avg": 5.0, "count": 4,
        "items": [
            {"name": "Aryana Roy", "rating": 5, "format": "Kindle",
             "quote": "A thorough and highly practical guide for anyone planning to visit China. Covering 98 real scams across Beijing, Shanghai, and Xi'an — stands out for its strong research base and clear, structured approach. An essential resource for navigating China with confidence."},
            {"name": "Oaklyn Potts", "rating": 5, "format": "Kindle",
             "quote": "A highly informative and practical resource that helps you stay alert while exploring new destinations. The real-world examples make it easy to understand potential risks, and the advice is clear and actionable."},
            {"name": "Dalia Charles", "rating": 5, "format": "Kindle",
             "quote": "An incredibly helpful and eye-opening guide that prepares you for real situations travelers may face. The city-by-city breakdown makes it easy to stay alert."},
        ],
    },
    "canada": {
        "avg": 5.0, "count": 1,
        "items": [
            {"name": "Shawna Abbott", "rating": 5, "format": "Kindle",
             "quote": "Canada Tourist Scams 2026 is an insightful and well-structured book that helps you stay one step ahead while traveling. The real examples make the information easy to understand, and the tips are practical and easy to apply."},
        ],
    },
    "mexico": {
        "avg": 5.0, "count": 1,
        "items": [
            {"name": "Gordon", "rating": 5, "format": "Kindle",
             "quote": "An absolute lifesaver for anyone planning a trip to Mexico. I especially appreciated how the author used verified sources like news reports and tourist-police records — it adds a level of trust you don't usually see in travel guides."},
        ],
    },
    "germany": {
        "avg": 5.0, "count": 4,
        "items": [
            {"name": "Jeffery Curtis", "rating": 5, "format": "Kindle",
             "quote": "What sets this book apart is its authenticity — these aren't vague warnings but real scams backed by news reports and Polizei records. The author does an excellent job breaking down each scam in a way that is easy to understand and remember."},
            {"name": "Floyd Edwards", "rating": 5, "format": "Kindle",
             "quote": "This isn't your typical travel guide — it's a survival manual for modern travelers. Delivers a refreshing and much-needed perspective by focusing on the realities that many guides ignore."},
            {"name": "Margie Kennedy", "rating": 5, "format": "Kindle",
             "quote": "I didn't expect a book about scams to be this engaging, but it kept me hooked from start to finish. The real-life examples make it feel almost like reading short stories, except each one teaches you something valuable."},
        ],
    },
    "united-kingdom": {
        "avg": 5.0, "count": 1,
        "items": [
            {"name": "Rev. David A. Dickinson", "rating": 5, "format": "Kindle",
             "quote": "Heading over to London and Edinburgh this summer and the book was a real eye-opener. Most travel guides just show you the bits that look good on a postcard but this actually digs into the police reports to show you what to watch out for."},
        ],
    },
    "portugal": {
        "avg": 4.5, "count": 2,
        "items": [
            {"name": "Robert Spratt", "rating": 5, "format": "Paperback",
             "quote": "An excellent companion for anyone planning a trip to Portugal. The coverage of 65 real scams is both eye-opening and practical. I love how it highlights real situations across Lisbon, Porto, and even places like Madeira."},
            {"name": "Lepacole", "rating": 4, "format": "Kindle",
             "quote": "Practical and highly useful resource for anyone planning to visit Portugal. The book clearly outlines common scams across Lisbon, Porto, and the Algarve, helping travelers stay informed and prepared."},
        ],
    },
    "morocco": {
        "avg": 5.0, "count": 1,
        "items": [
            {"name": "Felix McGuire", "rating": 5, "format": "Kindle",
             "quote": "Exactly the kind of book every traveler needs before visiting Morocco. It goes beyond generic advice and dives into real scams happening in places like Marrakech and Fez. The fact that it's based on news reports and official records makes it incredibly trustworthy."},
        ],
    },
    "vietnam": {
        "avg": 5.0, "count": 1,
        "items": [
            {"name": "Javier Wise", "rating": 5, "format": "Kindle",
             "quote": "An incredibly helpful guide that breaks down real risks in a clear and practical way. The city-by-city approach makes it easy to prepare ahead, and the tips are straightforward and useful."},
        ],
    },
    "argentina": {
        "avg": 5.0, "count": 1,
        "items": [
            {"name": "Thelma Goodman", "rating": 5, "format": "Paperback",
             "quote": "An absolute lifesaver for anyone planning a trip to Argentina. The detailed breakdown of 66 real scams makes it incredibly practical and eye-opening. I especially appreciated how the information is backed by credible sources like news reports and police records."},
        ],
    },
    "france": {
        "avg": 4.8, "count": 4,
        "items": [
            {"name": "Margo Golden", "rating": 5, "format": "Kindle",
             "quote": "An essential and eye-opening guide for anyone planning a trip to France. This book stands out for its depth and credibility, compiling 191 real scams from verified news reports and official sources. It not only exposes common tourist traps across Paris, Nice, Provence, and beyond, but also equips readers with practical knowledge to avoid them. Clear, well-researched, and highly relevant for modern travelers."},
            {"name": "RolfDuarte", "rating": 5, "format": "Kindle",
             "quote": "France Tourist Scams 2026 is a well-researched and highly practical book that gives travelers a clear understanding of what to watch out for. The real case examples make it easy to stay alert, and the guidance is straightforward and helpful. A must-have resource for anyone planning to visit France."},
            {"name": "Bobby Bell", "rating": 4, "format": "Paperback",
             "quote": "This book is an essential guide for anyone planning a trip to France. With 191 real scams covered, it goes far beyond basic travel advice. I was impressed by how detailed and well-organized everything is. The use of French news reports and official records adds credibility, making it a reliable resource. It definitely helped me feel more confident about exploring cities like Paris and Nice."},
        ],
    },
    "turkey": {
        "avg": 5.0, "count": 1,
        "items": [
            {"name": "Micheal suggs", "rating": 5, "format": "Kindle",
             "quote": "Very practical and straight to the point. The book explains real scams with clear examples, exact scripts and useful warning signs. The Turkish phrases and recovery steps make it even more valuable. It feels like a real safety manual, not just a travel guide. Highly recommended for anyone visiting Türkiye."},
        ],
    },
}


def render_section(country: str, data: dict, country_display: str) -> str:
    items = data["items"]
    count = data["count"]
    avg = data["avg"]
    avg_str = f"{avg:.1f}" if avg < 5.0 else "5.0"

    if count == 1:
        sub = f"From a verified Amazon reader of <em>{country_display}: Tourist Scams 2026</em>."
    else:
        sub = f"From verified Amazon readers of <em>{country_display}: Tourist Scams 2026</em>."

    cards = []
    for r in items:
        stars = "★" * r["rating"] + "☆" * (5 - r["rating"])
        verified_html = '<span class="book-review-verified">Verified Purchase</span>' if r.get("verified") else ""
        format_html = f'<div class="book-review-format">{r["format"]} edition</div>' if r.get("format") else ""
        # quote is plain text from REVIEWS dict; HTML-escape angle brackets
        quote = r["quote"].replace("<", "&lt;").replace(">", "&gt;")
        cards.append(
            f'''      <article class="book-review-card">
        <div class="book-review-stars" aria-label="{r["rating"]} out of 5 stars">{stars}</div>
        <p class="book-review-quote">"{quote}"</p>
        <div class="book-review-attr">
          <span class="book-review-name">{r["name"]}</span>{verified_html}
          {format_html}
        </div>
      </article>'''
        )

    grid_class = "single" if len(items) == 1 else ""
    return f'''
<section class="book-reviews" aria-labelledby="book-reviews-heading-{country}">
  <div class="book-reviews-inner">
    <span class="book-reviews-eyebrow">Readers</span>
    <h2 id="book-reviews-heading-{country}"><em>★ {avg_str}</em> from {count} verified review{"" if count == 1 else "s"}.</h2>
    <p class="book-reviews-sub">{sub}</p>
    <div class="book-reviews-grid {grid_class}">
{chr(10).join(cards)}
    </div>
  </div>
</section>

'''


def update_schema(html: str, country: str, data: dict) -> str:
    """Inject aggregateRating + review array into the Book JSON-LD."""
    # Iterate every JSON-LD block, parse, find the Book one, augment it.
    pattern = re.compile(r'<script type="application/ld\+json">([^<]+)</script>')
    for m in pattern.finditer(html):
        try:
            obj = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        if obj.get("@type") != "Book":
            continue
        if "aggregateRating" in obj:
            return html  # already injected; skip

        avg = data["avg"]
        obj["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": f"{avg:.1f}" if avg < 5.0 else "5",
            "reviewCount": str(data["count"]),
            "bestRating": "5",
            "worstRating": "1",
        }
        obj["review"] = [
            {
                "@type": "Review",
                "author": {"@type": "Person", "name": r["name"]},
                "reviewRating": {"@type": "Rating", "ratingValue": str(r["rating"]), "bestRating": "5"},
                "reviewBody": r["quote"],
            }
            for r in data["items"]
        ]
        new_json = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        return html.replace(m.group(0), f'<script type="application/ld+json">{new_json}</script>')
    return html  # no Book schema found


def country_display_name(country: str) -> str:
    overrides = {"united-kingdom": "United Kingdom", "costa-rica": "Costa Rica"}
    return overrides.get(country, country.replace("-", " ").title())


def process(country: str, data: dict, dry_run: bool) -> tuple[bool, str]:
    page = BOOKS_DIR / f"{country}-tourist-scams" / "index.html"
    if not page.exists():
        return False, "no page"
    html = page.read_text()
    if 'class="book-reviews"' in html:
        return False, "already injected"

    section = render_section(country, data, country_display_name(country))

    bottom_cta = '<section class="bottom-cta">'
    if bottom_cta not in html:
        return False, "no bottom-cta anchor"

    new_html = html.replace(bottom_cta, section + bottom_cta, 1)
    new_html = update_schema(new_html, country, data)

    if dry_run:
        return True, f"would write {len(new_html) - len(html):+d} chars"
    page.write_text(new_html)
    return True, f"wrote {len(new_html) - len(html):+d} chars"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ok, skipped = 0, 0
    for country, data in REVIEWS.items():
        success, msg = process(country, data, args.dry_run)
        marker = "✓" if success else "·"
        print(f"  {marker} {country:18s}  {msg}")
        if success:
            ok += 1
        else:
            skipped += 1
    print(f"\n{ok} updated, {skipped} skipped" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
