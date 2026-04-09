#!/usr/bin/env python3
"""
Enrich compare pages with missing verdict cards and Reddit-style quotes.

Reads each compare-data JSON, checks for missing elements, uses Gemini to generate
them, injects into HTML, and saves. Idempotent — skips pages that already have content.

Usage:
  python3 enrich_compare.py                   # Enrich all pages (dry-run)
  python3 enrich_compare.py --run             # Enrich all pages (write changes)
  python3 enrich_compare.py --run --slug tokyo-vs-kyoto  # Single page
  python3 enrich_compare.py --run --limit 50  # First N pages needing work
  python3 enrich_compare.py --stats           # Show current status
"""
from __future__ import annotations

import html as html_module
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "compare-data"
PROGRESS_PATH = Path("/tmp/enrich-compare-progress.json")

def _get_keychain_key(service):
    import subprocess as _sp
    return _sp.run(['security', 'find-generic-password', '-s', service, '-w'],
                   capture_output=True, text=True).stdout.strip()

GEMINI_KEY = os.environ.get("GEMINI_KEY") or _get_keychain_key("gemini-api-key")
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}"

# Subreddit mapping for common destinations/regions
SUBREDDIT_MAP = {
    "japan": ["r/JapanTravel", "r/japan"],
    "tokyo": ["r/JapanTravel", "r/Tokyo"],
    "kyoto": ["r/JapanTravel", "r/kyoto"],
    "osaka": ["r/JapanTravel", "r/osaka"],
    "bali": ["r/bali", "r/indonesia"],
    "thailand": ["r/ThailandTourism", "r/Thailand"],
    "bangkok": ["r/ThailandTourism", "r/Bangkok"],
    "chiang mai": ["r/ThailandTourism", "r/chiangmai"],
    "vietnam": ["r/VietnamTravel", "r/vietnam"],
    "korea": ["r/korea", "r/koreatravel"],
    "seoul": ["r/korea", "r/seoul"],
    "taiwan": ["r/taiwan"],
    "india": ["r/IndiaTravelGuide", "r/india"],
    "mexico": ["r/mexico", "r/MexicoTravel"],
    "mexico city": ["r/MexicoCity"],
    "colombia": ["r/Colombia"],
    "peru": ["r/PERU"],
    "costa rica": ["r/CostaRicaTravel"],
    "portugal": ["r/travelportugal", "r/portugal"],
    "spain": ["r/spain", "r/askspain"],
    "italy": ["r/ItalyTravel", "r/italy"],
    "france": ["r/france", "r/paris"],
    "paris": ["r/paris", "r/ParisTravelGuide"],
    "london": ["r/london"],
    "greece": ["r/greece"],
    "croatia": ["r/croatia"],
    "turkey": ["r/turkey", "r/istanbul"],
    "iceland": ["r/VisitingIceland"],
    "morocco": ["r/morocco"],
    "egypt": ["r/Egypt"],
    "new zealand": ["r/newzealand"],
    "australia": ["r/australia"],
    "hawaii": ["r/HawaiiVisitors"],
    "canada": ["r/canada"],
    "patagonia": ["r/Patagonia", "r/travel"],
    "argentina": ["r/argentina"],
    "brazil": ["r/Brazil"],
}


def guess_subreddits(dest1: str, dest2: str) -> list[str]:
    """Guess relevant subreddits from destination names."""
    subs = set()
    for dest in [dest1, dest2]:
        key = dest.lower()
        if key in SUBREDDIT_MAP:
            subs.update(SUBREDDIT_MAP[key])
        # Try partial matches
        for k, v in SUBREDDIT_MAP.items():
            if k in key or key in k:
                subs.update(v)
    subs.add("r/travel")
    subs.add("r/solotravel")
    return sorted(subs)[:4]


def call_gemini(prompt: str, max_retries: int = 3) -> str:
    """Call Gemini API and return the text response."""
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.85,
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json"
        }
    })

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                GEMINI_URL,
                data=body.encode(),
                headers={"Content-Type": "application/json"}
            )
            resp = urllib.request.urlopen(req, timeout=60)
            result = json.loads(resp.read())
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = re.sub(r'^```json\s*', '', text.strip())
            text = re.sub(r'\s*```$', '', text.strip())
            return text
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 + attempt * 3
                print(f"    Retry {attempt+1}: {e} (waiting {wait}s)")
                time.sleep(wait)
            else:
                raise


