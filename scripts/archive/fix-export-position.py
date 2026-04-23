#!/usr/bin/env python3
"""
Move export button next to CTA (inside nav-links), rename CTA to 'Plan Your Trip'.
"""
import glob, os, re

EXPORT_BUTTON = '''        <button class="export-nav" onclick="openExportModal();if(typeof gtag==='function')gtag('event','click_export_doc',{event_category:'engagement',event_label:location.pathname})" title="Export Google Doc">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          <span>Export Google Doc</span>
        </button>'''

updated = 0

for page in sorted(glob.glob(os.path.expanduser('~/tabiji/i/*/index.html'))):
    with open(page, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'export-nav' not in html:
        continue
    
    orig = html

    # Remove the standalone export button (between logo and hamburger)
    html = re.sub(
        r'    <button class="export-nav"[^>]*onclick="openExportModal\(\)[^"]*"[^>]*title="Export Google Doc">\s*'
        r'<svg[^>]*>.*?</svg>\s*'
        r'<span>Export Google Doc</span>\s*'
        r'</button>\n',
        '',
        html,
        flags=re.DOTALL
    )
    
    # Find the CTA link and add export button before it inside nav-links
    # Match various CTA text patterns
    html = re.sub(
        r'(<div class="nav-links">\s*\n)(\s*<a href="/plan" class="cta-nav">)',
        r'\1' + EXPORT_BUTTON + r'\n\2',
        html
    )
    
    # Rename CTA: any "Get Your ..." text to "Plan Your Trip"
    html = re.sub(
        r'>Get Your Free Custom Itinerary</a>',
        r'>Plan Your Trip</a>',
        html
    )
    html = re.sub(
        r'>Get Your Itinerary</a>',
        r'>Plan Your Trip</a>',
        html
    )
    html = re.sub(
        r'>Get Your Free Personalized Itinerary</a>',
        r'>Plan Your Trip</a>',
        html
    )

    if html != orig:
        with open(page, 'w', encoding='utf-8') as f:
            f.write(html)
        updated += 1

print(f"✅ Updated: {updated} pages")
