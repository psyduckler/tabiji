#!/usr/bin/env python3
"""
Backfill missing card descriptions in popular-picks-hub-data/{country}.json
files by pulling from popular-picks/picks-metadata.json. This fixes
pre-existing hub validation errors so hub HTML can be rebuilt.
"""
import json
import html
from pathlib import Path

ROOT = Path("/Users/bjh/Documents/tabiji")
HUB_DIR = ROOT / "popular-picks-hub-data"
META_PATH = ROOT / "popular-picks/picks-metadata.json"

def truncate(text, limit=200):
    if not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."

def main():
    metadata = json.loads(META_PATH.read_text())
    fixed_total = 0
    for hub_path in sorted(HUB_DIR.glob("*.json")):
        data = json.loads(hub_path.read_text())
        if data.get("pageType") != "popular-picks-hub":
            continue
        sections = data.get("sections", [])
        fixed = 0
        for sec in sections:
            for card in sec.get("cards", []):
                if card.get("description"):
                    continue
                slug = card.get("slug")
                meta = metadata.get(slug, {})
                desc = meta.get("description") or meta.get("title") or ""
                # Decode HTML entities (e.g. &#x27; → ')
                desc = html.unescape(desc)
                if not desc:
                    continue
                card["description"] = truncate(desc, 200)
                fixed += 1
        if fixed:
            hub_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            print(f"{hub_path.name}: fixed {fixed} card description(s)")
            fixed_total += fixed
    print(f"\nTotal fixed: {fixed_total}")

if __name__ == "__main__":
    main()
