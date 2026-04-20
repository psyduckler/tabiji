#!/usr/bin/env python3
"""
Fetch Semrush search volumes for every on-disk compare page (both directions).
Reuses prior progress from semrush-volume-progress.json.
Outputs:
  - compare-all-search-volumes.csv (full sorted by total_vol desc)
  - compare-tiers.csv (tier 1/2/3 classification)
"""

import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

_env_key = os.environ.get("SEMRUSH_API_KEY")
if _env_key:
    API_KEY = _env_key
else:
    import subprocess
    try:
        API_KEY = subprocess.check_output(
            ["security", "find-generic-password", "-s", "semrush-api-key", "-w"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        raise SystemExit("ERROR: SEMRUSH_API_KEY not set and 'semrush-api-key' not in macOS keychain.")
DATABASE = "us"

ROOT = "/Users/bjh/Documents/tabiji/.claude/worktrees/happy-tharp-5601b2"
COMPARE_DIR = os.path.join(ROOT, "compare")
PROGRESS_FILE = os.path.join(ROOT, "scripts", "semrush-volume-progress.json")
ANALYSIS = os.path.join(ROOT, "scripts", "compare-analysis")
OUTPUT_CSV = os.path.join(ANALYSIS, "compare-all-search-volumes.csv")
TIERS_CSV = os.path.join(ANALYSIS, "compare-tiers.csv")

BATCH_SIZE = 100


def slug_to_keywords(slug):
    parts = slug.split("-vs-")
    if len(parts) != 2:
        return None, None
    a = parts[0].replace("-", " ")
    b = parts[1].replace("-", " ")
    return f"{a} vs {b}", f"{b} vs {a}"


def fetch_batch(phrases):
    """Call phrase_these with up to 100 phrases, return dict keyword -> volume."""
    payload = ";".join(phrases)
    url = (
        "https://api.semrush.com/?type=phrase_these"
        f"&key={API_KEY}"
        f"&phrase={urllib.parse.quote(payload)}"
        f"&database={DATABASE}"
        "&export_columns=Ph,Nq"
    )
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8").strip()
    except Exception as e:
        print(f"  Batch error: {e}", file=sys.stderr)
        return {}

    out = {}
    lines = body.split("\n")
    if len(lines) < 2:
        return out
    for line in lines[1:]:
        parts = line.split(";")
        if len(parts) >= 2:
            try:
                out[parts[0]] = int(parts[1])
            except ValueError:
                out[parts[0]] = 0
    return out


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def list_on_disk_slugs():
    slugs = []
    for entry in sorted(os.listdir(COMPARE_DIR)):
        full = os.path.join(COMPARE_DIR, entry)
        if "-vs-" in entry and os.path.isdir(full):
            slugs.append(entry)
    return slugs


def classify_tiers(rows):
    """Tier 1: total_vol >= 500, Tier 2: 100-499, Tier 3: 10-99, Drop: <10."""
    tiered = []
    for r in rows:
        v = r["total_vol"]
        if v >= 500:
            tier = 1
        elif v >= 100:
            tier = 2
        elif v >= 10:
            tier = 3
        else:
            tier = 0  # drop
        tiered.append({**r, "tier": tier})
    return tiered


def main():
    slugs = list_on_disk_slugs()
    progress = load_progress()

    print(f"On-disk compare pages: {len(slugs)}")
    have = [s for s in slugs if s in progress]
    need = [s for s in slugs if s not in progress]
    print(f"Already in progress: {len(have)}")
    print(f"Need to fetch: {len(need)}")

    # Build list of keyword pairs for missing slugs
    pending = []
    for s in need:
        kw1, kw2 = slug_to_keywords(s)
        if kw1 is None:
            continue
        pending.append((s, kw1, kw2))

    # Build a flat list of all keywords to fetch, preserving which slug/direction
    queries = []
    for s, kw1, kw2 in pending:
        queries.append((s, 1, kw1))
        queries.append((s, 2, kw2))

    print(f"Total keywords to query: {len(queries)}")
    print(f"Batches (size {BATCH_SIZE}): {(len(queries) + BATCH_SIZE - 1) // BATCH_SIZE}")

    # Dedupe keywords within a batch (Semrush returns one row per unique phrase)
    fetched = {}
    batches_done = 0
    for i in range(0, len(queries), BATCH_SIZE):
        batch = queries[i : i + BATCH_SIZE]
        phrases = [q[2] for q in batch]
        # Dedupe preserving order
        seen = set()
        uniq = []
        for p in phrases:
            if p not in seen:
                seen.add(p)
                uniq.append(p)

        res = fetch_batch(uniq)
        for p in uniq:
            fetched[p] = res.get(p, 0)

        batches_done += 1
        print(
            f"  batch {batches_done}: {len(uniq)} phrases, "
            f"sample: {uniq[0]}={res.get(uniq[0], 0)}"
        )
        time.sleep(0.3)  # small courtesy delay between batches

    # Stitch back into slug rows
    for s, kw1, kw2 in pending:
        v1 = fetched.get(kw1, 0)
        v2 = fetched.get(kw2, 0)
        if v1 >= v2:
            best_kw, best_vol = kw1, v1
        else:
            best_kw, best_vol = kw2, v2
        progress[s] = {
            "slug": s,
            "url": f"https://tabiji.ai/compare/{s}/",
            "keyword_1": kw1,
            "vol_1": v1,
            "keyword_2": kw2,
            "vol_2": v2,
            "best_keyword": best_kw,
            "best_vol": best_vol,
            "total_vol": v1 + v2,
        }

    save_progress(progress)

    # Build output rows from on-disk slugs only
    rows = []
    for s in slugs:
        if s in progress:
            rows.append(progress[s])
        else:
            rows.append(
                {
                    "slug": s,
                    "url": f"https://tabiji.ai/compare/{s}/",
                    "keyword_1": "",
                    "vol_1": 0,
                    "keyword_2": "",
                    "vol_2": 0,
                    "best_keyword": "",
                    "best_vol": 0,
                    "total_vol": 0,
                }
            )

    rows.sort(key=lambda r: r["total_vol"], reverse=True)

    fieldnames = [
        "slug",
        "url",
        "keyword_1",
        "vol_1",
        "keyword_2",
        "vol_2",
        "best_keyword",
        "best_vol",
        "total_vol",
    ]
    with open(OUTPUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote {OUTPUT_CSV} ({len(rows)} rows)")

    tiered = classify_tiers(rows)
    tiered_fields = fieldnames + ["tier"]
    with open(TIERS_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=tiered_fields)
        w.writeheader()
        w.writerows(tiered)
    print(f"Wrote {TIERS_CSV}")

    # Summary
    from collections import Counter
    c = Counter(r["tier"] for r in tiered)
    print("\nTier breakdown:")
    print(f"  Tier 1 (>=500 vol): {c[1]}")
    print(f"  Tier 2 (100-499): {c[2]}")
    print(f"  Tier 3 (10-99): {c[3]}")
    print(f"  Drop (<10): {c[0]}")


if __name__ == "__main__":
    main()
