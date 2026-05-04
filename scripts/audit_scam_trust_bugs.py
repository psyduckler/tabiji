#!/usr/bin/env python3
"""Audit trust-breaking issues on Tabiji scam pages.

Checks the concrete regressions found during the /scams/ audit:
- no broken city-specific OG image URLs in scam page metadata (use default fallback)
- no broken UAE health-guide links
- no Cloudflare email-protection exposure or source mailto links in scam pages
- no generated-copy artifacts like "the The" or "documents 10,"
- /scams/ hub inventory stats match the rendered city-card inventory
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"
HUB = SCAMS / "index.html"
DEFAULT_OG = "https://img.tabiji.ai/tabiji-owl-logo.png"

CITY_PAGE_EXCLUDE = {"country", "everywhere", "atlas"}


def _failures() -> list[str]:
    failures: list[str] = []
    scam_pages = [p for p in SCAMS.rglob("index.html") if p != HUB]

    # Broken OG fallback: city-specific scams-*-og.jpg assets are not reliably present in R2.
    for path in scam_pages + [HUB]:
        text = path.read_text(errors="ignore")
        if re.search(r'<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image)["\'][^>]+content=["\']https://img\.tabiji\.ai/scams-[^"\']+-og\.jpg', text):
            failures.append(f"{path.relative_to(REPO)} uses missing-prone scam-specific OG image instead of fallback")
        if re.search(r'"image"\s*:\s*"https://img\.tabiji\.ai/scams-[^"]+-og\.jpg"', text):
            failures.append(f"{path.relative_to(REPO)} JSON-LD uses missing-prone scam-specific OG image instead of fallback")

    # Broken link and Cloudflare email-obfuscation leak.
    for path in scam_pages + [HUB]:
        text = path.read_text(errors="ignore")
        rel = path.relative_to(REPO)
        if "/health/united-arab-emirates/" in text:
            failures.append(f"{rel} links to broken /health/united-arab-emirates/")
        if "/cdn-cgi/l/email-protection" in text:
            failures.append(f"{rel} exposes /cdn-cgi/l/email-protection")
        if "mailto:" in text:
            failures.append(f"{rel} contains mailto: link that Cloudflare can rewrite to /cdn-cgi/l/email-protection")

        # Generated-copy artifacts.
        if re.search(r"\bthe The\b", text):
            failures.append(f"{rel} contains duplicate article artifact 'the The'")
        if re.search(r"\bdocuments\s+10,", text, re.I):
            failures.append(f"{rel} contains malformed 'documents 10,' generated sentence")

    # Hub stat consistency: stats bar must match city-card inventory.
    soup = BeautifulSoup(HUB.read_text(errors="ignore"), "html.parser")
    city_cards = soup.select('a.city-card[href^="/scams/"]')
    card_hrefs = [a.get("href", "") for a in city_cards]
    city_cards = [a for a, href in zip(city_cards, card_hrefs) if not any(href.startswith(f"/scams/{x}/") for x in CITY_PAGE_EXCLUDE)]
    countries = {a.get("data-country", "").upper() for a in city_cards if a.get("data-country")}
    card_scam_total = 0
    for a in city_cards:
        count_el = a.select_one(".scam-count")
        if not count_el:
            failures.append(f"scams/index.html city card missing .scam-count for {a.get('href')}")
            continue
        m = re.search(r"(\d+)", count_el.get_text(" ", strip=True))
        if not m:
            failures.append(f"scams/index.html city card has unparsable scam count for {a.get('href')}")
            continue
        card_scam_total += int(m.group(1))

    stats = [int(s.get_text(strip=True).replace(",", "")) for s in soup.select(".stats-bar .stat strong") if s.get_text(strip=True).replace(",", "").isdigit()]
    if len(stats) < 3:
        failures.append("scams/index.html stats bar does not expose numeric scams/cities/countries stats")
    else:
        stat_scams, stat_cities, stat_countries = stats[:3]
        if stat_scams != card_scam_total:
            failures.append(f"scams/index.html scams stat {stat_scams} != rendered card total {card_scam_total}")
        if stat_cities != len(city_cards):
            failures.append(f"scams/index.html cities stat {stat_cities} != rendered city-card count {len(city_cards)}")
        if stat_countries != len(countries):
            failures.append(f"scams/index.html countries stat {stat_countries} != rendered country count {len(countries)}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        print("Scam trust-bug audit FAILED:")
        for f in failures:
            print(f" - {f}")
        return 1
    print("Scam trust-bug audit passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
