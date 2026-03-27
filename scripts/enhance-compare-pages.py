#!/usr/bin/env python3
"""
Enhance compare leaf pages with:
1. Best-For Snapshot
2. Structured Scorecard
3. Tightened Verdict (Choose X if... / Choose Y if...)

Runs on all compare/*/index.html pages that have a verdict-box.
Skips hub/category pages (no verdict-box).
"""

import os
import re
import sys
from html import unescape

COMPARE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'compare')

# ─── Category Mapping ───
# Maps section heading keywords to scorecard/best-for categories
FOOD_KEYWORDS = ['food', 'dining', 'cuisine', 'bbq', 'eat', 'restaurant', 'drink']
CULTURE_KEYWORDS = ['culture', 'museum', 'temple', 'shrine', 'history', 'heritage', 'art']
NIGHTLIFE_KEYWORDS = ['nightlife', 'bar', 'club', 'entertainment', 'party']
BUDGET_KEYWORDS = ['cost', 'budget', 'price', 'money', 'cheap', 'afford']
SCENERY_KEYWORDS = ['beach', 'scenery', 'landscape', 'nature', 'hik', 'mountain', 'water', 'outdoor', 'view']
LOGISTICS_KEYWORDS = ['getting around', 'transit', 'transport', 'getting there', 'logistics']

CATEGORY_MAP = {
    'food': ('🍽️', 'Food', FOOD_KEYWORDS),
    'culture': ('🏛️', 'Culture', CULTURE_KEYWORDS),
    'nightlife': ('🌙', 'Nightlife', NIGHTLIFE_KEYWORDS),
    'budget': ('💰', 'Budget', BUDGET_KEYWORDS),
    'scenery': ('🏔️', 'Scenery', SCENERY_KEYWORDS),
    'logistics': ('🚆', 'Ease/Logistics', LOGISTICS_KEYWORDS),
}

TRAVELER_TYPES = {
    'first-timers': '🏖️',
    'couples': '👫',
    'solo': '🎒',
    'families': '👨‍👩‍👧‍👦',
}

# ─── CSS for new components ───
NEW_CSS = """
        /* BEST-FOR SNAPSHOT */
        .best-for-snapshot {
            display: flex; flex-wrap: wrap; gap: 0.6rem;
            margin-bottom: 2rem; padding: 1.25rem;
            background: rgba(245, 240, 232, 0.4);
            border: 1px solid var(--sand);
            border-radius: 14px;
        }
        .best-for-snapshot h3 {
            width: 100%; font-size: 0.9rem; font-weight: 700;
            color: var(--terracotta); text-transform: uppercase;
            letter-spacing: 0.05em; margin-bottom: 0.25rem;
        }
        .best-for-chip {
            display: inline-flex; align-items: center; gap: 0.4rem;
            background: rgba(254, 252, 249, 0.9);
            border: 1px solid var(--sand);
            border-radius: 100px; padding: 0.4rem 0.9rem;
            font-size: 0.85rem; color: var(--text);
        }
        .best-for-chip .bf-label { color: var(--text-muted); }
        .best-for-chip .bf-winner { font-weight: 600; color: var(--indigo); }
        /* SCORECARD */
        .scorecard-section {
            margin-bottom: 2.5rem; padding: 1.5rem;
            background: rgba(254, 252, 249, 0.6);
            border: 1px solid var(--sand);
            border-radius: 14px;
        }
        .scorecard-section h3 {
            font-size: 0.9rem; font-weight: 700;
            color: var(--terracotta); text-transform: uppercase;
            letter-spacing: 0.05em; margin-bottom: 1rem;
        }
        .scorecard-row {
            display: grid; grid-template-columns: 110px 1fr 1fr;
            gap: 0.5rem; align-items: center;
            padding: 0.5rem 0; border-bottom: 1px solid rgba(232, 223, 208, 0.5);
        }
        .scorecard-row:last-child { border-bottom: none; }
        .scorecard-cat { font-size: 0.85rem; font-weight: 600; color: var(--indigo); }
        .scorecard-bar-wrap {
            display: flex; align-items: center; gap: 0.5rem;
        }
        .scorecard-dest-name {
            font-size: 0.75rem; color: var(--text-muted);
            min-width: 60px; text-align: right;
        }
        .scorecard-dots {
            display: flex; gap: 3px;
        }
        .scorecard-dot {
            width: 10px; height: 10px; border-radius: 50%;
            background: var(--sand);
        }
        .scorecard-dot.filled { background: var(--terracotta); }
        .scorecard-dot.filled-alt { background: var(--indigo); }
        @media (max-width: 768px) {
            .scorecard-row { grid-template-columns: 80px 1fr 1fr; }
            .scorecard-dest-name { min-width: 40px; font-size: 0.7rem; }
            .best-for-chip { font-size: 0.8rem; padding: 0.35rem 0.7rem; }
        }
"""


