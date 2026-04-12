#!/usr/bin/env python3
"""
Fix three issues on compare pages:
1. Add responsive image sizes attributes to <img> tags
2. Fix outdated methodology dates (late 2023 / early 2024 -> early 2026)
3. Improve Croatia-vs-Montenegro title and meta description
"""

import os
import re
import glob

COMPARE_DIR = "/Users/bjh/Documents/tabiji/compare"
MIN_FILE_SIZE = 1000  # skip redirect stubs

# ── Counters ──
img_files_modified = 0
img_photo_grid_added = 0
img_section_added = 0
date_files_modified = 0
date_replacements = 0
croatia_modified = False


def add_sizes_to_images(content, filepath):
    """Add sizes attribute to <img> tags pointing to img.tabiji.ai."""
    global img_photo_grid_added, img_section_added

    photo_grid_count = 0
    section_count = 0

    # Build a set of character positions that are inside <div class="photo-grid"> blocks.
    # The photo-grid div contains the two destination images and closes with </div>.
    photo_grid_ranges = []
    for m in re.finditer(r'<div class="photo-grid">', content):
        start = m.start()
        # Find the matching closing: photo-grid contains two child <div>s,
        # so we look for the pattern </div>\n</div> or </img></div>\n</div>
        # Simpler: find the next </div> that closes the photo-grid (3rd </div> after start)
        # Actually, the structure is: <div class="photo-grid">\n<div>\n<img>...\n</div>\n<div>\n<img>...\n</div>\n</div>
        # Let's just find a generous end: next 1000 chars should be enough
        end = content.find('</div>\n</div>\n', start)
        if end == -1:
            end = content.find('</div></div>', start)
        if end == -1:
            # Fallback: just use 800 chars after start
            end = start + 800
        else:
            end += 20  # include the closing tags
        photo_grid_ranges.append((start, end))

    def is_in_photo_grid(pos):
        for start, end in photo_grid_ranges:
            if start <= pos <= end:
                return True
        return False

    def replace_img(match):
        nonlocal photo_grid_count, section_count
        tag = match.group(0)

        # Skip if already has sizes
        if 'sizes=' in tag:
            return tag

        # Only process img.tabiji.ai images
        if 'img.tabiji.ai' not in tag:
            return tag

        # Skip logo/icon images (not content images)
        if 'tabiji-owl-logo' in tag or 'apple-touch-icon' in tag or 'icon-192' in tag:
            return tag

        src_match = re.search(r'src="([^"]*)"', tag)
        if not src_match:
            return tag

        src = src_match.group(1)

        # Only process compare content images
        if '/compare/' not in src:
            return tag

        # Determine which sizes value to use based on context
        if '/dest1.jpg' in src or '/dest2.jpg' in src or is_in_photo_grid(match.start()):
            # Photo-grid images (either dest1/dest2 or inside photo-grid div)
            sizes_val = '(max-width: 768px) 100vw, 50vw'
            photo_grid_count += 1
        else:
            # Section images (named images like plitvice.jpg, sveti-stefan.jpg, etc.)
            sizes_val = '(max-width: 768px) 100vw, 65vw'
            section_count += 1

        # Insert sizes attribute before the closing > or />
        if tag.endswith('/>'):
            new_tag = tag[:-2].rstrip() + f' sizes="{sizes_val}" />'
        elif tag.endswith('>'):
            new_tag = tag[:-1].rstrip() + f' sizes="{sizes_val}">'
        else:
            new_tag = tag

        return new_tag

    new_content = re.sub(r'<img\b[^>]*>', replace_img, content)

    img_photo_grid_added += photo_grid_count
    img_section_added += section_count

    return new_content, (photo_grid_count + section_count) > 0


