#!/usr/bin/env python3
"""Pinterest pin orchestrator: render → upload → post.

Each scam in manifest.json gets 3 pins (stacked, hook, lesson).
State is tracked in state.json so re-runs skip already-posted pins.

Usage:
  python scripts/pinterest/pin.py --slug nyc-cd-hustle
  python scripts/pinterest/pin.py --slug nyc-cd-hustle --steps render
  python scripts/pinterest/pin.py --slug nyc-cd-hustle --dry-run    # render+upload, skip post
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from render import render_all, TMP  # noqa: E402
from upload import upload_slug  # noqa: E402
from post import create_pin  # noqa: E402

CONFIG = HERE / "config.json"
MANIFEST = HERE / "manifest.json"
# state.json lives outside the repo so git stash/checkout can't wipe in-flight
# cron mutations. The in-repo path is kept as a fallback for first-run seed.
STATE = Path.home() / ".local" / "share" / "tabiji-pinterest" / "state.json"
STATE_LEGACY = HERE / "state.json"
PUBLIC_BASE = "https://img.tabiji.ai"


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    if STATE_LEGACY.exists():
        return json.loads(STATE_LEGACY.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2) + "\n")


def utm_link(base_url: str, slug: str, fmt: str) -> str:
    head, sep, frag = base_url.partition("#")
    qsep = "&" if "?" in head else "?"
    qs = f"utm_source=pinterest&utm_medium=pin&utm_campaign={slug}&utm_content={fmt}"
    rebuilt = f"{head}{qsep}{qs}"
    return f"{rebuilt}#{frag}" if sep else rebuilt


def process(slug: str, steps: set[str], dry_run: bool) -> None:
    config = json.loads(CONFIG.read_text())
    manifest = json.loads(MANIFEST.read_text())
    state = load_state()

    entries = {e["slug"]: e for e in manifest["scams"]}
    if slug not in entries:
        sys.exit(f"slug not in manifest: {slug}")
    entry = entries[slug]

    if dry_run:
        steps = steps - {"post"}

    if "render" in steps:
        print(f"→ render {slug}")
        render_all(entry, TMP / slug)

    urls = {}
    if "upload" in steps:
        print(f"→ upload {slug}")
        urls = upload_slug(slug)
    else:
        for fmt in entry["formats"]:
            urls[fmt] = f"{PUBLIC_BASE}/pinterest/{slug}/{fmt}.jpg"

    if "post" in steps:
        board_id = config.get("board_id", "").strip()
        if not board_id:
            sys.exit("config.json: board_id is empty — run `python scripts/pinterest/post.py --resolve-board <name>` first")
        print(f"→ post {slug} (board={board_id})")
        for fmt, copy in entry["formats"].items():
            key = f"{slug}:{fmt}"
            if key in state and state[key].get("pin_id"):
                print(f"  {fmt}: already posted (pin_id={state[key]['pin_id']}), skipping")
                continue
            link = utm_link(entry["scam_url"], slug, fmt)
            try:
                pin = create_pin(
                    board_id=board_id,
                    image_url=urls[fmt],
                    link=link,
                    title=copy.get("pin_title", ""),
                    description=copy.get("pin_description", ""),
                    alt_text=copy.get("alt_text"),
                )
            except Exception as e:
                print(f"  {fmt}: ✗ {e}")
                continue
            state[key] = {"pin_id": pin.get("id"), "url": link, "image": urls[fmt]}
            save_state(state)
            print(f"  {fmt}: pin_id={pin.get('id')}")
            time.sleep(1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True, help="manifest entry slug to process")
    p.add_argument(
        "--steps",
        default="render,upload,post",
        help="comma-separated subset of: render,upload,post (default: all three)",
    )
    p.add_argument("--dry-run", action="store_true", help="render+upload only; skip Pinterest post")
    args = p.parse_args()
    process(args.slug, set(args.steps.split(",")), args.dry_run)


if __name__ == "__main__":
    main()
