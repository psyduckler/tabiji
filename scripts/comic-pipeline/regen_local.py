#!/usr/bin/env python3
"""Generate ONE scam comic to a LOCAL file using the hardened pipeline — NO R2 upload.

This is the "generate" half of the audited regeneration loop: produce the image
locally, let an auditor view it, and push to production R2 only once it passes
(see r2_push_comic.py). Keeping the upload out of this step is deliberate — it
prevents an unverified image from ever reaching the live CDN.

Reuses the production generator's internals (synthesize → Nano Banana Pro /edit
with /text-to-image fallback → JPEG+size verify) from generate.py, so the only
behavioural difference vs `generate.py` is "don't upload".

Usage:
    python3 scripts/comic-pipeline/regen_local.py united-states atlanta 2
    python3 scripts/comic-pipeline/regen_local.py united-states atlanta 2 --out /tmp/x.jpg

Prints a single JSON line describing the result; exits 0 on success, 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import (  # noqa: E402
    extract_scams, submit_nbp, poll_nbp, download_verify, _keychain,
    EDIT_EP, T2I_EP,
)
from synthesize import synthesize_prompt  # noqa: E402


def regen_one(country: str, city: str, n: int, out_path: Path, avoid: str = "") -> dict:
    scams = {s["n"]: s for s in extract_scams(city)}
    if n not in scams:
        return {"city": city, "n": n, "status": "error",
                "note": f"scam {n} not on scams/{city}/index.html (have {sorted(scams)})"}
    scam = scams[n]
    ws = _keychain("wavespeed-api-key")
    try:
        body = synthesize_prompt(country, scam)
    except Exception as e:
        return {"city": city, "n": n, "status": "error", "note": f"synthesize: {e}",
                "title": scam["title"]}
    # Per-comic override: explicitly neutralize the specific defect that made
    # earlier attempts fail (a garbled prop, a trademark the scam is about, etc.).
    if avoid:
        body["prompt"] += (
            "\n\nCRITICAL — FIX THESE SPECIFIC DEFECTS that ruined previous versions of this "
            f"exact comic (highest priority, overrides scene detail): {avoid}"
        )
    char = body.get("_character", "?")

    # Pass 1: /edit (style-locked via country pilot). Pass 2: /text-to-image.
    for endpoint, label in ((EDIT_EP, "edit"), (T2I_EP, "t2i")):
        tid = submit_nbp(body, endpoint, ws)
        if not tid:
            continue
        url = poll_nbp(tid, ws)
        if not url:
            continue
        ok, note = download_verify(url, out_path)
        if ok:
            dims = "?"
            try:
                from PIL import Image
                with Image.open(out_path) as im:
                    dims = f"{im.size[0]}x{im.size[1]}"
            except Exception:
                pass
            return {"city": city, "n": n, "status": "ok", "via": label,
                    "path": str(out_path), "bytes": out_path.stat().st_size,
                    "dims": dims, "character": char, "title": scam["title"]}

    return {"city": city, "n": n, "status": "failed", "note": "both passes failed",
            "character": char, "title": scam["title"]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("country", help="country style slug, e.g. united-states")
    ap.add_argument("city", help="city slug, e.g. atlanta")
    ap.add_argument("n", type=int, help="scam number")
    ap.add_argument("--out", default=None, help="output path (default /tmp/us-regen/<city>_scam-<n>.jpg)")
    ap.add_argument("--avoid", default="", help="per-comic defect to neutralize (appended to the NBP prompt)")
    a = ap.parse_args()
    out = Path(a.out) if a.out else Path(f"/tmp/us-regen/{a.city}_scam-{a.n}.jpg")
    out.parent.mkdir(parents=True, exist_ok=True)
    res = regen_one(a.country, a.city, a.n, out, a.avoid)
    print(json.dumps(res))
    sys.exit(0 if res.get("status") == "ok" else 1)


if __name__ == "__main__":
    main()
