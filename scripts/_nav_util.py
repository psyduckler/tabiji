"""Shared nav HTML loader for build scripts.

Reads `_includes/nav-main.html` as the single source of truth so build
scripts don't each carry a hardcoded copy of the nav block. The returned
string includes the `@include:nav:start/end` marker comments, which means
generated pages will be picked up by `scripts/build-partials.py` for
future syncs.

Consumers in `scripts/` can import directly. Consumers elsewhere need a
small `sys.path` insert first — see `scams/generate_pages.py` and
`functions/build-travel-alerts.py` for the pattern.
"""
from pathlib import Path

_NAV_PATH = Path(__file__).resolve().parents[1] / "_includes" / "nav-main.html"
_cached = None


def get_nav_html():
    global _cached
    if _cached is None:
        _cached = _NAV_PATH.read_text(encoding="utf-8").strip()
    return _cached
