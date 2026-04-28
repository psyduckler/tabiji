#!/usr/bin/env python3
"""Extract top threads + top comments for a given slug from the corpus.

Reads `tmp/scam_research/corpus.json`, looks up the corpus_keys for the
slug from `corpus-mapping.json`, sorts threads by upvote score, and
writes the top 8 threads + their top 5 comments each to
`tmp/scam-skill/<slug>/top_threads.json`.

Usage:
    python3 helpers/extract_top_threads.py <slug>
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SKILL_DIR = REPO / ".claude-skills" / "general-scams-article"
CORPUS = REPO / "tmp" / "scam_research" / "corpus.json"
STATE_DIR = REPO / "tmp" / "scam-skill"


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_top_threads.py <slug>", file=sys.stderr)
        sys.exit(1)
    slug = sys.argv[1]

    mapping = json.loads((SKILL_DIR / "corpus-mapping.json").read_text())
    if slug not in mapping or slug.startswith("_"):
        print(f"Slug '{slug}' not found in corpus-mapping.json", file=sys.stderr)
        print(f"Available: {[k for k in mapping if not k.startswith('_')]}", file=sys.stderr)
        sys.exit(1)

    corpus_keys = mapping[slug]["corpus_keys"]
    if not CORPUS.exists():
        print(f"Corpus not found at {CORPUS}", file=sys.stderr)
        sys.exit(1)

    corpus = json.loads(CORPUS.read_text())

    all_threads = []
    for key in corpus_keys:
        if key not in corpus:
            print(f"⚠ Corpus key '{key}' not in corpus.json", file=sys.stderr)
            continue
        for thread in corpus[key].get("threads", []):
            thread["_source_corpus_key"] = key
            all_threads.append(thread)

    # Sort by post score, take top 8
    all_threads.sort(key=lambda t: -t["post"]["score"])
    top_threads = all_threads[:8]

    # Trim each thread to top 5 comments
    for thread in top_threads:
        comments = sorted(thread.get("comments", []), key=lambda c: -c["score"])
        thread["comments"] = comments[:5]

    out_dir = STATE_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "top_threads.json"
    out_file.write_text(json.dumps(top_threads, indent=2, ensure_ascii=False))

    print(f"✓ Extracted {len(top_threads)} top threads to {out_file}")
    print()
    print("Top threads:")
    for t in top_threads:
        p = t["post"]
        print(f"  [{p['subreddit']} | {p['score']}] {p['title'][:80]}")
        print(f"    {p['url']}")


if __name__ == "__main__":
    main()
