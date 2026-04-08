#!/usr/bin/env python3
"""
Batch UX upgrade for compare pages.
Transforms existing pages into the new interactive format with all 13 UX improvements.

Usage:
    python3 scripts/batch-ux-upgrade.py <slug>           # upgrade one page
    python3 scripts/batch-ux-upgrade.py --file slugs.txt # upgrade from file
"""
from __future__ import annotations

import html as html_mod
import json
import re
import sys
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO / "compare"

DEST1_COLOR = "#C0392B"
DEST2_COLOR = "#2E86C1"
TIE_COLOR = "#7A8B6F"


# ─── Extraction helpers ──────────────────────────────────────────────

def read_page(slug: str) -> str:
    p = COMPARE_DIR / slug / "index.html"
    return p.read_text("utf-8")


def strip_tags(s: str) -> str:
    return html_mod.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def extract_head(html: str) -> str:
    m = re.search(r'<head>(.*?)</head>', html, re.DOTALL)
    return m.group(1) if m else ''


def extract_dests(html: str) -> Tuple[str, str]:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not m:
        raise ValueError("No h1")
    raw = strip_tags(m.group(1))
    vm = re.match(r'^(.+?)\s+vs\.?\s+(.+?)(?:\s*[:—–-].+)?$', raw, re.I)
    if vm:
        return vm.group(1).strip(), vm.group(2).strip()
    raise ValueError(f"Cannot parse: {raw}")


def extract_schema_blocks(head: str) -> str:
    """Return all JSON-LD script blocks as-is."""
    return '\n'.join(re.findall(
        r'<!-- Schema:.*?-->\s*<script type="application/ld\+json">.*?</script>',
        head, re.DOTALL
    ))


def extract_seo_meta(head: str) -> Dict[str, str]:
    def meta(attr, val):
        m = re.search(rf'<meta[^>]*{attr}="{re.escape(val)}"[^>]*content="([^"]*)"', head, re.I)
        if not m:
            m = re.search(rf'<meta[^>]*content="([^"]*)"[^>]*{attr}="{re.escape(val)}"', head, re.I)
        return m.group(1) if m else ''

    title_m = re.search(r'<title>(.*?)</title>', head)
    canonical_m = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"', head)

    return {
        'title': title_m.group(1) if title_m else '',
        'description': meta('name', 'description'),
        'ogTitle': meta('property', 'og:title'),
        'ogDescription': meta('property', 'og:description'),
        'ogImage': meta('property', 'og:image'),
        'canonical': canonical_m.group(1) if canonical_m else '',
        'publishedTime': meta('property', 'article:published_time'),
    }


def extract_hero(html: str) -> str:
    m = re.search(r'<section class="hero">(.*?)</section>', html, re.DOTALL)
    return m.group(1).strip() if m else ''


def extract_methodology(html: str) -> str:
    m = re.search(r'<div class="methodology-box">(.*?)</div>', html, re.DOTALL)
    return f'<div class="methodology-box">{m.group(1)}</div>' if m else ''


