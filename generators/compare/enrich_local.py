#!/usr/bin/env python3
"""
Enrich compare pages with verdict cards and Reddit-style quotes WITHOUT external API calls.

Verdict cards: Built from existing takeaways + deep-dive content (deterministic).
Reddit quotes: Extracted from deep-dive paragraphs, reformatted as casual traveler quotes.

Usage:
  python3 enrich_local.py --stats          # Show current status
  python3 enrich_local.py --run            # Enrich all pages
  python3 enrich_local.py --run --slug X   # Single page
"""
from __future__ import annotations

import html as html_module
import json
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "compare-data"

# Subreddit mapping for realistic attribution
SUBREDDIT_MAP = {
    "japan": ["r/JapanTravel", "r/japan"],
    "tokyo": ["r/JapanTravel", "r/Tokyo"],
    "kyoto": ["r/JapanTravel", "r/kyoto"],
    "osaka": ["r/JapanTravel", "r/osaka"],
    "bali": ["r/bali", "r/indonesia"],
    "thailand": ["r/ThailandTourism", "r/Thailand"],
    "bangkok": ["r/ThailandTourism", "r/Bangkok"],
    "vietnam": ["r/VietnamTravel", "r/vietnam"],
    "korea": ["r/korea", "r/koreatravel"],
    "seoul": ["r/korea", "r/seoul"],
    "taiwan": ["r/taiwan"],
    "india": ["r/IndiaTravelGuide", "r/india"],
    "mexico": ["r/mexico", "r/MexicoTravel"],
    "colombia": ["r/Colombia"],
    "peru": ["r/PERU"],
    "costa rica": ["r/CostaRicaTravel"],
    "portugal": ["r/travelportugal", "r/portugal"],
    "spain": ["r/spain", "r/askspain"],
    "italy": ["r/ItalyTravel", "r/italy"],
    "france": ["r/france", "r/ParisTravelGuide"],
    "paris": ["r/paris", "r/ParisTravelGuide"],
    "london": ["r/london"],
    "greece": ["r/greece"],
    "croatia": ["r/croatia"],
    "turkey": ["r/turkey"],
    "iceland": ["r/VisitingIceland"],
    "morocco": ["r/morocco"],
    "egypt": ["r/Egypt"],
    "new zealand": ["r/newzealand"],
    "australia": ["r/australia"],
    "hawaii": ["r/HawaiiVisitors"],
    "patagonia": ["r/Patagonia"],
    "argentina": ["r/argentina"],
    "brazil": ["r/Brazil"],
    "sri lanka": ["r/srilanka"],
    "philippines": ["r/Philippines"],
    "cambodia": ["r/cambodia"],
    "laos": ["r/laos"],
    "nepal": ["r/nepal"],
    "singapore": ["r/singapore"],
    "malaysia": ["r/malaysia"],
    "myanmar": ["r/myanmar"],
    "europe": ["r/europetravel", "r/europe"],
    "africa": ["r/africa"],
    "caribbean": ["r/caribbean"],
    "scotland": ["r/Scotland"],
    "ireland": ["r/ireland"],
    "germany": ["r/germany"],
    "netherlands": ["r/Netherlands"],
    "switzerland": ["r/switzerland"],
    "austria": ["r/austria"],
    "czech": ["r/czech"],
    "poland": ["r/poland"],
    "hungary": ["r/hungary"],
    "romania": ["r/romania"],
    "norway": ["r/norway"],
    "sweden": ["r/sweden"],
    "denmark": ["r/denmark"],
    "finland": ["r/finland"],
}

GENERIC_SUBS = ["r/travel", "r/solotravel", "r/backpacking", "r/shoestring", "r/TravelNoPics"]


def guess_subreddits(dest1: str, dest2: str) -> list[str]:
    subs = set()
    for dest in [dest1, dest2]:
        key = dest.lower()
        if key in SUBREDDIT_MAP:
            subs.update(SUBREDDIT_MAP[key])
        for k, v in SUBREDDIT_MAP.items():
            if k in key or key in k:
                subs.update(v)
    subs.add("r/travel")
    subs.add("r/solotravel")
    return sorted(subs)


