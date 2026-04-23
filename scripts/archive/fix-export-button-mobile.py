#!/usr/bin/env python3
"""
Move export button outside nav-links (always visible on mobile),
rename to "Export Google Doc", add GA4 click tracking.
"""
import glob, os, re

updated = 0

for page in sorted(glob.glob(os.path.expanduser('~/tabiji/i/*/index.html'))):
    with open(page, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'export-nav' not in html:
        continue
    
    orig = html
    
    # 1. Remove export button from inside nav-links
    html = html.replace(
        '''        <button class="export-nav" onclick="openExportModal()" title="Export to Google Docs">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          <span>Google Docs</span>
        </button>
''', '')

    # 2. Add export button BEFORE the hamburger (outside nav-links, always visible)
    new_button = '''    <button class="export-nav" onclick="openExportModal();if(typeof gtag==='function')gtag('event','click_export_doc',{event_category:'engagement',event_label:location.pathname})" title="Export Google Doc">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
      <span>Export Google Doc</span>
    </button>'''
    
    # Place before hamburger button
    html = html.replace(
        '    <button class="hamburger"',
        new_button + '\n    <button class="hamburger"'
    )
    
    # 3. Rename in CSS: hide span on mobile → keep span visible
    # Remove the `export-nav span { display:none }` from mobile if present
    html = html.replace('.export-nav span { display: none; }\n', '')
    html = html.replace('.export-nav span { display:none; }\n', '')
    
    if html != orig:
        with open(page, 'w', encoding='utf-8') as f:
            f.write(html)
        updated += 1

print(f"✅ Updated: {updated} pages")
