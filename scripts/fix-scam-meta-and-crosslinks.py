#!/usr/bin/env python3
"""
Fix three issues on scam pages:
1. Add og:image:width and og:image:height after og:image meta tags
2. Add publisher logo to Article schema JSON-LD
3. Add cross-links to popular-picks for matching cities
"""
import os
import re
import json
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAMS_DIR = os.path.join(BASE, "scams")
PP_DIR = os.path.join(BASE, "popular-picks")

# ── Build popular-picks lookup: city_slug -> sorted list of pp slugs ──
def build_pp_lookup():
    """Map each city slug to its matching popular-picks slugs."""
    if not os.path.isdir(PP_DIR):
        return {}
    all_pp = sorted(
        d for d in os.listdir(PP_DIR)
        if os.path.isdir(os.path.join(PP_DIR, d))
    )
    # Collect all scam city slugs
    scam_slugs = set()
    for d in os.listdir(SCAMS_DIR):
        full = os.path.join(SCAMS_DIR, d, "index.html")
        if os.path.isfile(full) and d != "country":
            scam_slugs.add(d)

    lookup = {}
    for slug in scam_slugs:
        prefix = slug + "-"
        matches = [pp for pp in all_pp if pp.startswith(prefix)]
        if matches:
            lookup[slug] = matches[:6]  # max 6 alphabetically (already sorted)
    return lookup


def slug_to_title(slug):
    """Convert a slug like 'hong-kong-dim-sum' to 'Hong Kong Dim Sum'."""
    return " ".join(w.capitalize() for w in slug.split("-"))


def city_name_from_slug(slug):
    """Extract city name from scam slug. e.g. 'hong-kong' -> 'Hong Kong'."""
    return " ".join(w.capitalize() for w in slug.split("-"))


# ── Issue 1: Add og:image:width and og:image:height ──
def fix_og_image_dimensions(content):
    """Insert og:image:width and og:image:height after og:image line if missing."""
    if 'og:image:width' in content:
        return content, False

    lines = content.split("\n")
    new_lines = []
    changed = False
    for line in lines:
        new_lines.append(line)
        if 'property="og:image"' in line and 'og:image:width' not in line:
            # Detect indentation of the og:image line
            indent = ""
            for ch in line:
                if ch in (" ", "\t"):
                    indent += ch
                else:
                    break
            new_lines.append(f'{indent}<meta property="og:image:width" content="1200">')
            new_lines.append(f'{indent}<meta property="og:image:height" content="630">')
            changed = True
    return "\n".join(new_lines), changed


# ── Issue 2: Add publisher logo to JSON-LD ──
def fix_publisher_logo(content):
    """Add logo ImageObject to publisher block in JSON-LD."""
    if '"ImageObject"' in content:
        return content, False

    # Match the multi-line publisher block (4-line indented form):
    #     "publisher": {
    #         "@type": "Organization",
    #         "name": "tabiji.ai",
    #         "url": "https://tabiji.ai/"
    #     },
    pattern_multiline = re.compile(
        r'("publisher":\s*\{\s*\n'
        r'(\s*)"@type":\s*"Organization",\s*\n'
        r'\s*"name":\s*"tabiji\.ai",\s*\n'
        r'\s*"url":\s*"https://tabiji\.ai/"\s*\n'
        r'\s*\})',
        re.MULTILINE
    )

    def replace_multiline(m):
        full = m.group(0)
        indent = m.group(2)  # indentation of @type line
        # Replace closing "}" with added logo
        old_close = full.rstrip().rstrip(",")
        # Find where the closing } is
        new_block = full.replace(
            '"url": "https://tabiji.ai/"\n' + indent[:-4] + '}',  # won't always match
            '"url": "https://tabiji.ai/",\n'
            + indent + '"logo": {\n'
            + indent + '    "@type": "ImageObject",\n'
            + indent + '    "url": "https://img.tabiji.ai/tabiji-owl-logo.png"\n'
            + indent + '}\n'
            + indent[:-4] + '}'
        )
        # If the simple replace didn't work, try a regex approach
        if new_block == full:
            # Use a more flexible approach
            new_block = re.sub(
                r'("url":\s*"https://tabiji\.ai/")\s*\n(\s*)\}',
                r'\1,\n'
                + indent + '"logo": {\n'
                + indent + '    "@type": "ImageObject",\n'
                + indent + '    "url": "https://img.tabiji.ai/tabiji-owl-logo.png"\n'
                + r'\2}',
                full
            )
        return new_block

    new_content, count = pattern_multiline.subn(replace_multiline, content)
    if count > 0:
        return new_content, True

    # Also handle compact single-line form in country pages:
    # "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai/"}
    pattern_compact = re.compile(
        r'"publisher":\s*\{"@type":\s*"Organization",\s*"name":\s*"tabiji\.ai",\s*"url":\s*"https://tabiji\.ai/"\}'
    )

    def replace_compact(m):
        return (
            '"publisher": {"@type": "Organization", "name": "tabiji.ai", '
            '"url": "https://tabiji.ai/", '
            '"logo": {"@type": "ImageObject", "url": "https://img.tabiji.ai/tabiji-owl-logo.png"}}'
        )

    new_content, count = pattern_compact.subn(replace_compact, content)
    if count > 0:
        return new_content, True

    return content, False


