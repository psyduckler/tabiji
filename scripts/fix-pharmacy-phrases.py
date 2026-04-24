#!/usr/bin/env python3
"""
fix-pharmacy-phrases.py — Populate empty pharmacy-phrase blocks on 30 country
health pages.

Background: 30 country pages in /health/{slug}/ ship with 5 blank
`<li><strong>:</strong> </li>` placeholders under the "Useful Pharmacy Phrases"
heading. The underlying health-data/*.json files already have the phrases
populated — this is a rendering gap in the original batch generator, not a
data gap. This script reads the JSON and patches the 30 HTML files in-place.

Usage:
    python3 scripts/fix-pharmacy-phrases.py          # patch all 30
    python3 scripts/fix-pharmacy-phrases.py --check  # dry-run; report what'd change
"""

import argparse
import html as html_mod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEALTH_DIR = ROOT / "health"
HEALTH_DATA = ROOT / "health-data"

# The batch generator left two variants of broken pharmacy-phrase blocks:
#   A) fully empty: `<li><strong>:</strong> </li>`   (e.g. Afghanistan, Syria)
#   B) partial:     `<li><strong>:</strong> I need headache medicine</li>`
#      (English-speaking countries where the "translation" slot got filled
#       but the English-prompt label got dropped)
# Both start the <ul> with <li><strong>:</strong> and have 5 such rows.
EMPTY_BLOCK_PATTERN = re.compile(
    r'(<ul>)\n(?:  <li><strong>:</strong>[^<\n]*</li>\n){5}(</ul>)',
    re.MULTILINE,
)

# Capture non-English text before a trailing parenthesized pronunciation.
_PRONUNCIATION = re.compile(r'^(.*?)\s*\(([^)]+)\)\s*$', re.DOTALL)


def split_pronunciation(text: str):
    """Return (native_text, pronunciation_or_None)."""
    m = _PRONUNCIATION.match(text.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return text.strip(), None


def normalize_entry(entry: dict):
    """Normalize a pharmacyPhrases entry to (english_prompt, native, pronunciation)."""
    meaning = (entry.get("meaning") or "").strip()
    phrase = (entry.get("phrase") or "").strip()
    local = (entry.get("local") or "").strip()

    if meaning and phrase and meaning != phrase:
        english_prompt = meaning
        native_raw = phrase
    elif phrase and local and phrase != local:
        english_prompt = phrase
        native_raw = local
    elif phrase and local and phrase == local:
        english_prompt = phrase
        native_raw = phrase
    elif meaning and not phrase:
        english_prompt = meaning
        native_raw = meaning
    else:
        english_prompt = meaning or phrase or local or "(missing phrase)"
        native_raw = phrase or local or meaning

    native, pronunciation = split_pronunciation(native_raw)
    return english_prompt, native, pronunciation


def render_phrases_block(phrases) -> str:
    """Render populated <li> rows for the 5 phrases (normalized from JSON)."""
    rows = []
    for entry in phrases[:5]:
        english_prompt, native, pronunciation = normalize_entry(entry)
        prompt_html = html_mod.escape(english_prompt)
        if native and native != english_prompt:
            if pronunciation:
                rows.append(
                    f'  <li><strong>{prompt_html}:</strong> {html_mod.escape(native)} '
                    f'<em>({html_mod.escape(pronunciation)})</em></li>'
                )
            else:
                rows.append(f'  <li><strong>{prompt_html}:</strong> {html_mod.escape(native)}</li>')
        elif pronunciation:
            rows.append(
                f'  <li><strong>{prompt_html}:</strong> '
                f'<em>({html_mod.escape(pronunciation)})</em></li>'
            )
        else:
            rows.append(f'  <li><strong>{prompt_html}</strong></li>')
    while len(rows) < 5:
        rows.append('  <li></li>')
    return "<ul>\n" + "\n".join(rows) + "\n</ul>"


def load_phrases_by_slug():
    """Map country slug → pharmacyPhrases list (from /health-data/*.json)."""
    out = {}
    for p in HEALTH_DATA.glob("*.json"):
        try:
            data = json.loads(p.read_text())
        except Exception:
            continue
        slug = data.get("countrySlug")
        phrases = data.get("pharmacyPhrases")
        if slug and phrases:
            out[slug] = phrases
    return out


def affected_country_pages():
    """Yield (slug, path) for pages that still contain the empty placeholder."""
    for path in sorted(HEALTH_DIR.glob("*/index.html")):
        text = path.read_text()
        if EMPTY_BLOCK_PATTERN.search(text):
            yield path.parent.name, path


def patch_file(path: Path, phrases) -> bool:
    text = path.read_text()
    new_block = render_phrases_block(phrases)
    new_text, n = EMPTY_BLOCK_PATTERN.subn(new_block, text, count=1)
    if n == 0:
        return False
    path.write_text(new_text)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Dry-run: report without writing")
    args = parser.parse_args()

    phrases_by_slug = load_phrases_by_slug()
    affected = list(affected_country_pages())
    print(f"Found {len(affected)} country pages with empty pharmacy phrases.")

    patched = 0
    skipped = []
    for slug, path in affected:
        phrases = phrases_by_slug.get(slug)
        if not phrases:
            skipped.append((slug, "no phrase data in health-data/"))
            continue
        if args.check:
            sample = normalize_entry(phrases[0])[0]
            print(f"  would patch {slug}  (first phrase: {sample!r})")
        else:
            if patch_file(path, phrases):
                patched += 1
                print(f"  patched {slug}")
            else:
                skipped.append((slug, "placeholder regex did not match"))

    if skipped:
        print("\nSkipped:")
        for slug, reason in skipped:
            print(f"  {slug}: {reason}")

    if not args.check:
        print(f"\nPatched {patched}/{len(affected)} pages.")


if __name__ == "__main__":
    main()
