#!/usr/bin/env python3
"""Build compare-data/greece-vs-turkey.json from scratch."""
import json
from pathlib import Path

# Load shell from reference page
ref_path = Path('/Users/psy/.openclaw/workspace/tabiji/compare-data/greece-vs-croatia.json')
with open(ref_path) as f:
    ref = json.load(f)
shell = ref['shell']

SLUG = "greece-vs-turkey"
D1 = "Greece"
D2 = "Turkey"
DATE = "2026-03-18"
DATE_ISO = "2026-03-18T00:00:00Z"
OG_IMAGE = "https://img.tabiji.ai/compare/greece-vs-turkey/greece_santorini.jpg"
CANONICAL = "https://tabiji.ai/compare/greece-vs-turkey/"

# --- FAQ items ---
faq_items = [
    {
        "question": "Is Greece or Turkey better for first-time visitors?",
        "answer": "It depends on what you want. Greece is easier: English is widely spoken in tourist areas, it's EU territory (familiar for Western travelers), and the Greek Islands deliver instant iconic beauty. Turkey rewards deeper exploration — Istanbul alone justifies the trip, and Cappadocia is genuinely one of the world's most surreal landscapes. Reddit consensus: if your priority is islands and beaches, Greece. If you want more variety and extraordinary value for money, Turkey. Both are safe for tourists and can be done in 10–14 days."
    },
    {
        "question": "Is Turkey cheaper than Greece to visit?",
        "answer": "Yes — significantly. Turkey's lira depreciation has made it exceptional value for USD/EUR travelers. A mid-range day in Istanbul or Cappadocia runs $45–65 (meals, accommodation, transport). A mid-range day in Athens or the Greek islands runs €70–100+, with Santorini and Mykonos pushing €120–180/day easily. On a 10-day trip, Turkey can be 30–50% cheaper than the equivalent Greek itinerary, especially for accommodation."
    },
    {
        "question": "Which has better ancient ruins — Greece or Turkey?",
        "answer": "This is surprisingly Turkey's strongest suit. Ephesus outside Izmir is larger and better-preserved than most Greek ruins. Add Troy, Pergamon, Hierapolis at Pamukkale, and the ancient sites of Cappadocia — and Turkey has extraordinary depth. Greece has the Acropolis (the most iconic single monument), Delphi, and Olympia, but they're more crowded and ticketing is increasingly expensive. History buffs who've done Athens should do Turkey next."
    },
    {
        "question": "Which country has better beaches, Greece or Turkey?",
        "answer": "Greece wins on beaches, especially the sandy ones. The Ionian Islands (Lefkada, Kefalonia, Zakynthos) and Aegean islands (Naxos, Milos, Crete) deliver turquoise water over fine sand. Turkey's Mediterranean coast (Bodrum, Fethiye, Antalya) is beautiful but predominantly pebbly — great for swimming, less ideal for the classic sand-and-lounge experience. If beaches are your #1 priority, Greece is the clear choice."
    },
    {
        "question": "When is the best time to visit Greece and Turkey?",
        "answer": "April–May and September–October are ideal for both countries: warm but not brutally hot, crowds manageable, accommodation cheaper. July–August is peak season for Greece's islands (expensive, crowded, 35–40°C) and Turkey's coasts. For Istanbul specifically, spring and fall are perfect. Cappadocia is spectacular in winter — cold and snowy but surreal, with fewer tourists and dramatic balloon photos over snow-dusted valleys."
    },
    {
        "question": "Is Turkey safe for tourists?",
        "answer": "The main tourist areas of Turkey — Istanbul, Cappadocia, Bodrum, Antalya, Ephesus — are safe for travelers. The US and UK governments maintain general advisories for Turkey (primarily concerning the border regions with Syria/Iraq, which tourists don't visit). Standard precautions apply. Greece has no meaningful safety concerns for tourists. Both countries are regularly visited by millions of Western tourists without incident."
    },
    {
        "question": "Can I visit both Greece and Turkey in one trip?",
        "answer": "Absolutely — and it's one of the best combos in the Eastern Mediterranean. Flying Athens→Istanbul takes about 1.5 hours (Turkish Airlines and Aegean Airlines both serve the route from ~€50–120). Some travelers also do a ferry from Rhodes to Marmaris or from Chios to Cesme (summer only). A classic 2-week combo: 4 nights Athens + day trip to Santorini or another island (3 nights), then fly to Istanbul (3 nights) + Cappadocia (2 nights). Reddit considers this a top-tier circuit."
    },
    {
        "question": "Which has better food — Greece or Turkey?",
        "answer": "Turkey's food culture is more complex and diverse. The Turkish breakfast spread (simit, olives, white cheese, eggs, jams, fresh bread) is genuinely world-class. Kebabs, meze, baklava, börek, and fresh-caught fish along the coast — Turkey has enormous regional variety. Greek food is delicious but narrower: taverna staples of moussaka, souvlaki, grilled octopus, and incredible olive oil. Reddit leans Turkey for sheer variety and value; Greece wins on fresh seafood on the islands. Either way, you eat well."
    }
]

