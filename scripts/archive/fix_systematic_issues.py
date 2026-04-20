#!/usr/bin/env python3
"""
Fix systematic issues across all compare pages:
1. Title too long → remove " | tabiji.ai" suffix; if still >70 chars, shorten phrase
2. Meta description too long → truncate to ≤155 chars with ellipsis
3. Slug-title mismatch for dalat-vs-da-nang → rename directory to da-lat-vs-da-nang
   and update all internal references
"""

import os
import re
import sys
import shutil

COMPARE_DIR = os.path.expanduser("~/.openclaw/workspace/tabiji/compare")

# Hub pages to skip (not compare articles)
HUBS = {
    "asia", "australia", "bali", "cities", "colombia", "countries", "croatia",
    "culture", "egypt", "europe", "global-mixed", "greece", "hawaii", "iceland",
    "islands", "italy", "japan", "latin-america", "luxury", "maldives", "mexico",
    "middle-east-africa", "morocco", "nature", "new-zealand", "north-america",
    "oceania", "portugal", "spain", "taiwan", "thailand", "trip-style-guides", "vietnam"
}

stats = {
    "titles_fixed": 0,
    "titles_still_long": 0,
    "descs_fixed": 0,
    "og_titles_fixed": 0,
    "slug_renamed": 0,
    "files_modified": 0,
    "errors": [],
}


def fix_title(html):
    """Remove ' | tabiji.ai' from <title>. If still >70, shorten 'Which Should You Visit?' to 'Which to Visit?'"""
    changed = False

    def replace_title(m):
        nonlocal changed
        title = m.group(1)
        original = title

        # Step 1: Remove " | tabiji.ai"
        if title.endswith(" | tabiji.ai"):
            title = title[: -len(" | tabiji.ai")]

        # Step 2: If still >70 chars, shorten the phrase
        if len(title) > 70 and "Which Should You Visit?" in title:
            title = title.replace("Which Should You Visit?", "Which to Visit?")

        # Step 3: If STILL >70 chars, try removing " (2026 Comparison)"
        if len(title) > 70 and "(2026 Comparison)" in title:
            title = title.replace(" (2026 Comparison)", " (2026)")

        if title != original:
            changed = True
            stats["titles_fixed"] += 1
            if len(title) > 70:
                stats["titles_still_long"] += 1
        return f"<title>{title}</title>"

    html = re.sub(r"<title>([^<]+)</title>", replace_title, html)
    return html, changed


def fix_og_title(html):
    """Remove ' — tabiji.ai' from og:title"""
    changed = False

    def replace_og(m):
        nonlocal changed
        prefix = m.group(1)
        content = m.group(2)
        suffix = m.group(3)
        original = content

        if content.endswith(" — tabiji.ai"):
            content = content[: -len(" — tabiji.ai")]
        elif content.endswith(" - tabiji.ai"):
            content = content[: -len(" - tabiji.ai")]

        if content != original:
            changed = True
            stats["og_titles_fixed"] += 1
        return f'{prefix}"{content}"{suffix}'

    html = re.sub(
        r'(<meta content=")([^"]+)(" property="og:title"/>)',
        replace_og,
        html,
    )
    return html, changed


def fix_meta_description(html):
    """Truncate meta descriptions to ≤155 chars"""
    changed = False

    def replace_desc(m):
        nonlocal changed
        prefix = m.group(1)
        desc = m.group(2)
        suffix = m.group(3)

        if len(desc) <= 155:
            return m.group(0)

        # Truncate at last sentence boundary or word boundary before 152 chars
        truncated = desc[:152]

        # Try to cut at last period
        last_period = truncated.rfind(".")
        if last_period > 100:
            truncated = truncated[: last_period + 1]
        else:
            # Cut at last space and add ellipsis
            last_space = truncated.rfind(" ")
            if last_space > 100:
                truncated = truncated[:last_space] + "..."
            else:
                truncated = truncated + "..."

        changed = True
        stats["descs_fixed"] += 1
        return f'{prefix}"{truncated}"{suffix}'

    # Match meta description tag (content before name)
    html = re.sub(
        r'(<meta content=")([^"]+)(" name="description"/>)',
        replace_desc,
        html,
    )
    return html, changed


