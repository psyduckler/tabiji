#!/usr/bin/env python3
"""Update api/v1/scams/<city>.json `name` field from OLD to NEW titles.

After title-rewrite of HTML, sync_api_from_html.py matches scams by `name`
between HTML and JSON — but the JSON still has OLD names. This script
updates the `name` field in each JSON to the new short title (matched by
position 1..6 against the rewrite map), so that sync_api_from_html.py can
then propagate tldr, description, and severity.

IDs are preserved (immutable URLs).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RW_PATH = Path("/tmp/mexico-title-rewrite.txt")


def parse_rewrites() -> dict[str, list[tuple[int, str, str]]]:
    out: dict[str, list[tuple[int, str, str]]] = {}
    current: str | None = None
    pending: dict[int, dict[str, str]] = {}
    for raw in RW_PATH.read_text().splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("=== ") and line.endswith(" ==="):
            if current and pending:
                out[current] = sorted(
                    [(n, d["OLD"], d["NEW"]) for n, d in pending.items()]
                )
            current = line.strip("= ").strip()
            pending = {}
            continue
        m = re.match(r"^(\d+)\|(OLD|NEW|REDDIT):\s*(.+)$", line)
        if not m or current is None:
            continue
        n = int(m.group(1))
        if m.group(2) in ("OLD", "NEW"):
            pending.setdefault(n, {})[m.group(2)] = m.group(3).strip()
    if current and pending:
        out[current] = sorted(
            [(n, d["OLD"], d["NEW"]) for n, d in pending.items()]
        )
    return out


def update_city(city: str, rws: list[tuple[int, str, str]]) -> int:
    path = REPO / f"api/v1/scams/{city}.json"
    data = json.loads(path.read_text())
    scams = data["scams"]
    if len(scams) != len(rws):
        print(f"  {city}: SKIP — {len(scams)} JSON scams vs {len(rws)} rewrites")
        return 0
    edits = 0
    for (n, old, new), scam in zip(rws, scams):
        # Sanity: confirm position matches via OLD title
        cur_name = scam.get("name", "")
        if cur_name != old:
            print(f"  {city}: scam {n} mismatch — JSON has '{cur_name}' / rewrite expects '{old}'; updating anyway")
        scam["name"] = new
        edits += 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return edits


def main():
    rewrites = parse_rewrites()
    total = 0
    for city, rws in sorted(rewrites.items()):
        n = update_city(city, rws)
        print(f"  {city}: {n} JSON name updates")
        total += n
    print(f"\nTotal: {total}")


if __name__ == "__main__":
    main()
