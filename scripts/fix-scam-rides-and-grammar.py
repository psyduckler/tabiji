#!/usr/bin/env python3
"""
Fix two issues across all scam city pages:

1. "is the The " grammar bug  -- double article in takeaways/JSON-LD/FAQ
   Replace "is the The " with "is the " everywhere.

2. Generic ride-service advice -- replace the one-size-fits-all
   "(Uber, Grab, Bolt)" line with region-appropriate alternatives
   based on the addressCountry code embedded in each page.
"""

import glob
import os
import re
import sys

SCAMS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scams")

# ── Region mapping: ISO-3166-1 alpha-2 codes ──────────────────────────

SOUTHEAST_ASIA = {"th", "vn", "kh", "la", "my", "id", "ph", "sg", "mm"}
EAST_ASIA = {"jp", "kr", "tw", "cn", "hk", "mo"}  # hk=Hong Kong SAR, mo=Macau SAR
SOUTH_ASIA = {"in", "np", "lk", "bd"}
EUROPE = {
    "gb", "fr", "de", "it", "es", "pt", "nl", "be", "at", "ch", "ie", "se",
    "dk", "no", "fi", "is", "gr", "tr", "pl", "cz", "sk", "hu", "ro", "bg",
    "hr", "si", "rs", "ba", "me", "al", "mk", "xk", "lt", "lv", "ee",
    "ua", "ru", "ge", "am", "az", "mc", "mt", "cy", "lu", "li", "ad", "sm",
    "va",
    "kz", "uz",  # Central Asia -- Bolt/Yandex operate here; closest to Europe mapping
}
NORTH_AMERICA = {"us", "ca", "pr"}
LATIN_AMERICA_CARIBBEAN = {
    "mx", "gt", "bz", "sv", "hn", "ni", "cr", "pa",
    "co", "ve", "ec", "pe", "bo", "cl", "ar", "uy", "py", "br", "gy", "sr",
    "jm", "ht", "do", "tt", "bb", "lc", "ag", "bs", "ky", "tc", "cw",
    "gd", "dm", "kn", "vc",
}
MIDDLE_EAST = {"ae", "qa", "jo", "il", "sa", "om", "lb", "bh", "kw", "iq", "ye"}
AFRICA = {
    "za", "ke", "tz", "eg", "ma", "ng", "gh", "sn", "et", "ug", "rw",
    "zm", "mz", "na", "tn", "dj", "sc", "mu", "mg", "cm", "ci",
    "bw", "zw", "mw", "ao", "cd", "cg", "ga", "ne",
}
OCEANIA = {"au", "nz", "fj", "pf"}  # pf = French Polynesia (Bora Bora)
# Also handle Maldives (mv) as South Asia-adjacent; map to Oceania style
OCEANIA.add("mv")

CUBA = {"cu"}

# ── Replacement lines ─────────────────────────────────────────────────

GENERIC_LINE = "<li>Use app-based ride services (Uber, Grab, Bolt) instead of street taxis</li>"

REPLACEMENTS = {
    "southeast_asia": "<li>Use app-based ride services (Grab, Gojek) instead of street taxis \u2014 always confirm the fare before departure</li>",
    "east_asia": "<li>Use app-based ride services or official metered taxis \u2014 avoid unmarked vehicles near tourist areas</li>",
    "south_asia": "<li>Use app-based ride services (Uber, Ola) instead of street taxis \u2014 always confirm the fare before departure</li>",
    "europe": "<li>Use app-based ride services (Uber, Bolt) or official metered taxis instead of unmarked vehicles</li>",
    "north_america": "<li>Use app-based ride services (Uber, Lyft) instead of unmarked vehicles or unlicensed cabs</li>",
    "latin_america_caribbean": "<li>Use app-based ride services (Uber, DiDi) instead of street taxis \u2014 avoid unmarked vehicles, especially at night</li>",
    "middle_east": "<li>Use app-based ride services (Uber, Careem) or official metered taxis instead of unmarked vehicles</li>",
    "africa": "<li>Use app-based ride services (Uber, Bolt) instead of unmarked taxis \u2014 always confirm the fare before departure</li>",
    "oceania": "<li>Use app-based ride services (Uber) or official metered taxis instead of unmarked vehicles</li>",
    "cuba": "<li>Negotiate taxi fares before departure and use official yellow taxis or your hotel\u2019s recommended transport</li>",
}


