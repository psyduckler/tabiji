#!/usr/bin/env python3
"""
Fix sitemap.xml lastmod dates to reflect actual git commit dates.

Reads sitemap.xml, maps each URL to its local file path, runs
`git log -1 --format="%ai"` to get the true last-modified date,
and rewrites sitemap.xml with accurate per-URL lastmod values.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"
SITE_ORIGIN = "https://tabiji.ai/"


def url_to_filepath(url: str) -> str:
    """Convert a sitemap URL to a relative file path in the repo."""
    if not url.startswith(SITE_ORIGIN):
        return None

    path = url[len(SITE_ORIGIN):]

    # Root URL
    if path == "" or path == "/":
        return "index.html"

    # Strip trailing slash
    path = path.rstrip("/")

    # Try path/index.html first (most common pattern)
    candidate = f"{path}/index.html"
    if (REPO_ROOT / candidate).exists():
        return candidate

    # Try path.html
    candidate = f"{path}.html"
    if (REPO_ROOT / candidate).exists():
        return candidate

    # Try path directly (for files without index.html)
    if (REPO_ROOT / path).is_file():
        return path

    return None


def get_git_date(filepath: str) -> str:
    """Get the last git commit date for a file as YYYY-MM-DD."""
    full_path = REPO_ROOT / filepath
    if not full_path.exists():
        return None

    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ai", "--", filepath],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            # Output is like "2026-04-10 14:23:45 -0700"
            return result.stdout.strip().split(" ")[0]
    except (subprocess.TimeoutExpired, OSError):
        pass

    return None


def main():
    if not SITEMAP_PATH.exists():
        print(f"Error: {SITEMAP_PATH} not found", file=sys.stderr)
        sys.exit(1)

    content = SITEMAP_PATH.read_text(encoding="utf-8")

    # Batch: collect all unique file paths first, then query git once per file
    # to avoid 4000+ individual git log calls.

    # Extract all <loc>...</loc> values
    loc_pattern = re.compile(r"<loc>(.*?)</loc>")
    urls = loc_pattern.findall(content)

    print(f"Found {len(urls)} URLs in sitemap.xml")

    # Map URLs to file paths
    url_file_map: dict[str, str] = {}
    for url in urls:
        url_file_map[url] = url_to_filepath(url)

    # Get unique file paths that exist
    unique_files = set(fp for fp in url_file_map.values() if fp is not None)
    print(f"Mapped {len(unique_files)} unique file paths")

    # Batch git log: get dates for all files at once using git log
    # Process in batches to avoid arg-length limits
    file_date_map: dict[str, str] = {}
    file_list = sorted(unique_files)

    BATCH_SIZE = 50
    for i in range(0, len(file_list), BATCH_SIZE):
        batch = file_list[i : i + BATCH_SIZE]
        for filepath in batch:
            date = get_git_date(filepath)
            if date:
                file_date_map[filepath] = date

    print(f"Got git dates for {len(file_date_map)} files")

    # Now replace lastmod dates in the sitemap
    # We process <url> blocks individually
    url_block_pattern = re.compile(
        r"(<url>\s*<loc>(.*?)</loc>\s*<lastmod>)(.*?)(</lastmod>)",
        re.DOTALL,
    )

    updated_count = 0
    unchanged_count = 0
    unmapped_count = 0

    def replace_lastmod(match):
        nonlocal updated_count, unchanged_count, unmapped_count
        prefix = match.group(1)
        url = match.group(2)
        old_date = match.group(3)
        suffix = match.group(4)

        filepath = url_file_map.get(url)
        if filepath and filepath in file_date_map:
            new_date = file_date_map[filepath]
            if new_date != old_date:
                updated_count += 1
                return f"{prefix}{new_date}{suffix}"
            else:
                unchanged_count += 1
                return match.group(0)
        else:
            unmapped_count += 1
            return match.group(0)

    new_content = url_block_pattern.sub(replace_lastmod, content)

    # Write back
    SITEMAP_PATH.write_text(new_content, encoding="utf-8")

    print(f"\nResults:")
    print(f"  Updated:   {updated_count}")
    print(f"  Unchanged: {unchanged_count}")
    print(f"  Unmapped:  {unmapped_count} (kept existing date)")
    print(f"  Total:     {updated_count + unchanged_count + unmapped_count}")


if __name__ == "__main__":
    main()