def needs_verdict_cards(data: dict) -> bool:
    verdict_html = data.get("content", {}).get("verdictHtml", "")
    return "verdict-card" not in verdict_html


def needs_reddit_quotes(data: dict) -> bool:
    dd_html = "".join(data.get("content", {}).get("deepDiveHtml", []))
    return "reddit-quote" not in dd_html


def extract_verdict_text(verdict_html: str) -> dict:
    """Extract existing verdict content for context."""
    summary_match = re.search(r'<strong>(.*?)</strong>', verdict_html, re.S)
    summary = html_module.unescape(re.sub(r'<[^>]+>', '', summary_match.group(1))) if summary_match else ""

    takeaways = []
    for m in re.finditer(r'<li><strong>([^<]+)</strong>\s*(.*?)</li>', verdict_html, re.S):
        takeaways.append({"label": m.group(1).strip(), "text": m.group(2).strip()})

    return {"summary": summary, "takeaways": takeaways}


def extract_deep_dive_context(deep_dives: list[str]) -> list[dict]:
    """Extract section name and text from each deep-dive for quote generation."""
    sections = []
    for dd in deep_dives:
        title_match = re.search(r'<h2[^>]*>(.*?)</h2>', dd, re.S)
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else "Unknown"
        # Remove emoji prefix
        title = re.sub(r'^[\U00010000-\U0010ffff\u2600-\u27bf\u2702-\u27b0]+\s*', '', title).strip()

        # Extract plain text
        text = re.sub(r'<[^>]+>', ' ', dd)
        text = html_module.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()[:500]

        sections.append({"title": title, "text": text})
    return sections


def generate_verdict_cards(dest1: str, dest2: str, verdict_context: dict) -> str | None:
    """Generate verdict cards HTML using Gemini."""
    prompt = f"""You are writing verdict cards for a travel comparison page: {dest1} vs {dest2}.

Existing verdict summary: "{verdict_context['summary']}"

Existing takeaways:
{json.dumps(verdict_context['takeaways'], indent=2)}

Generate exactly 2 verdict cards as JSON. Each card should be a compelling 2-3 sentence paragraph explaining when/why to choose that destination, with specific details (activities, traveler types, budget notes).

Output ONLY valid JSON:
{{
  "cards": [
    {{"heading": "Choose {dest1}", "body": "2-3 sentences about when to choose {dest1}..."}},
    {{"heading": "Choose {dest2}", "body": "2-3 sentences about when to choose {dest2}..."}}
  ]
}}

Requirements:
- Each card body should be 40-80 words
- Be specific and opinionated, not generic
- Mention specific activities, neighborhoods, or experiences
- Include who this destination is "best for"
- Don't repeat the summary verbatim — complement it
"""
    try:
        text = call_gemini(prompt)
        result = json.loads(text)
        cards = result.get("cards", [])
        if len(cards) < 2:
            return None

        cards_html = '<div class="verdict-cards">'
        for card in cards[:2]:
            heading = html_module.escape(card["heading"])
            body = html_module.escape(card["body"])
            cards_html += f'<div class="verdict-card"><h3>{heading}</h3><p>{body}</p></div>'
        cards_html += '</div>'
        return cards_html
    except Exception as e:
        print(f"    ❌ Verdict card generation failed: {e}")
        return None


