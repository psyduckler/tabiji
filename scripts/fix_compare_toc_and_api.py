#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parent.parent
COMPARE_DIR = REPO / 'compare'
API_COMPARE_DIR = REPO / 'api' / 'v1' / 'compare'
INVENTORY_PATH = COMPARE_DIR / 'inventory.json'
BASE_URL = 'https://tabiji.ai'

INVENTORY = json.loads(INVENTORY_PATH.read_text())
CARD_BY_SLUG = {card['slug']: card for card in INVENTORY['cards']}

TOC_SCRIPT = """<script>
const sections = document.querySelectorAll('[id]');
const tocLinks = document.querySelectorAll('.toc-sidebar a, .toc-mobile-dropdown a');
const mobileLabel = document.querySelector('.toc-active-label');
function updateTOC() {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top;
        if (sectionTop <= 120) current = section.id;
    });
    tocLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) {
            link.classList.add('active');
            if (mobileLabel && link.closest('.toc-mobile-dropdown')) {
                mobileLabel.textContent = link.textContent;
            }
        }
    });
}
window.addEventListener('scroll', updateTOC, { passive: true });
updateTOC();
document.querySelectorAll('.toc-mobile-dropdown a').forEach(a => {
    a.addEventListener('click', () => {
        document.getElementById('toc-mobile').classList.remove('open');
    });
});
</script>"""


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', text or '').strip()


