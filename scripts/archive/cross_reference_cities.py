#!/usr/bin/env python3
"""
Cross-reference Barcelona + Kyoto cleaned keyword data to find
templatizable long-tail patterns that exist in BOTH cities.

A pattern is "templatizable" if it follows the form `[city] X` or `X [city]`
and X (the modifier or structure) appears in both city datasets with
meaningful volume.
"""
import json
import re
from collections import defaultdict

BCN = json.load(open('/Users/bjh/Documents/tabiji/scripts/barcelona-research/clean_keywords.json'))
KYO = json.load(open('/Users/bjh/Documents/tabiji/scripts/kyoto-research/clean_keywords.json'))

def normalize(kw, city):
    """Replace city name with [CITY] placeholder so we can match patterns across cities."""
    s = kw.lower()
    s = re.sub(rf"\b{city}\b", "[CITY]", s)
    s = re.sub(r"\bspain\b", "", s)
    s = re.sub(r"\bjapan\b", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

bcn_patterns = defaultdict(int)
bcn_examples = defaultdict(list)
for r in BCN:
    norm = normalize(r["keyword"], "barcelona")
    if "[CITY]" not in norm: continue
    bcn_patterns[norm] += r["volume"]
    if len(bcn_examples[norm]) < 3:
        bcn_examples[norm].append((r["keyword"], r["volume"]))

kyo_patterns = defaultdict(int)
kyo_examples = defaultdict(list)
for r in KYO:
    norm = normalize(r["keyword"], "kyoto")
    if "[CITY]" not in norm: continue
    kyo_patterns[norm] += r["volume"]
    if len(kyo_examples[norm]) < 3:
        kyo_examples[norm].append((r["keyword"], r["volume"]))

# Patterns that exist in BOTH cities
common = set(bcn_patterns.keys()) & set(kyo_patterns.keys())
print(f"BCN patterns: {len(bcn_patterns)}, KYO patterns: {len(kyo_patterns)}, COMMON: {len(common)}")

# Score each common pattern by combined volume + symmetry (both cities have meaningful vol)
scored = []
for p in common:
    bv, kv = bcn_patterns[p], kyo_patterns[p]
    if bv < 50 or kv < 50:
        continue
    combined = bv + kv
    # Penalize asymmetric patterns
    ratio = min(bv, kv) / max(bv, kv)
    score = combined * (0.5 + ratio / 2)
    scored.append({
        "pattern": p,
        "bcn_vol": bv,
        "kyo_vol": kv,
        "combined": combined,
        "ratio": round(ratio, 2),
        "score": round(score),
        "bcn_examples": bcn_examples[p],
        "kyo_examples": kyo_examples[p],
    })

scored.sort(key=lambda r: -r["score"])
print(f"\nCommon patterns with vol >= 50 in both cities: {len(scored)}")
print(f"\n=== TOP 60 TEMPLATIZABLE PATTERNS ===")
print(f"{'Pattern':<55} {'BCN':>7} {'KYO':>7} {'Combined':>9} {'Ratio':>6}")
print("-" * 92)
for s in scored[:60]:
    print(f"{s['pattern'][:55]:<55} {s['bcn_vol']:>7,} {s['kyo_vol']:>7,} {s['combined']:>9,} {s['ratio']:>6}")

# Save
with open('/Users/bjh/Documents/tabiji/scripts/cross-ref-templates.json', 'w') as f:
    json.dump(scored[:200], f, indent=2)

print(f"\nSaved top 200 to scripts/cross-ref-templates.json")
