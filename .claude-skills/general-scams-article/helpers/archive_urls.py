#!/usr/bin/env python3
"""Submit cited URLs to archive.org for permanence.

Reads `tmp/scam-skill/<slug>/sources.md`, extracts every source URL,
submits each to https://web.archive.org/save/<URL>, and writes the
resulting archive URLs to `tmp/scam-skill/<slug>/archive-cache.json`.

Usage:
    python3 helpers/archive_urls.py <slug>
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
STATE_DIR = REPO / "tmp" / "scam-skill"


def extract_urls(sources_md: str) -> list[str]:
    urls = re.findall(r'https?://[^\s\)\]]+', sources_md)
    # Dedupe but preserve order
    seen = set()
    out = []
    for u in urls:
        u = u.rstrip('.,;:!?')
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def archive_one(url: str, retries: int = 2) -> str | None:
    """Submit URL to archive.org, return the archived URL on success."""
    save_url = f"https://web.archive.org/save/{url}"
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(save_url, headers={
                'User-Agent': 'tabiji-scam-skill/1.0 (archive submission)',
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                # archive.org redirects to /web/<timestamp>/<url> on success
                final = resp.geturl()
                if '/web/' in final:
                    return final
        except Exception as e:
            print(f"  attempt {attempt+1} failed for {url[:70]}: {e}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: archive_urls.py <slug>", file=sys.stderr)
        sys.exit(1)
    slug = sys.argv[1]

    sources_path = STATE_DIR / slug / "sources.md"
    if not sources_path.exists():
        print(f"sources.md not found at {sources_path}", file=sys.stderr)
        sys.exit(1)

    urls = extract_urls(sources_path.read_text())
    print(f"Found {len(urls)} unique URLs to archive")

    cache_path = STATE_DIR / slug / "archive-cache.json"
    cache: dict[str, str] = {}
    if cache_path.exists():
        cache = json.loads(cache_path.read_text())

    for url in urls:
        if url in cache:
            print(f"  [cached] {url[:70]}")
            continue
        print(f"  archiving {url[:70]}...")
        archived = archive_one(url)
        if archived:
            cache[url] = archived
            print(f"    → {archived[:70]}")
        else:
            print(f"    ✗ failed")
        time.sleep(2)  # be polite to archive.org

    cache_path.write_text(json.dumps(cache, indent=2))
    print(f"✓ Wrote {len(cache)} archive entries to {cache_path}")


if __name__ == "__main__":
    main()
