#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""Batch generate AI photos for tabiji destinations missing photos."""

import json
import os
import re
import subprocess
import sys
import time
from io import BytesIO
from pathlib import Path

def slugify(name):
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def main():
    base = Path(__file__).parent
    dest_file = base / "destinations.json"
    img_dir = base / "img"
    img_dir.mkdir(exist_ok=True)
    progress_file = base / "batch_progress.json"

    with open(dest_file) as f:
        destinations = json.load(f)

    # Load progress if exists
    completed = {}
    failed = []
    if progress_file.exists():
        with open(progress_file) as f:
            prog = json.load(f)
            completed = prog.get("completed", {})
            failed = prog.get("failed", [])
        print(f"Resuming: {len(completed)} already done, {len(failed)} previously failed")

    # Filter to empty photo fields
    to_process = []
    for i, d in enumerate(destinations):
        if d.get("photo"):
            continue
        slug = slugify(d["name"])
        if slug in completed:
            continue
        to_process.append((i, d, slug))

    print(f"To process: {len(to_process)} destinations")
    if not to_process:
        print("Nothing to do!")
        return

    # Setup Gemini client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    client = genai.Client(api_key=api_key)

    generated = 0
    errors = 0

    for count, (idx, dest, slug) in enumerate(to_process):
        name = dest["name"]
        region = dest.get("region", "")
        png_path = img_dir / f"{slug}.png"
        webp_path = img_dir / f"{slug}.webp"

        # Skip if webp already exists
        if webp_path.exists():
            completed[slug] = str(webp_path.relative_to(base))
            destinations[idx]["photo"] = f"img/{slug}.webp"
            generated += 1
            continue

        prompt = f"Beautiful cinematic landscape photograph of {name}, {region}. Travel photography, golden hour lighting, vivid colors, professional quality."

        print(f"[{count+1}/{len(to_process)}] Generating: {name} ({region})...", end=" ", flush=True)

        try:
            response = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                    image_config=types.ImageConfig(image_size="1K")
                )
            )

            image_saved = False
            for part in response.parts:
                if part.inline_data is not None:
                    import base64
                    image_data = part.inline_data.data
                    if isinstance(image_data, str):
                        image_data = base64.b64decode(image_data)
                    image = PILImage.open(BytesIO(image_data))
                    if image.mode != 'RGB':
                        if image.mode == 'RGBA':
                            rgb = PILImage.new('RGB', image.size, (255, 255, 255))
                            rgb.paste(image, mask=image.split()[3])
                            image = rgb
                        else:
                            image = image.convert('RGB')
                    image.save(str(png_path), 'PNG')
                    image_saved = True
                    break

            if not image_saved:
                print("FAILED (no image in response)")
                failed.append({"name": name, "slug": slug, "error": "no image in response"})
                errors += 1
                time.sleep(1)
                continue

            # Convert to webp
            result = subprocess.run(
                ["cwebp", "-q", "80", str(png_path), "-o", str(webp_path)],
                capture_output=True, text=True
            )
            if result.returncode == 0 and webp_path.exists():
                png_path.unlink()  # Delete PNG
            else:
                # Keep PNG, rename to webp approach - just use PNG
                print(f"cwebp failed, keeping PNG")

            rel_path = f"img/{slug}.webp" if webp_path.exists() else f"img/{slug}.png"
            completed[slug] = rel_path
            destinations[idx]["photo"] = rel_path
            generated += 1
            print("OK")

        except Exception as e:
            err_str = str(e)
            print(f"FAILED ({err_str[:80]})")
            failed.append({"name": name, "slug": slug, "error": err_str[:200]})
            errors += 1

            # If rate limited, wait longer
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                print("  Rate limited, waiting 30s...")
                time.sleep(30)

        # Save progress every 25 images
        if (count + 1) % 25 == 0:
            with open(progress_file, 'w') as f:
                json.dump({"completed": completed, "failed": failed}, f)
            with open(dest_file, 'w') as f:
                json.dump(destinations, f, indent=2)
            print(f"  [Progress saved: {generated} generated, {errors} errors]")

        # Small delay between requests
        time.sleep(2)

    # Final save
    with open(dest_file, 'w') as f:
        json.dump(destinations, f, indent=2)
    with open(progress_file, 'w') as f:
        json.dump({"completed": completed, "failed": failed}, f)

    print(f"\n=== DONE ===")
    print(f"Generated: {generated}")
    print(f"Failed: {errors}")
    if failed:
        print(f"Failed destinations:")
        for f_item in failed:
            print(f"  - {f_item['name']}: {f_item['error'][:80]}")

if __name__ == "__main__":
    main()
