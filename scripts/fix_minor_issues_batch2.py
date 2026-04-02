#!/usr/bin/env python3
"""
Fix minor issues in popular-picks/ directory:
1. Title-case cuisine-tag span contents
2. Remove competitor links (<a> tags to tripadvisor/yelp/booking), keeping inner text
3. Add missing datePublished/dateModified to Article JSON-LD schemas
"""

import json
import os
import re
import sys
from pathlib import Path

POPULAR_PICKS_DIR = Path(__file__).parent.parent / "popular-picks"

DATE_PUBLISHED = "2026-01-15"
DATE_MODIFIED = "2026-04-02"

COMPETITOR_DOMAINS = re.compile(
    r'tripadvisor\.|yelp\.com|booking\.com', re.IGNORECASE
)


def title_case(text: str) -> str:
    """Title-case a string (capitalize first letter of each word)."""
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda m: m.group(0).capitalize(), text)


def fix_cuisine_tags(html: str) -> tuple[str, int]:
    """Convert all cuisine-tag span contents to Title Case. Returns (new_html, count_changed)."""
    count = 0

    def replacer(m: re.Match) -> str:
        nonlocal count
        original = m.group(1)
        fixed = title_case(original)
        if fixed != original:
            count += 1
            return m.group(0).replace(original, fixed, 1)
        return m.group(0)

    new_html = re.sub(
        r'(<span\s+class="cuisine-tag[^"]*">)([^<]+)(</span>)',
        lambda m: m.group(1) + title_case(m.group(2)) + m.group(3)
        if title_case(m.group(2)) != m.group(2)
        else m.group(0),
        html,
    )
    # Count actual changes
    count = sum(
        1
        for orig, fixed in zip(
            re.findall(r'<span\s+class="cuisine-tag[^"]*">([^<]+)</span>', html),
            re.findall(r'<span\s+class="cuisine-tag[^"]*">([^<]+)</span>', new_html),
        )
        if orig != fixed
    )
    return new_html, count


def fix_competitor_links(html: str) -> tuple[str, int]:
    """Remove <a> tags linking to competitor sites, keeping inner text."""
    count = 0

    def replacer(m: re.Match) -> str:
        nonlocal count
        href = m.group(1)
        inner = m.group(2)
        if COMPETITOR_DOMAINS.search(href):
            count += 1
            return inner
        return m.group(0)

    # Match <a ...href="..."...>INNER</a> - inner may be simple text or nested inline html
    new_html = re.sub(
        r'<a\s[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
        replacer,
        html,
        flags=re.DOTALL,
    )
    return new_html, count


def fix_jsonld_dates(html: str) -> tuple[str, int]:
    """Add missing datePublished/dateModified to Article JSON-LD blocks."""
    count = 0

    def replacer(m: re.Match) -> str:
        nonlocal count
        script_open = m.group(1)
        json_text = m.group(2)
        script_close = m.group(3)

        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            return m.group(0)

        if data.get("@type") != "Article":
            return m.group(0)

        changed = False
        if "datePublished" not in data:
            data["datePublished"] = DATE_PUBLISHED
            changed = True
        if "dateModified" not in data:
            data["dateModified"] = DATE_MODIFIED
            changed = True

        if not changed:
            return m.group(0)

        count += 1
        # Preserve indentation style: detect leading whitespace on first key
        indent = 2
        new_json = json.dumps(data, indent=indent, ensure_ascii=False)
        return f"{script_open}{new_json}{script_close}"

    new_html = re.sub(
        r'(<script\s+type="application/ld\+json">)(.*?)(</script>)',
        replacer,
        html,
        flags=re.DOTALL,
    )
    return new_html, count


def process_file(path: Path) -> dict:
    """Process a single index.html file. Returns dict of changes made."""
    html = path.read_text(encoding="utf-8")
    original = html
    changes = {}

    html, n_cuisine = fix_cuisine_tags(html)
    if n_cuisine:
        changes["cuisine_tags"] = n_cuisine

    html, n_links = fix_competitor_links(html)
    if n_links:
        changes["competitor_links"] = n_links

    html, n_dates = fix_jsonld_dates(html)
    if n_dates:
        changes["jsonld_dates"] = n_dates

    if html != original:
        path.write_text(html, encoding="utf-8")

    return changes


def main():
    if not POPULAR_PICKS_DIR.exists():
        print(f"ERROR: {POPULAR_PICKS_DIR} not found", file=sys.stderr)
        sys.exit(1)

    totals = {"cuisine_tags": 0, "competitor_links": 0, "jsonld_dates": 0}
    files_changed = 0

    index_files = sorted(POPULAR_PICKS_DIR.glob("*/index.html"))
    print(f"Processing {len(index_files)} files in {POPULAR_PICKS_DIR}...\n")

    for path in index_files:
        slug = path.parent.name
        changes = process_file(path)
        if changes:
            files_changed += 1
            parts = []
            if "cuisine_tags" in changes:
                parts.append(f"{changes['cuisine_tags']} cuisine tags Title-Cased")
                totals["cuisine_tags"] += changes["cuisine_tags"]
            if "competitor_links" in changes:
                parts.append(f"{changes['competitor_links']} competitor link(s) removed")
                totals["competitor_links"] += changes["competitor_links"]
            if "jsonld_dates" in changes:
                parts.append("datePublished/dateModified added")
                totals["jsonld_dates"] += changes["jsonld_dates"]
            print(f"  {slug}: {', '.join(parts)}")

    print(f"\n--- Summary ---")
    print(f"Files changed:          {files_changed}")
    print(f"Cuisine tags fixed:     {totals['cuisine_tags']}")
    print(f"Competitor links removed:{totals['competitor_links']}")
    print(f"JSON-LD dates added:    {totals['jsonld_dates']}")


if __name__ == "__main__":
    main()