faq_schema_items = [
    {
        "@type": "Question",
        "name": q["question"],
        "acceptedAnswer": {
            "@type": "Answer",
            "text": q["answer"]
        }
    }
    for q in faq_items
]

# --- Build FAQ HTML ---
faq_html_items = ""
for q in faq_items:
    faq_html_items += f"""<div class="faq-item">
<h3>{q['question']}</h3>
<p>{q['answer']}</p>
</div>\n"""

faq_html = f"""<section class="faq-section">
<h2 id="frequently-asked-questions">❓ Frequently Asked Questions</h2>
{faq_html_items}</section>"""

# --- Deep Dive Sections ---
deep_dives = [
    # 1. Beaches
    """<section class="deep-dive">
<h2 id="beaches">🏖️ Beaches</h2>
<img src="https://img.tabiji.ai/compare/greece-vs-turkey/greece_santorini.jpg" alt="Santorini, Greece — iconic whitewashed buildings above turquoise Aegean waters" class="section-img" loading="lazy">
<p>This is the category where Greece dominates without argument. The Greek islands — Naxos, Milos, Elafonisi (Crete), Myrtos (Kefalonia), Porto Katsiki (Lefkada), Navagio (Zakynthos) — deliver the sandy, turquoise-water beach experience that Greece's entire tourism image is built on. The water is warm from June through October, the sand is fine, and visibility underwater is exceptional.</p>
<p>Turkey's coastline — the Aegean and Mediterranean shores of Bodrum, Antalya, Fethiye, and Ölüdeniz — is absolutely beautiful but predominantly pebbled. Ölüdeniz's famous Blue Lagoon is shallow and photogenic but small. Cleopatra Beach near Alanya is an exception with fine golden sand. Turkish gullets (wooden sailing boats) cruise turquoise bays that are as stunning as anything in Greece — but the shoreline itself is mostly rock and pebble.</p>
<blockquote class="reddit-quote">
"Turkey and Greece are very similar but I'd say Greece is nicer. The islands have more to offer and are just generally more put together (and arguably the food is better on the islands too)."
<span class="source">— r/travel</span>
</blockquote>
<div class="tabiji-verdict">
<strong>⚑ tabiji verdict:</strong> Greece wins beaches, and it's not close. Sandy shores, warm clear water, iconic island settings — if the beach is why you're going, Greece is the answer. Turkey's coast is beautiful but built more for gullet cruising than lounging on sand.
</div>
</section>""",

    # 2. Ancient Ruins & History
    """<section class="deep-dive">
<h2 id="ruins-history">🏛️ Ancient Ruins &amp; History</h2>
<img src="https://img.tabiji.ai/compare/greece-vs-turkey/greece_acropolis.jpg" alt="The Parthenon atop the Acropolis of Athens, Greece's most iconic ancient monument" class="section-img" loading="lazy">
<p>The Acropolis is the most recognizable ancient monument on earth and worth every tourist euro. But once you've done Athens — and especially if you're a serious history traveler — Turkey's archaeological depth is extraordinary and frequently surprising.</p>
<p>Ephesus (near Kusadasi/Selcuk) is jaw-dropping: a massive, well-preserved Roman city with marble-paved streets, a 25,000-seat theater, the Celsus Library, and far fewer crowds than the Acropolis in July. Turkey also has Troy (yes, <em>that</em> Troy) near Çanakkale, Pergamon with its steep theater, and Hierapolis — an ancient spa city whose ruined columns stand in Pamukkale's calcium terraces. In Cappadocia, underground cities at Derinkuyu and Kaymakli go 8–18 floors deep.</p>
<p>Greece has Delphi (genuinely stunning in the mountains), Olympia, the Minoan Palace at Knossos (Crete), Ancient Corinth, and Nafplio as a base. The Acropolis Museum in Athens is world-class. But many of Greece's best sites — especially on smaller islands — are modest compared to Ephesus's scale.</p>
<blockquote class="reddit-quote">
"Turkey for sure [for ruins]. Done both, and IMO plenty more to see and experience in Turkey with less crowds. Cappadocia underground cities and caves are incredible."
<span class="source">— r/travel</span>
</blockquote>
<div class="tabiji-verdict">
<strong>⚑ tabiji verdict:</strong> Turkey wins on ruins, volume, and value. The Acropolis is still Greece's crown jewel and no one should skip it — but Ephesus, Troy, Hierapolis/Pamukkale, and Cappadocia's underground cities collectively outmatch Greece's archaeological offerings outside Athens.
</div>
</section>""",

    # 3. Istanbul vs Athens
    """<section class="deep-dive">
<h2 id="istanbul-vs-athens">🏙️ Istanbul vs Athens</h2>
<p>This is the headline city matchup — and both cities are worth 3–5 days minimum.</p>
<p><strong>Athens</strong> is more compact and easier to navigate. The Acropolis anchors everything. Plaka (the old neighborhood below the Acropolis) is charming for evening dining. Monastiraki market is excellent for browsing. The Acropolis Museum is genuinely world-class. English is spoken essentially everywhere. Getting around by foot, metro, and taxi is straightforward. Day trips to Cape Sounion (Temple of Poseidon, 70km), Delphi (180km), and the Peloponnese are excellent.</p>
<p><strong>Istanbul</strong> is a 15-million-person megacity straddling two continents — more chaotic, overwhelming, and spectacular. The Blue Mosque, Hagia Sophia (€22 entry as of 2025), Topkapi Palace, and Grand Bazaar are clustered in Sultanahmet. Beyoglu and Karaköy have the best modern dining and rooftop bars. Crossing the Bosphorus by ferry for a few lira is a genuine highlight. Istanbul rewards multiple visits and is harder to fully "do" in 3 days.</p>
<blockquote class="reddit-quote">
"Istanbul is so unique. I'd say wait to visit Turkey this year since Athens is similar to Istanbul in many ways such as food, history, general friendliness of people — but Istanbul has more on offer."
<span class="source">— r/istanbul</span>
</blockquote>
<blockquote class="reddit-quote">
"Istanbul is way more expensive [than you'd expect for Turkey]. The Hagia Sophia is like 40 Euro. Lots of tourist traps in Sultanahmet area."
<span class="source">— r/travel</span>
</blockquote>
<div class="tabiji-verdict">
<strong>⚑ tabiji verdict:</strong> Istanbul edges Athens for sheer scale and spectacle — there's more to see across more neighborhoods. Athens is the better 3-day city for a tight schedule: easier to "complete" and less overwhelming. For first-timers, Athens is simpler; for experienced travelers, Istanbul is more rewarding.
</div>
</section>""",

    # 4. Cost Comparison
    """<section class="deep-dive">
<h2 id="cost-comparison">💰 Cost Comparison</h2>
<p>Turkey's lira depreciation has made it one of the best-value destinations in the world for Western currency holders. Greece, using the euro, is a mid-range European destination — good value compared to Paris or London, but a premium compared to Turkey.</p>
<p><strong>Turkey daily budget (mid-range, 2025/2026):</strong></p>
<ul>
<li>Accommodation: $25–55 (nice boutique hotel in Istanbul or Cappadocia cave hotel)</li>
<li>Food: $8–15/day eating local (kebabs, baklava, simit, pide, mezes)</li>
<li>Attractions: $5–15/attraction (Hagia Sophia entry is ~€22 as of 2025, but most mosques are free)</li>
<li>Transport: $2–5 for Bosphorus ferries, city buses; domestic flights Cappadocia-Istanbul from $30–60</li>
<li><strong>Total: ~$45–75/day mid-range</strong></li>
</ul>
<p><strong>Greece daily budget (mid-range, 2025/2026):</strong></p>
<ul>
<li>Accommodation: €60–120 (mid-range Athens hotel; island hotels jump sharply in summer)</li>
<li>Food: €20–35/day (taverna meals €12–20, coffee €3–5)</li>
<li>Islands: Santorini/Mykonos add 40–60% to accommodation costs vs Athens or Crete</li>
<li>Ferry transport: Athens→Santorini €35–75 each way depending on speed/class</li>
<li><strong>Total: €70–120/day (€120–180+ in Santorini/Mykonos)</strong></li>
</ul>
<blockquote class="reddit-quote">
"Turkey if you come from EU or US — exchange rate at your benefit. You can do much, much more here."
<span class="source">— r/travel (Croatia vs Italy vs Greece vs Turkey thread)</span>
</blockquote>
<div class="tabiji-verdict">
<strong>⚑ tabiji verdict:</strong> Turkey wins on budget by a wide margin. For a 10-day trip, you could easily spend €800+ less in Turkey than in Greece's islands. If budget matters, Turkey is the clear winner. If you want the Greek island experience specifically, you're paying the premium for a reason.
</div>
</section>""",

    # 5. Unique Experiences
    """<section class="deep-dive">
<h2 id="unique-experiences">✨ Unique Experiences</h2>
<img src="https://img.tabiji.ai/compare/greece-vs-turkey/turkey_cappadocia.jpg" alt="Hot air balloons over Cappadocia's fairy chimneys and volcanic landscape, Turkey" class="section-img" loading="lazy">
<p>Both countries have iconic "bucket list" experiences you won't find anywhere else on earth. This is where each truly shines.</p>
<p><strong>Greece:</strong></p>
<ul>
<li>Watching the sunset from Oia, Santorini — the world's most-photographed sunset, genuinely worth the crowds</li>
<li>Cruising the caldera around Santorini's volcanic rim</li>
<li>Stargazing from the mountains of Crete or the Cycladic islands (some of the darkest skies in Europe)</li>
<li>Walking the Samaria Gorge (Europe's longest gorge, 16km, Crete)</li>
<li>Swimming at Navagio Beach ("Shipwreck Beach," Zakynthos) — accessible only by boat</li>
</ul>
<p><strong>Turkey:</strong></p>
<ul>
<li>Hot air balloon over Cappadocia at sunrise — the single most surreal travel photo in the world. Book months ahead (€150–200/person)</li>
<li>Staying in a cave hotel in Goreme, Cappadocia</li>
<li>Swimming in Pamukkale's travertine calcium pools (thermal water, cotton-castle landscape)</li>
<li>Taking a Bosphorus ferry between Europe and Asia for less than €2</li>
<li>Turkish hammam (bath house) experience — full scrub, foam massage, total body reset</li>
</ul>
<blockquote class="reddit-quote">
"Greece is great, but I'd give the nod to Turkey. Although, to be fair, I'd give the nod to Turkey over most countries I've been to. Incredible food, history, landscapes, people."
<span class="source">— r/TravelNoPics</span>
</blockquote>
<div class="tabiji-verdict">
<strong>⚑ tabiji verdict:</strong> Tie — each has genuinely irreplaceable experiences. The Cappadocia balloon is one of the world's top travel moments. Santorini's sunset is equally legendary. Don't choose based on this category — both deliver.
</div>
</section>""",

    # 6. Food & Dining
    """<section class="deep-dive">
<h2 id="food-dining">🍽️ Food &amp; Dining</h2>
<img src="https://img.tabiji.ai/compare/greece-vs-turkey/turkey_istanbul.jpg" alt="Istanbul's Blue Mosque and Bosphorus skyline, reflecting Turkey's Byzantine and Ottoman heritage" class="section-img" loading="lazy">
<p>Both cuisines are among the Mediterranean's best — but they're different in scope and character.</p>
<p><strong>Turkish food</strong> has extraordinary range. The Turkish breakfast (<em>kahvaltı</em>) alone is worth a visit: spreads of white cheese, olives, tomatoes, cucumbers, jams, simit (sesame bagels), sucuk (spiced sausage), and fresh bread. Street food is exceptional — döner, lahmacun (Turkish pizza), simit, midye dolma (stuffed mussels). Sweets are world-class: baklava from Karaköy Güllüoğlu, künefe, dondurma (Turkish ice cream). Seafood restaurants along the Bosphorus and Aegean coast are exceptional. You can eat incredibly well for $10–15/day.</p>
<p><strong>Greek food</strong> is more focused: taverna classics of moussaka, spanakopita (spinach pie), grilled octopus, souvlaki, and fresh fish with lemon and olive oil. It's simple, high-quality, and deeply tied to local produce. On the islands, the combination of freshly-caught fish, feta, tomatoes ripened in volcanic soil (Santorini), and the world's best olive oil is difficult to beat. Prices are higher but quality is consistent.</p>
<blockquote class="reddit-quote">
"If you aren't going to bother with any of the Greek Islands and plan to spend an extensive amount of time in Athens, then I would just go to Turkey."
<span class="source">— r/TravelNoPics</span>
</blockquote>
<div class="tabiji-verdict">
<strong>⚑ tabiji verdict:</strong> Turkey for variety, value, and daily eating. Greece for the island dining experience (fresh fish + olive oil + view). If you're in Istanbul, visit <a href="/popular-picks/istanbul-kebabs/">Istanbul's best kebab spots</a> and the famous <a href="/popular-picks/istanbul-baklava-shops/">baklava shops in Karaköy</a>. Greece wins for a sunset taverna meal with grilled octopus and white wine — that specific experience is hard to beat.
</div>
</section>""",

    # 7. Getting Around / Logistics
    """<section class="deep-dive">
<h2 id="logistics">✈️ Getting There &amp; Getting Around</h2>
<p>Both countries have strong transport infrastructure for tourists, but with different complexities.</p>
<p><strong>Greece:</strong> Athens International Airport (ATH) is the main hub with direct connections across Europe and increasing transatlantic routes. Domestic travel is primarily by ferry (ANEK, Blue Star, SeaJets) or short domestic flights (Athens→Santorini ~40 min, €40–100 each way). Ferry times: Athens (Piraeus)→Santorini is 5–8 hours (fast ferry ~4h, €35–70). Athens→Crete is 7–9 hours overnight. Internal navigation is easy — ferries are well-organized, signs are in English, and Greece's tourist infrastructure is mature and EU-standard.</p>
<p><strong>Turkey:</strong> Istanbul has two major airports — Istanbul Airport (IST, opened 2019, enormous, on the European side) and Sabiha Gökçen (SAW, on the Asian side). Turkish Airlines flies almost everywhere affordably. Istanbul→Cappadocia (Kayseri or Nevsehir airport) is 1.5 hours by air (~$30–60), or 10–12 hours by overnight bus (~$15–20). Turkey's intercity bus network is excellent — better than Greece's — with modern coaches and competing companies keeping prices low. Language barrier is more significant outside Istanbul.</p>
<div class="tabiji-verdict">
<strong>⚑ tabiji verdict:</strong> Greece is easier to navigate as a tourist — English is widespread, ferries are well-organized, and the EU tourist infrastructure is reliable. Turkey requires slightly more planning but the bus network is exceptional and domestic flights are cheap. Both are manageable for independent travelers.
</div>
</section>""",

    # 8. Best Time to Visit
    """<section class="deep-dive">
<h2 id="best-time-to-visit">🌤️ Best Time to Visit</h2>
<p>Both countries share a Mediterranean climate but with regional variations that matter for trip planning.</p>
<p><strong>Greece - peak season: June–September.</strong> July–August: hottest (35–40°C in Athens, 28–32°C on islands), most crowded, most expensive. Santorini doubles in price; Mykonos is wall-to-wall tourists. Shoulder: May and October are the sweet spots — warm enough to swim (water 20–24°C in May, still warm in October), manageable crowds, 20–30% lower accommodation prices. Winter: Athens is mild and tourist-free (10–15°C); most island businesses close from November–March.</p>
<p><strong>Turkey - peak season: July–August for coasts; April–May, September–October for Istanbul/Cappadocia.</strong> Istanbul is spectacular in April (tulips, festivals, 15–20°C) and September (warm evenings, fewer tour groups). Cappadocia in winter (December–February) is uniquely beautiful with snow-dusted fairy chimneys — cold (0–5°C) but incredible for photos and far cheaper cave hotels. Turkish Riviera (Bodrum, Antalya) peaks in July–August like Greece.</p>
<div class="tabiji-verdict">
<strong>⚑ tabiji verdict:</strong> May and September are the best months for both countries. If you're visiting in July–August for beaches, go to the Greek islands (accept the crowds and cost). If you're doing cities and culture, September in Istanbul or spring in Athens — you'll have a better time than in the sweaty summer peak.
</div>
</section>""",

    # 9. Why Not Both?
    """<section class="deep-dive">
<h2 id="why-not-both">🔀 Why Not Both?</h2>
<p>Greece and Turkey are among the best travel combos in the world — geographically adjacent, culturally contrasting, and together covering an extraordinary range of ancient history, natural beauty, food, and beaches.</p>
<p><strong>A classic 2-week circuit:</strong></p>
<ul>
<li>Day 1–4: Athens — Acropolis, Acropolis Museum, Plaka, National Archaeological Museum, day trip to Cape Sounion</li>
<li>Day 5–7: Santorini — Oia sunset, caldera cruise, black sand beaches</li>
<li>Day 8–11: Istanbul — Hagia Sophia, Blue Mosque, Grand Bazaar, Bosphorus cruise, Beyoglu nightlife</li>
<li>Day 12–14: Cappadocia — balloon flight, cave hotel, underground cities, Rose Valley hike</li>
</ul>
<p>Athens→Istanbul by air: ~1.5 hours, ~€50–120. Santorini→Istanbul via Athens is easy with a stopover. Alternatively, from Rhodes or Kos (Greek islands), there are seasonal ferries to Bodrum or Marmaris on Turkey's coast.</p>
<blockquote class="reddit-quote">
"Greece trip? Considering doing Athens and Istanbul in the same trip. Istanbul should have more dedicated days than Athens. In Turkey, if you can pop over to Cappadocia or Pamukkale they are both very interesting."
<span class="source">— r/GreeceTravel</span>
</blockquote>
<div class="tabiji-verdict">
<strong>⚑ tabiji verdict:</strong> If you have 12–14 days, do both. Athens + one island (3 days) + Istanbul + Cappadocia is genuinely one of the best two-week trips in the Mediterranean. Don't make yourself choose if you have the time.
</div>
</section>"""
]

