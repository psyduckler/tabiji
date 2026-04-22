#!/usr/bin/env python3
"""Fetch Google Images photos via SerpAPI for destinations still on owl-logo.

Reads api/v1/destinations-full.json as canonical source. For each slug whose
`photo` field contains 'owl-logo', searches Google Images, downloads the top
candidate, converts to webp, uploads to R2 at find/img/{slug}.webp, and
updates the photo field in destinations-full.json in place.

Resumable: each run re-scans the JSON and picks slugs still on owl-logo.

Usage:
    python3 scripts/fetch-destination-photos.py [--limit N] [--parallel N] [--dry-run]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FULL_JSON = REPO / "api" / "v1" / "destinations-full.json"
LOG_FILE = REPO / "scripts" / "fetch-destination-photos.log"

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_PUBLIC = "https://img.tabiji.ai"

PLACEHOLDER_MARKER = "owl-logo"

_log_lock = threading.Lock()
_json_lock = threading.Lock()


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    with _log_lock:
        print(line, flush=True)
        try:
            with open(LOG_FILE, "a") as f:
                f.write(line + "\n")
        except OSError:
            pass


def get_keychain(name: str) -> str | None:
    try:
        r = subprocess.run(
            ["security", "find-generic-password", "-s", name, "-w"],
            capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip() or None
    except Exception:
        return None


# Keychain secrets loaded lazily by main() — keep import side-effect-free
# so tests/other modules can import this safely.
SERPAPI_KEY: str | None = None
CF_TOKEN: str | None = None


def search_google_images(query: str) -> list[dict]:
    """Top-5 Google Images results via SerpAPI."""
    params = urllib.parse.urlencode({
        "engine": "google_images",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": "5",
        "ijn": "0",
        "tbs": "isz:m",
    })
    url = f"https://serpapi.com/search.json?{params}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return [
            {
                "url": img.get("original", ""),
                "title": img.get("title", ""),
                "width": img.get("original_width", 0),
                "height": img.get("original_height", 0),
            }
            for img in data.get("images_results", [])[:5]
            if img.get("original")
        ]
    except Exception as e:
        log(f"  SerpAPI error: {str(e)[:150]}")
        return []


def download_image(url: str, dest: Path) -> bool:
    try:
        r = subprocess.run(
            ["curl", "-sL", "-o", str(dest), "--max-time", "15", url],
            capture_output=True, timeout=20,
        )
        if r.returncode != 0:
            return False
        size = dest.stat().st_size if dest.exists() else 0
        if size < 10_000:
            dest.unlink(missing_ok=True)
            return False
        return True
    except Exception:
        dest.unlink(missing_ok=True)
        return False


def convert_to_webp(src: Path, dest: Path) -> bool:
    """Resize to 1080px wide, jpeg intermediate, then webp at q=80."""
    try:
        tmp_jpg = src.with_suffix(".opt.jpg")
        subprocess.run(
            ["sips", "-Z", "1080", "--setProperty", "format", "jpeg",
             "--setProperty", "formatOptions", "85", str(src), "--out", str(tmp_jpg)],
            capture_output=True, timeout=15,
        )
        r = subprocess.run(
            ["cwebp", "-quiet", "-q", "80", str(tmp_jpg), "-o", str(dest)],
            capture_output=True, timeout=15,
        )
        tmp_jpg.unlink(missing_ok=True)
        return r.returncode == 0 and dest.exists() and dest.stat().st_size > 5_000
    except Exception:
        return False


def upload_to_r2(local: Path, key: str, content_type: str = "image/webp") -> str | None:
    try:
        r = subprocess.run(
            ["curl", "-s", "-X", "PUT",
             "-H", f"Authorization: Bearer {CF_TOKEN}",
             "-H", f"Content-Type: {content_type}",
             "--data-binary", f"@{local}",
             f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{key}"],
            capture_output=True, text=True, timeout=60,
        )
        if r.returncode != 0:
            return None
        try:
            resp = json.loads(r.stdout) if r.stdout else {}
        except Exception:
            resp = {}
        if resp.get("success", True):
            return f"{R2_PUBLIC}/{key}"
        return None
    except Exception as e:
        log(f"  R2 upload error: {e}")
        return None


def build_query(name: str, country: str, region: str) -> list[str]:
    """Build a list of queries to try, in order of preference."""
    queries = []
    if country:
        queries.append(f"{name} {country} travel")
    if region and region.lower() != (country or "").lower():
        queries.append(f"{name} {region}")
    queries.append(f"{name} travel photography")
    queries.append(name)
    # Dedup preserving order
    seen = set(); out = []
    for q in queries:
        if q not in seen:
            seen.add(q); out.append(q)
    return out


def process_slug(slug: str, entry: dict, dry_run: bool = False) -> str | None:
    name = entry.get("name") or slug
    country = entry.get("country") or ""
    region = entry.get("region") or ""

    for query in build_query(name, country, region):
        log(f"  [{slug}] q='{query}'")
        results = search_google_images(query)
        if not results:
            continue

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            for i, img in enumerate(results):
                raw = td / f"raw_{i}.jpg"
                if not download_image(img["url"], raw):
                    continue
                webp = td / f"{slug}.webp"
                if not convert_to_webp(raw, webp):
                    raw.unlink(missing_ok=True)
                    continue
                if dry_run:
                    log(f"  [{slug}] DRY-RUN would upload {webp.stat().st_size} bytes")
                    return f"{R2_PUBLIC}/find/img/{slug}.webp (dry-run)"
                key = f"find/img/{slug}.webp"
                public = upload_to_r2(webp, key)
                if public:
                    log(f"  [{slug}] OK -> {public}")
                    return public
    log(f"  [{slug}] FAILED after all queries")
    return None


def scan_missing(full: dict) -> list[str]:
    return [s for s, e in full.items() if PLACEHOLDER_MARKER in str(e.get("photo", ""))]


def save_full(full: dict) -> None:
    tmp = FULL_JSON.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(full, f, separators=(",", ":"), ensure_ascii=False)
    tmp.replace(FULL_JSON)


def main() -> None:
    global SERPAPI_KEY, CF_TOKEN
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="Process at most N slugs (0=all)")
    ap.add_argument("--parallel", type=int, default=4, help="Worker threads (default 4)")
    ap.add_argument("--dry-run", action="store_true", help="Skip R2 upload + JSON write")
    ap.add_argument("--save-every", type=int, default=20, help="Save JSON every N completions")
    args = ap.parse_args()

    SERPAPI_KEY = get_keychain("serpapi-key")
    CF_TOKEN = get_keychain("cloudflare-pages-token")
    if not SERPAPI_KEY:
        sys.exit("ERROR: serpapi-key not found in keychain")
    if not CF_TOKEN:
        sys.exit("ERROR: cloudflare-pages-token not found in keychain")

    with open(FULL_JSON) as f:
        full = json.load(f)

    missing = scan_missing(full)
    log(f"Found {len(missing)} slugs on owl-logo in destinations-full.json")
    if args.limit:
        missing = missing[: args.limit]
        log(f"Limiting to {len(missing)} (--limit)")

    if not missing:
        log("Nothing to do.")
        return

    processed = 0
    succeeded = 0
    failed = 0
    completed_since_save = 0

    def worker(slug: str) -> tuple[str, str | None]:
        return slug, process_slug(slug, full[slug], dry_run=args.dry_run)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.parallel)) as ex:
        futures = [ex.submit(worker, s) for s in missing]
        for fut in concurrent.futures.as_completed(futures):
            slug, url = fut.result()
            processed += 1
            if url:
                succeeded += 1
                if not args.dry_run:
                    with _json_lock:
                        full[slug]["photo"] = url
                        full[slug]["updatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                        completed_since_save += 1
                        if completed_since_save >= args.save_every:
                            save_full(full)
                            completed_since_save = 0
                            log(f"  [checkpoint] saved destinations-full.json ({succeeded} ok, {failed} fail, {processed}/{len(missing)})")
            else:
                failed += 1
            if processed % 10 == 0 or processed == len(missing):
                log(f"Progress: {processed}/{len(missing)}  ok={succeeded}  fail={failed}")

    if not args.dry_run and completed_since_save > 0:
        with _json_lock:
            save_full(full)
        log("Final save of destinations-full.json")

    log(f"Done. ok={succeeded} fail={failed} total={processed}")


if __name__ == "__main__":
    main()
