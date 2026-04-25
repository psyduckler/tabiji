"""Shared helpers for scam-page sweeps, the generator, and the lint script.

Consolidates three things that were copy-pasted across ~10 files:
  - `collect_scam_targets()` — the set of paths a sweep should walk
  - git-log date helpers (per-file and batched)
  - `is_tldr_complete()` — the rule 18 predicate, identical in all consumers

Keep this file lean: no business logic, no HTML parsing. Only paths + shell +
a single string predicate.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCAMS = REPO / "scams"
_API = REPO / "api" / "v1"


def collect_scam_targets(
    *,
    city_pages: bool = True,
    country_hubs: bool = False,
    master_hub: bool = False,
    research_json: bool = False,
    api_json: bool = False,
) -> list[Path]:
    """Build a target path list. Each flag adds one asset class."""
    out: list[Path] = []
    if city_pages:
        out.extend(
            p / "index.html"
            for p in sorted(SCAMS.iterdir())
            if p.is_dir()
            and p.name not in ("country", "research")
            and (p / "index.html").exists()
        )
    if country_hubs:
        country_dir = SCAMS / "country"
        if country_dir.exists():
            out.extend(sorted(country_dir.glob("*/index.html")))
    if master_hub and (SCAMS / "index.html").exists():
        out.append(SCAMS / "index.html")
    if research_json:
        out.extend(sorted((SCAMS / "research").glob("*.json")))
    if api_json:
        out.extend(sorted((_API / "scams").glob("*.json")))
        catalog = _API / "catalog" / "scams.json"
        if catalog.exists():
            out.append(catalog)
    return out


def git_first_commit(path: Path) -> str | None:
    """ISO-8601 timestamp of the commit that first added `path`, or None."""
    try:
        out = subprocess.check_output(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%aI",
             "--", str(path)],
            cwd=REPO, stderr=subprocess.DEVNULL,
        ).decode().strip()
    except subprocess.CalledProcessError:
        return None
    if not out:
        return None
    return out.splitlines()[-1]


def git_latest_commit(path: Path) -> str | None:
    """ISO-8601 timestamp of the most recent commit touching `path`, or None."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%aI", "--", str(path)],
            cwd=REPO, stderr=subprocess.DEVNULL,
        ).decode().strip()
    except subprocess.CalledProcessError:
        return None
    return out or None


def git_commit_times_batch() -> tuple[dict[Path, str], dict[Path, str]]:
    """One-shot walk of the repo's git history. Returns (first_added, latest)
    dicts keyed by absolute Path.

    ~40x faster than calling `git_first_commit` / `git_latest_commit` in a
    loop over 500+ files — one `git log` is ~2s, 1000 per-file calls are ~3 min.
    Missing paths (uncommitted) are simply absent from the dict.
    """
    first_added = _walk_git_log(["--diff-filter=A", "--reverse"])
    latest = _walk_git_log([])
    return first_added, latest


def _walk_git_log(extra_args: list[str]) -> dict[Path, str]:
    out = subprocess.check_output(
        ["git", "log", *extra_args, "--name-only", "--format=|%aI|"],
        cwd=REPO, stderr=subprocess.DEVNULL,
    ).decode()
    result: dict[Path, str] = {}
    current = None
    for line in out.splitlines():
        if line.startswith("|") and line.endswith("|"):
            current = line.strip("|")
        elif line and current and (REPO / line) not in result:
            result[REPO / line] = current
    return result


_TLDR_TRAIL_QUOTES = "'\"\u2019\u201d"


def is_tldr_complete(text: str) -> bool:
    """Rule 18: a TLDR text ends cleanly in `.`, `!`, or `?`.

    Used by the generator (post-check), the tldr-truncation sweep (should-fix
    predicate), and the HTML linter (REJECT condition). Keeping them aligned
    prevents the 3-way drift where one emits text another wants to rewrite.
    """
    if not text:
        return False
    stripped = text.rstrip().rstrip(_TLDR_TRAIL_QUOTES).rstrip()
    if not stripped:
        return False
    if stripped.endswith("...") or stripped.endswith("\u2026"):
        return False
    return stripped[-1] in ".!?"
