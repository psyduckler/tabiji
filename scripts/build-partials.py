#!/usr/bin/env python3
"""Sync managed shared-head/nav/footer blocks from _includes/ into HTML pages.

Default mode (no args): walks every tracked HTML file and rewrites the
managed blocks in-place. Used by the explicit sync workflow
(scripts/sync-partials.sh) when _includes/*.html changes.

--check: dry-run. Reports which files have stale managed blocks, writes
nothing, exits 1 if any drift is found. Used by CI to fail PRs with
outdated partials.

--staged-only: restrict the scan to HTML files currently staged in git
(diff-filter=AM). Pairs with --check in .githooks/pre-commit so a normal
commit only verifies the files the developer actually touched — no more
sweeping auto-rewrites of unrelated pages across the repo.

The old behavior (pre-commit auto-rewrites + `git add` every HTML file)
was the root cause of massive cross-branch merge conflicts whenever more
than one agent worked in parallel. This script still does the same
rewrite work when invoked explicitly, but it no longer runs as a
side-effect of every commit.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
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


def _eligible(path: Path) -> bool:
    """Matches the exclusions used by HTML_FILES scanning."""
    if ".git" in path.parts or "node_modules" in path.parts or "tmp" in path.parts:
        return False
    # Skip git worktrees — they're isolated repo copies that shouldn't be
    # propagated into. Without this, a build-partials run iterates 23+ worktrees
    # × thousands of HTML files each (effectively hangs the script).
    if ".claude" in path.parts:
        return False
    if path.is_relative_to(INCLUDES):
        return False
    return True


HTML_FILES = [p for p in ROOT.rglob("*.html") if _eligible(p)]


def managed_block(start: str, content: str, end: str) -> str:
    return f"{start}\n{content}\n{end}"


def replace_or_insert(text: str, start: str, end: str, content: str,
                      fallback_pattern: str | None = None,
                      fallback_repl: str | None = None) -> tuple[str, bool]:
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
    # Remove stray duplicate markers left by earlier runs. Pre-existing pages
    # sometimes had orphan start markers (or orphan end markers) accumulate
    # from fallback re-inserts. Collapse consecutive duplicates on both sides.
    for marker in (start, end):
        dup = f"{marker}\n{marker}"
        while dup in updated:
            updated = updated.replace(dup, marker)
    return updated, updated != text


def nav_partial_for(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    # Export nav only belongs on generated itinerary detail pages under /i/*.
    # Section index pages like /itineraries/ should keep the normal site nav.
    if parts[0] == "i":
        return PARTIALS["nav-export"]
    return PARTIALS["nav-main"]


def footer_partial_for(path: Path) -> str:
    return PARTIALS["footer-default"]


def process_file(path: Path, write: bool = True) -> bool:
    """Rewrite managed blocks in `path`. Returns True if content would change.

    When write=False, computes the diff but doesn't touch the file.
    """
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
        if write:
            path.write_text(text)
        return True
    return False


def validate(targets: list[Path]) -> None:
    unresolved = []
    missing = []
    for path in targets:
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


def staged_html_files() -> list[Path]:
    """HTML files currently staged for commit (added or modified)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
        capture_output=True, text=True, cwd=ROOT,
    )
    if result.returncode != 0:
        return []
    out: list[Path] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or not line.endswith(".html"):
            continue
        p = ROOT / line
        if p.is_file() and _eligible(p):
            out.append(p)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="Dry-run: report drift, write nothing, exit 1 if any file is stale.")
    parser.add_argument("--staged-only", action="store_true",
                        help="Limit the scan to HTML files staged in git (for pre-commit use).")
    parser.add_argument("--files", nargs="+", default=None, metavar="PATH",
                        help="Process only the given HTML files (relative or absolute). "
                             "Useful for generators that just wrote a single page and want to "
                             "sync it without sweeping the whole repo.")
    args = parser.parse_args()

    if args.files:
        targets = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = ROOT / p
            if p.is_file() and _eligible(p):
                targets.append(p)
            else:
                print(f"⚠️  skipping {f}: not a tracked HTML file", file=sys.stderr)
        if not targets:
            return 0
    elif args.staged_only:
        targets = staged_html_files()
        if not targets:
            # No staged HTML — hook has nothing to check.
            return 0
    else:
        targets = HTML_FILES

    drifted = [p for p in targets if process_file(p, write=not args.check)]

    if args.check:
        if drifted:
            print(f"❌ {len(drifted)} HTML file(s) have stale managed blocks "
                  f"(shared-head / nav / footer out of sync with _includes/):",
                  file=sys.stderr)
            for p in drifted[:20]:
                print(f"   {p.relative_to(ROOT)}", file=sys.stderr)
            if len(drifted) > 20:
                print(f"   ... and {len(drifted) - 20} more", file=sys.stderr)
            print(file=sys.stderr)
            print("   Fix: run `scripts/sync-partials.sh`, then re-stage the updated files.",
                  file=sys.stderr)
            return 1
        if args.files:
            print(f"✓ All {len(targets)} specified HTML file(s) are in sync with _includes/.")
        elif args.staged_only:
            print(f"✓ All {len(targets)} staged HTML file(s) are in sync with _includes/.")
        else:
            print(f"✓ All {len(targets)} tracked HTML file(s) are in sync with _includes/.")
        return 0

    # Non-check mode: rewrite the targets in place.
    if args.files:
        # Targeted sync — skip the full-tree validate() (which would touch files
        # the caller didn't ask about and is slow on large trees).
        print(f"Updated {len(drifted)}/{len(targets)} HTML file(s)")
        return 0

    # Full explicit sync: rewrite + validate.
    validate(HTML_FILES)
    print(f"Updated {len(drifted)} HTML file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
