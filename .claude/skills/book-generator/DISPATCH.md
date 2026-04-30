# Book Generator — Dispatch

When this skill fires, start here.

## 0. Triage

Ask (or infer) 3 things before Phase 1:

1. **Country slug + ISO code** — e.g., `germany` / `DE`. Required.
2. **Scope intent** — is it the whole country, or a subset (mainland only, main islands only, etc.)? Default: whole country.
3. **Volume number** — look at `books/index.html` Schema.org `hasPart` and count the current live books. Next volume = count + 1. (As of 2026-04-20: last live volume is Canada = Vol 10, so next is Vol 11.)

Don't ask if you can infer from context. If the user said "build Germany book" the slug + ISO + scope are obvious.

## 1. Open the playbook

Read **`book-generator.md`** (the main skill file, one directory up from this one) for the full 10-phase workflow. That file is the canonical source.

## 2. Reference files to have open

- `templates/config.yaml.template` — copy + fill in
- `templates/manuscript/*.template` — 10 manuscript skeletons
- `templates/scripts/*.py.template` — 6 Python scripts to copy verbatim into `book-<country>/` — includes `polish_scam_prose.py.template` which the build.py MUST import (see gotcha #16)
- `templates/build-templates/{style.css,header-includes.tex}` — EPUB CSS + LaTeX override
- `checklists/publisher-audit-prompts.md` — three parallel-audit agent prompts
- `checklists/desktop-readme-template.txt` — the desktop bundle README skeleton
- `checklists/gotchas-and-known-fixes.md` — 24 known anti-patterns with fixes — **READ IF YOU HIT ANY ERROR, especially #16 (Reddit scaffolding/word-breaks demand the polish module), #17 (patch-script escape bugs when editing existing build.py), #18 (KDP twoside gutter), #19 (always copy from templates/, never another shipped book), #20 (cover-art silent strip — all 3 sub-bugs), #21 (cover-overlay tagline halo on light skies), #22 (stat-badge box width), #23 (front cover MUST be a comic-style scam-in-action scene — read prompt aloud), and #24 (`bleed_colors` synergy with cover art, picked AFTER render)**

## 3. Reference volumes to pattern-match against

Do not reinvent. Study one of these and port:

- **`book-turkey/`** — most recent canonical. Best if the new country has a non-Latin-1 currency symbol (Turkish ₺ fix pattern).
- **`book-spain/`** — best if the new country is Romance-language, Latin alphabet, European Ministry-priced attractions.
- **`book-china/`** — best if the new country uses a non-Latin script (Chinese, Thai, Hebrew, Arabic, Cyrillic) and needs xeCJK/polyglossia font support.
- **`book-indonesia/`** — best if the new country has multi-island geography + tropical-tourism scam scene.

## 4. Time budget

| Phase | Wall-clock (approx) | Can parallelize? |
|---|---|---|
| 1. Setup | 5 min | — |
| 2. Asset generation | 15 min background + 10 min download | Yes — kick off in background during Phase 3 |
| 3. Manuscript writing | 60-90 min | Yes — all 10 files in parallel Write calls |
| 4. 5x copyedit | 10 min | Single Python diagnostic script |
| 5. Initial build | 3 min | — |
| 6. 3 publisher audits | 4 min | Yes — three parallel Agent calls |
| 7. Apply fixes + rebuild | 20 min | Mostly sequential |
| 8. Site integration | 30 min | — |
| 9. Deploy | 10 min | — |
| 10. Ship | 5 min | — |

**Total wall-clock: ~2.5-3 hours from "build X book" to "PR merged + desktop folder ready."**

## 5. Don't

- Don't truncate early. The user committed to the full workflow when they invoked the skill.
- Don't skip the audits. Every book has caught 3-8 blocker-grade issues at the audit stage.
- Don't write an inferior version of a phase because it's "probably fine." Match the quality bar set by `book-spain/` and `book-turkey/`.
- Don't omit the desktop bundle. It's the user's hand-off asset for KDP upload.