def extract_dest_names(html):
    """Extract the two destination names from the page title or h1."""
    # Try title first: "Tokyo vs Kyoto: ..."
    m = re.search(r'<title>([^<]+)</title>', html)
    if m:
        title = unescape(m.group(1))
        vm = re.match(r'(.+?)\s+vs\.?\s+(.+?)(?:\s*[:|\-–—])', title)
        if vm:
            return vm.group(1).strip(), vm.group(2).strip()
    # Try h1
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m:
        h1 = unescape(re.sub(r'<[^>]+>', '', m.group(1)))
        vm = re.match(r'(.+?)\s+vs\.?\s+(.+?)(?:\s*[:|\-–—?]|$)', h1)
        if vm:
            return vm.group(1).strip(), vm.group(2).strip()
    return None, None


def classify_section(heading_text):
    """Classify a section heading into a category key."""
    text = unescape(heading_text).lower()
    # Check each category
    for cat_key, (emoji, label, keywords) in CATEGORY_MAP.items():
        for kw in keywords:
            if kw in text:
                return cat_key
    return None


def extract_section_winners(html, dest1, dest2):
    """Extract winners from section-winner blocks, mapped to categories."""
    # Find pairs of (preceding deep-dive h2, section-winner block)
    results = {}

    # Split by deep-dive sections
    sections = re.split(r'<section class="deep-dive">', html)
    for section in sections[1:]:  # skip before first
        # Get h2
        h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', section)
        if not h2_match:
            continue
        heading = h2_match.group(1)
        cat = classify_section(heading)
        if not cat:
            continue

        # Get winner from section-winner
        winner_match = re.search(r'<strong>Winner:</strong>\s*(.*?)</li>', section)
        if not winner_match:
            continue
        winner_text = winner_match.group(1).strip()

        # Determine which destination wins
        if winner_text.lower() == 'depends' or winner_text.lower() == 'tie':
            results[cat] = 'depends'
        elif dest1 and dest1.lower() in winner_text.lower():
            results[cat] = dest1
        elif dest2 and dest2.lower() in winner_text.lower():
            results[cat] = dest2
        else:
            # Try partial match
            if dest1 and any(w in winner_text.lower() for w in dest1.lower().split()):
                results[cat] = dest1
            elif dest2 and any(w in winner_text.lower() for w in dest2.lower().split()):
                results[cat] = dest2
            else:
                results[cat] = winner_text  # use as-is

    return results


