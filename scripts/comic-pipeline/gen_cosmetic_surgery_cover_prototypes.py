#!/usr/bin/env python3
"""Generate four comic-style cover prototypes for The Cosmetic Surgery Field
Guide. Four distinct visual languages so the user can pick a direction
before we commit to the full series treatment.

Outputs into book-cosmetic-surgery/assets/cover-prototypes/:
  01-herge-ligne-claire.jpg     — clean flat color, adventure-comic vibe
  02-steinberg-line.jpg          — sparse line editorial, sophisticated wry
  03-rockwell-editorial.jpg      — warm narrative, kitchen-table deliberation
  04-pushpin-conceptual.jpg      — mid-century conceptual graphic

Run: python3 scripts/comic-pipeline/gen_cosmetic_surgery_cover_prototypes.py
"""
from __future__ import annotations

import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import (  # noqa: E402
    submit_nbp, poll_nbp, download_verify, _keychain, T2I_EP,
)

REPO = _HERE.parent.parent
OUT_DIR = REPO / "book-cosmetic-surgery" / "assets" / "cover-prototypes"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# Shared composition rules every prompt must honor for a book cover.
COVER_RULES = (
    "Vertical book-cover composition with a 1:1 square crop "
    "(the upper third must be visually quiet for a title overlay; "
    "richer detail lives in the lower two-thirds). "
    "NO embedded text, NO speech bubbles, NO captions, NO banners, NO logos. "
    "NO patient faces in clinical detail (avoid identifiable likeness). "
    "NO blood, NO surgical wounds, NO needles, NO scars visible. "
    "Tone: calm, considered, protective — NOT alarmist, glamorous, "
    "or commercial. This is a serious nonfiction buyer-protection book "
    "about cosmetic surgery travel; the cover should feel like the "
    "kind of book a careful adult would trust. "
    "2K resolution, JPEG output."
)


# ── Direction 1: Hergé / Tintin ligne-claire ────────────────────────────
HERGE_PROMPT = (
    "A vertical book-cover illustration in the Hergé / Tintin "
    "ligne-claire style: clean uniform black ink outlines of consistent "
    "weight, flat areas of saturated color (warm camel-tan, deep teal, "
    "muted brick red, cream, soft sky blue), no cross-hatching, no "
    "shading gradients, every shape simplified to its clearest "
    "silhouette. Mid-twentieth-century European adventure-comic feel. "
    "\n\nSCENE: A well-dressed traveler stands at an airport "
    "international gate, viewed from a three-quarter back angle so the "
    "face is mostly turned away. The traveler holds a clipboard with "
    "a printed checklist (the items unreadable but clearly a list), a "
    "passport with a boarding pass tucked into it, and a small "
    "rolling suitcase by their side. Through a large airport window "
    "behind them, a stylized commercial airliner taxis on a sunlit "
    "tarmac with palm trees in the distance. A round wall clock on "
    "the gate wall reads 5:40. The composition is tidy and confident. "
    "Upper third of the frame: clear sky-blue airport window, mostly "
    "empty, ready for a title overlay.\n\n" + COVER_RULES
)


# ── Direction 2: Saul Steinberg / New Yorker line editorial ────────────
STEINBERG_PROMPT = (
    "A vertical book-cover illustration in the Saul Steinberg / mid-"
    "century New Yorker editorial cartoon style: spare confident "
    "black-ink line drawing on a cream or off-white background, "
    "intentionally wobbly and economical, almost diagrammatic. "
    "Single thin ink color (black) with at most one accent color "
    "(soft warm red used sparingly). Wry, sophisticated, restrained. "
    "Generous negative space.\n\n"
    "SCENE: A solitary line-drawn figure (gender-ambiguous, "
    "shown from behind so no face is visible) sits at a small wooden "
    "kitchen table that has been drawn as a precise minimalist "
    "rectangle. On the table: a stack of paper labeled only by their "
    "shapes (one stack thick, one thin), a coffee cup with steam "
    "rising in a single curving line, and a desk lamp casting a soft "
    "warm-red glow across the page. A window in the upper-right "
    "corner shows a single line indicating night. The composition is "
    "intellectual, contemplative, and clearly the moment before a "
    "considered decision is made. Upper third of the frame: clean "
    "cream space with only the suggestion of a wall corner, ready "
    "for a title overlay.\n\n" + COVER_RULES
)


