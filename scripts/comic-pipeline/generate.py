#!/usr/bin/env python3
"""End-to-end comic generation pipeline — one scam at a time.

For each scam on a city's page:
1. Extract title, location, first story paragraph from the city's index.html
2. Call synthesize.synthesize_prompt() — Gemini produces a bespoke character +
   4-panel scene for this specific scam
3. Submit full Nano Banana Pro prompt via /edit with the country pilot as style anchor
4. Poll until completed (timeout 600s)
5. Download + verify (JPEG header + file-size threshold)
6. If first attempt fails quality gate: re-submit once via /text-to-image
   (more permissive content filter)
7. If still bad: flag for manual review — do NOT silently replace

Designed for print/publication quality. Expensive on purpose — each scam
gets a bespoke Gemini synthesis call + at least one Nano Banana Pro generation.

Usage:
    python3 scripts/comic-pipeline/generate.py germany berlin munich
    # Regenerates all scams for Berlin and Munich in the Germany style
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from synthesize import synthesize_prompt  # noqa: E402
from styles import PILOTS  # noqa: E402

REPO = _HERE.parent.parent  # /Users/bjh/Documents/tabiji/... or worktree
EDIT_EP = "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/edit"
T2I_EP = "https://api.wavespeed.ai/api/v3/google/nano-banana-pro/text-to-image"
RESULT_EP = "https://api.wavespeed.ai/api/v3/predictions/{}/result"

R2_ACCT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"

MIN_IMAGE_BYTES = 120_000  # below this is suspected as malformed / tiny


def _keychain(service: str) -> str:
    """Read credential from macOS keychain, with env-var fallback for non-macOS hosts.

    Service-name → env-var mapping is the ALL-CAPS, hyphens-to-underscores form:
      gemini-api-key       → GEMINI_API_KEY
      wavespeed-api-key    → WAVESPEED_API_KEY
      cloudflare-api-token → CLOUDFLARE_API_TOKEN

    Raises RuntimeError if neither source has the credential, so the caller fails
    loudly instead of submitting an empty Bearer token to the upstream API.
    """
    import os, shutil
    if shutil.which("security"):
        try:
            out = subprocess.run(
                ["security", "find-generic-password", "-s", service, "-w"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            if out:
                return out
        except subprocess.CalledProcessError:
            pass
    val = os.environ.get(service.upper().replace("-", "_"), "").strip()
    if not val:
        raise RuntimeError(
            f"missing credential for '{service}': not in macOS keychain "
            f"and ${service.upper().replace('-', '_')} env var is unset"
        )
    return val


def extract_scams(city: str) -> list[dict]:
    """Extract every scam card's title, location, and first story paragraph."""
    path = REPO / f"scams/{city}/index.html"
    html = path.read_text()
    out = []
    for cm in re.finditer(
        r'<div class="scam-card"[^>]*id="(scam-\d+)"[^>]*>(.*?)(?=<div class="scam-card"|<section|</section|$)',
        html, re.DOTALL,
    ):
        sid = cm.group(1)
        body = cm.group(2)
        tm = re.search(r'<div class="scam-title">([^<]+)</div>', body)
        loc = re.search(r'<div class="scam-location">([^<]+)</div>', body)
        # Story: first TLDR + first story paragraph if available
        story_parts = []
        for pm in re.finditer(r'<p class="scam-(?:tldr|story|story-body)">([^<]{50,2000})</p>', body):
            story_parts.append(pm.group(1).strip())
            if len(" ".join(story_parts)) > 1200:
                break
        if tm:
            out.append({
                "n": int(sid.split("-")[1]),
                "title": tm.group(1).strip(),
                "location": (loc.group(1).strip() if loc else "").replace("📍", "").strip(),
                "story": " ".join(story_parts),
                "city": city,
            })
    return out


