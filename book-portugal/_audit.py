#!/usr/bin/env python3
"""5-pass master-publisher editorial audit of the Portugal book manuscript.

Pass 1: Reddit shards & URL fragments (should be 0 after polish_scam_prose.py)
Pass 2: Truncated sentences / ellipses / cut-off strings
Pass 3: American-English consistency (colour→color, organise→organize, etc.)
Pass 4: Grammar & formatting (double spaces, missing apostrophes, orphan commas)
Pass 5: Cross-reference consistency (city counts, scam totals, all cities mentioned)
"""
import re, json, yaml
from pathlib import Path

HERE = Path("/tmp/pt-book/book-portugal")
MANUSCRIPT = HERE / "build" / "manuscript.md"
CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())
text = MANUSCRIPT.read_text()

# ──────────────────────────────────────────────────────
# PASS 1: Reddit shards & URL fragments
# ──────────────────────────────────────────────────────
print("=== PASS 1: Reddit shards / URL fragments ===")
issues_1 = 0
# comments/XXXXX or r/subreddit '...'
for m in re.finditer(r'r/\w+\s+[\'\"][^\'\"]+[\'\"][^.]*comments/\w+', text):
    issues_1 += 1
    if issues_1 <= 5:
        print(f'  ⚠ Reddit shard: ...{m.group(0)[:120]}...')
for m in re.finditer(r'\(comments/\w+[^)]*\)', text):
    issues_1 += 1
    if issues_1 <= 10:
        print(f'  ⚠ comments/... URL: {m.group(0)[:80]}')
# Raw URLs
for m in re.finditer(r'https?://reddit\.com/[^\s\)]*', text):
    issues_1 += 1
    if issues_1 <= 3:
        print(f'  ⚠ Raw Reddit URL: {m.group(0)[:100]}')
# subreddit-mention in the middle of prose (allowed in intro / cta; flag in scam bodies)
print(f'  Total Pass 1 issues: {issues_1}')
print()

# ──────────────────────────────────────────────────────
# PASS 2: Truncated sentences / ellipses
# ──────────────────────────────────────────────────────
print("=== PASS 2: Truncated sentences / ellipses ===")
issues_2 = 0
# Three-dot ellipses within sentences (not at end of paragraph)
for m in re.finditer(r'\.\.\.(?!\s*$)(?!\s*\n)', text):
    ctx = text[max(0, m.start()-30):m.end()+30].replace('\n', ' ')
    issues_2 += 1
    if issues_2 <= 5:
        print(f'  ⚠ Mid-sentence ellipsis: ...{ctx[:80]}...')
# Unclosed quotes
sentences = text.split('\n\n')
for para in sentences:
    if para.count("'") % 2 == 1 and para.count("'s") < para.count("'") / 2:
        # too many ' to be just contractions
        pass  # expensive false positives — skip
# Obvious truncations: sentence ends with preposition+space
trunc_regex = re.compile(r'\b(with|in|at|to|for|by|from|through|across|per|after)\.\s')
for m in trunc_regex.finditer(text):
    issues_2 += 1
    if issues_2 <= 5:
        print(f'  ⚠ Preposition-before-period: "...{text[max(0,m.start()-40):m.end()]}"')
print(f'  Total Pass 2 issues: {issues_2}')
print()

# ──────────────────────────────────────────────────────
# PASS 3: American-English consistency
# ──────────────────────────────────────────────────────
print("=== PASS 3: American-English consistency ===")
issues_3 = 0
# British spellings that should become American
british_to_american = {
    'colour': 'color',
    'colours': 'colors',
    'favour': 'favor',
    'favours': 'favors',
    'organise': 'organize',
    'organised': 'organized',
    'organisation': 'organization',
    'recognise': 'recognize',
    'realise': 'realize',
    'centre': 'center',
    'theatre': 'theater',
    'metre': 'meter',
    'metres': 'meters',
    'litre': 'liter',
    'kilometre': 'kilometer',
    'travelled': 'traveled',
    'travelling': 'traveling',
    'cancelled': 'canceled',
    'labelled': 'labeled',
    'aluminium': 'aluminum',
    'defence': 'defense',
    'offence': 'offense',
    'licence': 'license',  # noun vs verb — keep careful
    'practise': 'practice',  # verb
    'whilst': 'while',
    'amongst': 'among',
    'towards': 'toward',
}
for brit, amer in british_to_american.items():
    # Case-sensitive word boundary
    for m in re.finditer(rf'\b{brit}\b', text):
        issues_3 += 1
        if issues_3 <= 15:
            print(f'  ⚠ British → American: "{brit}" → "{amer}" at "...{text[max(0,m.start()-30):m.end()+30]}..."')
