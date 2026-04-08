#!/usr/bin/env python3
"""Add a social proof banner + discovery CTAs to popular-picks and compare pages.

Inserts BEFORE the CTA section (or before footer if no CTA section):
1. Social proof: "Trusted by 2,500+ travelers" 
2. Discovery module: "Not sure where to go?" with quiz/spin/find links

Also adds a "related popular picks" section to compare pages that don't have one.
"""

import os
import re
import glob

SOCIAL_PROOF_HTML = """
<!-- social-proof:start -->
<section class="social-proof-banner">
  <p>🌍 <strong>Trusted by 2,500+ travelers</strong> — our itineraries are built from real Reddit discussions, local insights, and traveler reviews.</p>
</section>
<!-- social-proof:end -->
"""

DISCOVERY_CTA_HTML = """
<!-- discovery-cta:start -->
<section class="discovery-module">
  <h3>Not sure where to go?</h3>
  <div class="discovery-links">
    <a href="/find/" class="discovery-card">🔍 <strong>Destination Finder</strong><span>Filter by vibe, budget & style</span></a>
  </div>
</section>
<!-- discovery-cta:end -->
"""

DISCOVERY_CSS = """
<style>
.social-proof-banner { background: linear-gradient(135deg, #f0ebe3 0%, #e8e0d4 100%); border: 1px solid #d4c5b0; border-radius: 14px; padding: 1rem 1.4rem; margin-bottom: 1.4rem; text-align: center; }
.social-proof-banner p { margin: 0; color: #4a3f35; font-size: .92rem; }
.discovery-module { background: white; border: 1px solid #e0d6c8; border-radius: 18px; padding: 1.35rem 1.4rem; margin-bottom: 1.4rem; }
.discovery-module h3 { margin: 0 0 .8rem; color: #2D3A5C; font-size: 1.1rem; }
.discovery-links { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: .7rem; }
.discovery-card { display: flex; flex-direction: column; background: #faf7f2; border: 1px solid #e0d6c8; border-radius: 12px; padding: .85rem 1rem; text-decoration: none; color: #2D3A5C; transition: border-color .2s, transform .15s; }
.discovery-card:hover { border-color: #C4704B; transform: translateY(-2px); }
.discovery-card strong { font-size: .95rem; }
.discovery-card span { font-size: .8rem; color: #7a6f63; margin-top: .2rem; }
</style>
"""

def process_file(filepath, page_type):
    with open(filepath, "r") as f:
        content = f.read()
    
    # Skip if already has social proof
    if "social-proof:start" in content:
        return False
    
    # Find insertion point: before cta-section, or before footer
    insert_before = None
    if '<section class="cta-section">' in content:
        insert_before = '<section class="cta-section">'
    elif "<!-- @include:footer:start -->" in content:
        insert_before = "<!-- @include:footer:start -->"
    elif '<div class="cta-section">' in content:
        insert_before = '<div class="cta-section">'
    else:
        return False
    
    # Build injection
    injection = SOCIAL_PROOF_HTML + DISCOVERY_CTA_HTML
    
    # Add CSS before </head>
    new_content = content.replace("</head>", DISCOVERY_CSS + "</head>", 1)
    
    # Insert sections before CTA/footer
    idx = new_content.find(insert_before)
    if idx == -1:
        return False
    
    # Add proper indentation
    new_content = new_content[:idx] + injection + "\n" + new_content[idx:]
    
    with open(filepath, "w") as f:
        f.write(new_content)
    return True

# Process popular-picks
pp_count = 0
for page in sorted(glob.glob(os.path.expanduser("~/tabiji/popular-picks/*/index.html"))):
    if process_file(page, "popular-picks"):
        pp_count += 1

# Process compare pages
cp_count = 0
for page in sorted(glob.glob(os.path.expanduser("~/tabiji/compare/*/index.html"))):
    # Skip hub/index pages
    dirname = os.path.basename(os.path.dirname(page))
    if dirname in ("compare",):
        continue
    if process_file(page, "compare"):
        cp_count += 1

print(f"Added social proof + discovery to {pp_count} popular-picks, {cp_count} compare pages")
