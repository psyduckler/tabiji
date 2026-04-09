#!/usr/bin/env python3
"""
Add deep-dive section images to compare pages using SerpAPI + Gemini vision scoring.

Adapts the Instagram photo adder workflow for compare pages:
1. Pick 2-3 key sections per page (nature, food, culture — most visual topics)
2. Search SerpAPI Google Images for high-quality travel photos
3. Score candidates with Gemini vision
4. Optimize to 800px JPEG
5. Upload to Cloudflare R2
6. Inject <img> tag into deep-dive HTML

Usage:
  python3 enrich_compare_images.py --stats            # Show how many pages need images
  python3 enrich_compare_images.py --run --slug tokyo-vs-kyoto  # Single page
  python3 enrich_compare_images.py --run --limit 10   # First N pages
  python3 enrich_compare_images.py --run               # All pages (long!)
"""
from __future__ import annotations

import base64
import html as html_module
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "compare-data"
TMPDIR = Path("/tmp/compare-images-enrich")
PROGRESS_PATH = Path("/tmp/enrich-compare-images-progress.json")

SERPAPI_KEY = os.environ.get(
    "SERPAPI_KEY", "3d4b51ea3336e8eb9c73d5a3a28594bf11ec8d9219655903acf9719a6711f639"
)
GEMINI_KEY = os.environ.get(
    "GEMINI_KEY", "AIzaSyCo9zeMqGnE0iBzu9Edk2W8W7ky9-JJwhY"
)
GEMINI_MODEL = "gemini-2.5-flash"

R2_ACCOUNT = "9ce95ed3e1df4a7e1d2a401e116c3c6f"
R2_BUCKET = "tabiji-media"

# Sections most likely to benefit from images (by keyword in section title)
VISUAL_SECTION_KEYWORDS = [
    "nature", "landscape", "scenery", "beach", "outdoor",
    "food", "cuisine", "dining", "eat",
    "culture", "temple", "architecture", "historic", "art",
    "nightlife", "entertainment",
    "why not both", "both",
    "cost", "budget",
    "getting around", "transit", "transport",
    "weather", "season", "time to visit",
    "stay", "accommodation", "hotel",
    "day trip",
]


def get_r2_token() -> str:
    return subprocess.run(
        ["security", "find-generic-password", "-s", "cloudflare-pages-token", "-w"],
        capture_output=True, text=True
    ).stdout.strip()


def needs_dd_images(data: dict) -> bool:
    dd_html = "".join(data.get("content", {}).get("deepDiveHtml", []))
    return "section-img" not in dd_html


def pick_sections_for_images(deep_dives: list[str], max_images: int = 3) -> list[int]:
    """Pick the best 2-3 sections to add images to."""
    scored = []
    for i, dd in enumerate(deep_dives):
        title_match = re.search(r"<h2[^>]*>(.*?)</h2>", dd, re.S)
        title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip().lower() if title_match else ""
        # Remove emoji
        title = re.sub(r"[\U00010000-\U0010ffff\u2600-\u27bf\u2702-\u27b0]+", "", title).strip()

        score = 0
        for kw in VISUAL_SECTION_KEYWORDS:
            if kw in title:
                score += 1
        # Prefer earlier sections (more impactful)
        score += max(0, (10 - i) * 0.1)
        scored.append((i, score, title))

    scored.sort(key=lambda x: -x[1])
    return [s[0] for s in scored[:max_images]]


def get_section_title(dd: str) -> str:
    title_match = re.search(r"<h2[^>]*>(.*?)</h2>", dd, re.S)
    title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip() if title_match else "Unknown"
    return re.sub(r"[\U00010000-\U0010ffff\u2600-\u27bf\u2702-\u27b0]+\s*", "", title).strip()


