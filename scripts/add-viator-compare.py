#!/usr/bin/env python3
"""Add Viator affiliate link blocks to all compare pages.

Inserts a Viator section after the CTA section (before </div><!-- /article-content -->)
and adds Viator CSS to the <style> block.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO_ROOT / "compare"
DATA_DIR = REPO_ROOT / "compare-data"

VIATOR_PID = "P00292930"
VIATOR_MCID = "42383"

VIATOR_CSS = """
      .viator-section { background:linear-gradient(135deg,#fff9f0 0%,#fff 100%); border:1px solid #e0d6c8; border-radius:18px; padding:1.35rem 1.4rem; margin-top:2rem; margin-bottom:1.4rem; }
      .viator-section h2 { font-size:1.3em; margin-bottom:6px; }
      .viator-subtitle { font-size:0.95em; color:#666; margin-bottom:20px; }
      .viator-cards { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
      @media(max-width:600px) { .viator-cards { grid-template-columns:1fr; } }
      .viator-card { background:#fff; border:1px solid #e8e8e8; border-radius:10px; padding:18px; text-decoration:none; color:inherit; transition:border-color .2s,box-shadow .2s; display:flex; flex-direction:column; gap:8px; }
      .viator-card:hover { border-color:var(--primary,#0696D7); box-shadow:0 2px 12px rgba(6,150,215,.12); }
      .viator-card .tour-type { font-size:.75em; text-transform:uppercase; letter-spacing:.5px; color:var(--primary,#0696D7); font-weight:600; }
      .viator-card .tour-name { font-size:1em; font-weight:600; line-height:1.3; }
      .viator-powered { font-size:.75em; color:#bbb; text-align:right; margin-top:14px; }"""


def viator_url(query: str) -> str:
    q = query.replace(" ", "+")
    return f"https://www.viator.com/search/{q}?pid={VIATOR_PID}&mcid={VIATOR_MCID}&medium=link"


def build_viator_html(dest1: str, dest2: str) -> str:
    return f"""<section class="viator-section">
        <h2>&#127903;&#65039; Book Tours & Experiences</h2>
        <p class="viator-subtitle">Hand-picked tours and activities for both destinations — book with free cancellation</p>
        <div class="viator-cards">
      <a class="viator-card" href="{viator_url(dest1 + ' tours')}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">Explore {dest1}</span>
        <span class="tour-name">{dest1} Tours & Activities →</span>
      </a>
      <a class="viator-card" href="{viator_url(dest1 + ' day trips')}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">{dest1} Day Trip</span>
        <span class="tour-name">{dest1} Day Trips & Excursions</span>
      </a>
      <a class="viator-card" href="{viator_url(dest2 + ' tours')}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">Explore {dest2}</span>
        <span class="tour-name">{dest2} Tours & Activities →</span>
      </a>
      <a class="viator-card" href="{viator_url(dest2 + ' day trips')}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">{dest2} Day Trip</span>
        <span class="tour-name">{dest2} Day Trips & Excursions</span>
      </a>
        </div>
        <p class="viator-powered">Experiences via Viator — free cancellation on most tours</p>
      </section>"""


def process_html_file(html_path: Path, dest1: str, dest2: str) -> bool:
    """Insert Viator block into a compare HTML file. Returns True if modified."""
    content = html_path.read_text(encoding="utf-8")

    if "viator-section" in content:
        return False  # Already has Viator block

    # Add CSS before </style>
    if VIATOR_CSS.strip().split("\n")[0].strip() not in content:
        content = content.replace("</style>", VIATOR_CSS + "\n</style>", 1)

    # Insert Viator HTML after the CTA section, before </div><!-- /article-content -->
    viator_html = build_viator_html(dest1, dest2)
    marker = '</div><!-- /article-content -->'
    if marker in content:
        content = content.replace(marker, viator_html + "\n" + marker, 1)
    else:
        print(f"  WARNING: Could not find insertion marker in {html_path}")
        return False

    html_path.write_text(content, encoding="utf-8")
    return True


def main():
    count = 0
    errors = []

    for data_path in sorted(DATA_DIR.glob("*.json")):
        slug = data_path.stem
        html_path = COMPARE_DIR / slug / "index.html"

        if not html_path.exists():
            errors.append(f"Missing HTML: {slug}")
            continue

        data = json.loads(data_path.read_text())
        dest1 = data["destinations"]["destination1"]
        dest2 = data["destinations"]["destination2"]

        if process_html_file(html_path, dest1, dest2):
            count += 1
            print(f"  ✅ {slug} ({dest1} vs {dest2})")
        else:
            print(f"  ⏭️  {slug} (already has Viator or skipped)")

    if errors:
        print(f"\n⚠️  Errors: {len(errors)}")
        for e in errors:
            print(f"  - {e}")

    print(f"\n✅ Added Viator blocks to {count} compare pages")


if __name__ == "__main__":
    main()
