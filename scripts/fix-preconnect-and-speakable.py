#!/usr/bin/env python3
"""
Fix two issues across the tabiji.ai site:

1. Add <link rel="preconnect" href="https://img.tabiji.ai"> to every HTML page
   that doesn't already have it (skipping redirect stubs < 900 bytes).

2. Replace ".hero .subtitle" with ".hero p" in speakable JSON-LD on compare pages.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRECONNECT_TAG = '<link rel="preconnect" href="https://img.tabiji.ai">'

# ---------------------------------------------------------------------------
# Counters
# ---------------------------------------------------------------------------
preconnect_added = 0
preconnect_skipped_already = 0
preconnect_skipped_redirect = 0
preconnect_skipped_no_head = 0
speakable_fixed = 0
speakable_already_ok = 0

# ---------------------------------------------------------------------------
# Collect every index.html under ROOT (except hidden dirs, scripts, assets)
# ---------------------------------------------------------------------------
SKIP_DIRS = {'.git', '.github', 'node_modules', 'scripts', 'assets', '.claude',
             '_templates', '__pycache__', 'data'}

html_files = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    # Prune irrelevant directories
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if fn.endswith('.html'):
            html_files.append(os.path.join(dirpath, fn))

html_files.sort()
print(f"Found {len(html_files)} HTML files to process.\n")

# ---------------------------------------------------------------------------
# Process each file
# ---------------------------------------------------------------------------
for filepath in html_files:
    rel = os.path.relpath(filepath, ROOT)
    content = open(filepath, 'r', encoding='utf-8').read()
    original = content
    modified = False

    # --- Issue 1: Preconnect ---
    file_size = len(content.encode('utf-8'))

    if 'preconnect" href="https://img.tabiji.ai"' in content:
        preconnect_skipped_already += 1
    elif file_size < 900 and ('http-equiv="refresh"' in content or "http-equiv='refresh'" in content
                               or 'window.location.replace' in content):
        preconnect_skipped_redirect += 1
    elif '<head>' not in content and '<head ' not in content:
        preconnect_skipped_no_head += 1
    else:
        # Special case: find/index.html -- insert before the fonts.googleapis.com preconnect
        if 'preconnect' in content and 'fonts.googleapis.com' in content:
            content = content.replace(
                '<link rel="preconnect" href="https://fonts.googleapis.com">',
                PRECONNECT_TAG + '\n<link rel="preconnect" href="https://fonts.googleapis.com">',
                1
            )
            if content != original:
                preconnect_added += 1
                modified = True
        else:
            # General strategy: insert after <meta name="viewport" ...> line
            # Try several patterns that cover the different template styles

            inserted = False

            # Pattern 1: <meta name="viewport" ...> (standard attribute order)
            vp_match = re.search(
                r'(<meta\s+name=["\']viewport["\'][^>]*>)[ \t]*\n',
                content, re.IGNORECASE
            )
            if vp_match:
                end = vp_match.end()
                # Detect indentation of the viewport line
                line_start = content.rfind('\n', 0, vp_match.start()) + 1
                indent = ''
                for ch in content[line_start:]:
                    if ch in ' \t':
                        indent += ch
                    else:
                        break
                content = content[:end] + indent + PRECONNECT_TAG + '\n' + content[end:]
                inserted = True

            # Pattern 2: <meta content="width=device-width..." name="viewport"/> (reversed attrs)
            if not inserted:
                vp_match = re.search(
                    r'(<meta\s+content=["\']width=device-width[^"\']*["\'][^>]*>)[ \t]*\n',
                    content, re.IGNORECASE
                )
                if vp_match:
                    end = vp_match.end()
                    line_start = content.rfind('\n', 0, vp_match.start()) + 1
                    indent = ''
                    for ch in content[line_start:]:
                        if ch in ' \t':
                            indent += ch
                        else:
                            break
                    content = content[:end] + indent + PRECONNECT_TAG + '\n' + content[end:]
                    inserted = True

            # Pattern 3: fallback -- after <meta charset=...> line
            if not inserted:
                cs_match = re.search(
                    r'(<meta\s+charset=[^>]*>)[ \t]*\n',
                    content, re.IGNORECASE
                )
                if cs_match:
                    end = cs_match.end()
                    line_start = content.rfind('\n', 0, cs_match.start()) + 1
                    indent = ''
                    for ch in content[line_start:]:
                        if ch in ' \t':
                            indent += ch
                        else:
                            break
                    content = content[:end] + indent + PRECONNECT_TAG + '\n' + content[end:]
                    inserted = True

            # Pattern 4: last resort -- right after <head> or <head ...>
            if not inserted:
                head_match = re.search(r'(<head[^>]*>)[ \t]*\n', content, re.IGNORECASE)
                if head_match:
                    end = head_match.end()
                    content = content[:end] + PRECONNECT_TAG + '\n' + content[end:]
                    inserted = True

            if inserted and content != original:
                preconnect_added += 1
                modified = True

    # --- Issue 2: Speakable ".hero .subtitle" -> ".hero p" in compare pages ---
    if rel.startswith('compare/') and '".hero .subtitle"' in content:
        content = content.replace('".hero .subtitle"', '".hero p"')
        speakable_fixed += 1
        modified = True

    # Write if modified
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
print("=== Issue 1: Preconnect for img.tabiji.ai ===")
print(f"  Added:              {preconnect_added}")
print(f"  Skipped (already):  {preconnect_skipped_already}")
print(f"  Skipped (redirect): {preconnect_skipped_redirect}")
print(f"  Skipped (no head):  {preconnect_skipped_no_head}")
print()
print("=== Issue 2: Speakable .hero .subtitle -> .hero p ===")
print(f"  Fixed:              {speakable_fixed}")
print()
print("Done.")
