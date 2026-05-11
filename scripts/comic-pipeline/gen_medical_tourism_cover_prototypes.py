#!/usr/bin/env python3
"""Generate four book-cover prototypes for The Medical Tourism Field Guide
(Volume Three). Four distinct visual languages so the user can pick a
direction before we commit to the full series treatment.

Series context: V1 dental used deep forest green; V2 cosmetic surgery used
warm brick red on cream. V3 medical tourism uses a passport-tone palette
— muted slate blue (#3A5566) and quiet teal (#1F6470) — to harmonize on
the shelf without repeating V2's accent. Each direction is briefed to
incorporate the slate-blue / teal accent rather than V2's warm red.

Outputs into book-medical-tourism/assets/cover-prototypes/:
  01-steinberg-line.jpg           — sparse line editorial; V2-rhyming
  02-herge-ligne-claire.jpg       — clean flat-color adventure-comic
  03-saul-bass-conceptual.jpg     — mid-century cinematic minimalism
  04-rockwell-editorial.jpg       — warm narrative deliberation

Run: python3 scripts/comic-pipeline/gen_medical_tourism_cover_prototypes.py
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
OUT_DIR = REPO / "book-medical-tourism" / "assets" / "cover-prototypes"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# Shared composition rules — match V2 exactly so series identity holds.
COVER_RULES = (
    "Vertical book-cover composition with a 1:1 square crop "
    "(the upper third must be visually quiet for a title overlay; "
    "richer detail lives in the lower two-thirds). "
    "NO embedded text, NO speech bubbles, NO captions, NO banners, NO logos. "
    "NO patient faces in clinical detail (avoid identifiable likeness). "
    "NO blood, NO surgical wounds, NO needles, NO scars visible, "
    "NO hospital signage, NO operating-room imagery. "
    "Tone: calm, considered, protective — NOT alarmist, glamorous, "
    "or commercial. This is a serious nonfiction buyer-protection book "
    "about healthcare decisions abroad; the cover should feel like the "
    "kind of book a careful adult would trust. "
    "Color palette accent must use muted slate blue (#3A5566) or quiet "
    "teal (#1F6470) rather than warm red — this is volume three of a "
    "series and warm red is already taken by volume two. "
    "2K resolution, JPEG output."
)


# ── Direction 1: Saul Steinberg / New Yorker line editorial ────────────
# V2 went with this direction; V3 PLAN recommends the same for series
# visual consistency. Scene: solitary figure with a world map/atlas
# instead of V2's window-corner — signals "across borders" without
# explicit travel imagery.
STEINBERG_PROMPT = (
    "A vertical book-cover illustration in the Saul Steinberg / mid-"
    "century New Yorker editorial cartoon style: spare confident "
    "black-ink line drawing on a cream or off-white background, "
    "intentionally wobbly and economical, almost diagrammatic. "
    "Single thin ink color (black) with at most one accent color "
    "(muted slate blue used sparingly — for a desk lamp's glow or "
    "the spine of an atlas). Wry, sophisticated, restrained. "
    "Generous negative space.\n\n"
    "SCENE: A solitary line-drawn figure (gender-ambiguous, shown "
    "from behind so no face is visible) sits at a small wooden table "
    "drawn as a precise minimalist rectangle. On the table: a large "
    "open book that reads as a world atlas (continents indicated by "
    "the loosest of line shapes — no place names, no flags), a stack "
    "of paper representing medical records or printed quotes "
    "(rectangles only, no text), a coffee cup with steam rising in a "
    "single curving line, and a small reading lamp casting a soft "
    "slate-blue glow across the page. A window in the upper-right "
    "corner shows a single line indicating evening. The composition "
    "is intellectual, contemplative, the moment before a considered "
    "cross-border decision is made. Upper third of the frame: clean "
    "cream space with only the suggestion of a wall corner, ready "
    "for a title overlay.\n\n" + COVER_RULES
)


# ── Direction 2: Hergé / Tintin ligne-claire ────────────────────────────
# Adventure-comic vibe; less moody than Steinberg. The scene is a
# considered traveler at an airport gate, but reframed for medical
# tourism — not a glamour shot, more like a businessperson reviewing
# their pre-trip checklist.
HERGE_PROMPT = (
    "A vertical book-cover illustration in the Hergé / Tintin "
    "ligne-claire style: clean uniform black ink outlines of consistent "
    "weight, flat areas of saturated color (muted slate blue, quiet "
    "teal, cream, warm camel-tan, soft sand), no cross-hatching, no "
    "shading gradients, every shape simplified to its clearest "
    "silhouette. Mid-twentieth-century European adventure-comic feel.\n\n"
    "SCENE: A well-dressed traveler stands at an airport international "
    "gate, viewed from a three-quarter back angle so the face is mostly "
    "turned away. The traveler holds a clipboard with a printed "
    "checklist (the items unreadable but clearly a list of organized "
    "questions), a passport with a boarding pass tucked into it, and a "
    "small rolling suitcase beside them. Through a large airport "
    "window behind them, a stylized commercial airliner is visible on "
    "a sunlit tarmac — slate-blue tail fin, no airline livery, no "
    "country indicators. A round wall clock on the gate wall reads "
    "5:40. The composition is tidy, calm, and confident — the "
    "traveler reads as prepared rather than rushed. Upper third of "
    "the frame: clear teal airport window, mostly empty, ready for "
    "a title overlay.\n\n" + COVER_RULES
)


# ── Direction 3: Saul Bass mid-century conceptual ──────────────────────
# Different direction from V2's Push Pin: Bass is sharper, more
# cinematic, often a single symbolic image at the heart of the
# composition. Less hand-cut paper, more geometric reduction.
SAULBASS_PROMPT = (
    "A vertical book-cover illustration in the Saul Bass mid-century "
    "conceptual style: bold flat areas of color with razor-sharp "
    "graphic edges, a limited and considered palette (muted slate "
    "blue, quiet teal, warm cream, and a single accent of sand-gold), "
    "shapes reduced to their cleanest geometric essence, with the "
    "intentional rough texture of mid-century silkscreen printing. "
    "Cinematic feel, designed by a graphic designer rather than an "
    "illustrator. Reminiscent of Bass's title-sequence work and his "
    "1960s book-jacket designs.\n\n"
    "SCENE: A single conceptual composition at the center — a "
    "stylized globe rendered as overlapping flat geometric arcs in "
    "slate blue and teal, with a single thin sand-gold line tracing "
    "a meridian or great-circle arc across the surface to suggest a "
    "considered cross-border path. Below the globe, the suggestion "
    "of a hand or open palm rendered as a single clean shape "
    "(no fingers detailed, no clinical iconography). No hospital "
    "symbols, no medical-cross imagery, no aircraft. The image "
    "reads instantly and symbolically: considered international "
    "decision-making, careful navigation. Upper third of the frame: "
    "clean cream graphic field, ready for a title overlay.\n\n"
    + COVER_RULES
)


# ── Direction 4: Norman Rockwell editorial illustration ─────────────────
# Warm narrative. Adapt V2's kitchen-table scene but with the
# medical-tourism context. Color palette stays Rockwell-warm but adds
# slate-blue accents to keep series identity.
ROCKWELL_PROMPT = (
    "A vertical book-cover illustration in the Norman Rockwell / "
    "Saturday Evening Post mid-century American editorial-illustration "
    "style: warm naturalistic painting with soft brushwork, gentle "
    "narrative storytelling, careful attention to fabric folds, "
    "expressive but tasteful body language, and the warm honey-amber "
    "palette of a domestic interior at evening — with restrained "
    "slate-blue accents (a coffee mug, a desk-lamp shade, the spine "
    "of a book) to keep the volume aligned with the series's V3 "
    "palette. Skin tones and specific features kept loose and "
    "generic; faces oriented away or in shadow so no identifiable "
    "likeness. Trustworthy, considered, human-scale.\n\n"
    "SCENE: A person in their forties or fifties (face mostly in "
    "shadow or turned toward the table) sits at a wooden kitchen "
    "table at evening, leaning thoughtfully on one elbow. On the "
    "table: an open atlas or world map showing a region "
    "indistinctly (no country names readable), a printed treatment "
    "quote with visible page-edge stacking, a notebook with "
    "handwritten questions visible only as ink loops, a phone "
    "face-down, a glass of water, a pair of reading glasses. A warm "
    "yellow pendant lamp lights the table from above; the lamp shade "
    "itself is slate blue. In the background, a softly out-of-focus "
    "kitchen with a window showing dusk. The mood is honest "
    "deliberation about a cross-border healthcare decision — not "
    "anxiety, not relief. Upper third of the frame: warm shadowed "
    "ceiling and the soft glow of the pendant lamp, mostly empty "
    "space, ready for a title overlay.\n\n" + COVER_RULES
)


PROMPTS = {
    "01-steinberg-line": STEINBERG_PROMPT,
    "02-herge-ligne-claire": HERGE_PROMPT,
    "03-saul-bass-conceptual": SAULBASS_PROMPT,
    "04-rockwell-editorial": ROCKWELL_PROMPT,
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
