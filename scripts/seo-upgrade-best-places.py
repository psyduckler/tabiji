#!/usr/bin/env python3
"""
SEO/AEO upgrade for all best-places-to-visit-in-* pages.
Fixes:
1. Add BreadcrumbList schema
2. Add ItemList schema (extract destinations from H2/H3 headings)
3. Add FAQPage schema (generate from content if FAQ section exists)
4. Add speakable to Article schema
5. Ensure datePublished/dateModified
"""
import os
import re
import json
import sys
from pathlib import Path

TABIJI_DIR = Path(os.path.expanduser("~/tabiji"))
TODAY = "2026-03-08"

# Month names for human-readable titles
MONTHS = {
    "january": "January", "february": "February", "march": "March",
    "april": "April", "may": "May", "june": "June",
    "july": "July", "august": "August", "september": "September",
    "october": "October", "november": "November", "december": "December"
}

stats = {"breadcrumb_added": 0, "itemlist_added": 0, "faq_added": 0, "speakable_added": 0, "total_processed": 0, "errors": []}

def extract_month(slug):
    """Extract month name from slug like best-places-to-visit-in-april."""
    m = re.search(r'in-(\w+)$', slug)
    return m.group(1) if m else ""

def extract_title(html):
    m = re.search(r'<title>([^<]+)</title>', html)
    return m.group(1).split(" — ")[0].split(" | ")[0].strip() if m else ""

def extract_destinations(html):
    """Extract destination names from dest-card labels or H2 headings."""
    # First try: dest-label spans (best-places pages use this pattern)
    labels = re.findall(r'<span class="dest-label">([^<]+)</span>', html)
    if labels:
        return labels[:15]
    
    # Second try: dest-card ids + dest-label
    cards = re.findall(r'class="dest-card" id="([^"]+)"', html)
    if cards:
        return [c.replace("-", " ").title() for c in cards][:15]
    
    # Third try: H2 headings
    headings = re.findall(r'<h2[^>]*>([^<]+)</h2>', html)
    destinations = []
    skip_words = ["faq", "frequently", "avoid", "skip", "methodology", "how we", "tl;dr", "bottom line", "places to avoid", "where not", "conclusion", "contents", "month-at-a-glance", "compared"]
    
    for text in headings:
        text = text.strip()
        if any(skip in text.lower() for skip in skip_words):
            continue
        text = re.sub(r'^\d+\.\s*', '', text)
        text = re.sub(r'[\U0001F300-\U0001F9FF]', '', text).strip()
        if text and len(text) > 2:
            destinations.append(text)
    
    return destinations[:15]

def extract_faq_from_html(html):
    """Extract FAQ Q&A pairs from the HTML if an FAQ section exists."""
    faqs = []
    # Look for FAQ section patterns
    faq_section = re.search(r'(?:id="faq"|class="faq-section"|<h2[^>]*>.*?FAQ.*?</h2>)(.*?)(?=<(?:footer|section class="cta)|$)', html, re.DOTALL | re.IGNORECASE)
    if not faq_section:
        return faqs
    
    faq_html = faq_section.group(0)
    # Extract Q&A pairs - look for h3 or strong/b questions followed by paragraph answers
    questions = re.findall(r'<(?:h3|strong|b)[^>]*>([^<]+)</(?:h3|strong|b)>', faq_html)
    # Get the text after each question until the next question or end
    parts = re.split(r'<(?:h3|strong|b)[^>]*>[^<]+</(?:h3|strong|b)>', faq_html)
    
    for i, q in enumerate(questions):
        q = q.strip().rstrip('?').strip() + '?'
        if i + 1 < len(parts):
            answer_html = parts[i + 1]
            # Strip HTML tags for clean answer text
            answer = re.sub(r'<[^>]+>', ' ', answer_html).strip()
            answer = re.sub(r'\s+', ' ', answer)[:500]  # Cap at 500 chars
            if answer and len(answer) > 20:
                faqs.append({"q": q, "a": answer})
    
    return faqs[:8]  # Cap at 8 FAQs

def build_breadcrumb_schema(month_name):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
            {"@type": "ListItem", "position": 2, "name": f"Best Places to Visit in {month_name}", "item": f"https://tabiji.ai/best-places-to-visit-in-{month_name.lower()}/"}
        ]
    }, indent=8)

