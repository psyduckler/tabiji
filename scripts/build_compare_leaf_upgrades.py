#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parent.parent
COMPARE_DIR = REPO / 'compare'
INVENTORY = json.loads((COMPARE_DIR / 'inventory.json').read_text())['cards']

STYLE_BLOCK = """
.bestfor-snapshot { margin: 2rem 0; padding: 1.5rem; background: rgba(245, 240, 232, 0.45); border: 1px solid var(--sand); border-radius: 16px; }
.bestfor-snapshot h2 { font-size: 1.35rem; color: var(--indigo); margin-bottom: 0.55rem; }
.bestfor-snapshot > p { color: var(--text-muted); margin-bottom: 1rem; }
.bestfor-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.9rem; }
.bestfor-card { background: var(--white); border: 1px solid var(--sand); border-radius: 14px; padding: 1rem; }
.bestfor-card h3 { font-size: 0.95rem; color: var(--earth); margin-bottom: 0.35rem; }
.bestfor-card strong { display: block; font-size: 1.05rem; color: var(--indigo); margin-bottom: 0.35rem; }
.bestfor-card p { font-size: 0.9rem; color: var(--text-muted); margin: 0; }
.scorecard-section { margin: 2rem 0; }
.scorecard-section h2 { font-size: 1.35rem; color: var(--indigo); margin-bottom: 0.55rem; }
.scorecard-section > p { color: var(--text-muted); margin-bottom: 1rem; }
.scorecard-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
.scorecard { background: var(--white); border: 1px solid var(--sand); border-radius: 14px; padding: 1rem; }
.scorecard h3 { font-size: 1.05rem; color: var(--indigo); margin-bottom: 0.8rem; }
.score-row { display: grid; grid-template-columns: 120px 1fr auto; gap: 0.7rem; align-items: center; margin-bottom: 0.55rem; }
.score-row span { font-size: 0.9rem; color: var(--text-muted); }
.score-dots { display: inline-flex; gap: 0.24rem; }
.score-dots i { width: 12px; height: 12px; display: inline-block; border-radius: 999px; background: var(--sand); }
.score-dots i.on { background: var(--terracotta); }
.score-val { font-size: 0.86rem; color: var(--earth); font-weight: 700; }
.verdict-card.split-card { border: 1px dashed var(--sage); }
.verdict-card.split-card h3 { color: var(--sage); }
@media (max-width: 900px) { .bestfor-grid, .scorecard-grid { grid-template-columns: 1fr; } }
"""


def find_row(rows, keywords):
    for row in rows:
        cat = row['category'].lower()
        if any(k in cat for k in keywords):
            return row
    return None


def norm(text: str) -> str:
    return re.sub(r'\s+', ' ', (text or '').strip())


def parse_rows(soup):
    table = soup.select_one('.comparison-table')
    if not table:
        return [], None, None
    trs = table.select('tr')
    if not trs:
        return [], None, None
    headers = [norm(x.get_text(' ', strip=True)) for x in trs[0].select('th,td')]
    d1 = re.sub(r'^[^A-Za-z0-9]+', '', headers[1]) if len(headers) > 1 else 'Destination 1'
    d2 = re.sub(r'^[^A-Za-z0-9]+', '', headers[2]) if len(headers) > 2 else 'Destination 2'
    rows = []
    for tr in trs[1:]:
        cells = [norm(x.get_text(' ', strip=True)) for x in tr.select('th,td')]
        if len(cells) >= 4:
            rows.append({'category': cells[0], 'd1': cells[1], 'd2': cells[2], 'winner': cells[3]})
    return rows, d1, d2


def winner_for_row(row, d1, d2):
    if not row:
        return 'Tie'
    w = row['winner'].lower()
    if d1.lower() in w:
        return d1
    if d2.lower() in w:
        return d2
    if 'tie' in w or w in {'—', '-', 'n/a'}:
        return 'Tie'
    if row['winner'] == d1:
        return d1
    if row['winner'] == d2:
        return d2
    return 'Tie'