def fix_og_description(html):
    """Also truncate og:description if >160 chars"""
    changed = False

    def replace_og_desc(m):
        nonlocal changed
        prefix = m.group(1)
        desc = m.group(2)
        suffix = m.group(3)

        if len(desc) <= 160:
            return m.group(0)

        truncated = desc[:157]
        last_space = truncated.rfind(" ")
        if last_space > 100:
            truncated = truncated[:last_space] + "..."
        else:
            truncated = truncated + "..."

        changed = True
        return f'{prefix}"{truncated}"{suffix}'

    html = re.sub(
        r'(<meta content=")([^"]+)(" property="og:description"/>)',
        replace_og_desc,
        html,
    )
    return html, changed


def process_file(slug):
    """Process a single compare page"""
    path = os.path.join(COMPARE_DIR, slug, "index.html")
    if not os.path.isfile(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html
    any_changed = False

    html, c = fix_title(html)
    any_changed = any_changed or c

    html, c = fix_og_title(html)
    any_changed = any_changed or c

    html, c = fix_meta_description(html)
    any_changed = any_changed or c

    html, c = fix_og_description(html)
    any_changed = any_changed or c

    if any_changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        stats["files_modified"] += 1


def rename_dalat():
    """Rename dalat-vs-da-nang to da-lat-vs-da-nang and update all references"""
    old_slug = "dalat-vs-da-nang"
    new_slug = "da-lat-vs-da-nang"
    old_path = os.path.join(COMPARE_DIR, old_slug)
    new_path = os.path.join(COMPARE_DIR, new_slug)

    if not os.path.exists(old_path):
        print(f"  Skipping rename: {old_slug} doesn't exist")
        return

    if os.path.exists(new_path):
        print(f"  Skipping rename: {new_slug} already exists")
        return

    # First update internal references in the file itself
    index_path = os.path.join(old_path, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Replace all URL references from old slug to new slug
    html = html.replace(f"/compare/{old_slug}/", f"/compare/{new_slug}/")
    html = html.replace(f"/compare/{old_slug}", f"/compare/{new_slug}")
    # Also fix image paths if they reference the slug
    html = html.replace(f"compare/{old_slug}/", f"compare/{new_slug}/")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Use git mv for proper tracking
    os.system(f'cd {COMPARE_DIR} && git mv "{old_slug}" "{new_slug}"')
    stats["slug_renamed"] += 1
    print(f"  Renamed {old_slug} → {new_slug}")


def main():
    print("=" * 60)
    print("Fixing systematic issues across compare pages")
    print("=" * 60)

    # Get all compare page slugs (excluding hubs)
    slugs = sorted(
        d
        for d in os.listdir(COMPARE_DIR)
        if os.path.isdir(os.path.join(COMPARE_DIR, d))
        and d not in HUBS
        and os.path.isfile(os.path.join(COMPARE_DIR, d, "index.html"))
    )
    print(f"Found {len(slugs)} compare pages to process")

    # Step 1: Rename dalat slug BEFORE processing files
    print("\n--- Step 1: Slug rename ---")
    rename_dalat()

    # Refresh slugs list after rename
    slugs = sorted(
        d
        for d in os.listdir(COMPARE_DIR)
        if os.path.isdir(os.path.join(COMPARE_DIR, d))
        and d not in HUBS
        and os.path.isfile(os.path.join(COMPARE_DIR, d, "index.html"))
    )

    # Step 2: Fix titles and meta descriptions
    print("\n--- Step 2: Fix titles and meta descriptions ---")
    for i, slug in enumerate(slugs):
        try:
            process_file(slug)
        except Exception as e:
            stats["errors"].append(f"{slug}: {e}")
        if (i + 1) % 200 == 0:
            print(f"  Processed {i + 1}/{len(slugs)}...")

    print(f"  Processed {len(slugs)}/{len(slugs)}")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Titles fixed: {stats['titles_fixed']}")
    print(f"  Titles still >70 chars after fix: {stats['titles_still_long']}")
    print(f"  OG titles fixed: {stats['og_titles_fixed']}")
    print(f"  Meta descriptions truncated: {stats['descs_fixed']}")
    print(f"  Slug renamed: {stats['slug_renamed']}")
    print(f"  Total files modified: {stats['files_modified']}")
    if stats["errors"]:
        print(f"  Errors: {len(stats['errors'])}")
        for e in stats["errors"][:10]:
            print(f"    {e}")


if __name__ == "__main__":
    main()
