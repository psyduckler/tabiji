# Compare upgrade batch — resume guide

## Goal
Upgrade compare pages from sub-100 to **100/100** on `scripts/score_compare.py`, one at a time, each in its own branch + PR + squash-merge.

## Status (as of 2026-04-25, post-100-milestone session)
- **Done so far:** 100 pages at 100/100 (10% of 916 total compare pages).
- **Remaining sub-100:** 816 pages total. Top 50 by impact saved in `scripts/queues/compare-batch-50.json`.
- **Next page to start:** top of `scripts/queues/compare-batch-50.json` — currently `crete-vs-santorini` (59, FAQ=16).

### Pages completed in the most recent long session (26):
catania-vs-palermo, colmar-vs-strasbourg, ghent-vs-bruges, nice-vs-cannes, peru-vs-bolivia, portugal-vs-croatia, rome-vs-florence, tallinn-vs-riga, sayulita-vs-puerto-vallarta, copenhagen-vs-stockholm, martinique-vs-guadeloupe, tulum-vs-puerto-vallarta, cinque-terre-vs-portofino, dubai-vs-singapore, lake-como-vs-lake-garda, mexico-city-vs-oaxaca, philippines-vs-thailand, san-sebastian-vs-bilbao, amsterdam-vs-berlin, anguilla-vs-st-barts, austin-vs-nashville, berlin-vs-hamburg, berlin-vs-prague, berlin-vs-vienna, bocas-del-toro-vs-san-blas, corfu-vs-crete.

## Hard rules from the user
- **No shortcuts.** Don't write helper scripts that auto-fix multiple pages. Every transformation on every page goes through individual `Edit` tool calls.
- **One page at a time.** Branch → edit → score gate → commit → PR → squash-merge → next page.
- **Thoroughness over speed.** Custom Quick Answers, Personalize, and Scorecard content per city pair — never templated.
- Pages must pass `python3 scripts/score_compare.py <slug> --gate 100` before commit.

## Per-page workflow (every page)
1. `git fetch origin main && git checkout -b compare/upgrade-<slug> origin/main`
2. Audit: `python3 scripts/score_compare.py <slug>`, then grep for `<title>`, photo-grid first img, verdict-box, body IDs.
3. Apply each fix as a separate `Edit`:
   - Trim title (drop `(2026 Comparison)` if total chars >65)
   - `replace_all` `<div class="section-winner"><h3>Winner takeaway</h3><ul>` → `<div class="tabiji-verdict"><strong>tabiji verdict:</strong> <ul>`
   - LCP fix on first `.photo-grid` `<img>`: remove `loading="lazy"`, add `fetchpriority="high"`
   - Insert custom Quick Answers + Personalize widget + Visual Scorecard between the photo-grid and verdict-box (city-pair-specific content; anchor cards to **existing** body IDs only — grep first)
   - Fix `&amp;amp;` double-encoded ampersands (commonly in related-card descriptions)
   - If FAQ <16: append items to reach **16+**, mirror them in the FAQPage JSON-LD
4. Verify: `python3 scripts/score_compare.py <slug> --gate 100` must exit 0
5. Commit, push, `gh pr create`, `gh pr merge <PR#> --squash --delete-branch`
6. Verify with `gh pr view <#> --json state,mergedAt`