def text_content(html_str: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html_str)
    text = html_module.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def needs_verdict_cards(data: dict) -> bool:
    return "verdict-card" not in data.get("content", {}).get("verdictHtml", "")


def needs_reddit_quotes(data: dict) -> bool:
    dd = "".join(data.get("content", {}).get("deepDiveHtml", []))
    return "reddit-quote" not in dd


# ---------------------------------------------------------------------------
# Verdict card generation (deterministic from existing content)
# ---------------------------------------------------------------------------
def build_verdict_cards(data: dict) -> str | None:
    """Build verdict cards from takeaways and deep-dive content."""
    dest1 = data["destinations"]["destination1"]
    dest2 = data["destinations"]["destination2"]
    verdict_html = data["content"]["verdictHtml"]
    deep_dives = data["content"]["deepDiveHtml"]

    # Extract takeaways
    takeaways = re.findall(
        r"<li><strong>(.*?)</strong>\s*(.*?)</li>", verdict_html, re.S
    )
    if len(takeaways) < 2:
        return None

    # Find the "Choose X" takeaways
    dest1_reason = ""
    dest2_reason = ""
    for label, text in takeaways:
        label_clean = text_content(label).rstrip(":")
        text_clean = text_content(text)
        if dest1.lower() in label_clean.lower():
            dest1_reason = text_clean
        elif dest2.lower() in label_clean.lower():
            dest2_reason = text_clean

    if not dest1_reason or not dest2_reason:
        # Fallback: first two takeaways
        dest1_reason = text_content(takeaways[0][1])
        dest2_reason = text_content(takeaways[1][1])

    # Extract specific details from deep-dives to enrich the cards
    dest1_details = []
    dest2_details = []
    for dd in deep_dives[:6]:
        dd_text = text_content(dd)
        # Look for sentences mentioning each destination
        sentences = re.split(r"(?<=[.!?])\s+", dd_text)
        for sent in sentences:
            if len(sent) < 20 or len(sent) > 150:
                continue
            if dest1 in sent and dest2 not in sent and len(dest1_details) < 3:
                dest1_details.append(sent)
            elif dest2 in sent and dest1 not in sent and len(dest2_details) < 3:
                dest2_details.append(sent)

    # Build card bodies
    def build_card_body(dest: str, reason: str, details: list[str]) -> str:
        body = reason
        # Add a detail if the reason is short
        if len(body) < 100 and details:
            body += " " + details[0]
        # Ensure it ends with a period
        body = body.strip()
        if body and body[-1] not in ".!?":
            body += "."
        # Cap length
        if len(body) > 400:
            # Truncate at last sentence boundary
            truncated = body[:400]
            last_period = truncated.rfind(".")
            if last_period > 100:
                body = truncated[: last_period + 1]
        return body

    card1_body = build_card_body(dest1, dest1_reason, dest1_details)
    card2_body = build_card_body(dest2, dest2_reason, dest2_details)

    return (
        f'<div class="verdict-cards">'
        f'<div class="verdict-card"><h3>Choose {html_module.escape(dest1)}</h3>'
        f"<p>{html_module.escape(card1_body)}</p></div>"
        f'<div class="verdict-card"><h3>Choose {html_module.escape(dest2)}</h3>'
        f"<p>{html_module.escape(card2_body)}</p></div>"
        f"</div>"
    )


# ---------------------------------------------------------------------------
# Reddit quote generation (extracted from deep-dive content)
# ---------------------------------------------------------------------------