def _api_post(url: str, body: bytes, token: str) -> dict:
    req = urllib.request.Request(url, method="POST", data=body)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def _api_get(url: str, token: str) -> dict:
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def submit_nbp(body: dict, endpoint: str, ws_token: str) -> str | None:
    """Submit to Nano Banana Pro, handle 429 backoff, return task id."""
    payload_body = {k: v for k, v in body.items() if not k.startswith("_")}
    if endpoint == T2I_EP:
        payload_body.pop("images", None)
        payload_body.setdefault("resolution", "2k")
    payload = json.dumps(payload_body).encode()
    for attempt in range(5):
        try:
            d = _api_post(endpoint, payload, ws_token)
            if d.get("code") == 200:
                return d["data"]["id"]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(3 + attempt * 2)
                continue
            return None
        except Exception:
            return None
    return None


def poll_nbp(task_id: str, ws_token: str, timeout: int = 600) -> str | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            d = _api_get(RESULT_EP.format(task_id), ws_token)
            data = d["data"]
            if data["status"] == "completed":
                out = data.get("outputs")
                return out[0] if out else None
            if data["status"] == "failed":
                return None
        except Exception:
            pass
        time.sleep(7)
    return None


def download_verify(url: str, out_path: Path) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except Exception as e:
        return False, f"download err: {e}"
    if len(data) < MIN_IMAGE_BYTES:
        return False, f"too small ({len(data)}B)"
    if data[:3] != b"\xff\xd8\xff":
        return False, "not JPEG"
    out_path.write_bytes(data)
    return True, "ok"


_S3_CLIENT = None


def _s3_client():
    """Lazy-init boto3 S3 client pointed at the R2 S3-compatible endpoint.

    Reads two new keychain entries (with env-var fallbacks):
      cloudflare-r2-access-key-id      → CLOUDFLARE_R2_ACCESS_KEY_ID
      cloudflare-r2-secret-access-key  → CLOUDFLARE_R2_SECRET_ACCESS_KEY

    The earlier `cloudflare-api-token` (Bearer-style) doesn't have R2
    write scope on this account, so the v4 Cloudflare API path silently
    fails. The S3-compatible endpoint with the access keys does work.
    """
    global _S3_CLIENT
    if _S3_CLIENT is not None:
        return _S3_CLIENT
    try:
        import boto3
        from botocore.config import Config as _BotoConfig
    except ImportError as e:
        raise RuntimeError(
            "boto3 not available — install with `pip3 install boto3`"
        ) from e
    _S3_CLIENT = boto3.client(
        "s3",
        endpoint_url=f"https://{R2_ACCT}.r2.cloudflarestorage.com",
        aws_access_key_id=_keychain("cloudflare-r2-access-key-id"),
        aws_secret_access_key=_keychain("cloudflare-r2-secret-access-key"),
        config=_BotoConfig(signature_version="s3v4", region_name="auto"),
    )
    return _S3_CLIENT


def upload_r2(src: Path, r2_key: str, _r2_token: str) -> bool:
    """Upload a JPEG to R2 via the S3-compatible endpoint.

    The `_r2_token` arg is preserved for backward-compat with callers but
    no longer used — auth comes from the access-key/secret pair stored
    under the cloudflare-r2-{access-key-id,secret-access-key} keychain
    entries.
    """
    body = src.read_bytes()
    for attempt in range(5):
        try:
            _s3_client().put_object(
                Bucket=R2_BUCKET, Key=r2_key, Body=body,
                ContentType="image/jpeg",
                CacheControl="public, max-age=31536000, immutable",
            )
            return True
        except Exception as e:
            transient = any(s in str(e).lower() for s in
                            ("throttl", "timeout", "503", "502", "500", "429"))
            if transient and attempt < 4:
                time.sleep(3 + attempt * 3)
                continue
            return False
    return False


