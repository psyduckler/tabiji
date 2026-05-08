#!/usr/bin/env python3
"""
Restore deleted /compare/{slug}/index.html pages from git history.

Background: PR #293 (commit efce3c8b068) deleted 628 compare pages with a
"<50 monthly searches" rationale that turned out to be wrong — many of the
deleted pages had high CTR and were the section's best performers. The
2026-05-08 GSC export shows ~239 clicks attributed to deleted URLs (vs 181
to live ones).

This script:
  1. For each slug, extracts the file content from its last-existing commit
     (the parent of the trim commit).
  2. Writes it back to compare/{slug}/index.html.
  3. Removes the matching `/compare/{slug}/ /compare/{hub}/ 301` line from
     _redirects.

Usage: pass slugs as args, or rely on the TIER1 default below.
"""
import subprocess, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRIM_COMMIT = "efce3c8b068"  # PR #293 — "infra: trim 628 low-volume compare pages"

# Tier 1: top 13 deleted compare pages by GSC click impact (2026-05-08 export).
# Each had ≥4 clicks and 1.27%–9.76% CTR before deletion.
TIER1 = [
    "bishkek-vs-almaty",
    "tirana-vs-sofia",
    "south-korea-vs-taiwan",
    "cook-islands-vs-samoa",
    "essaouira-vs-taghazout",
    "lake-bled-vs-hallstatt",
    "sao-tome-vs-cape-verde",
    "faroe-islands-vs-lofoten",
    "bhutan-vs-ladakh",
    "bukhara-vs-khiva",
    "st-barts-vs-maldives",
    "luang-prabang-vs-siem-reap",
    "naoshima-vs-teshima",
]


def restore_file(slug: str) -> dict:
    """Extract the file from TRIM_COMMIT^ and write it to compare/{slug}/index.html."""
    rel_path = f"compare/{slug}/index.html"
    # Get content from the parent of the trim commit (when the file last existed)
    proc = subprocess.run(
        ["git", "show", f"{TRIM_COMMIT}^:{rel_path}"],
        capture_output=True, text=True, cwd=ROOT,
    )
    if proc.returncode != 0:
        return {"slug": slug, "ok": False, "error": proc.stderr.strip()[:120]}

    out_path = ROOT / rel_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(proc.stdout)
    return {"slug": slug, "ok": True, "bytes": len(proc.stdout)}


def remove_redirect_lines(slugs: list) -> dict:
    """Strip `/compare/{slug}/ ...` redirect lines from _redirects, one per slug."""
    redirects_path = ROOT / "_redirects"
    content = redirects_path.read_text()
    lines = content.splitlines(keepends=True)

    removed = {}
    not_found = []
    for slug in slugs:
        # Match lines like: /compare/bishkek-vs-almaty/ /compare/global-mixed/ 301
        pattern = re.compile(rf"^/compare/{re.escape(slug)}/\s+\S+\s+30\d\s*$")
        new_lines = []
        found = None
        for line in lines:
            if found is None and pattern.match(line.rstrip("\n")):
                found = line.rstrip()
                continue
            new_lines.append(line)
        if found:
            removed[slug] = found
            lines = new_lines
        else:
            not_found.append(slug)

    redirects_path.write_text("".join(lines))
    return {"removed": removed, "not_found": not_found}


def main():
    slugs = sys.argv[1:] or TIER1
    print(f"Restoring {len(slugs)} compare pages from {TRIM_COMMIT}^...")
    results = [restore_file(s) for s in slugs]

    ok = [r for r in results if r["ok"]]
    failed = [r for r in results if not r["ok"]]

    print(f"\nRestored: {len(ok)}/{len(results)}")
    for r in ok:
        print(f"  ✓ {r['slug']} ({r['bytes']:,} bytes)")
    for r in failed:
        print(f"  ✗ {r['slug']}: {r['error']}")

    print("\nRemoving redirect rules...")
    redirect_result = remove_redirect_lines([r["slug"] for r in ok])
    print(f"Redirect lines removed: {len(redirect_result['removed'])}")
    for slug, line in redirect_result["removed"].items():
        print(f"  − {line}")
    if redirect_result["not_found"]:
        print(f"\nNo matching redirect line found for: {redirect_result['not_found']}")

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
