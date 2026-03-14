# Shared shell partials

Build command:

```bash
python3 scripts/build-partials.py
```

What it manages:

- `shared-head` → global shell assets
- `nav` → main site nav or export nav, depending on page family
- `footer` → one canonical footer (`footer-default.html`) used everywhere

Guardrails:

- `.githooks/pre-commit` runs `python3 scripts/build-partials.py` before commit and re-stages managed files
- `scripts/build-partials.py` refreshes managed blocks between explicit `@include:*` markers
- it backfills markers on legacy pages the first time it runs
- it fails if a page with `<head>`, `<nav>`, or `<footer>` is missing its managed block after build

Note:

- shared shell assets now use stable URLs instead of a hardcoded query-string version
