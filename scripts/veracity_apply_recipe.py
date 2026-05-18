#!/usr/bin/env python3
"""
Apply the veracity-experiment treatment recipe to a /compare/{slug}/index.html
page. Recipe = findings #1 + #2 + #4 + #5 from the Round 1 Veracity audit
(see docs/veracity-experiment.md).

  #1 generic_phrasing      — strip "shines / sheer X / excels / boasts / unparalleled"
  #2 hedging_and_absolutes — de-templatize "While X share Y, Z excels in W"
  #4 weak_provenance       — delete paraphrased attributions
                              ('"<quote>", a/an/another <noun> <verb>')
  #5 repetitive_structure  — convert tabiji-verdict <ul><li>Winner/Why/Who</li></ul>
                              to varied prose (cycle 4 patterns within a page)

Usage:
    python3 scripts/veracity_apply_recipe.py <slug>
    python3 scripts/veracity_apply_recipe.py --all-treated   # all 19 pages
    python3 scripts/veracity_apply_recipe.py --dry-run <slug>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
COHORT_ASSIGN = REPO_ROOT / "docs" / "data" / "veracity-experiment" / "cohort-assignment.json"


# ─────────────────────────────────────────────────────────────────────────────
# #1 generic_phrasing — strip templated intensifiers
# ─────────────────────────────────────────────────────────────────────────────
# Replacements are designed to remove the templated word and leave grammatical
# prose around it. Order matters — multi-word patterns first to avoid double-edits.
GENERIC_PHRASING_RULES = [
    # "X shines with its sheer variety of Y" → "X has its varied Y"
    (re.compile(r"\bshines with its sheer variety of\b"), "has its varied"),
    (re.compile(r"\bshines with its sheer ([a-z]+) of\b"), r"has its \1 of"),
    (re.compile(r"\bshines with\b"), "has"),
    (re.compile(r"\bshines for\b"), "works for"),
    (re.compile(r"\bshines in\b"), "is strongest in"),
    (re.compile(r"\bshines\b"), "stands out"),
    # "sheer volume/variety/scale/size of X" → just X
    (re.compile(r"\bsheer volume of\b"), "total count of"),
    (re.compile(r"\bsheer variety of\b"), "varied"),
    (re.compile(r"\bsheer scale of\b"), "count of"),
    (re.compile(r"\bsheer size of\b"), "size of"),
    (re.compile(r"\bsheer (size|scale|number|range|breadth)\b"), r"\1"),
    # "excels" — replace with concrete verb
    (re.compile(r"\bexcels in its preferred niche\b"), "fits its preferred travel style"),
    (re.compile(r"\bexcels in\b"), "is strongest at"),
    (re.compile(r"\bexcels for\b"), "fits"),
    (re.compile(r"\bexcels at\b"), "is strongest at"),
    (re.compile(r"\bexcels\b"), "is the pick"),
    # "boasts" — replace with neutral verb
    (re.compile(r"\bboasts of\b"), "has"),
    (re.compile(r"\bboasts\b"), "has"),
    # "unparalleled" — usually generic intensifier
    (re.compile(r"\bunparalleled diversity\b"), "notable diversity"),
    (re.compile(r"\bunparalleled\b"), "distinctive"),
]


def apply_generic_phrasing(text: str) -> tuple[str, int]:
    n = 0
    for pat, repl in GENERIC_PHRASING_RULES:
        new, k = pat.subn(repl, text)
        n += k
        text = new
    return text, n


# ─────────────────────────────────────────────────────────────────────────────
# #2 hedging_and_absolutes — de-templatize "While X share Y, Z excels/has/offers W"
# ─────────────────────────────────────────────────────────────────────────────
# Strict scope: only the clearest hedge→absolute construction where "While" is
# followed by "both" / "the X" sharing something, then a contrast clause with an
# absolute verb. Most "While X is true..." constructions are concessive prose
# that's fine.
HEDGE_ABSOLUTE_RULES = [
    # "While both islands/countries/cities share a ..., X is the pick in/has/offers..."
    # After #1 above, "excels" was already turned into "is the pick" — so we
    # mainly need to de-comma the "While ... , X ..." structure.
    (re.compile(
        r"\bWhile both (islands|countries|cities|destinations|locations) share a (deep |strong |rich |long )?([a-z]+ )?(history|past|heritage|tradition|background), "
    ), r"Both \1 share a \3\4. "),
    # "While X has Y, Z is the pick in W" → "X has Y. Z is the pick in W."
    # Skip for now — too risky to mass-apply without per-page judgment.
]


def apply_hedge_absolute(text: str) -> tuple[str, int]:
    n = 0
    for pat, repl in HEDGE_ABSOLUTE_RULES:
        new, k = pat.subn(repl, text)
        n += k
        text = new
    return text, n


# ─────────────────────────────────────────────────────────────────────────────
# #4 weak_provenance — delete paraphrased attributions
# ─────────────────────────────────────────────────────────────────────────────
# Patterns to find+delete:
#   "..." , (a|an|another|one) <up-to-3-words> <verb> [, <follow-up clause>] .
# Where verb ∈ {noted, said, shared, mentioned, loved, praised, wrote, reported,
#               recommended, warned, complained, added, observed, remarked,
#               stated, commented, claimed, declared}.
# Also catches "Conversely, another loved 'X.'" patterns.

ATTR_VERBS = (
    "noted|said|shared|mentioned|loved|praised|wrote|reported|recommended|"
    "warned|complained|added|observed|remarked|stated|commented|claimed|declared"
)

ATTR_RE = re.compile(
    # Optional leading space, then the quoted material (with trailing punct
    # variants), then the attribution clause
    r'\s*"[^"]{15,400}"[\s,]*'
    r'(a |an |another |one )'
    r'[a-z\-]+(?:\s+[a-z\-]+){0,2}\s+'
    r'(' + ATTR_VERBS + r')'
    # Optional trailing "highlighting the X" / "underscoring the Y" tail clause
    r'(?:,?\s+(highlighting|underscoring|capturing|reflecting|noting)[^."<]{0,180})?'
    r'\.?',
    re.IGNORECASE,
)

# Also catches "Conversely, another loved/praised 'X.'"
CONVERSELY_RE = re.compile(
    r'(?:Conversely,|Meanwhile,)?\s+another\s+(loved|praised|noted|added|liked)\s+"[^"]{10,300}"\.?',
    re.IGNORECASE,
)


def apply_provenance(text: str) -> tuple[str, int]:
    n_total = 0
    new, k = ATTR_RE.subn("", text)
    n_total += k
    new, k = CONVERSELY_RE.subn("", new)
    n_total += k
    # Clean up stranded double-spaces from deletions
    new = re.sub(r"  +", " ", new)
    # Fix stranded sentence-end glitches
    new = re.sub(r"\s+\.([<\s])", r".\1", new)
    return new, n_total


# ─────────────────────────────────────────────────────────────────────────────
# #5 repetitive_structure — restructure tabiji-verdict blocks
# ─────────────────────────────────────────────────────────────────────────────
# Two known variants seen across compare pages:
#   v1: <div class="tabiji-verdict"><strong>tabiji verdict:</strong> <ul>...</ul></div>
#   v2: <div class="tabiji-verdict"><h3>Winner takeaway</h3><ul>...</ul></div>
VERDICT_RE = re.compile(
    r'<div class="tabiji-verdict">'
    r'(?:<strong>tabiji verdict:</strong> |<h3>[^<]+</h3>)'
    r'<ul>'
    r'<li><strong>Winner:</strong>\s*(?P<winner>[^<]+)</li>'
    r'<li><strong>Why:</strong>\s*(?P<why>[^<]+)</li>'
    r'<li><strong>Who this matters for:</strong>\s*(?P<who>[^<]+)</li>'
    r'</ul>'
    r'</div>',
    re.DOTALL
)
# Replacement always uses the v1 prefix/suffix — normalizes the variants.
VERDICT_PREFIX = '<div class="tabiji-verdict"><strong>tabiji verdict:</strong>'
VERDICT_SUFFIX = '</div>'


def _clean(s: str) -> str:
    return s.strip().rstrip(".").rstrip()


def restructure_verdict(idx: int, winner: str, why: str, who: str) -> str:
    winner = winner.strip()
    why = _clean(why).strip()
    who = _clean(who).strip()
    is_tie = winner.lower() in ("tie", "tied")

    if is_tie:
        # Tie pattern — 2 variants cycled
        if idx % 2 == 0:
            body = f"Tie. {why}. The right pick depends on travel style."
        else:
            body = f"It's a tie — {why}. Either works depending on what you want."
    else:
        # 4 patterns cycled for non-tie verdicts. Each writes Winner/Why/Who in a
        # different sentence order to prevent Veracity from learning the new pattern.
        pattern = idx % 4
        if pattern == 0:
            body = f"{winner}. {why}. Best for {who}."
        elif pattern == 1:
            body = f"{why} — that's why {winner} takes this. For {who}, it matters most."
        elif pattern == 2:
            body = f"For {who}, {winner} is the pick: {why}."
        else:
            body = f"{winner} wins here. {why}. {who} will benefit most."
    return f"{VERDICT_PREFIX} {body}{VERDICT_SUFFIX}"


def apply_verdict_restructure(html: str) -> tuple[str, int]:
    # Use a stateful counter to cycle pattern indexes within a page
    counter = {"i": 0}

    def _sub(m):
        i = counter["i"]
        counter["i"] += 1
        return restructure_verdict(
            i,
            winner=m.group("winner"),
            why=m.group("why"),
            who=m.group("who"),
        )

    new_html, n = VERDICT_RE.subn(_sub, html)
    return new_html, n


# ─────────────────────────────────────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────────────────────────────────────
def apply_recipe_to_html(html: str) -> tuple[str, dict]:
    counts = {}
    html, counts["generic_phrasing"] = apply_generic_phrasing(html)
    html, counts["hedge_absolute"] = apply_hedge_absolute(html)
    html, counts["provenance"] = apply_provenance(html)
    html, counts["verdict_restructure"] = apply_verdict_restructure(html)
    return html, counts


def apply_to_slug(slug: str, dry_run: bool = False) -> dict:
    path = REPO_ROOT / "compare" / slug / "index.html"
    if not path.exists():
        raise SystemExit(f"page not found: {path}")
    html = path.read_text(encoding="utf-8")
    new_html, counts = apply_recipe_to_html(html)
    delta_chars = len(new_html) - len(html)
    if not dry_run:
        path.write_text(new_html, encoding="utf-8")
    return {"slug": slug, "counts": counts, "delta_chars": delta_chars}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--all-treated", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.all_treated:
        assign = json.loads(COHORT_ASSIGN.read_text())
        treated = [r["slug"] for r in assign["treated"]]
        results = []
        for slug in treated:
            results.append(apply_to_slug(slug, dry_run=args.dry_run))
        for r in results:
            print(f"  {r['slug']:<42} #1={r['counts']['generic_phrasing']:>3}  "
                  f"#2={r['counts']['hedge_absolute']:>2}  "
                  f"#4={r['counts']['provenance']:>3}  "
                  f"#5={r['counts']['verdict_restructure']:>3}  "
                  f"Δchars={r['delta_chars']:+d}")
        total = {k: sum(r["counts"][k] for r in results) for k in results[0]["counts"]}
        print(f"\nTOTAL across {len(results)} pages: {total}")
        return 0

    if not args.slug:
        raise SystemExit("usage: <slug> | --all-treated [--dry-run]")
    r = apply_to_slug(args.slug, dry_run=args.dry_run)
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