# ── Issue 3: Add popular-picks cross-links ──
def fix_crosslinks(content, city_slug, pp_slugs):
    """Add popular-picks links inside related-section, before 'Popular Nearby Destinations' h3."""
    if not pp_slugs:
        return content, False

    # Check if already has Popular Picks section
    if "Popular Picks in" in content:
        return content, False

    city_name = city_name_from_slug(city_slug)

    # Build the HTML block
    links = []
    for slug in pp_slugs:
        title = slug_to_title(slug)
        links.append(f'    <a href="/popular-picks/{slug}/" class="related-card">{title}</a>')
    links_html = "\n".join(links)

    pp_block = (
        f'<h3 style="font-size:0.78rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.08em;color:var(--text-muted);margin:1rem 0 0.5rem;">'
        f'Popular Picks in {city_name}</h3>\n'
        f'<div class="related-grid">\n'
        f'{links_html}\n'
        f'</div>\n'
    )

    # Try to insert before "Popular Nearby Destinations" h3
    nearby_pattern = re.compile(
        r'(<h3[^>]*>Popular Nearby Destinations</h3>)'
    )
    m = nearby_pattern.search(content)
    if m:
        # Find indentation of the nearby h3
        line_start = content.rfind("\n", 0, m.start()) + 1
        existing_indent = ""
        for ch in content[line_start:m.start()]:
            if ch in (" ", "\t"):
                existing_indent += ch
            else:
                break

        # Build indented block: h3, div.related-grid, links, /div
        indented_lines = []
        for line in pp_block.split("\n"):
            if line.strip():
                indented_lines.append(existing_indent + line)
            # skip empty lines
        indented_block = "\n".join(indented_lines) + "\n"

        # Insert at line_start (before the whitespace+h3 line)
        new_content = content[:line_start] + indented_block + content[line_start:]
        return new_content, True

    # Fallback: insert before closing </div> of related-section
    # Find <div class="related-section"> and its closing </div>
    rs_match = re.search(r'<div\s+class="related-section">', content)
    if rs_match:
        # Find the last </div> before the next major section
        # Simple approach: insert before the closing </div> of related-section
        # We look for the pattern: </div>\n    </div> (closing related-grid then related-section)
        # Actually, let's find the end more carefully
        # The related-section div closes, then there's usually a CTA or similar
        close_pattern = re.compile(r'(\s*</div>\s*\n\s*\n\s*<!-- CTA)', re.MULTILINE)
        cm = close_pattern.search(content, rs_match.start())
        if cm:
            insert_pos = cm.start()
            indented_block = "\n".join(
                "        " + line if line.strip() else line
                for line in pp_block.split("\n")
            )
            indented_block = indented_block.rstrip() + "\n"
            new_content = content[:insert_pos] + "\n" + indented_block + content[insert_pos:]
            return new_content, True

    return content, False