# --- Comparison Table ---
comparison_table_rows = [
    ["Daily Budget (mid-range)", "€70–100", "$45–75", f'<span class="edge-turkey">Turkey</span>'],
    ["Beaches", "Sandy, iconic, world-class", "Mostly pebbled, beautiful bays", f'<span class="edge-greece">Greece</span>'],
    ["Ancient Ruins", "Acropolis, Delphi, Olympia", "Ephesus, Troy, Pamukkale, Cappadocia", f'<span class="edge-turkey">Turkey</span>'],
    ["Iconic City", "Athens (3-4 days)", "Istanbul (3-5 days)", f'<span class="edge-tie">Tie</span>'],
    ["Unique Experience", "Santorini sunset, island hopping", "Cappadocia balloon, hammam, Bosphorus", f'<span class="edge-tie">Tie</span>'],
    ["Food Culture", "Fresh seafood, olive oil, mezedes", "Turkish breakfast, kebabs, baklava, meze", f'<span class="edge-turkey">Turkey</span>'],
    ["Language Ease", "Greek, English widely spoken", "Turkish, English patchy outside cities", f'<span class="edge-greece">Greece</span>'],
    ["Getting Around", "Ferries, easy, EU-standard", "Excellent buses, cheap domestic flights", f'<span class="edge-tie">Tie</span>'],
    ["Nightlife", "Athens, Mykonos (expensive)", "Istanbul Beyoglu, coastal resorts", f'<span class="edge-tie">Tie</span>'],
    ["Safety", "EU, very safe", "Safe in tourist areas, minor advisories", f'<span class="edge-greece">Greece</span>'],
    ["Best Time", "May, Sep–Oct", "April–May, Sep–Oct; Cappadocia in winter", f'<span class="edge-tie">Tie</span>'],
    ["Visa (US/EU/UK)", "Schengen/no visa", "€60 e-visa for most nationalities", f'<span class="edge-greece">Greece</span>'],
]

