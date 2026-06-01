#!/usr/bin/env python3
"""
Batch builder: spec JSON (one per book) → rendered A+ kit → Desktop folder.

For each spec in books/specs/*.json it:
  1. stages the book's comics + owl from img.tabiji.ai into templates/assets/source/
  2. writes templates/data.<slug>.jsx (IMG + C + THEMES, from the spec)
  3. renders via generate.mjs (serial — shared data.jsx, so one at a time)
  4. writes a compliant KDP-copy.md
  5. assembles  ~/Desktop/<Country> A+ Content - Ready to Upload/
       images/ (9 PNGs) · images-jpg/ (JPG fallbacks) · KDP-copy.md · README.txt

Usage:  python3 build_all.py            # all specs in books/specs/
        python3 build_all.py italy ...  # only these slugs
Spec schema: see the workflow that emits them (slug, country, scams, cities,
accent{terra,terraDeep,wash}, stamp3, sourcesLine, hero{kicker,head[3],sub,comicURL},
headerBody, quadHead, quad[4]{tag,city,title,tl,comicURL}, inside{head,caption,
comicURL,items[[t,s]],phrases[[p,s,g]]}, desc{price,body[3],badges[4]}).
"""
import json, os, re, shutil, subprocess, sys, urllib.request
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SRC = HERE / "templates" / "assets" / "source"
TPL = HERE / "templates"
OUT = HERE / "out"
SPECS = HERE / "books" / "specs"
DESK = Path.home() / "Desktop"

SERIF = '"Newsreader", Georgia, "Times New Roman", serif'
SANS  = '"Public Sans", system-ui, -apple-system, sans-serif'
MONO  = '"Spline Sans Mono", ui-monospace, monospace'
COND  = '"Saira Condensed", "Public Sans", sans-serif'
BASE_THEME = {  # Field Guide tokens shared by every book; accent overrides terra/terraDeep/wash
    "key": "A", "name": "Field Guide", "dark": False,
    "pageBg": "#F3EADB", "surface": "#FBF6EC", "surfaceAlt": "#F2E6D4",
    "ink": "#2A2117", "sub": "#6E5E49", "onPage": "#7A6A52", "onPageSub": "#9A8B72",
    "line": "#DAC8AD", "lineSoft": "#E7DAC3",
    "serif": SERIF, "sans": SANS, "mono": MONO, "cond": COND,
}
TILE_NAMES = ["a", "b", "c", "d"]  # 03a..03d
UA = {"User-Agent": "Mozilla/5.0 (tabiji-aplus)"}

FORBIDDEN = {"price ($)": r"\$\d", "star/rating": r"★|\b[0-9]\.[0-9]\s*star",
             "refund/return": r"\brefund\b|\breturn policy\b", "guarantee": r"\bguarantee|money-?back\b",
             "promo free": r"\bfree\b", "discount/sale": r"\bdiscount\b|\bsale\b|% off"}


def fetch(url, dest):
    if dest.exists() and dest.stat().st_size > 0:
        return
    req = urllib.request.Request(url, headers=UA)
    dest.write_bytes(urllib.request.urlopen(req, timeout=30).read())


def filename_for(url):
    return re.sub(r"[?].*$", "", url).rsplit("/", 2)  # not used directly; kept simple below


def stage(spec):
    SRC.mkdir(parents=True, exist_ok=True)
    s = spec["slug"]
    fetch("https://img.tabiji.ai/tabiji-owl-logo.png", SRC / "owl.png")
    files = {}  # role → local filename
    def grab(role, url):
        fn = f"{s}-{role}.webp"
        fetch(url, SRC / fn)
        files[role] = f"assets/source/{fn}"
    grab("hero", spec["hero"]["comicURL"])
    grab("inside", spec["inside"]["comicURL"])
    for i, q in enumerate(spec["quad"]):
        grab(f"t{i+1}", q["comicURL"])
    return files


def data_jsx(spec, files):
    IMG = {
        "owl": "assets/source/owl.png", "owlFly": "assets/source/owl.png",
        "beijing2": files["hero"], "shanghai1": files["inside"],
        "t1": files["t1"], "t2": files["t2"], "t3": files["t3"], "t4": files["t4"],
        "cover": files["hero"],
    }
    C = {
        "brand": {"series": "TRAVEL SAFETY SERIES", "country": spec["country"], "dom": "tabiji.ai",
                  "stamp3": spec["stamp3"], "vol": ""},
        "stat": {"scams": str(spec["scams"]), "cities": str(spec["cities"]),
                 "sources": spec.get("sources", []), "sourcesLine": spec["sourcesLine"]},
        "hero": {"authority": {"kicker": spec["hero"]["kicker"], "head": spec["hero"]["head"],
                               "sub": spec["hero"]["sub"]}},
        "quadHead": {"A": spec["quadHead"]},
        "quad": [{"n": f"{i+1:02d}", "tag": q["tag"], "city": q["city"], "title": q["title"],
                  "tl": q["tl"], "loss": q.get("loss", ""), "img": IMG[f"t{i+1}"]}
                 for i, q in enumerate(spec["quad"])],
        "inside": {"head": spec["inside"]["head"], "img": IMG["shanghai1"],
                   "caption": spec["inside"]["caption"], "items": spec["inside"]["items"],
                   "phrases": spec["inside"]["phrases"]},
        "desc": {"head": {"A": "Read it on the flight over."}, "price": spec["desc"]["price"],
                 "body": spec["desc"]["body"], "badges": spec["desc"]["badges"]},
    }
    THEMES = {"A": {**BASE_THEME, **{k: spec["accent"][k] for k in ("terra", "terraDeep", "wash")}}}
    j = lambda o: json.dumps(o, ensure_ascii=False, indent=2)
    return (f"/* GENERATED for {spec['country']} by build_all.py — edit the spec, not this file. */\n"
            f"const IMG = {j(IMG)};\nconst C = {j(C)};\nconst THEMES = {j(THEMES)};\n"
            f"window.TABIJI = {{ IMG, C, THEMES }};\n")


