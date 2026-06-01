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
    """Read Gemini API key from macOS keychain, with GEMINI_API_KEY env-var fallback.

    The cron sandbox is Linux and has no `security` CLI; without the env-var
    fallback, callers get an empty string and the upstream Gemini call returns
    a 401 with no signal that credentials were the problem.
    """
    import os, shutil
    if shutil.which("security"):
        try:
            out = subprocess.run(
                ["security", "find-generic-password", "-s", "gemini-api-key", "-w"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            if out:
                return out
        except subprocess.CalledProcessError:
            pass
    val = os.environ.get("GEMINI_API_KEY", "").strip()
    if not val:
        raise RuntimeError(
            "missing Gemini key: not in macOS keychain and $GEMINI_API_KEY is unset"
        )
    return val


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


_OVERUSED_TEMPLATES = """
ANTI-TEMPLATE DIRECTIVE — these 5 layouts are saturated across this country's series; if your scam fits one of these patterns, find a DIFFERENT visual angle:

1. AIRPORT-TAXI-TOUT — protagonist arriving with luggage at arrivals door + man in branded vest with clipboard offering inflated USD price + protagonist showing phone app with lower price + final panel inside a taxi/rideshare. Avoid this layout. Better angles: actual taxi mafia blockading a rideshare car, drivers throwing stones at an Uber, dual-pricing reveal where local pays one rate and tourist gets quoted another at the same counter, license plate photographed against app screenshot, the airport's specific landmark in the window.

2. BOOKING-PHISHING — protagonist at laptop with confirmation page + WhatsApp/email demanding wire deposit + reveal that the URL or sender is fake + final panel showing official platform. Avoid this layout. Better angles: typo-squat domain comparison side-by-side, scammer voice-message playback, hotel-extranet compromise visualization, deposit going to wrong bank, the property's actual building photographed at arrival vs the photo-stolen listing.

3. RESTAURANT-ENGLISH-MENU — waiter handing English menu + reveal Spanish menu has lower prices + bill with cubierto question + "always ask for the local menu" lesson. Avoid this layout. Better angles: surprise unrequested aperitivo or bread arriving, "servicio incluido" line being argued at the table, the OWNER coming out to dispute, photographing the menu before sitting down, walking out before the order, the chef's specials being upsold without prices.

4. CAMBIO-TOUT — older protagonist on pedestrian street + tout offering rate on a calculator + fake bill check + Western Union resolution. Avoid this layout. Better angles: rate quoted in writing on a piece of paper, the cueva interior with a metal grille, watermark-against-light on the sidewalk, mid-transaction switch where bills get rotated in the scammer's hand, MEP credit-card reveal at point of sale.

5. TOUR-BUNDLE-MARKUP — concierge with glossy brochure + protagonist checking phone showing direct rate + "always book direct" lesson. Avoid this layout. Better angles: the actual tour bus showing up vs what was promised, subcontractor swap mid-tour, helicopter that never arrives, brochure photographed next to a phone showing operator website, the operator's printed price-list at the kiosk vs the agency's marked-up version.

The above are FORBIDDEN starting points. If the scam title clearly matches one of these categories, your job is to compose a 4-panel sequence that depicts the SAME scam mechanic with a DIFFERENT visual layout — different camera angle, different beat sequencing, different specific details. Use the city's unique geography, signage, and architecture aggressively.
"""


def synthesize_scene(country: str, scam: dict) -> dict:
    """Generate a per-scam scene dict. Returns {'character': ..., 'panels': [...]}."""
    user_prompt = f"""COUNTRY: {country}
CITY: {scam.get('city', '')}
SCAM TITLE: {scam['title']}
LOCATION: {scam.get('location', '')}
MECHANIC (first paragraph of the scam story):
{scam.get('story', '')[:1500]}
{_OVERUSED_TEMPLATES if country == "argentina" else ""}
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
    # Hard text-rendering contract. Nano Banana Pro will otherwise letter the
    # art-direction itself INTO the image — character bios ("SOUTH ASIAN WOMAN,
    # 34"), scene/location descriptions as caption bands, even style-reference
    # names ("Jack Kirby") — which was the single biggest book-readiness defect.
    # The CHARACTER/SCENE blocks below are drawing instructions, NOT copy to set.
    text_contract = (
        "\n\nTEXT IN THE IMAGE — STRICT RULES. The CHARACTER and SCENE sections below are "
        "ART DIRECTION describing what to DRAW; they are NOT text to write into the picture. "
        "The ONLY text permitted anywhere in the image is: (1) the exact words inside each "
        "panel's speech balloon, quoted below; (2) at most one short comic sound-effect "
        "(KAPOW!, NO!) where it fits; (3) brief, naturalistic in-world signage that genuinely "
        "belongs in the scene. Letter every bit of that text in real, correctly-spelled "
        "English — never invented, garbled, doubled, or nonsense letters; keep signage short. "
        "Do NOT draw narration boxes, caption bands, title banners, location labels, or "
        "character labels. Never write a character's name, age, ethnicity, gender, or physical "
        "description, the word 'Panel', any panel/scene direction, or any artist or art-style "
        "reference (e.g. 'Kirby', 'Ditko') as visible text. When in doubt, leave text out. "
        "MINIMIZE in-image text — it is the most common failure. On receipts, bills, menus, "
        "phone screens, tickets and background signs, letter ONLY the one or two items the scam "
        "hinges on (a single price, a short domain) in large clear type, and draw every other "
        "line as a plain horizontal rule or blank surface — never fine print, never multi-line "
        "word lists. Every number must be a concrete value, never a placeholder ('X', '$3X.00', "
        "'HUGE PRICE', '[name]'). Never duplicate or repeat a word, line, or speech balloon, and "
        "do not add time-transition captions like 'Later' or 'Hours later'."
    )
    # Intellectual-property contract — keeps real trademarks/characters out of a
    # commercial print product (the Disney castle + Goofy, Warner Bros, Gucci,
    # Uber, Airbnb etc. flagged in the audit).
    ip_contract = (
        "\n\nINTELLECTUAL PROPERTY (this overrides scene realism). Even when the scam centers on "
        "a specific real brand, app, character, venue, or landmark, you MUST draw a clearly "
        "generic, invented stand-in — never the real mark. No copyrighted characters or mascots "
        "(no Mickey Mouse or other Disney/Universal characters); no real app logos, icons, or "
        "brand colors (no Cash App, Venmo, Zelle, Uber, Lyft, Facebook/Messenger, Airbnb); no "
        "real financial marks (no Visa, Mastercard, Bank of America); no trademarked architecture "
        "or landmarks (no Disney castle, no Hollywood Sign lettering, no Caesars Palace or "
        "Venetian facade); no third-party reseller brands (no Viator, Ticketmaster, Tripadvisor). "
        "Use a plain unbranded payment app, a generic bank card, a nondescript castle or hillside, "
        "an unbranded booking site. Naming a real venue ONCE in plain text is acceptable; drawing "
        "its logo, mascot, or signature architecture is not."
    )
    return (
        f"{style}{style_anchor}{text_contract}{ip_contract}"
        f"\n\nCHARACTER (draw this person; do NOT write any of this as text): {char}"
        f"\n\nSCENE (draw these four panels; the only words to letter are the quoted "
        f"speech-balloon lines):\n{panels_text}"
    )


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
        # Force 2K on the /edit pass too. submit_nbp only set "2k" on the
        # /text-to-image retry, so first-pass /edit renders defaulted to 1024px —
        # the source of the 83 half-resolution masters the audit found.
        "resolution": "2k",
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