table_rows_html = ""
for row in comparison_table_rows:
    table_rows_html += f"""<tr>
<td>{row[0]}</td>
<td>{row[1]}</td>
<td>{row[2]}</td>
<td>{row[3]}</td>
</tr>\n"""

comparison_html = f"""<div class="comparison-section">
<h2 id="quick-comparison">Quick Comparison</h2>
<table class="comparison-table">
<thead>
<tr>
<th>Category</th>
<th>🇬🇷 Greece</th>
<th>🇹🇷 Turkey</th>
<th>Winner</th>
</tr>
</thead>
<tbody>
{table_rows_html}</tbody>
</table>
</div>"""

# --- TOC items ---
toc_items = [
    {"href": "#the-tl-dr-verdict", "label": "⚡ TL;DR Verdict"},
    {"href": "#quick-comparison", "label": "📊 Quick Comparison"},
    {"href": "#beaches", "label": "🏖️ Beaches"},
    {"href": "#ruins-history", "label": "🏛️ Ruins & History"},
    {"href": "#istanbul-vs-athens", "label": "🏙️ Istanbul vs Athens"},
    {"href": "#cost-comparison", "label": "💰 Cost Comparison"},
    {"href": "#unique-experiences", "label": "✨ Unique Experiences"},
    {"href": "#food-dining", "label": "🍽️ Food & Dining"},
    {"href": "#logistics", "label": "✈️ Getting Around"},
    {"href": "#best-time-to-visit", "label": "🌤️ Best Time"},
    {"href": "#why-not-both", "label": "🔀 Why Not Both?"},
    {"href": "#the-decision-framework", "label": "🧭 Decision Framework"},
    {"href": "#frequently-asked-questions", "label": "❓ FAQ"},
]

