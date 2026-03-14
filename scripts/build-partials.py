#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCLUDES = ROOT / "_includes"

HEAD_START = "<!-- @include:shared-head:start -->"
HEAD_END = "<!-- @include:shared-head:end -->"
NAV_START = "<!-- @include:nav:start -->"
NAV_END = "<!-- @include:nav:end -->"
FOOTER_START = "<!-- @include:footer:start -->"
FOOTER_END = "<!-- @include:footer:end -->"

PARTIALS = {
    "shared-head": (INCLUDES / "shared-head.html").read_text(),
    "nav-main": (INCLUDES / "nav-main.html").read_text().strip(),
    "nav-export": (INCLUDES / "nav-export.html").read_text().strip(),
    "footer-default": (INCLUDES / "footer-default.html").read_text().strip(),
}

HTML_FILES = [
    p for p in ROOT.rglob("*.html")
    if ".git" not in p.parts
    and "node_modules" not in p.parts
    and not p.is_relative_to(INCLUDES)
]


def managed_block(start: str, content: str, end: str) -> str:
    return f"{start}\n{content}\n{end}"


def replace_or_insert(text: str, start: str, end: str, content: str, fallback_pattern: str | None = None, fallback_repl: str | None = None) -> tuple[str, bool]:
    block = managed_block(start, content, end)
    marker_re = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if marker_re.search(text):
        updated = marker_re.sub(block, text, count=1)
    elif fallback_pattern and fallback_repl is not None:
        fallback_re = re.compile(fallback_pattern, re.DOTALL)
        if fallback_re.search(text):
            updated = fallback_re.sub(fallback_repl, text, count=1)
        else:
            return text, False
    else:
        return text, False
    # Remove stray duplicate end markers left by earlier runs
    dup = f"{end}\n{end}"
    while dup in updated:
        updated = updated.replace(dup, end)
    return updated, updated != text


def nav_partial_for(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    if parts[0] in {"i", "itineraries"}:
        return PARTIALS["nav-export"]
    return PARTIALS["nav-main"]


def footer_partial_for(path: Path) -> str:
    return PARTIALS["footer-default"]


def process_file(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    original = path.read_text()
    text = original

    if rel.parts[0] == "export-doc":
        return False

    text, _ = replace_or_insert(
        text,
        HEAD_START,
        HEAD_END,
        PARTIALS["shared-head"].strip(),
        fallback_pattern=r"</head>",
        fallback_repl=managed_block(HEAD_START, PARTIALS["shared-head"].strip(), HEAD_END) + "\n</head>",
    )

    text, _ = replace_or_insert(
        text,
        NAV_START,
        NAV_END,
        nav_partial_for(path),
        fallback_pattern=r"<nav\b.*?</nav>",
        fallback_repl=managed_block(NAV_START, nav_partial_for(path), NAV_END),
    )

    if "<footer" in text:
        text, _ = replace_or_insert(
            text,
            FOOTER_START,
            FOOTER_END,
            footer_partial_for(path),
            fallback_pattern=r"<footer\b.*?</footer>",
            fallback_repl=managed_block(FOOTER_START, footer_partial_for(path), FOOTER_END),
        )

    if text != original:
        path.write_text(text)
        return True
    return False


def validate() -> None:
    unresolved = []
    missing = []
    for path in HTML_FILES:
        text = path.read_text()
        if "@include:" in text:
            for marker in re.findall(r"@include:[^:]+(?=:start|:end)?", text):
                if marker not in {"@include:shared-head", "@include:nav", "@include:footer"}:
                    unresolved.append((path, marker))
        if "<nav" in text and NAV_START not in text:
            missing.append((path, "nav"))
        if "<footer" in text and FOOTER_START not in text:
            missing.append((path, "footer"))
        if "</head>" in text and HEAD_START not in text:
            missing.append((path, "head"))
    if unresolved or missing:
        lines = []
        for path, marker in unresolved:
            lines.append(f"unresolved marker in {path.relative_to(ROOT)}: {marker}")
        for path, kind in missing:
            lines.append(f"missing managed {kind} block in {path.relative_to(ROOT)}")
        raise SystemExit("\n".join(lines))


def main() -> None:
    changed = sum(1 for path in HTML_FILES if process_file(path))
    validate()
    print(f"Updated {changed} HTML files")


if __name__ == "__main__":
    main()
