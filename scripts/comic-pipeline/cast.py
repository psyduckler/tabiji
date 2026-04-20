"""Canonical cast of four protagonists for scam comics.

Paste the CHARACTERS[<name>] string VERBATIM into the `CHARACTER:` section of every Nano Banana Pro prompt. Do not paraphrase — the locked wording is what keeps the same person rendering across panels and countries.
"""

CHARACTERS = {
    "margie": (
        "A 62-year-old Western woman with shoulder-length silver-gray hair worn under a "
        "woven straw sun hat with a cream ribbon, warm blue eyes behind tortoiseshell reading "
        "glasses often perched on her head, light olive complexion with gentle laugh lines and "
        "a friendly curious expression. She wears a cream linen blouse, tan wide-leg travel "
        "pants, and white canvas sneakers, with a small tan leather crossbody bag and a coral "
        "scarf. Gracious, cheerful, a little too trusting."
    ),
    "priya": (
        "A 34-year-old South Asian woman with long dark wavy hair pulled into a low ponytail "
        "under a wide-brim navy sun hat, warm brown eyes, clear brown skin, athletic build and "
        "confident posture. She wears olive utility shorts and a terracotta cotton t-shirt, "
        "white running sneakers, and carries a charcoal compact hiking backpack with a "
        "reusable water bottle clipped to the side. Sunglasses pushed up on her head. "
        "Capable, lightly skeptical, a prepared traveler."
    ),
    "harry": (
        "A 64-year-old Western man with close-cropped silver-white hair and a neatly-trimmed "
        "salt-and-pepper beard, warm hazel eyes with kind wrinkles, light tan complexion. He "
        "wears a pale-blue short-sleeve button-down, beige chinos, brown leather loafers, and "
        "a soft navy baseball cap, with a small brown leather sling bag and a simple silver "
        "watch. Affable, chatty, easily charmed."
    ),
    "marcus": (
        "A 34-year-old man of mixed heritage with short dark-brown hair and light stubble, "
        "warm medium-brown skin, athletic build. He wears an olive-green polo shirt, dark "
        "khaki slim travel trousers, and brown trail sneakers, with a black sling bag and a "
        "DSLR camera on a woven strap around his neck, sunglasses hooked at his collar. "
        "Observant, curious, slightly guarded but warm."
    ),
}

# Short pairing hints passed to the synthesizer LLM so it picks the right character
PAIRING_HINTS = {
    "margie": (
        "Best for: warm/trust-based scams, friendly-stranger cons, restaurant/market "
        "overcharge, rose sellers, fortune-tellers, fake charity, fake monk/temple donation, "
        "counterfeit merchandise, anything that plays on politeness or gentle manipulation. "
        "Margie is the archetypal easy mark for emotional-appeal scams."
    ),
    "priya": (
        "Best for: transit/taxi/airport/rental/scooter/jet-ski/boat scams, accommodation "
        "fraud, fake QR parking, fake Uber/Grab/Didi, overbooking, anything where a prepared "
        "traveler pushes back, compares prices on her phone, or demands an official channel."
    ),
    "harry": (
        "Best for: authority-impersonation (fake police, fake ticket inspector, fake border "
        "guard), ATM distraction, currency-exchange short-change, tailor/suit shops, verbal "
        "chat-up openers, lucky-face/compliment cons, wine-tasting pressure, anything where "
        "a chatty older gentleman gets verbally charmed."
    ),
    "marcus": (
        "Best for: nightlife (strip clubs, go-go bars, menu-switch bills), shell game / "
        "three-card monte / street gambling, beach theft, photo-with-costume, adventure-sport "
        "rentals (ATV/jet-ski/dive), phone-snatch, fake festival credentials, anything young "
        "+ active + camera-in-hand."
    ),
}
