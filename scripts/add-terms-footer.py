#!/usr/bin/env python3
"""
add-terms-footer.py
Adds a Terms of Service link to the footer of every HTML file in the tabiji repo.
Safe to run multiple times — skips files that already have the link.
"""

import os
import re
import sys

TERMS_LINK = '<a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a>'
SEPARATOR = ' · '

ROOT = os.path.expanduser('~/tabiji')

def find_html_files(root):
    """Walk the repo and find all .html files."""
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden dirs and node_modules
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']
        for fname in filenames:
            if fname.endswith('.html'):
                html_files.append(os.path.join(dirpath, fname))
    return sorted(html_files)

def add_terms_to_footer(content, filepath):
    """
    Add Terms of Service link to the last </p> inside <footer>...</footer>.
    Returns (new_content, changed: bool, reason: str).
    """
    # Quick check: already has the terms link?
    if '/terms/' in content and 'Terms of Service' in content:
        return content, False, 'already has Terms link'

    # Find the footer block
    footer_match = re.search(r'<footer>(.*?)</footer>', content, re.DOTALL | re.IGNORECASE)
    if not footer_match:
        return content, False, 'no <footer> found'

    footer_content = footer_match.group(1)
    footer_start = footer_match.start(1)
    footer_end = footer_match.end(1)

    # Find the last </p> inside the footer
    # We'll insert our link just before it
    last_p_close = footer_content.rfind('</p>')
    if last_p_close == -1:
        return content, False, 'no </p> inside footer'

    # Build the insertion: add separator + link just before </p>
    insert_pos = footer_start + last_p_close
    new_content = content[:insert_pos] + SEPARATOR + TERMS_LINK + content[insert_pos:]

    return new_content, True, 'updated'

def main():
    html_files = find_html_files(ROOT)
    print(f"Found {len(html_files)} HTML files")

    updated = 0
    skipped = 0
    errors = 0
    no_footer = 0

    for filepath in html_files:
        rel = os.path.relpath(filepath, ROOT)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original = f.read()

            new_content, changed, reason = add_terms_to_footer(original, filepath)

            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated += 1
                print(f"  ✓ {rel}")
            else:
                if 'no <footer>' in reason:
                    no_footer += 1
                    print(f"  - {rel}: {reason}")
                else:
                    skipped += 1
                    # Only print skipped if verbose
                    # print(f"  = {rel}: {reason}")

        except Exception as e:
            errors += 1
            print(f"  ✗ {rel}: ERROR — {e}", file=sys.stderr)

    print()
    print(f"Done. Updated: {updated} | Already done: {skipped} | No footer: {no_footer} | Errors: {errors}")
    print(f"Total files processed: {len(html_files)}")

if __name__ == '__main__':
    main()