## Reference pages (passing 100/100, can mimic structure)
- `compare/tokyo-vs-kyoto/` — first 100/100 example (gold standard)
- `compare/croatia-vs-montenegro/` — full template with all components
- `compare/morocco-vs-egypt/` — recent (PR #613, included FAQ expansion 7→16)
- `compare/london-vs-paris/` — recent (PR #624, FAQ expansion 8→16 + `&amp;amp;` fix)

## Common gotchas
- **JS string-quoting in fallbacks:** when writing the Personalize `recommendations` / `fallbacks` JS strings, never use unescaped double-quotes inside the value. Use `&lsquo;`/`&rsquo;` smart quotes or `&#39;` instead.
- **FAQ count off-by-one is the most common failure:** `score_compare.py` counts both `class="faq-item"` and `itemtype="Question"`. After adding "8 new items" to a 7-item FAQ, often lands at 15 not 16 — add one more. Pages with `itemtype="https://schema.org/Question"` on each faq-item count each one twice (visible item + itemtype = 2× count); these are easier to satisfy. **Verify after every FAQ expansion** before the score gate.
- **Quick Answers anchor IDs:** must point to existing IDs in the body. Run `grep -oE 'id="[a-z-]+"' <file> | sort -u` first to find real targets. **Don't reuse the same anchor for all 6 cards** — score gate flags broken anchors.
- **`git checkout main` may fail** with "main is already used by worktree" — use `git checkout -b <new> origin/main` instead.
- **`gh pr merge --squash --delete-branch` may fail** with the same worktree error but the merge usually still succeeds remotely. Verify with `gh pr view <#> --json state,mergedAt`.
- **Pages with both ux-cost-table AND ux-weather-table:** remove together in one Edit call, since they're sequential blocks.
- **Some pages have NO duplicate ux-cost-table/ux-weather-table** — skip that step on those pages.
- **Edit tool placeholder mistake:** when crafting the QA + Personalize + Scorecard block, write the entire block in one Edit, don't insert intermediate "REPLACE_THIS_SLOT" placeholders — the Edit tool literally inserts whatever you give it.
- **Bad git refs with spaces in filenames:** if you see `fatal: bad object refs/heads/main 2`, run `find .git/refs -type f -name '* *' | xargs -I {} rm -f "{}"` to clean up macOS Finder duplicates.
- **`&amp;amp;` encoding** is now in approximately every page that has related-card descriptions — always run `replace_all '&amp;amp;' → '&amp;'` early in workflow.

## Key files
- Score gate: `scripts/score_compare.py`
- Queue: `scripts/queues/compare-batch-50.json` (regenerate from current state)
- Skill doc: `.claude/skills/compare-article-builder.md` (rubric explained)
- Builder: `generators/compare/build_compare.py` (has `STRICT_QUALITY_GATE=1` env-var gate)

## To regenerate the queue (run before starting a new session)
```bash
python3 -c "
import sys, json, csv, pathlib, re
sys.path.insert(0, 'scripts')
from score_compare import score_all
results = score_all()
gsc = {}
try:
    with open('/tmp/tabiji-debug/gsc-data.csv') as f:
        for r in csv.DictReader(f):
            m = re.search(r'/compare/([^/#]+)/', r['url'])
            if m: gsc[m.group(1)] = (int(r['clicks']), int(r['impressions']))
except FileNotFoundError:
    pass
sub = [{'slug':r['slug'],'score':r['score'],'tier':r['tier'],'faq_n':r['faq_n'],'clicks':gsc.get(r['slug'],(0,0))[0],'impressions':gsc.get(r['slug'],(0,0))[1]} for r in results if r['score']<100]
sub.sort(key=lambda x:(-(x['impressions']*(100-x['score'])), x['score']))
pathlib.Path('scripts/queues/compare-batch-50.json').write_text(json.dumps(sub[:50], indent=2))
print(f'queue saved: top {len(sub[:50])} pages')
print('top 5:')
for r in sub[:5]: print(f'  {r[\"score\"]:>3}  impr={r[\"impressions\"]:>4}  {r[\"slug\"]}')
"
```

## Session productivity stats
- **Session 1 (long):** 33 pages
- **Session 2 (resume):** 15 pages
- **Session 3 (10-page batch):** 10 pages
- **Session 4 (26-page batch):** 26 pages
- **Total:** 100 pages at 100/100 (out of 916 total compare pages)

The pattern stabilizes around 5-7 minutes per page once the page already has FAQ=16, and 10-15 minutes for pages requiring FAQ expansion 7→16 or 8→16. The single most common failure is FAQ off-by-one (target 16, often lands at 15 — verify before commit).
