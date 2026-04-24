# Refactor brief — decouple partial sync from commits

**Date:** 2026-04-17
**Author:** Claude (session with bjh)
**Status:** Proposal — not yet approved

---

## Problem

Every commit to the repo currently runs `scripts/build-partials.py` via the `pre-commit` hook, then force-adds every HTML file with `git add '*.html'`. This means:

- **Every commit potentially touches 8,248 HTML files** (~341 MB of tracked HTML). Real session observed: a single-file `git add scams/research/title-ctr-experiment-2026-04-17.md` produced a commit touching **4,930 files** (one research doc + 15 intentional edits + 4,914 nav-partial sync).
- **Cross-actor merges conflict on files neither actor meaningfully touched.** In today's session merging 17 upstream commits into a branch with 15 intentional scam-page edits produced **24 merge conflicts** — 15 of them on files neither the upstream commits nor the local branch had any real business touching (Cartagena rebuilds conflicted with my nav-sync output, not my real changes).
- **Commit history is unreviewable.** `git log --stat` on a "fix one bug" commit shows thousands of nav-partial lines that drown out the actual change.
- **Failed commits leave 300+ dirty files.** The starting git status for this session had 300+ modified files that were output from a previous aborted commit's hook run — too many to confidently untangle from incoming real work.

## Goals

1. **Authors commit only what they changed.** A 1-file logical change = a 1-file diff in the commit.
2. **Nav/footer/head stays in sync** across every HTML page in production without manual effort.
3. **Cross-actor merges don't conflict on partial sync.** Two parallel changes to unrelated pages should merge cleanly.
4. **Existing hook protections (itinerary hero-bg check) stay intact.**
5. **No visible regression** — every deployed page has the same rendered nav/footer/head as today.

## Root cause

The `pre-commit` hook confuses two responsibilities: **enforcing invariants** (e.g., "itineraries must have hero-bg") vs. **propagating updates to managed blocks**. Invariants belong at commit time — they fail fast. Propagation belongs at deploy time — it only matters for what's served.

Mixing them means every commit pays the propagation cost, and any propagation failure/conflict blocks commits unrelated to partials.

## Options considered

### Option A — Move sync to `post-commit` with auto-follow-up commit
Pre-commit becomes invariant-only (keep the itinerary hero-bg check). Add a `post-commit` hook that runs `build-partials.py` and, if anything changed, creates a follow-up commit like `chore: sync partials`.

- **Pros:** Tiny change. "Always in sync" guarantee preserved. Feature commits are clean.
- **Cons:** Still produces huge sync commits (just separated). Cross-actor merges still conflict on sync output. Post-commit hooks can confuse tooling ("why are there extra commits?").
- **Effort:** ~1 hour. Low risk.

### Option B — Move sync to CI (GitHub Actions) or a nightly job
Remove sync from the local hook entirely. A workflow on `push` to main runs `build-partials.py`, opens a PR or auto-commits if anything's out of sync.

- **Pros:** Authors' local flow is clean and fast. No cross-actor conflicts on nav. Runs centrally with auditable history.
- **Cons:** Requires adding CI infra (none exists — no `.github/workflows/`). Brief window where `main` has un-synced partials between push and CI run. Needs a token with push-back-to-main permission.
- **Effort:** ~3–4 hours (workflow file, token setup, first full sync commit). Medium risk (depends on whether push-back to main is acceptable to other actors).

### Option C — Build partials at deploy time (Cloudflare Pages build command)
`REFACTOR-BRIEF.md` confirms deploy is Cloudflare Pages auto-building from `main`. Set the CF Pages **Build command** to `python3 scripts/build-partials.py`. Commit only marker placeholders (`<!-- @include:nav:start --><!-- @include:nav:end -->`) — the source HTML in git is "skeleton," the deployed output has full partials injected.

- **Pros:** Zero sync commits, ever. Nav change = 1-file PR. Impossible for git to drift from deployed state. Merge conflicts on nav cease to exist. Uses existing deploy infra — no new CI system.
- **Cons:** Biggest blast radius — a migration commit that "empties" nav content in 5,610 files. Local HTML viewed without a build step shows empty nav (`python3 scripts/build-partials.py` must be run locally before opening files). Requires CF Pages dashboard change (one-time).
- **Effort:** ~1 day (migration script + CF config + smoke-test of a few URLs post-deploy + write `scripts/dev-build.sh` for local dev). Medium-high risk (one-shot big migration).

### Option D — Client-side include (fetch + inject)
Replace nav block in every HTML with a placeholder div + `<script>fetch('/partials/nav.html')...</script>`.

- **Pros:** Zero sync, ever. Simple.
- **Cons:** FOUC on every page load. CLS regression (hurts Core Web Vitals / SEO). Nav links load via JS — Google renders JS so nav links are still crawlable, but it's weaker signal than static HTML. Breaks for users with JS disabled.
- **Effort:** ~4 hours. Low implementation risk but **high SEO risk** for a site whose primary channel is organic search.
- **Verdict:** Not recommended given tabiji's dependence on organic traffic.

## Recommendation