def extract_traveler_winners(html, dest1, dest2):
    """Infer traveler-type winners from verdict-box and decision-cards."""
    results = {}
    verdict_text = ''
    vm = re.search(r'<div class="verdict-box">(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
    if vm:
        verdict_text = unescape(re.sub(r'<[^>]+>', ' ', vm.group(1))).lower()

    # Also grab decision-card content
    cards = re.findall(r'<div class="decision-card[^"]*">(.*?)</div>\s*</div>', html, re.DOTALL)
    card_texts = {}
    for card in cards:
        card_plain = unescape(re.sub(r'<[^>]+>', ' ', card)).lower()
        if dest1 and dest1.lower() in card_plain[:100]:
            card_texts[dest1] = card_plain
        elif dest2 and dest2.lower() in card_plain[:100]:
            card_texts[dest2] = card_plain

    # Check traveler types
    traveler_keywords = {
        'first-timers': ['first-time', 'first time', 'first visit', 'first-timer', 'beginner', 'never been'],
        'couples': ['couple', 'romantic', 'romance', 'honeymoon', 'partner'],
        'solo': ['solo', 'alone', 'backpack', 'independent'],
        'families': ['famil', 'kid', 'child', 'toddler', 'family-friendly'],
    }

    for ttype, keywords in traveler_keywords.items():
        # Check verdict text
        for kw in keywords:
            if kw in verdict_text:
                # Which destination is it associated with?
                # Check if it appears near a dest name in the verdict
                for dest in [dest1, dest2]:
                    if not dest:
                        continue
                    # Find if keyword appears in context of "Choose [dest]" or "[dest] if"
                    pattern = rf'choose\s+{re.escape(dest.lower())}[^.]*{re.escape(kw)}'
                    pattern2 = rf'{re.escape(dest.lower())}[^.]*{re.escape(kw)}'
                    if re.search(pattern, verdict_text) or re.search(pattern2, verdict_text):
                        results[ttype] = dest
                        break
                if ttype in results:
                    break

        if ttype not in results:
            # Check decision cards
            for dest, card_text in card_texts.items():
                for kw in keywords:
                    if kw in card_text:
                        results[ttype] = dest
                        break
                if ttype in results:
                    break

    return results


def score_from_winner(winner, dest1, dest2):
    """Return (score1, score2) based on winner."""
    if winner == 'depends' or winner == 'Depends':
        return 3, 3
    elif winner == dest1:
        return 4, 3
    elif winner == dest2:
        return 3, 4
    else:
        return 3, 3


def generate_best_for_html(category_winners, traveler_winners, dest1, dest2):
    """Generate the best-for snapshot HTML."""
    chips = []

    # Category-based chips
    cat_display = {
        'food': '🍽️ Best for food',
        'nightlife': '🌙 Best for nightlife',
        'budget': '💰 Best for budget',
        'culture': '🏛️ Best for culture',
    }
    for cat, label in cat_display.items():
        if cat in category_winners:
            winner = category_winners[cat]
            if winner == 'depends':
                display = 'Tie'
            else:
                display = winner
            chips.append(f'<span class="best-for-chip"><span class="bf-label">{label}:</span> <span class="bf-winner">{display}</span></span>')

    # Traveler-type chips
    for ttype, emoji in TRAVELER_TYPES.items():
        if ttype in traveler_winners:
            label_map = {
                'first-timers': f'{emoji} Best for first-timers',
                'couples': f'{emoji} Best for couples',
                'solo': f'{emoji} Best for solo travelers',
                'families': f'{emoji} Best for families',
            }
            chips.append(f'<span class="best-for-chip"><span class="bf-label">{label_map[ttype]}:</span> <span class="bf-winner">{traveler_winners[ttype]}</span></span>')

    if not chips:
        return ''

    return f'''<div class="best-for-snapshot">
<h3>Best For at a Glance</h3>
{chr(10).join(chips)}
</div>'''


def generate_scorecard_html(category_winners, dest1, dest2):
    """Generate the scorecard HTML."""
    rows = []
    for cat_key in ['budget', 'food', 'culture', 'scenery', 'nightlife', 'logistics']:
        if cat_key not in category_winners:
            continue
        emoji, label, _ = CATEGORY_MAP[cat_key]
        winner = category_winners[cat_key]
        s1, s2 = score_from_winner(winner, dest1, dest2)

        dots1 = ''.join(f'<span class="scorecard-dot filled-alt"></span>' if i < s1 else '<span class="scorecard-dot"></span>' for i in range(5))
        dots2 = ''.join(f'<span class="scorecard-dot filled"></span>' if i < s2 else '<span class="scorecard-dot"></span>' for i in range(5))

        rows.append(f'''<div class="scorecard-row">
<span class="scorecard-cat">{emoji} {label}</span>
<div class="scorecard-bar-wrap"><span class="scorecard-dest-name">{dest1}</span><div class="scorecard-dots">{dots1}</div></div>
<div class="scorecard-bar-wrap"><span class="scorecard-dest-name">{dest2}</span><div class="scorecard-dots">{dots2}</div></div>
</div>''')

    if not rows:
        return ''

    return f'''<div class="scorecard-section">
<h3>📊 Head-to-Head Scorecard</h3>
{chr(10).join(rows)}
</div>'''


def tighten_verdict(html, dest1, dest2):
    """
    Check if verdict-box already has 'Choose X if' structure.
    If not, try to add it based on decision-cards or verdict content.
    Returns modified HTML.
    """
    verdict_match = re.search(r'(<div class="verdict-box">)(.*?)(</div>\s*</div>\s*</div>)', html, re.DOTALL)
    if not verdict_match:
        return html

    verdict_content = verdict_match.group(2)

    # Check if already has "Choose [dest1]" and "Choose [dest2]" structure
    has_choose_structure = False
    if dest1 and dest2:
        has_d1 = bool(re.search(rf'Choose\s+{re.escape(dest1)}', verdict_content, re.IGNORECASE))
        has_d2 = bool(re.search(rf'Choose\s+{re.escape(dest2)}', verdict_content, re.IGNORECASE))
        has_choose_structure = has_d1 and has_d2

    if has_choose_structure:
        return html  # Already tightened

    # Extract decision-card bullet points
    d1_bullets = []
    d2_bullets = []

    # Find decision cards
    cards = re.findall(r'<div class="decision-card[^"]*">\s*<h3>(.*?)</h3>\s*<ul>(.*?)</ul>', html, re.DOTALL)
    for card_title, card_ul in cards:
        items = re.findall(r'<li>(.*?)</li>', card_ul)
        items = [unescape(re.sub(r'<[^>]+>', '', item)).strip() for item in items]
        card_title_clean = unescape(re.sub(r'<[^>]+>', '', card_title)).strip().lower()
        if dest1 and dest1.lower() in card_title_clean:
            d1_bullets = items[:3]
        elif dest2 and dest2.lower() in card_title_clean:
            d2_bullets = items[:3]

    if not d1_bullets and not d2_bullets:
        # Try extracting from verdict text itself
        return html

    # Build the recommendation block
    rec_parts = []
    if d1_bullets and dest1:
        bullets = ''.join(f'<li>{b}</li>' for b in d1_bullets)
        rec_parts.append(f'<div class="verdict-card"><h3>Choose {dest1} if…</h3><ul style="margin:0.5rem 0 0 1.1rem;display:grid;gap:0.3rem;">{bullets}</ul></div>')
    if d2_bullets and dest2:
        bullets = ''.join(f'<li>{b}</li>' for b in d2_bullets)
        rec_parts.append(f'<div class="verdict-card"><h3>Choose {dest2} if…</h3><ul style="margin:0.5rem 0 0 1.1rem;display:grid;gap:0.3rem;">{bullets}</ul></div>')

    if not rec_parts:
        return html

    # Check if verdict already has verdict-cards
    if '<div class="verdict-cards">' in verdict_content:
        # Replace existing verdict-cards with enhanced version
        new_cards = f'<div class="verdict-cards">{chr(10).join(rec_parts)}</div>'
        new_verdict = re.sub(r'<div class="verdict-cards">.*?</div>\s*</div>', new_cards, verdict_content, flags=re.DOTALL)
        html = html.replace(verdict_content, new_verdict)
    else:
        # Add verdict-cards before the closing of verdict-box
        new_cards = f'<div class="verdict-cards">{chr(10).join(rec_parts)}</div>'
        # Insert before the last closing divs
        insertion = new_cards
        new_verdict = verdict_content + insertion
        html = html.replace(verdict_match.group(0),
                            verdict_match.group(1) + new_verdict + verdict_match.group(3))

    return html


def inject_css(html, new_css):
    """Inject new CSS before the closing </style> tag."""
    # Find the main </style> closing tag (the one in <head>)
    # Insert just before it
    idx = html.find('</style>')
    if idx == -1:
        return html
    return html[:idx] + new_css + '\n' + html[idx:]


def inject_blocks(html, best_for_html, scorecard_html):
    """Inject best-for and scorecard blocks right after the verdict-box."""
    if not best_for_html and not scorecard_html:
        return html

    # Find the end of the verdict-box
    # The verdict-box ends with multiple closing </div>s
    # We need to find the right insertion point: after the verdict-box closing

    # Strategy: find verdict-box start, then count div nesting
    vb_start = html.find('<div class="verdict-box">')
    if vb_start == -1:
        return html

    # Find matching closing: track div depth
    depth = 0
    i = vb_start
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1
            i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1
            i += 6
            if depth == 0:
                break
        else:
            i += 1

    if depth != 0:
        return html

    # Insert after the verdict-box
    insertion = '\n'
    if best_for_html:
        insertion += best_for_html + '\n'
    if scorecard_html:
        insertion += scorecard_html + '\n'

    return html[:i] + insertion + html[i:]


def process_page(filepath):
    """Process a single compare page. Returns status string."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip non-leaf pages
    if 'verdict-box' not in html:
        return 'skip-no-verdict'

    # Skip if already enhanced (check for actual HTML divs, not CSS class definitions)
    if '<div class="best-for-snapshot">' in html or '<div class="scorecard-section">' in html:
        return 'skip-already-enhanced'

    # Extract destination names
    dest1, dest2 = extract_dest_names(html)
    if not dest1 or not dest2:
        return 'skip-no-dest-names'

    # Extract winners from section-winner blocks
    category_winners = extract_section_winners(html, dest1, dest2)

    # For pages without section-winner blocks, try to infer from comparison table
    if not category_winners:
        # Try comparison table "Winner" column
        table_winners = re.findall(
            r'<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>',
            html, re.DOTALL
        )
        for row in table_winners:
            cat_text = unescape(re.sub(r'<[^>]+>', '', row[0])).strip().lower()
            winner_text = unescape(re.sub(r'<[^>]+>', '', row[3])).strip()

            cat_key = None
            for key, (emoji, label, keywords) in CATEGORY_MAP.items():
                for kw in keywords:
                    if kw in cat_text:
                        cat_key = key
                        break
                if cat_key:
                    break

            if cat_key and winner_text:
                if dest1.lower() in winner_text.lower():
                    category_winners[cat_key] = dest1
                elif dest2.lower() in winner_text.lower():
                    category_winners[cat_key] = dest2
                elif 'tie' in winner_text.lower() or 'draw' in winner_text.lower() or 'depends' in winner_text.lower():
                    category_winners[cat_key] = 'depends'

    # Extract traveler-type winners
    traveler_winners = extract_traveler_winners(html, dest1, dest2)

    # Generate HTML blocks
    best_for_html = generate_best_for_html(category_winners, traveler_winners, dest1, dest2)
    scorecard_html = generate_scorecard_html(category_winners, dest1, dest2)

    # Tighten verdict
    html = tighten_verdict(html, dest1, dest2)

    # Inject CSS
    html = inject_css(html, NEW_CSS)

    # Inject blocks after verdict-box
    html = inject_blocks(html, best_for_html, scorecard_html)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    has_bestfor = bool(best_for_html)
    has_scorecard = bool(scorecard_html)
    return f'enhanced(bestfor={has_bestfor},scorecard={has_scorecard})'


def main():
    if not os.path.isdir(COMPARE_DIR):
        print(f"Error: {COMPARE_DIR} not found")
        sys.exit(1)

    stats = {
        'enhanced': 0,
        'skip-no-verdict': 0,
        'skip-already-enhanced': 0,
        'skip-no-dest-names': 0,
        'errors': 0,
    }
    skipped_details = []

    dirs = sorted(os.listdir(COMPARE_DIR))
    total = 0

    for d in dirs:
        filepath = os.path.join(COMPARE_DIR, d, 'index.html')
        if not os.path.isfile(filepath):
            continue
        total += 1

        try:
            result = process_page(filepath)
            if result.startswith('enhanced'):
                stats['enhanced'] += 1
            elif result in stats:
                stats[result] += 1
                if result != 'skip-no-verdict':
                    skipped_details.append(f'{d}: {result}')
            else:
                stats['errors'] += 1
                skipped_details.append(f'{d}: unknown result {result}')
        except Exception as e:
            stats['errors'] += 1
            skipped_details.append(f'{d}: ERROR {e}')

    print(f"\n{'='*60}")
    print(f"Compare Page Enhancement Complete")
    print(f"{'='*60}")
    print(f"Total pages scanned: {total}")
    print(f"Enhanced: {stats['enhanced']}")
    print(f"Skipped (hub pages, no verdict): {stats['skip-no-verdict']}")
    print(f"Skipped (already enhanced): {stats['skip-already-enhanced']}")
    print(f"Skipped (no dest names): {stats['skip-no-dest-names']}")
    print(f"Errors: {stats['errors']}")

    if skipped_details:
        print(f"\nSkipped/Error details:")
        for detail in skipped_details:
            print(f"  - {detail}")


if __name__ == '__main__':
    main()
