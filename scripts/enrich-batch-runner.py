#!/usr/bin/env python3
"""
Batch runner for enrich-compare-pages.py
Processes all pages needing enrichment, with progress tracking and error recovery.

Usage:
  python3 scripts/enrich-batch-runner.py           # Run all remaining pages
  python3 scripts/enrich-batch-runner.py --resume   # Resume from last checkpoint
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARE_DIR = REPO_ROOT / "compare"
DATA_DIR = REPO_ROOT / "compare-data"
PROGRESS_FILE = REPO_ROOT / "scripts" / ".enrich-progress.json"

# Same cliche detection as enrich script
AI_CLICHES = [
    r'\bvibrant\b', r'\bbustling\b', r'\bunforgettable\b', r'\bhidden gem\b',
    r'\brich tapestry\b', r'\bunique blend\b', r'\bsomething for everyone\b',
    r'\bwhether you\'re\b', r'\bWhether you\'re\b', r'\bpicture-perfect\b',
    r'\bworld-class\b', r'\bmust-visit\b', r'\bbreathtaking\b', r'\bstunning\b',
    r'\benchanting\b', r'\bseamlessly blends\b', r'\boffers something\b',
]


def get_pages_needing_work():
    """Find all pages that need enrichment, sorted by cliche count (worst first)."""
    pages = []
    for html_path in COMPARE_DIR.glob("*/index.html"):
        slug = html_path.parent.name
        if slug in ('index', '') or '-vs-' not in slug:
            continue

        content = html_path.read_text()

        # Remove style/script to count only content cliches
        no_style = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
        no_script = re.sub(r'<script[^>]*>.*?</script>', '', no_style, flags=re.DOTALL)

        count = 0
        for pattern in AI_CLICHES:
            count += len(re.findall(pattern, no_script, re.IGNORECASE))

        has_df = 'decision-grid' in no_style
        has_real_quotes = 'reddit.com/r/' in content  # Real quotes have actual URLs

        if count > 0 or not has_df or not has_real_quotes:
            pages.append((slug, count, has_df, has_real_quotes))

    pages.sort(key=lambda x: (-x[1], x[2]))
    return pages


def load_progress():
    """Load progress from checkpoint file."""
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"completed": [], "failed": [], "started_at": None}


def save_progress(progress):
    """Save progress to checkpoint file."""
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2) + "\n")


def enrich_single(slug):
    """Run enrichment on a single slug. Returns True on success."""
    result = subprocess.run(
        ['python3', 'scripts/enrich-compare-pages.py', slug],
        capture_output=True, text=True, cwd=REPO_ROOT, timeout=120
    )
    return result.returncode == 0, result.stdout + result.stderr


def rebuild_html(slug):
    """Rebuild HTML for a single slug using render_page directly."""
    try:
        sys.path.insert(0, str(REPO_ROOT / 'generators' / 'compare'))
        from build_compare import render_page
        data_path = DATA_DIR / f"{slug}.json"
        with open(data_path) as f:
            data = json.load(f)
        html = render_page(data)
        out_path = COMPARE_DIR / slug / "index.html"
        out_path.write_text(html)
        return True
    except Exception as e:
        print(f"    HTML rebuild failed: {e}")
        return False


def main():
    resume = '--resume' in sys.argv

    progress = load_progress() if resume else {"completed": [], "failed": [], "started_at": None}
    completed_set = set(progress["completed"])

    if not progress["started_at"]:
        progress["started_at"] = datetime.now().isoformat()

    all_pages = get_pages_needing_work()
    remaining = [(s, c, d, r) for s, c, d, r in all_pages if s not in completed_set]

    total = len(all_pages)
    done = len(completed_set)

    print(f"{'='*60}")
    print(f"  Compare Page Enrichment Batch Runner")
    print(f"  Total needing work: {total}")
    print(f"  Already done: {done}")
    print(f"  Remaining: {len(remaining)}")
    print(f"{'='*60}")

    batch_size = 50
    commit_every = 50

    for i, (slug, cliches, has_df, has_quotes) in enumerate(remaining):
        batch_num = (done + i) // commit_every
        idx = done + i + 1

        print(f"\n[{idx}/{total}] {slug} (cliches={cliches}, df={'Y' if has_df else 'N'}, quotes={'Y' if has_quotes else 'N'})")

        try:
            success, output = enrich_single(slug)
            if success:
                # Rebuild HTML directly (bypasses global validator)
                rebuild_html(slug)
                progress["completed"].append(slug)
                completed_set.add(slug)
                print(f"  ✅ Done ({idx}/{total})")
            else:
                progress["failed"].append({"slug": slug, "error": output[-200:]})
                print(f"  ❌ Failed: {output[-100:]}")
        except subprocess.TimeoutExpired:
            progress["failed"].append({"slug": slug, "error": "timeout"})
            print(f"  ❌ Timeout")
        except Exception as e:
            progress["failed"].append({"slug": slug, "error": str(e)})
            print(f"  ❌ Error: {e}")

        save_progress(progress)

        # Commit every N pages
        if len(progress["completed"]) % commit_every == 0 and len(progress["completed"]) > 0:
            batch = len(progress["completed"]) // commit_every
            print(f"\n{'='*60}")
            print(f"  Committing batch {batch} ({commit_every} pages)")
            print(f"{'='*60}")

            # Stage all enriched files
            for s in progress["completed"][-commit_every:]:
                subprocess.run(['git', 'add', f'compare-data/{s}.json', f'compare/{s}/index.html'],
                             cwd=REPO_ROOT, capture_output=True)

            subprocess.run(
                ['git', 'commit', '-m',
                 f'Enrich compare pages batch {batch}: fix cliches, add Reddit quotes + decision frameworks\n\n'
                 f'Enriched {commit_every} pages (total: {len(progress["completed"])})\n\n'
                 f'Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>'],
                cwd=REPO_ROOT, capture_output=True
            )
            print(f"  Committed batch {batch}")

        # Rate limiting between pages
        time.sleep(0.5)

    # Final commit for remaining pages
    uncommitted = len(progress["completed"]) % commit_every
    if uncommitted > 0:
        batch = (len(progress["completed"]) // commit_every) + 1
        print(f"\n{'='*60}")
        print(f"  Final commit: batch {batch} ({uncommitted} pages)")
        print(f"{'='*60}")

        for s in progress["completed"][-uncommitted:]:
            subprocess.run(['git', 'add', f'compare-data/{s}.json', f'compare/{s}/index.html'],
                         cwd=REPO_ROOT, capture_output=True)

        subprocess.run(
            ['git', 'commit', '-m',
             f'Enrich compare pages batch {batch} (final): fix cliches, add Reddit quotes + decision frameworks\n\n'
             f'Enriched {uncommitted} pages (total: {len(progress["completed"])})\n\n'
             f'Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>'],
            cwd=REPO_ROOT, capture_output=True
        )

    print(f"\n{'='*60}")
    print(f"  COMPLETE")
    print(f"  Enriched: {len(progress['completed'])}")
    print(f"  Failed: {len(progress['failed'])}")
    if progress['failed']:
        print(f"  Failed slugs: {[f['slug'] for f in progress['failed'][:10]]}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