toc_li_html = "\n".join([f'<li><a href="{t["href"]}">{t["label"]}</a></li>' for t in toc_items])

toc_sidebar_html = f"""<aside class="toc-sidebar">
<h2>Contents</h2>
<ul>
{toc_li_html}
</ul>
</aside>"""

toc_mobile_html = f"""<div class="toc-mobile-sticky" id="toc-mobile">
<button class="toc-mobile-toggle" onclick="this.parentElement.classList.toggle('open')" aria-label="Jump to section">
<span class="toc-active-label" id="toc-active-label">Contents</span>
<span class="toc-chevron">▾</span>
</button>
<div class="toc-mobile-links">
<ul>
{toc_li_html}
</ul>
</div>
</div>"""

# --- Hero HTML ---
hero_html = """<section class="hero">
<div class="hero-badge">🆚 Mediterranean Showdown</div>
<h1>Greece vs Turkey: <em>Which Should You Visit?</em></h1>
<p class="subtitle">A data-backed comparison based on Reddit discussions, real costs, and traveler preferences — not generic AI filler.</p>
<div class="hero-meta">
<div><strong>Updated:</strong> March 2026</div>
<div><strong>Sources:</strong> 10+ Reddit threads, Numbeo, Open-Meteo</div>
<div><strong>Verdict:</strong> Turkey for value &amp; ruins; Greece for beaches &amp; islands</div>
</div>
</section>"""

