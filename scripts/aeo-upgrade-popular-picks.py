#!/usr/bin/env python3
"""
AEO Upgrade for Popular-Picks Pages
====================================
Two changes per page:
1. Answer-first rewrites: Intro paragraph + each pick's "Best experience" / "what-to-order" text
   gets rewritten so the first sentence is a self-contained, citable fact.
2. Agent Brief JSON-LD: A TouristTrip schema with additionalProperty fields summarizing
   the page's key data (best budget, best luxury, best overall, price range, etc.)

Uses Gemini 2.0 Flash for rewrites (cheap + fast).
Processes pages in batches with rate limiting.

Usage:
  python3 aeo-upgrade-popular-picks.py                    # Process all pages
  python3 aeo-upgrade-popular-picks.py --dry-run           # Preview without writing
  python3 aeo-upgrade-popular-picks.py --pages 5           # Process first N pages
  python3 aeo-upgrade-popular-picks.py --slug amsterdam-brunch  # Process one page
  python3 aeo-upgrade-popular-picks.py --skip-existing     # Skip pages already upgraded
"""

import os
import re
import json
import sys
import time
import argparse
import subprocess
from pathlib import Path

# --- Config ---
REPO_ROOT = Path(__file__).resolve().parent.parent
POPULAR_PICKS_DIR = REPO_ROOT / "popular-picks"
GEMINI_MODEL = "gemini-2.0-flash"

def get_api_key():
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "google-api-key", "-w"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

API_KEY = None  # Lazy-loaded

