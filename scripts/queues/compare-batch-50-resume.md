# Compare upgrade batch — resume guide

## Goal
Upgrade 50 compare pages from sub-100 to **100/100** on `scripts/score_compare.py`, one at a time, each in its own branch + PR + squash-merge.

## Status
- **Done so far:** 16 of 60 pages (10 from the original top-10 batch + 6 from this 50-batch).
- **Remaining in this batch:** 44 pages, ranks 17–60 in `scripts/queues/compare-batch-50.json`.
- **Next page to start:** rank 17 — see queue file for the current top of the list (it's regenerated each time, but `greece-vs-spain` was next when paused).

## Hard rules from the user
- **No shortcuts.** Don't write helper scripts that auto-fix multiple pages. Every transformation on every page goes through individual `Edit` tool calls.
- **One page at a time.** Branch → edit → score gate → commit → PR → squash-merge → next page.
- **Thoroughness over speed.** Custom Quick Answers, Personalize, and Scorecard content per city pair — never templated.
- Pages must pass `python3 scripts/score_compare.py <slug> --gate 100` before commit.

## Per-page workflow (every page)
1. `git fetch origin main && git checkout -b compare/upgrade-<slug> origin/main`
2. Audit: `python3 scripts/score_compare.py <slug>`, then grep for `<title>`, photo-grid first img, verdict-box, `class="ux-cost-table"`, `class="ux-weather-table"`, broken `<h3>Should you choose…</h3>` FAQ titles, body IDs.
3. Apply each fix as a separate `Edit`:
   - Trim title (drop `(2026 Comparison)` if total chars >65)
   - `replace_all` `<div class="section-winner"><h3>Winner takeaway</h3><ul>` → `<div class="tabiji-verdict"><strong>tabiji verdict:</strong> <ul>`
   - LCP fix on first `.photo-grid` `<img>`: remove `loading="lazy"`, add `fetchpriority="high"`
   - Fix any broken `<h3>Should you choose X or Y for …?</h3>` template titles
   - Insert custom Quick Answers + Personalize widget + Visual Scorecard between the photo-grid and verdict-box (city-pair-specific content)
   - Remove duplicate `ux-cost-table` and `ux-weather-table` blocks if present
   - If FAQ <16: append items to reach **16+**, mirror them in the FAQPage JSON-LD
4. Verify: `python3 scripts/score_compare.py <slug> --gate 100` must exit 0
5. Commit, push, `gh pr create`, `gh pr merge <PR#> --squash --delete-branch`

## Reference pages (passing 100/100, can mimic structure)
- `compare/tokyo-vs-kyoto/` — first 100/100 example (gold standard)
- `compare/croatia-vs-montenegro/` — full template with all components
- `compare/iceland-vs-ireland/` — most recent (rank 16, just completed)

## Common gotchas
- **FAQ count off-by-one:** `score_compare.py` counts `class="faq-item"` and `itemtype="Question"`. After adding 9 items to a 7-item FAQ, sometimes lands at 15 not 16 — add one more.
- **Quick Answers anchor IDs:** must point to existing IDs in the body. Run `grep -oE 'id="[a-z-]+"' <file> | sort -u` first to find real targets. Common mismatches: pages with `#beaches-and-islands` vs `#quick-comparison`.
- **`git checkout main` may fail** with "main is already used by worktree" — use `git checkout -b <new> origin/main` instead.
- **`gh pr merge` may fail** with the same worktree error but the merge still succeeds remotely. Verify with `gh pr view <#> --json state,mergedAt`.

## Key files
- Score gate: `scripts/score_compare.py`
- Queue: `scripts/queues/compare-batch-50.json` (regenerate from current state if stale)
- Skill doc: `.claude/skills/compare-article-builder.md` (rubric explained)
- Builder: `generators/compare/build_compare.py` (has `STRICT_QUALITY_GATE=1` env-var gate)

## To resume
```bash
# Check current state
python3 scripts/score_compare.py --all --below 90 | head -20

# Regenerate the next-50 queue from current state
python3 -c "
import sys, json, csv, pathlib, re
sys.path.insert(0, 'scripts')
from score_compare import score_all
results = score_all()
gsc = {}
with open('/tmp/tabiji-debug/gsc-data.csv') as f:
    for r in csv.DictReader(f):
        m = re.search(r'/compare/([^/#]+)/', r['url'])
        if m: gsc[m.group(1)] = (int(r['clicks']), int(r['impressions']))
sub = [{'slug':r['slug'],'score':r['score'],'tier':r['tier'],'faq_n':r['faq_n'],'clicks':gsc.get(r['slug'],(0,0))[0],'impressions':gsc.get(r['slug'],(0,0))[1]} for r in results if r['score']<100]
sub.sort(key=lambda x:(-(x['impressions']*(100-x['score'])), x['score']))
pathlib.Path('scripts/queues/compare-batch-50.json').write_text(json.dumps(sub[:50], indent=2))
print(f'queue size: {len(sub[:50])}, top 5:')
for r in sub[:5]: print(f'  {r[\"score\"]:>3}  impr={r[\"impressions\"]:>4}  {r[\"slug\"]}')
"

# Then pick up from rank 17
```

## Pages already 100/100 (skip these)
**Original top 10 batch:** croatia-vs-montenegro, st-barts-vs-turks-and-caicos, costa-rica-vs-hawaii, vietnam-vs-philippines, bali-vs-hawaii, portugal-vs-morocco, paris-vs-amsterdam, kyoto-vs-nara, osaka-vs-fukuoka, puerto-rico-vs-dominican-republic, tokyo-vs-kyoto.

**This batch so far (#11–16):** tokyo-vs-hong-kong, morocco-vs-turkey, greece-vs-italy, chennai-vs-mumbai, tokyo-vs-osaka, iceland-vs-ireland.
