#!/usr/bin/env python3
"""
Build tiered keep/drop list from compare-all-search-volumes.csv.

Tier 1 (flagship):     total_vol >= 2000   — heavy content investment
Tier 2 (solid):        500 <= vol < 2000   — solid pages, moderate upkeep
Tier 3 (maintain):     100 <= vol < 500    — keep alive, light upkeep
Drop  (delete):        vol < 100           — consider removing

Also tags likely non-travel (sports/politics) pairs where both halves
are major sporting nations and no city qualifier is present.
"""

import csv
import os

ROOT = "/Users/bjh/Documents/tabiji/.claude/worktrees/happy-tharp-5601b2"
ANALYSIS = os.path.join(ROOT, "scripts", "compare-analysis")
INPUT_CSV = os.path.join(ANALYSIS, "compare-all-search-volumes.csv")
OUTPUT_CSV = os.path.join(ANALYSIS, "compare-tiers.csv")
SUMMARY_MD = os.path.join(ANALYSIS, "compare-tiers-summary.md")

# Country-vs-country pairs where cricket/football dominates the SERP.
# If both sides are in this set, the volume is likely sports-inflated.
# Includes FIFA national teams (nearly every country), cricket nations,
# US states (college football), and Canadian provinces.
SPORTS_HEAVY_COUNTRIES = {
    # Cricket
    "england", "india", "pakistan", "australia", "bangladesh", "sri-lanka",
    "new-zealand", "south-africa", "west-indies", "ireland", "scotland",
    "afghanistan", "zimbabwe", "nepal",
    # Football (FIFA) — basically every country plays international matches
    "brazil", "argentina", "portugal", "spain", "france", "germany", "italy",
    "netherlands", "belgium", "uruguay", "colombia", "mexico", "usa",
    "united-states", "japan", "south-korea", "morocco", "senegal", "ghana",
    "nigeria", "cameroon", "tunisia", "egypt", "algeria", "ecuador",
    "costa-rica", "chile", "paraguay", "peru", "bolivia", "venezuela",
    "denmark", "sweden", "norway", "finland", "poland", "czech-republic",
    "slovakia", "hungary", "romania", "bulgaria", "greece", "albania",
    "kosovo", "north-macedonia", "montenegro", "bosnia", "croatia", "serbia",
    "slovenia", "estonia", "latvia", "lithuania", "iceland", "faroe-islands",
    "switzerland", "austria", "turkey", "iran", "iraq", "saudi-arabia",
    "qatar", "uae", "bahrain", "kuwait", "oman", "yemen", "syria", "lebanon",
    "jordan", "israel", "palestine", "panama", "honduras", "guatemala",
    "el-salvador", "nicaragua", "jamaica", "haiti", "dominican-republic",
    "cuba", "trinidad-and-tobago", "barbados", "bahamas",
    "azerbaijan", "armenia", "georgia", "kazakhstan", "uzbekistan",
    "turkmenistan", "kyrgyzstan", "tajikistan", "belarus", "ukraine",
    "russia", "moldova", "luxembourg", "liechtenstein", "andorra", "malta",
    "cyprus", "gibraltar", "san-marino",
    "thailand", "vietnam", "indonesia", "philippines", "malaysia", "singapore",
    "china", "hong-kong", "taiwan", "mongolia", "north-korea",
    "kenya", "uganda", "tanzania", "rwanda", "ethiopia", "somalia", "sudan",
    "south-sudan", "dr-congo", "angola", "zambia", "mozambique", "namibia",
    "botswana", "zimbabwe", "madagascar", "mauritius", "seychelles",
    "cape-verde", "gambia", "guinea", "mali", "burkina-faso", "ivory-coast",
    "liberia", "sierra-leone", "togo", "benin", "gabon", "congo",
    "equatorial-guinea", "libya",
    # US states (college football, SEC rivalries)
    "georgia", "texas", "florida", "alabama", "tennessee", "oklahoma",
    "california", "arkansas", "louisiana", "mississippi", "kentucky",
    "south-carolina", "north-carolina", "virginia", "ohio", "michigan",
    # Canadian provinces — minor sports noise
}

# City pairs that are actually football-club SERPs. If both are in this set
# (or one is in this set and the other is a major football city), volume is
# sports-inflated.
FOOTBALL_CLUB_CITIES = {
    "barcelona", "madrid", "valencia", "sevilla", "mallorca", "athletic",
    "villarreal", "real-sociedad", "atletico", "real-madrid",
    "liverpool", "manchester", "arsenal", "chelsea", "tottenham", "everton",
    "leicester", "newcastle", "leeds", "aston-villa", "west-ham", "fulham",
    "wolves", "nottingham", "brighton", "southampton",
    "milan", "inter", "juventus", "roma", "napoli", "lazio", "fiorentina",
    "torino", "atalanta",
    "bayern", "dortmund", "leipzig", "frankfurt", "leverkusen", "schalke",
    "psg", "marseille", "lyon", "monaco", "lille", "nice",
    "porto", "benfica", "sporting", "ajax", "psv", "feyenoord",
    "glasgow", "celtic", "rangers",
}


