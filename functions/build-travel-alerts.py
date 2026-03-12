#!/usr/bin/env python3
"""
Build Travel Alerts v1 for tabiji.ai
Fetches data from US State Dept, UK FCDO, CDC, GDACS and generates static HTML pages.
Re-runnable (idempotent) — designed for cron every 6h.
"""

import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import json
import os
import re
import html
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

TABIJI_ROOT = Path(__file__).resolve().parent.parent
ALERTS_DIR = TABIJI_ROOT / "alerts"
POPULAR_PICKS_DIR = TABIJI_ROOT / "popular-picks"
ITINERARIES_DIR = TABIJI_ROOT / "i"

# Country name normalization map
COUNTRY_ALIASES = {
    "Korea, Republic of": "South Korea",
    "Korea, Democratic People's Republic of": "North Korea",
    "Korea, North": "North Korea",
    "Korea, South": "South Korea",
    "Russian Federation": "Russia",
    "Viet Nam": "Vietnam",
    "Lao People's Democratic Republic": "Laos",
    "Syrian Arab Republic": "Syria",
    "Iran, Islamic Republic of": "Iran",
    "Venezuela, Bolivarian Republic of": "Venezuela",
    "Bolivia, Plurinational State of": "Bolivia",
    "Tanzania, United Republic of": "Tanzania",
    "Congo, Democratic Republic of the": "DR Congo",
    "Congo, Republic of the": "Republic of the Congo",
    "Cote d'Ivoire": "Ivory Coast",
    "Côte d'Ivoire": "Ivory Coast",
    "Cabo Verde": "Cape Verde",
    "Eswatini": "Eswatini",
    "Czechia": "Czech Republic",
    "Türkiye": "Turkey",
    "Turkiye": "Turkey",
    "Burma": "Myanmar",
    "The Bahamas": "Bahamas",
    "The Gambia": "Gambia",
    "Timor-Leste": "East Timor",
    "Brunei Darussalam": "Brunei",
    "Micronesia, Federated States of": "Micronesia",
    "Moldova, Republic of": "Moldova",
    "North Macedonia, Republic of": "North Macedonia",
    "Palestine": "Palestinian Territories",
    "West Bank and Gaza": "Palestinian Territories",
    "The West Bank and Gaza": "Palestinian Territories",
    "Hong Kong": "Hong Kong",
    "Macau": "Macau",
    "Taiwan": "Taiwan",
    "United Kingdom": "United Kingdom",
    "UK": "United Kingdom",
}

# Flag emojis for common countries
COUNTRY_FLAGS = {
    "Afghanistan": "🇦🇫", "Albania": "🇦🇱", "Algeria": "🇩🇿", "Argentina": "🇦🇷",
    "Armenia": "🇦🇲", "Australia": "🇦🇺", "Austria": "🇦🇹", "Azerbaijan": "🇦🇿",
    "Bahamas": "🇧🇸", "Bahrain": "🇧🇭", "Bangladesh": "🇧🇩", "Barbados": "🇧🇧",
    "Belarus": "🇧🇾", "Belgium": "🇧🇪", "Belize": "🇧🇿", "Benin": "🇧🇯",
    "Bhutan": "🇧🇹", "Bolivia": "🇧🇴", "Bosnia and Herzegovina": "🇧🇦",
    "Botswana": "🇧🇼", "Brazil": "🇧🇷", "Brunei": "🇧🇳", "Bulgaria": "🇧🇬",
    "Burkina Faso": "🇧🇫", "Burundi": "🇧🇮", "Cambodia": "🇰🇭", "Cameroon": "🇨🇲",
    "Canada": "🇨🇦", "Cape Verde": "🇨🇻", "Central African Republic": "🇨🇫",
    "Chad": "🇹🇩", "Chile": "🇨🇱", "China": "🇨🇳", "Colombia": "🇨🇴",
    "Comoros": "🇰🇲", "Costa Rica": "🇨🇷", "Croatia": "🇭🇷", "Cuba": "🇨🇺",
    "Cyprus": "🇨🇾", "Czech Republic": "🇨🇿", "DR Congo": "🇨🇩", "Denmark": "🇩🇰",
    "Djibouti": "🇩🇯", "Dominican Republic": "🇩🇴", "East Timor": "🇹🇱",
    "Ecuador": "🇪🇨", "Egypt": "🇪🇬", "El Salvador": "🇸🇻",
    "Equatorial Guinea": "🇬🇶", "Eritrea": "🇪🇷", "Estonia": "🇪🇪",
    "Eswatini": "🇸🇿", "Ethiopia": "🇪🇹", "Fiji": "🇫🇯", "Finland": "🇫🇮",
    "France": "🇫🇷", "Gabon": "🇬🇦", "Gambia": "🇬🇲", "Georgia": "🇬🇪",
    "Germany": "🇩🇪", "Ghana": "🇬🇭", "Greece": "🇬🇷", "Grenada": "🇬🇩",
    "Guatemala": "🇬🇹", "Guinea": "🇬🇳", "Guinea-Bissau": "🇬🇼", "Guyana": "🇬🇾",
    "Haiti": "🇭🇹", "Honduras": "🇭🇳", "Hong Kong": "🇭🇰", "Hungary": "🇭🇺",
    "Iceland": "🇮🇸", "India": "🇮🇳", "Indonesia": "🇮🇩", "Iran": "🇮🇷",
    "Iraq": "🇮🇶", "Ireland": "🇮🇪", "Israel": "🇮🇱", "Italy": "🇮🇹",
    "Ivory Coast": "🇨🇮", "Jamaica": "🇯🇲", "Japan": "🇯🇵", "Jordan": "🇯🇴",
    "Kazakhstan": "🇰🇿", "Kenya": "🇰🇪", "Kuwait": "🇰🇼", "Kyrgyzstan": "🇰🇬",
    "Laos": "🇱🇦", "Latvia": "🇱🇻", "Lebanon": "🇱🇧", "Lesotho": "🇱🇸",
    "Liberia": "🇱🇷", "Libya": "🇱🇾", "Lithuania": "🇱🇹", "Luxembourg": "🇱🇺",
    "Macau": "🇲🇴", "Madagascar": "🇲🇬", "Malawi": "🇲🇼", "Malaysia": "🇲🇾",
    "Maldives": "🇲🇻", "Mali": "🇲🇱", "Malta": "🇲🇹", "Mauritania": "🇲🇷",
    "Mauritius": "🇲🇺", "Mexico": "🇲🇽", "Moldova": "🇲🇩", "Mongolia": "🇲🇳",
    "Montenegro": "🇲🇪", "Morocco": "🇲🇦", "Mozambique": "🇲🇿", "Myanmar": "🇲🇲",
    "Namibia": "🇳🇦", "Nepal": "🇳🇵", "Netherlands": "🇳🇱", "New Zealand": "🇳🇿",
    "Nicaragua": "🇳🇮", "Niger": "🇳🇪", "Nigeria": "🇳🇬", "North Korea": "🇰🇵",
    "North Macedonia": "🇲🇰", "Norway": "🇳🇴", "Oman": "🇴🇲", "Pakistan": "🇵🇰",
    "Palestinian Territories": "🇵🇸", "Panama": "🇵🇦", "Papua New Guinea": "🇵🇬",
    "Paraguay": "🇵🇾", "Peru": "🇵🇪", "Philippines": "🇵🇭", "Poland": "🇵🇱",
    "Portugal": "🇵🇹", "Qatar": "🇶🇦", "Republic of the Congo": "🇨🇬",
    "Romania": "🇷🇴", "Russia": "🇷🇺", "Rwanda": "🇷🇼",
    "Saudi Arabia": "🇸🇦", "Senegal": "🇸🇳", "Serbia": "🇷🇸",
    "Sierra Leone": "🇸🇱", "Singapore": "🇸🇬", "Slovakia": "🇸🇰",
    "Slovenia": "🇸🇮", "Somalia": "🇸🇴", "South Africa": "🇿🇦",
    "South Korea": "🇰🇷", "South Sudan": "🇸🇸", "Spain": "🇪🇸",
    "Sri Lanka": "🇱🇰", "Sudan": "🇸🇩", "Suriname": "🇸🇷", "Sweden": "🇸🇪",
    "Switzerland": "🇨🇭", "Syria": "🇸🇾", "Taiwan": "🇹🇼", "Tajikistan": "🇹🇯",
    "Tanzania": "🇹🇿", "Thailand": "🇹🇭", "Togo": "🇹🇬",
    "Trinidad and Tobago": "🇹🇹", "Tunisia": "🇹🇳", "Turkey": "🇹🇷",
    "Turkmenistan": "🇹🇲", "Uganda": "🇺🇬", "Ukraine": "🇺🇦",
    "United Arab Emirates": "🇦🇪", "United Kingdom": "🇬🇧", "United States": "🇺🇸",
    "Uruguay": "🇺🇾", "Uzbekistan": "🇺🇿", "Venezuela": "🇻🇪",
    "Vietnam": "🇻🇳", "Yemen": "🇾🇪", "Zambia": "🇿🇲", "Zimbabwe": "🇿🇼",
}