def generate_reddit_quotes(dest1: str, dest2: str, sections: list[dict], subreddits: list[str]) -> list[dict] | None:
    """Generate Reddit-style quotes for deep-dive sections using Gemini."""
    section_list = "\n".join(
        f"  {i+1}. {s['title']}: {s['text'][:200]}..."
        for i, s in enumerate(sections)
    )
    sub_list = ", ".join(subreddits)

    prompt = f"""You are generating realistic Reddit-style quotes for a {dest1} vs {dest2} travel comparison page.

Sections needing quotes:
{section_list}

Generate 1-2 short Reddit quotes per section. These should sound like real travelers sharing genuine experiences — casual, specific, opinionated. Reference actual place names, prices, or experiences.

Available subreddits for attribution: {sub_list}

Output ONLY valid JSON:
{{
  "sections": [
    {{
      "sectionIndex": 0,
      "quotes": [
        {{"text": "Short casual quote (15-40 words)...", "subreddit": "r/travel"}}
      ]
    }},
    ...
  ]
}}

Requirements:
- Each quote should be 15-40 words
- Sound authentic — use casual language, specific details, personal experience
- Mix up the subreddit attributions (don't use the same one for every quote)
- 1 quote for simpler sections, 2 for major sections like food/budget/culture
- Don't use exclamation marks excessively
- Include specific costs, place names, or practical tips where natural
"""
    try:
        text = call_gemini(prompt)
        result = json.loads(text)
        return result.get("sections", [])
    except Exception as e:
        print(f"    ❌ Reddit quote generation failed: {e}")
        return None


def inject_verdict_cards(verdict_html: str, cards_html: str) -> str:
    """Inject verdict cards into existing verdict HTML (after takeaways list)."""
    # Insert cards right before the closing </div> of verdict-box
    insertion_point = verdict_html.rfind("</div>")
    if insertion_point == -1:
        return verdict_html
    return verdict_html[:insertion_point] + cards_html + verdict_html[insertion_point:]


def inject_reddit_quotes(deep_dives: list[str], quote_sections: list[dict], subreddits: list[str]) -> list[str]:
    """Inject Reddit quotes into deep-dive sections."""
    # Build a map of section index -> quotes
    quote_map = {}
    for qs in quote_sections:
        idx = qs.get("sectionIndex", -1)
        if 0 <= idx < len(deep_dives):
            quote_map[idx] = qs.get("quotes", [])

    enriched = []
    for i, dd in enumerate(deep_dives):
        if i not in quote_map:
            enriched.append(dd)
            continue

        quotes = quote_map[i]
        if not quotes:
            enriched.append(dd)
            continue

        # Build quote HTML
        quote_parts = []
        for q in quotes[:2]:  # Max 2 quotes per section
            sub = q.get("subreddit", "r/travel")
            if not sub.startswith("r/"):
                sub = f"r/{sub}"
            sub_url = f"https://www.reddit.com/{sub}/"
            quote_text = html_module.escape(q["text"].strip().strip('"'))
            quote_parts.append(
                f'<div class="reddit-quote">\n'
                f'            "{quote_text}"\n'
                f'            <span class="source">— <a href="{sub_url}">{sub} user</a></span>\n'
                f'</div>'
            )

        quote_block = "\n".join(quote_parts)

        # Insert quotes before the section-winner div, or before closing </section>
        winner_pos = dd.find('<div class="section-winner">')
        if winner_pos != -1:
            dd = dd[:winner_pos] + quote_block + "\n" + dd[winner_pos:]
        else:
            close_pos = dd.rfind("</section>")
            if close_pos != -1:
                dd = dd[:close_pos] + quote_block + "\n" + dd[close_pos:]

        enriched.append(dd)
    return enriched


def load_progress() -> dict:
    if PROGRESS_PATH.exists():
        return json.loads(PROGRESS_PATH.read_text())
    return {"completed": [], "failed": []}


def save_progress(progress: dict) -> None:
    PROGRESS_PATH.write_text(json.dumps(progress, indent=2))


