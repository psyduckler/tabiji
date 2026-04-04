#!/usr/bin/env python3
"""Find and fix broken popular-picks links in compare pages.

Checks each compare page for links to /popular-picks/ pages that don't exist,
and either removes the broken link or replaces with a valid alternative.
"""

import os
import re
import glob

PICKS_DIR = os.path.expanduser("~/tabiji/popular-picks")
COMPARE_DIR = os.path.expanduser("~/tabiji/compare")

# Build set of valid popular-picks slugs
valid_picks = set()
for page in glob.glob(os.path.join(PICKS_DIR, "*/index.html")):
    slug = os.path.basename(os.path.dirname(page))
    valid_picks.add(slug)

print(f"Found {len(valid_picks)} valid popular-picks pages")

# Check compare pages for broken links
broken_count = 0
fixed_count = 0

for page in sorted(glob.glob(os.path.join(COMPARE_DIR, "*/index.html"))):
    with open(page, "r") as f:
        content = f.read()
    
    # Find all popular-picks links
    links = re.findall(r'href="/popular-picks/([^/"]+)/"', content)
    if not links:
        continue
    
    dirname = os.path.basename(os.path.dirname(page))
    modified = False
    
    for link_slug in links:
        if link_slug not in valid_picks:
            broken_count += 1
            # Remove the broken link (the <a> tag containing it)
            # Pattern: <a href="/popular-picks/SLUG/">TEXT</a>
            pattern = rf'<a[^>]*href="/popular-picks/{re.escape(link_slug)}/"[^>]*>[^<]*</a>'
            new_content = re.sub(pattern, '', content)
            if new_content != content:
                content = new_content
                modified = True
                fixed_count += 1
    
    if modified:
        with open(page, "w") as f:
            f.write(content)

print(f"Found {broken_count} broken links, fixed {fixed_count}")
