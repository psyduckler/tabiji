#!/usr/bin/env python3
"""Compress 27 bloated AU scam-card TLDRs (>55 words) to NYC canonical
length (~33-45 words) using Gemini 2.5 Pro.

NYC TLDR pattern:
- One sentence, ~30-50 words
- Opens with the setup ("A X at Y does Z...")
- Ends with the financial hit (concrete $ amount)
- No backstory padding, no explanatory clauses

Outputs /tmp/au-tldr-drafts.json for review.
"""
from __future__ import annotations
import json, re, subprocess, sys, time, urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAMS = ROOT / "scams"

GEMINI_MODEL = "gemini-2.5-pro"
GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
)


def _gemini_key() -> str:
    return subprocess.run(
        ["security", "find-generic-password", "-s", "gemini-api-key", "-w"],
        capture_output=True, text=True,
    ).stdout.strip()


SYSTEM_PROMPT = """You are condensing scam-page TLDRs to match the New York City canonical at https://tabiji.ai/scams/new-york-city/. The current TLDR is bloated (60-91 words). Your job: write a tighter version of 33-50 words that preserves the hook + the financial hit.

NYC TLDR examples (target style):
1. "A man on 42nd Street presses a CD into your hand saying it's a free mixtape, then circles back demanding $20–$50 with two or three of his crew blocking your exit. The CD itself is worthless — you're paying to walk away." (45 words)

2. "A man in a fake-official vest in Battery Park tells you the Statue of Liberty is "sold out online" but he has $60 tickets that include the crown — you board the boat and it's a generic harbor cruise that never docks on the island." (45 words)

3. "A pedicab driver at Central Park's 59th Street entrance offers a "quick ride" with a smile but no price, then hands you a $180 bill ten minutes later — refuse and he blocks the sidewalk until you pay." (38 words)

Rules:
- 33-50 words total. Hard cap 50.
- Concrete: keep dollar amounts, location names, the specific mechanic.
- Drop: jet-lag tropes ("you've just landed after a 14-hour flight"), backstory hypotheticals ("you've dreamed about X your whole life"), narrator second-person speculation ("you don't know yet that..."), repetition of details that appear elsewhere on the page.
- Use straight apostrophes (HTML will encode).
- One or two sentences max.
- US English (defense, color, behavior, organize, meters).
- Don't start with "Imagine you" or "You've just".
- Keep the same landmark + dollar specifics that appear in the original.

Output JSON: {"tldr": "<the new TLDR text, NO surrounding <p> tags>"}.
"""


def _gemini_call(user_prompt: str, max_retries: int = 4) -> str:
    body = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.5,
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "object",
                "properties": {"tldr": {"type": "string"}},
                "required": ["tldr"],
            },
            "maxOutputTokens": 2048,
            "thinkingConfig": {"thinkingBudget": 512},
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
    raise RuntimeError(f"gemini call failed: {last}")


def find_bloated() -> list[dict]:
    """Find all scams with TLDR >55 words across the 14 AU cities."""
    out = []
    cities = ["adelaide","alice-springs","brisbane","byron-bay","cairns","canberra",
              "darwin","gold-coast","hobart","melbourne","perth","port-douglas",
              "sydney","whitsundays"]
    for c in cities:
        h = (SCAMS / c / "index.html").read_text()
        for m in re.finditer(
            r'<div class="scam-card"[^>]*id="scam-(\d+)"[\s\S]*?(?=<div class="scam-card"|<div class="action-section"|<div class="mid-cta"|<!-- What to do -->)',
            h,
        ):
            sid = int(m.group(1))
            body = m.group(0)
            tldr_m = re.search(r'<p class="scam-tldr">([\s\S]*?)</p>', body)
            title_m = re.search(r'<div class="scam-title">([^<]+)</div>', body)
            loc_m = re.search(r'<div class="scam-location">([^<]+)</div>', body)
            if not tldr_m or not title_m:
                continue
            tldr_text = re.sub(r'\s+', ' ', unescape(tldr_m.group(1))).strip()
            tldr_clean = re.sub(r'<[^>]+>', '', tldr_text)
            wc = len(tldr_clean.split())
            if wc > 55:
                out.append({
                    "city": c, "n": sid,
                    "title": unescape(title_m.group(1)).strip(),
                    "location": unescape(loc_m.group(1).replace("📍", "")).strip() if loc_m else "",
                    "tldr_orig": tldr_clean,
                    "wc_orig": wc,
                })
    return out


def main():
    targets = find_bloated()
    print(f"Found {len(targets)} bloated TLDRs")
    drafts = []
    failed = []
    for t in targets:
        prompt = (
            f"CITY: {t['city']}\n"
            f"SCAM TITLE: {t['title']}\n"
            f"LOCATION: {t['location']}\n"
            f"CURRENT TLDR ({t['wc_orig']} words):\n{t['tldr_orig']}\n\n"
            f"Compress to 33-50 words. Output JSON: {{\"tldr\": \"...\"}}"
        )
        try:
            raw = _gemini_call(prompt)
            parsed = json.loads(raw)
            new = parsed["tldr"].strip()
            new_wc = len(new.split())
            print(f"  {t['city']}-{t['n']}: {t['wc_orig']}w → {new_wc}w")
            drafts.append({**t, "tldr_new": new, "wc_new": new_wc})
        except Exception as e:
            print(f"  FAIL {t['city']}-{t['n']}: {e}")
            failed.append({**t, "err": str(e)})
        time.sleep(0.6)

    out = Path("/tmp/au-tldr-drafts.json")
    out.write_text(json.dumps({"drafts": drafts, "failed": failed}, indent=2))
    print(f"\n[summary] {len(drafts)} drafts, {len(failed)} failed → {out}")


if __name__ == "__main__":
    main()
