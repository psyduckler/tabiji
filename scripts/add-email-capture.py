#!/usr/bin/env python3
"""Add email capture module to popular-picks and compare pages.

Adds a lightweight "Get travel tips" email signup before the footer.
Uses FormSubmit.co (already used for media studio) to route to hello@tabiji.ai.
"""

import os
import glob

EMAIL_CSS = """
<style>
.email-capture { background: linear-gradient(135deg, #2D3A5C 0%, #3d4d70 100%); border-radius: 18px; padding: 1.8rem 1.6rem; margin-bottom: 1.4rem; text-align: center; color: white; }
.email-capture h3 { margin: 0 0 .4rem; font-size: 1.15rem; color: white; }
.email-capture p { margin: 0 0 1rem; font-size: .88rem; opacity: .85; }
.email-capture-form { display: flex; gap: .5rem; max-width: 420px; margin: 0 auto; }
.email-capture-form input[type="email"] { flex: 1; padding: .65rem 1rem; border: 2px solid rgba(255,255,255,.2); border-radius: 10px; background: rgba(255,255,255,.1); color: white; font-size: .9rem; outline: none; }
.email-capture-form input[type="email"]::placeholder { color: rgba(255,255,255,.5); }
.email-capture-form input[type="email"]:focus { border-color: #C4704B; }
.email-capture-form button { padding: .65rem 1.2rem; background: #C4704B; color: white; border: none; border-radius: 10px; font-weight: 700; font-size: .88rem; cursor: pointer; white-space: nowrap; transition: background .2s; }
.email-capture-form button:hover { background: #b5613e; }
.email-capture .privacy-note { font-size: .72rem; opacity: .5; margin-top: .6rem; }
@media (max-width: 500px) { .email-capture-form { flex-direction: column; } }
</style>
"""

EMAIL_HTML = """
<!-- email-capture:start -->
<section class="email-capture">
  <h3>✈️ Get Travel Tips & Hidden Gems</h3>
  <p>Join 500+ travelers who get weekly destination insights — no spam, ever.</p>
  <form class="email-capture-form" action="https://formsubmit.co/hello@tabiji.ai" method="POST">
    <input type="hidden" name="_subject" value="New subscriber from tabiji.ai">
    <input type="hidden" name="_template" value="table">
    <input type="hidden" name="_captcha" value="false">
    <input type="hidden" name="_next" value="https://tabiji.ai/thanks/">
    <input type="email" name="email" placeholder="your@email.com" required>
    <button type="submit">Subscribe</button>
  </form>
  <p class="privacy-note">No spam. Unsubscribe anytime.</p>
</section>
<!-- email-capture:end -->
"""

added = 0

def process_file(filepath):
    global added
    with open(filepath, "r") as f:
        content = f.read()
    
    if "email-capture:start" in content:
        return
    
    # Insert before footer
    marker = "<!-- @include:footer:start -->"
    if marker not in content:
        return
    
    content = content.replace(marker, EMAIL_HTML + "\n" + marker, 1)
    content = content.replace("</head>", EMAIL_CSS + "</head>", 1)
    
    with open(filepath, "w") as f:
        f.write(content)
    added += 1

# Popular picks
for page in sorted(glob.glob(os.path.expanduser("~/tabiji/popular-picks/*/index.html"))):
    process_file(page)

# Compare pages
for page in sorted(glob.glob(os.path.expanduser("~/tabiji/compare/*/index.html"))):
    process_file(page)

print(f"Added email capture to {added} pages")
