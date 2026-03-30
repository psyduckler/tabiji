#!/usr/bin/env python3
"""
Build travel advisories from US State Dept RSS + UK FCDO API.
Output: tabiji/app/data/advisories-us.json, advisories-uk.json
"""

import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from datetime import datetime

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# State Dept 2-letter FIPS codes → ISO 3166-1 alpha-2 mapping (they use FIPS, not ISO)
FIPS_TO_ISO = {
    "AF": "AF", "AL": "AL", "AG": "DZ", "AQ": "AS", "AN": "AD", "AO": "AO",
    "AC": "AG", "AR": "AR", "AM": "AM", "AA": "AW", "AS": "AU", "AU": "AT",
    "AJ": "AZ", "BF": "BS", "BA": "BH", "BG": "BD", "BB": "BB", "BO": "BY",
    "BE": "BE", "BH": "BZ", "BN": "BJ", "BD": "BM", "BT": "BT", "BL": "BO",
    "BK": "BA", "BC": "BW", "BR": "BR", "BX": "BN", "BU": "BG", "UV": "BF",
    "BM": "MM", "BY": "BI", "CV": "CV", "CB": "KH", "CM": "CM", "CA": "CA",
    "CT": "CF", "CD": "TD", "CI": "CL", "CH": "CN", "CO": "CO", "CN": "KM",
    "CG": "CD", "CF": "CG", "CS": "CR", "IV": "CI", "HR": "HR", "CU": "CU",
    "CY": "CY", "EZ": "CZ", "DA": "DK", "DJ": "DJ", "DO": "DM", "DR": "DO",
    "EC": "EC", "EG": "EG", "ES": "SV", "EK": "GQ", "ER": "ER", "EN": "EE",
    "ET": "ET", "FJ": "FJ", "FI": "FI", "FR": "FR", "GB": "GA", "GA": "GM",
    "GG": "GE", "GM": "DE", "GH": "GH", "GR": "GR", "GJ": "GD", "GT": "GT",
    "GV": "GN", "PU": "GW", "GY": "GY", "HA": "HT", "HO": "HN", "HU": "HU",
    "IC": "IS", "IN": "IN", "ID": "ID", "IR": "IR", "IZ": "IQ", "EI": "IE",
    "IS": "IL", "IT": "IT", "JM": "JM", "JA": "JP", "JO": "JO", "KZ": "KZ",
    "KE": "KE", "KR": "KI", "KN": "KP", "KS": "KR", "KU": "KW", "KG": "KG",
    "LA": "LA", "LG": "LV", "LE": "LB", "LT": "LS", "LI": "LR", "LY": "LY",
    "LS": "LI", "LH": "LT", "LU": "LU", "MK": "MG", "MI": "MW", "MY": "MY",
    "MV": "MV", "ML": "ML", "MT": "MT", "RM": "MH", "MR": "MR", "MP": "MU",
    "MX": "MX", "FM": "FM", "MD": "MD", "MN": "MC", "MG": "MN", "MJ": "ME",
    "MO": "MA", "MZ": "MZ", "WA": "NA", "NR": "NR", "NP": "NP", "NL": "NL",
    "NZ": "NZ", "NU": "NI", "NG": "NE", "NI": "NG", "NO": "NO", "MU": "OM",
    "PK": "PK", "PS": "PW", "PM": "PA", "PP": "PG", "PA": "PY", "PE": "PE",
    "RP": "PH", "PL": "PL", "PO": "PT", "QA": "QA", "RO": "RO", "RS": "RU",
    "RW": "RW", "SC": "KN", "ST": "LC", "VC": "VC", "WS": "WS", "SM": "SM",
    "TP": "ST", "SA": "SA", "SG": "SN", "RI": "RS", "SE": "SC", "SL": "SL",
    "SN": "SG", "LO": "SK", "SI": "SI", "BP": "SB", "SO": "SO", "SF": "ZA",
    "OD": "SS", "SP": "ES", "CE": "LK", "SU": "SD", "NS": "SR", "WZ": "SZ",
    "SW": "SE", "SZ": "CH", "SY": "SY", "TW": "TW", "TI": "TJ", "TZ": "TZ",
    "TH": "TH", "TT": "TL", "TO": "TG", "TN": "TO", "TD": "TT", "TS": "TN",
    "TU": "TR", "TX": "TM", "TV": "TV", "UG": "UG", "UP": "UA", "AE": "AE",
    "UK": "GB", "US": "US", "UY": "UY", "UZ": "UZ", "NH": "VU", "VE": "VE",
    "VM": "VN", "YM": "YE", "ZA": "ZM", "ZI": "ZW", "XK": "XK",
}

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
    def handle_data(self, d):
        self.result.append(d)
    def get_text(self):
        return ''.join(self.result).strip()