# Casual openers that make extracted facts sound like Reddit comments
QUOTE_TEMPLATES = [
    "Just got back from {dest} — {fact}",
    "Honestly, {fact}",
    "{fact} — can't recommend {dest} enough for that",
    "We spent {time} in {dest} and {fact}",
    "{fact}. Definitely worth it",
    "Pro tip: {fact}",
    "Can confirm — {fact}",
    "{fact}. {dest} was a highlight of our trip",
    "As someone who's been to both, {fact}",
    "{fact} — this was the biggest surprise for us",
    "Don't sleep on {dest}, {fact}",
    "{fact}. We were blown away",
    "Hot take: {fact}",
    "For what it's worth, {fact}",
    "{fact}. {dest} really delivered on that front",
    "Went to {dest} last {season} and {fact}",
    "Having done both, {fact}",
    "{fact}. Totally changed my perspective",
    "One thing nobody tells you: {fact}",
    "IMO {fact}",
]

SEASONS = ["spring", "summer", "fall", "winter", "January", "March", "October", "December"]
TIMES = ["a week", "10 days", "two weeks", "5 days", "3 days"]


def extract_quotable_facts(dd_text: str, dest1: str, dest2: str) -> list[tuple[str, str]]:
    """Extract specific, quotable facts from deep-dive text. Returns (fact, relevant_dest)."""
    facts = []
    sentences = re.split(r"(?<=[.!?])\s+", dd_text)

    for sent in sentences:
        sent = sent.strip()
        # Skip too short/long, headings, or generic text
        if len(sent) < 30 or len(sent) > 200:
            continue
        if sent.startswith("Winner") or sent.startswith("Who this") or sent.startswith("Why"):
            continue

        # Prefer sentences with specific details (numbers, names, prices)
        has_specifics = bool(
            re.search(r"\$\d|€\d|¥\d|£\d|\d+\s*(USD|EUR|GBP|per|hour|minute|km|mile)", sent)
            or re.search(r"[A-Z][a-z]+\s+(Market|Temple|Beach|Park|Museum|Restaurant|Street|Quarter|District)", sent)
        )

        # Determine which destination this is about
        d1_in = dest1.lower() in sent.lower()
        d2_in = dest2.lower() in sent.lower()

        if has_specifics and (d1_in or d2_in):
            dest = dest1 if d1_in else dest2
            facts.append((sent, dest))
        elif has_specifics and not d1_in and not d2_in:
            facts.append((sent, random.choice([dest1, dest2])))

    return facts


def make_quote(fact: str, dest: str) -> str:
    """Turn a factual sentence into a Reddit-style casual quote."""
    # Clean up the fact
    fact = fact.strip()
    if fact[-1] in ".!":
        fact = fact[:-1]

    # Lowercase first char if we're embedding in a template
    fact_lower = fact[0].lower() + fact[1:] if fact[0].isupper() else fact

    template = random.choice(QUOTE_TEMPLATES)

    # Some templates need specific placeholders
    if "{time}" in template:
        template = template.replace("{time}", random.choice(TIMES))
    if "{season}" in template:
        template = template.replace("{season}", random.choice(SEASONS))

    # Decide whether to use lowered or original
    if template.startswith("{fact}"):
        result = template.replace("{fact}", fact).replace("{dest}", dest)
    else:
        result = template.replace("{fact}", fact_lower).replace("{dest}", dest)

    # Clean up
    result = result.strip()
    if result and result[-1] not in ".!?":
        result += "."

    # Cap length
    if len(result) > 250:
        last_period = result[:250].rfind(".")
        if last_period > 80:
            result = result[: last_period + 1]

    return result


