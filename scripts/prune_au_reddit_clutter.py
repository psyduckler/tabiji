#!/usr/bin/env python3
"""Prune Reddit clutter from 8 AU city pages to match NYC baseline (3-4 r/
mentions across 6 scams, never as a paragraph opener, no long verbatim quotes).

Strategy: per scam-card with 3+ subreddit citations OR a verbatim quote >25
words, send the full story-body to Gemini and ask for a rewrite that:
  - Keeps AT MOST one r/ citation per scam (in P3, the citation paragraph)
  - Replaces "r/X threads document..." paragraph openers with story or fact
  - Paraphrases verbatim quotes longer than ~20 words
  - Preserves all concrete facts, dollar amounts, names of operators/agencies
  - Preserves the closing <strong> defensive line

Outputs /tmp/au-reddit-drafts.json for review.
"""
from __future__ import annotations
import json, re, subprocess, sys, time, urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAMS = ROOT / "scams"

# Cities with heavy clutter (10+ real r/ mentions per audit)
HEAVY_CITIES = ["darwin","gold-coast","hobart","melbourne","perth",
                "port-douglas","sydney","whitsundays"]

GEMINI_MODEL = "gemini-2.5-pro"
GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
)


def _gemini_key() -> str:
    return subprocess.run(
        ["security", "find-generic-password", "-s", "gemini-api-key", "-w"],
        capture_output=True, text=True,
    ).stdout.strip()


SYSTEM_PROMPT = """You are editing tourist-scam page story bodies to match the New York City canonical voice (https://tabiji.ai/scams/new-york-city/). The current 3-paragraph story body leans too heavily on Reddit citations — opens paragraphs with "r/X threads document..." or stacks multiple subreddit references. Your job: rewrite the same factual content with at most ONE r/ citation total, used naturally as a parenthetical, never as the paragraph opener.

NYC pattern (the standard you're matching):
- 6 scams across 1 page mention r/AskNYC and r/nyc 3-4 times TOTAL — once or twice per page in passing.
- The citation appears mid-paragraph as evidence: "r/AskNYC and r/nyc threads document the same play running daily on 42nd Street...".
- Direct verbatim quotes are <15 words. Longer ones are paraphrased.
- Paragraph 1 opens with the scene/bait. Paragraph 2 closes the trap. Paragraph 3 broadens to the pattern + ends with bold defensive line.

Constraints for your rewrite:
- Keep ALL: dollar amounts, location names, operator names, regulator names, specific data points, year references, the bold <strong>...</strong> defensive line at the end.
- Keep the SAME 3-paragraph structure (P1=scene, P2=trap closes, P3=broader pattern + strong-close).
- Allow at most ONE r/<subreddit> reference total in the rewrite. Lead with a fact or scene, never a subreddit name.
- Paraphrase any verbatim quote longer than ~20 words. Verbatim quotes <15 words are fine if attributed (a r/sydney commenter wrote, "...").
- US English: defense, color, behavior, organize, meters.
- Use straight apostrophes (HTML encodes). Use em-dashes — like this — with spaces.
- Don't write new facts. Don't drop facts. Pure tone/cite rebalancing.

Output JSON: {"p1": "<paragraph 1 inner text, no <p> wrapper>", "p2": "<p2 inner>", "p3": "<p3 inner WITH the closing <strong>...</strong> intact>"}.
"""


def _gemini_call(user_prompt: str, max_retries: int = 4) -> str:
    body = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.55,
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "object",
                "properties": {
                    "p1": {"type": "string"},
                    "p2": {"type": "string"},
                    "p3": {"type": "string"},
                },
                "required": ["p1", "p2", "p3"],
            },
            "maxOutputTokens": 6144,
            "thinkingConfig": {"thinkingBudget": 1536},
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
            with urllib.request.urlopen(req, timeout=120) as r:
                resp = json.loads(r.read())
            parts = resp["candidates"][0]["content"]["parts"]
            return "".join(p.get("text", "") for p in parts)
        except Exception as e:
            last = e
            time.sleep(3 + attempt * 3)
    raise RuntimeError(f"gemini call failed: {last}")


