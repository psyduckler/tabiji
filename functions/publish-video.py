#!/usr/bin/env python3
"""
publish-video.py — Unified publish pipeline for Tabiji video content.

Handles: Instagram Reel, YouTube Shorts, Facebook Page Reel,
         TikTok R2 staging, X staging, and #mission-control notification.

Usage (CLI):
    python3 publish-video.py --video reel.mp4 --caption "Caption here #travel"
    python3 publish-video.py --video reel.mp4 --caption "..." --thumb-offset 2000 --platforms ig,fb,tiktok
    python3 publish-video.py --video reel.mp4 --caption "..." --skip-publish  # R2 staging only

Usage (module):
    from publish_video import publish_video
    result = publish_video(video_path="reel.mp4", caption="...", thumb_offset=2000)

All credentials from macOS Keychain. Returns JSON summary on success.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"
R2_PUBLIC = "https://img.tabiji.ai"
IG_ACCOUNT = "17841449394591017"
FB_PAGE = "902878896251805"
MISSION_CONTROL_CHANNEL = "C0AEMUG5K8X"
PUBLISH_LOG = Path(__file__).parent / "publish-log.json"
DEDUP_WINDOW_HOURS = 24

PLATFORMS_ALL = ["ig", "yt", "fb", "tiktok", "x"]
PLATFORMS_DEFAULT = ["ig", "yt", "fb", "tiktok"]

# ── Publish Dedup ───────────────────────────────────────────────────────────

def video_fingerprint(video_path, caption):
    """Fast fingerprint for dedup: video filename + size + caption first line."""
    stat = os.stat(video_path)
    first_line = caption.split("\n")[0][:120]
    raw = f"{os.path.basename(video_path)}|{stat.st_size}|{first_line}"
    return hashlib.md5(raw.encode()).hexdigest()


def _load_publish_log():
    """Load publish log, returning list of entries."""
    if not PUBLISH_LOG.exists():
        return []
    try:
        with open(PUBLISH_LOG) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save_publish_log(entries):
    """Save publish log (keep last 500 entries)."""
    entries = entries[-500:]
    with open(PUBLISH_LOG, "w") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def check_dedup(fingerprint, title=""):
    """Check if this fingerprint or title was already published within the dedup window.
    Returns dict of {platform: url} for platforms that already succeeded, or {}.
    Uses BOTH fingerprint match AND title match to prevent double-posts
    from sub-agents that regenerate videos with different files."""
    entries = _load_publish_log()
    cutoff = time.time() - (DEDUP_WINDOW_HOURS * 3600)
    already = {}
    title_norm = title.strip().lower()[:100] if title else ""
    for entry in entries:
        ts = entry.get("ts", 0)
        if ts < cutoff:
            continue
        # Match by fingerprint OR by title
        fp_match = entry.get("fingerprint") == fingerprint
        entry_title_norm = (entry.get("title", "") or "").strip().lower()[:100]
        title_match = title_norm and entry_title_norm and title_norm == entry_title_norm
        if not fp_match and not title_match:
            continue
        for plat, url in entry.get("platforms", {}).items():
            if url:
                already[plat] = url
    return already


def record_publish(fingerprint, platform, url, title=""):
    """Record a successful publish to the dedup log."""
    entries = _load_publish_log()
    # Update existing entry for this fingerprint if within window
    cutoff = time.time() - (DEDUP_WINDOW_HOURS * 3600)
    updated = False
    for entry in entries:
        if entry.get("fingerprint") == fingerprint and entry.get("ts", 0) >= cutoff:
            entry["platforms"][platform] = url
            updated = True
            break
    if not updated:
        entries.append({
            "fingerprint": fingerprint,
            "ts": int(time.time()),
            "title": title[:100],
            "platforms": {platform: url},
        })
    _save_publish_log(entries)


# ── Keychain ───────────────────────────────────────────────────────────────

def get_key(name):
    """Read value from macOS Keychain. Returns None on failure."""
    result = subprocess.run(
        ["security", "find-generic-password", "-s", name, "-w"],
        capture_output=True, text=True, timeout=10
    )
    return result.stdout.strip() if result.returncode == 0 else None


# ── R2 Helpers ─────────────────────────────────────────────────────────────

def r2_upload(local_path, r2_key, content_type="video/mp4", token=None):
    """Upload file to R2. Returns public URL."""
    token = token or get_key("cloudflare-pages-token")
    if not token:
        raise RuntimeError("No cloudflare-pages-token in keychain")

    result = subprocess.run([
        "curl", "-s", "-X", "PUT",
        "-H", f"Authorization: Bearer {token}",
        "-H", f"Content-Type: {content_type}",
        "--data-binary", f"@{local_path}",
        f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}"
    ], capture_output=True, text=True, timeout=180)

    resp = json.loads(result.stdout)
    if not resp.get("success"):
        raise RuntimeError(f"R2 upload failed for {r2_key}: {resp}")

    url = f"{R2_PUBLIC}/{r2_key}"
    print(f"  📤 R2: {url}")
    return url


def r2_upload_bytes(data, r2_key, content_type="text/plain; charset=utf-8", token=None):
    """Upload bytes/string to R2 via temp file. Returns public URL."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(data)
        tmp = f.name
    try:
        return r2_upload(tmp, r2_key, content_type, token)
    finally:
        os.unlink(tmp)


