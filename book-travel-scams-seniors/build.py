#!/usr/bin/env python3
"""
Build Travel Scams for Seniors EPUB and assembled-markdown.

Pipeline:
  manuscript-source.md
    → insert chapter scene images at correct anchors
    → assembled markdown
    → EPUB (pandoc, with embedded cover + chapter scenes)

Usage:
    python3 book-travel-scams-seniors/build.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import yaml


HERE = Path(__file__).resolve().parent
MANUSCRIPT_SRC = HERE / "manuscript" / "manuscript-source.md"
ASSETS_SCENES = HERE / "assets" / "chapter-scenes"
ASSETS_COVERS = HERE / "assets" / "covers"
BUILD = HERE / "build"
BUILD.mkdir(parents=True, exist_ok=True)

CONFIG = yaml.safe_load((HERE / "config.yaml").read_text())

# Map chapter number → image filename. Chapters 3 and 18 deliberately have no
# scene illustration (text-only / preparation chapters).
CHAPTER_SCENES: dict[int, str] = {
    1: "ch01-mustard-stain.jpg",
    2: "ch02-midnight-call.jpg",
    4: "ch04-grandson-call.jpg",
    5: "ch05-airport-lanyard.jpg",
    6: "ch06-taxi-curb.jpg",
    7: "ch07-lobby-stranger.jpg",
    8: "ch08-crowded-atm.jpg",
    9: "ch09-no-commission.jpg",
    10: "ch10-fake-wifi.jpg",
    11: "ch11-cafe-table-cover.jpg",
    12: "ch12-vest-man.jpg",
    13: "ch13-front-desk-refusal.jpg",
    14: "ch14-cruise-jewelry.jpg",
    15: "ch15-no-prices-menu.jpg",
    16: "ch16-bracelet.jpg",
    17: "ch17-new-friend.jpg",
    19: "ch19-fake-fixer.jpg",
}

# Alt text per chapter (screen-reader friendly, KDP accessibility compliance).
CHAPTER_ALT: dict[int, str] = {
    1: "An older woman in a plaza looks at a smear on her sleeve as a man holds a napkin and an accomplice approaches her bag.",
    2: "An older woman in a dim hotel room sits up in bed holding a phone, the bedside clock reads 12:47, a passport rests on the nightstand.",
    4: "Split scene: a worried grandmother holds a phone in a kitchen at dawn while her grandson sleeps peacefully in his apartment.",
    5: "A tired older woman pulling a suitcase at airport arrivals while a man with a lanyard reaches for her luggage handle.",
    6: "An older man at an airport curb stands beside an unmarked sedan with open trunk while the official taxi line waits behind him.",
    7: "An older woman in a hotel lobby holds a phone with no Wi-Fi connection as a cheerful stranger gestures toward the street.",
    8: "An older Black woman shields the keypad of an airport ATM as a well-dressed stranger leans in and points at the buttons.",
    9: "An older couple at an outdoor exchange booth with a 'NO COMMISSION' sign while small print reveals an unfavorable rate.",
    10: "An older woman on a hotel bed holds a phone showing four similar Wi-Fi network names with a fake one highlighted.",
    11: "An older man at a cafe table with his sister moving his phone away as a man approaches with a donation card.",
    12: "An older woman and her adult son speaking with a man in a yellow safety vest at an empty tram stop.",
    13: "An older man holding a hotel-room phone while reading the official front desk number from a reservation card.",
    14: "An older couple at a cruise-port jewelry shop counter while a salesperson presents an appraisal sheet.",
    15: "An older Black woman and an older white man at an outdoor cafe with a menu showing 'MARKET PRICE' instead of prices.",
    16: "An older woman at a museum plaza calmly declining a colored bracelet a man tries to tie onto her wrist.",
    17: "An older woman in a cruise dining room sits across from a man whose body language is intimately attentive.",
    19: "An older woman on a stone bench is approached by a confident stranger offering a business card while the U.S. Consulate is visible in the background.",
}


def insert_chapter_images(text: str) -> str:
    """Insert image references after the chapter intro paragraphs and before
    the first `> **Quick Take**` blockquote in each chapter.

    Strategy: for each chapter heading, find the earliest `> **Quick Take**`
    that follows it. Insert the image markdown immediately before that line.
    """
    lines = text.split("\n")
    out: list[str] = []
    pending_chapter: int | None = None

    chapter_re = re.compile(r"^## Chapter (\d+):")

    for i, line in enumerate(lines):
        m = chapter_re.match(line)
        if m:
            pending_chapter = int(m.group(1))
            out.append(line)
            continue

        # When we hit the Quick Take callout for the chapter we're tracking,
        # emit the image just before it.
        if pending_chapter is not None and line.strip() == "> **Quick Take**":
            scene = CHAPTER_SCENES.get(pending_chapter)
            if scene:
                alt = CHAPTER_ALT.get(pending_chapter, f"Chapter {pending_chapter} illustration")
                # Ensure a blank line before the image
                if out and out[-1].strip() != "":
                    out.append("")
                out.append(f"![{alt}](assets/chapter-scenes/{scene})")
                out.append("")
            pending_chapter = None
            out.append(line)
            continue

        out.append(line)

    return "\n".join(out)


def build_assembled_markdown() -> Path:
    src = MANUSCRIPT_SRC.read_text()
    assembled = insert_chapter_images(src)
    dest = BUILD / "manuscript-with-images.md"
    dest.write_text(assembled)
    return dest


def build_epub(md_path: Path) -> Path:
    epub_out = BUILD / f'{CONFIG["output_filename"]}.epub'
    cover = ASSETS_COVERS / "front-titled.jpg"
    if not cover.exists():
        sys.exit(f"cover image not found at {cover}")

    cmd = [
        "pandoc",
        "--from=markdown+footnotes+pipe_tables+task_lists",
        "--to=epub3",
        f"--output={epub_out}",
        f"--metadata=title={CONFIG['title']}",
        f"--metadata=author={CONFIG['author']}",
        f"--metadata=publisher={CONFIG['publisher']}",
        f"--metadata=language={CONFIG['language']}",
        f"--metadata=rights={CONFIG['rights']}",
        f"--metadata=description={CONFIG['description'].strip()}",
        f"--epub-cover-image={cover}",
        "--toc",
        "--toc-depth=2",
        "--resource-path", str(HERE),
        str(md_path),
    ]
    print(f"[build] {' '.join(cmd[:4])}…")
    subprocess.run(cmd, check=True)
    return epub_out


def main() -> None:
    md = build_assembled_markdown()
    print(f"[build] assembled markdown → {md}")
    epub = build_epub(md)
    print(f"[build] EPUB → {epub}")


if __name__ == "__main__":
    main()