def slugify(name):
    """Convert country name to URL-friendly slug."""
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def normalize_country(name):
    """Normalize country name."""
    name = name.strip()
    if name in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[name]
    return name


def fetch_url(url, timeout=30):
    """Fetch URL content with error handling."""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'tabiji.ai/1.0 (travel alerts aggregator)'
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  ⚠️  Failed to fetch {url}: {e}")
        return None


def fetch_state_dept():
    """Fetch US State Department travel advisories."""
    print("📡 Fetching US State Department advisories...")
    content = fetch_url("https://travel.state.gov/_res/rss/TAsTWs.xml")
    if not content:
        return {}

    root = ET.fromstring(content)
    advisories = {}

    for item in root.findall('.//item'):
        title = item.findtext('title', '')
        # Parse "Country - Level X: Description"
        match = re.match(r'^(.+?)\s*-\s*Level\s*(\d):\s*(.+)$', title)
        if not match:
            continue

        country = normalize_country(match.group(1).strip())
        level = int(match.group(2))
        level_text = match.group(3).strip()

        desc_raw = item.findtext('description', '')
        # Strip HTML tags for plain text summary
        desc_clean = re.sub(r'<[^>]+>', ' ', desc_raw)
        desc_clean = re.sub(r'\s+', ' ', desc_clean).strip()
        # Keep first ~500 chars for summary
        summary = desc_clean[:500] + ('...' if len(desc_clean) > 500 else '')

        # Extract risk categories from description
        risk_categories = []
        risk_keywords = {
            'crime': 'Crime', 'terrorism': 'Terrorism', 'civil unrest': 'Civil Unrest',
            'kidnapping': 'Kidnapping', 'armed conflict': 'Armed Conflict',
            'landmines': 'Landmines', 'health': 'Health',
            'natural disaster': 'Natural Disaster', 'wrongful detention': 'Wrongful Detention',
        }
        desc_lower = desc_clean.lower()
        for keyword, label in risk_keywords.items():
            if keyword in desc_lower:
                risk_categories.append(label)

        pub_date = item.findtext('pubDate', '')
        link = item.findtext('link', '')

        advisories[country] = {
            'level': level,
            'level_text': level_text,
            'summary': summary,
            'risk_categories': risk_categories,
            'date': pub_date,
            'link': link,
            'full_html': desc_raw,
        }

    print(f"  ✅ Got {len(advisories)} advisories")
    return advisories


def fetch_fcdo():
    """Fetch UK FCDO travel advice."""
    print("📡 Fetching UK FCDO travel advice...")
    content = fetch_url("https://www.gov.uk/foreign-travel-advice.atom")
    if not content:
        return {}

    ns = {'atom': 'http://www.w3.org/2005/Atom', 'xhtml': 'http://www.w3.org/1999/xhtml'}
    root = ET.fromstring(content)
    advice = {}

    for entry in root.findall('atom:entry', ns):
        country = normalize_country(entry.findtext('atom:title', '', ns).strip())
        updated = entry.findtext('atom:updated', '', ns)
        link_el = entry.find('atom:link[@rel="alternate"]', ns)
        link = link_el.get('href', '') if link_el is not None else ''

        summary_el = entry.find('.//atom:summary', ns)
        summary_text = ''
        if summary_el is not None:
            # Get text content from the XHTML div
            summary_text = ET.tostring(summary_el, encoding='unicode', method='text').strip()
            summary_text = re.sub(r'\s+', ' ', summary_text).strip()

        advice[country] = {
            'summary': summary_text[:400] + ('...' if len(summary_text) > 400 else ''),
            'updated': updated,
            'link': link,
        }

    print(f"  ✅ Got {len(advice)} FCDO entries")
    return advice


