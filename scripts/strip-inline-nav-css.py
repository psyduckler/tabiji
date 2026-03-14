#!/usr/bin/env python3
"""Strip inline nav CSS from itinerary detail pages.

These pages now link shared-shell.css, so the inline nav/logo/hamburger/
nav-dropdown/cta-nav rules are redundant.

Strategy: parse each <style> block, identify and remove CSS rule blocks
whose selectors match nav-related patterns. Preserve everything else.
"""

import re, glob, sys

NAV_SELECTORS = re.compile(
    r'^\s*('
    r'nav\s*\{|'
    r'nav\s+a\.cta-nav|'
    r'\.logo\s*\{|'
    r'\.logo\s+span|'
    r'\.logo\s*\{position|'           # minified owl line
    r'\.logo:hover|'
    r'\.logo\s+\.owl|'
    r'\.hamburger|'
    r'\.nav-links|'
    r'\.nav-dropdown|'
    r'\.export-nav|'
    r'footer\s+a\s*\{'
    r')',
    re.MULTILINE
)

# Minified one-liner pattern (e.g. .logo{position:relative}.logo .owl-fly{display:none}...)
MINIFIED_NAV_LINE = re.compile(
    r'^\s*\.logo\{position:relative\}.*$', re.MULTILINE
)

def strip_nav_rules_from_style(css_text):
    """Remove nav-related CSS rules from a style block's content."""
    result_lines = []
    lines = css_text.split('\n')
    i = 0
    skip_depth = 0
    skipping = False

    while i < len(lines):
        line = lines[i]

        # Check for minified nav line
        if MINIFIED_NAV_LINE.match(line):
            i += 1
            continue

        # Check if this line starts a nav-related rule
        if not skipping and NAV_SELECTORS.match(line):
            # Start skipping - count braces
            skipping = True
            skip_depth = line.count('{') - line.count('}')
            if skip_depth <= 0:
                # Single-line rule, done skipping
                skipping = False
            i += 1
            continue

        if skipping:
            skip_depth += line.count('{') - line.count('}')
            if skip_depth <= 0:
                skipping = False
            i += 1
            continue

        result_lines.append(line)
        i += 1

    return '\n'.join(result_lines)


def strip_nav_from_media_queries(css_text):
    """Remove nav-related rules from inside @media blocks."""
    # Handle @media blocks that contain nav rules
    # We need to go inside media blocks and strip nav rules there too
    result = []
    lines = css_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Detect single-line @media with nav rules
        if stripped.startswith('@media') and any(kw in stripped for kw in ['nav {', 'nav a.cta', '.hamburger', '.nav-links', '.logo', '.nav-dropdown', '.export-nav']):
            # Check if entire media query is on one line
            if stripped.count('{') == stripped.count('}'):
                # Single line media query with nav rules - skip it
                i += 1
                continue
        
        # Multi-line @media block
        if stripped.startswith('@media') and '{' in stripped:
            # Collect the entire media block
            media_start = line
            brace_count = line.count('{') - line.count('}')
            media_lines = [line]
            i += 1
            while i < len(lines) and brace_count > 0:
                media_lines.append(lines[i])
                brace_count += lines[i].count('{') - lines[i].count('}')
                i += 1
            
            # Check if this media block contains nav rules
            media_content = '\n'.join(media_lines)
            if any(kw in media_content for kw in ['nav {', 'nav a.cta', '.hamburger', '.nav-links', '.logo', 'nav-dropdown', '.export-nav']):
                # Strip nav rules from inside the media block
                # Get the inner content (between first { and last })
                inner_start = media_content.index('{') + 1
                inner_end = media_content.rindex('}')
                inner = media_content[inner_start:inner_end]
                
                cleaned_inner = strip_nav_rules_from_style(inner)
                
                # If nothing left inside, skip the whole media block
                if cleaned_inner.strip():
                    # Rebuild the media block
                    # Get the @media line up to first {
                    media_header = media_content[:inner_start]
                    result.append(media_header)
                    result.append(cleaned_inner)
                    result.append('}')
                # else: drop the entire empty media block
            else:
                result.extend(media_lines)
            continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result)


def clean_empty_lines(text):
    """Collapse multiple blank lines into at most two."""
    return re.sub(r'\n{3,}', '\n\n', text)


def process_file(filepath, dry_run=False):
    with open(filepath) as f:
        original = f.read()
    
    content = original
    
    def replace_style(m):
        style_content = m.group(1)
        cleaned = strip_nav_rules_from_style(style_content)
        cleaned = strip_nav_from_media_queries(cleaned)
        cleaned = clean_empty_lines(cleaned)
        return f'<style>{cleaned}</style>'
    
    content = re.sub(r'<style>(.*?)</style>', replace_style, content, flags=re.DOTALL)
    
    if content != original:
        if not dry_run:
            with open(filepath, 'w') as f:
                f.write(content)
        removed = len(original) - len(content)
        return removed
    return 0


def main():
    dry_run = '--dry-run' in sys.argv
    files = sorted(glob.glob('itineraries/*/index.html'))
    total_removed = 0
    changed = 0
    
    for f in files:
        removed = process_file(f, dry_run=dry_run)
        if removed > 0:
            changed += 1
            total_removed += removed
            print(f'  {"[DRY] " if dry_run else ""}Cleaned {f} (-{removed} bytes)')
    
    print(f'\n{"[DRY RUN] " if dry_run else ""}Done: {changed}/{len(files)} files cleaned, {total_removed} bytes removed')


if __name__ == '__main__':
    main()