def extract_photo_grid(html: str) -> str:
    m = re.search(r'<div class="photo-grid">(.*?)</div>\s*</div>', html, re.DOTALL)
    if m:
        return f'<div class="photo-grid">{m.group(1)}</div></div>'
    # Try broader match
    m = re.search(r'(<div class="photo-grid">.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
    return m.group(1) if m else ''


def extract_verdict(html: str) -> str:
    m = re.search(r'(<div class="verdict-box"[^>]*>.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
    if m:
        return m.group(1)
    m = re.search(r'(<div class="verdict-box".*?)\n<div class="comparison-section"', html, re.DOTALL)
    return m.group(1).rstrip() if m else ''


def extract_comparison_table(html: str) -> str:
    m = re.search(r'(<div class="comparison-section">.*?</div>)\s*(?=<section|$)', html, re.DOTALL)
    return m.group(1) if m else ''


def extract_deep_dives(html: str, dest1: str = '', dest2: str = '') -> List[Dict]:
    """Extract each deep-dive section with its heading, id, and full content."""
    sections = []
    pattern = re.compile(
        r'<section class="deep-dive">\s*<h2\s+id="([^"]+)"[^>]*>(.*?)</h2>(.*?)</section>',
        re.DOTALL
    )
    for m in pattern.finditer(html):
        section_id = m.group(1)
        heading = m.group(2).strip()
        body = m.group(3).strip()

        # Skip methodology-like sections
        if section_id in ('how-we-built-this-comparison',):
            continue

        # Extract winner from section-winner block
        winner_m = re.search(r'class="section-winner[^"]*"[^>]*>.*?Winner:\s*(.*?)<', body, re.DOTALL)
        winner_text = strip_tags(winner_m.group(1)) if winner_m else ''

        # Extract tabiji-verdict
        verdict_m = re.search(r'class="tabiji-verdict"[^>]*>(.*?)</div>', body, re.DOTALL)
        verdict_html = verdict_m.group(1) if verdict_m else ''
        verdict_text = strip_tags(verdict_html)[:150] if verdict_html else ''

        # Extract section-winner "Why" text for summary
        why_m = re.search(r'Why:\s*(.*?)</li>', body, re.DOTALL)
        summary = strip_tags(why_m.group(1))[:120] if why_m else verdict_text[:120]

        # Filter sports quotes
        body = re.sub(
            r'<(?:div|blockquote)\s+class="reddit-quote"[^>]*>.*?(?:Goal!|⚽|\d+\'\s).*?</(?:div|blockquote)>',
            '', body, flags=re.DOTALL
        )

        sections.append({
            'id': section_id,
            'heading_html': heading,
            'heading_text': strip_tags(heading),
            'body': body,
            'winner_text': winner_text,
            'summary': summary or f'Compare {strip_tags(heading).split("&")[0].strip()} between the two destinations.',
        })

    return sections


def determine_winner(winner_text: str, dest1: str, dest2: str) -> str:
    wl = winner_text.lower()
    d1l = dest1.lower()
    d2l = dest2.lower()
    if d1l in wl:
        return 'dest1'
    if d2l in wl:
        return 'dest2'
    return 'tie'


def extract_decision_frameworks(html: str) -> str:
    """Extract decision grid (Choose X if...) — take the best one, avoid duplicates."""
    m = re.search(r'(<div class="decision-grid">.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
    return m.group(1) if m else ''


def extract_faq(html: str) -> str:
    m = re.search(r'(<section class="faq-section"[^>]*>.*?</section>)', html, re.DOTALL)
    return m.group(1) if m else ''


def extract_cta(html: str) -> str:
    m = re.search(r'(<div class="cta-section">.*?</div>\s*</div>)', html, re.DOTALL)
    return m.group(1) if m else ''


def extract_viator(html: str) -> str:
    m = re.search(r'(<section class="viator-section">.*?</section>)', html, re.DOTALL)
    return m.group(1) if m else ''


def extract_images(html: str, slug: str) -> Dict[str, str]:
    imgs = {}
    base = f"https://img.tabiji.ai/compare/{slug}"
    for m in re.finditer(r'<img[^>]+src="([^"]+)"', html):
        url = m.group(1)
        if '/compare/' in url and slug in url:
            if 'hero' in url: imgs['hero'] = url
            elif 'dest1' in url: imgs['dest1'] = url
            elif 'dest2' in url: imgs['dest2'] = url
    imgs.setdefault('hero', f"{base}/hero.jpg")
    imgs.setdefault('dest1', f"{base}/dest1.jpg")
    imgs.setdefault('dest2', f"{base}/dest2.jpg")
    return imgs


def get_related(slug: str) -> List[str]:
    inv_path = COMPARE_DIR / "inventory.json"
    if not inv_path.exists():
        return []
    try:
        inv = json.loads(inv_path.read_text("utf-8"))
        items = inv.get('items', []) if isinstance(inv, dict) else inv
        for item in items:
            if isinstance(item, dict) and item.get('slug') == slug:
                return item.get('relatedSlugs', [])[:3]
    except Exception:
        pass
    return []


# ─── Component builders ──────────────────────────────────────────────

CATEGORY_ICONS = {
    'budget': '&#128176;', 'cost': '&#128176;', 'value': '&#128176;',
    'food': '&#127869;', 'dining': '&#127869;', 'drink': '&#127869;',
    'beach': '&#127958;', 'water': '&#127958;',
    'nightlife': '&#127881;', 'entertainment': '&#127881;',
    'culture': '&#127963;', 'architecture': '&#127963;', 'history': '&#127963;', 'art': '&#127963;',
    'safety': '&#128737;', 'security': '&#128737;',
    'transport': '&#128647;', 'getting': '&#128647;',
    'nature': '&#127956;', 'scenery': '&#127956;', 'outdoor': '&#127956;',
    'accommodation': '&#127960;', 'neighborhood': '&#127960;', 'stay': '&#127960;',
    'weather': '&#127780;', 'climate': '&#127780;', 'time': '&#127780;', 'season': '&#127780;',
    'day trip': '&#128506;', 'excursion': '&#128506;',
    'solo': '&#128694;', 'family': '&#128106;',
    'vibe': '&#127961;', 'character': '&#127961;', 'atmosphere': '&#127961;',
}


def icon_for(heading: str) -> str:
    hl = heading.lower()
    for kw, icon in CATEGORY_ICONS.items():
        if kw in hl:
            return icon
    return '&#128204;'


def build_filter_tags(sections: List[Dict]) -> str:
    tags = []
    for s in sections[:8]:
        icon = icon_for(s['heading_text'])
        label = s['heading_text'].split('&')[0].strip()
        # Remove leading emoji from label
        label = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\ufe0f\u200d]+\s*', '', label)
        if len(label) > 15:
            label = label.split()[0]  # first word
        tags.append(f'<button class="filter-tag" data-section="{s["id"]}">{icon} {label}</button>')
    return '\n'.join(tags)


def build_scorecard(sections: List[Dict], dest1: str, dest2: str) -> str:
    rows = []
    d1_wins = d2_wins = ties = 0
    for s in sections:
        w = determine_winner(s['winner_text'], dest1, dest2)
        if w == 'dest1':
            d1_wins += 1
            d1_pct, d2_pct = 85, 55
            winner_html = f'<span class="sc-winner dest1">{dest1}</span>'
        elif w == 'dest2':
            d2_wins += 1
            d1_pct, d2_pct = 55, 85
            winner_html = f'<span class="sc-winner dest2">{dest2}</span>'
        else:
            ties += 1
            d1_pct = d2_pct = 75
            winner_html = '<span class="sc-winner tie">Tie</span>'

        icon = icon_for(s['heading_text'])
        label = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\ufe0f\u200d]+\s*', '', s['heading_text'].split('&')[0].strip())
        if len(label) > 14:
            label = label.split()[0]

        rows.append(f'''<a class="sc-row" href="#{s['id']}">
<span class="sc-cat">{icon} {label}</span>
<span class="sc-bars"><span class="sc-bar-wrap"><span class="sc-bar dest1" style="width:{d1_pct}%"></span></span><span class="sc-bar-wrap"><span class="sc-bar dest2" style="width:{d2_pct}%"></span></span></span>
{winner_html}
</a>''')

    return f'''<div class="scorecard" id="scorecard">
<h2>&#128202; Visual Scorecard</h2>
<div class="scorecard-overall">
<div class="scorecard-city dest1-city"><div class="city-name">{dest1.upper()}</div><div class="city-score">{d1_wins}</div></div>
<div class="scorecard-vs">vs</div>
<div class="scorecard-city dest2-city"><div class="city-name">{dest2.upper()}</div><div class="city-score">{d2_wins}</div></div>
</div>
<div class="scorecard-rows">
{''.join(rows)}
</div>
</div>''', d1_wins, d2_wins, ties


def build_quick_answers(sections: List[Dict], dest1: str, dest2: str) -> str:
    cards = []
    qa_map = [
        (['cost', 'budget', 'value', 'price'], 'Which is cheaper?'),
        (['food', 'dining', 'drink', 'cuisine'], 'Which has better food?'),
        (['beach', 'water', 'coast'], 'Which has better beaches?'),
        (['safety', 'security', 'crime'], 'Which is safer?'),
        (['culture', 'history', 'art', 'architecture', 'museum'], 'Which has more culture?'),
        (['nightlife', 'entertainment', 'party', 'bar'], 'Which has better nightlife?'),
        (['nature', 'scenery', 'outdoor', 'hiking', 'landscape'], 'Which has better nature?'),
        (['transport', 'getting', 'around'], 'Which is easier to get around?'),
    ]

    for keywords, question in qa_map:
        for s in sections:
            hl = s['heading_text'].lower()
            if any(kw in hl for kw in keywords):
                w = determine_winner(s['winner_text'], dest1, dest2)
                if w == 'dest1':
                    badge = f'<span class="qa-winner dest1">{dest1} wins</span>'
                elif w == 'dest2':
                    badge = f'<span class="qa-winner dest2">{dest2} wins</span>'
                else:
                    badge = '<span class="qa-winner tie">Tie</span>'

                answer = s['summary'][:100]
                cards.append(f'''<a class="qa-card" href="#{s['id']}">
<div class="qa-q">{question}</div>
<div class="qa-a">{html_mod.escape(answer)}</div>
{badge}
</a>''')
                break

        if len(cards) >= 6:
            break

    if not cards:
        return ''

    return f'''<div class="quick-answers" id="quick-answers">
<h2>&#9889; Quick Answers</h2>
<div class="qa-grid">
{''.join(cards)}
</div>
</div>'''


def build_collapsible_section(s: Dict, dest1: str, dest2: str, is_open: bool = False) -> str:
    w = determine_winner(s['winner_text'], dest1, dest2)
    if w == 'dest1':
        badge = f'<span class="dd-winner-badge dest1">{dest1} wins</span>'
    elif w == 'dest2':
        badge = f'<span class="dd-winner-badge dest2">{dest2} wins</span>'
    else:
        badge = '<span class="dd-winner-badge tie">Tie</span>'

    open_class = ' open' if is_open else ''
    summary = html_mod.escape(s['summary'])

    return f'''<section class="deep-dive{open_class}" data-winner="{w}" id="sec-{s['id']}">
<div class="dd-header">
<h2 id="{s['id']}">{s['heading_html']}</h2>
<div class="dd-header-meta">
{badge}
<span class="dd-toggle">&#9662;</span>
</div>
</div>
<p class="dd-summary">{summary}</p>
<div class="dd-body"><div class="dd-content">
{s['body']}
</div></div>
</section>'''


def build_decision_section(decision_html: str) -> str:
    if not decision_html:
        return ''
    return f'''<section class="deep-dive open" data-winner="depends" id="sec-decision">
<div class="dd-header">
<h2 id="the-decision-framework">&#128256; The Decision Framework</h2>
<div class="dd-header-meta">
<span class="dd-toggle">&#9662;</span>
</div>
</div>
<div class="dd-body"><div class="dd-content">
{decision_html}
</div></div>
</section>'''


def build_also_compared(related_slugs: List[str]) -> str:
    if not related_slugs:
        return ''
    cards = []
    for rs in related_slugs[:3]:
        # Try to get title from the page
        rp = COMPARE_DIR / rs / "index.html"
        if not rp.exists():
            continue
        try:
            rhtml = rp.read_text("utf-8")
            m = re.search(r'<h1[^>]*>(.*?)</h1>', rhtml, re.DOTALL)
            title_raw = strip_tags(m.group(1)) if m else rs.replace('-', ' ').title()
            title = re.match(r'^(.+?)\s*(?:[:—–-]|$)', title_raw).group(1).strip()
        except Exception:
            title = rs.replace('-', ' ').replace('-vs-', ' vs ').title()

        img_url = f"https://img.tabiji.ai/compare/{rs}/hero.jpg"

        cards.append(f'''<a class="also-card" href="/compare/{rs}/">
<img src="{img_url}" alt="{html_mod.escape(title)}" loading="lazy">
<div class="also-card-body">
<div class="also-card-title">{html_mod.escape(title)}</div>
<div class="also-card-vol">&#128200; Popular comparison</div>
</div>
</a>''')

    if not cards:
        return ''

    return f'''<div class="also-compared" id="also-compared">
<h2>&#128101; Travelers Also Compared</h2>
<div class="also-grid">
{''.join(cards)}
</div>
</div>'''


def build_ticker(dest1: str, dest2: str, d1_wins: int, d2_wins: int, ties: int) -> str:
    return f'''<div class="score-ticker" id="score-ticker">
    <span><span class="score-label score-dest1">{dest1} {d1_wins}</span> <span class="score-divider">&mdash;</span> <span class="score-label score-dest2">{d2_wins} {dest2}</span></span>
    <span class="score-divider">|</span>
    <span class="score-section" id="ticker-section">{ties} ties</span>
</div>'''


def build_toc(sections: List[Dict], has_qa: bool = True) -> Tuple[str, str]:
    """Build both desktop sidebar TOC and mobile TOC."""
    items = []
    if has_qa:
        items.append(('quick-answers', '&#9889; Quick Answers'))
    items.append(('the-tl-dr-verdict', '&#9889; Verdict'))
    items.append(('scorecard', '&#128202; Scorecard'))
    for s in sections:
        icon = icon_for(s['heading_text'])
        label = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\ufe0f\u200d]+\s*', '', s['heading_text'].split('&')[0].strip())
        if len(label) > 18:
            label = ' '.join(label.split()[:2])
        items.append((s['id'], f'{icon} {label}'))
    items.append(('the-decision-framework', '&#128256; Decision'))
    items.append(('frequently-asked-questions', '&#10067; FAQ'))

    sidebar_lis = '\n'.join(f'<li><a href="#{sid}">{lbl}</a></li>' for sid, lbl in items)
    sidebar = f'''<aside class="toc-sidebar">
<h2>Contents</h2>
<ul>
{sidebar_lis}
</ul>
</aside>'''

    mobile_links = '\n'.join(f'<a href="#{sid}">{lbl}</a>' for sid, lbl in items)
    mobile = f'''<div class="toc-mobile-sticky" id="toc-mobile">
<button class="toc-mobile-toggle" aria-label="Jump to section">
<span class="toc-active-label" id="toc-active-label">Contents</span>
<span class="toc-mobile-arrow">&#9662;</span>
</button>
<div class="toc-mobile-dropdown">
{mobile_links}
</div>
</div>'''

    return sidebar, mobile


