#!/usr/bin/env python3
"""Convert <span class="filter-chip" ...>X</span> to <button type="button" ...>X</button>.

Filter chips have to be keyboard-focusable + activatable with Enter/Space.
Spans are not, so we swap to <button>. Visual styling comes from the existing
per-leaf inline `.filter-chip` rules; the global CSS shim in shared-shell.css
handles the browser-default button reset.

Match shape (single-line, no nested tags inside chip text):
    <span class="filter-chip" data-filter-group="..." data-filter-value="...">TEXT</span>

Only the class-as-sole-attribute prefix `<span class="filter-chip"` is targeted
to avoid colliding with any future multi-class spans.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Greedy on attrs (between class="filter-chip" and the closing >) but
# non-greedy on inner text so we don't span across chips.
CHIP_RE = re.compile(
    r'<span class="filter-chip"([^>]*)>([^<]*)</span>'
)


def convert(text: str) -> tuple[str, int]:
    new_text, n = CHIP_RE.subn(
        r'<button type="button" class="filter-chip"\1>\2</button>',
        text,
    )
    return new_text, n


def tracked_html_files() -> list[Path]:
    out = subprocess.check_output(
        ["git", "ls-files", "*.html"], cwd=ROOT, text=True
    )
    return [ROOT / p for p in out.splitlines() if p]


def main() -> None:
    files_changed = 0
    chips_converted = 0
    for path in tracked_html_files():
        try:
            text = path.read_text()
        except (OSError, UnicodeDecodeError):
            continue
        if 'class="filter-chip"' not in text:
            continue
        new_text, n = convert(text)
        if n == 0 or new_text == text:
            continue
        path.write_text(new_text)
        files_changed += 1
        chips_converted += n
    print(f"converted {chips_converted} chips across {files_changed} files")


if __name__ == "__main__":
    main()