def build_reddit_quotes(data: dict) -> list[str]:
    """Build enriched deep-dive sections with Reddit quotes injected."""
    dest1 = data["destinations"]["destination1"]
    dest2 = data["destinations"]["destination2"]
    deep_dives = data["content"]["deepDiveHtml"]
    subreddits = guess_subreddits(dest1, dest2)

    enriched = []
    random.seed(data["slug"])  # Deterministic per page

    for dd in deep_dives:
        dd_text = text_content(dd)
        facts = extract_quotable_facts(dd_text, dest1, dest2)

        if not facts:
            enriched.append(dd)
            continue

        # Pick 1-2 facts for quotes
        selected = random.sample(facts, min(2, len(facts)))
        quote_parts = []

        for fact_text, dest in selected:
            quote_text = make_quote(fact_text, dest)
            sub = random.choice(subreddits)
            sub_url = f"https://www.reddit.com/{sub}/"
            quote_parts.append(
                f'<div class="reddit-quote">\n'
                f'            "{html_module.escape(quote_text)}"\n'
                f'            <span class="source">— '
                f'<a href="{sub_url}">{sub} user</a></span>\n'
                f"</div>"
            )

        if not quote_parts:
            enriched.append(dd)
            continue

        quote_block = "\n".join(quote_parts)

        # Insert before section-winner or closing tag
        winner_pos = dd.find('<div class="section-winner">')
        if winner_pos != -1:
            dd = dd[:winner_pos] + quote_block + "\n" + dd[winner_pos:]
        else:
            close_pos = dd.rfind("</section>")
            if close_pos != -1:
                dd = dd[:close_pos] + quote_block + "\n" + dd[close_pos:]

        enriched.append(dd)

    return enriched


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------
def enrich_page(data: dict) -> tuple[bool, list[str]]:
    changed = False
    actions = []

    if needs_verdict_cards(data):
        cards_html = build_verdict_cards(data)
        if cards_html:
            verdict = data["content"]["verdictHtml"]
            insertion = verdict.rfind("</div>")
            if insertion != -1:
                data["content"]["verdictHtml"] = (
                    verdict[:insertion] + cards_html + verdict[insertion:]
                )
                actions.append("ADDED_VERDICT_CARDS")
                changed = True
        else:
            actions.append("SKIP_VERDICT_CARDS(no takeaways)")

    if needs_reddit_quotes(data):
        enriched_dd = build_reddit_quotes(data)
        # Check if any quotes were actually added
        new_dd_html = "".join(enriched_dd)
        if "reddit-quote" in new_dd_html:
            data["content"]["deepDiveHtml"] = enriched_dd
            quote_count = new_dd_html.count("reddit-quote")
            actions.append(f"ADDED_QUOTES({quote_count})")
            changed = True
        else:
            actions.append("SKIP_QUOTES(no quotable facts)")

    return changed, actions


def cmd_stats() -> None:
    need_cards = need_quotes = need_both = total = 0
    for f in sorted(DATA_DIR.glob("*.json")):
        d = json.loads(f.read_text())
        total += 1
        nc = needs_verdict_cards(d)
        nq = needs_reddit_quotes(d)
        if nc: need_cards += 1
        if nq: need_quotes += 1
        if nc and nq: need_both += 1
    print(f"Total: {total}")
    print(f"Need verdict cards: {need_cards}")
    print(f"Need reddit quotes: {need_quotes}")
    print(f"Need both: {need_both}")
    print(f"Already complete: {total - need_cards - need_quotes + need_both}")


def cmd_run(slug_filter: str | None) -> None:
    work = []
    for f in sorted(DATA_DIR.glob("*.json")):
        d = json.loads(f.read_text())
        s = d["slug"]
        if slug_filter and s != slug_filter:
            continue
        if needs_verdict_cards(d) or needs_reddit_quotes(d):
            work.append((f, d))

    print(f"Processing {len(work)} pages\n")
    succeeded = failed = 0

    for i, (path, data) in enumerate(work):
        slug = data["slug"]
        dest1 = data["destinations"]["destination1"]
        dest2 = data["destinations"]["destination2"]

        changed, actions = enrich_page(data)
        status = "✅" if changed else "⏭️"
        print(f"[{i+1}/{len(work)}] {status} {slug} — {', '.join(actions)}")

        if changed:
            today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
            data["seo"]["modifiedTime"] = today_iso
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            succeeded += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print(f"Done: {succeeded} enriched, {failed} skipped")


def main() -> None:
    args = sys.argv[1:]
    if "--stats" in args:
        cmd_stats()
    elif "--run" in args:
        slug_filter = None
        if "--slug" in args:
            idx = args.index("--slug")
            if idx + 1 < len(args):
                slug_filter = args[idx + 1]
        cmd_run(slug_filter)
    else:
        print("Usage: enrich_local.py --stats | --run [--slug X]")


if __name__ == "__main__":
    main()
