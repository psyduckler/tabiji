#!/usr/bin/env python3
"""Regenerate the Hergé / Tintin ligne-claire cover prototype for V3
with a CREAM upper third (instead of the teal-sky upper third the first
generation produced). The cream upper third is critical because V2's
cover-front.svg pattern embeds the cover-art 1:1 image into the lower
2/3 of a cream-background 1200×1800 canvas, with the title overlaid on
the cream upper third. If the cover-art's upper third is teal, the
title-overlay area visually clashes with the surrounding cream.

Also: explicit no-frame, no-panel-border, no-comic-page-margin rules
to fix the panel-within-frame composition issue from the first
generation.

Output overwrites: book-medical-tourism/assets/cover-prototypes/
                   02-herge-ligne-claire.jpg
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from generate import (  # noqa: E402
    submit_nbp, poll_nbp, download_verify, _keychain, T2I_EP,
)

REPO = _HERE.parent.parent
OUT_DIR = REPO / "book-medical-tourism" / "assets" / "cover-prototypes"
OUT_PATH = OUT_DIR / "02-herge-ligne-claire.jpg"


PROMPT = (
    "A vertical book-cover illustration in the Hergé / Tintin "
    "ligne-claire style: clean uniform black ink outlines of consistent "
    "weight, flat areas of saturated color (muted slate blue, quiet "
    "teal, cream, warm camel-tan, soft sand), no cross-hatching, no "
    "shading gradients, every shape simplified to its clearest "
    "silhouette. Mid-twentieth-century European adventure-comic feel. "
    "The composition is full-bleed and edge-to-edge — NO panel border, "
    "NO comic-page frame, NO white margin around the image, NO matte. "
    "The illustration fills the entire frame.\n\n"
    "SCENE: A well-dressed traveler stands at an airport international "
    "gate, viewed from a three-quarter back angle so the face is mostly "
    "turned away. The traveler holds a clipboard with a printed "
    "checklist (the items unreadable but clearly a list of organized "
    "questions), a passport with a boarding pass tucked into it, and a "
    "small rolling suitcase beside them. Through a large airport "
    "window behind them, a stylized commercial airliner is visible on "
    "a sunlit tarmac — slate-blue tail fin, no airline livery, no "
    "country indicators, no logos. A round wall clock on the gate wall "
    "reads 5:40. The composition is tidy, calm, and confident — the "
    "traveler reads as prepared rather than rushed.\n\n"
    "CRITICAL — UPPER THIRD COMPOSITION: the upper third of the frame "
    "must be visually QUIET CREAM (off-white #fcf9e8 / #f5f0e3), NOT "
    "teal and NOT sky. The cream is the airport's interior wall above "
    "the window line, or a simple flat cream ceiling, with at most one "
    "small architectural detail (a hanging gate-number sign rendered "
    "as a simple slate-blue rectangle, OR a single round wall clock at "
    "the top-left corner). The cream upper third must be generously "
    "empty so a title can be overlaid on it later — this is the most "
    "important compositional constraint. The teal sky and the airliner "
    "live in the MIDDLE band of the frame, visible through the window. "
    "The airport floor and the traveler live in the lower band. The "
    "upper band is cream wall.\n\n"
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


def main() -> int:
    ws = _keychain("wavespeed-api-key")
    if not ws:
        print("ERROR: missing wavespeed-api-key in keychain", file=sys.stderr)
        return 1

    print("Regenerating Hergé prototype with cream upper third...")
    body = {
        "prompt": PROMPT,
        "aspect_ratio": "1:1",
        "resolution": "2k",
        "output_format": "jpeg",
    }
    tid = submit_nbp(body, T2I_EP, ws)
    if not tid:
        print("FAIL: submit", file=sys.stderr)
        return 1
    raw_url = poll_nbp(tid, ws, timeout=600)
    if not raw_url:
        print("FAIL: poll", file=sys.stderr)
        return 1
    ok, note = download_verify(raw_url, OUT_PATH)
    if not ok:
        print(f"FAIL: dl {note}", file=sys.stderr)
        return 1
    print(f"OK: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
