#!/usr/bin/env python3
"""
Fix two issues on compare pages:
1. Remove broken <a > tags (no href) from TOC in 5 specific files
2. Wrap <div class="article-content"> in <main> tags across all compare pages
"""

import glob
import re

COMPARE_DIR = "/Users/bjh/Documents/tabiji/compare"

# ── Issue 1: Remove broken TOC links ──────────────────────────────────────────

BROKEN_TOC_FILES = [
    f"{COMPARE_DIR}/south-africa-vs-kenya/index.html",
    f"{COMPARE_DIR}/seoul-vs-taipei/index.html",
    f"{COMPARE_DIR}/penang-vs-ipoh/index.html",
    f"{COMPARE_DIR}/osaka-vs-fukuoka/index.html",
    f"{COMPARE_DIR}/cartagena-vs-havana/index.html",
]

print("=" * 60)
print("Issue 1: Removing broken TOC links (no href)")
print("=" * 60)

toc_fixed = 0
for filepath in BROKEN_TOC_FILES:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match <li><a >...</a></li> or <li><a  ...>...</a></li> (anchor with no href)
    # Pattern: <li> with optional whitespace, then <a followed by > or space+>,
    # then content, then </a>, then optional whitespace, then </li>
    original = content
    content = re.sub(
        r'<li>\s*<a\s+>.*?</a>\s*</li>\n?',
        '',
        content
    )
    # Also handle the variant with extra spaces: <a  >
    content = re.sub(
        r'<li>\s*<a\s{2,}>.*?</a>\s*</li>\n?',
        '',
        content
    )

    if content != original:
        removed_count = original.count('<a >') + original.count('<a  >')
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        short = filepath.replace(COMPARE_DIR + "/", "")
        print(f"  Fixed: {short} (removed {removed_count} broken links)")
        toc_fixed += 1
    else:
        short = filepath.replace(COMPARE_DIR + "/", "")
        print(f"  Skipped (no broken links): {short}")

print(f"\nTotal files fixed for Issue 1: {toc_fixed}")

# ── Issue 2: Add <main> landmark ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("Issue 2: Adding <main> landmark to compare pages")
print("=" * 60)

all_files = sorted(glob.glob(f"{COMPARE_DIR}/*/index.html"))
print(f"Found {len(all_files)} compare page files")

main_added = 0
already_has_main = 0
skipped = 0

for filepath in all_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip files that already have a <main> tag
    if "<main>" in content or "<main " in content:
        already_has_main += 1
        continue

    original = content

    # Replace the opening tag
    content = content.replace(
        '<div class="article-content">',
        '<main>\n<div class="article-content">'
    )

    # Replace the closing tag
    content = content.replace(
        '</div><!-- /article-content -->',
        '</div><!-- /article-content -->\n</main>'
    )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        main_added += 1
    else:
        skipped += 1

print(f"  Files modified (main added): {main_added}")
print(f"  Files already had <main>:    {already_has_main}")
print(f"  Files skipped (no match):    {skipped}")
print(f"  Total files scanned:         {len(all_files)}")
print("\nDone.")
