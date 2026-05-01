#!/usr/bin/env python3
"""After regen, bump cache-bust query string on the 33 regenerated img tags only.

Pattern per pipeline.md: append `?v=2` (or higher) to the `src` when the R2
object is overwritten — R2 is fronted by Cloudflare CDN which doesn't
invalidate on PUT.

Idempotent: if `?v=2` is already present, bumps to `?v=3` etc.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from regen_indonesia import FLAGGED  # noqa: E402

REPO = _HERE.parent.parent


def bump_one(city: str, n: int) -> tuple[bool, str]:
    path = REPO / f"scams/{city}/index.html"
    html = path.read_text()
    # Match only THIS city's scam-N.jpg src (with or without existing ?v=...)
    pat = re.compile(
        rf'(src="https://img\.tabiji\.ai/scams/{re.escape(city)}/scam-{n}\.jpg)(\?v=(\d+))?(")'
    )
    m = pat.search(html)
    if not m:
        return False, "no img tag found"
    current = int(m.group(3)) if m.group(3) else 1  # no ?v= means v1
    new = current + 1
    replacement = f'{m.group(1)}?v={new}{m.group(4)}'
    new_html = pat.sub(replacement, html, count=1)
    if new_html == html:
        return False, "substitution was a no-op"
    path.write_text(new_html)
    return True, f"v={current} → v={new}"


def main():
    changed = skipped = 0
    for city, n, reason in FLAGGED:
        ok, note = bump_one(city, n)
        tag = "OK" if ok else "SKIP"
        print(f"  [{tag}] {city}/scam-{n}  [{reason}]  {note}")
        if ok:
            changed += 1
        else:
            skipped += 1
    print(f"\nChanged: {changed}  Skipped: {skipped}  Total: {len(FLAGGED)}")


if __name__ == "__main__":
    main()