def likely_sports(slug):
    parts = slug.split("-vs-")
    if len(parts) != 2:
        return False
    a, b = parts
    if a in SPORTS_HEAVY_COUNTRIES and b in SPORTS_HEAVY_COUNTRIES:
        return True
    if a in FOOTBALL_CLUB_CITIES and b in FOOTBALL_CLUB_CITIES:
        return True
    # One football club + another football-named place
    if (a in FOOTBALL_CLUB_CITIES and b in SPORTS_HEAVY_COUNTRIES) or (
        b in FOOTBALL_CLUB_CITIES and a in SPORTS_HEAVY_COUNTRIES
    ):
        return True
    return False


def tier_of(vol):
    if vol >= 2000:
        return 1
    if vol >= 500:
        return 2
    if vol >= 100:
        return 3
    return 0


def main():
    with open(INPUT_CSV) as f:
        rows = list(csv.DictReader(f))

    for r in rows:
        r["total_vol"] = int(r["total_vol"])
        r["vol_1"] = int(r["vol_1"])
        r["vol_2"] = int(r["vol_2"])
        r["best_vol"] = int(r["best_vol"])
        r["tier"] = tier_of(r["total_vol"])
        r["likely_sports"] = "yes" if likely_sports(r["slug"]) else ""

    rows.sort(key=lambda r: (-r["total_vol"], r["slug"]))

    fieldnames = [
        "tier", "total_vol", "best_vol", "best_keyword", "slug", "url",
        "vol_1", "vol_2", "keyword_1", "keyword_2", "likely_sports",
    ]
    with open(OUTPUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fieldnames})
    print(f"Wrote {OUTPUT_CSV} ({len(rows)} rows)")

    # Build markdown summary
    from collections import Counter
    tc = Counter(r["tier"] for r in rows)
    sports_flag = sum(1 for r in rows if r["likely_sports"])

    t1 = [r for r in rows if r["tier"] == 1]
    t2 = [r for r in rows if r["tier"] == 2]
    t3 = [r for r in rows if r["tier"] == 3]
    drop = [r for r in rows if r["tier"] == 0]

    t1_travel = [r for r in t1 if not r["likely_sports"]]
    t1_sports = [r for r in t1 if r["likely_sports"]]

    t2_travel = [r for r in t2 if not r["likely_sports"]]
    t2_sports = [r for r in t2 if r["likely_sports"]]
    t3_travel = [r for r in t3 if not r["likely_sports"]]
    t3_sports = [r for r in t3 if r["likely_sports"]]

    lines = []
    lines.append("# Compare Pages — Tiered Keep List")
    lines.append("")
    lines.append(f"- **Total compare pages on disk:** {len(rows)}")
    lines.append(f"- **Data source:** Semrush US database, `phrase_these` endpoint")
    lines.append(f"- **Method:** For each slug `A-vs-B`, we queried both `A vs B` and `B vs A` and summed monthly search volumes.")
    lines.append("")
    lines.append("## ⚠️ Sports/politics caveat — read this first")
    lines.append("")
    lines.append("Raw SEMrush volumes for country-vs-country and major-club city pairs are heavily ")
    lines.append("inflated by sports SERPs (football/cricket national teams, La Liga, Premier League, NFL, ")
    lines.append("College Football, etc.) — not travel intent. We flag these with `likely_sports=yes` ")
    lines.append("in the CSV. **The true editorial priority tier is `likely_sports=no` + Tier 1/2** — ")
    lines.append("because those are the pages where the search volume actually reflects travel intent.")
    lines.append("")
    lines.append(f"- {sports_flag} of {len(rows)} rows flagged as likely sports-inflated.")
    lines.append(f"- Tier 1: **{len(t1_travel)} pure-travel** + {len(t1_sports)} sports-inflated")
    lines.append(f"- Tier 2: **{len(t2_travel)} pure-travel** + {len(t2_sports)} sports-inflated")
    lines.append(f"- Tier 3: **{len(t3_travel)} pure-travel** + {len(t3_sports)} sports-inflated")
    lines.append("")
    lines.append("## Tier breakdown")
    lines.append("")
    lines.append("| Tier | Volume range | Total | Pure-travel | Sports-inflated | Action |")
    lines.append("|------|--------------|------:|------------:|----------------:|--------|")
    lines.append(f"| **1 — Flagship** | ≥ 2,000 | {tc[1]} | {len(t1_travel)} | {len(t1_sports)} | Heavy content investment; update regularly |")
    lines.append(f"| **2 — Solid**    | 500–1,999 | {tc[2]} | {len(t2_travel)} | {len(t2_sports)} | Moderate upkeep; rewrite when time allows |")
    lines.append(f"| **3 — Maintain** | 100–499 | {tc[3]} | {len(t3_travel)} | {len(t3_sports)} | Keep alive, minimal investment |")
    lines.append(f"| **Drop**         | < 100 | {tc[0]} | — | — | Consider deleting |")
    lines.append("")
    lines.append(f"**Keep (raw):** {tc[1] + tc[2] + tc[3]} pages   |   ")
    lines.append(f"**Keep (travel-only):** {len(t1_travel) + len(t2_travel) + len(t3_travel)} pages   |   ")
    lines.append(f"**Drop (< 100 vol):** {tc[0]} pages")
    lines.append("")
    lines.append("## Recommended editorial strategy")
    lines.append("")
    lines.append("1. **Invest heavily** in Tier 1 travel-only pages (the ~55 flagship travel comparisons).")
    lines.append("2. **Maintain** Tier 2 + Tier 3 travel-only pages (~320 additional pages).")
    lines.append("3. **Audit individually** Tier 1 sports-inflated pages — keep only those already ranking or where destination brand is a valid secondary reason for the search.")
    lines.append("4. **Delete or archive** the 707 pages with < 100 total search volume.")
    lines.append("")
    lines.append("## Tier 1 — Flagship travel pages (full list)")
    lines.append("")
    lines.append("| Vol | Best keyword | URL |")
    lines.append("|----:|--------------|-----|")
    for r in t1_travel:
        lines.append(f"| {r['total_vol']:,} | {r['best_keyword']} | [{r['slug']}](compare/{r['slug']}/) |")
    lines.append("")
    lines.append("## Tier 1 — Sports-inflated (review individually, top 40)")
    lines.append("")
    lines.append("These have huge raw volumes but the SERP is dominated by sports matches. ")
    lines.append("Low ROI unless the page already ranks for a travel-intent query. See full list in `compare-tiers.csv`.")
    lines.append("")
    lines.append("| Vol | Slug |")
    lines.append("|----:|------|")
    for r in t1_sports[:40]:
        lines.append(f"| {r['total_vol']:,} | {r['slug']} |")
    if len(t1_sports) > 40:
        lines.append(f"| ... | {len(t1_sports) - 40} more in CSV |")
    lines.append("")
    lines.append("## Tier 2 — Solid travel pages (top 40)")
    lines.append("")
    lines.append("| Vol | Slug |")
    lines.append("|----:|------|")
    for r in t2_travel[:40]:
        lines.append(f"| {r['total_vol']:,} | {r['slug']} |")
    if len(t2_travel) > 40:
        lines.append(f"| ... | {len(t2_travel) - 40} more in CSV |")
    lines.append("")
    lines.append("## Tier 3 — Maintain travel pages (top 30)")
    lines.append("")
    lines.append("| Vol | Slug |")
    lines.append("|----:|------|")
    for r in t3_travel[:30]:
        lines.append(f"| {r['total_vol']:,} | {r['slug']} |")
    if len(t3_travel) > 30:
        lines.append(f"| ... | {len(t3_travel) - 30} more in CSV |")
    lines.append("")
    lines.append("## Drop candidates — top 20 of the 707 low-vol pages")
    lines.append("")
    lines.append("| Vol | Slug |")
    lines.append("|----:|------|")
    for r in drop[:20]:
        lines.append(f"| {r['total_vol']:,} | {r['slug']} |")
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("- `compare-all-search-volumes.csv` — raw Semrush data, all 1,520 pages")
    lines.append("- `compare-tiers.csv` — tiered list with `tier` and `likely_sports` columns (use this for editorial planning)")
    lines.append("- `compare-tiers-summary.md` — this file")
    lines.append("")

    with open(SUMMARY_MD, "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {SUMMARY_MD}")

    # Console summary
    print()
    print("=" * 60)
    print(f"Total: {len(rows)}")
    print(f"Tier 1 (>=2000):  {tc[1]:>4}  ({len(t1_travel)} travel, {len(t1_sports)} sports-inflated)")
    print(f"Tier 2 (500-1999):{tc[2]:>4}")
    print(f"Tier 3 (100-499): {tc[3]:>4}")
    print(f"Drop   (<100):    {tc[0]:>4}")
    print(f"Keep total: {tc[1] + tc[2] + tc[3]}")


if __name__ == "__main__":
    main()