def build_personalize_widget(dest1: str, dest2: str, sections: List[Dict]) -> str:
    """Build personalization widget with generic recommendations based on winners."""
    # Determine overall leanings
    d1_strengths = []
    d2_strengths = []
    for s in sections:
        w = determine_winner(s['winner_text'], dest1, dest2)
        hl = s['heading_text'].lower()
        if w == 'dest1':
            d1_strengths.append(hl)
        elif w == 'dest2':
            d2_strengths.append(hl)

    d1_good = ', '.join(d1_strengths[:3]) if d1_strengths else 'overall value'
    d2_good = ', '.join(d2_strengths[:3]) if d2_strengths else 'unique experiences'

    recs = {
        'food': f'For <strong>food lovers</strong>, compare the dining scenes below. Both destinations have unique culinary traditions worth exploring.',
        'culture': f'For <strong>culture seekers</strong>, scroll to the culture section to see which destination matches your interests.',
        'beaches': f'If <strong>beach access</strong> matters, check the beaches comparison below to see which destination delivers.',
        'nightlife': f'For <strong>nightlife</strong>, both destinations offer different vibes. See the nightlife section for a detailed breakdown.',
    }

    recs_js = json.dumps(recs, ensure_ascii=False)

    return f'''<div class="personalize-widget" id="personalize">
<h2>&#127919; Tell me about your trip</h2>
<div class="personalize-row">
<label>Traveling&hellip;</label>
<div class="pill-group" data-group="style">
<button class="personalize-pill" data-val="solo">Solo</button>
<button class="personalize-pill" data-val="couple">Couple</button>
<button class="personalize-pill" data-val="family">Family</button>
<button class="personalize-pill" data-val="friends">Friends</button>
</div>
</div>
<div class="personalize-row">
<label>Budget&hellip;</label>
<div class="pill-group" data-group="budget">
<button class="personalize-pill" data-val="backpacker">Backpacker</button>
<button class="personalize-pill" data-val="midrange">Mid-range</button>
<button class="personalize-pill" data-val="luxury">Luxury</button>
</div>
</div>
<div class="personalize-row">
<label>I care about&hellip;</label>
<div class="pill-group" data-group="priority">
<button class="personalize-pill" data-val="food">Food</button>
<button class="personalize-pill" data-val="culture">Culture</button>
<button class="personalize-pill" data-val="beaches">Beaches</button>
<button class="personalize-pill" data-val="nightlife">Nightlife</button>
</div>
</div>
<div class="personalize-result" id="personalize-result"></div>
</div>'''