# --- Photo Grid ---
photo_grid_html = """<div class="photo-grid">
<div>
<img src="https://img.tabiji.ai/compare/greece-vs-turkey/greece_santorini.jpg" alt="Santorini, Greece — iconic whitewashed buildings and blue domes above turquoise Aegean waters" loading="lazy">
<p class="caption">Greece — Santorini, Cyclades</p>
</div>
<div>
<img src="https://img.tabiji.ai/compare/greece-vs-turkey/turkey_istanbul.jpg" alt="Istanbul's Blue Mosque at sunset, with minarets reflected in the Bosphorus" loading="lazy">
<p class="caption">Turkey — Istanbul, Blue Mosque</p>
</div>
</div>"""

# --- Verdict HTML ---
verdict_html = """<div class="verdict-box"><h2 id="the-tl-dr-verdict">⚡ The TL;DR Verdict</h2><p class="verdict-summary"><strong>Turkey wins on value, ancient ruins, food variety, and sheer quantity of extraordinary experiences. Greece wins on beaches, island beauty, and ease of travel.</strong> If you want sandy islands and iconic sunsets, go to Greece. If you want budget travel, world-class ruins (Ephesus!), Cappadocia's landscape, and Istanbul's energy, go to Turkey. Have 12+ days? Do both — Athens + one island + Istanbul + Cappadocia is one of the world's great travel circuits.</p><ul class="verdict-list"><li>🇬🇷 <strong>Greece:</strong> Best for beaches, island hopping, Santorini sunset, easy EU travel</li><li>🇹🇷 <strong>Turkey:</strong> Best for budget travel, Cappadocia, Ephesus, Istanbul, food culture</li><li>✈️ <strong>Both:</strong> 12+ days? Athens (4) + Santorini (3) + Istanbul (3) + Cappadocia (2) = perfect circuit</li></ul></div>"""

