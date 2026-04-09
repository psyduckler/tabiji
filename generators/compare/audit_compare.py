#!/usr/bin/env python3
"""
Audit all compare pages against the gold-standard quality benchmark.

Gold standard: tokyo-vs-kyoto
- Verdict box with 2+ cards
- Reddit quotes in deep-dive sections
- Images in deep-dive sections
- Section winners in all deep-dives
- Photo grid with 2+ images + descriptive alt text
- 7+ FAQ items with substantial answers
- 10+ comparison table rows
- 9+ deep-dive sections

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
DATA_DIR = REPO_ROOT / "compare-data"

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
    "reddit_quotes_min": 1,       # at least some
    "dd_images_min": 1,           # at least some
    "section_winners_min": 5,     # at least half of deep-dives
    "faq_answer_min_len": 30,
    "meta_desc_max_len": 160,
    "title_max_len": 100,
}


def audit_page(data: dict) -> dict:
    """Audit a single compare page, return metrics + issues."""
    slug = data.get("slug", "unknown")
    content = data.get("content", {})
    seo = data.get("seo", {})

    # --- Extract metrics ---
    deep_dives = content.get("deepDiveHtml", [])
    dd_html = "".join(deep_dives)

    photo_html = content.get("photoGridHtml", "")
    verdict_html = content.get("verdictHtml", "")
    comp_html = content.get("comparisonHtml", "")
    faq_items = content.get("faqItems", [])
    toc_items = content.get("tocItems", [])

    metrics = {
        "slug": slug,
        "dest1": data.get("destinations", {}).get("destination1", ""),
        "dest2": data.get("destinations", {}).get("destination2", ""),
        "deep_dives": len(deep_dives),
        "faq_items": len(faq_items),
        "toc_items": len(toc_items),
        "photo_count": len(re.findall(r"<img ", photo_html)),
        "dd_images": len(re.findall(r"<img ", dd_html)),
        "reddit_quotes": len(re.findall(r"reddit-quote", dd_html)),
        "section_winners": len(re.findall(r"section-winner", dd_html)),
        "comp_rows": max(0, len(re.findall(r"<tr>", comp_html)) - 1),
        "verdict_cards": len(re.findall(r"verdict-card", verdict_html)),
        "has_year_in_title": bool(re.search(r"202[4-9]", seo.get("title", ""))),
        "title_len": len(seo.get("title", "")),
        "meta_desc_len": len(seo.get("metaDescription", "")),
        "modified_time": seo.get("modifiedTime", "")[:10],
        "has_og_image": bool(seo.get("ogImage", "").strip()),
    }

    # --- Photo alt text quality ---
    photo_alts = re.findall(r'alt="([^"]*)"', photo_html)
    generic_alt = sum(1 for a in photo_alts if len(a) < 10 or a.lower() in ("image", "photo", "picture", ""))
    metrics["generic_photo_alts"] = generic_alt

    # --- Deep-dive image alt quality ---
    dd_alts = re.findall(r'alt="([^"]*)"', dd_html)
    dd_generic_alt = sum(1 for a in dd_alts if len(a) < 10 or a.lower() in ("image", "photo", "picture", ""))
    metrics["generic_dd_alts"] = dd_generic_alt

    # --- FAQ answer quality ---
    short_faq_answers = sum(1 for faq in faq_items if len(faq.get("answer", "")) < BENCHMARKS["faq_answer_min_len"])
    metrics["short_faq_answers"] = short_faq_answers

    # --- Verdict text quality ---
    verdict_text = re.sub(r"<[^>]+>", " ", verdict_html)
    verdict_text = re.sub(r"\s+", " ", verdict_text).strip()
    metrics["verdict_text_len"] = len(verdict_text)
    metrics["has_verdict_takeaways"] = bool(re.search(r"verdict-takeaways", verdict_html))

    # --- Check for placeholder/template text ---
    placeholder_patterns = [
        r"better if you want\s*\.",
        r"<li><strong>Choose [^:]+:</strong>\s*</li>",
        r'<div class="verdict-card">\s*<h3>[^<]+</h3>\s*<p>\s*</p>\s*</div>',
        r"Who this matters for:</strong>[^<]* between\s+and\s+\.",
        r"\[TODO\]",
        r"\[INSERT\]",
        r"\[PLACEHOLDER\]",
    ]
    placeholders = []
    all_html = verdict_html + dd_html + comp_html
    for pat in placeholder_patterns:
        if re.search(pat, all_html, re.I):
            placeholders.append(pat)
    metrics["placeholder_count"] = len(placeholders)

    # --- Score calculation ---
    issues = []
    score = 100  # Start at 100, deduct for issues

    # Critical issues (10 points each)
    if metrics["verdict_cards"] == 0:
        issues.append("NO_VERDICT_CARDS")
        score -= 10
    if metrics["reddit_quotes"] == 0:
        issues.append("NO_REDDIT_QUOTES")
        score -= 10
    if metrics["dd_images"] == 0:
        issues.append("NO_DD_IMAGES")
        score -= 10
    if metrics["placeholder_count"] > 0:
        issues.append(f"PLACEHOLDERS({metrics['placeholder_count']})")
        score -= 15

    # Medium issues (5 points each)
    if metrics["deep_dives"] < BENCHMARKS["deep_dives_min"]:
        issues.append(f"LOW_DEEP_DIVES({metrics['deep_dives']})")
        score -= 5
    if metrics["section_winners"] < BENCHMARKS["section_winners_min"]:
        issues.append(f"LOW_SECTION_WINNERS({metrics['section_winners']})")
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

    # Minor issues (2 points each)
    if metrics["generic_photo_alts"] > 0:
        issues.append(f"GENERIC_PHOTO_ALTS({metrics['generic_photo_alts']})")
        score -= 2
    if metrics["generic_dd_alts"] > 0:
        issues.append(f"GENERIC_DD_ALTS({metrics['generic_dd_alts']})")
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

    metrics["score"] = max(0, score)
    metrics["issues"] = issues
    metrics["tier"] = (
        "A" if score >= 90 else
        "B" if score >= 70 else
        "C" if score >= 50 else
        "D"
    )

    return metrics


def load_all() -> list[dict]:
    results = []
    for f in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        results.append(audit_page(data))
    return results


def print_summary(results: list[dict]) -> None:
    total = len(results)
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
    print(f"  Min:    {min(scores)}  ({[r['slug'] for r in results if r['score'] == min(scores)][0]})")
    print(f"  Max:    {max(scores)}  ({[r['slug'] for r in results if r['score'] == max(scores)][0]})")

    # Issue frequency
    issue_counts = Counter()
    for r in results:
        for issue in r["issues"]:
            # Strip the parenthetical detail
            base = re.sub(r"\(.*\)", "", issue)
            issue_counts[base] += 1

    print(f"\nISSUE FREQUENCY:")
    for issue, count in issue_counts.most_common():
        pct = count / total * 100
        print(f"  {issue:<25} {count:>5} ({pct:5.1f}%)")

    # Biggest wins (what to fix to move the most pages up)
    print(f"\nIMPACT ANALYSIS (fixing these moves the most pages to Tier A):")
    # Calculate how many pages would jump to A if each issue were fixed
    for issue_base in ["NO_VERDICT_CARDS", "NO_REDDIT_QUOTES", "NO_DD_IMAGES"]:
        would_fix = sum(1 for r in results if r["tier"] != "A" and issue_base in r["issues"]
                        and r["score"] + 10 >= 90)
        print(f"  Fix {issue_base}: {would_fix} pages would reach Tier A")


def print_full_report(results: list[dict]) -> None:
    print_summary(results)

    # Bottom 20 pages
    worst = sorted(results, key=lambda r: r["score"])[:20]
    print(f"\n{'='*60}")
    print("BOTTOM 20 PAGES:")
    print(f"{'='*60}")
    for r in worst:
        print(f"\n  {r['slug']} (score: {r['score']}, tier: {r['tier']})")
        print(f"    {r['dest1']} vs {r['dest2']}")
        print(f"    Issues: {', '.join(r['issues'])}")
        print(f"    Deep-dives: {r['deep_dives']}  FAQ: {r['faq_items']}  "
              f"Reddit quotes: {r['reddit_quotes']}  DD images: {r['dd_images']}  "
              f"Verdict cards: {r['verdict_cards']}")

    # Tier A pages (the ones to aspire to)
    tier_a = [r for r in results if r["tier"] == "A"]
    if tier_a:
        print(f"\n{'='*60}")
        print(f"TIER A PAGES ({len(tier_a)} total):")
        print(f"{'='*60}")
        for r in sorted(tier_a, key=lambda r: r["score"], reverse=True)[:20]:
            print(f"  {r['slug']} (score: {r['score']}) — "
                  f"quotes:{r['reddit_quotes']} imgs:{r['dd_images']} vcards:{r['verdict_cards']}")


def print_csv(results: list[dict]) -> None:
    fields = [
        "slug", "dest1", "dest2", "score", "tier",
        "deep_dives", "faq_items", "toc_items", "photo_count",
        "dd_images", "reddit_quotes", "section_winners", "comp_rows",
        "verdict_cards", "has_verdict_takeaways", "placeholder_count",
        "short_faq_answers", "generic_photo_alts", "generic_dd_alts",
        "title_len", "meta_desc_len", "modified_time", "issues",
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