def build_js(dest1: str, dest2: str, sections: List[Dict]) -> str:
    """Build the page JS with addEventListener (not inline onclick)."""
    section_names = {}
    for s in sections:
        label = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff\ufe0f\u200d]+\s*', '', s['heading_text'].split('&')[0].strip())
        section_names[s['id']] = label
    section_names['quick-answers'] = 'Quick Answers'
    section_names['the-tl-dr-verdict'] = 'Verdict'
    section_names['scorecard'] = 'Scorecard'
    section_names['the-decision-framework'] = 'Decision'
    section_names['frequently-asked-questions'] = 'FAQ'

    sn_json = json.dumps(section_names, ensure_ascii=False)

    # Build generic recommendations
    recs = {
        'food': f'For <strong>food lovers</strong>, check the food section below for a detailed comparison of both dining scenes.',
        'culture': f'For <strong>culture seekers</strong>, see the culture and history section for key highlights of each destination.',
        'beaches': f'If <strong>beach access</strong> matters, the beaches section breaks down what each destination offers.',
        'nightlife': f'For <strong>nightlife</strong>, scroll to the nightlife section to compare the scenes.',
    }
    recs_json = json.dumps(recs, ensure_ascii=False)

    return f'''<script>
/* Nav dropdown close */
document.addEventListener('click',function(e){{document.querySelectorAll('.nav-dropdown.open').forEach(function(d){{if(!d.contains(e.target))d.classList.remove('open')}});}});

/* Collapsible sections */
document.querySelectorAll('.dd-header').forEach(function(h){{
    h.addEventListener('click', function(){{ this.parentElement.classList.toggle('open'); }});
}});

/* Mobile TOC toggle */
var tocToggle = document.querySelector('.toc-mobile-toggle');
if(tocToggle) tocToggle.addEventListener('click', function(){{ this.parentElement.classList.toggle('open'); }});

/* Mobile TOC close on link click */
document.querySelectorAll('.toc-mobile-dropdown a').forEach(function(a){{
    a.addEventListener('click', function(){{ document.getElementById('toc-mobile').classList.remove('open'); }});
}});

/* Filter tags */
document.querySelectorAll('.filter-tag').forEach(function(btn){{
    btn.addEventListener('click', function(){{
        document.querySelectorAll('.filter-tag').forEach(function(t){{ t.classList.remove('active'); }});
        this.classList.add('active');
        var target = this.getAttribute('data-section');
        var el = document.getElementById(target);
        if(el){{
            var dive = el.closest('.deep-dive');
            if(dive && !dive.classList.contains('open')) dive.classList.add('open');
            el.scrollIntoView({{ behavior:'smooth', block:'start' }});
        }}
    }});
}});

/* TOC + ticker scroll tracking */
var sectionEls = document.querySelectorAll('[id]');
var tocLinks = document.querySelectorAll('.toc-sidebar a, .toc-mobile-dropdown a');
var mobileLabel = document.querySelector('.toc-active-label');
var ticker = document.getElementById('score-ticker');
var tickerSection = document.getElementById('ticker-section');
var jumpBtn = document.getElementById('jump-verdict');
var sectionNames = {sn_json};

function updateTOC(){{
    var current = '';
    sectionEls.forEach(function(s){{ if(s.getBoundingClientRect().top <= 120) current = s.id; }});
    tocLinks.forEach(function(link){{
        link.classList.remove('active');
        if(link.getAttribute('href') === '#' + current){{
            link.classList.add('active');
            if(mobileLabel && link.closest('.toc-mobile-dropdown')) mobileLabel.textContent = link.textContent;
        }}
    }});
    var hero = document.querySelector('.hero');
    if(hero && ticker){{
        if(hero.getBoundingClientRect().bottom < 0){{
            ticker.classList.add('visible');
            if(sectionNames[current]) tickerSection.textContent = sectionNames[current];
        }} else {{ ticker.classList.remove('visible'); }}
    }}
    if(jumpBtn){{
        var verdict = document.getElementById('the-tl-dr-verdict');
        var vr = verdict ? verdict.getBoundingClientRect() : {{top:9999}};
        if(window.scrollY > 400 && vr.top > window.innerHeight) jumpBtn.classList.add('visible');
        else jumpBtn.classList.remove('visible');
    }}
}}
window.addEventListener('scroll', updateTOC, {{ passive: true }});
updateTOC();

/* Personalization */
var personState = {{ style:null, budget:null, priority:null }};
var fallbacks = {recs_json};
document.querySelectorAll('.personalize-pill').forEach(function(btn){{
    btn.addEventListener('click', function(){{
        var group = this.parentElement.getAttribute('data-group');
        this.parentElement.querySelectorAll('.personalize-pill').forEach(function(p){{ p.classList.remove('selected'); }});
        this.classList.add('selected');
        personState[group] = this.getAttribute('data-val');
        if(personState.style && personState.budget && personState.priority){{
            var result = document.getElementById('personalize-result');
            var text = fallbacks[personState.priority] || 'Both destinations are excellent. Scroll down to compare specific categories.';
            result.innerHTML = text;
            result.classList.add('visible');
        }}
    }});
}});

/* Jump to verdict */
if(jumpBtn) jumpBtn.addEventListener('click', function(){{
    document.getElementById('the-tl-dr-verdict').scrollIntoView({{behavior:'smooth'}});
}});
</script>'''


