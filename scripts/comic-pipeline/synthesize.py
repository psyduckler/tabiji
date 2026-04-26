#!/usr/bin/env python3
"""Per-scam prompt synthesizer using Gemini 2.5 Pro.

Given a scam card (title + location + first story paragraph), asks Gemini to:
1. Pick the right character from the 4-member cast based on scam-fit
2. Write a bespoke 4-panel script with scene descriptions + distinctive dialogue
3. Return JSON that can be assembled into a Nano Banana Pro prompt

This replaces the earlier keyword-classified themed-template approach, which
produced generic comics for multi-mechanic scams (e.g. "petition + bracelet
pickpocket" rendered as a generic U-Bahn pickpocket because "pickpocket" was
the first keyword to match).

Usage:
    from scripts.comic_pipeline.synthesize import synthesize_prompt
    prompt_body = synthesize_prompt(country="germany", scam={
        "title": "Fake S-Bahn Ticket Inspector Cash Fine Scam",
        "location": "S-Bahn platforms (Alexanderplatz...)",
        "story": "A fake inspector demands €60 cash on the spot...",
        "city": "berlin",
    })
    # prompt_body is ready to POST to Nano Banana Pro /edit

Env / creds:
    - gemini-api-key in macOS keychain
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from cast import CHARACTERS, PAIRING_HINTS  # noqa: E402
from styles import STYLES, PILOTS  # noqa: E402

GEMINI_MODEL = "gemini-2.5-pro"
GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
)


def _gemini_key() -> str:
    return subprocess.run(
        ["security", "find-generic-password", "-s", "gemini-api-key", "-w"],
        capture_output=True, text=True,
    ).stdout.strip()


SYSTEM_PROMPT = """You are a master comic-strip writer creating 4-panel cautionary scam illustrations for an international travel-safety book aimed at older (55+), slightly female-skewing readers. These will be printed. Quality matters.

Given one specific scam (title + location + mechanic description), output a JSON object with:
- "character": which protagonist best fits this specific scam
- "character_reason": one short sentence on why
- "panels": array of exactly 4 objects, each {"scene": "...", "dialogue": "..."}

CAST — choose ONE based on fit:

""" + "\n".join(f"- **{name}**: {hint}" for name, hint in PAIRING_HINTS.items()) + """

RULES:
- All dialogue in ENGLISH, under 8 words per bubble, distinctive to THIS specific scam (not generic travel-advice filler)
- It's fine to sprinkle ONE local flavour word if natural (e.g. "Grüß Gott!", "Dienstausweis please!", "Arigato!") but the sentence itself stays English
- Panel 1 = setup (protagonist arrives in location, scammer approaches or situation begins)
- Panel 2 = the scam mechanic happens (the specific bait, switch, distraction, or overcharge)
- Panel 3 = realization or pushback (protagonist notices, refuses, or discovers the loss)
- Panel 4 = lesson / aftermath (safer alternative, Tourist Police, official channel, or wry conclusion)
- Each scene: 1-2 sentences describing what we see — include a specific landmark, local signage, or cultural detail where it adds authenticity
- Panel 4 dialogue should be a memorable one-line lesson
- The comic must be recognizably ABOUT this specific scam — never a generic "pickpocket on transit" scene when the real mechanic is petition, bracelet, fake inspector, etc.

OUTPUT: valid JSON only, no prose before or after. Do NOT wrap in markdown fences."""


RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "character": {"type": "string", "enum": list(CHARACTERS.keys())},
        "character_reason": {"type": "string"},
        "panels": {
            "type": "array",
            "minItems": 4,
            "maxItems": 4,
            "items": {
                "type": "object",
                "properties": {
                    "scene": {"type": "string"},
                    "dialogue": {"type": "string"},
                },
                "required": ["scene", "dialogue"],
            },
        },
    },
    "required": ["character", "character_reason", "panels"],
}


def _gemini_call(user_prompt: str, max_retries: int = 4) -> str:
    """Call Gemini and return the raw text response."""
    body = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.85,
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
            # Pro 2.5 spends reasoning tokens; need generous budget
            "maxOutputTokens": 8192,
            "thinkingConfig": {"thinkingBudget": 2048},
        },
    }
    url = f"{GEMINI_ENDPOINT}?key={_gemini_key()}"
    req = urllib.request.Request(
        url, method="POST",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    last_err = None
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                resp = json.loads(r.read())
            parts = resp["candidates"][0]["content"]["parts"]
            return "".join(p.get("text", "") for p in parts)
        except Exception as e:
            last_err = e
            import time
            time.sleep(2 + attempt * 2)
    raise RuntimeError(f"Gemini call failed after {max_retries} attempts: {last_err}")


def synthesize_scene(country: str, scam: dict) -> dict:
    """Generate a per-scam scene dict. Returns {'character': ..., 'panels': [...]}."""
    user_prompt = f"""COUNTRY: {country}
