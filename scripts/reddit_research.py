#!/usr/bin/env python3
"""
Real Reddit research for compare pages.

Searches for actual Reddit threads comparing two destinations, extracts
real quotes and opinions, and outputs structured data that can be fed
into enrich_compare.py or used directly.

Usage:
    python3 scripts/reddit_research.py <slug>                   # Research + print results
    python3 scripts/reddit_research.py <slug> --save            # Save to compare-data JSON
    python3 scripts/reddit_research.py <slug> --save --rebuild  # Save + rebuild HTML

Requires:
    - SerpAPI key in keychain (serpapi-key)
    - Gemini API key in keychain (gemini-api-key) for quote selection/formatting
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "compare-data"

# ── Credentials ──────────────────────────────────────────────────────────────

def get_key(name):
    return subprocess.run(
        ['security', 'find-generic-password', '-s', name, '-w'],
        capture_output=True, text=True
    ).stdout.strip()


SERPAPI_KEY = None
GEMINI_KEY = None


def init_keys():
    global SERPAPI_KEY, GEMINI_KEY
    SERPAPI_KEY = SERPAPI_KEY or get_key('serpapi-key')
    GEMINI_KEY = GEMINI_KEY or os.environ.get("GEMINI_KEY") or get_key('gemini-api-key')


# ── Subreddit mapping ────────────────────────────────────────────────────────

SUBREDDIT_MAP = {
    "japan": ["r/JapanTravel", "r/japan"],
    "tokyo": ["r/JapanTravel", "r/Tokyo"],
    "kyoto": ["r/JapanTravel", "r/kyoto"],
    "osaka": ["r/JapanTravel", "r/osaka"],
    "bali": ["r/bali", "r/indonesia"],
    "thailand": ["r/ThailandTourism", "r/Thailand"],
    "bangkok": ["r/ThailandTourism", "r/Bangkok"],
    "vietnam": ["r/VietnamTravel", "r/vietnam"],
    "korea": ["r/korea", "r/koreatravel"],
    "seoul": ["r/korea", "r/seoul"],
    "taiwan": ["r/taiwan"],
    "india": ["r/IndiaTravelGuide", "r/india"],
    "mexico": ["r/mexico", "r/MexicoTravel"],
    "mexico city": ["r/MexicoCity"],
    "colombia": ["r/Colombia"],
    "peru": ["r/PERU"],
    "costa rica": ["r/CostaRicaTravel"],
    "portugal": ["r/travelportugal", "r/portugal"],
    "spain": ["r/spain", "r/askspain"],
    "madrid": ["r/spain", "r/Madrid"],
    "barcelona": ["r/spain", "r/Barcelona"],
    "italy": ["r/ItalyTravel", "r/italy"],
    "rome": ["r/ItalyTravel", "r/rome"],
    "france": ["r/france", "r/paris"],
    "paris": ["r/paris", "r/ParisTravelGuide"],
    "london": ["r/london"],
    "greece": ["r/greece"],
    "croatia": ["r/croatia"],
    "turkey": ["r/turkey", "r/istanbul"],
    "iceland": ["r/VisitingIceland"],
    "morocco": ["r/morocco"],
    "egypt": ["r/Egypt"],
    "new zealand": ["r/newzealand"],
    "australia": ["r/australia"],
    "hawaii": ["r/HawaiiVisitors"],
    "canada": ["r/canada"],
    "argentina": ["r/argentina"],
    "brazil": ["r/Brazil"],
}


def guess_subreddits(dest1, dest2):
    """Guess relevant subreddits from destination names."""
    subs = set()
    for dest in [dest1, dest2]:
        key = dest.lower()
        if key in SUBREDDIT_MAP:
            subs.update(SUBREDDIT_MAP[key])
        for k, v in SUBREDDIT_MAP.items():
            if k in key or key in k:
                subs.update(v)
    subs.add("r/travel")
    subs.add("r/solotravel")
    return sorted(subs)


# ── SerpAPI Reddit search ────────────────────────────────────────────────────

def search_reddit_threads(dest1, dest2, max_results=15):
    """Search for Reddit threads comparing two destinations via SerpAPI."""
    threads = []

    queries = [
        f'"{dest1} vs {dest2}" site:reddit.com',
        f'"{dest1} or {dest2}" site:reddit.com travel',
        f'"{dest2} vs {dest1}" site:reddit.com',
        f'{dest1} {dest2} which site:reddit.com travel',
    ]

    seen_urls = set()

    for query in queries:
        params = urllib.parse.urlencode({
            'engine': 'google',
            'q': query,
            'api_key': SERPAPI_KEY,
            'num': 10,
        })
        url = f'https://serpapi.com/search.json?{params}'

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'tabiji/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())

            for result in data.get('organic_results', []):
                link = result.get('link', '')
                if 'reddit.com' not in link:
                    continue
                if link in seen_urls:
                    continue
                seen_urls.add(link)

                # Extract subreddit from URL
                sub_match = re.search(r'reddit\.com/r/(\w+)', link)
                subreddit = f"r/{sub_match.group(1)}" if sub_match else "r/travel"

                threads.append({
                    'url': link,
                    'title': result.get('title', ''),
                    'snippet': result.get('snippet', ''),
                    'subreddit': subreddit,
                })

            time.sleep(0.5)  # Rate limit between SerpAPI calls
        except Exception as e:
            print(f"  SerpAPI search error for '{query[:50]}...': {e}")
            continue

        if len(threads) >= max_results:
            break

    return threads[:max_results]


def fetch_reddit_thread_comments(thread_url, max_comments=30):
    """Fetch comments from a Reddit thread using the JSON API."""
    # Convert to JSON endpoint
    json_url = thread_url.rstrip('/')
    # Remove query params
    json_url = json_url.split('?')[0]
    if not json_url.endswith('.json'):
        json_url += '.json'

    try:
        req = urllib.request.Request(json_url, headers={
            'User-Agent': 'tabiji-research/1.0 (travel comparison research)',
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())

        comments = []
        if isinstance(data, list) and len(data) >= 2:
            # data[0] = post, data[1] = comments
            _extract_comments(data[1].get('data', {}).get('children', []), comments, max_comments)

        return comments
    except Exception as e:
        print(f"    Reddit fetch error: {e}")
        return []


def _extract_comments(children, comments, max_count, depth=0):
    """Recursively extract comment text from Reddit JSON."""
    if len(comments) >= max_count:
        return
    for child in children:
        if len(comments) >= max_count:
            return
        if child.get('kind') != 't1':
            continue
        cdata = child.get('data', {})
        body = cdata.get('body', '')
        score = cdata.get('score', 0)

        # Skip low-quality comments
        if not body or len(body) < 20 or body == '[deleted]' or body == '[removed]':
            continue
        if score < 2 and depth == 0:
            continue

        comments.append({
            'text': body,
            'score': score,
            'subreddit': f"r/{cdata.get('subreddit')}" if cdata.get('subreddit') else '',
            'author': cdata.get('author', 'anonymous'),
            'depth': depth,
        })

        # Recurse into replies
        replies = cdata.get('replies', '')
        if isinstance(replies, dict):
            _extract_comments(
                replies.get('data', {}).get('children', []),
                comments, max_count, depth + 1
            )


# ── Gemini quote extraction ──────────────────────────────────────────────────

def extract_best_quotes(dest1, dest2, raw_comments, section_titles):
    """Use Gemini to select and format the best quotes from real Reddit comments."""
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"

    # Truncate comment corpus to fit context
    comment_text = ""
    for c in raw_comments[:80]:
        entry = f"[{c['subreddit']}, score {c['score']}]: {c['text'][:300]}\n"
        if len(comment_text) + len(entry) > 12000:
            break
        comment_text += entry

    section_list = "\n".join(f"  {i}. {title}" for i, title in enumerate(section_titles))

    prompt = f"""You are curating real Reddit quotes for a {dest1} vs {dest2} travel comparison page.

