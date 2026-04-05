#!/usr/bin/env python3
"""
Enrich existing compare pages:
1. Replace AI cliches with specific language
2. Scrape real Reddit quotes for each comparison
3. Rewrite meta descriptions to be unique with specific numbers
4. Add decision framework ("Choose X If..." grid)
5. Rebuild HTML from updated JSON

Usage:
  python3 scripts/enrich-compare-pages.py <slug1> <slug2> ...
  python3 scripts/enrich-compare-pages.py --list  # show candidates
"""

import json
import os
import re
import subprocess
import sys
import html as html_module
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "compare-data"
COMPARE_DIR = REPO_ROOT / "compare"

# AI cliches to replace
AI_CLICHES = {
    r'\bvibrant\b': ['lively', 'colorful', 'energetic', 'packed', 'loud', 'neon-lit', 'chaotic', 'dense'],
    r'\bbustling\b': ['crowded', 'packed', 'busy', 'hectic', 'noisy', 'fast-moving', 'chaotic'],
    r'\bunforgettable\b': ['memorable', 'worth the trip', 'hard to top', 'one you remember', 'standout'],
    r'\bhidden gem\b': ['lesser-known spot', 'local favorite', 'off the main drag', 'underrated pick', 'under-the-radar'],
    r'\brich tapestry\b': ['deep history', 'layered culture', 'long tradition', 'mix of influences'],
    r'\bunique blend\b': ['mix of', 'combination of', 'overlap of', 'cross between'],
    r'\bsomething for everyone\b': ['enough variety to keep most travelers happy', 'options across budgets and interests'],
    r'\bwhether you\'re\b': ['if you\'re', 'for those who are'],
    r'\bWhether you\'re\b': ['If you\'re', 'For those who are'],
    r'\bwhether you are\b': ['if you are', 'for those who are'],
    r'\bno matter what\b': ['regardless of', 'whatever your', 'across all'],
    r'\ba feast for the senses\b': ['sensory overload in the best way', 'hits you from every angle'],
    r'\bsteeped in history\b': ['centuries old', 'with roots going back to', 'historically layered'],
    r'\bmelting pot\b': ['cultural crossroads', 'immigrant-shaped', 'multi-ethnic'],
    r'\bpicture-perfect\b': ['photogenic', 'camera-ready', 'good-looking', 'well-preserved'],
    r'\bworld-class\b': ['top-tier', 'internationally recognized', 'among the best', 'elite-level'],
    r'\bmust-visit\b': ['worth prioritizing', 'high on the list', 'don\'t skip'],
    r'\bbreathtaking\b': ['dramatic', 'striking', 'jaw-dropping', 'impressive', 'wide-open'],
    r'\bstunning\b': ['impressive', 'striking', 'sharp', 'gorgeous', 'excellent'],
    r'\benchanting\b': ['charming', 'atmospheric', 'moody', 'appealing'],
    r'\bseamlessly blends\b': ['mixes', 'combines', 'merges', 'layers'],
    r'\boffers something\b': ['has options', 'provides', 'gives you', 'delivers'],
}

import random

def fix_cliches(text):
    """Replace AI cliches with more natural alternatives."""
    fixed = text
    replacements_made = 0
    for pattern, alternatives in AI_CLICHES.items():
        matches = list(re.finditer(pattern, fixed, re.IGNORECASE))
        for match in reversed(matches):
            replacement = random.choice(alternatives)
            # Preserve case of first letter
            if match.group()[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            fixed = fixed[:match.start()] + replacement + fixed[match.end():]
            replacements_made += 1
    return fixed, replacements_made


def search_reddit_quotes(dest1, dest2, serpapi_key):
    """Search Reddit for real quotes comparing two destinations."""
    quotes = []
    queries = [
        f"{dest1} vs {dest2} site:reddit.com",
        f"{dest1} or {dest2} which site:reddit.com r/travel",
        f"{dest2} vs {dest1} site:reddit.com",
    ]

    seen_urls = set()
    for query in queries:
        try:
            url = f"https://serpapi.com/search.json?engine=google&q={urllib.parse.quote(query)}&api_key={serpapi_key}&num=5"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read())

            for result in data.get('organic_results', []):
                link = result.get('link', '')
                snippet = result.get('snippet', '')
                title = result.get('title', '')

                if 'reddit.com' not in link:
                    continue
                if link in seen_urls:
                    continue
                seen_urls.add(link)

                # Extract subreddit from URL
                sub_match = re.search(r'reddit\.com/r/(\w+)', link)
                subreddit = f"r/{sub_match.group(1)}" if sub_match else "r/travel"

                # Clean up snippet — remove date prefixes, ellipsis artifacts
                snippet = re.sub(r'^\w{3}\s+\d+,\s+\d{4}\s*[·—-]\s*', '', snippet)
                snippet = re.sub(r'^\d+\s+votes?,?\s*\d*\s*comments?\s*[·—-]\s*', '', snippet)
                snippet = snippet.strip()

                if len(snippet) > 40 and len(snippet) < 400:
                    # Check it mentions at least one destination
                    d1_lower = dest1.lower()
                    d2_lower = dest2.lower()
                    snip_lower = snippet.lower()
                    if d1_lower in snip_lower or d2_lower in snip_lower:
                        quotes.append({
                            'text': snippet,
                            'subreddit': subreddit,
                            'url': link,
                            'title': title,
                        })

            time.sleep(0.5)
        except Exception as e:
            print(f"    Reddit search error for '{query}': {e}")
            continue

    # Deduplicate by text similarity
    unique_quotes = []
    for q in quotes:
        is_dupe = False
        for uq in unique_quotes:
            # Simple overlap check
            if q['text'][:50] == uq['text'][:50]:
                is_dupe = True
                break
        if not is_dupe:
            unique_quotes.append(q)

    return unique_quotes[:5]  # Max 5 quotes


