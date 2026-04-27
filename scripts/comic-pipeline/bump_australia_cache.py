#!/usr/bin/env python3
"""After the 2026-04-27 Australia regen, bump the cache-bust query string on
the 16 regenerated `<img>` tags so Cloudflare CDN serves the new R2 object
instead of the cached miniature.

Pattern per pipeline.md: append `?v=2` (or higher) to the img `src` when the
R2 object is overwritten — R2 is fronted by Cloudflare CDN which doesn't
invalidate on PUT.

Idempotent: if `?v=N` is already present, bumps to `?v=N+1`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from regen_australia_audit_2026_04_27 import TARGETS  # noqa: E402

REPO = _HERE.parent.parent


def bump_one(city: str, n: int) -> tuple[bool, str]:
    path = REPO / f"scams/{city}/index.html"
    html = path.read_text()
    pat = re.compile(
        rf'(src="https://img\.tabiji\.ai/scams/{re.escape(city)}/scam-{n}\.jpg)(\?v=(\d+))?(")'
    )
    m = pat.search(html)
    if not m:
        return False, "no img tag found"
    current = int(m.group(3)) if m.group(3) else 1
    new = current + 1
    replacement = f'{m.group(1)}?v={new}{m.group(4)}'
    new_html = pat.sub(replacement, html, count=1)
    if new_html == html:
        return False, "substitution was a no-op"
    path.write_text(new_html)
    return True, f"v={current} → v={new}"


def main() -> int:
    changed = skipped = 0
    for city, scams in TARGETS.items():
        for n in scams:
            ok, note = bump_one(city, n)
            tag = "OK" if ok else "SKIP"
            print(f"  [{tag}] {city}/scam-{n}  {note}")
            if ok:
                changed += 1
            else:
                skipped += 1
    print(f"\nBumped {changed}, skipped {skipped}")
    return 0 if skipped == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
