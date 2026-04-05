#!/usr/bin/env python3
"""Bulk fix audit issues directly in compare HTML files and JSON data."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "compare-data"
API_DIR = REPO_ROOT / "api" / "v1" / "compare"
COMPARE_DIR = REPO_ROOT / "compare"


def load_json(p: Path):
    return json.loads(p.read_text("utf-8"))


def write_json(p: Path, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", "utf-8")


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def strip_a_tags(text: str) -> str:
    """Remove <a> tags but keep inner text."""
    return re.sub(r"<a\b[^>]*>(.*?)</a>", r"\1", text)


PUBLISHER_LOGO = {
    "@type": "ImageObject",
    "url": "https://img.tabiji.ai/apple-touch-icon.png",
}


# ---------------------------------------------------------------------------
# Fix 1: Broken budget meta descriptions in HTML
# ---------------------------------------------------------------------------
def fix_budget_meta_html(html: str, dest1: str, dest2: str) -> tuple[str, bool]:
    meta_match = re.search(r'(content=")(.*?)("\s*name="description")', html)
    if not meta_match:
        return html, False
    meta = meta_match.group(2)

    budget_match = re.search(
        r"budgets \(\$(\d+(?:,\d+)?(?:[–-]\d+(?:,\d+)?)?),\s*\$(\d+(?:,\d+)?(?:[–-]\d+(?:,\d+)?)?)\)",
        meta,
    )
    if not budget_match:
        return html, False

    def is_broken(val: str) -> bool:
        base = re.split(r"[–-]", val)[0]
        if "," in base:
            return False
        try:
            return int(base) <= 5
        except ValueError:
            return False

    if not (is_broken(budget_match.group(1)) or is_broken(budget_match.group(2))):
        return html, False

    new_meta = (
        f"{dest1} vs {dest2} compared: costs, food, culture, and which "
        f"suits your travel style best. Updated 2026."
    )
    html = html.replace(meta_match.group(0), f'{meta_match.group(1)}{new_meta}{meta_match.group(3)}')
    return html, True


# ---------------------------------------------------------------------------
# Fix 2: HTML in JSON-LD FAQ schemas in HTML
# ---------------------------------------------------------------------------
def fix_faq_jsonld_html(html: str) -> tuple[str, bool]:
    changed = False
    # Find all JSON-LD blocks
    def fix_jsonld_block(m):
        nonlocal changed
        raw = m.group(1)
        if "<a " not in raw and "<a>" not in raw:
            return m.group(0)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # If it can't parse, try stripping HTML first
            cleaned = strip_a_tags(raw)
            try:
                data = json.loads(cleaned)
                changed = True
                return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, indent=4)}</script>'
            except json.JSONDecodeError:
                return m.group(0)

        if data.get("@type") != "FAQPage":
            return m.group(0)
        for entity in data.get("mainEntity", []):
            answer = entity.get("acceptedAnswer", {})
            text = answer.get("text", "")
            if "<a " in text or "<a>" in text:
                answer["text"] = strip_a_tags(text)
                changed = True
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, indent=4)}</script>'

    html = re.sub(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        fix_jsonld_block,
        html,
    )
    return html, changed


# ---------------------------------------------------------------------------
# Fix 3: CSS class naming in HTML
# ---------------------------------------------------------------------------
def fix_css_classes_html(html: str, dest1_slug: str, dest2_slug: str) -> tuple[str, bool]:
    changed = False
    original = html

    # --- CSS definitions ---
    # Find what edge classes are defined with --indigo (dest1) and --terracotta (dest2)
    # Common patterns: .edge-ishigaki, .edge-{city}, etc.
    css_match = re.search(r"<style>([\s\S]*?)</style>", html)
    if not css_match:
        return html, False

    css = css_match.group(1)

    # Find dest1 name (associated with --indigo) in edge classes
    indigo_edge = re.search(r"\.edge-([a-z0-9-]+)\s*\{[^}]*--indigo", css)
    terracotta_edge = re.search(r"\.edge-([a-z0-9-]+)\s*\{[^}]*--terracotta", css)

    if not indigo_edge and not terracotta_edge:
        # Check if already using dest1/dest2
        if ".edge-dest1" in css:
            return html, False
        return html, False

    old_dest1 = indigo_edge.group(1) if indigo_edge else None
    old_dest2 = terracotta_edge.group(1) if terracotta_edge else None

    # Skip if already dest1/dest2
    if old_dest1 == "dest1" and old_dest2 == "dest2":
        return html, False

    # Replace in CSS
    if old_dest1 and old_dest1 != "dest1":
        css = css.replace(f".edge-{old_dest1}", ".edge-dest1")
        css = css.replace(f".{old_dest1}-card", ".dest1-card")
        css = css.replace(f".cta-btn-{old_dest1}", ".cta-btn-dest1")
    if old_dest2 and old_dest2 != "dest2":
        css = css.replace(f".edge-{old_dest2}", ".edge-dest2")
        css = css.replace(f".{old_dest2}-card", ".dest2-card")
        css = css.replace(f".cta-btn-{old_dest2}", ".cta-btn-dest2")

    html = html.replace(css_match.group(1), css)

    # --- Body HTML ---
    # Replace edge classes in body (comparison table, deep dives)
    html = re.sub(
        rf'class="edge-{re.escape(dest1_slug)}"',
        'class="edge-dest1"',
        html,
    )
    html = re.sub(
        rf'class="edge-{re.escape(dest2_slug)}"',
        'class="edge-dest2"',
        html,
    )
    # Also handle if old_dest1/old_dest2 are used in body (non-ishigaki pages)
    if old_dest1 and old_dest1 not in ("dest1", dest1_slug):
        html = re.sub(rf'class="edge-{re.escape(old_dest1)}"', 'class="edge-dest1"', html)
    if old_dest2 and old_dest2 not in ("dest2", dest2_slug):
        html = re.sub(rf'class="edge-{re.escape(old_dest2)}"', 'class="edge-dest2"', html)

    # Replace CTA button classes
    html = re.sub(r'class="cta-btn-primary"', 'class="cta-btn-dest1"', html)
    html = re.sub(r'class="cta-btn-secondary"', 'class="cta-btn-dest2"', html)
    if old_dest1 and old_dest1 != "dest1":
        html = re.sub(rf'class="cta-btn-{re.escape(old_dest1)}"', 'class="cta-btn-dest1"', html)
    if old_dest2 and old_dest2 != "dest2":
        html = re.sub(rf'class="cta-btn-{re.escape(old_dest2)}"', 'class="cta-btn-dest2"', html)

    # Replace decision card classes
    if old_dest1 and old_dest1 != "dest1":
        html = re.sub(
            rf'class="decision-card {re.escape(old_dest1)}-card"',
            'class="decision-card dest1-card"', html,
        )
    if old_dest2 and old_dest2 != "dest2":
        html = re.sub(
            rf'class="decision-card {re.escape(old_dest2)}-card"',
            'class="decision-card dest2-card"', html,
        )

    return html, html != original


# ---------------------------------------------------------------------------
# Fix 4: Add publisher.logo to Article schema in HTML
# ---------------------------------------------------------------------------
def fix_publisher_logo_html(html: str) -> tuple[str, bool]:
    def fix_article_block(m):
        raw = m.group(1)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return m.group(0)
        if data.get("@type") != "Article":
            return m.group(0)
        publisher = data.get("publisher", {})
        if "logo" in publisher:
            return m.group(0)
        publisher["logo"] = PUBLISHER_LOGO
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, indent=4)}</script>'

    new_html = re.sub(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        fix_article_block,
        html,
        count=1,  # Article schema is always the first JSON-LD block
    )
    return new_html, new_html != html


# ---------------------------------------------------------------------------
# Fix 7: Short meta descriptions in HTML
# ---------------------------------------------------------------------------
def fix_short_meta_html(html: str, dest1: str, dest2: str) -> tuple[str, bool]:
    meta_match = re.search(r'(content=")(.*?)("\s*name="description")', html)
    if not meta_match:
        return html, False
    meta = meta_match.group(2)
    if len(meta) >= 80:
        return html, False

    if meta.lower().startswith("choosing between"):
        new_meta = (
            f"{meta} "
            f"Compare real costs, traveler reviews, and honest verdicts. Updated 2026."
        )
    elif meta.startswith("Choose "):
        new_meta = (
            f"Choosing between {dest1} and {dest2}? {meta} "
            f"Compare real costs, traveler reviews, and honest verdicts. Updated 2026."
        )
    else:
        new_meta = (
            f"{dest1} vs {dest2}: {meta} "
            f"Compare real costs, traveler reviews, and honest verdicts. Updated 2026."
        )
    html = html.replace(meta_match.group(0), f'{meta_match.group(1)}{new_meta}{meta_match.group(3)}')
    return html, True


# ---------------------------------------------------------------------------
# Also fix compare-data JSON files for consistency
# ---------------------------------------------------------------------------
def fix_json_data(data: dict) -> bool:
    changed = False

    # Fix publisher logo
    article = data.get("schema", {}).get("article", {})
    publisher = article.get("publisher", {})
    if "logo" not in publisher:
        publisher["logo"] = PUBLISHER_LOGO
        changed = True

    # Fix FAQ HTML tags
    faq = data.get("schema", {}).get("faq", {})
    for entity in faq.get("mainEntity", []):
        answer = entity.get("acceptedAnswer", {})
        text = answer.get("text", "")
        if "<a " in text or "<a>" in text:
            answer["text"] = strip_a_tags(text)
            changed = True

    return changed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def get_destinations(slug: str) -> tuple[str, str]:
    """Get destination names from API JSON or data JSON."""
    api_path = API_DIR / f"{slug}.json"
    if api_path.exists():
        data = load_json(api_path)
        return data.get("destination1", ""), data.get("destination2", "")
    data_path = DATA_DIR / f"{slug}.json"
    if data_path.exists():
        data = load_json(data_path)
        dests = data.get("destinations", {})
        return dests.get("destination1", ""), dests.get("destination2", "")
    return "", ""


def main():
    stats = {
        "budgets_fixed": 0,
        "faq_html_fixed": 0,
        "css_fixed": 0,
        "logo_added": 0,
        "short_meta_fixed": 0,
        "html_files_modified": 0,
        "json_files_modified": 0,
    }

    # Process HTML files
    html_dirs = sorted(
        [p for p in COMPARE_DIR.iterdir() if p.is_dir() and (p / "index.html").exists()]
    )
    print(f"Processing {len(html_dirs)} HTML compare pages...")

    for page_dir in html_dirs:
        slug = page_dir.name
        html_path = page_dir / "index.html"
        html = html_path.read_text("utf-8")
        modified = False

        # Skip hub pages (no "vs" in slug usually)
        if "vs" not in slug:
            continue

        dest1, dest2 = get_destinations(slug)
        if not dest1 or not dest2:
            # Try to infer from slug
            parts = slug.split("-vs-")
            if len(parts) == 2:
                dest1 = parts[0].replace("-", " ").title()
                dest2 = parts[1].replace("-", " ").title()
            else:
                continue

        dest1_slug = slugify(dest1)
        dest2_slug = slugify(dest2)

        html, fixed = fix_budget_meta_html(html, dest1, dest2)
        if fixed:
            stats["budgets_fixed"] += 1
            modified = True

        html, fixed = fix_faq_jsonld_html(html)
        if fixed:
            stats["faq_html_fixed"] += 1
            modified = True

        html, fixed = fix_css_classes_html(html, dest1_slug, dest2_slug)
        if fixed:
            stats["css_fixed"] += 1
            modified = True

        html, fixed = fix_publisher_logo_html(html)
        if fixed:
            stats["logo_added"] += 1
            modified = True

        html, fixed = fix_short_meta_html(html, dest1, dest2)
        if fixed:
            stats["short_meta_fixed"] += 1
            modified = True

        if modified:
            html_path.write_text(html, "utf-8")
            stats["html_files_modified"] += 1

    # Process JSON data files
    print(f"\nProcessing compare-data JSON files...")
    json_count = 0
    for json_path in sorted(DATA_DIR.glob("*.json")):
        data = load_json(json_path)
        if fix_json_data(data):
            write_json(json_path, data)
            json_count += 1
    stats["json_files_modified"] = json_count

    print(f"\nResults:")
    for key, val in stats.items():
        print(f"  {key}: {val}")


if __name__ == "__main__":
    main()