def kdp_md(spec):
    q = spec["quad"]
    rows = "\n".join(
        f"| {i+1} | images/03{TILE_NAMES[i]}-{spec['slug']}-tile-300x300.png | {x['tag'].title()} · {x['city'].title()} {x['title']} | {x['tl']} |"
        for i, x in enumerate(q))
    items = "\n".join(f"  - {t} — {s2.rstrip('.')}." for t, s2 in spec["inside"]["items"])
    phr = " · ".join(f"“{p}” ({sc} — {g.rstrip('.')})" for p, sc, g in spec["inside"]["phrases"])
    body = "\n\n".join(spec["desc"]["body"])
    badges = " · ".join(spec["desc"]["badges"])
    return f"""# {spec['country'].title()}: Tourist Scams — Kindle A+ Content · SET A (Field Guide)

In Amazon A+, upload the image for each module and type the heading/body. Images are in images/.
Clean for A+ review: no price, ratings, or refund/promo wording.

---
## ① Standard Company Logo
- Image: images/01-company-logo-600x180.png (600×180) · no text

## ② Standard Image Header With Text
- Image: images/02-image-header-970x300.png (970×300)
- Headline: {spec['scams']} documented scams. {spec['cities']} cities.
- Body: {spec['headerBody']}

## ③ Standard Four Image & Text
| # | Image | Heading | Body |
|---|-------|---------|------|
{rows}

## ④ Standard Multiple Image Module A
- Image: images/04-multiple-image-A-FULL-970.png (970×300, full baked) — or the 300×300 native variant
- Headline: {spec['inside']['head']}
- Body:
{items}

  In-language: {phr}

## ⑤ Standard Product Description Text
- Image: images/05-product-description-970.png (970×300) — or paste the text below

{body}

{badges}
"""


def render(slug):
    shutil.copyfile(TPL / f"data.{slug}.jsx", TPL / "data.jsx")
    r = subprocess.run(["node", "generate.mjs"], cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"render {slug} failed:\n{r.stderr[-800:]}")


def assemble(spec):
    slug, country = spec["slug"], spec["country"].title()
    dest = DESK / f"{country} A+ Content - Ready to Upload"
    if dest.exists():
        shutil.rmtree(dest)
    (dest / "images").mkdir(parents=True)
    (dest / "images-jpg").mkdir(parents=True)
    rename = {
        "03a-four-image-ambush-300x300.png":      f"03a-{slug}-tile-300x300.png",
        "03b-four-image-charm-300x300.png":       f"03b-{slug}-tile-300x300.png",
        "03c-four-image-counterfeit-300x300.png": f"03c-{slug}-tile-300x300.png",
        "03d-four-image-gouge-300x300.png":       f"03d-{slug}-tile-300x300.png",
    }
    for f in sorted(OUT.glob("*.png")):
        name = rename.get(f.name, f.name)
        shutil.copyfile(f, dest / "images" / name)
        Image.open(f).convert("RGB").save(dest / "images-jpg" / (name[:-4] + ".jpg"),
                                          "JPEG", quality=92, optimize=True)
    (dest / "KDP-copy.md").write_text(kdp_md(spec), encoding="utf-8")
    (dest / "README.txt").write_text(
        f"{country}: Tourist Scams — Kindle A+ upload kit.\n"
        f"Upload images/ to KDP module by module; paste text from KDP-copy.md.\n"
        f"970×300 slot: header, 04-FULL, 05. 300×300: the four 03 tiles + 04 native.\n"
        f"images-jpg/ = JPG fallbacks (if KDP rejects a PNG upload).\n"
        f"Compliant: no price/ratings/refund. Field Guide design, {spec['accent'].get('note','')} accent.\n",
        encoding="utf-8")
    return dest


def compliance_ok(spec):
    blob = " ".join(spec["desc"]["body"]) + " " + " ".join(spec["desc"]["badges"]) + " " + \
        spec["desc"]["price"] + " " + spec["headerBody"] + " " + " ".join(q["tl"] for q in spec["quad"])
    hits = {k: re.findall(p, blob, re.I) for k, p in FORBIDDEN.items()}
    return {k: v for k, v in hits.items() if v}


def build(slug):
    spec = json.loads((SPECS / f"{slug}.json").read_text(encoding="utf-8"))
    bad = compliance_ok(spec)
    if bad:
        print(f"  ⚠ {slug}: A+ compliance flags {bad} — skipping (fix the spec)")
        return None
    files = stage(spec)
    (TPL / f"data.{slug}.jsx").write_text(data_jsx(spec, files), encoding="utf-8")
    render(slug)
    dest = assemble(spec)
    return dest


def main():
    slugs = sys.argv[1:] or sorted(p.stem for p in SPECS.glob("*.json"))
    print(f"building {len(slugs)} book(s): {', '.join(slugs)}")
    done, fail = [], []
    for s in slugs:
        try:
            d = build(s)
            (done if d else fail).append(s)
            if d:
                print(f"  ✓ {s} → {d}")
        except Exception as e:
            fail.append(s)
            print(f"  ✗ {s}: {e}")
    print(f"\nDone: {len(done)} ok, {len(fail)} failed{': ' + ', '.join(fail) if fail else ''}")


if __name__ == "__main__":
    main()