def build_itemlist_schema(title, url, destinations):
    items = []
    for i, dest in enumerate(destinations, 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": dest,
            "url": url + f"#{dest.lower().replace(' ', '-').replace(',', '').replace('—', '').strip()}"
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": title,
        "url": url,
        "numberOfItems": len(destinations),
        "itemListElement": items
    }, indent=8)

def build_faq_schema(faqs):
    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }, indent=8)

def process_page(page_dir):
    slug = page_dir.name
    index_file = page_dir / "index.html"
    if not index_file.exists():
        return
    
    html = index_file.read_text(encoding="utf-8")
    original = html
    month_key = extract_month(slug)
    month_name = MONTHS.get(month_key, month_key.title())
    title = extract_title(html)
    url = f"https://tabiji.ai/{slug}/"
    
    # 1. Add speakable to Article schema
    if '"speakable"' not in html and '"Article"' in html:
        # Find the Article schema block
        article_start = html.find('"@type":"Article"')
        if article_start == -1:
            article_start = html.find('"@type": "Article"')
        
        if article_start > 0:
            block_start = html.rfind('<script type="application/ld+json">', 0, article_start)
            block_end = html.find('</script>', article_start)
            if block_start > 0 and block_end > 0:
                block = html[block_start:block_end]
                json_match = re.search(r'\{.*\}', block, re.DOTALL)
                if json_match:
                    try:
                        schema = json.loads(json_match.group(0))
                        schema["speakable"] = {
                            "@type": "SpeakableSpecification",
                            "cssSelector": [".hero h1", ".hero .subtitle"]
                        }
                        new_block = f'<script type="application/ld+json">\n    {json.dumps(schema)}\n    </script>'
                        html = html[:block_start] + new_block + html[block_end + len('</script>'):]
                        stats["speakable_added"] += 1
                    except json.JSONDecodeError:
                        pass
    
    # 2. Add BreadcrumbList
    if "BreadcrumbList" not in html:
        breadcrumb_json = build_breadcrumb_schema(month_name)
        schema_block = f'\n    <script type="application/ld+json">\n    {breadcrumb_json}\n    </script>'
        html = html.replace('</head>', f'{schema_block}\n    </head>')
        stats["breadcrumb_added"] += 1
    
    # 3. Add ItemList for ranked destinations
    if "ItemList" not in html:
        destinations = extract_destinations(html)
        if destinations:
            itemlist_json = build_itemlist_schema(title, url, destinations)
            schema_block = f'\n    <script type="application/ld+json">\n    {itemlist_json}\n    </script>'
            html = html.replace('</head>', f'{schema_block}\n    </head>')
            stats["itemlist_added"] += 1
    
    # 4. Add FAQPage if FAQ content exists but no schema
    if "FAQPage" not in html:
        faqs = extract_faq_from_html(html)
        if faqs:
            faq_json = build_faq_schema(faqs)
            schema_block = f'\n    <script type="application/ld+json">\n    {faq_json}\n    </script>'
            html = html.replace('</head>', f'{schema_block}\n    </head>')
            stats["faq_added"] += 1
    
    if html != original:
        index_file.write_text(html, encoding="utf-8")
        stats["total_processed"] += 1

def main():
    # Find all best-places-to-visit-in-* directories
    dirs = sorted([d for d in TABIJI_DIR.iterdir() if d.is_dir() and d.name.startswith("best-places-to-visit-in-") and (d / "index.html").exists()])
    print(f"Found {len(dirs)} best-places pages to process")
    
    for page_dir in dirs:
        try:
            process_page(page_dir)
        except Exception as e:
            stats["errors"].append(f"{page_dir.name}: {str(e)}")
            print(f"ERROR processing {page_dir.name}: {e}")
    
    print(f"\n=== Results ===")
    print(f"Total pages modified: {stats['total_processed']}")
    print(f"BreadcrumbList added: {stats['breadcrumb_added']}")
    print(f"ItemList added: {stats['itemlist_added']}")
    print(f"FAQPage added: {stats['faq_added']}")
    print(f"Speakable added: {stats['speakable_added']}")
    if stats["errors"]:
        print(f"Errors ({len(stats['errors'])}):")
        for e in stats["errors"]:
            print(f"  - {e}")

if __name__ == "__main__":
    main()
