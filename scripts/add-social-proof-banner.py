#!/usr/bin/env python3
"""Add a social proof banner to popular-picks and compare pages.

Inserts BEFORE the CTA section (or before footer if no CTA section):
- Social proof: "Trusted by 2,500+ travelers"
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

DISCOVERY_CSS = """
<style>
.social-proof-banner { background: linear-gradient(135deg, #f0ebe3 0%, #e8e0d4 100%); border: 1px solid #d4c5b0; border-radius: 14px; padding: 1rem 1.4rem; margin-bottom: 1.4rem; text-align: center; }
.social-proof-banner p { margin: 0; color: #4a3f35; font-size: .92rem; }
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
    
    new_content = content.replace("</head>", DISCOVERY_CSS + "</head>", 1)

    idx = new_content.find(insert_before)
    if idx == -1:
        return False

    new_content = new_content[:idx] + SOCIAL_PROOF_HTML + "\n" + new_content[idx:]
    
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
