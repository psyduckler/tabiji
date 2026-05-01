# Compare upgrade batch — resume guide

## Goal
Upgrade compare pages from sub-100 to **100/100** on `scripts/score_compare.py`, one at a time, each in its own branch + PR + squash-merge.

## Status (as of 2026-04-27, post-263-page session)
- **Done so far:** ~263 pages at 100/100 (~28.7% of 916 total compare pages).
- **Remaining sub-100:** ~653 pages. Top 50 by impact saved in `scripts/queues/compare-batch-50.json` — **regenerate before starting a new session** (most of the entries from the prior queue are now done).
- **Active goal:** completing 100 more pages (117 done so far in the active goal session).

### Most recent batch (20 pages, 2026-04-26 second batch):
portland-vs-vancouver, sweden-vs-united-states, aconcagua-vs-denali, adelaide-vs-melbourne, albania-vs-montenegro, alps-vs-rockies, anguilla-vs-antigua, antigua-vs-barbados, arches-vs-canyonlands, aspen-vs-vail, atlanta-vs-charlotte, atlanta-vs-miami, atlanta-vs-nashville, auckland-vs-melbourne, auckland-vs-sydney, auckland-vs-wellington, austin-vs-denver, austin-vs-san-antonio, bali-vs-maldives, banff-vs-jasper.

### Pages completed in the most recent three sessions (68 pages):
**Two sessions ago (24):** amalfi-coast-vs-french-riviera, buenos-aires-vs-rio-de-janeiro, glacier-national-park-vs-banff, gold-coast-vs-sunshine-coast, grand-canyon-vs-antelope-canyon, grand-canyon-vs-bryce-canyon, haiti-vs-dominican-republic, joshua-tree-vs-death-valley, philadelphia-vs-washington-dc, rio-de-janeiro-vs-sao-paulo, sacramento-vs-san-francisco, san-francisco-vs-los-angeles, turks-and-caicos-vs-bahamas, victoria-falls-vs-iguazu-falls, yellowstone-vs-grand-canyon, andaman-islands-vs-maldives, costa-rica-vs-united-states, croatia-vs-czech-republic, galapagos-vs-amazon-ecuador, new-zealand-vs-united-states, santa-barbara-vs-monterey, albuquerque-vs-santa-fe, amsterdam-vs-copenhagen, asheville-vs-gatlinburg.

**Last session (24):** azores-vs-canary-islands, bangkok-vs-kuala-lumpur, buenos-aires-vs-montevideo, casablanca-vs-marrakech, christchurch-vs-queenstown, cuba-vs-dominican-republic, denver-vs-salt-lake-city, denver-vs-san-francisco, french-alps-vs-swiss-alps, hanoi-vs-ho-chi-minh, iguazu-vs-victoria-falls, kuala-lumpur-vs-singapore, kyrgyzstan-vs-tajikistan, lake-como-vs-amalfi-coast, liverpool-vs-manchester, los-angeles-vs-las-vegas, moscow-vs-st-petersburg, nashville-vs-new-orleans, new-orleans-vs-charleston, new-york-vs-los-angeles, new-zealand-vs-australia, philippines-vs-indonesia, playa-del-carmen-vs-tulum, quebec-city-vs-montreal.

**Most recent (20):** solomon-islands-vs-vanuatu, south-africa-vs-tanzania, tenerife-vs-gran-canaria, tuscany-vs-amalfi-coast, washington-dc-vs-boston, washington-dc-vs-new-york, yosemite-vs-grand-canyon, yosemite-vs-yellowstone, chiang-mai-vs-chiang-rai, koh-samui-vs-koh-phangan, argentina-vs-austria, argentina-vs-bolivia, australia-vs-south-korea, bali-vs-new-caledonia, barcelona-vs-monaco, hong-kong-vs-sri-lanka, luxembourg-vs-sweden, monaco-vs-strasbourg, netherlands-vs-scotland, norway-vs-switzerland.

### Skipped (stub pages, not real):
- `oahu-vs-maui` — `score_compare.py` returned "page not found or is a redirect stub". If the queue surfaces this again, skip and move on.

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

## Streamlined commit/PR/merge command (one-shot, post-edit)
After all edits are in place, this single chained command handles everything:
```bash
python3 scripts/score_compare.py <slug> --gate 100 && \
git add compare/<slug>/index.html && \
git commit -m "compare: <slug> XX → 100" && \
git push -u origin compare/upgrade-<slug> 2>&1 | tail -2 && \
gh pr create --title "compare: <slug> XX → 100" --body "QA + Personalize + Scorecard + FAQ X → 16. Score 100/100." 2>&1 | tail -2 && \
PR=$(gh pr list --head compare/upgrade-<slug> --json number --jq '.[0].number') && \
gh pr merge $PR --squash --delete-branch 2>&1 | tail -2
```

