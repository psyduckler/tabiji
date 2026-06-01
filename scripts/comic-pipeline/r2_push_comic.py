#!/usr/bin/env python3
"""Push a scam comic to R2: the 2048px .jpg print master plus a derived 1024px
.webp web variant, at scams/<city>/scam-<n>.{jpg,webp}.

The site's <img class="scam-comic"> tags load the .webp; the book pulls the .jpg.
generate.py only ever uploaded the .jpg, so the .webp had to be made separately —
this script does both from one local master, keeping the two in lock-step.

Modes:
  (default)      --jpg <path>: upload that local jpg as the master AND derive+upload the webp
  --webp-only    no --jpg: download the existing R2 jpg master and (re)build only the webp

Auth/upload reuses generate.upload_r2 (boto3 → R2 S3 endpoint, content-type from
magic bytes). After pushing, bump the page's ?v= with cachebust.py so the CDN
serves fresh bytes.

Usage:
    python3 scripts/comic-pipeline/r2_push_comic.py atlanta 2 --jpg /tmp/us-regen/atlanta_scam-2.jpg
    python3 scripts/comic-pipeline/r2_push_comic.py savannah 5 --webp-only
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import download_verify, upload_r2  # noqa: E402  (boto3 S3 helpers)

WEBP_EDGE = 1024   # web variant long edge — matches existing convention
WEBP_QUALITY = 82


def _make_webp(jpg_path: Path, webp_path: Path) -> None:
    from PIL import Image
    with Image.open(jpg_path) as im:
        im = im.convert("RGB")
        if max(im.size) > WEBP_EDGE:
            im.thumbnail((WEBP_EDGE, WEBP_EDGE), Image.LANCZOS)
        im.save(webp_path, "WEBP", quality=WEBP_QUALITY, method=6)


def push(city: str, n: int, jpg: Path | None, webp_only: bool) -> dict:
    out = {"city": city, "n": n, "jpg": None, "webp": None}
    jpg_key = f"scams/{city}/scam-{n}.jpg"
    webp_key = f"scams/{city}/scam-{n}.webp"
    tmp = Path(tempfile.mkdtemp(prefix="r2push-"))
    try:
        if webp_only:
            # Reuse generate.download_verify (same UA + JPEG check + 120KB floor)
            # rather than a weaker hand-rolled fetch, so a truncated master can't
            # slip through into a broken webp.
            src_jpg = tmp / "master.jpg"
            ok_dl, note = download_verify(f"https://img.tabiji.ai/{jpg_key}", src_jpg)
            if not ok_dl:
                return {**out, "error": f"could not fetch existing R2 jpg master: {note}"}
        else:
            if not jpg or not jpg.exists():
                return {**out, "error": "missing --jpg <path>"}
            src_jpg = jpg
            out["jpg"] = "ok" if upload_r2(src_jpg, jpg_key, "") else "FAILED"
            if out["jpg"] == "FAILED":
                # Never ship a fresh webp paired with a stale jpg master — that
                # is the exact jpg/webp desync this script exists to prevent.
                return {**out, "error": "jpg master upload failed — skipped webp to avoid desync"}

        webp_path = tmp / "variant.webp"
        _make_webp(src_jpg, webp_path)
        out["webp"] = "ok" if upload_r2(webp_path, webp_key, "") else "FAILED"
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("city")
    ap.add_argument("n", type=int)
    ap.add_argument("--jpg", default=None, help="local jpg master to upload")
    ap.add_argument("--webp-only", action="store_true",
                    help="rebuild only the webp from the existing R2 jpg")
    a = ap.parse_args()
    res = push(a.city, a.n, Path(a.jpg) if a.jpg else None, a.webp_only)
    print(json.dumps(res))
    sys.exit(1 if res.get("error") or "FAILED" in (res.get("jpg"), res.get("webp")) else 0)


if __name__ == "__main__":
    main()
