#!/usr/bin/env python3
"""
Audit all compare pages against the gold-standard quality benchmark.

Reads HTML files directly from compare/*-vs-*/index.html (the `compare-data/`
JSON source was retired during the post-2026-04 catalog rebuild). The
audit covers structural, SEO, schema, accessibility, and content-quality
dimensions.

Gold standard: tokyo-vs-kyoto

Usage:
    python3 audit_compare.py              # Full audit report
    python3 audit_compare.py --summary    # Summary only
    python3 audit_compare.py --csv        # CSV output for spreadsheet
    python3 audit_compare.py --fix-list   # Just slugs that need work
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPARE_DIR = REPO_ROOT / "compare"

# ---------------------------------------------------------------------------
# Gold-standard benchmarks (from tokyo-vs-kyoto)
# ---------------------------------------------------------------------------
BENCHMARKS = {
    "deep_dives_min": 9,
    "faq_items_min": 7,
    "toc_items_min": 12,
    "photo_grid_min": 2,
    "comp_rows_min": 8,
    "verdict_cards_min": 2,
    "reddit_quotes_min": 3,
    "dd_images_min": 1,
    "section_winners_min": 5,
    "faq_answer_min_len": 30,
    "meta_desc_max_len": 200,
    "title_max_len": 100,
    "ai_tells_max": 10,
    "currency_symbols_max": 2,
    "generic_reddit_url_pct_max": 50,
}

AI_TELLS = (
    "vibrant", "bustling", "perfect for", "world-class", "delve into",
    "must-see", "hidden gem", "magical", "breathtaking", "treasure trove",
    "nestled", "boasts", "you'll love",
)

CURRENCY_SYMBOLS = ("$", "¥", "£", "€", "₩", "₹", "฿", "₱", "₽", "CHF", "CAD")


def _extract_block(text: str, start_re: str, end_re: str = r"</section>") -> str:
    m = re.search(start_re + r".*?" + end_re, text, re.S)
    return m.group(0) if m else ""


def audit_page(slug: str, html: str) -> dict:
    """Audit one compare-page HTML string, return metrics + issues."""
    # ----- Extract meta -----
    title_m = re.search(r"<title>([^<]+)</title>", html)
    title = title_m.group(1).strip() if title_m else ""
    meta_desc_m = (
        re.search(r'<meta\s+content="([^"]+)"\s+name="description"', html)
        or re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    )
    meta_desc = meta_desc_m.group(1) if meta_desc_m else ""
    og_image_m = (
        re.search(r'property="og:image"[^>]*content="([^"]+)"', html)
        or re.search(r'<meta\s+content="([^"]+)"\s+property="og:image"', html)
    )
    og_image = og_image_m.group(1) if og_image_m else ""
    mod_m = re.search(r'article:modified_time"[^>]*content="(\d{4}-\d{2}-\d{2})', html)
    modified_time = mod_m.group(1) if mod_m else ""

    # ----- Section detection -----
    # FAQ section has two markup patterns across the corpus:
    #   gold standard:  <section id="frequently-asked-questions">
    #   older pages:    <div class="faq-section" id="faq">
    # End pattern stops at related-comparisons blocks (which use h3 too).
    faq_section = _extract_block(
        html,
        (
            r'(?:'
            r'<section[^>]*id="frequently-asked-questions"|'
            r'id="frequently-asked-questions"[^>]*>|'
            r'<div[^>]*class="faq-section"|'
            r'<section[^>]*id="faq"\b|'
            r'class="faq-section"[^>]*>'
            r')'
        ),
        (
            r'(?:'
            r'<section\b|<footer\b|</main>|'
            r'<!-- compare-related|'
            r'<div[^>]*class="(?:ux-)?related|'
            r'<div[^>]*class="related-comparisons|'
            r'<h2[^>]*>(?:[^<]*Related|🔗|↩)'
            r')'
        ),
    )
    photo_html = _extract_block(html, r'<div class="photo-grid"', r"</div>\s*</section>|</div>\s*<div class=")

    # Body = everything between <main ...> and </main>
    main_m = re.search(r"<main\b[^>]*>(.*?)</main>", html, re.S)
    body = main_m.group(1) if main_m else html

    # ----- Metrics -----
    metrics = {
        "slug": slug,
        "title": title,
        "title_len": len(title),
        "meta_desc_len": len(meta_desc),
        "modified_time": modified_time,
        "has_og_image": bool(og_image),
        "og_image_dest_generic": ("dest1.jpg" in og_image or "dest2.jpg" in og_image),
        "deep_dives": len(re.findall(r'<h2\b[^>]*\bid=', body)),
        "faq_items": html.count('"@type": "Question"') + html.count('"@type":"Question"'),
        "faq_visible_h3": sum(
            1 for q in re.findall(r"<h3[^>]*>([^<]+)</h3>", faq_section)
            if q.strip().endswith('?')
        ),
        "photo_count": len(re.findall(r"<img\b", photo_html)),
        "dd_images": body.count("<img"),
        "reddit_quote_blocks": body.count("reddit-quote"),
        "section_winners": (
            body.count("section-winner")
            + body.count("qa-winner")
            + body.count("sc-winner")
        ),
        "comp_rows": max(0, len(re.findall(r"<tr>", body)) - 1),
        "verdict_cards": html.count("verdict-card"),
        "has_year_in_title": bool(re.search(r"202[4-9]", title)),
        "has_verdict_takeaways": "verdict-takeaways" in html,
        "has_visible_breadcrumb": 'aria-label="Breadcrumb"' in html,
        "has_byline": 'class="page-byline"' in html,
        "has_person_author": ('"@type": "Person"' in html or '"@type":"Person"' in html),
        "has_scorecard": "scorecard" in html,
        "has_related_block": (
            "related-comparisons" in html
            or "compare-related:start" in html
            or "ux-related-links" in html
        ),
        "has_methodology_box": "methodology-box" in html,
    }

    # Reddit URL hygiene
    all_reddit = re.findall(r'href="(https?://(?:www\.)?reddit\.com/[^"]+)"', body)
    specific_thread = sum(1 for u in all_reddit if "/comments/" in u)
    metrics["reddit_urls_total"] = len(all_reddit)
    metrics["reddit_urls_specific"] = specific_thread
    metrics["reddit_urls_generic_pct"] = (
        round(100 * (len(all_reddit) - specific_thread) / len(all_reddit), 1)
        if all_reddit else 0
    )
    metrics["reddit_links_have_rel_ugc"] = body.count('rel="noopener nofollow ugc"')

    # Alt text quality
    photo_alts = re.findall(r'alt="([^"]*)"', photo_html)
    metrics["photo_count_alts"] = len(photo_alts)
    metrics["generic_photo_alts"] = sum(
        1 for a in photo_alts if len(a) < 10 or a.lower() in ("image", "photo", "picture", "")
    )

    # FAQ answer quality (read from JSON-LD)
    short_faq = 0
    for m in re.finditer(r'"@type":\s*"Question"[^}]*"text":\s*"([^"]+)"', html):
        if len(m.group(1)) < BENCHMARKS["faq_answer_min_len"]:
            short_faq += 1
    metrics["short_faq_answers"] = short_faq

    # FAQ schema-vs-body parity (only count h3s that look like real questions —
    # end with '?' — to avoid related-link headings being misclassified)
    ld_qs = re.findall(r'"@type":\s*"Question"[^"]*"name":\s*"([^"]+)"', html)
    visible_qs = re.findall(r"<h3[^>]*>([^<]+)</h3>", faq_section)
    real_visible_qs = [q for q in visible_qs if q.strip().endswith('?')]
    metrics["faq_schema_body_count_mismatch"] = (len(ld_qs) != len(real_visible_qs))

    # Placeholders / template debris
    placeholder_patterns = (
        r"\[TODO\]", r"\[INSERT\]", r"\[PLACEHOLDER\]",
        r"\{\{[a-z_]+\}\}", r"\bundefined\b\s*(?:vs|of)",
    )
    metrics["placeholder_count"] = sum(
        1 for p in placeholder_patterns if re.search(p, body)
    )

    # Empty rendered sections
    metrics["empty_p"] = len(re.findall(r"<p>\s*</p>", body))
    metrics["empty_reddit_quote"] = len(re.findall(r'<div class="reddit-quote">\s*</div>', body))

    # AI tells (count phrase occurrences across body)
    ai_tell_hits = sum(
        len(re.findall(r"\b" + re.escape(phrase) + r"\b", body, re.I))
        for phrase in AI_TELLS
    )
    metrics["ai_tell_count"] = ai_tell_hits

    # Currency overload
    metrics["currency_symbols_present"] = sum(1 for s in CURRENCY_SYMBOLS if s in body)

    # Stale/pandemic references
    stale_patterns = (
        r"\bCOVID\b", r"\bpandemic\b", r"\bcoronavirus\b",
        r"Expo 2020", r"Olympics 202[0-4]",
    )
    metrics["stale_refs"] = sum(1 for p in stale_patterns if re.search(p, body))

    # ----- Score calc -----
    issues = []
    score = 100

    # CRITICAL (-25)
    if metrics["verdict_cards"] == 0:
        issues.append("NO_VERDICT_CARDS")
        score -= 25
    if metrics["section_winners"] < BENCHMARKS["section_winners_min"]:
        issues.append(f"LOW_SECTION_WINNERS({metrics['section_winners']})")
        score -= 25
    if not metrics["has_visible_breadcrumb"]:
        issues.append("NO_BREADCRUMB_HTML")
        score -= 10
    if metrics["reddit_quote_blocks"] == 0:
        issues.append("NO_REDDIT_QUOTES")
        score -= 15
    if metrics["dd_images"] == 0:
        issues.append("NO_DD_IMAGES")
        score -= 10
    if not metrics["has_byline"]:
        issues.append("NO_BYLINE")
        score -= 10
    if not metrics["has_person_author"]:
        issues.append("NO_PERSON_AUTHOR")
        score -= 5
    if metrics["placeholder_count"] > 0:
        issues.append(f"PLACEHOLDERS({metrics['placeholder_count']})")
        score -= 20

    # HIGH (-10)
    if metrics["reddit_urls_total"] > 0 and metrics["reddit_urls_generic_pct"] > BENCHMARKS["generic_reddit_url_pct_max"]:
        issues.append(f"GENERIC_REDDIT_URLS({metrics['reddit_urls_generic_pct']}%)")
        score -= 10
    if not metrics["has_related_block"]:
        issues.append("NO_RELATED_BLOCK")
        score -= 5
    if metrics["faq_schema_body_count_mismatch"]:
        issues.append("FAQ_COUNT_MISMATCH")
        score -= 10

    # MEDIUM (-5)
    if metrics["deep_dives"] < BENCHMARKS["deep_dives_min"]:
        issues.append(f"LOW_DEEP_DIVES({metrics['deep_dives']})")
        score -= 5
    if metrics["comp_rows"] < BENCHMARKS["comp_rows_min"]:
        issues.append(f"LOW_COMP_ROWS({metrics['comp_rows']})")
        score -= 5
    if metrics["faq_items"] < BENCHMARKS["faq_items_min"]:
        issues.append(f"LOW_FAQ({metrics['faq_items']})")
        score -= 5
    if metrics["short_faq_answers"] > 0:
        issues.append(f"SHORT_FAQ_ANSWERS({metrics['short_faq_answers']})")
        score -= 5
    if metrics["ai_tell_count"] > BENCHMARKS["ai_tells_max"]:
        issues.append(f"AI_TELLS_HIGH({metrics['ai_tell_count']})")
        score -= 5
    if metrics["currency_symbols_present"] > BENCHMARKS["currency_symbols_max"]:
        issues.append(f"CURRENCY_OVERLOAD({metrics['currency_symbols_present']})")
        score -= 3
    if metrics["stale_refs"] > 0:
        issues.append(f"STALE_REFS({metrics['stale_refs']})")
        score -= 3
    if (
        metrics["reddit_urls_total"] > 0
        and metrics["reddit_links_have_rel_ugc"] == 0
    ):
        issues.append("NO_REL_UGC")
        score -= 3

    # MINOR (-2)
    if metrics["empty_p"] > 0 or metrics["empty_reddit_quote"] > 0:
        issues.append("EMPTY_TAGS")
        score -= 2
    if not metrics["has_verdict_takeaways"]:
        issues.append("NO_VERDICT_TAKEAWAYS")
        score -= 2
    if metrics["title_len"] > BENCHMARKS["title_max_len"]:
        issues.append(f"LONG_TITLE({metrics['title_len']})")
        score -= 2
    if metrics["meta_desc_len"] > BENCHMARKS["meta_desc_max_len"]:
        issues.append(f"LONG_META_DESC({metrics['meta_desc_len']})")
        score -= 2
    if metrics["og_image_dest_generic"]:
        issues.append("GENERIC_OG_IMAGE")
        score -= 2

    metrics["score"] = max(0, score)
    metrics["issues"] = issues
    metrics["tier"] = (
        "A" if score >= 95 else
        "B" if score >= 80 else
        "C" if score >= 60 else
        "D"
    )

    return metrics


def load_all() -> list[dict]:
    results = []
    for d in sorted(os.listdir(COMPARE_DIR)):
        if "-vs-" not in d:
            continue
        p = COMPARE_DIR / d / "index.html"
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        results.append(audit_page(d, html))
    return results


def print_summary(results: list[dict]) -> None:
    total = len(results)
    if not total:
        print("No compare pages found.")
        return
    tiers = Counter(r["tier"] for r in results)
    scores = [r["score"] for r in results]

    print(f"\n{'='*60}")
    print(f"COMPARE PAGE AUDIT REPORT — {total} pages")
    print(f"{'='*60}\n")

    print("TIER DISTRIBUTION:")
    for tier in ["A", "B", "C", "D"]:
        count = tiers.get(tier, 0)
        pct = count / total * 100
        bar = "█" * int(pct / 2)
        print(f"  Tier {tier}: {count:>5} ({pct:5.1f}%) {bar}")

    print(f"\nSCORE STATS:")
    print(f"  Mean:   {sum(scores)/len(scores):.1f}")
    print(f"  Median: {sorted(scores)[len(scores)//2]}")
    print(f"  Min:    {min(scores)}")
    print(f"  Max:    {max(scores)}")

    issue_counts = Counter()
    for r in results:
        for issue in r["issues"]:
            base = re.sub(r"\(.*\)", "", issue)
            issue_counts[base] += 1

    print(f"\nISSUE FREQUENCY:")
    for issue, count in issue_counts.most_common():
        pct = count / total * 100
        print(f"  {issue:<25} {count:>5} ({pct:5.1f}%)")


def print_full_report(results: list[dict]) -> None:
    print_summary(results)
    worst = sorted(results, key=lambda r: r["score"])[:20]
    print(f"\n{'='*60}")
    print("BOTTOM 20 PAGES:")
    print(f"{'='*60}")
    for r in worst:
        print(f"\n  {r['slug']} (score: {r['score']}, tier: {r['tier']})")
        print(f"    Issues: {', '.join(r['issues'])}")


def print_csv(results: list[dict]) -> None:
    fields = [
        "slug", "score", "tier",
        "deep_dives", "faq_items", "faq_visible_h3", "faq_schema_body_count_mismatch",
        "photo_count", "dd_images", "reddit_quote_blocks", "section_winners",
        "comp_rows", "verdict_cards", "has_verdict_takeaways", "placeholder_count",
        "short_faq_answers", "generic_photo_alts",
        "title_len", "meta_desc_len", "modified_time", "has_og_image",
        "og_image_dest_generic", "reddit_urls_total", "reddit_urls_specific",
        "reddit_urls_generic_pct", "reddit_links_have_rel_ugc",
        "has_visible_breadcrumb", "has_byline", "has_person_author",
        "has_related_block", "has_methodology_box",
        "empty_p", "empty_reddit_quote", "ai_tell_count",
        "currency_symbols_present", "stale_refs",
        "issues",
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for r in sorted(results, key=lambda r: r["score"]):
        row = {**r, "issues": "; ".join(r["issues"])}
        writer.writerow(row)


def print_fix_list(results: list[dict]) -> None:
    for r in sorted(results, key=lambda r: r["score"]):
        if r["tier"] in ("C", "D"):
            print(r["slug"])


def main() -> None:
    results = load_all()

    if "--csv" in sys.argv:
        print_csv(results)
    elif "--fix-list" in sys.argv:
        print_fix_list(results)
    elif "--summary" in sys.argv:
        print_summary(results)
    else:
        print_full_report(results)


if __name__ == "__main__":
    main()
