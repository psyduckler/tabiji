#!/usr/bin/env python3
"""
Build an Amazon KDP "A+ Content" kit for any Tabiji Travel Safety Series book.

A+ Content is uploaded by hand through KDP's A+ Content Manager web UI: you pick
a module type, type the text into its fields, and upload an image at that
module's exact pixel dimensions. This tool generates everything you paste/upload:

  * upload-ready PNGs at each module's exact KDP dimensions (composited from the
    book's existing city scam comics on img.tabiji.ai)
  * copy.md — every module's headline / body / alt-text, paste-ready, labelled
    with the KDP module type and the image file + dimensions to upload
  * kit.html — a visual preview laying the 5 modules out roughly as KDP renders
    them, so you can eyeball the kit before submitting

It is country-agnostic. Point it at any book directory that has an aplus.yaml:

    python3 generators/aplus-content/build_aplus.py book-china

Output: book-china/build/aplus/  (gitignored, like every book-*/build/)

The 5-module template (standard, non-Premium A+):
  1. Standard Company Logo            600x180
  2. Standard Image Header With Text  970x300   (hero — comic + baked title)
  3. Standard Four Image & Text       4x 300x300 (the comic showcase)
  4. Standard Multiple Image Module A 300x300   (one comic + "what's inside")
  5. Standard Product Description     text only  (closing trust block)

Requires: Pillow, pyyaml. Comics are fetched from img.tabiji.ai and cached.
"""
from __future__ import annotations

import html
import re
import sys
import textwrap
import urllib.request
from hashlib import md5
from io import BytesIO
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is required: pip3 install pyyaml")
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required: pip3 install Pillow")

REPO = Path(__file__).resolve().parents[2]

# KDP module image dimensions (px). Source of truth for what we composite.
DIMS = {
    "logo": (600, 180),
    "hero": (970, 300),
    "tile": (300, 300),  # Four Image & Text tiles + Multiple Image Module A
}

# Brand palette (from books/index.html :root).
C = {
    "indigo": "#2D3A5C",
    "indigo_light": "#3D4E7A",
    "cream": "#F5F0E8",
    "cream_soft": "#FAF6EE",
    "sand": "#E8DFD0",
    "terracotta": "#A85A37",
    "brown": "#3E2F23",
    "text": "#2C2419",
    "white": "#FEFCF9",
}

# macOS system fonts (graceful fallback to Pillow default if absent, e.g. in CI).
FONT_SERIF = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
FONT_SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"

UA = {"User-Agent": "Mozilla/5.0 (tabiji-aplus-builder)"}


# --------------------------------------------------------------------------- #
# Fonts & image helpers
# --------------------------------------------------------------------------- #
def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


def fetch(url: str, cache: Path) -> Image.Image:
    """Fetch an image URL (cached by URL hash) and return an RGBA PIL image."""
    cache.mkdir(parents=True, exist_ok=True)
    key = cache / (md5(url.encode()).hexdigest() + Path(url.split("?")[0]).suffix)
    if not key.exists():
        req = urllib.request.Request(url, headers=UA)
        key.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    return Image.open(BytesIO(key.read_bytes())).convert("RGBA")


def cover(im: Image.Image, w: int, h: int) -> Image.Image:
    """Resize + center-crop so the image exactly fills w x h (no distortion)."""
    scale = max(w / im.width, h / im.height)
    rw, rh = round(im.width * scale), round(im.height * scale)
    im = im.resize((rw, rh), Image.LANCZOS)
    left, top = (rw - w) // 2, (rh - h) // 2
    return im.crop((left, top, left + w, top + h))


