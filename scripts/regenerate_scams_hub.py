#!/usr/bin/env python3
"""Regenerate the 3 data-driven sections of scams/index.html from corpus:
stats-bar, country-filter, and city-grid.

Scans scams/<slug>/index.html for every slug that has a live page, extracts
(city, country_code, country_name, scam_count, tagline) by parsing the page's
own <h1>, schema.org Place, and .scam-title elements. Preserves the flag
emoji from the current hub card when available (authoritative source), falls
back to a country→flag mapping for cities not yet in the hub.

Preserves everything outside the 3 sections (nav, hero, search, footer).

Usage:
    python3 scripts/regenerate_scams_hub.py           # rewrite scams/index.html
    python3 scripts/regenerate_scams_hub.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"
HUB = SCAMS / "index.html"

_H1_RE = re.compile(r"^\d+\s+Tourist Scams in\s+(.+?)$")

# Country-code → (full name, flag emoji). Covers the 60 current country hubs
# plus a few extras. If a city's schema.org addressCountry isn't in this map,
# the card falls back to "?" name and 🌍 flag — prompt to add here.
COUNTRY_META: dict[str, tuple[str, str]] = {
    "AE": ("United Arab Emirates", "🇦🇪"), "AG": ("Antigua and Barbuda", "🇦🇬"),
    "AL": ("Albania", "🇦🇱"), "AM": ("Armenia", "🇦🇲"),
    "AR": ("Argentina", "🇦🇷"), "AT": ("Austria", "🇦🇹"),
    "AW": ("Aruba", "🇦🇼"),
    "AU": ("Australia", "🇦🇺"), "AZ": ("Azerbaijan", "🇦🇿"),
    "BA": ("Bosnia and Herzegovina", "🇧🇦"), "BB": ("Barbados", "🇧🇧"),
    "BD": ("Bangladesh", "🇧🇩"), "BE": ("Belgium", "🇧🇪"),
    "BG": ("Bulgaria", "🇧🇬"), "BH": ("Bahrain", "🇧🇭"),
    "BM": ("Bermuda", "🇧🇲"), "BO": ("Bolivia", "🇧🇴"),
    "BR": ("Brazil", "🇧🇷"), "BS": ("Bahamas", "🇧🇸"),
    "BT": ("Bhutan", "🇧🇹"), "BZ": ("Belize", "🇧🇿"),
    "CA": ("Canada", "🇨🇦"), "CH": ("Switzerland", "🇨🇭"),
    "CI": ("Ivory Coast", "🇨🇮"), "CL": ("Chile", "🇨🇱"),
    "CN": ("China", "🇨🇳"), "CO": ("Colombia", "🇨🇴"),
    "CR": ("Costa Rica", "🇨🇷"), "CU": ("Cuba", "🇨🇺"),
    "CW": ("Curaçao", "🇨🇼"), "CY": ("Cyprus", "🇨🇾"),
    "CZ": ("Czech Republic", "🇨🇿"), "DE": ("Germany", "🇩🇪"),
    "DK": ("Denmark", "🇩🇰"), "DO": ("Dominican Republic", "🇩🇴"),
    "EC": ("Ecuador", "🇪🇨"), "EE": ("Estonia", "🇪🇪"),
    "EG": ("Egypt", "🇪🇬"), "ES": ("Spain", "🇪🇸"),
    "ET": ("Ethiopia", "🇪🇹"), "FI": ("Finland", "🇫🇮"),
    "FJ": ("Fiji", "🇫🇯"), "FR": ("France", "🇫🇷"),
    "GB": ("United Kingdom", "🇬🇧"), "GE": ("Georgia", "🇬🇪"),
    "GH": ("Ghana", "🇬🇭"), "GR": ("Greece", "🇬🇷"),
    "GT": ("Guatemala", "🇬🇹"), "HK": ("Hong Kong", "🇭🇰"),
    "HN": ("Honduras", "🇭🇳"), "HR": ("Croatia", "🇭🇷"),
    "HT": ("Haiti", "🇭🇹"), "HU": ("Hungary", "🇭🇺"),
    "ID": ("Indonesia", "🇮🇩"), "IE": ("Ireland", "🇮🇪"),
    "IL": ("Israel", "🇮🇱"), "IN": ("India", "🇮🇳"),
    "IR": ("Iran", "🇮🇷"), "IS": ("Iceland", "🇮🇸"),
    "IT": ("Italy", "🇮🇹"), "JM": ("Jamaica", "🇯🇲"),
    "JO": ("Jordan", "🇯🇴"), "JP": ("Japan", "🇯🇵"),
    "KE": ("Kenya", "🇰🇪"), "KG": ("Kyrgyzstan", "🇰🇬"),
    "KH": ("Cambodia", "🇰🇭"), "KN": ("Saint Kitts and Nevis", "🇰🇳"),
    "KR": ("South Korea", "🇰🇷"), "KW": ("Kuwait", "🇰🇼"),
    "KY": ("Cayman Islands", "🇰🇾"), "KZ": ("Kazakhstan", "🇰🇿"),
    "LA": ("Laos", "🇱🇦"), "LB": ("Lebanon", "🇱🇧"),
    "LC": ("Saint Lucia", "🇱🇨"), "LK": ("Sri Lanka", "🇱🇰"),
    "LT": ("Lithuania", "🇱🇹"), "LV": ("Latvia", "🇱🇻"),
    "MA": ("Morocco", "🇲🇦"), "MC": ("Monaco", "🇲🇨"),
    "ME": ("Montenegro", "🇲🇪"), "MG": ("Madagascar", "🇲🇬"),
    "MK": ("North Macedonia", "🇲🇰"), "MM": ("Myanmar", "🇲🇲"),
    "MN": ("Mongolia", "🇲🇳"), "MO": ("Macau", "🇲🇴"),
    "MT": ("Malta", "🇲🇹"), "MU": ("Mauritius", "🇲🇺"),
    "MV": ("Maldives", "🇲🇻"), "MX": ("Mexico", "🇲🇽"),
    "MY": ("Malaysia", "🇲🇾"), "MZ": ("Mozambique", "🇲🇿"),
    "NA": ("Namibia", "🇳🇦"), "NC": ("New Caledonia", "🇳🇨"),
    "NG": ("Nigeria", "🇳🇬"), "NI": ("Nicaragua", "🇳🇮"),
    "NL": ("Netherlands", "🇳🇱"), "NO": ("Norway", "🇳🇴"),
    "NP": ("Nepal", "🇳🇵"), "NZ": ("New Zealand", "🇳🇿"),
    "OM": ("Oman", "🇴🇲"), "PA": ("Panama", "🇵🇦"),
    "PE": ("Peru", "🇵🇪"), "PF": ("French Polynesia", "🇵🇫"),
    "PH": ("Philippines", "🇵🇭"), "PK": ("Pakistan", "🇵🇰"),
    "PL": ("Poland", "🇵🇱"), "PR": ("Puerto Rico", "🇵🇷"),
    "PT": ("Portugal", "🇵🇹"), "PY": ("Paraguay", "🇵🇾"),
    "QA": ("Qatar", "🇶🇦"), "RO": ("Romania", "🇷🇴"),
    "RS": ("Serbia", "🇷🇸"), "RU": ("Russia", "🇷🇺"),
    "RW": ("Rwanda", "🇷🇼"), "SA": ("Saudi Arabia", "🇸🇦"),
    "SC": ("Seychelles", "🇸🇨"), "SE": ("Sweden", "🇸🇪"),
    "SG": ("Singapore", "🇸🇬"), "SI": ("Slovenia", "🇸🇮"),
    "SK": ("Slovakia", "🇸🇰"), "SN": ("Senegal", "🇸🇳"),
    "SR": ("Suriname", "🇸🇷"), "SV": ("El Salvador", "🇸🇻"),
    "SX": ("Sint Maarten", "🇸🇽"),
    "TC": ("Turks and Caicos", "🇹🇨"), "TH": ("Thailand", "🇹🇭"),
    "TN": ("Tunisia", "🇹🇳"), "TR": ("Turkey", "🇹🇷"),
    "TT": ("Trinidad and Tobago", "🇹🇹"), "TW": ("Taiwan", "🇹🇼"),
    "TZ": ("Tanzania", "🇹🇿"), "UA": ("Ukraine", "🇺🇦"),
    "UG": ("Uganda", "🇺🇬"), "US": ("United States", "🇺🇸"),
    "UY": ("Uruguay", "🇺🇾"), "UZ": ("Uzbekistan", "🇺🇿"),
    "VN": ("Vietnam", "🇻🇳"), "VU": ("Vanuatu", "🇻🇺"),
    "ZA": ("South Africa", "🇿🇦"), "ZM": ("Zambia", "🇿🇲"),
    "ZW": ("Zimbabwe", "🇿🇼"),
}


def _existing_hub_country_codes(hub_src: str) -> dict[str, str]:
    """Map slug → country code from the existing hub's `data-country` attribute.

    Used as a fallback for legacy city pages that don't emit schema.org Place.
    """
    out: dict[str, str] = {}
    soup = BeautifulSoup(hub_src, "html.parser")
    for a in soup.select("a.city-card"):
        href = a.get("href", "")
        m = re.match(r"/scams/([^/]+)/$", href)
        if m and a.get("data-country"):
            out[m.group(1)] = a["data-country"].upper()
    return out


def _scan_city_page(path: Path) -> dict | None:
    """Parse one scams/<slug>/index.html for the metadata the hub needs."""
    try:
        soup = BeautifulSoup(path.read_text(), "html.parser")
    except Exception:
        return None
    h1 = soup.select_one("h1")
    if not h1:
        return None
    # Editorial-v2 wraps city in <em>, which collapses into "inCity" under
    # default strip — force a separator so "7 Tourist Scams in Palermo" stays joined.
    m = _H1_RE.match(re.sub(r"\s+", " ", h1.get_text(" ", strip=True)))
    if not m:
        return None
    city_name = m.group(1).strip()
    scam_count = len(soup.select(".scam-card"))
    if scam_count == 0:
        return None
    country_code = ""
    for sc in soup.select('script[type="application/ld+json"]'):
        try:
            ld = json.loads(sc.string or "{}")
        except Exception:
            continue
        graph = ld.get("@graph", [ld]) if isinstance(ld, dict) else []
        for g in graph:
            if g.get("@type") == "Place":
                country_code = (g.get("address", {}) or {}).get("addressCountry", "")
                break
        if country_code:
            break
    names = [t.get_text(strip=True) for t in soup.select(".scam-title")][:3]
    tagline = ", ".join(names) + (", and more" if scam_count > 3 else ".")
    return {
        "slug": path.parent.name,
        "city": city_name,
        "country_code": country_code.upper(),
        "scam_count": scam_count,
        "tagline": tagline,
    }


def _flag_preservation(hub_src: str) -> dict[str, str]:
    """Map slug → flag emoji from the existing hub (authoritative for legacy pages)."""
    flags: dict[str, str] = {}
    soup = BeautifulSoup(hub_src, "html.parser")
    for a in soup.select("a.city-card"):
        href = a.get("href", "")
        m = re.match(r"/scams/([^/]+)/$", href)
        if not m:
            continue
        flag_el = a.select_one(".flag")
        if flag_el:
            flags[m.group(1)] = flag_el.get_text(strip=True)
    return flags


def _render_card(entry: dict, country_name: str, flag: str) -> str:
    tagline_esc = entry["tagline"].replace("'", "&#39;")
    city_data_attr = f'{entry["city"].lower()} {country_name.lower()}'
    return (
        f'        <a href="/scams/{entry["slug"]}/" class="city-card" '
        f'data-city="{city_data_attr}" data-country="{entry["country_code"]}">\n'
        f'            <div class="flag">{flag}</div>\n'
        f'            <div class="city-name">{entry["city"]}</div>\n'
        f'            <div class="city-country">{country_name}</div>\n'
        f'            <div class="scam-count">{entry["scam_count"]} scams documented</div>\n'
        f'            <div class="city-tagline">{tagline_esc}</div>\n'
        f'            <div class="card-date" style="font-size:0.72rem;color:#9ca3af;margin-top:0.4rem;">Updated Apr 2026</div>\n'
        f'            <div class="arrow">Read the guide →</div>\n'
        f'        </a>'
    )


def _render_filter_pills(country_counts: Counter) -> str:
    lines = ['<div class="country-filter">',
             '    <button class="filter-pill active" data-filter="all">All</button>']
    # Hub convention: top countries by city count only (current hub shows 24 pills).
    for cc, n in country_counts.most_common(24):
        if cc not in COUNTRY_META:
            continue
        name, flag = COUNTRY_META[cc]
        # UK display label matches current hub ("UK" not "United Kingdom")
        label = "UK" if cc == "GB" else ("USA" if cc == "US" else name)
        lines.append(
            f'        <a class="filter-pill" data-filter="{cc}" '
            f'href="/scams/country/{cc.lower()}/">{flag} {label} ({n})</a>'
        )
    lines.append("    </div>")
    return "\n".join(lines)


def _render_stats_bar(total_cities: int, total_scams: int, total_countries: int) -> str:
    return (
        '<div class="stats-bar">\n'
        f'    <div class="stat"><strong>{total_scams:,}</strong>Scams Documented</div>\n'
        f'    <div class="stat"><strong>{total_cities}</strong>Cities Covered</div>\n'
        f'    <div class="stat"><strong>{total_countries}</strong>Countries</div>\n'
        '    <div class="stat"><strong>Reddit</strong>Sourced &amp; Verified</div>\n'
        "</div>"
    )


def regenerate_hub(dry_run: bool = False) -> tuple[int, int, int]:
    entries = sorted(
        (e for e in (_scan_city_page(p / "index.html")
                     for p in sorted(SCAMS.iterdir()) if p.is_dir() and p.name != "country")
         if e is not None),
        key=lambda e: e["city"].lower(),
    )
    hub_src = HUB.read_text()
    flag_map = _flag_preservation(hub_src)
    legacy_cc_map = _existing_hub_country_codes(hub_src)

    cards = []
    country_counts: Counter[str] = Counter()
    for entry in entries:
        cc = entry["country_code"] or legacy_cc_map.get(entry["slug"], "")
        entry["country_code"] = cc
        if cc not in COUNTRY_META:
            print(f"  [warn] {entry['slug']}: unknown country code {cc!r} — add to COUNTRY_META", file=sys.stderr)
            name, flag = "Unknown", "🌍"
        else:
            name, flag = COUNTRY_META[cc]
        flag = flag_map.get(entry["slug"], flag)  # preserve existing flag if set
        cards.append(_render_card(entry, name, flag))
        country_counts[cc] += 1

    total_cities = len(entries)
    total_scams = sum(e["scam_count"] for e in entries)
    total_countries = len(country_counts)

    # Splice in three blocks.
    # 1. stats-bar
    new_stats = _render_stats_bar(total_cities, total_scams, total_countries)
    hub_src = re.sub(
        r'<div class="stats-bar">.+?</div>\s*(?=\n\s*<div class="search-section)',
        new_stats + "\n\n",
        hub_src,
        count=1,
        flags=re.DOTALL,
    )

    # 2. country-filter
    new_filter = _render_filter_pills(country_counts)
    hub_src = re.sub(
        r'<div class="country-filter">.+?</div>\s*(?=\s*<div id="country-link")',
        new_filter + "\n    ",
        hub_src,
        count=1,
        flags=re.DOTALL,
    )

    # 3. city-grid (preserve wrapper + label; replace only inner <a> children)
    grid_block = "\n\n" + "\n".join(cards) + "\n\n    "
    hub_src = re.sub(
        r'(<div class="city-grid" id="city-grid">)(.*?)(</div>\s*</div>)',
        lambda m: m.group(1) + grid_block + m.group(3),
        hub_src,
        count=1,
        flags=re.DOTALL,
    )

    # 4. JSON-LD numberOfItems (both CollectionPage and ItemList)
    hub_src = re.sub(r'"numberOfItems":\s*\d+', f'"numberOfItems": {total_cities}', hub_src)

    # 5. meta descriptions that mention "N+ cities"
    hub_src = re.sub(r'\b\d{3,4}\+ cities', f"{total_cities}+ cities", hub_src)
    hub_src = re.sub(r'\b\d{3,4}\+ destinations', f"{total_cities}+ destinations", hub_src)

    if dry_run:
        print(f"DRY RUN — would write {len(hub_src):,} bytes to {HUB}")
    else:
        HUB.write_text(hub_src)
        print(f"Wrote {len(hub_src):,} bytes to {HUB}")
    print(f"  {total_cities} cities · {total_scams:,} scams · {total_countries} countries")
    return total_cities, total_scams, total_countries


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    regenerate_hub(dry_run=args.dry_run)
