#!/usr/bin/env python3
"""Pinterest API v5 client — token check, board lookup, pin creation."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

import requests

API = "https://api.pinterest.com/v5"


def get_token() -> str:
    return subprocess.check_output(
        ["security", "find-generic-password", "-s", "pinterest-access-token", "-w"],
        text=True,
    ).strip()


def headers() -> dict:
    return {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def check_token() -> dict:
    r = requests.get(f"{API}/user_account", headers=headers(), timeout=30)
    if r.status_code != 200:
        sys.exit(f"token check failed ({r.status_code}): {r.text[:400]}")
    return r.json()


def list_boards() -> list[dict]:
    boards, bookmark = [], None
    while True:
        params = {"page_size": 100}
        if bookmark:
            params["bookmark"] = bookmark
        r = requests.get(f"{API}/boards", headers=headers(), params=params, timeout=30)
        if r.status_code != 200:
            sys.exit(f"list_boards failed ({r.status_code}): {r.text[:400]}")
        body = r.json()
        boards.extend(body.get("items", []))
        bookmark = body.get("bookmark")
        if not bookmark:
            break
    return boards


def find_board(query: str) -> dict:
    q_slug = slugify(query)
    for b in list_boards():
        if b.get("id") == query:
            return b
        if slugify(b.get("name", "")) == q_slug:
            return b
    sys.exit(f"board not found matching: {query}")


def create_pin(
    board_id: str,
    image_url: str,
    link: str,
    title: str,
    description: str,
    alt_text: str | None = None,
) -> dict:
    payload = {
        "board_id": board_id,
        "title": title[:100],
        "description": description[:500],
        "link": link,
        "media_source": {"source_type": "image_url", "url": image_url},
    }
    if alt_text:
        payload["alt_text"] = alt_text[:500]
    r = requests.post(f"{API}/pins", headers=headers(), json=payload, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"create_pin failed ({r.status_code}): {r.text[:400]}")
    return r.json()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true", help="verify token + print user info")
    p.add_argument("--list-boards", action="store_true", help="list all accessible boards")
    p.add_argument("--resolve-board", help="board name or slug to find ID for")
    args = p.parse_args()

    if args.check:
        info = check_token()
        print(f"✓ token valid — username={info.get('username')}, type={info.get('account_type')}")
        return
    if args.list_boards:
        for b in list_boards():
            print(f"  {b['id']}  {b['name']}")
        return
    if args.resolve_board:
        b = find_board(args.resolve_board)
        print(json.dumps({"id": b["id"], "name": b["name"], "privacy": b.get("privacy")}, indent=2))
        return
    print("nothing to do — try --check, --list-boards, or --resolve-board")


if __name__ == "__main__":
    main()
