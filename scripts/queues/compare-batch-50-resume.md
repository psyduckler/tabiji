# Compare upgrade batch — resume guide

## Goal
Upgrade compare pages from sub-100 to **100/100** on `scripts/score_compare.py`, one at a time, each in its own branch + PR + squash-merge.

## Status (as of 2026-04-25, after second long session)
- **Done so far:** 64 pages at 100/100.
- **Remaining sub-100:** 852 pages total. Top 50 by impact saved in `scripts/queues/compare-batch-50.json`.
- **Next page to start:** top of `scripts/queues/compare-batch-50.json` — currently `nha-trang-vs-phu-quoc` (65, impr=110, FAQ=8 — needs FAQ expansion).

### Pages completed in the most recent long session (15):
seychelles-vs-maldives, cayman-islands-vs-bahamas, shanghai-vs-hong-kong, bangkok-vs-singapore, norway-vs-iceland, morocco-vs-egypt (FAQ 7→16), samoa-vs-tonga, tonga-vs-fiji, jamaica-vs-st-lucia, kansas-city-vs-st-louis, london-vs-paris (FAQ 8→16, fixed `&amp;amp;`), cayman-islands-vs-turks-and-caicos, bali-vs-koh-samui, aruba-vs-curacao, japan-vs-vietnam.

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
   - Insert custom Quick Answers + Personalize widget + Visual Scorecard between the photo-grid and verdict-box (city-pair-specific content; anchor cards to **existing** body IDs only — grep first)
   - Remove duplicate `ux-cost-table` and `ux-weather-table` blocks if present (most pages have NO duplicates — skip on those)
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
- **JS string-quoting in fallbacks:** when writing the Personalize `recommendations` / `fallbacks` JS strings, never use unescaped double-quotes inside the value. Use `&lsquo;`/`&rsquo;` smart quotes or `&#39;` instead. (Hit this in kansas-city-vs-st-louis on "big four".)
- **FAQ count off-by-one:** `score_compare.py` counts both `class="faq-item"` and `itemtype="Question"`. After adding 9 items to a 7-item FAQ, sometimes lands at 15 not 16 — add one more. Pages with `itemtype="https://schema.org/Question"` on each faq-item count each one twice (visible item + itemtype = 2× count); these are easier to satisfy.
- **Quick Answers anchor IDs:** must point to existing IDs in the body. Run `grep -oE 'id="[a-z-]+"' <file> | sort -u` first to find real targets. **Don't reuse the same anchor for all 6 cards** — score gate flags broken anchors and you'll need to re-edit.
- **`git checkout main` may fail** with "main is already used by worktree" — use `git checkout -b <new> origin/main` instead.
- **`gh pr merge --squash --delete-branch` may fail** with the same worktree error but the merge usually still succeeds remotely. Verify with `gh pr view <#> --json state,mergedAt`. The `--delete-branch` flag may also fail (branch already deleted by GH); follow up with `git push origin --delete compare/upgrade-<slug>` (which often errors "remote ref does not exist" — that means GH already cleaned it up).
- **Pages with both ux-cost-table AND ux-weather-table:** remove together in one Edit call, since they're sequential blocks.
- **Some pages have NO duplicate ux-cost-table/ux-weather-table** — skip that step on those pages.
- **Edit tool placeholder mistake:** when crafting the QA + Personalize + Scorecard block, write the entire block in one Edit, don't insert intermediate "REPLACE_THIS_SLOT" placeholders — the Edit tool literally inserts whatever you give it. (Hit this in kansas-city-vs-st-louis; recovered by writing a second Edit that completed the broken block.)

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

## Pages already 100/100 (skip these)

**Original top 10 batch:** croatia-vs-montenegro, st-barts-vs-turks-and-caicos, costa-rica-vs-hawaii, vietnam-vs-philippines, bali-vs-hawaii, portugal-vs-morocco, paris-vs-amsterdam, kyoto-vs-nara, osaka-vs-fukuoka, puerto-rico-vs-dominican-republic, tokyo-vs-kyoto.

**Earlier batch (#11–16):** tokyo-vs-hong-kong, morocco-vs-turkey, greece-vs-italy, chennai-vs-mumbai, tokyo-vs-osaka, iceland-vs-ireland.

**Long session 1 (33 pages):** greece-vs-spain, st-lucia-vs-martinique, greece-vs-croatia, tokyo-vs-seoul, new-caledonia-vs-fiji, maldives-vs-hawaii, cyprus-vs-crete, berlin-vs-munich, cyprus-vs-malta, slovenia-vs-austria, bali-vs-fiji, dominica-vs-st-lucia, chamonix-vs-zermatt, cook-islands-vs-fiji, costa-rica-vs-colombia, auckland-vs-christchurch, faroe-islands-vs-iceland, tokyo-vs-shanghai, buenos-aires-vs-santiago, mexico-city-vs-cancun, malta-vs-sicily, india-vs-nepal, naxos-vs-paros, edinburgh-vs-dublin, shenzhen-vs-hong-kong, galway-vs-cork, tibet-vs-nepal, mauritius-vs-seychelles, queenstown-vs-wanaka, beijing-vs-hong-kong, st-kitts-vs-antigua, antwerp-vs-brussels, spain-vs-italy.

**Long session 2 (15 pages, this session):** seychelles-vs-maldives, cayman-islands-vs-bahamas, shanghai-vs-hong-kong, bangkok-vs-singapore, norway-vs-iceland, morocco-vs-egypt, samoa-vs-tonga, tonga-vs-fiji, jamaica-vs-st-lucia, kansas-city-vs-st-louis, london-vs-paris, cayman-islands-vs-turks-and-caicos, bali-vs-koh-samui, aruba-vs-curacao, japan-vs-vietnam.

(Treat `scripts/queues/compare-batch-50.json` as authoritative — anything not in there is either already 100/100 or below the impact threshold.)
