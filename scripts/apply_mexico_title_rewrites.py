#!/usr/bin/env python3
"""Apply 114 Mexico title rewrites from /tmp/mexico-title-rewrite.txt.

Titles appear in multiple places per page:
  - <div class="scam-title">TITLE</div>
  - TOC entry: <a href="#scam-N">...TITLE</a>
  - img alt="TITLE — comic illustration"
  - Key Takeaways "The #1 reported scam is the {TITLE}"
  - meta description / og:description (first scam, sometimes)
  - twitter:description "Hard-won X travel safety: TITLE-1, TITLE-2, ..."

Strategy: full-text exact-string replace. Each old title is unique enough
that there are no collisions in the file. Also replaces in JSON-LD
structured data and any HTML-escaped variant (& → &amp;).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RW_PATH = Path("/tmp/mexico-title-rewrite.txt")


def parse_rewrites() -> dict[str, list[tuple[int, str, str, str]]]:
    """Returns {city: [(n, old, new, reddit), ...]}."""
    out: dict[str, list[tuple[int, str, str, str]]] = {}
    current_city: str | None = None
    pending: dict[int, dict[str, str]] = {}
    for raw in RW_PATH.read_text().splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("=== ") and line.endswith(" ==="):
            if current_city and pending:
                out[current_city] = sorted(
                    [(n, d["OLD"], d["NEW"], d["REDDIT"]) for n, d in pending.items()]
                )
            current_city = line.strip("= ").strip()
            pending = {}
            continue
        m = re.match(r"^(\d+)\|(OLD|NEW|REDDIT):\s*(.+)$", line)
        if not m or current_city is None:
            continue
        n = int(m.group(1))
        key = m.group(2)
        val = m.group(3).strip()
        pending.setdefault(n, {})[key] = val
    if current_city and pending:
        out[current_city] = sorted(
            [(n, d["OLD"], d["NEW"], d["REDDIT"]) for n, d in pending.items()]
        )
    return out


def html_escape(s: str) -> str:
    return s.replace("&", "&amp;")


def apply_to_file(path: Path, rewrites: list[tuple[int, str, str, str]]) -> int:
    html = path.read_text()
    edits = 0
    for n, old, new, _reddit in rewrites:
        # Try unescaped first, then HTML-escaped
        for old_s, new_s in [(old, new), (html_escape(old), html_escape(new))]:
            count = html.count(old_s)
            if count:
                html = html.replace(old_s, new_s)
                edits += count
    path.write_text(html)
    return edits


def main():
    parsed = parse_rewrites()
    print(f"parsed {len(parsed)} cities")
    total = 0
    for city, rws in sorted(parsed.items()):
        path = REPO / f"scams/{city}/index.html"
        if not path.exists():
            print(f"  SKIP {city}: no file")
            continue
        edits = apply_to_file(path, rws)
        print(f"  {city}: {len(rws)} title rewrites, {edits} string replacements")
        total += edits
    print(f"\nTotal: {total} replacements across {len(parsed)} cities")


if __name__ == "__main__":
    main()
