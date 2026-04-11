#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPARE_DIR = REPO_ROOT / "compare"
DATA_DIR = REPO_ROOT / "compare-data"
API_COMPARE_DIR = REPO_ROOT / "api" / "v1" / "compare"
INVENTORY_PATH = COMPARE_DIR / "inventory.json"

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


def viator_search_url(query: str) -> str:
    q = query.replace(" ", "+")
    return f"https://www.viator.com/search/{q}?pid={VIATOR_PID}&mcid={VIATOR_MCID}&medium=link"


def build_viator_html(dest1: str, dest2: str) -> str:
    return f"""<section class="viator-section">
        <h2>&#127903;&#65039; Book Tours & Experiences</h2>
        <p class="viator-subtitle">Hand-picked tours and activities for both destinations — book with free cancellation</p>
        <div class="viator-cards">
      <a class="viator-card" href="{viator_search_url(dest1 + ' tours')}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">Explore {dest1}</span>
        <span class="tour-name">{dest1} Tours & Activities →</span>
      </a>
      <a class="viator-card" href="{viator_search_url(dest1 + ' day trips')}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">{dest1} Day Trip</span>
        <span class="tour-name">{dest1} Day Trips & Excursions</span>
      </a>
      <a class="viator-card" href="{viator_search_url(dest2 + ' tours')}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">Explore {dest2}</span>
        <span class="tour-name">{dest2} Tours & Activities →</span>
      </a>
      <a class="viator-card" href="{viator_search_url(dest2 + ' day trips')}" target="_blank" rel="noopener sponsored">
        <span class="tour-type">{dest2} Day Trip</span>
        <span class="tour-name">{dest2} Day Trips & Excursions</span>
      </a>
        </div>
        <p class="viator-powered">Experiences via Viator — free cancellation on most tours</p>
      </section>"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data) -> None:
    write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def load_json(path: Path):
    return json.loads(read_text(path))


def find_tag_block(html: str, marker: str, tag: str, start_at: int = 0) -> Tuple[str, int, int]:
    start = html.find(marker, start_at)
    if start == -1:
        raise ValueError(f"Marker not found: {marker}")
    return extract_balanced_tag(html, start, tag)


def extract_balanced_tag(html: str, start: int, tag: str) -> Tuple[str, int, int]:
    open_re = re.compile(rf"<(?:{tag})\b", re.I)
    close_re = re.compile(rf"</(?:{tag})>", re.I)
    pos = start
    depth = 0
    first_open = open_re.search(html, pos)
    if not first_open or first_open.start() != start:
        raise ValueError(f"Expected <{tag}> at index {start}")
    pos = start
    while True:
        o = open_re.search(html, pos)
        c = close_re.search(html, pos)
        if not c:
            raise ValueError(f"Unclosed <{tag}> block starting at {start}")
        if o and o.start() < c.start():
            depth += 1
            pos = o.end()
        else:
            depth -= 1
            pos = c.end()
            if depth == 0:
                return html[start:pos], start, pos


def extract_jsonld_blocks(head_html: str) -> List[Dict]:
    blocks = []
    for match in re.finditer(r'<script type="application/ld\+json">\s*([\s\S]*?)\s*</script>', head_html):
        raw = match.group(1)
        try:
            blocks.append(json.loads(raw))
        except Exception:
            blocks.append({"parseError": True, "raw": raw})
    return blocks


def inner_html(block: str, tag: str) -> str:
    block = block.strip()
    open_end = block.find(">") + 1
    close_start = block.lower().rfind(f"</{tag.lower()}>")
    return block[open_end:close_start]


def extract_head_field(head_html: str, pattern: str, label: str) -> str:
    match = re.search(pattern, head_html, re.I | re.S)
    if not match:
        raise ValueError(f"Missing {label}")
    return match.group(1).strip()


def extract_meta_content(head_html: str, attr: str, value: str, label: str) -> str:
    tag_re = re.compile(r"<meta\b[^>]*>", re.I)
    for match in tag_re.finditer(head_html):
        tag = match.group(0)
        if re.search(rf'{attr}="{re.escape(value)}"', tag, re.I):
            content = re.search(r'content="([^"]*)"', tag, re.I)
            if content:
                return content.group(1).strip()
    raise ValueError(f"Missing {label}")


def extract_link_href(head_html: str, rel_value: str, label: str) -> str:
    tag_re = re.compile(r"<link\b[^>]*>", re.I)
    for match in tag_re.finditer(head_html):
        tag = match.group(0)
        if re.search(rf'rel="{re.escape(rel_value)}"', tag, re.I):
            href = re.search(r'href="([^"]*)"', tag, re.I)
            if href:
                return href.group(1).strip()
    raise ValueError(f"Missing {label}")


def extract_page(html_path: Path) -> Dict:
    html = read_text(html_path)
    slug = html_path.parent.name
    head = extract_head_field(html, r"<head>([\s\S]*?)</head>", "head block")
    body = extract_head_field(html, r"<body>([\s\S]*?)</body>", "body block")

    style_css = extract_head_field(head, r"<style>([\s\S]*?)</style>", "style block")
    title = extract_head_field(head, r"<title>(.*?)</title>", "title")
    meta_description = extract_meta_content(head, "name", "description", "meta description")
    og_title = extract_meta_content(head, "property", "og:title", "og:title")
    og_description = extract_meta_content(head, "property", "og:description", "og:description")
    og_image = extract_meta_content(head, "property", "og:image", "og:image")
    twitter_title = extract_meta_content(head, "name", "twitter:title", "twitter:title")
    twitter_description = extract_meta_content(head, "name", "twitter:description", "twitter:description")
    twitter_image = extract_meta_content(head, "name", "twitter:image", "twitter:image")
    published_time = extract_meta_content(head, "property", "article:published_time", "published time")
    modified_time = extract_meta_content(head, "property", "article:modified_time", "modified time")
    canonical = extract_link_href(head, "canonical", "canonical")

    jsonld = extract_jsonld_blocks(head)
    article_schema = next((b for b in jsonld if b.get("@type") == "Article"), None)
    breadcrumb_schema = next((b for b in jsonld if b.get("@type") == "BreadcrumbList"), None)
    faq_schema = next((b for b in jsonld if b.get("@type") == "FAQPage"), None)
    if not article_schema or not breadcrumb_schema or not faq_schema:
        raise ValueError(f"{slug}: missing required JSON-LD blocks")

    nav_block, _, _ = find_tag_block(body, "<nav>", "nav")
    hero_block, _, _ = find_tag_block(body, '<section class="hero">', "section")
    toc_mobile_block, _, toc_mobile_end = find_tag_block(body, '<div class="toc-mobile-sticky"', "div")
    methodology_block, _, _ = find_tag_block(body, '<div class="methodology-box">', "div")
    toc_sidebar_block, _, _ = find_tag_block(body, '<aside class="toc-sidebar">', "aside")
    photo_grid_block, _, photo_end = find_tag_block(body, '<div class="photo-grid">', "div")
    verdict_block, _, verdict_end = find_tag_block(body, '<div class="verdict-box">', "div", start_at=photo_end)
    comparison_block, _, comparison_end = find_tag_block(body, '<div class="comparison-section">', "div", start_at=verdict_end)

    deep_dives = []
    cursor = comparison_end
    while True:
        idx = body.find('<section class="deep-dive">', cursor)
        if idx == -1:
            break
        block, _, cursor = extract_balanced_tag(body, idx, "section")
        deep_dives.append(block)

    faq_block, _, faq_end = find_tag_block(body, '<section class="faq-section">', "section")
    cta_block, _, _ = find_tag_block(body, '<div class="cta-section">', "div", start_at=faq_end)
    footer_block, _, footer_end = find_tag_block(body, '<footer>', "footer")

    script_blocks = [m.group(0) for m in re.finditer(r"<script[\s\S]*?</script>", body[footer_end:])]

    toc_items = [
        {"href": m.group(1), "label": m.group(2)}
        for m in re.finditer(r'<li><a href="([^"]+)">([\s\S]*?)</a></li>', toc_sidebar_block)
    ]

    faq_items = [
        {"question": re.sub(r"<[^>]+>", "", m.group(1)).strip(), "answer": re.sub(r"<[^>]+>", "", m.group(2)).strip()}
        for m in re.finditer(r'<div class="faq-item">\s*<h3>([\s\S]*?)</h3>\s*<p>([\s\S]*?)</p>\s*</div>', faq_block)
    ]

    api_json = load_json(API_COMPARE_DIR / f"{slug}.json")

    return {
        "slug": slug,
        "pageType": "compare-leaf",
        "status": "published",
        "destinations": {
            "destination1": api_json["destination1"],
            "destination2": api_json["destination2"],
        },
        "seo": {
            "title": title,
            "metaDescription": meta_description,
            "ogTitle": og_title,
            "ogDescription": og_description,
            "ogImage": og_image,
            "twitterTitle": twitter_title,
            "twitterDescription": twitter_description,
            "twitterImage": twitter_image,
            "publishedTime": published_time,
            "modifiedTime": modified_time,
            "canonical": canonical,
        },
        "schema": {
            "article": article_schema,
            "breadcrumb": breadcrumb_schema,
            "faq": faq_schema,
        },
        "shell": {
            "styleCss": style_css,
            "navHtml": nav_block,
            "footerHtml": footer_block,
            "scripts": script_blocks,
        },
        "content": {
            "heroHtml": hero_block,
            "tocMobileHtml": toc_mobile_block,
            "methodologyHtml": methodology_block,
            "tocSidebarHtml": toc_sidebar_block,
            "tocItems": toc_items,
            "photoGridHtml": photo_grid_block,
            "verdictHtml": verdict_block,
            "comparisonHtml": comparison_block,
            "deepDiveHtml": deep_dives,
            "faqHtml": faq_block,
            "faqItems": faq_items,
            "ctaHtml": cta_block,
        },
    }


def render_page(data: Dict) -> str:
    seo = data["seo"]
    schema = data["schema"]
    shell = data["shell"]
    content = data["content"]
    rich = data.get("richContent", {})
    dest1 = data["destinations"]["destination1"]
    dest2 = data["destinations"]["destination2"]
    slug = data["slug"]
    d1slug = dest1.lower().replace(' ', '-')
    d2slug = dest2.lower().replace(' ', '-')

    # ── Score ticker ──
    d1_score = rich.get("dest1Score", 0)
    d2_score = rich.get("dest2Score", 0)
    tie_count = rich.get("tieCount", 0)
    score_ticker_html = f'''<div class="score-ticker" id="score-ticker">
<span><span class="score-label score-dest1">{html.escape(dest1)} {d1_score}</span> <span class="score-divider">&mdash;</span> <span class="score-label score-dest2">{d2_score} {html.escape(dest2)}</span></span>
<span class="score-divider">|</span>
<span class="score-section" id="ticker-section">{tie_count} ties</span>
</div>''' if d1_score or d2_score else ""

    # ── Quick answers ──
    qa_html = ""
    qa_items = rich.get("quickAnswers", [])
    if qa_items:
        qa_cards = ""
        for qa in qa_items[:6]:
            winner_raw = qa.get("winner", "Tie")
            if winner_raw == dest1:
                wcls = "dest1"
            elif winner_raw == dest2:
                wcls = "dest2"
            else:
                wcls = "tie"
            link_id = qa.get("linkId", "")
            href = f'href="#{html.escape(link_id)}"' if link_id else ""
            qa_cards += f'''<a class="qa-card" {href}>
<div class="qa-q">{html.escape(qa.get("question",""))}</div>
<div class="qa-a">{html.escape(qa.get("answer",""))}</div>
<span class="qa-winner {wcls}">{html.escape(winner_raw)} wins</span>
</a>\n'''
        qa_html = f'<div class="quick-answers" id="quick-answers"><h2>&#9889; Quick Answers</h2><div class="qa-grid">{qa_cards}</div></div>'

    # ── Visual scorecard ──
    sc_html = ""
    sc_rows = rich.get("scorecardRows", [])
    if sc_rows:
        rows_html = ""
        for row in sc_rows:
            w = row.get("winner", "Tie")
            if w == dest1:
                wcls = "dest1"
            elif w == dest2:
                wcls = "dest2"
            else:
                wcls = "tie"
            rows_html += f'''<div class="sc-row">
<span class="sc-cat">{html.escape(row.get("emoji",""))} {html.escape(row.get("label",""))}</span>
<span class="sc-bars"><span class="sc-bar-wrap"><span class="sc-bar dest1" style="width:{row.get("dest1Pct",50)}%"></span></span><span class="sc-bar-wrap"><span class="sc-bar dest2" style="width:{row.get("dest2Pct",50)}%"></span></span></span>
<span class="sc-winner {wcls}">{html.escape(w)}</span>
</div>\n'''
        sc_html = f'''<div class="scorecard" id="scorecard">
<h2>&#128202; Visual Scorecard</h2>
<div class="scorecard-overall">
<div class="scorecard-city dest1"><div class="city-name">{html.escape(dest1)}</div><div class="city-score">{d1_score}</div></div>
<div class="scorecard-vs">vs</div>
<div class="scorecard-city dest2"><div class="city-name">{html.escape(dest2)}</div><div class="city-score">{d2_score}</div></div>
</div>
<div class="scorecard-rows">{rows_html}</div>
</div>'''

    # ── Cost widget ──
    cost_html = ""
    cost_data = rich.get("costTable", {})
    if cost_data.get("items"):
        rows = ""
        for item in cost_data["items"]:
            rows += f'<tr><td>{html.escape(item.get("label",""))}</td><td>{html.escape(item.get("dest1Price",""))}</td><td>{html.escape(item.get("dest2Price",""))}</td></tr>\n'
        savings = cost_data.get("savingsSummary", "")
        savings_html = f'<div class="cost-savings">&#127942; {html.escape(savings)}</div>' if savings else ""
        cost_html = f'''<div class="cost-widget" id="cost-widget">
<h2>&#128176; Daily Cost Comparison</h2>
<table class="cost-table"><thead><tr><th>Expense</th><th>{html.escape(dest1)}</th><th>{html.escape(dest2)}</th></tr></thead>
<tbody>{rows}</tbody></table>
{savings_html}</div>'''

    # ── Weather chart ──
    weather_html = ""
    weather_data = rich.get("weatherData", [])
    if weather_data:
        months_html = ""
        for m in weather_data:
            flag = m.get("flag", "")
            cls = f' {flag}' if flag in ("best", "avoid") else ""
            months_html += f'<div class="weather-month{cls}"><div class="wm-label">{html.escape(m.get("month",""))}</div><div class="wm-temps"><div class="wm-dest1">{html.escape(m.get("dest1Temp",""))}</div><div class="wm-dest2">{html.escape(m.get("dest2Temp",""))}</div></div></div>\n'
        weather_html = f'''<div class="weather-chart" id="weather">
<h2>&#127780; When to Visit</h2>
<p class="weather-note">Average high temperatures (&deg;C). <span style="color:var(--sage)">Green</span> = best months, <span style="color:var(--terracotta)">orange</span> = avoid.</p>
<div class="weather-months">{months_html}</div>
<div class="weather-legend"><span><span class="legend-dot dest1"></span> {html.escape(dest1)}</span><span><span class="legend-dot dest2"></span> {html.escape(dest2)}</span><span><span class="legend-dot best"></span> Best months</span></div>
</div>'''

    # ── Itineraries ──
    itin_html = ""
    itins = rich.get("itineraries", [])
    if itins:
        tabs_html = ""
        panels_html = ""
        for i, itin in enumerate(itins):
            active = " active" if i == 0 else ""
            tabs_html += f'<button class="ux-itin-tab{active}" data-panel="itin-{i}">{html.escape(itin.get("tabLabel",""))}</button>\n'
            days_html = ""
            for day in itin.get("days", []):
                days_html += f'<div class="ux-itin-day"><span class="day-num">{html.escape(day.get("dayNum",""))}</span><span class="day-desc">{html.escape(day.get("desc",""))}</span></div>\n'
            tip = itin.get("tip", "")
            tip_html = f'<p class="ux-itin-tip">&#128161; {html.escape(tip)}</p>' if tip else ""
            panels_html += f'<div class="ux-itin-panel{active}" id="itin-{i}"><div class="ux-itin-card"><h3>{html.escape(itin.get("title",""))}</h3>{days_html}{tip_html}</div></div>\n'
        itin_html = f'<div class="ux-itineraries" id="sample-itineraries"><h2>&#128197; Sample Itineraries</h2><div class="ux-itin-tabs">{tabs_html}</div>{panels_html}</div>'

    # ── Deep dives (collapsible) ──
    deep_dives_html = ""
    for i, dd_raw in enumerate(content.get("deepDiveHtml", [])):
        # Extract title, determine if it's the decision framework
        title_match = re.search(r'<h2[^>]*id="([^"]*)"[^>]*>(.*?)</h2>', dd_raw, re.S)
        if not title_match:
            title_match = re.search(r'<h2[^>]*>(.*?)</h2>', dd_raw, re.S)

        section_id = title_match.group(1) if title_match and title_match.lastindex >= 1 else f"section-{i}"

        # Check if this is the decision framework (keep it open)
        is_decision = "decision-framework" in dd_raw or "decision_framework" in section_id or "the-decision-framework" in dd_raw
        open_class = " open" if (i == 0 or is_decision) else ""

        # Extract winner from section-winner block
        winner_match = re.search(r'<strong>Winner:</strong>\s*(\w[\w\s]*)', dd_raw)
        winner_text = winner_match.group(1).strip() if winner_match else "—"
        if winner_text == dest1:
            badge_cls = "dest1"
        elif winner_text == dest2:
            badge_cls = "dest2"
        else:
            badge_cls = "tie"

        # Extract summary (first <p> tag content, truncated)
        summary_match = re.search(r'<p>(.*?)</p>', dd_raw, re.S)
        summary_text = ""
        if summary_match:
            raw = re.sub(r'<[^>]+>', '', summary_match.group(1))
            summary_text = html.unescape(raw)[:180].rsplit(' ', 1)[0] + "…" if len(raw) > 180 else html.unescape(raw)

        # Get the full section title HTML
        full_title = title_match.group(0) if title_match else ""

        # Get body content (everything after the first h2)
        h2_end = dd_raw.find('</h2>')
        body_content = dd_raw[h2_end+5:] if h2_end != -1 else dd_raw
        # Remove wrapping <section> tags
        body_content = re.sub(r'^<section[^>]*>', '', body_content)
        body_content = re.sub(r'</section>\s*$', '', body_content)

        badge_html = f'<span class="dd-winner-badge {badge_cls}">{html.escape(winner_text)}</span>' if not is_decision else ""

        # data-winner attribute for CSS hooks
        dw_attr = f' data-winner="{badge_cls}"' if not is_decision else ' data-winner="depends"'

        # Photo pair for this section
        photo_pair_html = ""
        if not is_decision and i < 5:  # First 5 deep-dives get photo pairs
            # Use section-specific images if available, else fall back to dest images
            d1_img = f"https://img.tabiji.ai/compare/{slug}/section-{i+1}-dest1.jpg"
            d2_img = f"https://img.tabiji.ai/compare/{slug}/section-{i+1}-dest2.jpg"
            d1_fallback = f"https://img.tabiji.ai/compare/{slug}/dest1.jpg"
            d2_fallback = f"https://img.tabiji.ai/compare/{slug}/dest2.jpg"
            # Extract section title for alt text
            sec_title = re.sub(r'<[^>]+>', '', full_title).strip() if full_title else f"Section {i+1}"
            sec_title = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u27bf\u2702-\u27b0]+\s*', '', sec_title).strip()
            photo_pair_html = f'''<div class="photo-pair">
<div><img src="{d1_img}" alt="{html.escape(dest1)} — {html.escape(sec_title)}" loading="lazy" onerror="this.src='{d1_fallback}'"><p class="photo-caption">{html.escape(dest1)}</p></div>
<div><img src="{d2_img}" alt="{html.escape(dest2)} — {html.escape(sec_title)}" loading="lazy" onerror="this.src='{d2_fallback}'"><p class="photo-caption">{html.escape(dest2)}</p></div>
</div>'''

        # Convert section-winner to tabiji-verdict if present
        body_content = body_content.replace(
            '<div class="section-winner"><h3>Winner takeaway</h3>',
            '<div class="tabiji-verdict"><strong>tabiji verdict:</strong> '
        )
        # Close the tabiji-verdict properly
        body_content = re.sub(
            r'</ul>\s*</div>\s*$', '</ul></div>',
            body_content
        )

        deep_dives_html += f'''<section class="deep-dive{open_class}"{dw_attr} id="sec-{section_id}">
<div class="dd-header" onclick="toggleSection(this.parentElement)">
{full_title}
<div class="dd-header-meta">
{badge_html}
<span class="dd-toggle">&#9662;</span>
</div>
</div>
<p class="dd-summary">{html.escape(summary_text)}</p>
<div class="dd-body"><div class="dd-content">
{photo_pair_html}
{body_content}
</div></div>
</section>\n'''

    # ── Personalization widget ──
    personalize_html = ""
    recs = rich.get("personalizeRecommendations", {})
    if recs:
        fallbacks_js = json.dumps({
            "food": f"For <strong>food lovers</strong>, compare the food sections below for {html.escape(dest1)} vs {html.escape(dest2)}.",
            "culture": f"For <strong>culture seekers</strong>, both offer rich experiences — scroll to the culture section for specifics.",
            "beaches": f"If <strong>beaches</strong> matter, check the beaches section for a detailed comparison.",
            "nightlife": f"For <strong>nightlife</strong>, see the nightlife section for specific venue recommendations.",
        }, ensure_ascii=False)
        recs_js = json.dumps(recs, ensure_ascii=False)
        personalize_html = f'''<div class="personalize-widget" id="personalize">
<h2>&#127919; Tell me about your trip</h2>
<div class="personalize-row"><label>Traveling&hellip;</label><div class="pill-group" data-group="style">
<button class="personalize-pill" data-val="solo" onclick="selectPill(this)">Solo</button>
<button class="personalize-pill" data-val="couple" onclick="selectPill(this)">Couple</button>
<button class="personalize-pill" data-val="family" onclick="selectPill(this)">Family</button>
<button class="personalize-pill" data-val="friends" onclick="selectPill(this)">Friends</button>
</div></div>
<div class="personalize-row"><label>Budget&hellip;</label><div class="pill-group" data-group="budget">
<button class="personalize-pill" data-val="backpacker" onclick="selectPill(this)">Backpacker</button>
<button class="personalize-pill" data-val="midrange" onclick="selectPill(this)">Mid-range</button>
<button class="personalize-pill" data-val="luxury" onclick="selectPill(this)">Luxury</button>
</div></div>
<div class="personalize-row"><label>I care about&hellip;</label><div class="pill-group" data-group="priority">
<button class="personalize-pill" data-val="food" onclick="selectPill(this)">Food</button>
<button class="personalize-pill" data-val="culture" onclick="selectPill(this)">Culture</button>
<button class="personalize-pill" data-val="beaches" onclick="selectPill(this)">Beaches</button>
<button class="personalize-pill" data-val="nightlife" onclick="selectPill(this)">Nightlife</button>
</div></div>
<div class="personalize-result" id="personalize-result"></div>
</div>
<script>
var personState={{}};
var recommendations={recs_js};
var fallbacks={fallbacks_js};
function selectPill(btn){{var g=btn.parentElement.getAttribute('data-group');btn.parentElement.querySelectorAll('.personalize-pill').forEach(function(p){{p.classList.remove('selected')}});btn.classList.add('selected');personState[g]=btn.getAttribute('data-val');showRecommendation()}}
function showRecommendation(){{var s=personState;if(!s.style||!s.budget||!s.priority)return;var key=s.style+'_'+s.budget+'_'+s.priority;var result=document.getElementById('personalize-result');var text=recommendations[key]||fallbacks[s.priority]||'Both destinations are excellent. Scroll down to compare specific categories.';result.innerHTML=text;result.classList.add('visible')}}
</script>'''

    # ── Related comparisons ──
    related_html = ""
    related = rich.get("relatedComparisons", [])
    if related:
        cards = ""
        for r in related[:3]:
            rslug = r.get("slug", "")
            cards += f'''<a class="also-card" href="/compare/{html.escape(rslug)}/">
<div class="also-card-body"><div class="also-card-title">{html.escape(r.get("title",""))}</div><div class="also-card-desc">{html.escape(r.get("desc",""))}</div></div></a>\n'''
        related_html = f'<div class="also-compared" id="also-compared"><h2>&#128101; Travelers Also Compared</h2><div class="also-grid">{cards}</div></div>'

    return f"""<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