def fix_methodology_dates(content, filepath):
    """Fix outdated dates in methodology sections."""
    global date_replacements

    count = 0

    # We need to be careful to only replace dates near methodology context.
    # All the patterns appear within <li> tags inside methodology-points sections,
    # or in FAQ sections about exchange rates.
    #
    # Strategy: find lines containing "Verified" or methodology context and replace there.
    # Also handle broader patterns that appear in methodology <li> items.

    # Replacements to apply within methodology-context lines
    methodology_replacements = [
        (r'in late 2023 and early 2024', 'in early 2026'),
        (r'in November 2023-February 2024', 'in early 2026'),
        (r'in November 2023–February 2024', 'in early 2026'),
        (r'in 2023 and early 2024', 'in early 2026'),
        # "as of late 2023 / early 2024" or "as of late 2023/early 2024"
        (r'as of late 2023\s*/\s*early 2024', 'as of early 2026'),
        (r'in late 2023\s*/\s*early 2024', 'in early 2026'),
        # "as of early 2024" standalone
        (r'as of early 2024', 'as of early 2026'),
        # "in early 2024" standalone
        (r'in early 2024', 'in early 2026'),
        # "in late 2023" standalone
        (r'in late 2023', 'in early 2026'),
        # Parenthesized: "(early 2024)" -> "(early 2026)"
        (r'\(early 2024\)', '(early 2026)'),
        # "reflecting early 2024 prices" -> "reflecting early 2026 prices"
        (r'early 2024 prices', 'early 2026 prices'),
        # Q4 2023 / Q1 2024 patterns
        (r'(?:for |in )Q4 2023\s*/\s*Q1 2024(?:\s*pricing)?', 'in early 2026'),
        (r'(?:for |in )Q1 2024(?:\s*data)?', 'in early 2026'),
        (r'Q4 2023\s*/\s*Q1 2024', 'early 2026'),
        (r'Q[34]/Q[14] 2024', 'early 2026'),
        (r'Q1 2024', 'early 2026'),
    ]

    # Only apply within methodology-relevant lines:
    # Lines containing "Verified" in methodology context
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        # Check if this line is in a methodology context
        is_methodology = (
            'Verified costs' in line or
            'Verified current costs' in line or
            ('Verified' in line and 'booking platform' in line) or
            ('Verified' in line and 'logistics' in line) or
            ('Verified' in line and 'traveler report' in line) or
            ('Verified' in line and 'Skyscanner' in line) or
            ('Verified' in line and 'Booking.com' in line) or
            ('Verified' in line and 'Agoda' in line)
        )

        if is_methodology:
            new_line = line
            for pattern, replacement in methodology_replacements:
                new_line, n = re.subn(pattern, replacement, new_line)
                count += n
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    new_content = '\n'.join(new_lines)

    # Also handle FAQ exchange rate date references that appear outside methodology
    # These are "(as of late 2023/early 2024)" or "As of late 2023" in FAQ sections
    # about exchange rates and visa info -- also outdated given 2026 page dates
    faq_patterns = [
        (r'\(as of late 2023/early 2024\)', '(as of early 2026)'),
        (r'\(as of late 2023 / early 2024\)', '(as of early 2026)'),
        (r'As of late 2023/early 2024', 'As of early 2026'),
        (r'As of early 2024', 'As of early 2026'),
        (r'As of late 2023', 'As of early 2026'),
        (r'as of late 2023', 'as of early 2026'),
    ]
    for pattern, replacement in faq_patterns:
        new_content, n = re.subn(pattern, replacement, new_content)
        count += n

    date_replacements += count
    return new_content, count > 0


def fix_croatia_montenegro(content):
    """Fix title and meta description for Croatia vs Montenegro page."""
    new_title = "Croatia vs Montenegro: Beaches, Costs &amp; Honest Verdict (2026)"
    new_desc = "Montenegro costs 40% less but Croatia has better beaches and food. We compared costs, weather, nightlife, and day trips — here&#x27;s who wins each category."
    new_og_title = "Croatia vs Montenegro: Beaches, Costs &amp; Honest Verdict — tabiji.ai"
    new_twitter_title = "Croatia vs Montenegro: Beaches, Costs &amp; Honest Verdict"

    # Replace <title>
    content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{new_title}</title>',
        content,
        count=1
    )

    # Replace meta description
    content = re.sub(
        r'(<meta content=")[^"]*(" name="description"/>)',
        rf'\g<1>{new_desc}\2',
        content,
        count=1
    )

    # Replace og:title
    content = re.sub(
        r'(<meta content=")[^"]*(" property="og:title"/>)',
        rf'\g<1>{new_og_title}\2',
        content,
        count=1
    )

    # Replace twitter:title
    content = re.sub(
        r'(<meta content=")[^"]*(" name="twitter:title"/>)',
        rf'\g<1>{new_twitter_title}\2',
        content,
        count=1
    )

    return content


def process_file(filepath):
    global img_files_modified, date_files_modified, croatia_modified

    # Skip small files (redirect stubs)
    if os.path.getsize(filepath) < MIN_FILE_SIZE:
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    modified = False

    # Issue 1: Add sizes to images
    content, img_changed = add_sizes_to_images(content, filepath)
    if img_changed:
        img_files_modified += 1
        modified = True

    # Issue 2: Fix methodology dates
    content, date_changed = fix_methodology_dates(content, filepath)
    if date_changed:
        date_files_modified += 1
        modified = True

    # Issue 3: Croatia-vs-Montenegro meta fix
    if filepath.endswith('croatia-vs-montenegro/index.html'):
        content = fix_croatia_montenegro(content)
        croatia_modified = True
        modified = True

    if modified and content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    # Find all compare page index.html files
    pattern = os.path.join(COMPARE_DIR, '*/index.html')
    files = sorted(glob.glob(pattern))

    print(f"Found {len(files)} compare page files")

    for filepath in files:
        process_file(filepath)

    print()
    print("=== Issue 1: Responsive image sizes ===")
    print(f"  Files modified: {img_files_modified}")
    print(f"  Photo-grid sizes added (dest1/dest2): {img_photo_grid_added}")
    print(f"  Section image sizes added: {img_section_added}")
    print(f"  Total sizes attributes added: {img_photo_grid_added + img_section_added}")
    print()
    print("=== Issue 2: Methodology date fixes ===")
    print(f"  Files modified: {date_files_modified}")
    print(f"  Date replacements made: {date_replacements}")
    print()
    print("=== Issue 3: Croatia-vs-Montenegro meta ===")
    print(f"  Modified: {croatia_modified}")
    print()
    print(f"Total files touched: {len(set(range(img_files_modified)) | set(range(date_files_modified))) if img_files_modified or date_files_modified else 0}")


if __name__ == '__main__':
    main()