def validate_json_ld(content):
    """Extract and validate JSON-LD blocks from HTML content."""
    pattern = re.compile(
        r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>',
        re.DOTALL
    )
    for m in pattern.finditer(content):
        try:
            json.loads(m.group(1))
        except json.JSONDecodeError as e:
            return False, str(e), m.group(1)[:200]
    return True, None, None


def main():
    pp_lookup = build_pp_lookup()

    # Collect all scam page paths (city + country)
    city_pages = sorted(glob.glob(os.path.join(SCAMS_DIR, "*/index.html")))
    country_pages = sorted(glob.glob(os.path.join(SCAMS_DIR, "country/*/index.html")))

    # Remove country/* from city_pages (glob might not pick them up anyway with single *)
    city_pages = [p for p in city_pages if "/country/" not in p]

    all_pages = city_pages + country_pages

    stats = {
        "og_image_dims_added": 0,
        "publisher_logo_added": 0,
        "crosslinks_added": 0,
        "crosslinks_total_links": 0,
        "files_modified": 0,
        "json_ld_errors": [],
        "total_city_pages": len(city_pages),
        "total_country_pages": len(country_pages),
    }

    for filepath in all_pages:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original = content
        is_city = "/country/" not in filepath

        # Issue 1: og:image dimensions (city pages only -- country pages don't have og:image)
        og_changed = False
        if is_city:
            content, og_changed = fix_og_image_dimensions(content)
            if og_changed:
                stats["og_image_dims_added"] += 1

        # Issue 2: publisher logo (both city and country pages have publisher)
        content, logo_changed = fix_publisher_logo(content)
        if logo_changed:
            stats["publisher_logo_added"] += 1

        # Issue 3: crosslinks (city pages only)
        cross_changed = False
        if is_city:
            # Extract slug from path
            slug = os.path.basename(os.path.dirname(filepath))
            pp_slugs = pp_lookup.get(slug, [])
            if pp_slugs:
                content, cross_changed = fix_crosslinks(content, slug, pp_slugs)
                if cross_changed:
                    stats["crosslinks_added"] += 1
                    stats["crosslinks_total_links"] += len(pp_slugs)

        # Write if changed
        if content != original:
            # Validate JSON-LD before writing
            valid, err, snippet = validate_json_ld(content)
            if not valid:
                stats["json_ld_errors"].append((filepath, err, snippet))
                print(f"  JSON-LD ERROR in {filepath}: {err}")
                print(f"  Snippet: {snippet}")
                continue

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            stats["files_modified"] += 1

    # Print report
    print("=" * 60)
    print("Scam Pages Fix Report")
    print("=" * 60)
    print(f"Total city pages processed:    {stats['total_city_pages']}")
    print(f"Total country pages processed: {stats['total_country_pages']}")
    print(f"Files modified:                {stats['files_modified']}")
    print()
    print(f"Issue 1 - og:image dimensions added:  {stats['og_image_dims_added']}")
    print(f"Issue 2 - Publisher logo added:        {stats['publisher_logo_added']}")
    print(f"Issue 3 - Cross-links added:           {stats['crosslinks_added']} pages ({stats['crosslinks_total_links']} total links)")
    print()
    if stats["json_ld_errors"]:
        print(f"JSON-LD validation errors: {len(stats['json_ld_errors'])}")
        for path, err, _ in stats["json_ld_errors"]:
            print(f"  {path}: {err}")
    else:
        print("JSON-LD validation: All OK")
    print()

    # Show which cities got crosslinks
    if pp_lookup:
        matched_cities = sorted(pp_lookup.keys())
        print(f"Cities with popular-picks matches: {len(matched_cities)}")
        for city in matched_cities[:10]:
            print(f"  {city}: {len(pp_lookup[city])} links")
        if len(matched_cities) > 10:
            print(f"  ... and {len(matched_cities) - 10} more")


if __name__ == "__main__":
    main()
