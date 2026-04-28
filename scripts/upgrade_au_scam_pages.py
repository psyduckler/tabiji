#!/usr/bin/env python3
"""Upgrade the 14 Australia city scam pages from the legacy 'editorial-v2'
template to the NYC-canonical template.

Idempotent. Touches only the AU set. Each delta is independent and skipped
if already present.

Deltas applied per page:
  1. Hero: append severity-summary + reading-time divs (computed)
  2. Content: prepend cross-links section
  3. Rename key-takeaways → takeaways-box
  4. Replace toc-box <ul> with toc <ol class="toc-list"> + severity badges
  5. Wrap "The X Scams" h2 in a flex container with share-btn + add <hr>
  6. Inject mid-cta between scam-3 and scam-4
  7. Add id="emergency" to action-section
  8. Append emergency-fab + back-to-top floats after footer (before mobile-book-bar)
  9. Article schema: add image + speakable
 10. Add Place schema entry to @graph

Reading time formula: max(2, round(words_in_main / 540))
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAMS = ROOT / "scams"
WPM = 540

CITIES = [
    "adelaide", "alice-springs", "brisbane", "byron-bay", "cairns",
    "canberra", "darwin", "gold-coast", "hobart", "melbourne",
    "perth", "port-douglas", "sydney", "whitsundays",
]

DISPLAY = {
    "adelaide": "Adelaide", "alice-springs": "Alice Springs", "brisbane": "Brisbane",
    "byron-bay": "Byron Bay", "cairns": "Cairns", "canberra": "Canberra",
    "darwin": "Darwin", "gold-coast": "Gold Coast", "hobart": "Hobart",
    "melbourne": "Melbourne", "perth": "Perth", "port-douglas": "Port Douglas",
    "sydney": "Sydney", "whitsundays": "Whitsundays",
}


def severity_counts(html: str) -> tuple[int, int, int]:
    """Count high/medium/low danger badges in scam-card headers."""
    high = len(re.findall(r'class="danger-badge danger-high"', html))
    med = len(re.findall(r'class="danger-badge danger-medium"', html))
    low = len(re.findall(r'class="danger-badge danger-low"', html))
    return high, med, low


def reading_time(html: str) -> int:
    """Words inside <main>...</main>, /540 wpm, floor 2."""
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL)
    if not m:
        # Fall back to whole-body word count after the breadcrumb
        body_text = re.sub(r"<[^>]+>", " ", html)
    else:
        body_text = re.sub(r"<[^>]+>", " ", m.group(1))
    words = len(body_text.split())
    return max(2, round(words / WPM))


def scam_titles_with_severity(html: str) -> list[tuple[str, str]]:
    """Return ordered list of (severity_class, title) per scam-card."""
    out = []
    for cm in re.finditer(
        r'<div class="scam-card"[^>]*>(.*?)(?=<div class="scam-card"|<div class="action-section"|<!-- What to do)',
        html, re.DOTALL,
    ):
        body = cm.group(1)
        sev_m = re.search(r'class="danger-badge danger-(high|medium|low)"', body)
        title_m = re.search(r'<div class="scam-title">([^<]+)</div>', body)
        if sev_m and title_m:
            out.append((sev_m.group(1), title_m.group(1).strip()))
    return out


def upgrade_hero(html: str, h: int, m: int, l: int, mins: int) -> tuple[str, bool]:
    """Insert severity-summary + reading-time after hero-meta inside .hero."""
    if 'class="severity-summary"' in html and 'class="reading-time"' in html:
        return html, False
    # Find </div> that closes the .hero — the one right after hero-meta closes.
    # Hero-meta is a flat div with 4 spans, then </div> then </div> for .hero
    pat = re.compile(r'(<div class="hero-meta">.*?</div>)\s*(</div>\s*<div\s+(?:id="main"\s+)?class="content"|</div>\s*<main|<div\s+(?:id="main"\s+)?class="content"|</div>\s*<div\s+id="main")', re.DOTALL)
    snippet = (
        f'\n<div class="severity-summary"><span class="severity-pill high">{h} High Risk</span>'
        f'<span class="severity-pill medium">{m} Medium</span>'
        f'<span class="severity-pill low">{l} Low</span></div>\n'
        f'<div class="reading-time">📖 {mins} min read</div>\n'
    )
    new_html, n = pat.subn(rf'\1{snippet}\2', html, count=1)
    if n == 0:
        # Simpler fallback: find hero-meta and insert right after its closing </div>
        hm_pat = re.compile(r'(<div class="hero-meta">[\s\S]*?</div>)', re.DOTALL)
        match = hm_pat.search(html)
        if not match:
            return html, False
        new_html = html[:match.end()] + snippet + html[match.end():]
    return new_html, True


def upgrade_cross_links(html: str, country_iso: str, country_name: str, city_display: str) -> tuple[str, bool]:
    """Insert cross-links as first child of .content div."""
    if 'class="cross-links"' in html:
        return html, False
    cross_div = (
        f'\n<div class="cross-links">'
        f'<a class="cross-link" href="/health/{country_name.lower().replace(" ", "-")}/">🏥 {country_name} Health Guide</a>'
        f'<a class="cross-link" href="/scams/country/{country_iso}/">🗺 All {country_name} Scam Guides</a>'
        f'<a class="cross-link" href="/plan/">📋 Free {city_display} Itinerary</a>'
        f'</div>\n'
    )
    # Match the content open — could be `<div id="main" class="content">` or `<div class="content">`
    pat = re.compile(r'(<div(?:\s+id="main")?\s+class="content"[^>]*>)', re.DOTALL)
    new_html, n = pat.subn(rf'\1{cross_div}', html, count=1)
    return new_html, (n > 0)


def upgrade_takeaways(html: str) -> tuple[str, bool]:
    """key-takeaways → takeaways-box (cosmetic class rename)."""
    if 'class="takeaways-box"' in html:
        return html, False
    new_html = re.sub(
        r'<div\s+class="key-takeaways"\s*>',
        '<div class="takeaways-box">',
        html, count=1,
    )
    return new_html, new_html != html


def upgrade_toc(html: str, scams: list[tuple[str, str]]) -> tuple[str, bool]:
    """Replace toc-box <ul> with toc <ol class='toc-list'> with severity badges."""
    if 'class="toc-list"' in html or '<div class="toc">' in html:
        return html, False
    pat = re.compile(
        r'<div\s+class="toc-box">\s*<h2>([^<]+)</h2>\s*<ul>\s*([\s\S]*?)\s*</ul>\s*</div>',
        re.DOTALL,
    )
    m = pat.search(html)
    if not m:
        return html, False
    h2_text = m.group(1)
    items = []
    for i, (sev, title) in enumerate(scams, 1):
        sev_label = {"high": "High", "medium": "Medium", "low": "Low"}[sev]
        # decode &amp; in title for display
        title_clean = title.replace("&amp;", "&")
        items.append(
            f'<li><a href="#scam-{i}"><span class="toc-badge {sev}">{sev_label}</span> {title_clean}</a></li>'
        )
    items_html = "\n".join(items)
    replacement = f'<div class="toc">\n<h2>{h2_text}</h2>\n<ol class="toc-list">\n{items_html}\n</ol>\n</div>'
    new_html = pat.sub(replacement, html, count=1)
    return new_html, True


def upgrade_section_heading(html: str) -> tuple[str, bool]:
    """Replace the bare 'The X Scams' h2 with the flex+share-btn pattern."""
    if 'class="share-btn"' in html:
        return html, False
    pat = re.compile(
        r'<h2\s+class="section-heading"\s+style="margin-bottom:0;border-bottom:none;padding-bottom:0;">The (\d+) Scams</h2>',
        re.DOTALL,
    )
    m = pat.search(html)
    if not m:
        return html, False
    n = m.group(1)
    replacement = (
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">\n'
        f'<h2 class="section-heading" style="margin-bottom:0;border-bottom:none;padding-bottom:0;">The {n} Scams</h2>\n'
        f'<button class="share-btn" onclick="if(navigator.share)navigator.share({{title:document.title,url:location.href}});else{{navigator.clipboard.writeText(location.href);this.textContent=\'✓ Link copied!\';setTimeout(()=&gt;this.innerHTML=\'🔗 Share this guide\',2000)}}">🔗 Share this guide</button>\n'
        f'</div>\n'
        f'<hr style="border:none;border-top:2px solid var(--sand);margin:0.6rem 0 1.25rem;"/>'
    )
    new_html = pat.sub(replacement, html, count=1)
    return new_html, True


def upgrade_mid_cta(html: str, city_display: str) -> tuple[str, bool]:
    """Insert mid-cta between scam-3 closing and <!-- Scam 4 -->."""
    if 'class="mid-cta"' in html:
        return html, False
    cta = (
        f'\n<div class="mid-cta">\n'
        f'<p>Like what you\'re reading? Get a full {city_display} itinerary with safety tips built in.</p>\n'
        f'<a href="/plan/">Get Free Itinerary →</a>\n'
        f'</div>\n'
    )
    # Sit between the scam-3 closing div and the "<!-- Scam 4 -->" comment.
    # Pages have varied indentation, so anchor on the comment.
    pat = re.compile(r'(\n\s*<!--\s*Scam\s+4\s*-->)', re.DOTALL)
    new_html, n = pat.subn(rf'{cta}\1', html, count=1)
    return new_html, (n > 0)


def upgrade_emergency_id(html: str) -> tuple[str, bool]:
    """Add id='emergency' to <div class='action-section'> if missing."""
    if re.search(r'<div class="action-section" id="emergency"', html) or \
       re.search(r'<div\s+class="action-section"\s+id="emergency"', html):
        return html, False
    pat = re.compile(r'<div\s+class="action-section">')
    new_html, n = pat.subn('<div class="action-section" id="emergency">', html, count=1)
    return new_html, (n > 0)


def upgrade_floats(html: str) -> tuple[str, bool]:
    """Add emergency-fab + back-to-top floats after the closing </footer>.
    On legacy AU pages there is a mobile-book-bar after the footer; we insert
    the FABs after the existing book-bar block so they layer above on mobile.
    """
    if 'class="emergency-fab"' in html and 'class="back-to-top"' in html:
        return html, False
    floats_html = (
        '\n<a aria-label="Emergency help" class="emergency-fab" href="#emergency">🆘</a>\n'
        '<span class="emergency-fab-tooltip">Been scammed? Get help</span>\n'
        '<a aria-label="Back to top" class="back-to-top" href="#" id="btt">▲</a>\n'
        '<script>\n'
        '(function(){var b=document.getElementById(\'btt\');if(!b)return;'
        'window.addEventListener(\'scroll\',function(){b.classList.toggle(\'visible\',window.scrollY>600)},{passive:true});'
        'b.addEventListener(\'click\',function(e){e.preventDefault();window.scrollTo({top:0,behavior:\'smooth\'})});'
        '})();\n'
        '</script>\n'
    )
    # Insert just before </body>
    new_html, n = re.subn(r'</body>', floats_html + '</body>', html, count=1)
    return new_html, (n > 0)


def upgrade_article_schema(html: str, og_image_url: str) -> tuple[str, bool]:
    """Add image + speakable to the Article entry in @graph."""
    # Find the "Article" object inside @graph
    pat = re.compile(
        r'("@type":\s*"Article",\s*\n\s*"headline":\s*"[^"]+",\s*\n\s*"description":\s*"[^"]+",\s*\n\s*"url":\s*"[^"]+",)\s*\n(\s*)("datePublished")',
        re.DOTALL,
    )
    m = pat.search(html)
    if not m:
        return html, False
    if '"image":' in html[m.start():m.end() + 800]:
        # Already has image
        already_speak = '"speakable"' in html[m.start():m.end() + 1200]
        if already_speak:
            return html, False
    indent = m.group(2)
    insertion = f'\n{indent}"image": "{og_image_url}",'
    new_html = html[:m.end(1)] + insertion + html[m.end(1):]
    # Also append speakable after publisher block — find publisher object closing
    speak = (
        f',\n{indent}"speakable": {{\n'
        f'{indent}    "@type": "SpeakableSpecification",\n'
        f'{indent}    "cssSelector": [\n'
        f'{indent}        ".takeaways-box",\n'
        f'{indent}        ".faq-a"\n'
        f'{indent}    ]\n'
        f'{indent}}}'
    )
    pat2 = re.compile(
        r'("publisher":\s*\{\s*\n[\s\S]*?"url":\s*"https://tabiji\.ai/"\s*\n\s*\})',
        re.DOTALL,
    )
    m2 = pat2.search(new_html)
    if m2 and '"speakable"' not in new_html[m2.end():m2.end() + 400]:
        new_html = new_html[:m2.end()] + speak + new_html[m2.end():]
    return new_html, True


def og_image_url(city_slug: str) -> str:
    return f"https://img.tabiji.ai/scams-{city_slug}-og.jpg"


def process(city: str) -> dict:
    path = SCAMS / city / "index.html"
    html = path.read_text()
    out = {"city": city, "before_bytes": len(html), "deltas": []}

    h, m, l = severity_counts(html)
    mins = reading_time(html)
    scams = scam_titles_with_severity(html)
    if len(scams) != h + m + l:
        out["deltas"].append(f"WARN scam-count {len(scams)} != sev-sum {h+m+l}")

    html, did = upgrade_hero(html, h, m, l, mins)
    if did:
        out["deltas"].append(f"hero(+sev,+rt {mins}min)")

    html, did = upgrade_cross_links(html, "au", "Australia", DISPLAY[city])
    if did:
        out["deltas"].append("cross-links")

    html, did = upgrade_takeaways(html)
    if did:
        out["deltas"].append("takeaways-box")

    html, did = upgrade_toc(html, scams)
    if did:
        out["deltas"].append(f"toc(+{len(scams)} badges)")

    html, did = upgrade_section_heading(html)
    if did:
        out["deltas"].append("share-btn")

    html, did = upgrade_mid_cta(html, DISPLAY[city])
    if did:
        out["deltas"].append("mid-cta")

    html, did = upgrade_emergency_id(html)
    if did:
        out["deltas"].append("#emergency")

    html, did = upgrade_floats(html)
    if did:
        out["deltas"].append("emergency-fab+btt")

    html, did = upgrade_article_schema(html, og_image_url(city))
    if did:
        out["deltas"].append("schema(image+speakable)")

    if html != path.read_text():
        path.write_text(html)
        out["wrote"] = True
    else:
        out["wrote"] = False
    out["after_bytes"] = len(html)
    return out


def main():
    results = [process(c) for c in CITIES]
    for r in results:
        print(json.dumps(r))
    total_deltas = sum(len(r["deltas"]) for r in results)
    wrote = sum(1 for r in results if r.get("wrote"))
    print(f"\n[summary] wrote={wrote}/{len(CITIES)} files, {total_deltas} deltas")


if __name__ == "__main__":
    main()