def wrap_to_width(draw, text, fnt, max_w):
    """Greedy word-wrap to fit max_w px; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------------------- #
# Comic resolution — read the live scam page HTML for authoritative URL + caption
# --------------------------------------------------------------------------- #
COMIC_IMG = re.compile(r"<img[^>]*\bclass=\"scam-comic\"[^>]*>")
ATTR = lambda name, tag: (re.search(rf'{name}="([^"]*)"', tag) or [None, None])[1]


def comics_for_city(city: str) -> list[tuple[str, str]]:
    """Return ordered [(comic_url, scam_name), ...] for a city's scam page.

    The Nth entry is scam N (scam-N.webp). URL includes any ?v= cache-bust.
    """
    page = REPO / "scams" / city / "index.html"
    if not page.exists():
        raise SystemExit(f"no scam page for city '{city}' at {page}")
    out = []
    for tag in COMIC_IMG.findall(page.read_text(encoding="utf-8")):
        src, alt = ATTR("src", tag), ATTR("alt", tag) or ""
        if src:
            name = html.unescape(alt).replace(" — comic illustration", "").strip()
            out.append((src, name))
    return out


def resolve(ref: dict, cache: Path) -> tuple[Image.Image, str]:
    """ref = {city, n}; returns (PIL image, scam_name). n is 1-based."""
    comics = comics_for_city(ref["city"])
    idx = ref["n"] - 1
    if not (0 <= idx < len(comics)):
        raise SystemExit(f"{ref['city']} has {len(comics)} comics; asked for #{ref['n']}")
    url, name = comics[idx]
    return fetch(url, cache), name


# --------------------------------------------------------------------------- #
# Module compositors
# --------------------------------------------------------------------------- #
def rounded(im: Image.Image, radius: int) -> Image.Image:
    """Apply rounded corners to an RGBA image."""
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), im.size], radius, fill=255)
    im.putalpha(mask)
    return im


def make_logo(brand: dict, cache: Path) -> Image.Image:
    w, h = DIMS["logo"]
    img = Image.new("RGBA", (w, h), C["cream"])
    d = ImageDraw.Draw(img)
    # Owl mark on the left.
    x = 40
    if brand.get("logo_url"):
        owl = fetch(brand["logo_url"], cache)
        oh = 112
        ow = round(owl.width * oh / owl.height)
        owl = owl.resize((ow, oh), Image.LANCZOS)
        img.paste(owl, (x, (h - oh) // 2), owl)
        x += ow + 26
    # Wordmark + series line.
    word = brand.get("wordmark", "TABIJI")
    series = brand.get("series", "TRAVEL SAFETY SERIES")
    fw, fs = font(FONT_SERIF, 58), font(FONT_SANS_BOLD, 18)
    wbox = d.textbbox((0, 0), word, font=fw)
    sbox = d.textbbox((0, 0), series.upper(), font=fs)
    block_h = (wbox[3] - wbox[1]) + 14 + (sbox[3] - sbox[1])
    y = (h - block_h) // 2 - wbox[1]
    d.text((x, y), word, font=fw, fill=C["indigo"])
    sy = y + (wbox[3] - wbox[1]) + 16
    d.text((x + 2, sy), series.upper(), font=fs, fill=C["terracotta"])
    # letter-spacing fake: draw small rule under series
    d.line([(x + 2, sy + sbox[3] - sbox[1] + 8),
            (x + 2 + sbox[2] - sbox[0], sy + sbox[3] - sbox[1] + 8)],
           fill=C["sand"], width=2)
    return img.convert("RGB")


def make_hero(mod: dict, cache: Path) -> Image.Image:
    w, h = DIMS["hero"]
    img = Image.new("RGB", (w, h), C["indigo"])
    d = ImageDraw.Draw(img)
    # Subtle vertical band lighten on the left text area.
    for i in range(h):
        t = i / h
        r = int(0x2D + (0x3D - 0x2D) * t)
        g = int(0x3A + (0x4E - 0x3A) * t)
        b = int(0x5C + (0x7A - 0x5C) * t)
        d.line([(0, i), (640, i)], fill=(r, g, b))

    # Comic chip on the right.
    comic, _ = resolve(mod["comic"], cache)
    chip = 248
    cx = w - chip - 46
    cy = (h - chip) // 2
    # terracotta frame
    d.rounded_rectangle([(cx - 6, cy - 6), (cx + chip + 6, cy + chip + 6)],
                        18, fill=C["terracotta"])
    img.paste(rounded(cover(comic, chip, chip), 12).convert("RGB"), (cx, cy),
              rounded(cover(comic, chip, chip), 12))

    # Left text block.
    x = 46
    eyebrow = mod.get("eyebrow", "TABIJI TRAVEL SAFETY SERIES")
    d.text((x, 34), eyebrow.upper(), font=font(FONT_SANS_BOLD, 16), fill=C["terracotta"])
    title = mod.get("title", "")
    d.text((x, 58), title, font=font(FONT_SERIF, 70), fill=C["white"])
    sub = mod.get("title_sub", "")
    d.text((x, 140), sub, font=font(FONT_SANS, 22), fill=C["sand"])
    # Hook (wrapped).
    hook_f = font(FONT_SANS, 17)
    for j, line in enumerate(wrap_to_width(d, mod.get("hook", ""), hook_f, 560)[:2]):
        d.text((x, 176 + j * 23), line, font=hook_f, fill=C["cream"])
    # Stat pill.
    stat = mod.get("stat", "")
    if stat:
        sf = font(FONT_SANS_BOLD, 14)
        tw = d.textlength(stat, font=sf)
        d.rounded_rectangle([(x, 250), (x + tw + 28, 282)], 16, fill=C["terracotta"])
        d.text((x + 14, 257), stat, font=sf, fill=C["white"])
    return img


def make_tile(ref: dict, cache: Path) -> Image.Image:
    w, h = DIMS["tile"]
    comic, _ = resolve(ref, cache)
    img = cover(comic, w, h).convert("RGB")
    # thin sand border so the tile reads as an edge on KDP's white canvas
    ImageDraw.Draw(img).rectangle([(0, 0), (w - 1, h - 1)], outline=C["sand"], width=2)
    return img


# --------------------------------------------------------------------------- #
# Kit renderers (copy.md + kit.html)
# --------------------------------------------------------------------------- #
def render_copy(book: dict, mods: list[dict], out: Path):
    L = [f"# A+ Content kit — {book['title']}", ""]
    L += [f"_{book.get('subtitle','')}_", "",
          "Paste each module into KDP's A+ Content Manager. Upload the named image "
          "at the stated pixel size. Module types match KDP's standard (non-Premium) library; "
          "if a name differs slightly in your account, match by description.",
          "",
          "Text fields are plain text — apply bold/bullets with KDP's editor toolbar, "
          "don't type HTML. Module names may vary slightly by account.",
          "", "---", ""]
    for i, m in enumerate(mods, 1):
        L.append(f"## Module {i} — {m['_kdp']}")
        if m.get("_img"):
            dw, dh = m["_dim"]
            L.append(f"**Upload:** `{m['_img']}` ({dw}×{dh} px) · alt: \"{m.get('alt','')}\"")
        if m.get("headline"):
            L.append(f"**Headline:** {m['headline']}")
        if m["type"] == "quad":
            for t in m["_tiles"]:
                L += ["", f"- **Tile — `{t['img']}` (300×300)** · {t['title']}",
                      f"  - Body: {t['body']}", f"  - alt: \"{t['alt']}\""]
        if m.get("body"):
            L += ["", m["body"]]
        if m.get("bullets"):
            L.append("")
            L += [f"- {b}" for b in m["bullets"]]
        L += ["", "---", ""]
    out.write_text("\n".join(L), encoding="utf-8")


def render_html(book: dict, mods: list[dict], out: Path):
    css = """body{margin:0;background:#33373f;font-family:-apple-system,Segoe UI,Arial,sans-serif;color:#2C2419}
    .page{max-width:880px;margin:0 auto;padding:32px}
    .hdr{color:#F5F0E8;text-align:center;margin:8px 0 28px}
    .hdr h1{margin:0;font-family:Georgia,serif;font-size:26px}.hdr p{opacity:.7;margin:4px}
    .mod{background:#fff;border-radius:10px;margin:0 0 22px;overflow:hidden;box-shadow:0 2px 14px rgba(0,0,0,.3)}
    .mlabel{background:#2D3A5C;color:#E8DFD0;font-size:12px;letter-spacing:.5px;padding:7px 14px;font-weight:700}
    .body{padding:18px 20px}.body img{max-width:100%;display:block;border-radius:6px}
    .h{font-size:19px;font-weight:700;margin:0 0 10px;color:#2D3A5C}
    .quad{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:6px}
    .quad .t img{width:100%}.quad .t h4{margin:8px 0 4px;color:#A85A37;font-size:15px}
    .quad .t p{margin:0;font-size:13px;line-height:1.45;color:#3E2F23}
    .feat{display:grid;grid-template-columns:300px 1fr;gap:20px;align-items:start}
    .feat ul{margin:0;padding-left:18px}.feat li{margin:0 0 9px;font-size:14px;line-height:1.4}
    .txt p{font-size:14px;line-height:1.6}.hl{color:#6B5D4F;font-style:italic;margin:-4px 0 12px}"""
    H = [f"<!doctype html><meta charset=utf-8><title>A+ kit — {book['title']}</title>",
         f"<style>{css}</style><div class=page>",
         f"<div class=hdr><h1>{book['title']}</h1><p>{book.get('subtitle','')}</p>",
         "<p>A+ Content preview — approximate KDP rendering</p></div>"]
    for i, m in enumerate(mods, 1):
        H.append(f"<div class=mod><div class=mlabel>MODULE {i} · {m['_kdp']}</div><div class=body>")
        if m.get("headline"):
            H.append(f"<div class=h>{m['headline']}</div>")
        if m["type"] in ("logo", "hero") and m.get("_img"):
            H.append(f"<img src='img/{m['_img']}' alt='{m.get('alt','')}'>")
        elif m["type"] == "quad":
            H.append("<div class=quad>")
            for t in m["_tiles"]:
                H.append(f"<div class=t><img src='img/{t['img']}'><h4>{t['title']}</h4>"
                         f"<p>{t['body']}</p></div>")
            H.append("</div>")
        elif m["type"] == "feature":
            H.append("<div class=feat>")
            H.append(f"<img src='img/{m['_img']}' alt='{m.get('alt','')}'>")
            lis = []
            for b in m.get("bullets", []):
                # bold the label before the em-dash (preview only; pasted copy stays plain)
                lead, sep, rest = b.partition(" — ")
                lis.append(f"<li><b>{lead}</b> — {rest}</li>" if sep else f"<li>{b}</li>")
            H.append("<ul>" + "".join(lis) + "</ul></div>")
        elif m["type"] == "text":
            H.append(f"<div class=txt><p>{m.get('body','')}</p></div>")
        H.append("</div></div>")
    H.append("</div>")
    out.write_text("\n".join(H), encoding="utf-8")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    if len(sys.argv) != 2:
        sys.exit("usage: build_aplus.py <book-dir>   e.g. book-china")
    book_dir = REPO / sys.argv[1]
    cfg = yaml.safe_load((book_dir / "aplus.yaml").read_text())
    book = cfg["book"]
    brand = cfg.get("brand", {})
    out = book_dir / "build" / "aplus"
    img_dir = out / "img"
    cache = out / ".cache"
    img_dir.mkdir(parents=True, exist_ok=True)

    mods = cfg["modules"]
    for m in mods:
        t = m["type"]
        if t == "logo":
            m["_kdp"], m["_dim"], m["_img"] = "Standard Company Logo", DIMS["logo"], "1-logo.png"
            make_logo(brand, cache).save(img_dir / m["_img"])
        elif t == "hero":
            m["_kdp"], m["_dim"], m["_img"] = "Standard Image Header With Text", DIMS["hero"], "2-hero.png"
            make_hero(m, cache).save(img_dir / m["_img"])
        elif t == "quad":
            m["_kdp"], m["_dim"] = "Standard Four Image & Text", DIMS["tile"]
            for j, t2 in enumerate(m["tiles"], 1):
                im, name = make_tile(t2, cache), resolve(t2, cache)[1]
                t2.setdefault("alt", f"{name} — comic illustration")
                t2["img"] = f"3-tile-{j}.png"
                im.save(img_dir / t2["img"])
            m["_tiles"] = m["tiles"]
        elif t == "feature":
            m["_kdp"], m["_dim"], m["_img"] = "Standard Multiple Image Module A", DIMS["tile"], "4-feature.png"
            im, name = make_tile(m["comic"], cache), resolve(m["comic"], cache)[1]
            m.setdefault("alt", f"{name} — comic illustration")
            im.save(img_dir / m["_img"])
        elif t == "text":
            m["_kdp"], m["_dim"], m["_img"] = "Standard Product Description Text", None, None
        else:
            raise SystemExit(f"unknown module type: {t}")

    render_copy(book, mods, out / "copy.md")
    render_html(book, mods, out / "kit.html")

    imgs = sorted(p.name for p in img_dir.glob("*.png"))
    print(f"✓ A+ kit for {book['title']}")
    print(f"  {out}/kit.html      (visual preview)")
    print(f"  {out}/copy.md       (paste-ready copy)")
    print(f"  {out}/img/          ({len(imgs)} images: {', '.join(imgs)})")


if __name__ == "__main__":
    main()