def generate_one(
    country: str,
    scam: dict,
    out_dir: Path,
    ws_token: str,
    r2_token: str,
    force: bool = False,
) -> dict:
    """Full one-scam pipeline. Returns status dict with keys:
    status: "ok" | "ok-retried" | "flagged"
    note: explanation
    character: chosen cast member
    prompt: the full Nano Banana Pro prompt that was used (for audit)
    """
    city = scam["city"]
    n = scam["n"]
    out_path = out_dir / f"{city}_scam-{n}.jpg"

    if out_path.exists() and out_path.stat().st_size >= MIN_IMAGE_BYTES and not force:
        return {"status": "ok-cached", "note": f"{out_path.stat().st_size}B",
                "character": "?", "prompt": None}

    # 1) Synthesize bespoke prompt via Gemini
    try:
        body = synthesize_prompt(country, scam)
    except Exception as e:
        return {"status": "flagged", "note": f"synthesize err: {e}",
                "character": "?", "prompt": None}

    chosen = body["_character"]
    audit_prompt = body["prompt"][:300]  # short snippet for the log

    # 2) First pass: /edit (style-locked via pilot)
    tid = submit_nbp(body, EDIT_EP, ws_token)
    if tid:
        url = poll_nbp(tid, ws_token)
        if url:
            ok, note = download_verify(url, out_path)
            if ok:
                if upload_r2(out_path, f"scams/{city}/scam-{n}.jpg", r2_token):
                    return {"status": "ok", "note": note, "character": chosen,
                            "prompt": audit_prompt}

    # 3) Retry: /text-to-image (permissive filter)
    tid = submit_nbp(body, T2I_EP, ws_token)
    if tid:
        url = poll_nbp(tid, ws_token)
        if url:
            ok, note = download_verify(url, out_path)
            if ok:
                if upload_r2(out_path, f"scams/{city}/scam-{n}.jpg", r2_token):
                    return {"status": "ok-retried", "note": note, "character": chosen,
                            "prompt": audit_prompt}

    return {"status": "flagged", "note": "both passes failed",
            "character": chosen, "prompt": audit_prompt}


def run(country: str, cities: list[str], batch_size: int = 3, force: bool = False) -> dict:
    """Top-level orchestrator.

    Processes `batch_size` scams concurrently (default 3). Quality-gates each.
    Returns summary dict.
    """
    out_dir = Path(f"/tmp/{country}-comics-v2")
    out_dir.mkdir(parents=True, exist_ok=True)
    audit_log = Path(f"/tmp/{country}-audit.jsonl")
    audit_log.write_text("")
    flagged_log = Path(f"/tmp/{country}-flagged.log")
    flagged_log.write_text("")

    ws_token = _keychain("wavespeed-api-key")
    r2_token = _keychain("cloudflare-api-token")

    all_scams = []
    for city in cities:
        all_scams.extend(extract_scams(city))
    print(f"[{country}] processing {len(all_scams)} scams across {len(cities)} cities "
          f"(batch size {batch_size})", flush=True)

    ok = retried = flagged = 0
    for i in range(0, len(all_scams), batch_size):
        batch = all_scams[i:i + batch_size]
        print(f"\n=== batch {i // batch_size + 1} ({len(batch)} items) ===", flush=True)
        with ThreadPoolExecutor(max_workers=batch_size) as ex:
            futures = [ex.submit(generate_one, country, s, out_dir, ws_token, r2_token, force)
                       for s in batch]
            for s, f in zip(batch, futures):
                res = f.result()
                label = f"{s['city']}/scam-{s['n']}"
                line = f"{label}: {res['status']} char={res['character']} ({res['note']})"
                print(f"  {line}", flush=True)
                audit_log.open("a").write(json.dumps({
                    "city": s["city"], "n": s["n"], "title": s["title"], **res,
                }) + "\n")
                if res["status"] in ("ok", "ok-cached"):
                    ok += 1
                elif res["status"] == "ok-retried":
                    retried += 1
                    ok += 1
                else:
                    flagged += 1
                    flagged_log.open("a").write(line + "\n")

    summary = {
        "country": country, "total": len(all_scams),
        "ok": ok, "retried": retried, "flagged": flagged,
        "audit_log": str(audit_log), "flagged_log": str(flagged_log),
    }
    print(f"\n[{country}] FINAL: {json.dumps(summary)}", flush=True)
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("country", help="country slug (e.g. germany)")
    p.add_argument("cities", nargs="+", help="one or more city slugs")
    p.add_argument("--batch-size", type=int, default=3)
    p.add_argument("--force", action="store_true",
                   help="Regenerate even if a local file already exists")
    args = p.parse_args()
    run(args.country, args.cities, args.batch_size, args.force)