## Reference pages (passing 100/100, can mimic structure)
- `compare/tokyo-vs-kyoto/` — first 100/100 example (gold standard)
- `compare/croatia-vs-montenegro/` — full template with all components
- `compare/lisbon-vs-barcelona/` — recent FAQ-8→16 expansion example (PR #697)
- `compare/sicily-vs-sardinia/` — recent FAQ-8→16 expansion (PR #702)

## Common gotchas
- **JS string-quoting in fallbacks:** when writing the Personalize `recommendations` / `fallbacks` JS strings, never use unescaped double-quotes inside the value. Use `&lsquo;`/`&rsquo;` smart quotes or `&#39;` instead.
- **FAQ count off-by-one is the most common failure:** `score_compare.py` counts both `class="faq-item"` and `itemtype="Question"`. After adding "8 new items" to a 7-item FAQ, often lands at 15 not 16 — add one more. Pages with `itemtype="https://schema.org/Question"` on each faq-item count each one twice (visible item + itemtype = 2× count); these are easier to satisfy. **Verify after every FAQ expansion** before the score gate.
- **For FAQ=7 pages, plan to add 9 visible + 9 JSON-LD entries** (not 8) to safely land at 16. For FAQ=8 pages, 8 visible + 8 JSON-LD entries should land at 16 — but verify, since some pages double-count and end up at 17.
- **Quick Answers anchor IDs:** must point to existing IDs in the body. Run `grep -oE 'id="[a-z-]+"' <file> | sort -u` first to find real targets. **Don't reuse the same anchor for all 6 cards** — score gate flags broken anchors.
- **section-winner replacement is not optional:** even pages where you forget to do it will score lower (5/5 tabiji-verdict points lost). The `replace_all` is harmless if no occurrences exist (returns "0 changes").
- **`git checkout main` may fail** with "main is already used by worktree" — use `git checkout -b <new> origin/main` instead.
- **`gh pr merge --squash --delete-branch` may fail** with the same worktree error but the merge usually still succeeds remotely. Verify with `gh pr view <#> --json state,mergedAt`. PRs that say "Pull request was already merged" mean the merge succeeded — proceed.
- **Pages with both ux-cost-table AND ux-weather-table:** remove together in one Edit call, since they're sequential blocks.
- **Some pages have NO duplicate ux-cost-table/ux-weather-table** — skip that step on those pages.
- **Edit tool placeholder mistake:** when crafting the QA + Personalize + Scorecard block, write the entire block in one Edit, don't insert intermediate "REPLACE_THIS_SLOT" placeholders — the Edit tool literally inserts whatever you give it.
- **`&amp;amp;` encoding** is now in approximately every page that has related-card descriptions — always run `replace_all '&amp;amp;' → '&amp;'` early in workflow.
- **Base-branch-modified merge errors:** if `gh pr merge` returns "Base branch was modified", just retry the same command — usually succeeds on second attempt.

## Standard insertion block structure (refer to recent PRs for full content)
The QA + Personalize + Scorecard block (~10K tokens of HTML/JS) goes between `</div>` closing photo-grid and `<div class="verdict-box">`. Three sections in order:

1. `<section class="quick-answers">` — 6 `<a class="qa-card" href="#anchor-id">` cards, each with `qa-q` / `qa-a` / `qa-winner` divs
2. `<section class="personalize-widget">` — 3 pill groups (style, budget, priority) × 12+ keyed recommendations, plus fallback messages, plus a small JS handler
3. `<section class="visual-scorecard">` — 9 `sc-row` entries with bars + `sc-winner`

Use existing `id="..."` body anchors for QA cards; use 4 priorities × 3 styles × 3 budgets = 36 recommendations in the Personalize widget for full coverage.

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

## Pages currently at top of queue (as of 2026-04-26 end of session)
**Regenerate queue with the script below.** Likely-next high-impact pages:
- san-diego-vs-los-angeles (63, faq=16)
- san-francisco-vs-new-york (63, faq=16)
- san-francisco-vs-seattle (63, faq=16)
- bangkok-vs-ho-chi-minh (61, faq=8) — needs FAQ expansion
- london-vs-amsterdam (61, faq=8) — needs FAQ expansion
- tokyo-vs-london (61, faq=8) — needs FAQ expansion
- (likely 700+ more sub-100 pages remain after regen — most at 63&ndash;75)

(Regenerate queue before starting — these may be slightly different by then.)

### MED tier template note
Many pages now have a different MED tier template structure where the photo-grid is followed by blank lines (not directly by `<div class="verdict-box">`). When inserting QA + Personalize + Scorecard sections, the anchor for the Edit becomes `<div class="caption">DEST_NAME</div>\n</div>\n</div>` followed by blank lines — NOT followed by `<div class="verdict-box">`. **Don't accidentally inject a duplicate verdict-box opening.** If you see `class="verdict-box"` already at line 0/9 audit, that means the page is MED tier and already has the verdict marker.

## Session productivity stats
- **Session 1 (long):** 33 pages
- **Session 2 (resume):** 15 pages
- **Session 3 (10-page batch):** 10 pages
- **Session 4 (26-page batch):** 26 pages
- **Session 5 (25-page batch):** 25 pages
- **Session 6 (7-page batch from "21 more pages" request):** 7 pages
- **Session 7 (24-page batch):** 24 pages
- **Session 8 (24-page batch, continuing 100-page goal):** 24 pages
- **Session 9 (2-page test of cron skill before remote disabled):** 2 pages (bangkok-vs-ho-chi-minh, london-vs-amsterdam)
- **Session 10 (10-page batch, manual local resumption after cron failure):** 10 pages
  - tokyo-vs-london (FAQ-8 expansion), san-diego-vs-los-angeles, san-francisco-vs-new-york, san-francisco-vs-seattle, santorini-vs-amalfi-coast, scottsdale-vs-palm-springs, serengeti-vs-masai-mara, slovakia-vs-czech-republic
- **Total:** 192 pages at 100/100 (out of 916 total compare pages, 21.0%)

The pattern stabilizes around 5-7 minutes per page once the page already has FAQ=16, and 10-15 minutes for pages requiring FAQ expansion 7→16 or 8→16. The single most common failure is FAQ off-by-one (target 16, often lands at 15 — verify before commit).

## Context-pressure tradeoff observation
Each FAQ-expansion page consumes ~10-15K tokens of context (large QA+Personalize+Scorecard insertion + 8 new FAQ entries × 2 for visible+JSON-LD + frequent off-by-one re-runs). Pages already at FAQ=16 only consume ~6-8K tokens. **For long batch sessions, prefer FAQ=16 pages first to maximize throughput** — when the queue mixes both types, sort by FAQ=16 first within the same score bucket.