<link href="/favicon.ico" rel="icon" type="image/x-icon"/>
<link href="https://img.tabiji.ai/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="https://img.tabiji.ai/icon-192.png" rel="icon" sizes="192x192" type="image/png"/>
<title>{seo['title']}</title>
<meta content="{seo['metaDescription']}" name="description"/>
<meta content="{seo['ogTitle']}" property="og:title"/>
<meta content="{seo['ogDescription']}" property="og:description"/>
<meta content="article" property="og:type"/>
<meta content="{seo['canonical']}" property="og:url"/>
<meta content="{seo['ogImage']}" property="og:image"/>
<meta content="tabiji.ai" property="og:site_name"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{seo['twitterTitle']}" name="twitter:title"/>
<meta content="{seo['twitterDescription']}" name="twitter:description"/>
<meta content="{seo['twitterImage']}" name="twitter:image"/>
<meta content="{seo['publishedTime']}" property="article:published_time"/>
<meta content="{seo['modifiedTime']}" property="article:modified_time"/>
<meta content="index, follow, max-image-preview:large" name="robots"/>
<link href="{seo['canonical']}" rel="canonical"/>
<!-- Schema: Article -->
<script type="application/ld+json">{json.dumps(schema['article'], ensure_ascii=False, indent=4)}</script>
<!-- Schema: BreadcrumbList -->
<script type="application/ld+json">{json.dumps(schema['breadcrumb'], ensure_ascii=False, indent=4)}</script>
<!-- Schema: FAQPage -->
<script type="application/ld+json">{json.dumps(schema['faq'], ensure_ascii=False, indent=4)}</script>
<style>
{shell['styleCss']}
{VIATOR_CSS}
</style>
<!-- @include:shared-head:start -->
<link rel="stylesheet" href="/assets/shared-shell.css">
<script defer src="/assets/shared-shell.js"></script>
<!-- @include:shared-head:end -->
</head>
<body>
<!-- @include:nav:start -->
{shell['navHtml']}
<!-- @include:nav:end -->
{score_ticker_html}
{content['tocMobileHtml']}
{content['heroHtml']}
<div class="content-wrapper">
{content['tocSidebarHtml']}
<div class="article-content">
{content['methodologyHtml']}
{content['photoGridHtml']}
{qa_html}
{personalize_html}
{content['verdictHtml']}
{sc_html}
{cost_html}
{weather_html}
{content['comparisonHtml']}
{deep_dives_html}
{itin_html}
{content['faqHtml']}
{content['ctaHtml']}
{related_html}
{build_viator_html(dest1, dest2)}
</div><!-- /article-content -->
</div><!-- /content-wrapper -->
<!-- @include:footer:start -->
{shell['footerHtml']}
<!-- @include:footer:end -->
{chr(10).join(shell['scripts'])}
</body>
</html>
"""


def text_content(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = html.unescape(value)
    value = value.replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip()


def has_meaningful_text(value: str, min_len: int = 8) -> bool:
    text = text_content(value)
    return len(text) >= min_len and text not in {"—", "-", "Tie", "Depends"}


def compare_winner_aliases(data: Dict) -> set[str]:
    destination1 = data["destinations"]["destination1"]
    destination2 = data["destinations"]["destination2"]
    aliases = {destination1, destination2, "Tie", "Depends", "—", "-"}
    tokens = [destination1, destination2]
    for name in tokens:
        parts = name.split()
        aliases.add(parts[-1])
        aliases.add(name.replace(" ", ""))
        if len(parts) > 1:
            aliases.add(parts[0])
        if len(name) <= 5:
            aliases.add(name.upper())
    hardcoded = {
        "Mexico City": {"CDMX"},
        "Buenos Aires": {"BA"},
        "Guadalajara": {"GDL"},
        "Hong Kong": {"HK"},
        "New Zealand": {"NZ"},
        "South Korea": {"Korea"},
    }
    aliases.update(hardcoded.get(destination1, set()))
    aliases.update(hardcoded.get(destination2, set()))
    return aliases


def validate_compare_content(data: Dict) -> List[str]:
    errors = []
    content = data.get("content", {})
    verdict_html = content.get("verdictHtml", "")
    cta_html = content.get("ctaHtml", "")
    comparison_html = content.get("comparisonHtml", "")

    placeholder_patterns = [
        (r"better if you want\s*\.", "verdict summary contains an empty 'better if you want' clause"),
        (r"<li><strong>Choose [^:]+:</strong>\s*</li>", "verdict takeaways contain an empty choose bullet"),
        (r"<div class=\"verdict-card\">\s*<h3>[^<]+</h3>\s*<p>\s*</p>\s*</div>", "verdict cards contain empty body copy"),
        (r"Who this matters for:</strong>[^<]* between\s+and\s+\.", "deep-dive winner note contains placeholder destination text"),
    ]
    for pattern, message in placeholder_patterns:
        if re.search(pattern, verdict_html) or any(re.search(pattern, block) for block in content.get("deepDiveHtml", [])):
            errors.append(message)

    if not has_meaningful_text(verdict_html, min_len=40):
        errors.append("verdictHtml must contain meaningful text")

    verdict_cards = re.findall(r'<div class="verdict-card">([\s\S]*?)</div>', verdict_html)
    if len(verdict_cards) < 2:
        errors.append("verdictHtml must contain at least two verdict cards")
    for idx, card in enumerate(verdict_cards, start=1):
        if not has_meaningful_text(card, min_len=20):
            errors.append(f"verdict card {idx} must contain meaningful text")

    comparison_rows = re.findall(r"<tr>([\s\S]*?)</tr>", comparison_html)
    if len(comparison_rows) < 4:
        errors.append("comparisonHtml must contain at least 4 table rows")
    valid_winners = compare_winner_aliases(data)
    for idx, row in enumerate(comparison_rows[1:], start=1):
        cells = [text_content(cell) for cell in re.findall(r"<t[dh][^>]*>([\s\S]*?)</t[dh]>", row)]
        if len(cells) != 4:
            errors.append(f"comparison row {idx} must contain exactly 4 cells")
            continue
        if any(not cell for cell in cells[:3]):
            errors.append(f"comparison row {idx} contains empty required cells")
        winner = cells[3]
        if winner not in valid_winners:
            errors.append(f"comparison row {idx} has invalid winner value: {winner}")

    if not has_meaningful_text(cta_html, min_len=30):
        errors.append("ctaHtml must contain meaningful text")
    cta_links = re.findall(r"<a [^>]*>([\s\S]*?)</a>", cta_html)
    if len(cta_links) < 2:
        errors.append("ctaHtml must contain at least two CTA links")
    for idx, label in enumerate(cta_links, start=1):
        if len(text_content(label)) < 8:
            errors.append(f"CTA link {idx} text is too short")

    for idx, question in enumerate(content.get("faqItems", []), start=1):
        if len(question.get("question", "").strip()) < 10:
            errors.append(f"faq item {idx} question is too short")
        if len(question.get("answer", "").strip()) < 30:
            errors.append(f"faq item {idx} answer is too short")

    for idx, block in enumerate(content.get("deepDiveHtml", []), start=1):
        if not has_meaningful_text(block, min_len=120):
            errors.append(f"deep-dive section {idx} lacks meaningful text")
        winner_block = re.search(r'<div class="section-winner">([\s\S]*?)</div>', block)
        if not winner_block:
            continue
        winner_html = winner_block.group(1)
        winner_items = [text_content(item) for item in re.findall(r"<li>([\s\S]*?)</li>", winner_html)]
        if len(winner_items) < 3:
            errors.append(f"deep-dive section {idx} must contain 3 winner bullets")
            continue
        for bullet_idx, item in enumerate(winner_items[:3], start=1):
            if item.endswith(":") or item.endswith("between and ."):
                errors.append(f"deep-dive section {idx} winner bullet {bullet_idx} contains placeholder text")

    return errors


def validate_source(data: Dict) -> List[str]:
    errors = []
    for field in ["slug", "pageType", "status", "destinations", "seo", "schema", "shell", "content"]:
        if field not in data:
            errors.append(f"missing top-level field: {field}")
    if data.get("pageType") != "compare-leaf":
        errors.append("pageType must equal compare-leaf")
    if not re.fullmatch(r"[a-z0-9-]+", data.get("slug", "")):
        errors.append("slug must be kebab-case")
    content = data.get("content", {})
    if len(content.get("deepDiveHtml", [])) < 1:
        errors.append("deepDiveHtml must contain at least 1 section")
    if len(content.get("faqItems", [])) < 1:
        errors.append("faqItems must contain at least 1 item")
    if len(content.get("tocItems", [])) < 1:
        errors.append("tocItems must contain at least 1 item")
    seo = data.get("seo", {})
    for field in ["title", "metaDescription", "ogImage", "canonical"]:
        if not str(seo.get(field, "")).strip():
            errors.append(f"seo.{field} is required")
    shell = data.get("shell", {})
    for field in ["styleCss", "navHtml", "footerHtml"]:
        if not str(shell.get(field, "")).strip():
            errors.append(f"shell.{field} is required")
    errors.extend(validate_compare_content(data))
    return errors


def validate_rendered_output(data: Dict, html: str) -> List[str]:
    errors = []
    if data["seo"]["title"] not in html:
        errors.append("rendered HTML missing title")
    if 'class="verdict-box"' not in html:
        errors.append("rendered HTML missing verdict-box")
    if 'class="comparison-section"' not in html:
        errors.append("rendered HTML missing comparison-section")
    if len(re.findall(r'class="deep-dive[" ]', html)) != len(data["content"]["deepDiveHtml"]):
        errors.append("deep-dive count mismatch")
    if html.count('class="faq-item"') != len(data["content"]["faqItems"]):
        errors.append("faq-item count mismatch")
    if 'application/ld+json' not in html:
        errors.append("rendered HTML missing JSON-LD")
    return errors


def iter_compare_html_files() -> List[Path]:
    return sorted([p / "index.html" for p in COMPARE_DIR.iterdir() if p.is_dir() and (p / "index.html").exists()])


def inventory_slugs() -> List[str]:
    inventory = load_json(INVENTORY_PATH)
    return [card["slug"] for card in inventory["cards"]]


def cmd_extract() -> int:
    count = 0
    for html_path in iter_compare_html_files():
        data = extract_page(html_path)
        out = DATA_DIR / f"{data['slug']}.json"
        write_json(out, data)
        count += 1
    print(f"Backfilled {count} compare leaf JSON files into {DATA_DIR.relative_to(REPO_ROOT)}")
    return 0


def cmd_build() -> int:
    count = 0
    for slug in inventory_slugs():
        data_path = DATA_DIR / f"{slug}.json"
        if not data_path.exists():
            raise SystemExit(f"Missing data file: {data_path}")
        data = load_json(data_path)
        errors = validate_source(data)
        if errors:
            raise SystemExit(f"Source validation failed for {slug}:\n" + "\n".join(errors))
        html = render_page(data)
        output_errors = validate_rendered_output(data, html)
        if output_errors:
            raise SystemExit(f"Output validation failed for {slug}:\n" + "\n".join(output_errors))
        write_text(COMPARE_DIR / slug / "index.html", html)
        count += 1
    print(f"Built {count} compare leaves from structured JSON")
    return 0


def cmd_validate() -> int:
    errors = []
    warnings = []
    slugs = inventory_slugs()
    for slug in slugs:
        data_path = DATA_DIR / f"{slug}.json"
        html_path = COMPARE_DIR / slug / "index.html"
        if not data_path.exists():
            errors.append(f"missing data file: compare-data/{slug}.json")
            continue
        if not html_path.exists():
            errors.append(f"missing leaf html: compare/{slug}/index.html")
            continue
        data = load_json(data_path)
        source_errors = validate_source(data)
        errors.extend(f"{slug}: {err}" for err in source_errors)
        rendered = render_page(data)
        output_errors = validate_rendered_output(data, rendered)
        errors.extend(f"{slug}: {err}" for err in output_errors)
        live = read_text(html_path)
        if live != rendered:
            warnings.append(f"{slug}: live HTML differs from generated output; run build")
    extra_json = sorted(p.stem for p in DATA_DIR.glob("*.json") if p.stem not in slugs)
    if extra_json:
        warnings.append("extra compare-data JSON not in inventory: " + ", ".join(extra_json))
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAILED with {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: compare leaf system valid ({len(slugs)} leaves, {len(warnings)} warning(s))")
    return 0


def main(argv: List[str]) -> int:
    if len(argv) < 2 or argv[1] not in {"extract", "build", "validate"}:
        print("Usage: build_compare.py <extract|build|validate>")
        return 1
    cmd = argv[1]
    if cmd == "extract":
        return cmd_extract()
    if cmd == "build":
        return cmd_build()
    return cmd_validate()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
