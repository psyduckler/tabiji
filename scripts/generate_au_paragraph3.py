#!/usr/bin/env python3
"""Generate the missing 3rd story-body paragraph for Australia scam pages.

Audit (2026-04-28) found 8 of 14 AU cities have only 2 story-body paragraphs
per scam, while NYC canonical has 3. Paragraph 3 carries the broader-pattern
citation (Reddit thread, regulator/embassy/consumer-protection rule, or
established-operator name list) AND ends with a bold-emphasized defensive
recommendation wrapped in <strong>...</strong>.

Cities affected: darwin, gold-coast, hobart, melbourne, perth, port-douglas,
sydney, whitsundays — 48 scams total.

Process:
  1. For each scam, extract (title, location, tldr, p1, p2) from the existing
     index.html. Skip if 3+ paragraphs already exist.
  2. Call Gemini 2.5 Pro with a strict NYC-style prompt + 3 in-corpus examples
     pulled from cairns/byron-bay/canberra (the AU cities already on 3-para).
  3. Write all drafts to /tmp/au-p3-drafts.json for review.

Apply step is separate (apply_au_paragraph3.py) so drafts can be reviewed.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAMS = ROOT / "scams"

CITIES = ["darwin", "gold-coast", "hobart", "melbourne", "perth",
          "port-douglas", "sydney", "whitsundays"]

GEMINI_MODEL = "gemini-2.5-pro"
GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
)


def _gemini_key() -> str:
    return subprocess.run(
        ["security", "find-generic-password", "-s", "gemini-api-key", "-w"],
        capture_output=True, text=True,
    ).stdout.strip()


SYSTEM_PROMPT = """You are a travel-safety editor for tabiji.ai writing the third story-body paragraph for a scam-page card. Your style imitates the New York City canonical at https://tabiji.ai/scams/new-york-city/.

The page already has:
- Paragraph 1: sets the scene with sensory detail and the bait
- Paragraph 2: closes the trap, describes the demand and the social pressure
- Paragraph 3 (the one you write): broader-pattern citation + bold-emphasized defensive line

Required structure for paragraph 3 (~60-95 words):
- Open with EITHER (a) a Reddit-thread reference ("r/<sub> threads document...", "A 2025 r/<sub> thread describes..."), OR (b) a regulator / consumer-protection / industry-body reference (Australian Consumer Law, Fair Trading, ATO, ASIC, NSW Police, MARA, ABN, Tourism Australia, the Indigenous Art Code, etc.), OR (c) a list of legitimate established operators by name.
- Add a specific data point — neighborhood / street name / dollar amount / year / rule code — that anchors the paragraph in this exact city, not a generic Australian city.
- End with a single sentence wrapped in <strong>...</strong> that gives the practical defensive move. The strong-line is followed (outside the <strong>) by an em-dash (—) and one tactical tail clause.

The <strong> sentence must be ACTIONABLE: "Book at <official site>", "Pay only by credit card with chargeback rights", "Verify ABN at abn.business.gov.au", "Walk past anyone offering X — use Y instead", "Film every panel before driving off the lot", etc.