def fetch_cdc():
    """Fetch CDC travel health notices by scraping the page."""
    print("📡 Fetching CDC travel health notices...")
    content = fetch_url("https://wwwnc.cdc.gov/travel/notices")
    if not content:
        return {}

    notices = {}
    # Find all notice links
    pattern = r'<a href="/travel/notices/(level\d)/([^"]+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, content)

    for level_str, slug, title in matches:
        level = int(level_str.replace('level', ''))
        # Extract country from title like "Chikungunya in Mayotte" or "Rabies in Morocco"
        country_match = re.search(r'\bin\s+(?:the\s+)?(.+)$', title, re.IGNORECASE)
        if country_match:
            countries_raw = country_match.group(1).strip()
            # Handle "Ghana and Liberia" → multiple countries
            country_list = re.split(r'\s+and\s+', countries_raw)
            for c in country_list:
                country = normalize_country(c.strip())
                if country not in notices:
                    notices[country] = []
                notices[country].append({
                    'title': title.strip(),
                    'level': level,
                    'link': f"https://wwwnc.cdc.gov/travel/notices/{level_str}/{slug}",
                })
        else:
            # Global notices
            if 'Global' not in notices:
                notices['Global'] = []
            notices['Global'].append({
                'title': title.strip(),
                'level': level,
                'link': f"https://wwwnc.cdc.gov/travel/notices/{level_str}/{slug}",
            })

    total = sum(len(v) for v in notices.values())
    print(f"  ✅ Got {total} CDC notices across {len(notices)} countries/regions")
    return notices