def explanation_for_row(row, winner, d1, d2):
    if not row:
        return 'Not a clean call from the comparison table, so treat this as situational.'
    if winner == d1:
        return row['d1']
    if winner == d2:
        return row['d2']
    return f"Both have a credible case here: {row['d1']} vs {row['d2']}."


def detect_first_timers(rows, d1, d2, overall=None):
    best = find_row(rows, ['best for'])
    if best:
        if 'first' in best['d1'].lower() and 'first' not in best['d2'].lower():
            return d1, best['d1']
        if 'first' in best['d2'].lower() and 'first' not in best['d1'].lower():
            return d2, best['d2']
    transit = find_row(rows, ['public transit', 'transport', 'logistics'])
    winner = winner_for_row(transit, d1, d2)
    if winner != 'Tie':
        return winner, explanation_for_row(transit, winner, d1, d2)
    return overall or 'Tie', 'A softer call based on overall ease and beginner-friendliness.'


def detect_people_type(rows, d1, d2, mode, overall):
    best = find_row(rows, ['best for'])
    text1 = (best['d1'].lower() if best else '')
    text2 = (best['d2'].lower() if best else '')
    keywords = {
        'couples': ['couple', 'romantic', 'honeymoon', 'photographers', 'slow travelers'],
        'solo': ['solo', 'first-timers', 'foodies', 'pop culture'],
        'families': ['famil', 'kids', 'easy', 'day trips']
    }[mode]
    if any(k in text1 for k in keywords) and not any(k in text2 for k in keywords):
        return d1, best['d1']
    if any(k in text2 for k in keywords) and not any(k in text1 for k in keywords):
        return d2, best['d2']

    if mode == 'couples':
        row = find_row(rows, ['nature', 'scenery', 'romance', 'culture', 'temples'])
    elif mode == 'solo':
        row = find_row(rows, ['public transit', 'nightlife', 'food'])
    else:
        row = find_row(rows, ['day trips', 'public transit', 'budget'])
    winner = winner_for_row(row, d1, d2)
    if winner != 'Tie':
        return winner, explanation_for_row(row, winner, d1, d2)
    return overall or 'Tie', 'This one depends more on your exact trip style than on a universal winner.'


def score_pair(rows, d1, d2):
    mapping = {
        'budget': ['budget', 'cost'],
        'food': ['food'],
        'culture': ['culture', 'history', 'temples', 'shrines', 'museums', 'art'],
        'scenery': ['nature', 'beaches', 'beach', 'scenery', 'views'],
        'nightlife': ['nightlife'],
        'ease': ['public transit', 'logistics', 'day trips', 'transport']
    }
    scores = {d1: {k: 3.0 for k in mapping}, d2: {k: 3.0 for k in mapping}}
    for key, needles in mapping.items():
        matched = [r for r in rows if any(n in r['category'].lower() for n in needles)]
        if not matched:
            continue
        for row in matched:
            w = winner_for_row(row, d1, d2)
            if w == d1:
                scores[d1][key] += 1.0
                scores[d2][key] -= 0.5
            elif w == d2:
                scores[d2][key] += 1.0
                scores[d1][key] -= 0.5
            else:
                scores[d1][key] += 0.2
                scores[d2][key] += 0.2
    for dest in [d1, d2]:
        for key in mapping:
            scores[dest][key] = max(1, min(5, int(round(scores[dest][key]))))
    return scores