DO NOT:
- Repeat sentences from paragraphs 1 or 2
- Use the word "defence" (it's en-GB; this corpus is en-US — use "defense")
- Open with "Your defense is" (overused; the existing 6 cities lead with that and it has become a tic)
- Use British spellings (centre→center, organised→organized, metres→meters, kerb→curb, mislabelled→mislabeled)
- Mention dollar amounts already stated in P1 or P2

DO:
- Use US-style apostrophes — straight ' not curly. The HTML will encode them.
- Reference Australian-specific institutions where relevant (Fair Trading NSW/QLD/VIC/WA/SA/TAS/NT, ABN, ACL, ACCC, Office of Fair Trading, Tourism Australia, etc.)
- Vary the opening across the 6 scams of one city — don't start every paragraph the same way
- Make the <strong> line a single concrete sentence the reader can do TODAY

Reference examples from cities already in canonical 3-para format:

EXAMPLE 1 (cairns scam-1):
"Outer-reef sites — Agincourt Ribbon Reefs, Moore Reef, Flynn Reef, Michaelmas Cay — are 75–90 minutes from Cairns by high-speed catamaran. Visibility is 15–20 meters, hard and soft coral cover is dense, and these are the locations that generate the underwater photos tourists expect. The $99 tour departs on a slower vessel to Green Island; the outer reef is visible in the distance but not visited. The 'all-inclusive' tag on the cheap tour excludes equipment rental and pontoon lunch that add $30–$50 per person on the day."
followed by:
"Asking the specific site name is the only filter that matters. <strong>Book directly with Passions of Paradise, Silverswift, Sunlover, Quicksilver, or Ocean Freedom and confirm the outer-reef destination site name before paying</strong> — outer-reef full days with lunch and snorkel gear start at $220; any tour priced below $160 operates to an inner-reef or half-day coastal site."

(The above is the current P3 — yours should be similar in structure.)

EXAMPLE 2 (cairns scam-2 — backpacker hostel):
"<strong>Never pay a deposit for a Cairns hostel or sharehouse before seeing the room in person and meeting the existing housemates</strong> — established Cairns backpacker hostels (Gilligan's, Tropic Days, Calypso, Travelers Oasis, Nomads) take payment at check-in or via HostelWorld and Booking.com with platform protection, and no legitimate sharehouse landlord requires bank-transfer prepayment before an in-person viewing."

EXAMPLE 3 (canberra scam-1):
"<strong>Use Uber or DiDi from the Canberra Airport rideshare bay where fares are app-displayed before pickup</strong> — typical CBD/Civic fare is $25-$32, and the Canberra Airport publishes a maximum taxi fare ($35-$45) on signage at the rank that the driver is legally required to honor.

Output a JSON object: {"paragraph": "<the full <p class='scam-story-body'>...</p> wrapper, with the paragraph text and the <strong>...</strong> close>"}.

The output must be the FULL paragraph wrapped in <p class="scam-story-body">...</p>. No commentary. No markdown.
"""


def _gemini_call(user_prompt: str, max_retries: int = 4) -> str:
    body = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.6,
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "object",
                "properties": {"paragraph": {"type": "string"}},
                "required": ["paragraph"],
            },
            "maxOutputTokens": 4096,
            "thinkingConfig": {"thinkingBudget": 1024},
        },
    }
    url = f"{GEMINI_ENDPOINT}?key={_gemini_key()}"
    last = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                url, method="POST",
                data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=90) as r:
                resp = json.loads(r.read())
            parts = resp["candidates"][0]["content"]["parts"]
            return "".join(p.get("text", "") for p in parts)
        except Exception as e:
            last = e
            time.sleep(3 + attempt * 3)
    raise RuntimeError(f"gemini call failed after {max_retries}: {last}")


def extract_scams(city: str) -> list[dict]:
    """Extract (n, title, location, tldr, p1, p2, n_paragraphs) per scam."""
    html = (SCAMS / city / "index.html").read_text()
    out = []
    cards = re.findall(
        r'<div class="scam-card"[^>]*id="scam-(\d+)"[^>]*>([\s\S]*?)(?=<div class="scam-card"|<div class="action-section"|<div class="mid-cta"|<!-- What to do -->)',
        html,
    )
    for sid, body in cards:
        title_m = re.search(r'<div class="scam-title">([^<]+)</div>', body)
        loc_m = re.search(r'<div class="scam-location">([^<]+)</div>', body)
        tldr_m = re.search(r'<p class="scam-tldr">([\s\S]*?)</p>', body)
        bodies = re.findall(r'<p class="scam-story-body">([\s\S]*?)</p>', body)
        if not title_m:
            continue
        out.append({
            "city": city,
            "n": int(sid),
            "title": unescape(title_m.group(1)).strip(),
            "location": unescape(loc_m.group(1).replace("📍", "")).strip() if loc_m else "",
            "tldr": unescape(re.sub(r"\s+", " ", tldr_m.group(1))).strip() if tldr_m else "",
            "paragraphs": [unescape(re.sub(r"\s+", " ", b)).strip() for b in bodies],
            "n_paragraphs": len(bodies),
        })
    return out


def build_user_prompt(scam: dict) -> str:
    p1 = scam["paragraphs"][0] if len(scam["paragraphs"]) > 0 else ""
    p2 = scam["paragraphs"][1] if len(scam["paragraphs"]) > 1 else ""
    return (
        f"CITY: {scam['city']}\n"
        f"SCAM TITLE: {scam['title']}\n"
        f"LOCATION: {scam['location']}\n"
        f"TLDR: {scam['tldr']}\n\n"
        f"PARAGRAPH 1 (already on the page):\n{p1}\n\n"
        f"PARAGRAPH 2 (already on the page):\n{p2}\n\n"
        f"Write paragraph 3 in the canonical NYC style. Output JSON: "
        f"{{\"paragraph\": \"<p class='scam-story-body'>...</p>\"}}"
    )


def main():
    drafts = []
    failed = []
    for city in CITIES:
        for scam in extract_scams(city):
            if scam["n_paragraphs"] >= 3:
                continue
            print(f"  {city}/{scam['n']} {scam['title'][:50]}...", flush=True)
            try:
                raw = _gemini_call(build_user_prompt(scam))
                parsed = json.loads(raw)
                p3 = parsed["paragraph"].strip()
                # Sanity: must contain <strong> and start with <p
                if "<strong>" not in p3 or not p3.startswith("<p"):
                    print(f"    SKIP: malformed output: {p3[:80]}", flush=True)
                    failed.append({"city": city, "n": scam["n"], "raw": raw[:200]})
                    continue
                drafts.append({
                    "city": city, "n": scam["n"],
                    "title": scam["title"], "p3": p3,
                })
                print(f"    OK ({len(p3)} chars)", flush=True)
            except Exception as e:
                print(f"    FAIL: {e}", flush=True)
                failed.append({"city": city, "n": scam["n"], "err": str(e)})
            time.sleep(1)  # avoid rate-limit

    out_path = Path("/tmp/au-p3-drafts.json")
    out_path.write_text(json.dumps({"drafts": drafts, "failed": failed}, indent=2))
    print(f"\n[summary] {len(drafts)} drafts written to {out_path}, {len(failed)} failed")


if __name__ == "__main__":
    main()