CITY: {scam.get('city', '')}
SCAM TITLE: {scam['title']}
LOCATION: {scam.get('location', '')}
MECHANIC (first paragraph of the scam story):
{scam.get('story', '')[:1500]}

Synthesize the JSON now."""
    raw = _gemini_call(user_prompt)
    # Gemini sometimes still wraps in markdown; strip defensively
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
    data = json.loads(raw)
    # Validate shape
    assert data["character"] in CHARACTERS, f"invalid character: {data['character']}"
    assert len(data["panels"]) == 4, f"need 4 panels, got {len(data['panels'])}"
    for p in data["panels"]:
        assert "scene" in p and "dialogue" in p, f"panel missing scene/dialogue: {p}"
    return data


def build_full_prompt(country: str, scene: dict) -> str:
    """Assemble the final Nano Banana Pro prompt from a synthesized scene.

    Falls back to the "_default" STYLE block when the country has no specific lock
    (or its entry is an empty placeholder). See styles/_default.md for the rationale.
    """
    style = STYLES.get(country, "").strip() or STYLES["_default"].strip()
    char = CHARACTERS[scene["character"]]
    panels_text = "\n".join(
        f"Panel {i+1}: {p['scene']} Speech bubble: \"{p['dialogue']}\""
        for i, p in enumerate(scene["panels"])
    )
    # Add the edit-endpoint anchor instruction when using a reference image
    style_anchor = (
        " Match the style palette, linework, and lettering of the reference image exactly; "
        "the protagonist must be the NEW character described in CHARACTER below."
    )
    return f"{style}{style_anchor}\n\nCHARACTER: {char}\n\nSCENE:\n{panels_text}"


def synthesize_prompt(country: str, scam: dict) -> dict:
    """Full flow: synthesize scene → assemble Nano Banana Pro body.

    Returns dict ready to POST to /edit:
        {"prompt": "...", "images": [...], "aspect_ratio": "1:1", "output_format": "jpeg"}
    Also includes the synthesized scene under "_scene" for logging / audit.
    """
    scene = synthesize_scene(country, scam)
    prompt_text = build_full_prompt(country, scene)
    pilot = PILOTS.get(country) or PILOTS["_default"]
    return {
        "prompt": prompt_text,
        "images": [pilot],
        "aspect_ratio": "1:1",
        "output_format": "jpeg",
        "_scene": scene,
        "_character": scene["character"],
    }


if __name__ == "__main__":
    # Smoke test against a real German scam
    sample = {
        "city": "berlin",
        "title": "Fake S-Bahn / U-Bahn Ticket Inspector Cash Fine Scam",
        "location": "S-Bahn platforms (Alexanderplatz, Friedrichstraße, Hauptbahnhof)",
        "story": (
            "Individuals in plain clothes or fake uniforms claim to be ticket inspectors "
            "(Fahrscheinkontrolleure) after checking your ticket; they assert your ticket "
            "is 'invalid' (wrong zone, wrong validation, wrong date) and demand a €60 "
            "'on-the-spot fine' in cash. Real BVG/S-Bahn inspectors work in teams of 2–3, "
            "always with a photo ID badge (Dienstausweis) clearly displayed, and the "
            "official fine is paid with a printed receipt OR within 2 weeks via bank "
            "transfer to the BVG address on the printed ticket."
        ),
    }
    out = synthesize_prompt("germany", sample)
    print("CHARACTER:", out["_character"])
    print("PROMPT PREVIEW:")
    print(out["prompt"][:1500])
    print("...")