def find_targets() -> list[dict]:
    """For the 8 heavy cities, find scams with 2+ r/ mentions OR a long quote."""
    targets = []
    for c in HEAVY_CITIES:
        h = (SCAMS / c / "index.html").read_text()
        for m in re.finditer(
            r'<div class="scam-card"[^>]*id="scam-(\d+)"[\s\S]*?(?=<div class="scam-card"|<div class="action-section"|<div class="mid-cta"|<!-- What to do -->)',
            h,
        ):
            sid = int(m.group(1))
            card = m.group(0)
            title_m = re.search(r'<div class="scam-title">([^<]+)</div>', card)
            loc_m = re.search(r'<div class="scam-location">([^<]+)</div>', card)
            tldr_m = re.search(r'<p class="scam-tldr">([\s\S]*?)</p>', card)
            bodies = re.findall(r'<p class="scam-story-body">([\s\S]*?)</p>', card)
            if len(bodies) < 3 or not title_m:
                continue
            full_body = " ".join(bodies)
            text = re.sub(r'<[^>]+>', ' ', unescape(full_body))
            r_count = len(re.findall(r'r/[a-zA-Z][a-zA-Z0-9_]+', text))
            # Detect long quotes — anything in single-quotes >20 words
            quote_lens = [len(q.split()) for q in re.findall(r"'([^']{30,400})'", text) if len(q.split()) > 18]
            has_long_quote = any(quote_lens)
            if r_count >= 2 or has_long_quote:
                targets.append({
                    "city": c, "n": sid,
                    "title": unescape(title_m.group(1)).strip(),
                    "location": unescape(loc_m.group(1).replace("📍", "")).strip() if loc_m else "",
                    "tldr": unescape(re.sub(r'\s+', ' ', tldr_m.group(1))).strip() if tldr_m else "",
                    "p1": unescape(re.sub(r'\s+', ' ', bodies[0])).strip(),
                    "p2": unescape(re.sub(r'\s+', ' ', bodies[1])).strip(),
                    "p3": unescape(re.sub(r'\s+', ' ', bodies[2])).strip(),
                    "r_count": r_count,
                    "long_quotes": quote_lens,
                })
    return targets


def main():
    targets = find_targets()
    print(f"Found {len(targets)} scams needing rewrite")
    drafts, failed = [], []
    for t in targets:
        prompt = (
            f"CITY: {t['city']}\n"
            f"SCAM TITLE: {t['title']}\n"
            f"LOCATION: {t['location']}\n"
            f"TLDR: {t['tldr']}\n\n"
            f"PARAGRAPH 1 (current):\n{t['p1']}\n\n"
            f"PARAGRAPH 2 (current):\n{t['p2']}\n\n"
            f"PARAGRAPH 3 (current):\n{t['p3']}\n\n"
            f"Current r/ count: {t['r_count']}. Long-quote word counts: {t['long_quotes']}.\n"
            f"Rewrite to NYC canonical voice. Output JSON with p1, p2, p3."
        )
        try:
            raw = _gemini_call(prompt)
            parsed = json.loads(raw)
            p1 = parsed["p1"].strip()
            p2 = parsed["p2"].strip()
            p3 = parsed["p3"].strip()
            # Sanity: must keep <strong> in p3
            if "<strong>" not in p3:
                print(f"  SKIP {t['city']}-{t['n']}: lost <strong> close")
                failed.append({**t, "err": "missing strong close"})
                continue
            drafts.append({**t, "p1_new": p1, "p2_new": p2, "p3_new": p3})
            new_text = " ".join([p1, p2, p3])
            new_r = len(re.findall(r'r/[a-zA-Z][a-zA-Z0-9_]+', new_text))
            print(f"  {t['city']}-{t['n']}: r/ {t['r_count']} → {new_r}")
        except Exception as e:
            print(f"  FAIL {t['city']}-{t['n']}: {e}")
            failed.append({**t, "err": str(e)})
        time.sleep(0.8)
    out = Path("/tmp/au-reddit-drafts.json")
    out.write_text(json.dumps({"drafts": drafts, "failed": failed}, indent=2))
    print(f"\n[summary] {len(drafts)} drafts, {len(failed)} failed → {out}")


if __name__ == "__main__":
    main()