def generate_meta_and_framework(slug, dest1, dest2, existing_data):
    """Use Gemini to generate a unique meta description and decision framework."""
    api_key = subprocess.run(
        ['security', 'find-generic-password', '-s', 'gemini-api-key', '-w'],
        capture_output=True, text=True
    ).stdout.strip()

    # Extract existing verdict for context
    verdict = ''
    verdict_html = existing_data.get('content', {}).get('verdictHtml', '')
    verdict_match = re.search(r'verdict-summary[^>]*>.*?<strong>(.*?)</strong>', verdict_html, re.DOTALL)
    if verdict_match:
        verdict = verdict_match.group(1)[:300]

    # Extract comparison categories for context
    categories = []
    for section in existing_data.get('content', {}).get('deepDiveHtml', []):
        h2_match = re.search(r'<h2[^>]*>(.+?)</h2>', section)
        winner_match = re.search(r'<strong>Winner:</strong>\s*(.+?)</li>', section)
        if h2_match:
            cat_name = re.sub(r'<[^>]+>', '', h2_match.group(1)).strip()
            winner = winner_match.group(1).strip() if winner_match else 'Tie'
            categories.append(f"{cat_name}: {winner}")

    prompt = f"""For a travel comparison page: {dest1} vs {dest2}

Context — verdict: {verdict}
Categories & winners: {'; '.join(categories[:10])}

Generate ONLY valid JSON (no markdown fences):

{{
  "metaDescription": "Unique meta description, max 155 chars. MUST include at least one specific number (daily budget, flight time, or price). Be punchy, not generic.",
  "decisionFramework": {{
    "dest1Reasons": ["7-9 specific, concrete reasons to choose {dest1}. Each should be a real, practical reason like 'You want $3 pad thai at midnight' or 'You need direct flights from most US cities'. No generic 'you love culture' items."],
    "dest2Reasons": ["7-9 specific, concrete reasons to choose {dest2}. Same standard — practical, specific, grounded."]
  }}
}}

BANNED: vibrant, bustling, unforgettable, hidden gem, world-class, stunning, breathtaking, enchanting, unique blend, something for everyone, whether you're, rich tapestry, must-visit, picture-perfect, seamlessly blends.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json"
        }
    })

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=body.encode(), headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=60)
            result = json.loads(resp.read())
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = re.sub(r'^```json\s*', '', text.strip())
            text = re.sub(r'\s*```$', '', text.strip())
            return json.loads(text)
        except Exception as e:
            if attempt < 2:
                print(f"    Retry {attempt+1}: {e}")
                time.sleep(2)
            else:
                print(f"    Failed to generate meta/framework: {e}")
                return None


def inject_reddit_quotes(deep_dive_html_list, quotes, dest1, dest2):
    """Insert real Reddit quotes into deep dive sections."""
    if not quotes:
        return deep_dive_html_list

    updated = list(deep_dive_html_list)
    quote_idx = 0

    # Distribute quotes across sections (skip decision framework which is last)
    content_sections = [i for i, s in enumerate(updated) if 'decision-grid' not in s]

    # Pick evenly-spaced sections
    if len(content_sections) < 2:
        return updated

    step = max(1, len(content_sections) // min(len(quotes), 5))
    target_indices = content_sections[1::step][:len(quotes)]  # Skip first section

    for section_idx in target_indices:
        if quote_idx >= len(quotes):
            break

        q = quotes[quote_idx]
        quote_html = f'''<div class="reddit-quote">
            "{html_module.escape(q['text'])}"
            <span class="source">— <a href="{html_module.escape(q['url'])}">{html_module.escape(q['subreddit'])} user</a></span>
</div>'''

        # Insert before the winner section
        section = updated[section_idx]
        winner_pos = section.find('<div class="section-winner">')
        if winner_pos > 0:
            section = section[:winner_pos] + quote_html + '\n' + section[winner_pos:]
        else:
            # Insert before closing </section>
            close_pos = section.rfind('</section>')
            if close_pos > 0:
                section = section[:close_pos] + quote_html + '\n' + section[close_pos:]

        updated[section_idx] = section
        quote_idx += 1

    return updated


def build_decision_framework_html(dest1, dest2, framework_data):
    """Build the decision framework HTML section."""
    dest1_reasons = framework_data.get('dest1Reasons', [])
    dest2_reasons = framework_data.get('dest2Reasons', [])

    dest1_li = "\n".join(f"<li>{html_module.escape(r)}</li>" for r in dest1_reasons)
    dest2_li = "\n".join(f"<li>{html_module.escape(r)}</li>" for r in dest2_reasons)

    return f'''<section class="deep-dive">
<h2 id="the-decision-framework">🎯 The Decision Framework</h2>
<div class="decision-grid">
<div class="decision-card dest1-card">
<h3>Choose {html_module.escape(dest1)} If…</h3>
<ul>
{dest1_li}
</ul>
</div>
<div class="decision-card dest2-card">
<h3>Choose {html_module.escape(dest2)} If…</h3>
<ul>
{dest2_li}
</ul>
</div>
</div>
</section>'''


def enrich_page(slug):
    """Full enrichment pipeline for a single compare page."""
    data_path = DATA_DIR / f"{slug}.json"
    html_path = COMPARE_DIR / slug / "index.html"

    if not data_path.exists():
        print(f"  ❌ No data file for {slug}")
        return False

    print(f"\n{'='*60}")
    print(f"  Enriching: {slug}")
    print(f"{'='*60}")

    with open(data_path) as f:
        data = json.load(f)

    dest1 = data.get('destinations', {}).get('destination1', '')
    dest2 = data.get('destinations', {}).get('destination2', '')
    if not dest1 or not dest2:
        parts = slug.split('-vs-')
        dest1 = ' '.join(w.capitalize() for w in parts[0].split('-'))
        dest2 = ' '.join(w.capitalize() for w in parts[1].split('-'))

    # ── Step 1: Fix AI cliches in deep dive HTML ──
    print("  📝 Fixing AI cliches...")
    total_replacements = 0
    deep_dives = data.get('content', {}).get('deepDiveHtml', [])
    fixed_dives = []
    for section in deep_dives:
        fixed, count = fix_cliches(section)
        fixed_dives.append(fixed)
        total_replacements += count

    # Also fix verdict, FAQ, hero, comparison table
    for key in ['verdictHtml', 'heroHtml', 'faqHtml', 'ctaHtml', 'comparisonHtml']:
        if key in data.get('content', {}):
            fixed, count = fix_cliches(data['content'][key])
            data['content'][key] = fixed
            total_replacements += count

    # Fix FAQ items text too
    for faq in data.get('content', {}).get('faqItems', []):
        fixed_q, c1 = fix_cliches(faq.get('question', ''))
        fixed_a, c2 = fix_cliches(faq.get('answer', ''))
        faq['question'] = fixed_q
        faq['answer'] = fixed_a
        total_replacements += c1 + c2

    # Fix schema FAQ too
    for faq in data.get('schema', {}).get('faq', {}).get('mainEntity', []):
        fixed_q, _ = fix_cliches(faq.get('name', ''))
        fixed_a, _ = fix_cliches(faq.get('acceptedAnswer', {}).get('text', ''))
        faq['name'] = fixed_q
        faq['acceptedAnswer']['text'] = fixed_a

    print(f"    → {total_replacements} cliche replacements")

    # ── Step 2: Search for real Reddit quotes ──
    print("  🔍 Searching Reddit for real quotes...")
    serpapi_key = subprocess.run(
        ['security', 'find-generic-password', '-s', 'serpapi-key', '-w'],
        capture_output=True, text=True
    ).stdout.strip()

    quotes = search_reddit_quotes(dest1, dest2, serpapi_key)
    print(f"    → Found {len(quotes)} quotes")
    for q in quotes:
        print(f"      [{q['subreddit']}] {q['text'][:80]}...")

    # ── Step 3: Remove existing fake reddit quotes ──
    print("  🗑️  Removing existing fake reddit quotes...")
    cleaned_dives = []
    removed_count = 0
    for section in fixed_dives:
        # Remove existing reddit-quote divs
        cleaned = re.sub(
            r'<div class="reddit-quote">.*?</div>\s*',
            '',
            section,
            flags=re.DOTALL
        )
        if cleaned != section:
            removed_count += 1
        cleaned_dives.append(cleaned)
    print(f"    → Removed {removed_count} fake quote blocks")

    # ── Step 4: Inject real Reddit quotes ──
    print("  💬 Injecting real Reddit quotes...")
    enriched_dives = inject_reddit_quotes(cleaned_dives, quotes, dest1, dest2)

    # ── Step 5: Generate meta description and decision framework ──
    print("  🤖 Generating meta description + decision framework...")
    gen_data = generate_meta_and_framework(slug, dest1, dest2, data)

    if gen_data:
        # Update meta description
        new_meta = gen_data.get('metaDescription', '')
        if new_meta:
            old_meta = data.get('seo', {}).get('metaDescription', '')
            data['seo']['metaDescription'] = new_meta[:200]
            data['schema']['article']['description'] = new_meta[:200]
            print(f"    → Meta: {new_meta[:100]}...")

        # Add decision framework
        framework = gen_data.get('decisionFramework', {})
        if framework.get('dest1Reasons') and framework.get('dest2Reasons'):
            df_html = build_decision_framework_html(dest1, dest2, framework)

            # Remove existing decision framework if present
            enriched_dives = [s for s in enriched_dives if 'decision-grid' not in s]
            enriched_dives.append(df_html)

            # Update TOC to include decision framework
            toc_items = data.get('content', {}).get('tocItems', [])
            has_df_toc = any(t.get('href') == '#the-decision-framework' for t in toc_items)
            if not has_df_toc:
                # Insert before FAQ
                faq_idx = next((i for i, t in enumerate(toc_items) if t.get('href') == '#faq'), len(toc_items))
                toc_items.insert(faq_idx, {"href": "#the-decision-framework", "label": "🎯 Decision Framework"})
                data['content']['tocItems'] = toc_items

                # Rebuild TOC HTML
                toc_links = "\n".join(f'<a href="{t["href"]}">{t["label"]}</a>' for t in toc_items)
                data['content']['tocMobileHtml'] = f'''<div class="toc-mobile" id="toc-mobile" onclick="this.classList.toggle('open')">
<span class="toc-active-label">⚡ The TL;DR Verdict</span>
<div class="toc-mobile-dropdown">
{toc_links}
</div>
</div>'''
                data['content']['tocSidebarHtml'] = f'''<aside class="toc-sidebar">
<div class="toc-title">On this page</div>
{toc_links}
</aside>'''

            print(f"    → Decision framework: {len(framework['dest1Reasons'])} + {len(framework['dest2Reasons'])} reasons")

    # ── Step 6: Save updated data JSON ──
    data['content']['deepDiveHtml'] = enriched_dives
    data['seo']['modifiedTime'] = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")

    with open(data_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f"  ✅ Saved {data_path.name}")

    # ── Step 7: Rebuild HTML ──
    print("  🔨 Rebuilding HTML...")
    result = subprocess.run(
        ['python3', 'generators/compare/build_compare.py', 'build', slug],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    if result.returncode == 0:
        print(f"  ✅ Rebuilt {slug}/index.html")
    else:
        print(f"  ⚠️ Build output: {result.stderr[:200]}")
        # Fallback: we still have the data JSON updated

    return True


def list_candidates():
    """Show batch-generated pages that need enrichment."""
    cliche_counts = []

    for html_path in sorted(COMPARE_DIR.glob("*/index.html")):
        slug = html_path.parent.name
        if slug in ('index', '') or '-vs-' not in slug:
            continue

        content = html_path.read_text()

        # Count cliches
        count = 0
        for pattern in AI_CLICHES:
            count += len(re.findall(pattern, content, re.IGNORECASE))

        # Check for decision framework
        has_df = 'decision-grid' in content

        # Check for reddit quotes
        quote_count = content.count('reddit-quote')

        if count > 5 or not has_df:
            cliche_counts.append((slug, count, has_df, quote_count))

    cliche_counts.sort(key=lambda x: (-x[1], x[2]))

    print(f"{'Slug':<45} {'Cliches':>8} {'DecFW':>6} {'Quotes':>7}")
    print("-" * 70)
    for slug, count, has_df, quotes in cliche_counts[:30]:
        df_str = "✓" if has_df else "✗"
        print(f"{slug:<45} {count:>8} {df_str:>6} {quotes:>7}")

    print(f"\nTotal pages needing work: {len(cliche_counts)}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/enrich-compare-pages.py <slug1> [slug2] ...")
        print("       python3 scripts/enrich-compare-pages.py --list")
        sys.exit(1)

    if sys.argv[1] == '--list':
        list_candidates()
    else:
        slugs = sys.argv[1:]
        success = 0
        for slug in slugs:
            if enrich_page(slug):
                success += 1
            time.sleep(1)  # Rate limiting
        print(f"\n{'='*60}")
        print(f"  Done: {success}/{len(slugs)} pages enriched")
        print(f"{'='*60}")