# --- Methodology HTML ---
methodology_html = """<div class="methodology-box">
<h2>📋 Our Methodology</h2>
<p>This comparison is built from real sources, not AI guesswork:</p>
<ul class="methodology-points">
<li>10+ Reddit threads from r/travel, r/solotravel, r/TravelNoPics, r/GreeceTravel, r/istanbul synthesized</li>
<li>Cost data from Numbeo (March 2026), recent Reddit trip reports, and Booking.com ranges</li>
<li>Weather from Open-Meteo monthly averages (Athens, Istanbul, Cappadocia, Santorini)</li>
<li>Local transport costs verified against current ferry/flight prices</li>
</ul>
</div>"""

# --- Decision Framework ---
decision_framework_html = """<section class="deep-dive decision-section" id="the-decision-framework">
<h2>🧭 The Decision Framework</h2>
<div class="decision-matrix">
<div class="decision-col">
<h3>🇬🇷 Choose Greece If…</h3>
<ul>
<li>Sandy beaches and island hopping are your #1 priority</li>
<li>You want the Santorini / Mykonos postcard experience</li>
<li>You prefer EU-standard ease of travel (English everywhere, familiar infrastructure)</li>
<li>You've already done Istanbul</li>
<li>You want a shorter trip (5–7 days: Athens + one island covers it well)</li>
<li>You're traveling in July–August and want swimmable sandy beaches</li>
<li>You're a first-time traveler wanting the "iconic Mediterranean" experience</li>
</ul>
</div>
<div class="decision-col">
<h3>🇹🇷 Choose Turkey If…</h3>
<ul>
<li>Budget matters — you'll spend 30–50% less than equivalent Greece</li>
<li>Cappadocia's landscape is on your bucket list (it should be)</li>
<li>You love ancient ruins and haven't seen Ephesus</li>
<li>You want Istanbul's extraordinary scale and energy</li>
<li>Food and cultural immersion matter as much as beaches</li>
<li>You've already been to Greece</li>
<li>You want a hammam experience and Turkish breakfast culture</li>
</ul>
</div>
</div>
</section>"""