def strip_html(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_text()

def parse_advisory_level(text):
    """Extract level number from advisory text."""
    m = re.search(r'Level\s+(\d)', text)
    return int(m.group(1)) if m else None

def build_us_advisories():
    """Parse State Dept RSS feed."""
    print("Fetching US State Dept travel advisories...")
    url = "https://travel.state.gov/_res/rss/TAsTWs.xml"
    req = urllib.request.Request(url, headers={'User-Agent': 'tabiji.ai/1.0'})
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        xml_data = resp.read()
    
    root = ET.fromstring(xml_data)
    advisories = {}
    
    for item in root.findall('.//item'):
        title = item.findtext('title', '')
        link = item.findtext('link', '')
        pub_date = item.findtext('pubDate', '')
        description = item.findtext('description', '')
        
        # Extract country name and level from title
        # Format: "Japan - Level 1: Exercise Normal Precautions"
        m = re.match(r'^(.+?)\s*-\s*Level\s+(\d):\s*(.+)$', title)
        if not m:
            continue
        
        country_name = m.group(1).strip()
        level = int(m.group(2))
        level_text = m.group(3).strip()
        
        # Get FIPS code from categories
        fips_code = None
        for cat in item.findall('category'):
            if cat.get('domain') == 'Country-Tag':
                fips_code = cat.text
                break
        
        iso_code = FIPS_TO_ISO.get(fips_code, fips_code) if fips_code else None
        
        # Clean description
        summary = strip_html(description)[:500] if description else ""
        
        entry = {
            "country": country_name,
            "iso2": iso_code,
            "level": level,
            "levelText": level_text,
            "summary": summary,
            "url": link,
            "publishedDate": pub_date,
        }
        
        # Use ISO code as key if available, otherwise country name
        key = iso_code or country_name
        advisories[key] = entry
    
    output = {
        "version": "1.0.0",
        "source": "US Department of State",
        "lastFetched": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "count": len(advisories),
        "advisories": advisories
    }
    
    out_path = os.path.join(OUT_DIR, 'advisories-us.json')
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Built US advisories for {len(advisories)} countries → {out_path}")
    
    # Level distribution
    levels = {}
    for a in advisories.values():
        l = a['level']
        levels[l] = levels.get(l, 0) + 1
    for l in sorted(levels):
        print(f"   Level {l}: {levels[l]} countries")

def build_uk_advisories():
    """Fetch UK FCDO advisories via gov.uk API."""
    print("\nFetching UK FCDO travel advisories...")
    
    # First get the list of all countries with FCDO advice
    url = "https://www.gov.uk/api/content/foreign-travel-advice"
    req = urllib.request.Request(url, headers={'User-Agent': 'tabiji.ai/1.0'})
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    
    # FCDO country slug → ISO mapping (partial, for common countries)
    SLUG_TO_ISO = {
        "japan": "JP", "thailand": "TH", "mexico": "MX", "italy": "IT",
        "france": "FR", "spain": "ES", "portugal": "PT", "greece": "GR",
        "germany": "DE", "costa-rica": "CR", "colombia": "CO", "peru": "PE",
        "vietnam": "VN", "indonesia": "ID", "morocco": "MA", "turkey": "TR",
        "south-korea": "KR", "australia": "AU", "new-zealand": "NZ",
        "united-kingdom": "GB", "canada": "CA", "brazil": "BR", "india": "IN",
        "china": "CN", "egypt": "EG", "south-africa": "ZA", "argentina": "AR",
        "chile": "CL", "cuba": "CU", "iceland": "IS", "ireland": "IE",
        "nepal": "NP", "sri-lanka": "LK", "cambodia": "KH", "laos": "LA",
        "philippines": "PH", "singapore": "SG", "malaysia": "MY",
        "taiwan": "TW", "hong-kong": "HK", "israel": "IL", "jordan": "JO",
        "oman": "OM", "qatar": "QA", "uae": "AE", "saudi-arabia": "SA",
        "kenya": "KE", "tanzania": "TZ", "uganda": "UG", "ethiopia": "ET",
        "ghana": "GH", "nigeria": "NG", "senegal": "SN", "rwanda": "RW",
        "croatia": "HR", "czech-republic": "CZ", "poland": "PL",
        "hungary": "HU", "romania": "RO", "bulgaria": "BG", "austria": "AT",
        "switzerland": "CH", "netherlands": "NL", "belgium": "BE",
        "sweden": "SE", "norway": "NO", "finland": "FI", "denmark": "DK",
        "estonia": "EE", "latvia": "LV", "lithuania": "LT",
        "serbia": "RS", "montenegro": "ME", "albania": "AL",
        "north-macedonia": "MK", "slovenia": "SI", "slovakia": "SK",
        "malta": "MT", "cyprus": "CY", "luxembourg": "LU",
        "dominican-republic": "DO", "panama": "PA", "belize": "BZ",
        "guatemala": "GT", "honduras": "HN", "nicaragua": "NI",
        "el-salvador": "SV", "ecuador": "EC", "bolivia": "BO",
        "paraguay": "PY", "uruguay": "UY", "venezuela": "VE",
        "trinidad-and-tobago": "TT", "jamaica": "JM", "barbados": "BB",
        "fiji": "FJ", "maldives": "MV", "mauritius": "MU",
        "madagascar": "MG", "tunisia": "TN", "namibia": "NA",
        "botswana": "BW", "zimbabwe": "ZW", "zambia": "ZM",
        "mozambique": "MZ", "malawi": "MW",
        "russia": "RU", "ukraine": "UA", "georgia": "GE",
        "armenia": "AM", "azerbaijan": "AZ", "kazakhstan": "KZ",
        "uzbekistan": "UZ", "tajikistan": "TJ", "kyrgyzstan": "KG",
        "turkmenistan": "TM", "mongolia": "MN", "myanmar": "MM",
        "pakistan": "PK", "bangladesh": "BD", "iran": "IR", "iraq": "IQ",
        "lebanon": "LB", "syria": "SY", "afghanistan": "AF",
    }
    
    # Get country list from the links
    countries = data.get('links', {}).get('children', [])
    advisories = {}
    
    for c in countries:
        slug = c.get('base_path', '').replace('/foreign-travel-advice/', '')
        title = c.get('title', '')
        description = c.get('description', '')
        updated = c.get('public_updated_at', '')
        
        iso = SLUG_TO_ISO.get(slug)
        
        entry = {
            "country": title,
            "iso2": iso,
            "slug": slug,
            "summary": description[:500] if description else "",
            "lastUpdated": updated[:10] if updated else None,
            "url": f"https://www.gov.uk/foreign-travel-advice/{slug}"
        }
        
        key = iso or slug
        advisories[key] = entry
    
    output = {
        "version": "1.0.0",
        "source": "UK Foreign, Commonwealth & Development Office",
        "lastFetched": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "count": len(advisories),
        "advisories": advisories
    }
    
    out_path = os.path.join(OUT_DIR, 'advisories-uk.json')
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Built UK advisories for {len(advisories)} countries → {out_path}")
    mapped = sum(1 for a in advisories.values() if a.get('iso2'))
    print(f"   {mapped} mapped to ISO codes, {len(advisories) - mapped} unmapped")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    build_us_advisories()
    build_uk_advisories()

if __name__ == '__main__':
    main()