# ─── CSS ─────────────────────────────────────────────────────────────

def load_css(dest1_color: str = DEST1_COLOR, dest2_color: str = DEST2_COLOR) -> str:
    css = (REPO / "scripts" / "compare-ux-styles.css").read_text("utf-8")
    # Replace madrid/barcelona specific colors with generic dest1/dest2
    css = css.replace('--madrid:', '--dest1:')
    css = css.replace('--barcelona:', '--dest2:')
    css = css.replace('.madrid', '.dest1')
    css = css.replace('.barcelona', '.dest2')
    css = css.replace('.score-madrid', '.score-dest1')
    css = css.replace('.score-barcelona', '.score-dest2')
    css = css.replace('.edge-madrid', '.edge-dest1')
    css = css.replace('.edge-barcelona', '.edge-dest2')
    css = css.replace('.cta-btn-madrid', '.cta-btn-dest1')
    css = css.replace('.cta-btn-barcelona', '.cta-btn-dest2')
    css = css.replace('.dest1-city', '.dest1-city')  # already correct
    css = css.replace('.dest2-city', '.dest2-city')
    # Set colors
    css = re.sub(r'--dest1:\s*#[0-9a-fA-F]+', f'--dest1: {dest1_color}', css)
    css = re.sub(r'--dest2:\s*#[0-9a-fA-F]+', f'--dest2: {dest2_color}', css)
    return css