def fetch_gdacs():
    """Fetch GDACS disaster alerts."""
    print("📡 Fetching GDACS disaster alerts...")
    content = fetch_url("https://www.gdacs.org/xml/rss.xml")
    if not content:
        return {}

    ns = {
        'gdacs': 'http://www.gdacs.org',
        'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    }
    root = ET.fromstring(content)
    disasters = []

    for item in root.findall('.//item'):
        title = item.findtext('title', '')
        desc = item.findtext('description', '')
        link = item.findtext('link', '')
        alert_level = item.findtext('gdacs:alertlevel', '', ns)
        event_type = item.findtext('gdacs:eventtype', '', ns)
        severity = item.find('gdacs:severity', ns)
        severity_text = severity.text if severity is not None else ''

        # Extract country from title (after "in")
        country_match = re.search(r'\bin\s+(.+?)(?:\s+\d{1,2}/|\s+on\s+)', title)
        if not country_match:
            country_match = re.search(r'\bin\s+(.+?)(?:,|\s+potentially)', title)

        country = ''
        if country_match:
            country = normalize_country(country_match.group(1).strip().rstrip('.'))

        # Map event types
        event_type_map = {
            'EQ': '🌍 Earthquake', 'TC': '🌀 Cyclone', 'FL': '🌊 Flood',
            'VO': '🌋 Volcano', 'DR': '☀️ Drought', 'WF': '🔥 Wildfire',
            'TS': '🌊 Tsunami',
        }
        event_label = event_type_map.get(event_type, event_type)

        # Only include Orange and Red alerts (significant ones)
        if alert_level in ('Orange', 'Red'):
            disasters.append({
                'title': title,
                'country': country,
                'alert_level': alert_level,
                'event_type': event_type,
                'event_label': event_label,
                'severity': severity_text,
                'link': link,
                'description': desc,
            })

    print(f"  ✅ Got {len(disasters)} significant GDACS alerts (Orange/Red)")
    return disasters


def find_tabiji_links(country_slug):
    """Find existing tabiji content for a country."""
    links = []

    # Check popular-picks (country-level directory)
    pp_dir = POPULAR_PICKS_DIR / country_slug
    if pp_dir.is_dir():
        links.append({
            'url': f'/popular-picks/{country_slug}/',
            'label': 'Popular Picks Guide',
            'icon': '🧡',
        })

    # Check for popular-picks with country prefix
    if POPULAR_PICKS_DIR.exists():
        for d in POPULAR_PICKS_DIR.iterdir():
            if d.is_dir() and d.name.startswith(country_slug + '-') and d.name != country_slug:
                nice_name = d.name.replace(country_slug + '-', '').replace('-', ' ').title()
                links.append({
                    'url': f'/popular-picks/{d.name}/',
                    'label': f'{nice_name}',
                    'icon': '📍',
                })

    return links[:5]  # Cap at 5 links


def get_level_color(level):
    """Get color for US advisory level."""
    return {1: '#22c55e', 2: '#eab308', 3: '#f97316', 4: '#ef4444'}.get(level, '#94a3b8')


def get_level_bg(level):
    """Get background color for US advisory level."""
    return {1: '#f0fdf4', 2: '#fefce8', 3: '#fff7ed', 4: '#fef2f2'}.get(level, '#f8fafc')


def get_level_label(level):
    """Get short label for advisory level."""
    return {
        1: 'Exercise Normal Precautions',
        2: 'Exercise Increased Caution',
        3: 'Reconsider Travel',
        4: 'Do Not Travel',
    }.get(level, 'Unknown')


def build_html_head(title, description, canonical_path):
    """Generate HTML head section matching tabiji design."""
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-D7QHNRXLHJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-D7QHNRXLHJ');
    </script>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.tabiji.ai/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://img.tabiji.ai/icon-192.png">
    <title>{html.escape(title)} | tabiji.ai</title>
    <meta name="description" content="{html.escape(description)}">
    <meta property="og:title" content="{html.escape(title)} — tabiji.ai">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://tabiji.ai{canonical_path}">
    <meta property="og:site_name" content="tabiji.ai">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{html.escape(title)}">
    <meta name="twitter:description" content="{html.escape(description)}">
    <meta property="article:modified_time" content="{now}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://tabiji.ai{canonical_path}">
'''


def build_css():
    """Generate CSS matching tabiji design system."""
    return '''    <style>
        :root {
            --indigo: #2D3A5C;
            --indigo-light: #3D4E7A;
            --warm-cream: #F5F0E8;
            --sand: #E8DFD0;
            --earth: #8B7355;
            --earth-light: #A6906F;
            --terracotta: #C4704B;
            --deep-brown: #3E2F23;
            --sage: #7A8B6F;
            --white: #FEFCF9;
            --text: #2C2419;
            --text-muted: #6B5D4F;
            --level-1: #22c55e; --level-1-bg: #f0fdf4;
            --level-2: #eab308; --level-2-bg: #fefce8;
            --level-3: #f97316; --level-3-bg: #fff7ed;
            --level-4: #ef4444; --level-4-bg: #fef2f2;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            color: var(--text); background: var(--white); line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }
        nav {
            position: fixed; top: 0; width: 100%; z-index: 100;
            background: rgba(254, 252, 249, 0.92);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--sand);
            padding: 1rem 2rem;
            display: flex; justify-content: space-between; align-items: center;
        }
        .logo { font-size: 1.4rem; font-weight: 700; color: var(--indigo); text-decoration: none; letter-spacing: -0.02em; }
        .logo span { color: var(--terracotta); }
        .logo { position: relative; }
        .logo .owl-fly { display: none; }
        .logo:hover .owl-default { display: none; }
        .logo:hover .owl-fly { display: inline; }
        nav a.cta-nav {
            background: var(--terracotta); color: white;
            padding: 0.5rem 1.2rem; border-radius: 8px;
            text-decoration: none; font-size: 0.9rem; font-weight: 500;
            transition: background 0.2s;
        }
        nav a.cta-nav:hover { background: #b5633f; }
        .hamburger {
            display: none; background: none; border: none; font-size: 1.5rem;
            cursor: pointer; color: var(--indigo);
        }
        .nav-links {
            display: flex; align-items: center; gap: 1.5rem;
        }
        .nav-links a { color: var(--indigo); text-decoration: none; font-size: 0.9rem; font-weight: 500; }
        .nav-dropdown { position: relative; }
        .nav-dropdown-toggle {
            background: none; border: none; color: var(--indigo);
            font-size: 0.9rem; font-weight: 500; cursor: pointer; padding: 0.25rem 0;
        }
        .nav-dropdown-menu {
            display: none; position: absolute; top: 100%; left: 0;
            background: white; border: 1px solid var(--sand); border-radius: 8px;
            padding: 0.5rem 0; min-width: 220px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            z-index: 200;
        }
        .nav-dropdown.open .nav-dropdown-menu { display: block; }
        .nav-dropdown-menu a {
            display: block; padding: 0.5rem 1rem; color: var(--text);
            text-decoration: none; font-size: 0.85rem;
        }
        .nav-dropdown-menu a:hover { background: var(--warm-cream); }
        .hero {
            padding: 7rem 2rem 2rem;
            max-width: 900px; margin: 0 auto;
        }
        .hero-badge {
            display: inline-block;
            background: var(--sand); color: var(--earth);
            padding: 0.3rem 0.8rem; border-radius: 20px;
            font-size: 0.85rem; margin-bottom: 1rem;
        }
        .hero h1 {
            font-size: 2.4rem; font-weight: 800; color: var(--indigo);
            line-height: 1.15; margin-bottom: 0.75rem;
        }
        .hero h1 em { font-style: normal; color: var(--terracotta); }
        .hero p { color: var(--text-muted); font-size: 1.05rem; max-width: 650px; }
        .stats-bar {
            display: flex; gap: 1.5rem; flex-wrap: wrap;
            margin: 1.5rem 0; padding: 1rem 0;
            border-top: 1px solid var(--sand); border-bottom: 1px solid var(--sand);
        }
        .stat { text-align: center; }
        .stat-num { font-size: 1.8rem; font-weight: 800; color: var(--indigo); }
        .stat-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
        .controls {
            max-width: 900px; margin: 0 auto; padding: 0 2rem 1rem;
            display: flex; gap: 0.75rem; flex-wrap: wrap; align-items: center;
        }
        .search-input {
            flex: 1; min-width: 200px; padding: 0.6rem 1rem;
            border: 1px solid var(--sand); border-radius: 8px;
            font-size: 0.95rem; background: white; color: var(--text);
        }
        .search-input:focus { outline: none; border-color: var(--terracotta); }
        .filter-btn {
            padding: 0.5rem 1rem; border: 1px solid var(--sand);
            border-radius: 20px; background: white; color: var(--text);
            font-size: 0.85rem; cursor: pointer; transition: all 0.2s;
        }
        .filter-btn:hover, .filter-btn.active {
            background: var(--indigo); color: white; border-color: var(--indigo);
        }
        .filter-btn.level-1.active { background: var(--level-1); border-color: var(--level-1); }
        .filter-btn.level-2.active { background: var(--level-2); border-color: var(--level-2); color: #000; }
        .filter-btn.level-3.active { background: var(--level-3); border-color: var(--level-3); }
        .filter-btn.level-4.active { background: var(--level-4); border-color: var(--level-4); }
        .sort-select {
            padding: 0.5rem 0.75rem; border: 1px solid var(--sand);
            border-radius: 8px; font-size: 0.85rem; background: white; color: var(--text);
        }
        .country-grid {
            max-width: 900px; margin: 0 auto; padding: 1rem 2rem 3rem;
            display: grid; gap: 0.75rem;
        }
        .country-card {
            display: flex; align-items: center; gap: 1rem;
            padding: 1rem 1.25rem; border: 1px solid var(--sand);
            border-radius: 10px; background: white;
            text-decoration: none; color: var(--text);
            transition: all 0.2s;
        }
        .country-card:hover {
            border-color: var(--terracotta); box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transform: translateY(-1px);
        }
        .level-badge {
            display: inline-flex; align-items: center; justify-content: center;
            width: 36px; height: 36px; border-radius: 8px;
            font-weight: 800; font-size: 1.1rem; flex-shrink: 0;
        }
        .level-badge.l1 { background: var(--level-1-bg); color: #16a34a; }
        .level-badge.l2 { background: var(--level-2-bg); color: #a16207; }
        .level-badge.l3 { background: var(--level-3-bg); color: #ea580c; }
        .level-badge.l4 { background: var(--level-4-bg); color: #dc2626; }
        .card-info { flex: 1; min-width: 0; }
        .card-country { font-weight: 600; font-size: 1rem; }
        .card-flag { margin-right: 0.25rem; }
        .card-level-text { font-size: 0.8rem; color: var(--text-muted); }
        .card-tags { display: flex; gap: 0.35rem; flex-wrap: wrap; margin-top: 0.25rem; }
        .card-tag {
            font-size: 0.7rem; padding: 0.15rem 0.5rem;
            border-radius: 10px; background: var(--warm-cream); color: var(--earth);
        }
        .card-tag.health { background: #fef3c7; color: #92400e; }
        .card-tag.disaster { background: #fce7f3; color: #9d174d; }
        .card-tag.fcdo { background: #ede9fe; color: #5b21b6; }
        .card-date { font-size: 0.75rem; color: var(--text-muted); white-space: nowrap; }
        /* Country detail page */
        .detail-content {
            max-width: 800px; margin: 0 auto; padding: 0 2rem 3rem;
        }
        .alert-section {
            margin-bottom: 2rem; padding: 1.5rem;
            border: 1px solid var(--sand); border-radius: 12px;
            background: white;
        }
        .alert-section h2 {
            font-size: 1.2rem; font-weight: 700; color: var(--indigo);
            margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;
        }
        .alert-section p { font-size: 0.95rem; color: var(--text-muted); line-height: 1.7; }
        .alert-section a { color: var(--terracotta); }
        .risk-tags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin: 0.75rem 0; }
        .risk-tag {
            font-size: 0.8rem; padding: 0.25rem 0.75rem;
            border-radius: 15px; font-weight: 500;
        }
        .big-level-badge {
            display: inline-flex; align-items: center; gap: 0.75rem;
            padding: 0.75rem 1.25rem; border-radius: 10px;
            font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;
        }
        .big-level-badge.l1 { background: var(--level-1-bg); color: #16a34a; }
        .big-level-badge.l2 { background: var(--level-2-bg); color: #a16207; }
        .big-level-badge.l3 { background: var(--level-3-bg); color: #ea580c; }
        .big-level-badge.l4 { background: var(--level-4-bg); color: #dc2626; }
        .tabiji-links {
            display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1rem;
        }
        .tabiji-link {
            display: inline-flex; align-items: center; gap: 0.35rem;
            padding: 0.5rem 1rem; border: 1px solid var(--sand);
            border-radius: 8px; text-decoration: none; color: var(--terracotta);
            font-size: 0.9rem; font-weight: 500; transition: all 0.2s;
        }
        .tabiji-link:hover { background: var(--warm-cream); border-color: var(--terracotta); }
        .source-link {
            display: inline-block; margin-top: 0.5rem;
            font-size: 0.8rem; color: var(--terracotta);
        }
        .back-link {
            display: inline-flex; align-items: center; gap: 0.25rem;
            color: var(--terracotta); text-decoration: none; font-size: 0.9rem;
            font-weight: 500; margin-bottom: 1rem;
        }
        .cdc-notice {
            padding: 0.75rem 1rem; border-radius: 8px;
            margin-bottom: 0.5rem; font-size: 0.9rem;
        }
        .cdc-notice.cdc-l1 { background: #fef9c3; border-left: 3px solid #eab308; }
        .cdc-notice.cdc-l2 { background: #fff7ed; border-left: 3px solid #f97316; }
        .disaster-item {
            padding: 0.75rem 1rem; border-radius: 8px;
            background: #fef2f2; border-left: 3px solid #ef4444;
            margin-bottom: 0.5rem; font-size: 0.9rem;
        }
        .disaster-item.orange { background: #fff7ed; border-left-color: #f97316; }
        .updated-text {
            font-size: 0.8rem; color: var(--text-muted);
            margin-top: 2rem; text-align: center;
            padding-top: 1rem; border-top: 1px solid var(--sand);
        }
        footer {
            text-align: center; padding: 2rem; font-size: 0.8rem;
            color: var(--text-muted); border-top: 1px solid var(--sand);
        }
        footer a { color: var(--terracotta); text-decoration: none; }
        footer a:hover { text-decoration: underline; }
        @media (max-width: 640px) {
            .hamburger { display: block; }
            .nav-links {
                display: none; flex-direction: column;
                position: absolute; top: 100%; left: 0; right: 0;
                background: white; border-bottom: 1px solid var(--sand);
                padding: 1rem; gap: 0.75rem;
            }
            .nav-links.open { display: flex; }
            .hero h1 { font-size: 1.7rem; }
            .stats-bar { gap: 1rem; }
            .controls { flex-direction: column; }
            .country-card { flex-wrap: wrap; }
        }
    </style>
'''


def build_nav():
    """Generate nav bar matching tabiji design."""
    return '''<nav>
    <a href="/" class="logo"><img class="owl-default" src="https://img.tabiji.ai/tabiji-owl-logo.png" alt="tabiji.ai" style="height:32px;vertical-align:middle;margin-right:6px;"><img class="owl-fly" src="https://img.tabiji.ai/tabiji-owl-logo-flying.png?v=2" alt="tabiji.ai" style="height:32px;vertical-align:middle;margin-right:6px;">tabiji<span>.ai</span></a>
    <button class="hamburger" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Menu">☰</button>
    <div class="nav-links">
        <div class="nav-dropdown">
            <button class="nav-dropdown-toggle" onclick="this.parentElement.classList.toggle('open')">Explore</button>
            <div class="nav-dropdown-menu">
                <a href="/compare/">🆚 Compare Destinations</a>
                <a href="/find/">🔍 Destination Finder</a>
                <a href="/spin/">🌎 Spin the Globe</a>
                <a href="/resources/">📚 Resources</a>
                <a href="/owl/">🧭 Tabiji Travel Agency</a>
                <a href="/trends/">📊 Travel Trends</a>
                <a href="/alerts/">⚠️ Travel Alerts</a>
                <a href="/api/">🔌 API</a>
            </div>
        </div>
        <a href="/itineraries/" style="color:var(--indigo);text-decoration:none;font-size:0.9rem;font-weight:500;">Sample Itineraries</a>
        <a href="/popular-picks/" style="color:var(--terracotta);text-decoration:none;font-size:0.9rem;font-weight:600;">Popular Picks</a>
        <a href="/about/" style="color:var(--indigo);text-decoration:none;font-size:0.9rem;font-weight:500;">About</a>
        <a href="/plan" class="cta-nav">Get Your Free Custom Itinerary</a>
    </div>
</nav>
'''


def build_footer():
    """Generate footer matching tabiji design."""
    return '''<footer>
    <p><strong>tabiji.ai</strong> — AI-powered travel planning, backed by real traveler wisdom.</p>
    <p style="margin-top: 0.5rem;">Data from US State Dept, UK FCDO, CDC, and GDACS. Auto-updated every 6 hours.</p>
    <p style="margin-top: 1rem;">
        <a href="/alerts/">← All Travel Alerts</a> &nbsp;·&nbsp;
        <a href="/popular-picks/">Popular Picks</a> &nbsp;·&nbsp;
        <a href="/plan">Plan Your Trip →</a>
        &nbsp;·&nbsp; <a href="/terms/">Terms</a> · <a href="/privacy/">Privacy</a> · <a href="/delete-data/">Delete My Data</a> · <a href="https://www.instagram.com/tabiji.ai/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.youtube.com/@tabijiai" target="_blank" rel="noopener">YouTube</a> · <a href="https://www.pinterest.com/tabijiai/" target="_blank" rel="noopener">Pinterest</a> · <a href="https://x.com/tabijiai" target="_blank" rel="noopener">X</a> · <a href="/api/">API</a>
    </p>
</footer>
'''


def build_dashboard(countries_data, state_dept, fcdo, cdc, gdacs):
    """Build the main dashboard page."""
    print("🏗️  Building dashboard...")
    now = datetime.now(timezone.utc).strftime('%B %d, %Y at %H:%M UTC')

    # Stats
    total_countries = len(countries_data)
    level_counts = defaultdict(int)
    for c in countries_data.values():
        if 'us_level' in c:
            level_counts[c['us_level']] += 1
    health_countries = len([c for c in countries_data.values() if c.get('cdc_notices')])
    disaster_count = len(gdacs)

    # Sort countries by level (highest first), then name
    sorted_countries = sorted(
        countries_data.items(),
        key=lambda x: (-x[1].get('us_level', 0), x[0])
    )

    # Build country cards JSON for client-side filtering
    cards_json = []
    for name, data in sorted_countries:
        cards_json.append({
            'name': name,
            'slug': data['slug'],
            'level': data.get('us_level', 0),
            'flag': COUNTRY_FLAGS.get(name, '🌍'),
            'risks': data.get('risk_categories', []),
            'has_cdc': bool(data.get('cdc_notices')),
            'has_disaster': bool(data.get('disasters')),
            'has_fcdo': bool(data.get('fcdo')),
            'date': data.get('us_date', ''),
        })

    # Build cards HTML
    cards_html = []
    for name, data in sorted_countries:
        level = data.get('us_level', 0)
        flag = COUNTRY_FLAGS.get(name, '🌍')
        slug = data['slug']
        level_text = data.get('us_level_text', get_level_label(level)) if level else 'No US advisory'

        tags_html = ''
        if data.get('risk_categories'):
            tags_html += ''.join(f'<span class="card-tag">{r}</span>' for r in data['risk_categories'][:3])
        if data.get('cdc_notices'):
            tags_html += f'<span class="card-tag health">🏥 {len(data["cdc_notices"])} health notice{"s" if len(data["cdc_notices"]) > 1 else ""}</span>'
        if data.get('disasters'):
            tags_html += f'<span class="card-tag disaster">⚠️ Active disaster</span>'
        if data.get('fcdo') and not level:
            tags_html += '<span class="card-tag fcdo">🇬🇧 FCDO update</span>'

        date_str = data.get('us_date', data.get('fcdo_updated', ''))
        if date_str:
            # Simplify date display
            try:
                if 'T' in date_str:
                    dt = datetime.fromisoformat(date_str.replace('+00:00', '+00:00'))
                    date_str = dt.strftime('%b %d')
                else:
                    # Parse "Thu, 12 Mar 2026" format
                    parts = date_str.replace(',', '').split()
                    if len(parts) >= 4:
                        date_str = f"{parts[2]} {parts[1]}"
            except:
                pass

        cards_html.append(f'''        <a href="/alerts/{slug}/" class="country-card" data-level="{level}" data-name="{html.escape(name.lower())}" data-cdc="{1 if data.get('cdc_notices') else 0}" data-disaster="{1 if data.get('disasters') else 0}">
            <div class="level-badge l{level}">{level if level else '—'}</div>
            <div class="card-info">
                <div class="card-country"><span class="card-flag">{flag}</span> {html.escape(name)}</div>
                <div class="card-level-text">{html.escape(level_text)}</div>
                <div class="card-tags">{tags_html}</div>
            </div>
            <div class="card-date">{html.escape(date_str)}</div>
        </a>''')

    page = build_html_head(
        'Travel Alerts & Safety — Real-Time Advisories for Every Country',
        f'Live travel advisories for {total_countries}+ countries. US State Dept threat levels, UK FCDO advice, CDC health notices, and active natural disasters — all in one place.',
        '/alerts/'
    )
    page += build_css()
    page += '''</head>
<body>
'''
    page += build_nav()

    page += f'''
<section class="hero">
    <div class="hero-badge">⚠️ Travel Alerts & Safety</div>
    <h1>Travel Alerts & <em>Safety</em></h1>
    <p>Real-time travel advisories from the US State Department, UK Foreign Office, CDC health notices, and global disaster alerts — all in one place.</p>

    <div class="stats-bar">
        <div class="stat">
            <div class="stat-num">{total_countries}</div>
            <div class="stat-label">Countries Tracked</div>
        </div>
        <div class="stat">
            <div class="stat-num" style="color: var(--level-4);">{level_counts.get(4, 0)}</div>
            <div class="stat-label">Do Not Travel</div>
        </div>
        <div class="stat">
            <div class="stat-num" style="color: var(--level-3);">{level_counts.get(3, 0)}</div>
            <div class="stat-label">Reconsider Travel</div>
        </div>
        <div class="stat">
            <div class="stat-num" style="color: var(--level-2);">{level_counts.get(2, 0)}</div>
            <div class="stat-label">Increased Caution</div>
        </div>
        <div class="stat">
            <div class="stat-num" style="color: var(--level-1);">{level_counts.get(1, 0)}</div>
            <div class="stat-label">Normal Precautions</div>
        </div>
    </div>
</section>

<div class="controls">
    <input type="text" class="search-input" placeholder="Search countries..." id="searchInput" oninput="filterCards()">
    <button class="filter-btn" onclick="toggleFilter('all')" id="filter-all">All</button>
    <button class="filter-btn level-4" onclick="toggleFilter(4)" id="filter-4">Level 4</button>
    <button class="filter-btn level-3" onclick="toggleFilter(3)" id="filter-3">Level 3</button>
    <button class="filter-btn level-2" onclick="toggleFilter(2)" id="filter-2">Level 2</button>
    <button class="filter-btn level-1" onclick="toggleFilter(1)" id="filter-1">Level 1</button>
    <button class="filter-btn" onclick="toggleFilter('health')" id="filter-health">🏥 Health</button>
    <button class="filter-btn" onclick="toggleFilter('disaster')" id="filter-disaster">⚠️ Disasters</button>
    <select class="sort-select" id="sortSelect" onchange="sortCards()">
        <option value="level-desc">Highest Risk First</option>
        <option value="level-asc">Lowest Risk First</option>
        <option value="name-asc">A → Z</option>
        <option value="name-desc">Z → A</option>
    </select>
</div>

<div class="country-grid" id="countryGrid">
{chr(10).join(cards_html)}
</div>

<p class="updated-text">Last updated: {now} · Data from <a href="https://travel.state.gov" target="_blank" rel="noopener">US State Dept</a>, <a href="https://www.gov.uk/foreign-travel-advice" target="_blank" rel="noopener">UK FCDO</a>, <a href="https://wwwnc.cdc.gov/travel/notices" target="_blank" rel="noopener">CDC</a>, <a href="https://www.gdacs.org/" target="_blank" rel="noopener">GDACS</a></p>

'''
    page += build_footer()

    # Client-side filtering/sorting JS
    page += '''
<script>
let activeFilter = 'all';
function toggleFilter(f) {
    activeFilter = f;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    if (f === 'all') document.getElementById('filter-all').classList.add('active');
    else if (f === 'health') document.getElementById('filter-health').classList.add('active');
    else if (f === 'disaster') document.getElementById('filter-disaster').classList.add('active');
    else document.getElementById('filter-' + f).classList.add('active');
    filterCards();
}
function filterCards() {
    const q = document.getElementById('searchInput').value.toLowerCase();
    document.querySelectorAll('.country-card').forEach(card => {
        const name = card.dataset.name;
        const level = parseInt(card.dataset.level);
        const cdc = card.dataset.cdc === '1';
        const disaster = card.dataset.disaster === '1';
        let show = true;
        if (q && !name.includes(q)) show = false;
        if (activeFilter === 'health' && !cdc) show = false;
        if (activeFilter === 'disaster' && !disaster) show = false;
        if (typeof activeFilter === 'number' && level !== activeFilter) show = false;
        card.style.display = show ? '' : 'none';
    });
}
function sortCards() {
    const grid = document.getElementById('countryGrid');
    const cards = [...grid.querySelectorAll('.country-card')];
    const sort = document.getElementById('sortSelect').value;
    cards.sort((a, b) => {
        if (sort === 'level-desc') return parseInt(b.dataset.level) - parseInt(a.dataset.level);
        if (sort === 'level-asc') return parseInt(a.dataset.level) - parseInt(b.dataset.level);
        if (sort === 'name-asc') return a.dataset.name.localeCompare(b.dataset.name);
        if (sort === 'name-desc') return b.dataset.name.localeCompare(a.dataset.name);
    });
    cards.forEach(c => grid.appendChild(c));
}
toggleFilter('all');
</script>
</body>
</html>'''

    os.makedirs(ALERTS_DIR, exist_ok=True)
    with open(ALERTS_DIR / 'index.html', 'w') as f:
        f.write(page)
    print(f"  ✅ Dashboard written ({len(sorted_countries)} countries)")


def build_country_page(name, data, cdc, gdacs_for_country):
    """Build a per-country detail page."""
    slug = data['slug']
    flag = COUNTRY_FLAGS.get(name, '🌍')
    level = data.get('us_level', 0)

    page_dir = ALERTS_DIR / slug
    os.makedirs(page_dir, exist_ok=True)

    desc = f"Travel advisory for {name}: US State Dept Level {level}, UK FCDO advice, CDC health notices, and active disasters."

    page = build_html_head(
        f'{flag} {name} Travel Advisory & Safety',
        desc,
        f'/alerts/{slug}/'
    )
    page += build_css()
    page += '</head>\n<body>\n'
    page += build_nav()

    page += f'''
<section class="hero">
    <a href="/alerts/" class="back-link">← All Travel Alerts</a>
    <h1>{flag} {html.escape(name)} <em>Travel Advisory</em></h1>
'''

    if level:
        page += f'''    <div class="big-level-badge l{level}">
        Level {level}: {html.escape(get_level_label(level))}
    </div>
'''

    # Risk tags
    if data.get('risk_categories'):
        page += '    <div class="risk-tags">\n'
        for r in data['risk_categories']:
            color = '#ef4444' if r in ('Terrorism', 'Armed Conflict', 'Kidnapping') else '#f97316' if r in ('Crime', 'Civil Unrest') else '#eab308'
            page += f'        <span class="risk-tag" style="background: {color}20; color: {color};">{html.escape(r)}</span>\n'
        page += '    </div>\n'

    page += '</section>\n\n<div class="detail-content">\n'

    # US State Dept section
    if data.get('us_advisory'):
        adv = data['us_advisory']
        page += f'''<div class="alert-section">
    <h2>🇺🇸 US State Department Advisory</h2>
    <div class="big-level-badge l{level}" style="font-size: 0.95rem; padding: 0.5rem 1rem;">
        Level {level}: {html.escape(adv.get('level_text', get_level_label(level)))}
    </div>
    <p>{html.escape(adv.get('summary', ''))}</p>
    <a class="source-link" href="{html.escape(adv.get('link', ''))}" target="_blank" rel="noopener">Read full advisory on travel.state.gov →</a>
    <div style="margin-top: 0.5rem; font-size: 0.8rem; color: var(--text-muted);">Updated: {html.escape(adv.get('date', ''))}</div>
</div>
'''

    # UK FCDO section
    if data.get('fcdo'):
        fc = data['fcdo']
        page += f'''<div class="alert-section">
    <h2>🇬🇧 UK Foreign Office (FCDO)</h2>
    <p>{html.escape(fc.get('summary', 'See FCDO website for details.'))}</p>
    <a class="source-link" href="{html.escape(fc.get('link', ''))}" target="_blank" rel="noopener">Read full advice on gov.uk →</a>
    <div style="margin-top: 0.5rem; font-size: 0.8rem; color: var(--text-muted);">Updated: {html.escape(fc.get('updated', '')[:10] if fc.get('updated') else '')}</div>
</div>
'''

    # CDC section
    if data.get('cdc_notices'):
        page += '<div class="alert-section">\n    <h2>🏥 CDC Health Notices</h2>\n'
        for notice in data['cdc_notices']:
            css_class = f'cdc-l{notice["level"]}'
            page += f'''    <div class="cdc-notice {css_class}">
        <strong>{html.escape(notice['title'])}</strong>
        — <a href="{html.escape(notice['link'])}" target="_blank" rel="noopener">CDC Level {notice['level']}</a>
    </div>
'''
        page += '</div>\n'

    # GDACS disasters
    if gdacs_for_country:
        page += '<div class="alert-section">\n    <h2>🌍 Active Disasters (GDACS)</h2>\n'
        for d in gdacs_for_country:
            css = 'orange' if d['alert_level'] == 'Orange' else ''
            page += f'''    <div class="disaster-item {css}">
        <strong>{html.escape(d['event_label'])}</strong> — {html.escape(d.get('severity', ''))}
        <br><a href="{html.escape(d['link'])}" target="_blank" rel="noopener" style="font-size:0.8rem; color: var(--terracotta);">View on GDACS →</a>
    </div>
'''
        page += '</div>\n'

    # Tabiji links
    tabiji_links = find_tabiji_links(slug)
    if tabiji_links:
        page += '<div class="alert-section">\n    <h2>✈️ Planning a Trip?</h2>\n'
        page += f'    <p>Despite advisories, many travelers visit {html.escape(name)} safely every year. Check our guides for practical tips:</p>\n'
        page += '    <div class="tabiji-links">\n'
        for link in tabiji_links:
            page += f'        <a href="{link["url"]}" class="tabiji-link">{link["icon"]} {html.escape(link["label"])}</a>\n'
        page += '    </div>\n</div>\n'

    now = datetime.now(timezone.utc).strftime('%B %d, %Y at %H:%M UTC')
    page += f'\n<p class="updated-text">Last updated: {now}</p>\n'
    page += '</div>\n'
    page += build_footer()
    page += '\n</body>\n</html>'

    with open(page_dir / 'index.html', 'w') as f:
        f.write(page)


def build_level_page(level, countries_data):
    """Build a level filter page."""
    level_dir = ALERTS_DIR / f'level-{level}'
    os.makedirs(level_dir, exist_ok=True)

    label = get_level_label(level)
    matching = {n: d for n, d in countries_data.items() if d.get('us_level') == level}
    sorted_countries = sorted(matching.items(), key=lambda x: x[0])

    desc = f"{len(matching)} countries at US State Dept Level {level}: {label}."
    page = build_html_head(f'Level {level}: {label} — Travel Alerts', desc, f'/alerts/level-{level}/')
    page += build_css()
    page += '</head>\n<body>\n'
    page += build_nav()

    color = get_level_color(level)
    page += f'''
<section class="hero">
    <a href="/alerts/" class="back-link">← All Travel Alerts</a>
    <div class="hero-badge" style="background: {get_level_bg(level)}; color: {color};">Level {level}</div>
    <h1 style="color: {color};">Level {level}: <em>{html.escape(label)}</em></h1>
    <p>{len(matching)} countries are currently at Level {level}.</p>
</section>

<div class="country-grid">
'''

    for name, data in sorted_countries:
        flag = COUNTRY_FLAGS.get(name, '🌍')
        slug = data['slug']
        level_text = data.get('us_level_text', label)
        risks = data.get('risk_categories', [])
        tags_html = ''.join(f'<span class="card-tag">{r}</span>' for r in risks[:3])

        page += f'''    <a href="/alerts/{slug}/" class="country-card">
        <div class="level-badge l{level}">{level}</div>
        <div class="card-info">
            <div class="card-country"><span class="card-flag">{flag}</span> {html.escape(name)}</div>
            <div class="card-level-text">{html.escape(level_text)}</div>
            <div class="card-tags">{tags_html}</div>
        </div>
    </a>
'''

    page += '</div>\n'
    page += build_footer()
    page += '\n</body>\n</html>'

    with open(level_dir / 'index.html', 'w') as f:
        f.write(page)
    print(f"  ✅ Level {level} page ({len(matching)} countries)")


def main():
    print("=" * 60)
    print("🚀 Building Travel Alerts v1 for tabiji.ai")
    print("=" * 60)

    # Fetch all sources
    state_dept = fetch_state_dept()
    fcdo = fetch_fcdo()
    cdc = fetch_cdc()
    gdacs = fetch_gdacs()

    # Merge into unified country data
    countries_data = {}

    # Start with State Dept (primary source)
    for country, adv in state_dept.items():
        slug = slugify(country)
        countries_data[country] = {
            'slug': slug,
            'us_level': adv['level'],
            'us_level_text': adv['level_text'],
            'us_date': adv['date'],
            'us_advisory': adv,
            'risk_categories': adv['risk_categories'],
        }

    # Add FCDO data
    for country, advice in fcdo.items():
        if country in countries_data:
            countries_data[country]['fcdo'] = advice
            countries_data[country]['fcdo_updated'] = advice['updated']
        else:
            slug = slugify(country)
            countries_data[country] = {
                'slug': slug,
                'fcdo': advice,
                'fcdo_updated': advice['updated'],
            }

    # Add CDC data
    for country, notices in cdc.items():
        if country == 'Global':
            continue  # Skip global notices for per-country pages
        if country in countries_data:
            countries_data[country]['cdc_notices'] = notices
        else:
            slug = slugify(country)
            countries_data[country] = {
                'slug': slug,
                'cdc_notices': notices,
            }

    # Match GDACS disasters to countries (best-effort)
    gdacs_by_country = defaultdict(list)
    for disaster in gdacs:
        if disaster['country']:
            # Try to match country name
            matched = False
            for cname in countries_data:
                if disaster['country'].lower() in cname.lower() or cname.lower() in disaster['country'].lower():
                    gdacs_by_country[cname].append(disaster)
                    matched = True
                    break
            if not matched:
                norm = normalize_country(disaster['country'])
                gdacs_by_country[norm].append(disaster)

    for country, disasters in gdacs_by_country.items():
        if country in countries_data:
            countries_data[country]['disasters'] = disasters
        else:
            slug = slugify(country)
            countries_data[country] = {
                'slug': slug,
                'disasters': disasters,
            }

    print(f"\n📊 Total: {len(countries_data)} countries")
    print(f"   US State Dept: {len(state_dept)}")
    print(f"   UK FCDO: {len(fcdo)}")
    print(f"   CDC: {sum(len(v) for v in cdc.values())} notices")
    print(f"   GDACS: {len(gdacs)} significant alerts")

    # Build pages
    print(f"\n🏗️  Generating pages...")

    # Dashboard
    build_dashboard(countries_data, state_dept, fcdo, cdc, gdacs)

    # Per-country pages
    for name, data in sorted(countries_data.items()):
        gdacs_for = gdacs_by_country.get(name, [])
        build_country_page(name, data, cdc, gdacs_for)
    print(f"  ✅ {len(countries_data)} country pages")

    # Level filter pages
    for level in range(1, 5):
        build_level_page(level, countries_data)

    print(f"\n✅ Done! {len(countries_data)} country pages + 4 level pages + dashboard")
    print(f"   Output: {ALERTS_DIR}/")


if __name__ == '__main__':
    main()