**Phase 1 — Option A now** (~1 hour). Cheapest de-risking step:
- Move partial sync from `pre-commit` → `post-commit` (or run it manually / via `scripts/dev-build.sh`).
- Keep `pre-commit` for invariants only (itinerary hero-bg check + optional light validation).
- Removes the hardest friction (giant auto-fattened commits) with minimal infra change.

**Phase 2 — Option C within 1–2 weeks** (~1 day). The right long-term answer:
- Configure Cloudflare Pages to run `python3 scripts/build-partials.py` as the build step.
- One migration commit reduces all 5,610 HTML files to marker placeholders.
- All future nav/footer/head changes become 1-file PRs touching only the partial source.
- Local dev: `scripts/dev-build.sh` runs the same script against the working tree so local preview matches prod.

**Skip Option B** (CI). Redundant with CF Pages' existing build step and adds a new system to maintain.

**Skip Option D** (client-side). SEO risk is disproportionate to the benefit.

---

## Migration plan

### Phase 1 — Hook split (1 hour)

1. Edit `.githooks/pre-commit`:
   - Remove lines 5–9 (the `build-partials.py` run + force `git add '*.html'`).
   - Keep lines 11–42 (itinerary hero-bg enforcement).
2. Create `.githooks/post-commit` — runs `build-partials.py`, and if anything changed, exits with a warning telling the committer to `git add -A && git commit -m 'chore: sync partials'` (don't auto-commit in post-commit; it causes recursion). Give them the exact command to copy-paste.
3. Add `scripts/dev-build.sh` wrapper for explicit runs.
4. Update `CLAUDE.md` / `REFACTOR-BRIEF.md` with the new workflow.
5. Tell the other Claude-Code actors / the human author about the change (commits now require an explicit sync step if nav changed).

**Exit criterion:** Next commit that touches a single file produces a 1-file diff.

### Phase 2 — Deploy-time build (1 day)

1. **Local dry run:** Run `build-partials.py` with output to a scratch dir (not in-place), diff against current state, confirm output is byte-identical to what's currently on disk.
2. **CF Pages config:** Set Build command to `python3 scripts/build-partials.py` in the Cloudflare dashboard. Set Python version if needed. Test with a PR deploy first (CF Pages supports preview deployments per branch).
3. **Verify preview:** Pick 5–10 representative URLs (home, a scam page, a compare page, a popular-picks page, an itinerary under `/i/`). Confirm nav/footer/head render identically to production.
4. **Migration commit:** Run a "skeletonize" script that replaces all managed blocks in-tree with marker-only placeholders. This is one big commit (probably 5,610 files), but it's the LAST sync-shaped commit.
5. **Ship Phase 2:** Merge to main. CF Pages auto-builds → partials inject at build time → deployed site matches pre-migration.
6. **Add local dev story:** `scripts/dev-build.sh` syncs partials into working tree for local HTML preview. `.gitignore` does not need changes because `build-partials.py` writes back to the same files.

**Exit criterion:** A commit changing `_includes/nav-main.html` is 1 file, and the deployed site shows the new nav.

---

## Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Phase 2 breaks prod (broken partial injection on deploy) | Low | High | CF Pages preview deployment + side-by-side diff of 10 URLs before merge. |
| Local authors view skeleton HTML instead of rendered (empty nav in browser when opening a file directly) | Medium | Low | `scripts/dev-build.sh` + document in REFACTOR-BRIEF.md. For most tabiji work the dev loop is "edit → commit → CF preview URL" anyway, not local file view. |
| Python not available in CF Pages build env | Low | High | Verify in docs; fallback is adding a `requirements.txt` or pinning Python version in CF dashboard. CF Pages supports Python. |
| Migration commit has an error on a handful of files (regex miss) | Medium | Low | Dry-run the skeletonize script, diff output vs current, manually inspect diffs that don't match expected pattern before committing. |
| Other actors / scripts (e.g., `fulfill-order.js`) assume partials are already inlined in HTML | Medium | Medium | Audit all scripts that read HTML files — they may parse nav. Check `fulfill-order.js`, `add-related-links.js`, anything touching HTML DOM. |
| Third-party tools (SEO auditors, sitemap generators) assume static-rendered HTML | Low | Low | Deployed HTML is still static rendered; only the git-stored copy is a skeleton. External tools see final HTML. |

## Rollback

- **Phase 1:** Revert the hook change — 1 commit, one-line flip.
- **Phase 2:** Revert the skeletonize migration commit + flip CF Pages build command back to empty. Because `build-partials.py` is idempotent and reads the same partial sources, reverting the skeleton commit re-inlines everything.

## Success metrics (90 days post-Phase 2)

- Average commit size: from ~4,000 files → <10 files (excluding intentional batch operations).
- Merge conflicts on nav/footer/head across cross-actor PRs: **0** per month (vs. observed 24 conflicts in a single merge today).
- Time from "author decides to change nav" → "nav changed on prod": from "depends who merges first" → deterministic single PR.

## Open questions for the human

1. Are there other actors (human contributors, scheduled bots) who rely on the current "commit = everything stays synced" behavior?
2. Is the Cloudflare Pages build allowed to run Python? (Known yes per CF docs, but needs confirmation in this account.)
3. Any existing scripts that `git diff` HTML files expecting inlined nav? (Quick audit needed.)