def enrich_page(data: dict, dry_run: bool = True) -> tuple[bool, list[str]]:
    """Enrich a single page. Returns (changed, actions_taken)."""
    slug = data["slug"]
    dest1 = data["destinations"]["destination1"]
    dest2 = data["destinations"]["destination2"]
    actions = []
    changed = False

    # --- Verdict cards ---
    if needs_verdict_cards(data):
        verdict_context = extract_verdict_text(data["content"]["verdictHtml"])
        if dry_run:
            actions.append("WOULD_ADD_VERDICT_CARDS")
        else:
            cards_html = generate_verdict_cards(dest1, dest2, verdict_context)
            if cards_html:
                data["content"]["verdictHtml"] = inject_verdict_cards(
                    data["content"]["verdictHtml"], cards_html
                )
                actions.append("ADDED_VERDICT_CARDS")
                changed = True
            else:
                actions.append("FAILED_VERDICT_CARDS")

    # --- Reddit quotes ---
    if needs_reddit_quotes(data):
        sections = extract_deep_dive_context(data["content"]["deepDiveHtml"])
        subreddits = guess_subreddits(dest1, dest2)
        if dry_run:
            actions.append(f"WOULD_ADD_QUOTES({len(sections)} sections)")
        else:
            quote_sections = generate_reddit_quotes(dest1, dest2, sections, subreddits)
            if quote_sections:
                data["content"]["deepDiveHtml"] = inject_reddit_quotes(
                    data["content"]["deepDiveHtml"], quote_sections, subreddits
                )
                actions.append(f"ADDED_QUOTES({len(quote_sections)} sections)")
                changed = True
            else:
                actions.append("FAILED_QUOTES")

    return changed, actions


def cmd_stats() -> None:
    """Print current enrichment status."""
    need_cards = 0
    need_quotes = 0
    need_both = 0
    total = 0

    for f in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        total += 1
        nc = needs_verdict_cards(data)
        nq = needs_reddit_quotes(data)
        if nc:
            need_cards += 1
        if nq:
            need_quotes += 1
        if nc and nq:
            need_both += 1

    print(f"Total compare pages: {total}")
    print(f"Need verdict cards:  {need_cards}")
    print(f"Need reddit quotes:  {need_quotes}")
    print(f"Need both:           {need_both}")
    print(f"Already complete:    {total - need_cards - need_quotes + need_both}")

    progress = load_progress()
    if progress["completed"]:
        print(f"\nPreviously enriched: {len(progress['completed'])}")
    if progress["failed"]:
        print(f"Previously failed:   {len(progress['failed'])}")


def cmd_enrich(dry_run: bool, slug_filter: str | None, limit: int | None) -> None:
    """Enrich pages missing verdict cards and/or reddit quotes."""
    progress = load_progress()

    # Collect pages needing work — check actual data, not progress file
    work = []
    for f in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        s = data["slug"]
        if slug_filter and s != slug_filter:
            continue
        if needs_verdict_cards(data) or needs_reddit_quotes(data):
            work.append((f, data))

    if limit:
        work = work[:limit]

    print(f"{'DRY RUN — ' if dry_run else ''}Processing {len(work)} pages\n")

    succeeded = 0
    failed = 0

    for i, (path, data) in enumerate(work):
        slug = data["slug"]
        dest1 = data["destinations"]["destination1"]
        dest2 = data["destinations"]["destination2"]
        print(f"[{i+1}/{len(work)}] {slug} ({dest1} vs {dest2})")

        try:
            changed, actions = enrich_page(data, dry_run=dry_run)
            print(f"  → {', '.join(actions)}")

            if changed and not dry_run:
                # Update modifiedTime
                today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
                data["seo"]["modifiedTime"] = today_iso

                # Save JSON
                path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
                print(f"  ✅ Saved {path.name}")

                # Track progress
                progress["completed"].append(slug)
                save_progress(progress)
                succeeded += 1

                # Rate limit: ~1 request per second
                time.sleep(1.5)
            elif dry_run:
                succeeded += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if not dry_run:
                progress["failed"].append(slug)
                save_progress(progress)
            failed += 1
            time.sleep(2)

    print(f"\n{'='*50}")
    print(f"{'DRY RUN ' if dry_run else ''}Results: {succeeded} succeeded, {failed} failed")
    if not dry_run:
        print(f"Progress saved to {PROGRESS_PATH}")
        print(f"\nTo rebuild HTML, run: python3 generators/compare/build_compare.py build")


def main() -> None:
    args = sys.argv[1:]

    if "--stats" in args:
        cmd_stats()
        return

    dry_run = "--run" not in args
    slug_filter = None
    limit = None

    if "--slug" in args:
        idx = args.index("--slug")
        if idx + 1 < len(args):
            slug_filter = args[idx + 1]

    if "--limit" in args:
        idx = args.index("--limit")
        if idx + 1 < len(args):
            limit = int(args[idx + 1])

    cmd_enrich(dry_run, slug_filter, limit)


if __name__ == "__main__":
    main()
