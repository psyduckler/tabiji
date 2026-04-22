#!/usr/bin/env python3
"""Audit and fix scam counts on every /scams/country/{code}/ hub page so they
match what the city pages actually have.

Per country hub, updates (if mismatched):
  - Meta description + og/twitter description totals
  - Hero subtitle "N scams documented from real Reddit traveler stories."
  - Hero stat pill <strong>N</strong> scams documented
  - Body intro paragraph's N-high-risk statement
  - Per-city `.city-card-count` "N scams documented"
  - Per-city `.city-risk-badge` 🔴 count (scams with data-risk="high" or
    class containing "high")

All 13 live-book country hubs are audited by default; pass --only <code>... to
restrict.

Usage:
    python3 scripts/book-cta-rollout/audit_country_hub_scam_counts.py --dry-run
    python3 scripts/book-cta-rollout/audit_country_hub_scam_counts.py
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCAMS = REPO / "scams"

CODES = {
    "japan": "jp", "italy": "it", "france": "fr", "indonesia": "id",
    "brazil": "br", "portugal": "pt", "canada": "ca", "united-kingdom": "gb",
    "vietnam": "vn", "germany": "de", "spain": "es", "greece": "gr",
    "thailand": "th",
}


def count_scams(html: str) -> int:
    ids = set(re.findall(r'id="scam-(\d+)"', html))
    if ids:
        return len(ids)
    return len(set(re.findall(r'>Scam\s*#(\d+)<', html)))


def count_high_risk(html: str) -> int:
    # Matches the danger-badge for "High" severity in city pages.
    # Example: <span class="danger-badge danger-high">🚨 High</span>
    return len(re.findall(r'class="[^"]*danger-high[^"]*"', html))


def audit_city(slug: str) -> tuple[int, int]:
    p = SCAMS / slug / "index.html"
    if not p.exists():
        return 0, 0
    html = p.read_text()
    return count_scams(html), count_high_risk(html)


def audit_country(name: str, code: str, write: bool) -> dict:
    hub = SCAMS / "country" / code / "index.html"
    if not hub.exists():
        return {"name": name, "code": code, "error": "no hub"}

    html = hub.read_text()
    original = html

    # Pull the schema.org hasPart city list (order + slugs)
    urls = re.findall(r'"url":"https://tabiji\.ai/scams/([a-z0-9-]+)/"', html)
    city_slugs: list[str] = []
    seen: set[str] = set()
    for u in urls:
        if u in (code, "country") or u in seen:
            continue
        seen.add(u)
        city_slugs.append(u)

    per_city: dict[str, dict] = {}
    total_scams = 0
    total_high = 0
    for slug in city_slugs:
        scams, high = audit_city(slug)
        per_city[slug] = {"scams": scams, "high": high}
        total_scams += scams
        total_high += high

    # --- Update per-city card counts ---
    # Pattern: each city card is an `<a href="/scams/<slug>/" class="city-card">…`
    # block up to the closing `</a>`. Inside that block we update:
    #   <span class="city-risk-badge" title="N high-risk scams">🔴 N high</span>
    #   <div class="city-card-count">N scams documented</div>
    changes = []

    def _patch_city_block(m: re.Match, slug: str, expected_scams: int, expected_high: int) -> str:
        block = m.group(0)
        new = block
        # risk-badge
        def _rb(match):
            return f'<span class="city-risk-badge" title="{expected_high} high-risk scams">🔴 {expected_high} high</span>'
        new = re.sub(
            r'<span class="city-risk-badge"[^>]*>🔴\s*\d+\s*high</span>',
            _rb, new, count=1,
        )
        # card count
        new = re.sub(
            r'<div class="city-card-count">\d+\s*scams?\s*documented</div>',
            f'<div class="city-card-count">{expected_scams} scams documented</div>',
            new, count=1,
        )
        return new

    for slug, data in per_city.items():
        pattern = re.compile(
            rf'<a href="/scams/{re.escape(slug)}/"\s+class="city-card">.*?</a>',
            re.DOTALL,
        )
        m = pattern.search(html)
        if not m:
            continue
        new_block = _patch_city_block(m, slug, data["scams"], data["high"])
        if new_block != m.group(0):
            changes.append(f"{slug}: → {data['scams']} scams, {data['high']} high")
            html = html[:m.start()] + new_block + html[m.end():]

    # --- Update country-level totals ---
    # 1. Meta description: "N scams documented from real Reddit..."
    html, n1 = re.subn(
        r'(Tourist scam guides for \d+ cities in [^.]+\.\s+)(\d+)(\s+scams documented)',
        lambda m: f"{m.group(1)}{total_scams}{m.group(3)}",
        html,
    )
    # 2. og:description + twitter:description: "N scams documented across ..."
    html, n2 = re.subn(
        r'(")(\d+)(\s+scams\s+documented across)',
        lambda m: f"{m.group(1)}{total_scams}{m.group(3)}",
        html,
    )
    # 3. twitter short form: "N scams across N cities."
    html, n3 = re.subn(
        r'("[^"]*")(\d+)(\s+scams across \d+ cities\. Reddit-sourced\.")',
        # Careful: re.subn receives the whole match via group 0. Use a simpler pattern:
        lambda m: m.group(0),
        html,
    )
    # Simpler: twitter short form
    html, _ = re.subn(
        r'(\d+)(\s+scams across \d+ cities\. Reddit-sourced\.)',
        lambda m: f"{total_scams}{m.group(2)}",
        html,
    )
    # 4. H1 hero "Tourist Scams in <Country>" — usually contains total in section-sub <p>
    # Body paragraph: "Scam guides for N cities in <Country>, sourced from real Reddit traveler reports. N scams across <Country> are rated high risk."
    html, _ = re.subn(
        r'(\d+)(\s+scams across\s+[A-Z][^.]*?\s+are rated high risk\.)',
        lambda m: f"{total_high}{m.group(2)}",
        html,
    )
    # 5. Hero stat pill "<strong>N</strong> scams documented"
    html, _ = re.subn(
        r'<strong>\d+</strong>(\s+scams documented)',
        lambda m: f"<strong>{total_scams}</strong>{m.group(1)}",
        html,
    )

    touched = html != original
    if write and touched:
        hub.write_text(html)

    return {
        "name": name,
        "code": code,
        "cities": len(city_slugs),
        "total_scams": total_scams,
        "total_high": total_high,
        "per_city_changes": changes,
        "touched": touched,
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args(argv)

    write = not args.dry_run
    only = set(args.only) if args.only else None
    tag = "[dry]" if args.dry_run else "[write]"

    for name, code in CODES.items():
        if only and code not in only and name not in only:
            continue
        res = audit_country(name, code, write)
        if res.get("error"):
            print(f"{tag} {name:16} {code:3}  ERROR: {res['error']}")
            continue
        marker = "✓" if res["touched"] else " "
        print(f"{tag} {name:16} {code:3}  {marker}  "
              f"total_scams={res['total_scams']}  "
              f"total_high={res['total_high']}  "
              f"cities={res['cities']}  "
              f"per_city_fixes={len(res['per_city_changes'])}")
        for c in res["per_city_changes"]:
            print(f"             {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