# --- CTA HTML ---
cta_html = f"""<div class="cta-section">
<h2>Ready to plan your Mediterranean adventure?</h2>
<p>Get a free custom itinerary for Greece, Turkey, or both — built from real traveler insights, not generic templates.</p>
<div class="cta-buttons">
<a class="cta-btn-greece" href="/i/athens-5-day-itinerary/">Plan Your Greece Trip →</a>
<a class="cta-btn-turkey" href="/i/istanbul-5-day-itinerary/">Plan Your Turkey Trip →</a>
</div>
<p class="cta-sub">Also compare: <a href="/compare/greece-vs-croatia/">Greece vs Croatia</a> · <a href="/compare/croatia-vs-turkey/">Croatia vs Turkey</a> · <a href="/compare/greece-vs-spain/">Greece vs Spain</a></p>
</div>"""

# --- Build full JSON ---
data = {
    "slug": SLUG,
    "pageType": "compare-leaf",
    "status": "published",
    "destinations": {
        "destination1": D1,
        "destination2": D2
    },
    "seo": {
        "title": f"{D1} vs {D2}: Which Should You Visit? (2026 Comparison) | tabiji.ai",
        "metaDescription": f"{D1} vs {D2} — a data-backed comparison based on Reddit discussions, real costs, and traveler preferences. Beaches, ruins, food, Cappadocia, islands: which Mediterranean destination wins?",
        "ogTitle": f"{D1} vs {D2}: Which Should You Visit? — tabiji.ai",
        "ogDescription": f"Reddit-backed comparison of Greece and Turkey. Real costs, ancient ruins, beaches, and honest verdicts from thousands of travelers.",
        "ogImage": OG_IMAGE,
        "twitterTitle": f"{D1} vs {D2}: Which Should You Visit?",
        "twitterDescription": "Data-backed comparison from Reddit discussions, real costs, and traveler preferences.",
        "twitterImage": OG_IMAGE,
        "publishedTime": DATE_ISO,
        "modifiedTime": DATE_ISO,
        "canonical": CANONICAL
    },
    "schema": {
        "article": {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": f"{D1} vs {D2}: Which Should You Visit?",
            "description": f"A data-backed comparison of Greece and Turkey based on Reddit discussions, real costs, weather data, and traveler preferences.",
            "author": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
            "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
            "datePublished": DATE,
            "dateModified": DATE,
            "mainEntityOfPage": CANONICAL,
            "image": OG_IMAGE,
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [".hero h1", ".hero .subtitle", ".verdict-box", ".faq-section"]
            }
        },
        "breadcrumb": {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tabiji.ai/"},
                {"@type": "ListItem", "position": 2, "name": "Compare", "item": "https://tabiji.ai/compare/"},
                {"@type": "ListItem", "position": 3, "name": f"{D1} vs {D2}", "item": CANONICAL}
            ]
        },
        "faq": {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema_items
        }
    },
    "shell": shell,
    "content": {
        "heroHtml": hero_html,
        "tocMobileHtml": toc_mobile_html,
        "methodologyHtml": methodology_html,
        "tocSidebarHtml": toc_sidebar_html,
        "tocItems": toc_items,
        "photoGridHtml": photo_grid_html,
        "verdictHtml": verdict_html,
        "comparisonHtml": comparison_html,
        "deepDiveHtml": deep_dives + [decision_framework_html],
        "faqHtml": faq_html,
        "faqItems": faq_items,
        "ctaHtml": cta_html
    }
}

out_path = Path('/Users/psy/.openclaw/workspace/tabiji/compare-data/greece-vs-turkey.json')
with open(out_path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print(f"Written: {out_path}")
print(f"Size: {out_path.stat().st_size:,} bytes")
PYEOF