print(f'  Total Pass 3 issues: {issues_3}')
print()

# ──────────────────────────────────────────────────────
# PASS 4: Grammar & formatting
# ──────────────────────────────────────────────────────
print("=== PASS 4: Grammar & formatting ===")
issues_4 = 0
# Double spaces (except after period for old-style type)
for m in re.finditer(r'(?<=[a-z])  +(?=[a-z])', text):
    issues_4 += 1
    if issues_4 <= 5:
        print(f'  ⚠ Double space: "...{text[max(0,m.start()-30):m.end()+30]}..."')
# Triple+ newlines
for m in re.finditer(r'\n\n\n\n+', text):
    issues_4 += 1
    if issues_4 <= 5:
        print(f'  ⚠ Excessive blank lines')
# Orphan commas (sentence ending with " , ")
for m in re.finditer(r'\s,\s', text):
    ctx = text[max(0, m.start()-20):m.end()+20]
    if ', ' not in ctx[ctx.find(' ,'):ctx.find(' ,')+4]:  # not a comma with space
        issues_4 += 1
        if issues_4 <= 3:
            print(f'  ⚠ Orphan comma: "...{ctx}..."')
# Unicode-smart-quote inconsistency
straight = text.count('"')
curly_open = text.count(chr(8220))
curly_close = text.count(chr(8221))
if straight and (curly_open or curly_close):
    issues_4 += 1
    print(f'  ⚠ Mixed straight/curly double-quotes: {straight} straight, {curly_open+curly_close} curly')
# Curly apostrophes vs straight
straight_apos = len(re.findall(r"(?<![0-9])'(?![0-9])", text))  # apostrophes not in year refs
# (That check is noisy; skip in summary)
print(f'  Total Pass 4 issues: {issues_4}')
print()

# ──────────────────────────────────────────────────────
# PASS 5: Cross-reference consistency
# ──────────────────────────────────────────────────────
print("=== PASS 5: Cross-reference consistency ===")
issues_5 = 0

# Scam total (body uses "sixty-five", numeric references should match)
if "sixty-five" not in text:
    issues_5 += 1
    print(f'  ⚠ Missing canonical "sixty-five" scam count in prose')
# Volume number
if "Volume 14" not in text and "Volume Fourteen" not in text:
    issues_5 += 1
    print(f'  ⚠ Missing "Volume 14" reference')
# All 10 cities should be named in the Cities at a Glance section
PT_CITIES = ['Lisbon','Porto','Sintra','Funchal','Faro','Albufeira','Lagos','Cascais','Coimbra','Nazaré']
for city in PT_CITIES:
    if text.count(city) < 3:
        issues_5 += 1
        print(f'  ⚠ {city} mentioned only {text.count(city)}× (expected 3+)')

# Check all 10 city chapters are present
for slug in ('lisbon','porto','sintra','funchal','faro','albufeira','lagos-portugal','cascais','coimbra','nazare'):
    data_path = HERE / f"../api/v1/scams/{slug}.json"
    if data_path.exists():
        d = json.load(open(data_path))
        city = d['city']
        # expect the city name as an h1
        if f'\n\n# {city}' not in text:
            issues_5 += 1
            print(f'  ⚠ Missing city chapter "# {city}"')

print(f'  Total Pass 5 issues: {issues_5}')
print()

total = issues_1 + issues_2 + issues_3 + issues_4 + issues_5
print(f"════════════════════════════════")
print(f"TOTAL AUDIT ISSUES:  {total}")
print(f"════════════════════════════════")