def build_bestfor_section(soup, rows, d1, d2):
    budget = find_row(rows, ['budget', 'cost'])
    food = find_row(rows, ['food'])
    nightlife = find_row(rows, ['nightlife'])
    overall = winner_for_row(find_row(rows, ['best for']), d1, d2)
    first_timers = detect_first_timers(rows, d1, d2, overall)
    couples = detect_people_type(rows, d1, d2, 'couples', overall)
    solo = detect_people_type(rows, d1, d2, 'solo', overall)
    families = detect_people_type(rows, d1, d2, 'families', overall)

    cards = [
        ('Best for food', winner_for_row(food, d1, d2), explanation_for_row(food, winner_for_row(food, d1, d2), d1, d2)),
        ('Best for nightlife', winner_for_row(nightlife, d1, d2), explanation_for_row(nightlife, winner_for_row(nightlife, d1, d2), d1, d2)),
        ('Best for budget', winner_for_row(budget, d1, d2), explanation_for_row(budget, winner_for_row(budget, d1, d2), d1, d2)),
        ('Best for first-timers', first_timers[0], first_timers[1]),
        ('Best for couples', couples[0], couples[1]),
        ('Best for solo travelers', solo[0], solo[1]),
        ('Best for families', families[0], families[1]),
    ]

    section = soup.new_tag('section', attrs={'class': 'bestfor-snapshot'})
    h2 = soup.new_tag('h2')
    h2.string = 'Best-for snapshot'
    section.append(h2)
    p = soup.new_tag('p')
    p.string = 'Fast answers first: who each destination tends to serve best, pulled from the page’s own comparison table and verdict.'
    section.append(p)
    grid = soup.new_tag('div', attrs={'class': 'bestfor-grid'})
    for title, winner, expl in cards:
        card = soup.new_tag('div', attrs={'class': 'bestfor-card'})
        h3 = soup.new_tag('h3')
        h3.string = title
        strong = soup.new_tag('strong')
        strong.string = winner
        desc = soup.new_tag('p')
        desc.string = expl
        card.extend([h3, strong, desc])
        grid.append(card)
    section.append(grid)
    return section


def build_scorecard_section(soup, rows, d1, d2):
    scores = score_pair(rows, d1, d2)
    section = soup.new_tag('section', attrs={'class': 'scorecard-section'})
    h2 = soup.new_tag('h2')
    h2.string = 'Quick scorecards'
    section.append(h2)
    p = soup.new_tag('p')
    p.string = 'Lightweight scoring for scanability — a decision aid, not fake precision.'
    section.append(p)
    grid = soup.new_tag('div', attrs={'class': 'scorecard-grid'})
    labels = [('budget', 'Budget'), ('food', 'Food'), ('culture', 'Culture'), ('scenery', 'Scenery'), ('nightlife', 'Nightlife'), ('ease', 'Ease / logistics')]
    for dest in [d1, d2]:
        card = soup.new_tag('div', attrs={'class': 'scorecard'})
        h3 = soup.new_tag('h3')
        h3.string = dest
        card.append(h3)
        for key, label in labels:
            row = soup.new_tag('div', attrs={'class': 'score-row'})
            span = soup.new_tag('span')
            span.string = label
            dots = soup.new_tag('div', attrs={'class': 'score-dots'})
            score = scores[dest][key]
            for i in range(5):
                dot = soup.new_tag('i')
                if i < score:
                    dot['class'] = 'on'
                dots.append(dot)
            val = soup.new_tag('div', attrs={'class': 'score-val'})
            val.string = f'{score}/5'
            row.extend([span, dots, val])
            card.append(row)
        grid.append(card)
    section.append(grid)
    return section


def reason_from_decision_cards(soup, d1, d2):
    cards = soup.select('.decision-card')
    d1_reason = None
    d2_reason = None
    for card in cards:
        heading = norm(card.get_text(' ', strip=True)).lower()
        bullets = [norm(li.get_text(' ', strip=True)) for li in card.select('li')][:3]
        if not bullets:
            continue
        joined = ', '.join(bullets)
        if d1.lower() in heading or 'choose ' + d1.lower() in heading:
            d1_reason = joined
        elif d2.lower() in heading or 'choose ' + d2.lower() in heading:
            d2_reason = joined
    return d1_reason, d2_reason


def reason_from_row_wins(rows, d1, d2):
    d1_wins = [r['category'] for r in rows if winner_for_row(r, d1, d2) == d1][:3]
    d2_wins = [r['category'] for r in rows if winner_for_row(r, d1, d2) == d2][:3]
    d1_reason = ', '.join(d1_wins).lower() if d1_wins else None
    d2_reason = ', '.join(d2_wins).lower() if d2_wins else None
    if d1_reason:
        d1_reason = f'{d1_reason}.'
    if d2_reason:
        d2_reason = f'{d2_reason}.'
    return d1_reason, d2_reason