def search_images(query: str, num: int = 8) -> list[dict]:
    """Search SerpAPI Google Images for travel photos."""
    url = (
        f"https://serpapi.com/search.json?engine=google_images"
        f"&q={urllib.parse.quote(query)}"
        f"&api_key={SERPAPI_KEY}&ijn=0&num={num}"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "tabiji/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        results = []
        for img in data.get("images_results", [])[:num]:
            w = img.get("original_width", 0)
            h = img.get("original_height", 0)
            orig = img.get("original", "")
            if w >= 600 and h >= 400 and orig and not orig.endswith(".svg"):
                results.append({
                    "url": orig,
                    "width": w,
                    "height": h,
                    "title": img.get("title", ""),
                    "source": img.get("source", ""),
                })
        return results
    except Exception as e:
        print(f"    ⚠️ Image search failed: {e}")
        return []


def download_image(url: str, local_path: Path) -> bool:
    """Download image to local path."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Accept": "image/*,*/*",
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            if len(data) < 5000:
                return False
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(data)
            return True
    except Exception:
        return False


def score_images_with_gemini(image_paths: list[Path], query: str) -> int | None:
    """Use Gemini vision to score images and pick the best. Returns index of best."""
    if not image_paths:
        return None

    # Build parts with inline image data
    parts = [{"text": (
        f"Score each photo 1-10 on how well it represents \"{query}\" "
        f"as a travel destination. Consider: visual quality, composition, "
        f"atmosphere, showing what makes this place special. "
        f"Output ONLY valid JSON: {{\"scores\": [{{\"index\": 0, \"score\": 8, \"reason\": \"brief reason\"}},...], \"best\": 0}}"
    )}]

    for i, path in enumerate(image_paths):
        try:
            img_data = path.read_bytes()
            b64 = base64.b64encode(img_data).decode()
            parts.append({"text": f"Photo {i}:"})
            parts.append({"inline_data": {"mime_type": "image/jpeg", "data": b64}})
        except Exception:
            continue

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"
    body = json.dumps({
        "contents": [{"parts": parts}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1024,
            "responseMimeType": "application/json",
        },
    })

    try:
        req = urllib.request.Request(url, data=body.encode(), headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read())
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        text = re.sub(r"^```json\s*", "", text.strip())
        text = re.sub(r"\s*```$", "", text.strip())
        parsed = json.loads(text)
        best = parsed.get("best", 0)
        if 0 <= best < len(image_paths):
            return best
        # Fallback: pick highest scored
        scores = parsed.get("scores", [])
        if scores:
            return max(scores, key=lambda s: s.get("score", 0)).get("index", 0)
        return 0
    except Exception as e:
        print(f"    ⚠️ Gemini vision scoring failed: {e}")
        return 0


def optimize_image(path: Path) -> bool:
    """Resize to 800px wide, 80% JPEG quality using sips."""
    try:
        subprocess.run(
            ["sips", "-Z", "800", "--setProperty", "formatOptions", "80", str(path)],
            capture_output=True, timeout=10,
        )
        return True
    except Exception:
        return False


def upload_to_r2(local_path: Path, r2_key: str) -> bool:
    """Upload to Cloudflare R2."""
    r2_token = get_r2_token()
    if not r2_token:
        print("    ⚠️ No R2 token found")
        return False
    try:
        result = subprocess.run(
            [
                "curl", "-s", "-X", "PUT",
                "-H", f"Authorization: Bearer {r2_token}",
                "-H", "Content-Type: image/jpeg",
                "--data-binary", f"@{local_path}",
                f"https://api.cloudflare.com/client/v4/accounts/{R2_ACCOUNT}/r2/buckets/{R2_BUCKET}/objects/{r2_key}",
            ],
            capture_output=True, text=True, timeout=30,
        )
        resp = json.loads(result.stdout) if result.stdout else {}
        return resp.get("success", False)
    except Exception as e:
        print(f"    ⚠️ R2 upload failed: {e}")
        return False


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text[:50].strip("-")


def process_section(
    slug: str, dest1: str, dest2: str, section_idx: int, dd: str, section_title: str
) -> str | None:
    """Process a single deep-dive section: search, score, optimize, upload, return img tag."""
    # Build search query
    query = f"{dest1} {dest2} {section_title} travel scenic photography"
    print(f"    🔍 Searching: {section_title}")

    results = search_images(query, num=6)
    if not results:
        # Fallback: search just the destinations
        results = search_images(f"{dest1} {section_title} travel photo", num=6)
    if not results:
        print(f"    ⚠️ No images found for {section_title}")
        return None

    # Download top 5 candidates
    workdir = TMPDIR / slug / f"section-{section_idx}"
    workdir.mkdir(parents=True, exist_ok=True)

    downloaded = []
    for i, img in enumerate(results[:5]):
        local = workdir / f"candidate_{i}.jpg"
        if download_image(img["url"], local):
            downloaded.append(local)
        time.sleep(0.2)

    if not downloaded:
        print(f"    ⚠️ No images downloaded for {section_title}")
        return None

    # Vision-score with Gemini
    print(f"    🎯 Scoring {len(downloaded)} candidates...")
    best_idx = score_images_with_gemini(downloaded, f"{section_title} in {dest1} or {dest2}")
    if best_idx is None or best_idx >= len(downloaded):
        best_idx = 0

    winner = downloaded[best_idx]

    # Optimize
    optimize_image(winner)

    # Generate filename
    filename = f"{slugify(section_title)}.jpg"
    r2_key = f"compare/{slug}/{filename}"
    cdn_url = f"https://img.tabiji.ai/{r2_key}"

    # Upload to R2
    print(f"    ☁️ Uploading {filename}...")
    if not upload_to_r2(winner, r2_key):
        print(f"    ⚠️ Upload failed for {filename}")
        return None

    # Build alt text
    alt_text = f"{dest1} and {dest2} — {section_title.lower()} comparison travel photo"

    # Cleanup
    for f in workdir.iterdir():
        f.unlink(missing_ok=True)
    workdir.rmdir()

    return (
        f'<img alt="{html_module.escape(alt_text)}" class="section-img" '
        f'loading="lazy" src="{cdn_url}"/>'
    )


def inject_image_into_section(dd: str, img_tag: str) -> str:
    """Insert image tag right after the <h2> heading."""
    h2_end = re.search(r"</h2>", dd)
    if h2_end:
        pos = h2_end.end()
        return dd[:pos] + "\n" + img_tag + "\n" + dd[pos:]
    return dd


def load_progress() -> dict:
    if PROGRESS_PATH.exists():
        return json.loads(PROGRESS_PATH.read_text())
    return {"completed": [], "failed": []}


def save_progress(progress: dict) -> None:
    PROGRESS_PATH.write_text(json.dumps(progress, indent=2))


def cmd_stats() -> None:
    need = 0
    total = 0
    for f in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        total += 1
        if needs_dd_images(data):
            need += 1
    print(f"Total compare pages: {total}")
    print(f"Need deep-dive images: {need}")
    print(f"Already have images: {total - need}")

    progress = load_progress()
    if progress["completed"]:
        print(f"Previously processed: {len(progress['completed'])}")


def cmd_enrich(slug_filter: str | None, limit: int | None) -> None:
    progress = load_progress()
    completed_set = set(progress["completed"])

    work = []
    for f in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        s = data["slug"]
        if slug_filter and s != slug_filter:
            continue
        if s in completed_set:
            continue
        if needs_dd_images(data):
            work.append((f, data))

    if limit:
        work = work[:limit]

    print(f"Processing {len(work)} pages (2-3 images each)\n")

    succeeded = 0
    failed = 0

    for i, (path, data) in enumerate(work):
        slug = data["slug"]
        dest1 = data["destinations"]["destination1"]
        dest2 = data["destinations"]["destination2"]
        deep_dives = data["content"]["deepDiveHtml"]

        print(f"[{i+1}/{len(work)}] {slug} ({dest1} vs {dest2})")

        # Pick which sections get images
        section_indices = pick_sections_for_images(deep_dives, max_images=3)
        images_added = 0

        for idx in section_indices:
            section_title = get_section_title(deep_dives[idx])
            try:
                img_tag = process_section(slug, dest1, dest2, idx, deep_dives[idx], section_title)
                if img_tag:
                    deep_dives[idx] = inject_image_into_section(deep_dives[idx], img_tag)
                    images_added += 1
                    print(f"    ✅ Added image for: {section_title}")
                time.sleep(0.5)
            except Exception as e:
                print(f"    ❌ Error for {section_title}: {e}")

        if images_added > 0:
            data["content"]["deepDiveHtml"] = deep_dives
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            print(f"  ✅ Saved {path.name} ({images_added} images added)")
            progress["completed"].append(slug)
            succeeded += 1
        else:
            print(f"  ⚠️ No images added for {slug}")
            progress["failed"].append(slug)
            failed += 1

        save_progress(progress)
        time.sleep(1)

    # Cleanup tmpdir
    if TMPDIR.exists():
        for d in TMPDIR.iterdir():
            if d.is_dir():
                for f in d.iterdir():
                    f.unlink(missing_ok=True)
                d.rmdir()

    print(f"\n{'='*50}")
    print(f"Results: {succeeded} succeeded, {failed} failed")
    print(f"Progress saved to {PROGRESS_PATH}")
    print(f"\nTo rebuild HTML, run: python3 generators/compare/build_compare.py build")


def main() -> None:
    args = sys.argv[1:]

    if "--stats" in args:
        cmd_stats()
        return

    if "--run" not in args:
        print("Dry run mode. Use --run to actually process pages.")
        print("Use --stats to see current status.")
        return

    slug_filter = None
    limit = None

    if "--slug" in args:
        idx = args.index("--slug")
        if idx + 1 < len(args):
            slug_filter = args[idx + 1]

    if "--limit" in args:
        idx = args.index("--limit")
        if idx + 1 < len(args):
            limit = int(args[idx + 1])

    cmd_enrich(slug_filter, limit)


if __name__ == "__main__":
    main()