def slugify(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('⚡', '').replace('📊', '').replace('🍜', '').replace('🏛️', '').replace('💰', '').replace('🚇', '').replace('🏖️', '').replace('🎉', '').replace('🏕️', '').replace('🌸', '').replace('🏨', '').replace('🔀', '').replace('❓', '').replace('🎟️', '')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text or 'section'


def parse_quote(block):
    text = clean(block.get_text(' ', strip=True))
    source = ''
    source_url = ''
    source_node = block.select_one('.source')
    if source_node:
        source = clean(source_node.get_text(' ', strip=True)).lstrip('—- ')
        link = source_node.find('a')
        if link and link.get('href'):
            source_url = link['href']
        source_node.extract()
        text = clean(block.get_text(' ', strip=True))
    return {'text': text, 'source': source, 'sourceUrl': source_url}


def parse_winner_summary(section, dest1, dest2):
    box = section.select_one('.section-winner') or section.find(class_=re.compile('section-winner'))
    if not box:
        return None
    winner = 'Depends'
    why_parts = []
    for li in box.select('li'):
        txt = clean(li.get_text(' ', strip=True))
        if txt.lower().startswith('winner:'):
            winner = clean(txt.split(':', 1)[1])
        else:
            why_parts.append(txt)
    if not why_parts:
        why_parts = [clean(box.get_text(' ', strip=True))]
    return {
        'winner': winner,
        'why': ' '.join(why_parts),
        'who_this_matters_for': f'Matters most if this category is likely to drive your choice between {dest1} and {dest2}.'
    }


def ensure_toc(slug: str) -> bool:
    path = COMPARE_DIR / slug / 'index.html'
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    html = str(soup)
    if 'class="toc-sidebar"' in html or 'id="toc-mobile"' in html:
        return False
    content = soup.select_one('.content-wrapper')
    article = soup.select_one('.content-wrapper .article-content')
    nav = soup.find('nav')
    hero = soup.find(class_='hero')
    if not content or not article or not nav or not hero:
        return False

    toc_items = []
    for h2 in article.select('h2'):
        label = clean(h2.get_text(' ', strip=True))
        if not label or label.lower() in {'how we built this comparison'}:
            continue
        if not h2.get('id'):
            h2['id'] = slugify(label)
        toc_items.append((h2['id'], label))
    if not toc_items:
        return False

    toc_mobile = soup.new_tag('div', attrs={'class': 'toc-mobile-sticky', 'id': 'toc-mobile'})
    toggle = soup.new_tag('button', attrs={'class': 'toc-mobile-toggle', 'onclick': "this.parentElement.classList.toggle('open')"})
    label_span = soup.new_tag('span', attrs={'class': 'toc-active-label'})
    label_span.string = toc_items[0][1]
    chev = soup.new_tag('span', attrs={'class': 'toc-chevron'})
    chev.string = '▼'
    toggle.extend([label_span, chev])
    dropdown = soup.new_tag('div', attrs={'class': 'toc-mobile-dropdown'})
    ul = soup.new_tag('ul')
    for target, label in toc_items:
        li = soup.new_tag('li')
        a = soup.new_tag('a', href=f'#{target}')
        a.string = label
        li.append(a)
        ul.append(li)
    dropdown.append(ul)
    toc_mobile.extend([toggle, dropdown])
    hero.insert_before(toc_mobile)

    aside = soup.new_tag('aside', attrs={'class': 'toc-sidebar'})
    h2 = soup.new_tag('h2')
    h2.string = 'On this page'
    aside.append(h2)
    ul2 = soup.new_tag('ul')
    for target, label in toc_items:
        li = soup.new_tag('li')
        a = soup.new_tag('a', href=f'#{target}')
        a.string = label
        li.append(a)
        ul2.append(li)
    aside.append(ul2)
    content.insert(0, aside)

    if TOC_SCRIPT not in str(soup):
        body = soup.body or soup
        body.append(BeautifulSoup(TOC_SCRIPT, 'html.parser'))

    path.write_text(str(soup))
    return True


def parse_api(slug: str) -> dict:
    html_path = COMPARE_DIR / slug / 'index.html'
    soup = BeautifulSoup(html_path.read_text(), 'html.parser')
    card = CARD_BY_SLUG.get(slug, {})

    title = clean((soup.title.get_text(' ', strip=True) if soup.title else '').split('|')[0])
    description = soup.find('meta', attrs={'name': 'description'})
    description = description['content'].strip() if description and description.get('content') else card.get('description', '')
    canonical = soup.find('link', rel='canonical')
    url = canonical['href'] if canonical and canonical.get('href') else f'{BASE_URL}/compare/{slug}/'
    hero_img = ''
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    if og_image and og_image.get('content'):
        hero_img = og_image['content']
    elif card.get('image1'):
        hero_img = card['image1']

    h1 = clean(soup.find('h1').get_text(' ', strip=True)) if soup.find('h1') else title
    if card.get('destination1') and card.get('destination2'):
        destination1 = card.get('destination1', '')
        destination2 = card.get('destination2', '')
    elif ' vs ' in h1.lower():
        parts = re.split(r'\s+vs\.?\s+', h1, flags=re.I)
        destination1 = clean(parts[0])
        destination2 = clean(re.split(r'[:\-–—?(]', parts[1])[0])
    else:
        destination1 = card.get('destination1', '')
        destination2 = card.get('destination2', '')

    verdict_box = soup.select_one('.verdict-box')
    verdict_summary = ''
    takeaways = []
    cards = []
    if verdict_box:
        summary = verdict_box.select_one('.verdict-summary')
        if summary:
            verdict_summary = clean(summary.get_text(' ', strip=True))
        for li in verdict_box.select('.verdict-takeaways li, .verdict-list li'):
            txt = clean(li.get_text(' ', strip=True))
            if txt:
                takeaways.append(txt)
        for card_node in verdict_box.select('.verdict-card'):
            h3 = card_node.find(['h3', 'strong'])
            p = card_node.find('p')
            cards.append({'title': clean(h3.get_text(' ', strip=True)) if h3 else '', 'text': clean(p.get_text(' ', strip=True)) if p else clean(card_node.get_text(' ', strip=True))})

    categories = []
    for section in soup.select('.deep-dive'):
        h2 = section.find('h2')
        if not h2:
            continue
        title_text = clean(h2.get_text(' ', strip=True))
        summary = ''
        for p in section.find_all('p', recursive=False):
            txt = clean(p.get_text(' ', strip=True))
            if txt:
                summary = txt
                break
        highlights = []
        for p in section.find_all('p'):
            txt = clean(p.get_text(' ', strip=True))
            if txt and txt != summary and txt not in highlights:
                highlights.append(txt)
            if len(highlights) >= 3:
                break
        reddit_quotes = [parse_quote(q) for q in section.select('.reddit-quote')][:3]
        winner_summary = parse_winner_summary(section, destination1, destination2)
        cat = {
            'title': title_text,
            'summary': summary,
            'highlights': highlights,
        }
        if reddit_quotes:
            cat['redditQuotes'] = reddit_quotes
        if winner_summary:
            cat['winnerSummary'] = winner_summary
        categories.append(cat)

    faqs = []
    faq_section = soup.select_one('.faq-section')
    if faq_section:
        for item in faq_section.select('.faq-item'):
            q = item.find(['h3', 'h4'])
            a = item.find('p')
            if q and a:
                faqs.append({'question': clean(q.get_text(' ', strip=True)), 'answer': clean(a.get_text(' ', strip=True))})

    return {
        'slug': slug,
        'title': title,
        'description': description,
        'destination1': destination1 or card.get('destination1', ''),
        'destination2': destination2 or card.get('destination2', ''),
        'heroImage': hero_img,
        'url': url,
        'categoryCount': len(categories),
        'categories': categories,
        'verdict': {
            'summary': verdict_summary,
            'takeaways': takeaways,
            'cards': cards,
        },
        'faqs': faqs,
    }


def main():
    toc_fixed = []
    api_written = []
    leaves = sorted([p.name for p in COMPARE_DIR.iterdir() if p.is_dir() and '-vs-' in p.name and (p / 'index.html').exists()])
    for slug in leaves:
        if ensure_toc(slug):
            toc_fixed.append(slug)
        api_path = API_COMPARE_DIR / f'{slug}.json'
        if not api_path.exists():
            api_path.write_text(json.dumps(parse_api(slug), indent=2, ensure_ascii=False) + '\n')
            api_written.append(slug)
    print(json.dumps({'toc_fixed': toc_fixed, 'api_written_count': len(api_written), 'api_written': api_written}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
