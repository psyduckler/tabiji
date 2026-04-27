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

# HTML danger-badge class → api/v1 severity vocabulary. The HTML side uses
# high/medium/low (the generator pattern-matches these literals for the hero
# severity-pill counter); the api/v1 side uses high/moderate/low (the book
# series convention). This sync is the single mechanism that keeps them in
# lockstep — never edit api/v1 severity by hand.
DANGER_TO_SEVERITY = {
    "high": "high",
    "medium": "moderate",
    "low": "low",
}


def _extract_severity(card) -> str | None:
    """Pull api/v1 severity from a .scam-card's danger-badge class.
    The badge carries two classes — `danger-badge` (container) and
    `danger-{high,medium,low}` (level). Match the level, not the container."""
    badge = card.select_one(".danger-badge")
    if not badge:
        return None
    for cls in badge.get("class", []) or []:
        if cls.startswith("danger-"):
            mapped = DANGER_TO_SEVERITY.get(cls[len("danger-"):])
            if mapped:
                return mapped
    return None


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
            "severity": _extract_severity(card),
        }

    data = json.loads(api_path.read_text())
    data["lastUpdated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    updated = 0
    sev_normalized = 0
    missing = []
    for scam in data["scams"]:
        new = content_by_name.get(scam["name"])
        if not new:
            missing.append(scam["name"])
            continue
        changed = False
        if scam.get("tldr") != new["tldr"]:
            scam["tldr"] = new["tldr"]
            changed = True
        if scam.get("description") != new["description"]:
            scam["description"] = new["description"]
            changed = True
        if new["severity"] and scam.get("severity") != new["severity"]:
            scam["severity"] = new["severity"]
            sev_normalized += 1
            changed = True
        if changed:
            updated += 1

    api_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"  {slug}: updated {updated} scams; lastUpdated={data['lastUpdated']}")
    if sev_normalized:
        print(f"  {slug}: severity normalized for {sev_normalized} scams (HTML danger-badge → api/v1 severity)")
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