# ── Direction 3: Norman Rockwell editorial illustration ─────────────────
ROCKWELL_PROMPT = (
    "A vertical book-cover illustration in the Norman Rockwell / "
    "Saturday Evening Post mid-century American editorial-illustration "
    "style: warm naturalistic painting with soft brushwork, gentle "
    "narrative storytelling, careful attention to fabric folds, "
    "expressive but tasteful body language, and the warm honey-amber "
    "palette of a domestic interior at evening. Skin tones and "
    "specific features kept loose and generic; faces oriented away or "
    "in shadow so no identifiable likeness. Trustworthy, considered, "
    "human-scale.\n\n"
    "SCENE: A person in their forties or fifties (face mostly in "
    "shadow or turned toward the table) sits at a wooden kitchen "
    "table at evening, leaning thoughtfully on one elbow. On the "
    "table: a printed-out treatment quote with visible page-edge "
    "stacking, a notebook with handwritten questions visible only as "
    "ink loops, a phone face-down, a glass of water, a pair of "
    "reading glasses. A warm yellow pendant lamp lights the table "
    "from above. In the background, a softly out-of-focus kitchen "
    "with a window showing dusk. The mood is honest deliberation, "
    "not anxiety. Upper third of the frame: warm shadowed ceiling "
    "and the soft glow of the pendant lamp, mostly empty space, "
    "ready for a title overlay.\n\n" + COVER_RULES
)


# ── Direction 4: Push Pin / Milton Glaser mid-century conceptual ────────
PUSHPIN_PROMPT = (
    "A vertical book-cover illustration in the Push Pin Studios / "
    "Milton Glaser / Seymour Chwast mid-century conceptual graphic "
    "style: bold flat areas of color with sharp graphic edges, a "
    "limited palette of saturated mustard, deep teal, terra-cotta, "
    "and cream, hand-cut paper feel with subtle texture, and one "
    "clean symbolic image carrying the entire concept. Designer-y, "
    "intelligent, conceptual, not narrative. Reminiscent of 1960s "
    "and 1970s nonfiction book jackets and editorial-magazine covers.\n\n"
    "SCENE: A single graphic conceptual image at the center of the "
    "composition — a vintage international passport, opened to a "
    "page, with the visa stamp area transformed into a stylized "
    "medical chart or anatomical diagram silhouette (no surgical "
    "detail, no body parts, no clinical iconography that suggests "
    "harm — just a clean graphic mark, almost like a heraldic "
    "device). The passport sits on a soft mustard-and-teal "
    "geometric ground that suggests a desk or table from above. A "
    "small abstract suitcase-handle or boarding-pass shape peeks "
    "into one corner. The image reads instantly and symbolically: "
    "travel + medical decision. Upper third of the frame: clean "
    "teal or cream graphic field, ready for a title overlay.\n\n"
    + COVER_RULES
)


PROMPTS = {
    "01-herge-ligne-claire": HERGE_PROMPT,
    "02-steinberg-line": STEINBERG_PROMPT,
    "03-rockwell-editorial": ROCKWELL_PROMPT,
    "04-pushpin-conceptual": PUSHPIN_PROMPT,
}


def generate_one(slug: str, prompt: str, ws: str) -> tuple[str, str]:
    body = {
        "prompt": prompt,
        "aspect_ratio": "1:1",
        "resolution": "2k",
        "output_format": "jpeg",
    }
    tid = submit_nbp(body, T2I_EP, ws)
    if not tid:
        return slug, "FAIL: submit"
    raw_url = poll_nbp(tid, ws, timeout=600)
    if not raw_url:
        return slug, "FAIL: poll"
    out = OUT_DIR / f"{slug}.jpg"
    ok, note = download_verify(raw_url, out)
    if not ok:
        return slug, f"FAIL: dl {note}"
    return slug, str(out)


def main() -> int:
    ws = _keychain("wavespeed-api-key")
    if not ws:
        print("ERROR: missing wavespeed-api-key in keychain", file=sys.stderr)
        return 1

    print(f"Generating {len(PROMPTS)} cover prototypes in parallel...\n")
    with ThreadPoolExecutor(max_workers=len(PROMPTS)) as pool:
        futures = {
            pool.submit(generate_one, slug, prompt, ws): slug
            for slug, prompt in PROMPTS.items()
        }
        for fut in as_completed(futures):
            slug, result = fut.result()
            print(f"  [{slug}] -> {result}")

    print(f"\nDone. Output: {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
