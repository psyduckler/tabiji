#!/usr/bin/env python3
"""Sync api/v1/scams/<slug>.json with the rewritten HTML scam stories.

Run from any tabiji worktree — repo root is auto-detected via git.

Usage:
    python3 scripts/sync_api_from_html.py <slug>

Used by the scam-narrative-rewrite-batch skill (see .claude/skills/) after
each city's HTML rewrite to keep API JSON in lockstep with the rendered HTML.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup


def repo_root() -> Path:
    """Locate the current worktree root via git."""
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return Path(out)


REPO = repo_root()


def sync(slug: str) -> None:
    html_path = REPO / "scams" / slug / "index.html"
    api_path = REPO / "api" / "v1" / "scams" / f"{slug}.json"
    soup = BeautifulSoup(html_path.read_text(), "html.parser")

    content_by_name: dict[str, dict] = {}
    for card in soup.select(".scam-card"):
        title_el = card.select_one(".scam-title")
        if not title_el:
            continue
        name = title_el.get_text(strip=True)
        tldr_el = card.select_one(".scam-tldr")
        body_paras = card.select(".scam-story-body")
        content_by_name[name] = {
            "tldr": tldr_el.get_text(" ", strip=True) if tldr_el else "",
            "description": "\n\n".join(p.get_text(" ", strip=True) for p in body_paras),
        }

    data = json.loads(api_path.read_text())
    data["lastUpdated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    updated = 0
    missing = []
    for scam in data["scams"]:
        new = content_by_name.get(scam["name"])
        if not new:
            missing.append(scam["name"])
            continue
        if scam.get("tldr") != new["tldr"] or scam.get("description") != new["description"]:
            scam["tldr"] = new["tldr"]
            scam["description"] = new["description"]
            updated += 1

    api_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"  {slug}: updated {updated} scams; lastUpdated={data['lastUpdated']}")
    if missing:
        print(f"  WARNING: {len(missing)} scams in API not found in HTML: {missing}")


def mark_queue_complete(slug: str, pr_number: int | None) -> None:
    queue_path = REPO / "scripts" / "queues" / "scam-narrative-rewrite-queue.json"
    q = json.loads(queue_path.read_text())
    for entry in q["queue"]:
        if entry["slug"] == slug:
            entry["status"] = "complete"
            entry["pr_number"] = pr_number
            entry["completed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            print(f"  queue: marked {slug} complete")
            break
    queue_path.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    slug = sys.argv[1]
    sync(slug)
    mark_queue_complete(slug, None)  # PR number filled in after PR opens