def r2_delete(r2_key, token=None):
    """Delete object from R2. Non-blocking."""
    token = token or get_key("cloudflare-pages-token")
    if not token:
        return
    subprocess.run([
        "curl", "-s", "-X", "DELETE",
        "-H", f"Authorization: Bearer {token}",
        f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}"
    ], capture_output=True, text=True, timeout=30)


def r2_wait_for_edge(url, max_wait=60):
    """Wait for R2 edge to serve the URL. Returns True if accessible."""
    time.sleep(5)  # Initial propagation delay
    for i in range(max_wait // 5):
        try:
            result = subprocess.run(
                ["curl", "-sI", url, "-o", "/dev/null", "-w", "%{http_code}"],
                capture_output=True, text=True, timeout=15
            )
            if result.stdout.strip() == "200":
                return True
        except Exception:
            pass
        time.sleep(5)
    return False


# ── Instagram ─────────────────────────────────────────────────────────────

def publish_ig(video_path, caption, thumb_offset=1000, r2_key=None):
    """Publish Reel to Instagram. Returns (media_id, permalink) or raises."""
    token = get_key("instagram-access-token")
    if not token:
        raise RuntimeError("No instagram-access-token in keychain")

    # Upload to R2 temp
    ts = int(time.time())
    r2_key = r2_key or f"tmp/publish-video/ig-{ts}.mp4"
    cf_token = get_key("cloudflare-pages-token")

    video_url = r2_upload(video_path, r2_key, token=cf_token)
    print("  ⏳ Waiting for R2 edge...")
    if not r2_wait_for_edge(video_url):
        raise RuntimeError(f"R2 edge not serving: {video_url}")

    # Create container
    print(f"  📱 Creating IG container (thumb_offset={thumb_offset}ms)...")
    params = urllib.parse.urlencode({
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "thumb_offset": thumb_offset,
        "share_to_feed": "true",
        "access_token": token,
    })
    req = urllib.request.Request(
        f"https://graph.facebook.com/v22.0/{IG_ACCOUNT}/media",
        data=params.encode(), method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        container = json.loads(resp.read())

    container_id = container.get("id")
    if not container_id:
        raise RuntimeError(f"IG container creation failed: {container}")
    print(f"  📦 Container: {container_id}")

    # Poll for processing
    print("  ⏳ IG processing...")
    status_code = "UNKNOWN"
    for attempt in range(24):
        time.sleep(10)
        status_url = (
            f"https://graph.facebook.com/v22.0/{container_id}"
            f"?fields=status_code,status&access_token={token}"
        )
        with urllib.request.urlopen(status_url, timeout=15) as resp:
            status = json.loads(resp.read())

        status_code = status.get("status_code", "UNKNOWN")
        print(f"    [{(attempt+1)*10}s] {status_code}")

        if status_code == "FINISHED":
            break
        elif status_code == "ERROR":
            raise RuntimeError(f"IG processing failed: {status}")

    if status_code != "FINISHED":
        if status_code == "UNKNOWN":
            print(f"  ⚠️ IG processing status UNKNOWN after polling — attempting publish anyway")
        else:
            raise RuntimeError(f"IG processing timed out (last: {status_code})")

    # Publish
    print("  🚀 Publishing IG Reel...")
    params = urllib.parse.urlencode({
        "creation_id": container_id,
        "access_token": token,
    })
    req = urllib.request.Request(
        f"https://graph.facebook.com/v22.0/{IG_ACCOUNT}/media_publish",
        data=params.encode(), method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())

    media_id = result.get("id")
    if not media_id:
        raise RuntimeError(f"IG publish failed: {result}")

    # Get permalink
    time.sleep(3)
    permalink = ""
    try:
        with urllib.request.urlopen(
            f"https://graph.facebook.com/v22.0/{media_id}?fields=permalink&access_token={token}",
            timeout=15
        ) as resp:
            permalink = json.loads(resp.read()).get("permalink", "")
    except Exception:
        pass

    # Cleanup R2 temp
    r2_delete(r2_key, cf_token)

    url = permalink or f"https://www.instagram.com/reel/{media_id}"
    print(f"  ✅ IG: {url}")
    return media_id, url


# ── YouTube Shorts ────────────────────────────────────────────────────────

def publish_yt(video_path, title, description="", tags="travel,tabiji", thumbnail_path=None):
    """Upload to YouTube Shorts. Returns video URL or raises."""
    client_id = get_key("youtube-client-id")
    client_secret = get_key("youtube-client-secret")
    refresh_token = get_key("youtube-refresh-token")

    if not all([client_id, client_secret, refresh_token]):
        raise RuntimeError("YouTube credentials not found in keychain")

    # Refresh access token
    token_data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=token_data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        access_token = json.loads(resp.read())["access_token"]

    # Build metadata
    metadata = {
        "snippet": {
            "title": title[:100],
            "description": description or title,
            "tags": [t.strip() for t in tags.split(",") if t.strip()],
            "categoryId": "19",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        }
    }

    # Resumable upload init
    print("  📺 Uploading to YouTube...")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(metadata, f)
        meta_path = f.name

    try:
        init_result = subprocess.run([
            "curl", "-s", "-X", "POST",
            "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
            "-H", f"Authorization: Bearer {access_token}",
            "-H", "Content-Type: application/json",
            "-d", f"@{meta_path}",
            "-D", "-", "-o", "/dev/null"
        ], capture_output=True, text=True, timeout=30)

        upload_url = ""
        for line in init_result.stdout.split("\n"):
            if line.lower().startswith("location:"):
                upload_url = line.split(": ", 1)[1].strip()
                break

        if not upload_url:
            raise RuntimeError(f"No upload URL from YouTube: {init_result.stdout[:500]}")

        # Upload video binary
        upload_result = subprocess.run([
            "curl", "-s", "-X", "PUT", upload_url,
            "-H", "Content-Type: video/mp4",
            "--data-binary", f"@{video_path}"
        ], capture_output=True, text=True, timeout=300)

        clean = re.sub(r'[\x00-\x1f]', ' ', upload_result.stdout)
        yt_data = json.loads(clean)
        video_id = yt_data.get("id")

        if not video_id:
            raise RuntimeError(f"YouTube upload failed: {clean[:500]}")

    finally:
        os.unlink(meta_path)

    yt_url = f"https://youtube.com/shorts/{video_id}"
    print(f"  📺 Uploaded: {yt_url}")

    # Set thumbnail if provided
    if thumbnail_path and os.path.exists(thumbnail_path):
        print("  🖼 Setting YT thumbnail...")
        subprocess.run([
            "curl", "-s", "-X", "POST",
            f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}&uploadType=media",
            "-H", f"Authorization: Bearer {access_token}",
            "-H", "Content-Type: image/jpeg",
            "--data-binary", f"@{thumbnail_path}"
        ], capture_output=True, text=True, timeout=30)
        print("  ✓ Thumbnail set")

    print(f"  ✅ YT: {yt_url}")
    return yt_url


# ── Facebook Page Reel ────────────────────────────────────────────────────

def publish_fb(video_path, caption):
    """Publish Reel to Facebook Page. Returns URL or empty string (non-blocking)."""
    token = get_key("instagram-access-token")  # same token covers IG + FB
    page_id = get_key("facebook-page-id") or FB_PAGE

    if not token:
        print("  ⚠️ FB: No token")
        return ""

    file_size = os.path.getsize(video_path)

    try:
        # Init
        result = subprocess.run([
            "curl", "-s", "-X", "POST",
            f"https://graph.facebook.com/v22.0/{page_id}/video_reels",
            "-d", "upload_phase=start",
            "-d", f"access_token={token}"
        ], capture_output=True, text=True, timeout=30)
        init = json.loads(result.stdout)

        video_id = init.get("video_id")
        upload_url = init.get("upload_url", f"https://rupload.facebook.com/video-upload/v22.0/{video_id}")
        if not video_id:
            print(f"  ⚠️ FB init failed: {init}")
            return ""

        # Upload binary
        result = subprocess.run([
            "curl", "-s", "-X", "POST", upload_url,
            "-H", f"Authorization: OAuth {token}",
            "-H", "offset: 0",
            "-H", f"file_size: {file_size}",
            "-H", "Content-Type: application/octet-stream",
            "--data-binary", f"@{video_path}"
        ], capture_output=True, text=True, timeout=120)
        upload = json.loads(result.stdout)

        if not upload.get("success"):
            print(f"  ⚠️ FB upload failed: {upload}")
            return ""

        # Publish
        result = subprocess.run([
            "curl", "-s", "-X", "POST",
            f"https://graph.facebook.com/v22.0/{page_id}/video_reels",
            "-d", "upload_phase=finish",
            "-d", f"video_id={video_id}",
            "-d", "video_state=PUBLISHED",
            "--data-urlencode", f"description={caption}",
            "-d", f"access_token={token}"
        ], capture_output=True, text=True, timeout=30)
        finish = json.loads(result.stdout)

        if finish.get("success") or finish.get("post_id"):
            fb_url = f"https://www.facebook.com/reel/{video_id}"
            print(f"  ✅ FB: {fb_url}")
            return fb_url
        else:
            print(f"  ⚠️ FB publish failed: {finish}")
            return ""

    except Exception as e:
        print(f"  ⚠️ FB error (non-blocking): {e}")
        return ""


# ── TikTok Publishing ────────────────────────────────────────────────────

def refresh_tiktok_token():
    """Refresh TikTok access token. Stores new tokens in keychain. Returns access_token or None."""
    client_key = get_key("tiktok-client-key")
    client_secret = get_key("tiktok-client-secret")
    refresh_token = get_key("tiktok-refresh-token")

    if not all([client_key, client_secret, refresh_token]):
        print("  ⚠️ TikTok: Missing credentials for token refresh")
        return None

    try:
        result = subprocess.run([
            "curl", "-s", "-X", "POST",
            "https://open.tiktokapis.com/v2/oauth/token/",
            "-H", "Content-Type: application/x-www-form-urlencoded",
            "-d", f"client_key={client_key}",
            "-d", f"client_secret={client_secret}",
            "-d", "grant_type=refresh_token",
            "-d", f"refresh_token={refresh_token}",
        ], capture_output=True, text=True, timeout=30)

        data = json.loads(result.stdout)
        if data.get("access_token"):
            # Update keychain
            subprocess.run(["security", "add-generic-password", "-U", "-s", "tiktok-access-token", "-a", "tabijiai", "-w", data["access_token"]], capture_output=True, timeout=10)
            if data.get("refresh_token"):
                subprocess.run(["security", "add-generic-password", "-U", "-s", "tiktok-refresh-token", "-a", "tabijiai", "-w", data["refresh_token"]], capture_output=True, timeout=10)
            if data.get("open_id"):
                subprocess.run(["security", "add-generic-password", "-U", "-s", "tiktok-open-id", "-a", "tabijiai", "-w", data["open_id"]], capture_output=True, timeout=10)
            print("  🔄 TikTok token refreshed")
            return data["access_token"]
        else:
            print(f"  ⚠️ TikTok refresh failed: {data}")
            return None
    except Exception as e:
        print(f"  ⚠️ TikTok refresh error: {e}")
        return None


def get_tiktok_token():
    """Get a valid TikTok access token, refreshing if needed. Returns token or None."""
    token = get_key("tiktok-access-token")
    if token:
        return token
    return refresh_tiktok_token()


def publish_tiktok(video_path, caption, slug="untitled"):
    """Publish video directly to TikTok via Content Posting API (Direct Post).
    Uploads video to R2, then tells TikTok to pull from URL.
    Returns TikTok publish URL or raises."""
    access_token = get_tiktok_token()
    if not access_token:
        raise RuntimeError("No TikTok access token — authorize at /media/dashboard/")

    # Upload video to R2 (TikTok pulls from URL)
    ts = int(time.time())
    base = f"{slug}-{ts}"
    cf_token = get_key("cloudflare-pages-token")

    r2_key = f"tmp/tiktok/{base}.mp4"
    video_url = r2_upload(video_path, r2_key, token=cf_token)
    print("  ⏳ Waiting for R2 edge...")
    if not r2_wait_for_edge(video_url):
        raise RuntimeError(f"R2 edge not serving TikTok video: {video_url}")

    # TikTok caption limit: 2200 chars, no hashtags in description for SEO
    tiktok_caption = caption[:2200]

    # Init direct post (TikTok pulls video from URL)
    post_info = {
        "title": tiktok_caption[:150],  # TikTok title max 150 chars
        "privacy_level": "PUBLIC_TO_EVERYONE",
        "disable_duet": False,
        "disable_comment": False,
        "disable_stitch": False,
        "video_cover_timestamp_ms": 1000,
    }

    source_info = {
        "source": "PULL_FROM_URL",
        "video_url": video_url,
    }

    print("  🎵 Initiating TikTok direct post...")
    result = subprocess.run([
        "curl", "-s", "-X", "POST",
        "https://tabiji.ai/api/tiktok-post",
        "-H", "Content-Type: application/json",
        "--data-raw", json.dumps({
            "access_token": access_token,
            "post_info": post_info,
            "source_info": source_info,
        }),
    ], capture_output=True, text=True, timeout=60)

    resp = json.loads(result.stdout)

    # TikTok response: { "data": { "publish_id": "..." }, "error": { "code": "ok" } }
    if resp.get("error", {}).get("code") != "ok":
        err = resp.get("error", {})
        err_msg = err.get("message", str(err))
        # If token expired, try refresh and retry once
        if err.get("code") == "access_token_expired" or "token" in err_msg.lower():
            print("  🔄 TikTok token expired, refreshing...")
            access_token = refresh_tiktok_token()
            if access_token:
                result = subprocess.run([
                    "curl", "-s", "-X", "POST",
                    "https://tabiji.ai/api/tiktok-post",
                    "-H", "Content-Type: application/json",
                    "--data-raw", json.dumps({
                        "access_token": access_token,
                        "post_info": post_info,
                        "source_info": source_info,
                    }),
                ], capture_output=True, text=True, timeout=60)
                resp = json.loads(result.stdout)
                if resp.get("error", {}).get("code") != "ok":
                    raise RuntimeError(f"TikTok post failed after refresh: {resp.get('error', {})}")
            else:
                raise RuntimeError(f"TikTok token refresh failed, cannot post: {err_msg}")
        else:
            raise RuntimeError(f"TikTok post failed: {err_msg}")

    publish_id = resp.get("data", {}).get("publish_id")
    if not publish_id:
        raise RuntimeError(f"TikTok post returned no publish_id: {resp}")

    print(f"  📦 TikTok publish_id: {publish_id}")

    # Poll for publish status
    print("  ⏳ TikTok processing...")
    status_str = "PROCESSING_UPLOAD"
    for attempt in range(24):
        time.sleep(10)
        status_result = subprocess.run([
            "curl", "-s", "-X", "POST",
            "https://tabiji.ai/api/tiktok-status",
            "-H", "Content-Type: application/json",
            "--data-raw", json.dumps({
                "access_token": access_token,
                "publish_id": publish_id,
            }),
        ], capture_output=True, text=True, timeout=30)
        status_resp = json.loads(status_result.stdout)

        status_str = status_resp.get("data", {}).get("status", "UNKNOWN")
        print(f"    [{(attempt+1)*10}s] {status_str}")

        if status_str == "PUBLISH_COMPLETE":
            break
        elif status_str in ("FAILED", "FAILED_PROCESSING", "FAILED_UPLOAD"):
            fail_reason = status_resp.get("data", {}).get("fail_reason", "unknown")
            raise RuntimeError(f"TikTok publish failed: {status_str} — {fail_reason}")

    if status_str != "PUBLISH_COMPLETE":
        raise RuntimeError(f"TikTok processing timed out (last: {status_str})")

    # Get the public post ID from the final status response
    public_post_id = status_resp.get("data", {}).get("publicaly_available_post_id", publish_id)

    # Cleanup R2 temp
    r2_delete(r2_key, cf_token)

    tiktok_url = f"https://www.tiktok.com/@tabiji1/video/{public_post_id}"
    print(f"  ✅ TikTok: {tiktok_url}")
    return tiktok_url


# ── X/Twitter Staging ─────────────────────────────────────────────────────

def stage_x(video_path, caption, slug="untitled"):
    """Upload video to R2 for manual X posting. Returns video URL. X API currently disabled."""
    ts = int(time.time())
    video_url = r2_upload(video_path, f"tmp/x/{slug}-{ts}.mp4")
    print(f"  ✅ X staged: {video_url}")
    return video_url


# ── #mission-control Notification ─────────────────────────────────────────

def notify_mission_control(results, caption, source="", video_path="", tiktok_url=""):
    """Post publish summary to #mission-control via openclaw message."""
    lines = []
    if source:
        lines.append(f"🎬 *Published: {source}*")
    else:
        lines.append("🎬 *Video Published*")

    # Extract first line as title
    title = caption.split("\n")[0][:80]
    lines.append(f"_{title}_")
    lines.append("")

    if results.get("ig"):
        lines.append(f"📸 IG: {results['ig']}")
    if results.get("yt"):
        lines.append(f"📺 YT: {results['yt']}")
    if results.get("fb"):
        lines.append(f"📘 FB: {results['fb']}")
    if results.get("tiktok"):
        lines.append(f"🎵 TikTok: {results['tiktok']}")
    if results.get("x"):
        lines.append(f"🐦 X: {results['x']}")

    # Hashtags
    hashtags = " ".join(re.findall(r'#[a-zA-Z0-9_]+', caption))
    if hashtags:
        lines.append(f"\n{hashtags}")

    msg = "\n".join(lines)

    try:
        cmd = [
            "openclaw", "message", "send",
            "--channel", "slack",
            "--target", MISSION_CONTROL_CHANNEL,
            "--message", msg,
        ]

        subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        print("  📢 Posted to #mission-control")
    except Exception as e:
        print(f"  ⚠️ Mission control notification failed: {e}")


# ── Main Pipeline ─────────────────────────────────────────────────────────

def publish_video(
    video_path: str,
    caption: str,
    title: str = "",
    description: str = "",
    tags: str = "travel,tabiji",
    thumb_offset: int = 1000,
    yt_thumbnail: str = "",
    platforms: list = None,
    source: str = "",
    slug: str = "",
    cost: float = 0.0,
    skip_publish: bool = False,
    notify: bool = True,
):
    """
    Unified publish pipeline.

    Returns dict with platform URLs and metadata.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    if platforms is None:
        platforms = PLATFORMS_DEFAULT

    # Derive title from caption if not provided
    if not title:
        title = caption.split("\n")[0][:100]
    if not description:
        description = caption
    if not slug:
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower())[:40].strip('-')

    results = {
        "source": source,
        "video": video_path,
        "title": title,
        "cost": cost,
        "published_at": datetime.now(timezone.utc).isoformat(),
        "platforms": {},
    }

    if skip_publish:
        # Just stage to R2
        ts = int(time.time())
        staging_url = r2_upload(video_path, f"tmp/staged/{slug}-{ts}.mp4")
        results["staging_url"] = staging_url
        print(f"\n📦 Staged (no publish): {staging_url}")
        return results

    # ── Dedup check ──
    fp = video_fingerprint(video_path, caption)
    already_published = check_dedup(fp, title)
    if already_published:
        skipped_platforms = {p: u for p, u in already_published.items() if p in platforms}
        if skipped_platforms:
            print(f"  ⏭️ Dedup: skipping {', '.join(skipped_platforms)} — already published within {DEDUP_WINDOW_HOURS}h")
            for plat, url in skipped_platforms.items():
                results["platforms"][plat] = url
                results[f"{plat}_dedup"] = True
            # Remove already-published from the list to process
            platforms = [p for p in platforms if p not in skipped_platforms]

    if not platforms and already_published:
        print(f"  ✅ All platforms already published — nothing to do")
        print(f"\n__PUBLISH_RESULT__{json.dumps(results)}__END_RESULT__")
        return results

    print(f"\n{'═' * 50}")
    print(f"🚀 Publishing: {title[:60]}")
    print(f"   Platforms: {', '.join(platforms)}")
    print(f"   Thumb offset: {thumb_offset}ms")
    print(f"{'═' * 50}\n")

    # ── Instagram ──
    if "ig" in platforms:
        try:
            media_id, ig_url = publish_ig(video_path, caption, thumb_offset)
            results["platforms"]["ig"] = ig_url
            results["ig_media_id"] = media_id
            record_publish(fp, "ig", ig_url, title)
        except Exception as e:
            print(f"  ❌ IG failed: {e}")
            results["platforms"]["ig"] = None
            results["ig_error"] = str(e)

    # ── YouTube ──
    if "yt" in platforms:
        try:
            yt_url = publish_yt(video_path, title, description, tags, yt_thumbnail or None)
            results["platforms"]["yt"] = yt_url
            record_publish(fp, "yt", yt_url, title)
        except Exception as e:
            print(f"  ❌ YT failed: {e}")
            results["platforms"]["yt"] = None
            results["yt_error"] = str(e)

    # ── Facebook ──
    if "fb" in platforms:
        fb_url = publish_fb(video_path, caption)
        results["platforms"]["fb"] = fb_url or None
        if fb_url:
            record_publish(fp, "fb", fb_url, title)

    # ── TikTok auto-publish ──
    if "tiktok" in platforms:
        try:
            tiktok_url = publish_tiktok(video_path, caption, slug)
            results["platforms"]["tiktok"] = tiktok_url
            record_publish(fp, "tiktok", tiktok_url, title)
        except Exception as e:
            print(f"  ❌ TikTok failed: {e}")
            results["platforms"]["tiktok"] = None
            results["tiktok_error"] = str(e)

    # ── X staging ──
    if "x" in platforms:
        try:
            x_url = stage_x(video_path, caption, slug)
            results["platforms"]["x"] = x_url
        except Exception as e:
            print(f"  ❌ X staging failed: {e}")
            results["platforms"]["x"] = None

    # ── #mission-control ──
    if notify:
        notify_mission_control(
            results["platforms"], caption, source,
        )

    # ── Summary ──
    print(f"\n{'═' * 50}")
    print("📊 Summary:")
    for platform, url in results["platforms"].items():
        icon = {"ig": "📸", "yt": "📺", "fb": "📘", "tiktok": "🎵", "x": "🐦"}.get(platform, "🔗")
        status = url if url else "❌ failed"
        print(f"  {icon} {platform}: {status}")
    if cost > 0:
        print(f"  💰 Cost: ${cost:.2f}")
    print(f"{'═' * 50}")

    # Machine-readable JSON result for agent consumption
    print(f"\n__PUBLISH_RESULT__{json.dumps(results)}__END_RESULT__")

    return results


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Unified Tabiji video publish pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full publish (IG + YT + FB, plus automatic TikTok handoff to #mission-control):
  python3 publish-video.py --video reel.mp4 --caption "Caption #travel"

  # Skip YouTube, custom thumbnail timing:
  python3 publish-video.py --video reel.mp4 --caption "..." --platforms ig,fb --thumb-offset 2000

  # Stage only (no publish):
  python3 publish-video.py --video reel.mp4 --caption "..." --skip-publish
"""
    )
    parser.add_argument("--video", required=True, help="Path to video MP4")
    parser.add_argument("--caption", required=True, help="Caption with hashtags")
    parser.add_argument("--title", default="", help="YouTube title (default: first line of caption)")
    parser.add_argument("--description", default="", help="YouTube description (default: full caption)")
    parser.add_argument("--tags", default="travel,tabiji", help="YouTube tags (comma-separated)")
    parser.add_argument("--thumb-offset", type=int, default=1000, help="IG thumbnail offset in ms (default: 1000)")
    parser.add_argument("--yt-thumbnail", default="", help="Custom YouTube thumbnail image path")
    parser.add_argument("--platforms", default="ig,yt,fb,tiktok", help="Comma-separated publish platforms (default: ig,yt,fb,tiktok)")
    parser.add_argument("--source", default="", help="Format/skill name for logging")
    parser.add_argument("--slug", default="", help="URL slug for R2 keys")
    parser.add_argument("--cost", type=float, default=0.0, help="Video generation cost for tracking")
    parser.add_argument("--skip-publish", action="store_true", help="Upload to R2 staging only")
    parser.add_argument("--no-notify", action="store_true", help="Skip #mission-control notification")

    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"❌ Video not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    platforms = [p.strip().lower() for p in args.platforms.split(",")]

    result = publish_video(
        video_path=args.video,
        caption=args.caption,
        title=args.title,
        description=args.description,
        tags=args.tags,
        thumb_offset=args.thumb_offset,
        yt_thumbnail=args.yt_thumbnail,
        platforms=platforms,
        source=args.source,
        slug=args.slug,
        cost=args.cost,
        skip_publish=args.skip_publish,
        notify=not args.no_notify,
    )

    # Output JSON for automation
    print(f"\n{json.dumps(result, indent=2)}")

    # Exit code: 0 if skip-publish, or at least one platform succeeded
    if args.skip_publish:
        sys.exit(0)
    successes = [v for v in result["platforms"].values() if v]
    sys.exit(0 if successes else 1)


if __name__ == "__main__":
    main()
