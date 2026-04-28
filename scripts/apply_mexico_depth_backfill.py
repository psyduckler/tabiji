#!/usr/bin/env python3
"""Splice synth-generated narrative opening paragraphs into Mexico HTML.

For each under-depth scam card (depth=2), the synth subagent generated
one new opening paragraph. We insert it as the FIRST <p class="scam-story-body">
in that card — pushing the existing two paragraphs to positions 2 and 3,
matching NYC's scene → mechanism → defense flow.

Insertion point: just before the existing first <p class="scam-story-body">.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INPUT = Path("/tmp/mexico-depth-synth-output.json")


def card_pattern(scam_n: int) -> re.Pattern:
    return re.compile(
        r'(<div class="scam-card"[^>]*id="scam-' + str(scam_n) + r'"[^>]*>)(.*?)'
        r'(?=<div class="scam-card"|<div class="mid-cta"|<!-- What to do)',
        re.DOTALL,
    )


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def splice_one(html: str, scam_n: int, new_para: str) -> tuple[str, bool]:
    pat = card_pattern(scam_n)
    m = pat.search(html)
    if not m:
        return html, False
    head = m.group(1)
    body = m.group(2)
    first_body_m = re.search(r'<p class="scam-story-body">', body)
    if not first_body_m:
        return html, False
    insertion = f'<p class="scam-story-body">{html_escape(new_para)}</p>\n        '
    new_body = (
        body[:first_body_m.start()]
        + insertion
        + body[first_body_m.start():]
    )
    new_html = html[:m.start()] + head + new_body + html[m.end():]
    return new_html, True


def main():
    items = json.loads(INPUT.read_text())
    by_city: dict[str, list[tuple[int, str]]] = {}
    for it in items:
        by_city.setdefault(it["city"], []).append((it["n"], it["new_paragraph"]))

    total_ok = total_fail = 0
    for city, entries in sorted(by_city.items()):
        path = REPO / f"scams/{city}/index.html"
        html = path.read_text()
        # Sort by n descending so earlier-position card edits don't shift
        # later-position card offsets (each splice is local to the card).
        entries.sort(key=lambda x: x[0], reverse=True)
        ok = fail = 0
        for n, new_para in entries:
            html, success = splice_one(html, n, new_para)
            if success:
                ok += 1
            else:
                fail += 1
                print(f"  WARN: {city} scam-{n} splice failed")
        path.write_text(html)
        print(f"  {city}: spliced {ok}/{ok + fail} cards")
        total_ok += ok
        total_fail += fail

    print(f"\nTotal: {total_ok} spliced, {total_fail} failed")


if __name__ == "__main__":
    main()
