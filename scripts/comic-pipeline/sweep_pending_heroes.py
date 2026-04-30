#!/usr/bin/env python3
"""Find every atlas entry whose hero comic is missing on R2 and (re)generate it.

Use case: the cron sandbox can't reach the macOS keychain, so it ships atlas pages
without generating a hero comic and marks them with `<!-- HERO_COMIC_PENDING -->`.
Run this script from a Mac that DOES have keychain access to fill in the gaps.

Strategy:
  1. List local atlas slugs (= every directory under scams/atlas/ except scams/atlas/index.html)
  2. For each, HEAD https://img.tabiji.ai/scams/atlas/{slug}/hero.jpg
  3. If non-200, call generate_atlas.py for that slug
  4. After all gens, optionally remove the HERO_COMIC_PENDING marker comment from each page
     so future PR diffs are clean

By default, --auto-clean-marker is OFF so you can review the output first. Pass it
to also strip the HTML comment marker after a successful re-upload.

Usage:
    python3 scripts/comic-pipeline/sweep_pending_heroes.py
    python3 scripts/comic-pipeline/sweep_pending_heroes.py --auto-clean-marker
    python3 scripts/comic-pipeline/sweep_pending_heroes.py --dry-run
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ATLAS = REPO / "scams" / "atlas"
PIPELINE = REPO / "scripts" / "comic-pipeline" / "generate_atlas.py"

R2_URL_TEMPLATE = "https://img.tabiji.ai/scams/atlas/{slug}/hero.jpg"
PENDING_MARKER = "<!-- HERO_COMIC_PENDING -->"


def hero_status(slug: str) -> int:
    """Return HTTP status of the hero comic on R2; 0 on connection error.

    Uses a Range-limited GET (first 256 bytes) instead of HEAD because Cloudflare's
    hotlink protection on img.tabiji.ai returns 403 to HEAD requests but serves GET.
    """
    req = urllib.request.Request(
        R2_URL_TEMPLATE.format(slug=slug),
        headers={"Range": "bytes=0-255", "User-Agent": "tabiji-hero-sweeper/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def list_slugs() -> list[str]:
    return sorted(p.name for p in ATLAS.iterdir() if p.is_dir() and (p / "index.html").exists())


def remove_pending_marker(slug: str) -> bool:
    path = ATLAS / slug / "index.html"
    text = path.read_text()
    if PENDING_MARKER not in text:
        return False
    new = text.replace(PENDING_MARKER + "\n", "").replace(PENDING_MARKER, "")
    path.write_text(new)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true",
                        help="Just list which heroes are missing; don't generate")
    parser.add_argument("--auto-clean-marker", action="store_true",
                        help="After successful re-upload, strip <!-- HERO_COMIC_PENDING --> from the page")
    parser.add_argument("--slugs", nargs="*", default=None,
                        help="Only check these specific slugs (space-separated). Defaults to all live atlas slugs.")
    args = parser.parse_args()

    slugs = args.slugs or list_slugs()
    print(f"checking {len(slugs)} atlas hero comics on R2...")
    missing: list[str] = []
    for slug in slugs:
        code = hero_status(slug)
        ok = code in (200, 206)
        marker = "✓" if ok else "✗"
        print(f"  {marker} {slug}: {code}")
        if not ok:
            missing.append(slug)

    if not missing:
        print("\nAll heroes present on R2. Nothing to do.")
        return 0

    print(f"\n{len(missing)} hero(s) missing: {', '.join(missing)}")
    if args.dry_run:
        return 0

    failed: list[str] = []
    for slug in missing:
        print(f"\n--- generating {slug} ---")
        result = subprocess.run([sys.executable, str(PIPELINE), slug], cwd=REPO)
        if result.returncode != 0:
            print(f"❌ {slug}: pipeline exited {result.returncode}")
            failed.append(slug)
            continue
        # verify upload
        if hero_status(slug) not in (200, 206):
            print(f"❌ {slug}: still 404 after pipeline")
            failed.append(slug)
            continue
        print(f"✓ {slug}: hero now on R2")
        if args.auto_clean_marker:
            if remove_pending_marker(slug):
                print(f"  cleaned HERO_COMIC_PENDING marker from page")

    if failed:
        print(f"\n{len(failed)} failed: {', '.join(failed)}")
        return 1
    print(f"\nAll {len(missing)} heroes regenerated.")
    if args.auto_clean_marker:
        print("Markers cleaned. Commit with: git add scams/atlas/ && git commit -m '...'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