def call_gemini(prompt, max_tokens=4096):
    """Call Gemini API for text generation."""
    global API_KEY
    if API_KEY is None:
        API_KEY = get_api_key()

    import urllib.request
    import urllib.error

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.3}
    })

    req = urllib.request.Request(url, data=payload.encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        print(f"  ⚠️ Gemini API error: {e.code} {e.read().decode()[:200]}")
        return None
    except Exception as e:
        print(f"  ⚠️ Gemini error: {e}")
        return None


def clean_text(value):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', value or '')).strip()


def extract_price_numbers(price_str):
    if not price_str:
        return []
    nums = []
    for match in re.findall(r'(?:[$€£¥₩฿RM]\s?|USD\s?|EUR\s?|GBP\s?)(\d+(?:,\d+)?(?:\.\d+)?)', price_str):
        nums.append(float(match.replace(',', '')))
    return nums


def pick_numeric_price(pick):
    nums = extract_price_numbers(pick.get('price', ''))
    return min(nums) if nums else float('inf')


def extract_picks(html):
    """Extract pick data from HTML using regex (no BS4 dependency)."""
    picks = []
    section_pattern = re.compile(r'<section class="([^"]*-section)"[^>]*id="([^"]+)"[^>]*>(.*?)</section>', re.DOTALL)

    for idx, match in enumerate(section_pattern.finditer(html)):
        section_class, section_id, section = match.groups()
        pick = {'section_class': section_class, 'section_id': section_id, 'rank': idx + 1}

        h2_match = re.search(r'<h2>.*?</span>\s*(.*?)</h2>', section, re.DOTALL)
        if h2_match:
            pick['name'] = clean_text(h2_match.group(1))

        tag_match = re.search(r'class="(?:cuisine-tag|lodge-tag|pick-tag|experience-tag)[^"]*">(.*?)</span>', section, re.DOTALL)
        if tag_match:
            pick['category'] = clean_text(tag_match.group(1))

        rating_match = re.search(r'class="google-rating">.*?★.*?(\d+\.?\d*)\s*·\s*([\d,]+)\s*reviews', section, re.DOTALL)
        if rating_match:
            pick['rating'] = rating_match.group(1)
            pick['reviews'] = rating_match.group(2).replace(',', '')

        price_match = re.search(r'(?:💰|💴)\s*(.*?)</span>', section)
        if price_match:
            pick['price'] = clean_text(price_match.group(1))

        loc_match = re.search(r'📍\s*(.*?)</span>', section)
        if loc_match:
            pick['location'] = clean_text(loc_match.group(1))

        hours_match = re.search(r'class="shop-hours".*?<summary>\s*([^<]+)</summary>(.*?)</div>\s*</details>', section, re.DOTALL)
        if hours_match:
            pick['hours_summary'] = clean_text(hours_match.group(1))
            pick['hours_text'] = clean_text(hours_match.group(2))

        exp_match = re.search(r'class="what-to-order">(.*?)</div>', section, re.DOTALL)
        if exp_match:
            pick['experience_html'] = exp_match.group(1).strip()
            pick['experience_text'] = clean_text(pick['experience_html'])

        verdict_match = re.search(r'class="tabiji-verdict">(.*?)</div>', section, re.DOTALL)
        if verdict_match:
            pick['verdict'] = clean_text(verdict_match.group(1))

        if pick.get('name'):
            picks.append(pick)

    return picks


def extract_page_meta(html):
    """Extract page-level metadata."""
    meta = {}

    title_match = re.search(r'<title>(.*?)</title>', html)
    if title_match:
        meta['title'] = title_match.group(1)

    desc_match = re.search(r'<meta name="description" content="(.*?)"', html)
    if desc_match:
        meta['description'] = desc_match.group(1)

    # Hero badge (country/city)
    badge_match = re.search(r'class="hero-badge">(.*?)</div>', html)
    if badge_match:
        meta['location_badge'] = re.sub(r'<[^>]+>', '', badge_match.group(1)).strip()

    # H1
    h1_match = re.search(r'<h1>(.*?)</h1>', html, re.DOTALL)
    if h1_match:
        meta['h1'] = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

    # Intro text
    intro_match = re.search(r'class="intro-section">(.*?)</div>\s*(?:<!--|\s*<section)', html, re.DOTALL)
    if intro_match:
        # Get all <p> tags in intro
        intro_ps = re.findall(r'<p[^>]*>(.*?)</p>', intro_match.group(1), re.DOTALL)
        meta['intro_paragraphs'] = [re.sub(r'<[^>]+>', '', p).strip() for p in intro_ps if '<details' not in p and 'methodology' not in p]

    # Subtitle
    sub_match = re.search(r'class="subtitle">(.*?)</p>', html, re.DOTALL)
    if sub_match:
        meta['subtitle'] = re.sub(r'<[^>]+>', '', sub_match.group(1)).strip()

    # Canonical URL
    canon_match = re.search(r'rel="canonical" href="(.*?)"', html)
    if canon_match:
        meta['url'] = canon_match.group(1)

    # Count (from hero meta)
    count_match = re.search(r'<strong>(\d+)</strong>\s*(?:spots|experiences|restaurants|cafés|shops|bars|markets|tours|lodges|camps|beaches|trails|dishes|places)', html)
    if count_match:
        meta['count'] = count_match.group(1)

    # Reddit posts analyzed
    reddit_match = re.search(r'<strong>(\d+\+?)</strong>\s*Reddit', html)
    if reddit_match:
        meta['reddit_posts'] = reddit_match.group(1)

    return meta


def score_pick(pick, keywords=(), anti_keywords=()):
    text = ' '.join([
        pick.get('category', ''),
        pick.get('verdict', ''),
        pick.get('experience_text', ''),
        pick.get('hours_summary', ''),
        pick.get('hours_text', ''),
        pick.get('location', '')
    ]).lower()
    score = 0
    for word in keywords:
        if word in text:
            score += 1
    for word in anti_keywords:
        if word in text:
            score -= 1
    score += max(0, 4 - min(pick.get('rank', 99), 4)) * 0.2
    return score


def format_quick_pick(pick):
    bits = []
    if pick.get('price'):
        bits.append(pick['price'])
    if pick.get('location'):
        bits.append(pick['location'])
    return f"<strong>{pick['name']}</strong>" + (f" <span>— {' · '.join(bits)}</span>" if bits else '')


def build_quick_answer_cards(meta, picks):
    if not picks:
        return []

    cards = []
    used = set()

    def add_card(label, reason, pick):
        if not pick or pick.get('name') in used:
            return
        cards.append({'label': label, 'reason': reason, 'pick': pick})
        used.add(pick['name'])

    def best_unused(score_fn, minimum=0):
        ranked = sorted(picks, key=score_fn, reverse=True)
        for pick in ranked:
            if pick.get('name') in used:
                continue
            if score_fn(pick) > minimum:
                return pick
        return None

    add_card('Best overall', 'Start here if you just want the safest high-confidence pick.', picks[0])

    cheapest = None
    for pick in sorted(picks, key=pick_numeric_price):
        if pick.get('name') not in used and pick_numeric_price(pick) != float('inf'):
            cheapest = pick
            break
    add_card('Best budget', 'Best value if price matters more than hype.', cheapest)

    late_score = lambda p: score_pick(p, keywords=('24 hours', 'until 3am', 'until 2am', 'late-night', 'late night', 'post-club', 'midnight', 'dawn', 'night owl', 'night market', '4am', '5am', 'open 24 hours', 'after dark', 'evening', 'open late'))
    add_card('Best late-night', 'Most useful when your timing is the real constraint.', best_unused(late_score))

    first_timer_score = lambda p: score_pick(p, keywords=('first-timer', 'first timer', 'accessible', 'safe bet', 'stress-free', 'intro', 'introduction', 'tourist-friendly', 'beginner', 'can\'t go wrong', 'easy', 'welcoming', 'family-friendly', 'well-known', 'classic', 'iconic', 'famous'))
    add_card('Best for first-timers', 'Good fit when you want the easiest, most approachable starting point.', best_unused(first_timer_score))

    local_score = lambda p: score_pick(p, keywords=('local', 'locals', 'resident', 'residents', 'under the tourist radar', 'under the radar', 'hidden gem', 'insider', 'off the tourist trail', 'local\'s local', 'where locals go', 'neighborhood', 'artisan', 'craft', 'independent', 'family-run', 'hole in the wall'), anti_keywords=('touristy', 'world famous', 'instagram', 'chain', 'franchise'))
    add_card('Best local favorite', 'The pick with the strongest locals-actually-go-here signal.', best_unused(local_score))

    # Cap price contribution at 500 so extreme outliers ($3500+) don't dominate the score
    splurge_score = lambda p: score_pick(p, keywords=('luxury', 'splurge', 'high-end', 'exclusive', 'special occasion', 'private wing', 'premium', 'heritage luxury', 'boutique', 'designer', 'world-class', 'award-winning', 'michelin')) + (min(pick_numeric_price(p), 500) / 500 if pick_numeric_price(p) != float('inf') else 0)
    add_card('Best splurge', 'Worth the premium if you care more about the experience ceiling than value.', best_unused(splurge_score))

    return cards[:4]


def render_quick_answer_block(meta, picks):
    cards = build_quick_answer_cards(meta, picks)
    if not cards:
        return ''

    card_html = []
    for card in cards:
        card_html.append(
            f'''<div class="quick-answer-card">\n                <div class="quick-answer-label">{card['label']}</div>\n                <div class="quick-answer-pick">{format_quick_pick(card['pick'])}</div>\n                <p>{card['reason']}</p>\n            </div>'''
        )

    joiner = '\n        '
    return f'''<section class="quick-answer-block">\n    <div class="quick-answer-header">⚡ Quick answer</div>\n    <p class="quick-answer-kicker">If you're deciding fast, use these picks instead of reading the whole list top-to-bottom.</p>\n    <div class="quick-answer-grid">\n        {joiner.join(card_html)}\n    </div>\n</section>'''


def build_agent_brief_jsonld(meta, picks):
    """Build the TouristTrip JSON-LD agent brief from extracted data."""
    if not picks:
        return None

    # Determine price range
    prices_usd = []
    for p in picks:
        price_str = p.get('price', '')
        # Extract USD amounts
        usd_matches = re.findall(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', price_str)
        for m in usd_matches:
            prices_usd.append(float(m.replace(',', '')))

    price_range = ""
    if prices_usd:
        low = min(prices_usd)
        high = max(prices_usd)
        price_range = f"${int(low)}–${int(high)}"

    # Determine best by category
    rated_picks = [p for p in picks if p.get('rating')]
    budget_picks = [p for p in picks if p.get('category') and 'budget' in p['category'].lower()]
    luxury_picks = [p for p in picks if p.get('category') and 'luxury' in p['category'].lower()]

    def format_pick(p):
        parts = [p['name']]
        if p.get('price'):
            parts.append(p['price'])
        if p.get('rating') and p.get('reviews'):
            parts.append(f"{p['rating']}★ ({p['reviews']} reviews)")
        return " — ".join(parts)

    # Best overall = highest rated with most reviews
    best_overall = None
    if rated_picks:
        best_overall = max(rated_picks, key=lambda p: (float(p.get('rating', 0)), int(p.get('reviews', 0))))

    properties = []
    properties.append({"@type": "PropertyValue", "name": "totalOptions", "value": str(len(picks))})

    if price_range:
        properties.append({"@type": "PropertyValue", "name": "priceRangeUSD", "value": price_range})

    if budget_picks:
        best_budget = budget_picks[0]  # First listed budget pick (highest ranked)
        properties.append({"@type": "PropertyValue", "name": "bestBudgetOption", "value": format_pick(best_budget)})

    if luxury_picks:
        best_luxury = max(luxury_picks, key=lambda p: float(p.get('rating', 0))) if len(luxury_picks) > 1 else luxury_picks[0]
        properties.append({"@type": "PropertyValue", "name": "bestLuxuryOption", "value": format_pick(best_luxury)})

    if best_overall:
        properties.append({"@type": "PropertyValue", "name": "bestOverall", "value": format_pick(best_overall)})

    # Top pick = #1 in the list
    if picks:
        properties.append({"@type": "PropertyValue", "name": "topPick", "value": format_pick(picks[0])})

    if meta.get('reddit_posts'):
        properties.append({"@type": "PropertyValue", "name": "sourcesAnalyzed", "value": f"{meta['reddit_posts']} Reddit posts"})

    properties.append({"@type": "PropertyValue", "name": "lastVerified", "value": "2026-03"})

    # Build description
    desc_parts = []
    if meta.get('count'):
        desc_parts.append(f"{meta['count']} best options")
    if meta.get('location_badge'):
        desc_parts.append(f"in {meta['location_badge']}")
    if price_range:
        desc_parts.append(f"ranging from {price_range}")
    if meta.get('reddit_posts'):
        desc_parts.append(f"curated from {meta['reddit_posts']} Reddit reviews")
    desc_parts.append("verified March 2026")

    jsonld = {
        "@context": "https://schema.org",
        "@type": "TouristTrip",
        "name": meta.get('h1', meta.get('title', '')),
        "description": ", ".join(desc_parts) + ".",
        "url": meta.get('url', ''),
        "additionalProperty": properties
    }

    return jsonld


def rewrite_with_gemini(meta, picks):
    """Use Gemini to rewrite intro + pick descriptions to be answer-first."""
    if not picks:
        return None

    # Build the prompt
    picks_summary = []
    for i, p in enumerate(picks):
        picks_summary.append(f"""
Pick #{i+1}: {p.get('name', 'Unknown')}
Category: {p.get('category', 'N/A')}
Price: {p.get('price', 'N/A')}
Rating: {p.get('rating', 'N/A')}★ ({p.get('reviews', '?')} reviews)
Location: {p.get('location', 'N/A')}
Current "Best experience" text: {p.get('experience_text', 'N/A')}
""")

    intro_text = "\n".join(meta.get('intro_paragraphs', []))

    prompt = f"""You are rewriting travel content for Answer Engine Optimization (AEO). The goal: AI assistants (ChatGPT, Gemini, Perplexity) should be able to extract and cite specific facts from the first sentence of each section.

RULES:
1. Each pick's rewritten text MUST start with a self-contained, citable first sentence containing: name, key differentiator, price, and location (if relevant).
2. The rest of the text should flow naturally after the fact-dense opener.
3. Keep the same information — just restructure so facts lead.
4. Keep the same tone (informative, opinionated, traveler-focused).
5. Do NOT add information that isn't in the original.
6. The intro paragraph rewrite should lead with a summary sentence covering: price range across all options, top recommendation, and key qualifier (season, location, etc).

PAGE: {meta.get('h1', 'Unknown')}
LOCATION: {meta.get('location_badge', 'Unknown')}
SUBTITLE: {meta.get('subtitle', '')}

CURRENT INTRO (first 1-2 paragraphs, not counting methodology):
{intro_text}

PICKS:
{''.join(picks_summary)}

Return ONLY valid JSON with this structure (no markdown, no explanation):
{{
  "intro_rewrite": "The rewritten intro paragraph (just the first paragraph — the factual summary opener). Keep it to 2-3 sentences max.",
  "picks": [
    {{
      "index": 0,
      "rewrite": "The rewritten Best experience / what-to-order text. Start with the citable fact sentence, then the rest."
    }},
    ...
  ]
}}"""

    result = call_gemini(prompt, max_tokens=4096)
    if not result:
        return None

    # Parse JSON from response
    try:
        # Strip markdown code fences if present
        result = result.strip()
        if result.startswith("```"):
            result = re.sub(r'^```(?:json)?\n?', '', result)
            result = re.sub(r'\n?```$', '', result)
        return json.loads(result)
    except json.JSONDecodeError as e:
        print(f"  ⚠️ Failed to parse Gemini response: {e}")
        print(f"  Response preview: {result[:200]}")
        return None


def apply_changes(html, meta, picks, rewrites, jsonld):
    """Apply the answer-first rewrites, decision block, and JSON-LD to the HTML."""
    modified = html

    quick_answer_css = '''
        .quick-answer-block { background: linear-gradient(135deg, #FEFCF9, #F5F0E8); border: 1px solid #E8DFD0; border-radius: 16px; padding: 22px 24px; margin: 0 0 28px; }
        .quick-answer-header { font-size: 1rem; font-weight: 800; color: #2D3A5C; margin-bottom: 0.35rem; }
        .quick-answer-kicker { margin: 0 0 1rem; color: var(--text-muted); font-size: 0.96rem; }
        .quick-answer-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
        .quick-answer-card { background: rgba(255,255,255,0.72); border: 1px solid #E8DFD0; border-radius: 14px; padding: 14px 15px; }
        .quick-answer-label { font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 800; color: #C4704B; margin-bottom: 0.45rem; }
        .quick-answer-pick { color: #2D3A5C; line-height: 1.45; margin-bottom: 0.45rem; }
        .quick-answer-pick span { color: var(--text-muted); }
        .quick-answer-card p { margin: 0; color: var(--text-muted); font-size: 0.92rem; line-height: 1.5; }
    '''

    if '.quick-answer-block' not in modified:
        modified = re.sub(r'(\n\s*\.intro-section \{)', '\n' + quick_answer_css + '\n\\1', modified, count=1)

    modified = re.sub(r'\s*<section class="quick-answer-block">.*?</section>\s*', '\n', modified, flags=re.DOTALL)

    quick_answer_html = render_quick_answer_block(meta, picks)
    if quick_answer_html:
        intro_open = re.search(r'<div class="intro-section">', modified)
        if intro_open:
            modified = modified[:intro_open.start()] + quick_answer_html + '\n\n' + modified[intro_open.start():]

    if rewrites and rewrites.get('intro_rewrite'):
        intro_match = re.search(r'(class="intro-section">\s*(?:<h2>.*?</h2>\s*)?)\s*(<p[^>]*>)', modified, re.DOTALL)
        if intro_match:
            existing_bold = re.search(r'<div class="intro-section">\s*(?:<h2>.*?</h2>\s*)?<p><strong>.*?</strong></p>', modified, re.DOTALL)
            if not existing_bold:
                new_intro_p = f'<p><strong>{rewrites["intro_rewrite"]}</strong></p>\n            '
                insert_pos = intro_match.start(2)
                modified = modified[:insert_pos] + new_intro_p + modified[insert_pos:]

    if rewrites and rewrites.get('picks'):
        wo_pattern = re.compile(r'(<div class="what-to-order">\s*<strong>)(.*?)(</strong>)(.*?)(</div>)', re.DOTALL)
        wo_matches = list(wo_pattern.finditer(modified))
        for pick_rewrite in reversed(rewrites.get('picks', [])):
            idx = pick_rewrite.get('index', -1)
            if 0 <= idx < len(wo_matches):
                match = wo_matches[idx]
                replacement = f'{match.group(1)}{match.group(2)}{match.group(3)} {pick_rewrite["rewrite"]}{match.group(5)}'
                modified = modified[:match.start()] + replacement + modified[match.end():]

    if jsonld and '"TouristTrip"' not in modified:
        jsonld_str = json.dumps(jsonld, indent=8, ensure_ascii=False)
        style_match = re.search(r'\n\s*<style>', modified)
        if style_match:
            injection = f'''    <script type="application/ld+json">
    {jsonld_str}
    </script>
'''
            modified = modified[:style_match.start()] + '\n' + injection + modified[style_match.start():]

    return modified


def is_already_upgraded(html):
    """Check if page already has the AEO upgrade."""
    return '"TouristTrip"' in html


def process_page(slug, dry_run=False):
    """Process a single popular-picks page."""
    page_dir = POPULAR_PICKS_DIR / slug
    html_file = page_dir / "index.html"

    if not html_file.exists():
        print(f"  ⚠️ No index.html found")
        return False

    html = html_file.read_text(encoding='utf-8')

    # Extract data
    meta = extract_page_meta(html)
    picks = extract_picks(html)

    if not picks:
        print(f"  ⚠️ No picks found, skipping")
        return False

    print(f"  📊 Found {len(picks)} picks, {len([p for p in picks if p.get('rating')])} with ratings")

    # Build JSON-LD (programmatic, no LLM needed)
    jsonld = build_agent_brief_jsonld(meta, picks)

    # Rewrite with Gemini
    print(f"  🤖 Calling Gemini for answer-first rewrites...")
    rewrites = rewrite_with_gemini(meta, picks)

    if not rewrites:
        print(f"  ⚠️ Gemini rewrite failed, applying JSON-LD only")

    # Apply changes
    modified = apply_changes(html, meta, picks, rewrites, jsonld)

    if modified == html:
        print(f"  ℹ️ No changes needed")
        return False

    if dry_run:
        # Show diff stats
        original_lines = html.count('\n')
        modified_lines = modified.count('\n')
        print(f"  🔍 DRY RUN: Would add {modified_lines - original_lines} lines")
        if jsonld:
            print(f"  📋 JSON-LD: {len(jsonld.get('additionalProperty', []))} properties")
        if rewrites:
            print(f"  ✏️ Rewrites: intro + {len(rewrites.get('picks', []))} picks")
        return True

    # Write changes
    html_file.write_text(modified, encoding='utf-8')
    print(f"  ✅ Updated")
    return True


def main():
    parser = argparse.ArgumentParser(description='AEO upgrade for popular-picks pages')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    parser.add_argument('--pages', type=int, default=0, help='Process first N pages (0=all)')
    parser.add_argument('--slug', type=str, help='Process a single page by slug')
    parser.add_argument('--skip-existing', action='store_true', help='Skip pages already upgraded')
    parser.add_argument('--offset', type=int, default=0, help='Start from page N (for batching)')
    args = parser.parse_args()

    if args.slug:
        slugs = [args.slug]
    else:
        slugs = sorted([d.name for d in POPULAR_PICKS_DIR.iterdir() if d.is_dir() and (d / "index.html").exists()])

    if args.offset:
        slugs = slugs[args.offset:]
    if args.pages:
        slugs = slugs[:args.pages]

    print(f"🚀 AEO Upgrade: {len(slugs)} pages to process")
    if args.dry_run:
        print("🔍 DRY RUN mode — no files will be modified\n")

    success = 0
    skipped = 0
    failed = 0

    for i, slug in enumerate(slugs):
        print(f"\n[{i+1}/{len(slugs)}] {slug}")

        if args.skip_existing:
            html = (POPULAR_PICKS_DIR / slug / "index.html").read_text(encoding='utf-8')
            if is_already_upgraded(html):
                print(f"  ⏭️ Already upgraded, skipping")
                skipped += 1
                continue

        try:
            if process_page(slug, dry_run=args.dry_run):
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1

        # Rate limiting: 0.5s between pages
        if i < len(slugs) - 1:
            time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"✅ Success: {success}")
    print(f"⏭️ Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"Total: {len(slugs)}")


if __name__ == '__main__':
    main()