def get_region(country_code: str):
    cc = country_code.lower().strip()
    if cc in CUBA:
        return "cuba"
    if cc in SOUTHEAST_ASIA:
        return "southeast_asia"
    if cc in EAST_ASIA:
        return "east_asia"
    if cc in SOUTH_ASIA:
        return "south_asia"
    if cc in EUROPE:
        return "europe"
    if cc in NORTH_AMERICA:
        return "north_america"
    if cc in LATIN_AMERICA_CARIBBEAN:
        return "latin_america_caribbean"
    if cc in MIDDLE_EAST:
        return "middle_east"
    if cc in AFRICA:
        return "africa"
    if cc in OCEANIA:
        return "oceania"
    return None


def extract_country_code(html: str) -> str:
    """Pull the addressCountry value from the JSON-LD block."""
    m = re.search(r'"addressCountry"\s*:\s*"([a-zA-Z]{2})"', html)
    return m.group(1).lower() if m else ""


def fix_file(filepath: str) -> dict:
    """Fix a single scam page. Returns stats dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    content = original
    stats = {"grammar_fixes": 0, "ride_fixes": 0, "country_code": "", "region": ""}

    # ── Issue 1: "is the The " grammar bug ──
    count = content.count("is the The ")
    if count > 0:
        content = content.replace("is the The ", "is the ")
        stats["grammar_fixes"] = count

    # Also check HTML-entity variant "is the The&" (e.g., The&amp;)
    count2 = content.count("is the The&")
    if count2 > 0:
        content = content.replace("is the The&", "is the &")
        stats["grammar_fixes"] += count2

    # ── Issue 2: Generic ride-service advice ──
    cc = extract_country_code(content)
    stats["country_code"] = cc
    if GENERIC_LINE in content and cc:
        region = get_region(cc)
        stats["region"] = region or "UNKNOWN"
        if region and region in REPLACEMENTS:
            content = content.replace(GENERIC_LINE, REPLACEMENTS[region])
            stats["ride_fixes"] = 1
        else:
            print(f"  WARNING: No region mapping for country code '{cc}' in {filepath}")

    # Write back only if changed
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return stats


def main():
    pattern = os.path.join(SCAMS_DIR, "*/index.html")
    files = sorted(glob.glob(pattern))

    # Exclude country/ hub pages — only city pages
    files = [f for f in files if "/country/" not in f]

    print(f"Found {len(files)} scam city pages\n")

    grammar_total = 0
    grammar_pages = 0
    ride_total = 0
    ride_pages = 0
    unmapped = []

    for filepath in files:
        city_slug = os.path.basename(os.path.dirname(filepath))
        stats = fix_file(filepath)

        if stats["grammar_fixes"] > 0:
            grammar_total += stats["grammar_fixes"]
            grammar_pages += 1
            print(f"  [grammar] {city_slug}: fixed {stats['grammar_fixes']} 'is the The' occurrence(s)")

        if stats["ride_fixes"] > 0:
            ride_total += stats["ride_fixes"]
            ride_pages += 1

        if stats["region"] == "UNKNOWN":
            unmapped.append((city_slug, stats["country_code"]))

    print(f"\n{'='*60}")
    print(f"ISSUE 1 - Grammar ('is the The')")
    print(f"  Pages fixed: {grammar_pages}")
    print(f"  Total replacements: {grammar_total}")
    print(f"\nISSUE 2 - Region-appropriate ride advice")
    print(f"  Pages fixed: {ride_pages}")
    print(f"  Total replacements: {ride_total}")

    if unmapped:
        print(f"\nWARNING: {len(unmapped)} pages with unmapped country codes:")
        for slug, cc in unmapped:
            print(f"  {slug} -> {cc}")

    print(f"\nDone.")


if __name__ == "__main__":
    main()