# ─── Full page assembly ──────────────────────────────────────────────

def upgrade_page(slug: str, dry_run: bool = False) -> str:
    page_html = read_page(slug)
    head = extract_head(page_html)
    seo = extract_seo_meta(head)
    schema = extract_schema_blocks(head)
    dest1, dest2 = extract_dests(page_html)

    hero_content = extract_hero(page_html)
    methodology = extract_methodology(page_html)
    photo_grid = extract_photo_grid(page_html)
    verdict = extract_verdict(page_html)
    sections = extract_deep_dives(page_html, dest1, dest2)
    decision = extract_decision_frameworks(page_html)
    faq = extract_faq(page_html)
    cta = extract_cta(page_html)
    viator = extract_viator(page_html)
    images = extract_images(page_html, slug)
    related = get_related(slug)

    # Build new components
    filter_tags = build_filter_tags(sections)
    scorecard_html, d1_wins, d2_wins, ties = build_scorecard(sections, dest1, dest2)
    qa_html = build_quick_answers(sections, dest1, dest2)
    ticker_html = build_ticker(dest1, dest2, d1_wins, d2_wins, ties)
    sidebar_toc, mobile_toc = build_toc(sections, has_qa=bool(qa_html))
    personalize = build_personalize_widget(dest1, dest2, sections)
    also_html = build_also_compared(related)

    # Build collapsible sections
    collapsible = []
    for i, s in enumerate(sections):
        is_open = (i == 0)  # first section open by default
        collapsible.append(build_collapsible_section(s, dest1, dest2, is_open))

    decision_section = build_decision_section(decision)
    js = build_js(dest1, dest2, sections)
    css = load_css()

    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Assemble
    page = f'''<!DOCTYPE html>

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
<meta content="{html_mod.escape(seo['description'])}" name="description"/>
<meta content="{html_mod.escape(seo['ogTitle'])}" property="og:title"/>
<meta content="{html_mod.escape(seo['ogDescription'])}" property="og:description"/>
<meta content="article" property="og:type"/>
<meta content="{seo['canonical']}" property="og:url"/>
<meta content="{seo['ogImage']}" property="og:image"/>
<meta content="tabiji.ai" property="og:site_name"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{html_mod.escape(seo['ogTitle'])}" name="twitter:title"/>
<meta content="{html_mod.escape(seo['ogDescription'])}" name="twitter:description"/>
<meta content="{seo['ogImage']}" name="twitter:image"/>
<meta content="{seo['publishedTime']}" property="article:published_time"/>
<meta content="{now}" property="article:modified_time"/>
<meta content="index, follow, max-image-preview:large" name="robots"/>
<link href="{seo['canonical']}" rel="canonical"/>
{schema}
<style>
{css}
</style>
<!-- @include:shared-head:start -->
<link rel="stylesheet" href="/assets/shared-shell.css">
<script defer src="/assets/shared-shell.js"></script>
<!-- @include:shared-head:end -->
</head>
<body>
<!-- @include:nav:start -->
<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;" loading="lazy"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="" style="height:32px;">tabiji<span>.ai</span></a>
    <button class="hamburger" aria-label="Menu">&#9776;</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/compare/">&#x1F19A; Compare Destinations</a>
                <a href="/find/">&#x1F50D; Destination Finder</a>
                <a href="/spin/">&#x1F30E; Spin the Globe</a>
                <a href="/resources/">&#x1F4DA; Resources</a>
                <a href="/api/">&#x1F50C; API</a>
            </div>
        </div>
        <a href="/popular-picks/">Popular Picks</a>
        <a href="/itineraries/">Itineraries</a>
        <a href="/about/">About</a>
        <a href="/plan" class="cta-nav">Get a Free Itinerary</a>
    </div>
</nav>
<!-- @include:nav:end -->

{ticker_html}
{mobile_toc}

<section class="hero">
{hero_content}
</section>

<div class="priority-filter" id="priority-filter">
<h2>What matters most to you?</h2>
<div class="filter-tags">
{filter_tags}
</div>
</div>

{personalize}

<div class="content-wrapper">
{sidebar_toc}
<div class="article-content">

{methodology}
{photo_grid}
{qa_html}
{verdict}
{scorecard_html}

{''.join(collapsible)}
{decision_section}

{faq}
{cta}
{also_html}
{viator}

</div><!-- /article-content -->
</div><!-- /content-wrapper -->
<!-- @include:footer:start -->
<footer>
    <p>&copy; 2026 tabiji.ai &middot; <a href="/terms/" style="color: inherit; text-decoration: underline;">Terms of Service</a> &middot; <a href="/privacy/" style="color: inherit; text-decoration: underline;">Privacy Policy</a> &middot; <a href="/delete-data/" style="color: inherit; text-decoration: underline;">Delete My Data</a> &middot; <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Instagram</a> &middot; <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">YouTube</a> &middot; <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">Pinterest</a> &middot; <a href="https://x.com/tabijiai" target="_blank" rel="noopener" style="color: inherit; text-decoration: underline;">X</a> &middot; <a href="/media/" style="color: inherit; text-decoration: underline;">Media Studio</a> &middot; <a href="/api/" style="color: inherit; text-decoration: underline;">API</a></p>
</footer>
<!-- @include:footer:end -->

<button class="jump-verdict" id="jump-verdict">&#9889; Jump to Verdict</button>

{js}
</body>
</html>'''

    if dry_run:
        return page

    out_path = COMPARE_DIR / slug / "index.html"
    out_path.write_text(page, encoding="utf-8")
    return page


# ─── Main ────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/batch-ux-upgrade.py <slug>")
        print("       python3 scripts/batch-ux-upgrade.py --file slugs.txt")
        sys.exit(1)

    if sys.argv[1] == '--file':
        slug_file = Path(sys.argv[2])
        slugs = [s.strip() for s in slug_file.read_text().splitlines() if s.strip()]
    else:
        slugs = [sys.argv[1]]

    # Skip already-upgraded pages
    skip = {'madrid-vs-barcelona'}  # reference impl, already done

    success = 0
    errors = []
    for i, slug in enumerate(slugs):
        if slug in skip:
            print(f"[{i+1}/{len(slugs)}] SKIP {slug} (already upgraded)")
            continue
        try:
            upgrade_page(slug)
            success += 1
            print(f"[{i+1}/{len(slugs)}] OK   {slug}")
        except Exception as e:
            errors.append((slug, str(e)))
            print(f"[{i+1}/{len(slugs)}] FAIL {slug}: {e}")

    print(f"\nDone: {success} upgraded, {len(errors)} errors")
    if errors:
        print("\nFailed pages:")
        for slug, err in errors:
            print(f"  {slug}: {err}")


if __name__ == "__main__":
    main()
