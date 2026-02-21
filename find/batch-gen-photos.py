#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""Batch generate AI photos for tabiji destinations missing photos."""

import json, os, re, subprocess, sys, time
from pathlib import Path
from io import BytesIO

from google import genai
from google.genai import types
from PIL import Image as PILImage

SCRIPT_DIR = Path(__file__).parent
DEST_FILE = SCRIPT_DIR / "destinations.json"
IMG_DIR = SCRIPT_DIR / "img"

def slugify(name):
    s = name.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

def generate_image(client, prompt, png_path):
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=f"Generate an image: {prompt}",
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        )
    )
    for part in response.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            if isinstance(image_data, str):
                import base64
                image_data = base64.b64decode(image_data)
            image = PILImage.open(BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(str(png_path), 'PNG')
            return True
    return False

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set"); sys.exit(1)

    client = genai.Client(api_key=api_key)

    with open(DEST_FILE) as f:
        destinations = json.load(f)

    todo = [(i, d) for i, d in enumerate(destinations) if not d.get("photo")]
    print(f"Generating photos for {len(todo)} destinations...", flush=True)

    generated = 0
    failures = []

    for batch_idx, (i, dest) in enumerate(todo):
        name = dest["name"]
        region = dest.get("region", "")
        slug = slugify(name)
        png_path = IMG_DIR / f"{slug}.png"
        webp_path = IMG_DIR / f"{slug}.webp"

        if webp_path.exists():
            destinations[i]["photo"] = f"img/{slug}.webp"
            generated += 1
            print(f"[{generated}/{len(todo)}] {name} — exists", flush=True)
            continue

        prompt = f"Beautiful cinematic landscape photograph of {name}, {region}. Travel photography, golden hour lighting, vivid colors, professional quality."

        try:
            ok = generate_image(client, prompt, png_path)
            if not ok:
                print(f"[FAIL] {name} — no image in response", flush=True)
                failures.append(name)
                time.sleep(2)
                continue

            # Convert to webp
            r = subprocess.run(["cwebp", "-q", "80", str(png_path), "-o", str(webp_path)], capture_output=True, timeout=30)
            if webp_path.exists():
                png_path.unlink(missing_ok=True)
            else:
                png_path.rename(webp_path)

            destinations[i]["photo"] = f"img/{slug}.webp"
            generated += 1
            main._c429 = 0
            print(f"[{generated}/{len(todo)}] {name} ✓", flush=True)

        except Exception as e:
            err = str(e)
            print(f"[ERROR] {name}: {err[:150]}", flush=True)
            failures.append(name)
            png_path.unlink(missing_ok=True)
            if "429" in err and "RESOURCE_EXHAUSTED" in err:
                consecutive_429 = getattr(main, '_c429', 0) + 1
                main._c429 = consecutive_429
                if consecutive_429 >= 5:
                    print("Hit rate limit 5x in a row, stopping.", flush=True)
                    break
                time.sleep(10)
                continue
            else:
                main._c429 = 0

        # Save every 25
        if generated > 0 and generated % 25 == 0:
            with open(DEST_FILE, "w") as f:
                json.dump(destinations, f, indent=2)
            print(f"  — saved ({generated} done)", flush=True)

        time.sleep(2)

    # Final save
    with open(DEST_FILE, "w") as f:
        json.dump(destinations, f, indent=2)

    print(f"\nDone! Generated: {generated}, Failures: {len(failures)}", flush=True)
    if failures:
        print("Failed:", failures, flush=True)

if __name__ == "__main__":
    main()