def tighten_verdict(soup, rows, d1, d2):
    verdict = soup.select_one('.verdict-box')
    if not verdict:
        return
    # remove old injected split items if rerun
    for el in verdict.select('.split-card'):
        el.decompose()
    for el in verdict.select('.split-takeaway'):
        el.decompose()

    best = find_row(rows, ['best for'])
    card_d1_reason, card_d2_reason = reason_from_decision_cards(soup, d1, d2)
    row_d1_reason, row_d2_reason = reason_from_row_wins(rows, d1, d2)
    d1_reason = best['d1'] if best else (card_d1_reason or row_d1_reason or f'{d1} brings the stronger version of its biggest wins on this page.')
    d2_reason = best['d2'] if best else (card_d2_reason or row_d2_reason or f'{d2} brings the stronger version of its biggest wins on this page.')
    split_reason = f'Split your trip if you want {d1} for its strongest wins but still want {d2} for the categories where it clearly does better.'

    summary = verdict.select_one('.verdict-summary')
    if summary:
        summary.string = ''
        strong = soup.new_tag('strong')
        strong.string = f'Choose {d1} if you want {d1_reason.lower()} Choose {d2} if you want {d2_reason.lower()} Split your trip if you want both experiences without forcing one city to do the other’s job.'
        summary.append(strong)

    takeaways = verdict.select_one('.verdict-takeaways')
    if takeaways:
        items = takeaways.select('li')
        if len(items) >= 2:
            items[0].clear()
            s = soup.new_tag('strong')
            s.string = f'Choose {d1}: '
            items[0].append(s)
            items[0].append(d1_reason)
            items[1].clear()
            s = soup.new_tag('strong')
            s.string = f'Choose {d2}: '
            items[1].append(s)
            items[1].append(d2_reason)
        li = soup.new_tag('li', attrs={'class': 'split-takeaway'})
        s = soup.new_tag('strong')
        s.string = 'Split your trip: '
        li.append(s)
        li.append(split_reason)
        takeaways.append(li)

    cards = verdict.select_one('.verdict-cards')
    if cards:
        split = soup.new_tag('div', attrs={'class': 'verdict-card split-card'})
        h3 = soup.new_tag('h3')
        h3.string = 'Split your trip'
        p = soup.new_tag('p')
        p.string = split_reason
        split.extend([h3, p])
        cards.append(split)


def inject_sections(soup, rows, d1, d2):
    article = soup.select_one('.article-content') or soup.select_one('.content-wrapper') or soup.body
    verdict = soup.select_one('.verdict-box')
    table = soup.select_one('.comparison-table')
    if not verdict or not table:
        return False

    for old in soup.select('.bestfor-snapshot, .scorecard-section'):
        old.decompose()

    bestfor = build_bestfor_section(soup, rows, d1, d2)
    scorecards = build_scorecard_section(soup, rows, d1, d2)
    verdict.insert_after(bestfor)
    bestfor.insert_after(scorecards)
    return True


def ensure_styles(soup):
    style_tag = None
    for tag in soup.find_all('style'):
        if ':root' in tag.get_text():
            style_tag = tag
            break
    if not style_tag:
        return
    text = style_tag.get_text()
    if '.bestfor-snapshot' not in text:
        style_tag.string = text + '\n' + STYLE_BLOCK


def process_page(path: Path):
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    ensure_styles(soup)
    rows, d1, d2 = parse_rows(soup)
    if not rows or not d1 or not d2:
        return False
    inject_sections(soup, rows, d1, d2)
    tighten_verdict(soup, rows, d1, d2)
    path.write_text(str(soup))
    return True


def main():
    slugs = [item['slug'] for item in INVENTORY]
    changed = 0
    for slug in slugs:
        page = COMPARE_DIR / slug / 'index.html'
        if page.exists() and process_page(page):
            changed += 1
    print(f'Updated {changed} compare leaf pages with smarter snapshots, scorecards, and tighter verdicts.')


if __name__ == '__main__':
    main()