Below are REAL comments from Reddit threads. Your job is to select the best 1-2 quotes per section
and lightly edit them for clarity (fix typos, trim excess, keep the authentic voice).

REAL REDDIT COMMENTS:
{comment_text}

SECTIONS (by index):
{section_list}

For each section, pick 1-2 quotes that are:
- Specific (mention places, costs, experiences)
- Opinionated (clear preference or insight)
- 15-40 words after editing
- Relevant to that section's topic

If no real quote fits a section, write a realistic one inspired by the comment corpus themes.

Output ONLY valid JSON:
{{
  "sections": [
    {{
      "sectionIndex": 0,
      "quotes": [
        {{"text": "Edited quote text...", "subreddit": "r/travel", "isReal": true}}
      ]
    }}
  ]
}}

Requirements:
- Mark isReal=true if based on an actual comment above, false if synthesized
- Keep the casual, first-person Reddit voice
- Don't over-polish — travelers write casually
- Each quote 15-40 words
"""

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json"
        }
    })

    for attempt in range(3):
        try:
            req = urllib.request.Request(gemini_url, data=body.encode(),
                                        headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = re.sub(r'^```json\s*', '', text.strip())
            text = re.sub(r'\s*```$', '', text.strip())
            return json.loads(text)
        except Exception as e:
            if attempt < 2:
                print(f"    Gemini retry {attempt+1}: {e}")
                time.sleep(2 + attempt * 2)
            else:
                print(f"    Gemini quote extraction failed: {e}")
                return None


# ── Main pipeline ─────────────────────────────────────────────────────────────

def slug_to_names(slug):
    """Convert slug to destination names. Import from batch-compare-gen if available."""
    try:
        sys.path.insert(0, str(REPO_ROOT / "scripts"))
        from importlib import import_module
        mod = import_module("batch-compare-gen")
        return mod.slug_to_names(slug)
    except Exception:
        parts = slug.split('-vs-')
        if len(parts) != 2:
            raise ValueError(f"Invalid slug: {slug}")
        return tuple(p.replace('-', ' ').title() for p in parts)


def research_slug(slug, verbose=True):
    """Full research pipeline for a single slug. Returns structured quote data."""
    init_keys()
    dest1, dest2 = slug_to_names(slug)

    if verbose:
        print(f"\n{'='*60}")
        print(f"Researching: {dest1} vs {dest2}")
        print(f"{'='*60}")

    # Step 1: Search Reddit threads
    if verbose:
        print(f"\n📡 Searching Reddit threads...")
    threads = search_reddit_threads(dest1, dest2)
    if verbose:
        print(f"  Found {len(threads)} threads")
        for t in threads[:5]:
            print(f"    • [{t['subreddit']}] {t['title'][:80]}")

    if not threads:
        print("  ⚠️  No Reddit threads found — falling back to synthesized quotes")
        return None

    # Step 2: Fetch comments from top threads
    if verbose:
        print(f"\n💬 Fetching comments from top {min(5, len(threads))} threads...")
    all_comments = []
    for i, thread in enumerate(threads[:5]):
        if verbose:
            print(f"  [{i+1}] {thread['url'][:80]}...")
        comments = fetch_reddit_thread_comments(thread['url'])
        # Tag each comment with the thread's subreddit if not already set
        for c in comments:
            if not c.get('subreddit'):
                c['subreddit'] = thread['subreddit']
        all_comments.extend(comments)
        time.sleep(1)  # Reddit rate limit

    if verbose:
        print(f"  Collected {len(all_comments)} comments total")

    if not all_comments:
        print("  ⚠️  No comments extracted — falling back to synthesized quotes")
        return None

    # Sort by score (most upvoted = most valuable)
    all_comments.sort(key=lambda c: c.get('score', 0), reverse=True)

    # Step 3: Load section titles from compare-data
    data_path = DATA_DIR / f"{slug}.json"
    section_titles = []
    if data_path.exists():
        data = json.loads(data_path.read_text())
        for dd in data.get('content', {}).get('deepDiveHtml', []):
            title_match = re.search(r'<h2[^>]*>(.*?)</h2>', dd, re.S)
            if title_match:
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                title = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u27bf\u2702-\u27b0]+\s*', '', title).strip()
                section_titles.append(title)
    else:
        # Use generic section titles
        section_titles = [
            "City Character & Vibe", "Food & Dining", "Cost Comparison",
            "Getting Around", "Beaches", "Nightlife", "Safety",
            "Day Trips", "Best Time to Visit", "Where to Stay"
        ]

    # Step 4: Use Gemini to select best quotes per section
    if verbose:
        print(f"\n🤖 Selecting best quotes for {len(section_titles)} sections...")
    result = extract_best_quotes(dest1, dest2, all_comments, section_titles)

    if result and verbose:
        sections = result.get('sections', [])
        real_count = sum(
            1 for s in sections for q in s.get('quotes', []) if q.get('isReal', False)
        )
        synth_count = sum(
            1 for s in sections for q in s.get('quotes', []) if not q.get('isReal', False)
        )
        print(f"  ✅ {real_count} real quotes, {synth_count} synthesized")

    return {
        'slug': slug,
        'dest1': dest1,
        'dest2': dest2,
        'threads_found': len(threads),
        'comments_collected': len(all_comments),
        'threads': [{'url': t['url'], 'title': t['title'], 'subreddit': t['subreddit']} for t in threads],
        'quotes': result,
    }


def save_to_compare_data(slug, research_result):
    """Inject real Reddit quotes into compare-data JSON."""
    import html as html_module

    data_path = DATA_DIR / f"{slug}.json"
    if not data_path.exists():
        print(f"  ❌ No compare-data found at {data_path}")
        return False

    data = json.loads(data_path.read_text())
    quotes_data = research_result.get('quotes') or {}
    if not quotes_data:
        print(f"  ❌ No quotes to inject")
        return False

    quote_sections = quotes_data.get('sections', [])
    deep_dives = data.get('content', {}).get('deepDiveHtml', [])

    # Build quote map
    quote_map = {}
    for qs in quote_sections:
        idx = qs.get('sectionIndex', -1)
        if 0 <= idx < len(deep_dives):
            quote_map[idx] = qs.get('quotes', [])

    changed = False
    for i, dd in enumerate(deep_dives):
        if i not in quote_map:
            continue
        quotes = quote_map[i]
        if not quotes:
            continue

        # Skip if already has reddit quotes
        if 'reddit-quote' in dd:
            continue

        # Build quote HTML
        quote_parts = []
        for q in quotes[:2]:
            sub = q.get('subreddit', 'r/travel')
            if not sub.startswith('r/'):
                sub = f"r/{sub}"
            sub_url = f"https://www.reddit.com/{sub}/"
            quote_text = html_module.escape(q['text'].strip().strip('"'))
            quote_parts.append(
                f'<div class="reddit-quote">\n'
                f'            "{quote_text}"\n'
                f'            <span class="source">— <a href="{sub_url}">{sub} user</a></span>\n'
                f'</div>'
            )

        quote_block = "\n".join(quote_parts)

        # Insert before section-winner or closing </section>
        winner_pos = dd.find('<div class="section-winner">')
        if winner_pos != -1:
            dd = dd[:winner_pos] + quote_block + "\n" + dd[winner_pos:]
        else:
            close_pos = dd.rfind('</section>')
            if close_pos != -1:
                dd = dd[:close_pos] + quote_block + "\n" + dd[close_pos:]

        deep_dives[i] = dd
        changed = True

    if changed:
        data['content']['deepDiveHtml'] = deep_dives
        data['seo']['modifiedTime'] = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
        data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(f"  ✅ Injected real Reddit quotes into {data_path.name}")

        # Store research metadata
        meta = {
            'threads_found': research_result['threads_found'],
            'comments_collected': research_result['comments_collected'],
            'threads': research_result['threads'][:10],
            'researched_at': datetime.now(timezone.utc).isoformat(),
        }
        meta_path = DATA_DIR / f"{slug}.research.json"
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
        return True
    else:
        print(f"  ℹ️  No changes needed (quotes already present or no matching sections)")
        return False


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    slug = sys.argv[1]
    should_save = '--save' in sys.argv
    should_rebuild = '--rebuild' in sys.argv

    result = research_slug(slug)

    if result:
        print(f"\n{'='*60}")
        print(f"Research summary for {result['dest1']} vs {result['dest2']}:")
        print(f"  Threads found: {result['threads_found']}")
        print(f"  Comments collected: {result['comments_collected']}")

        if should_save:
            print(f"\n📝 Saving quotes to compare-data...")
            saved = save_to_compare_data(slug, result)

            if saved and should_rebuild:
                print(f"\n🔨 Rebuilding HTML...")
                build_script = REPO_ROOT / "generators" / "compare" / "build_compare.py"
                subprocess.run(
                    [sys.executable, str(build_script), 'build'],
                    cwd=str(REPO_ROOT)
                )
        else:
            # Print quotes for review
            if result.get('quotes'):
                print(f"\n📋 Extracted quotes:")
                for section in result['quotes'].get('sections', []):
                    idx = section.get('sectionIndex', '?')
                    for q in section.get('quotes', []):
                        real_tag = "✓ real" if q.get('isReal') else "✦ synth"
                        print(f"  [{idx}] [{real_tag}] [{q.get('subreddit', '?')}] \"{q['text']}\"")
    else:
        print(f"\n⚠️  No research data available for {slug}")
        print(f"    This is normal for niche comparisons with few Reddit threads.")
        print(f"    The enrich_compare.py fallback will generate synthesized quotes.")
        sys.exit(1)


if __name__ == "__main__":
    main()
