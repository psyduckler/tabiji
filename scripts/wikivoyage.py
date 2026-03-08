#!/usr/bin/env python3
"""Fetch travel tips from Wikivoyage for a destination.

Usage:
    python3 wikivoyage.py <destination>
    python3 wikivoyage.py Tokyo
    python3 wikivoyage.py "Buenos Aires"

Returns structured JSON with: summary, sections (get_in, get_around, see, do,
buy, eat, drink, sleep, stay_safe, cope), and key practical info.
"""
import sys, json, urllib.request, urllib.parse, re, html

API = "https://en.wikivoyage.org/w/api.php"

def search_page(query: str) -> str:
    """Find the best matching Wikivoyage page title."""
    params = {
        "action": "opensearch",
        "search": query,
        "limit": 5,
        "format": "json"
    }
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "tabiji/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    titles = data[1] if len(data) > 1 else []
    if not titles:
        raise ValueError(f"No Wikivoyage page found for: {query}")
    return titles[0]

def get_page_content(title: str) -> str:
    """Get the full wikitext of a page."""
    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json"
    }
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "tabiji/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    return data.get("parse", {}).get("wikitext", {}).get("*", "")

def clean_wikitext(text: str) -> str:
    """Strip wikitext markup to plain text."""
    text = re.sub(r'\{\{[^}]*\}\}', '', text)  # templates
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', text)  # links
    text = re.sub(r"'''?", '', text)  # bold/italic
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)  # refs
    text = re.sub(r'<[^>]+>', '', text)  # HTML tags
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = html.unescape(text)
    return text.strip()

def parse_sections(wikitext: str) -> dict:
    """Parse wikitext into named sections."""
    section_pattern = re.compile(r'^(={2,})\s*(.+?)\s*\1\s*$', re.MULTILINE)
    sections = {}
    matches = list(section_pattern.finditer(wikitext))

    for i, match in enumerate(matches):
        level = len(match.group(1))
        name = match.group(2).strip().lower().replace(' ', '_')
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(wikitext)
        content = clean_wikitext(wikitext[start:end]).strip()
        if content and len(content) > 20:
            # Truncate very long sections
            if len(content) > 2000:
                content = content[:2000] + "..."
            sections[name] = content

    return sections

TRAVEL_SECTIONS = [
    "understand", "get_in", "get_around", "see", "do", "buy",
    "eat", "drink", "sleep", "stay_safe", "cope", "connect",
    "respect", "talk", "budget", "climate"
]

def fetch_destination(name: str) -> dict:
    title = search_page(name)
    wikitext = get_page_content(title)

    # Extract intro (before first section)
    first_section = re.search(r'^==', wikitext, re.MULTILINE)
    intro = clean_wikitext(wikitext[:first_section.start()]) if first_section else clean_wikitext(wikitext[:500])
    if len(intro) > 1000:
        intro = intro[:1000] + "..."

    all_sections = parse_sections(wikitext)

    # Filter to travel-relevant sections
    travel_info = {}
    for key in TRAVEL_SECTIONS:
        if key in all_sections:
            travel_info[key] = all_sections[key]

    return {
        "destination": title,
        "summary": intro,
        "sections": travel_info,
        "url": f"https://en.wikivoyage.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 wikivoyage.py <destination>")
        sys.exit(1)
    dest = " ".join(sys.argv[1:])
    result = fetch_destination(dest)
    print(json.dumps(result, indent=2, ensure_ascii=False))
