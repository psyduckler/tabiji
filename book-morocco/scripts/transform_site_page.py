#!/usr/bin/env python3
"""
Transform books/mexico-tourist-scams/index.html (already copied to
books/morocco-tourist-scams/index.html) into a Morocco book page via bulk
substitutions + a few targeted block replacements.

Run from repo root:
    python3 book-morocco/scripts/transform_site_page.py
"""
from __future__ import annotations

import re
from pathlib import Path

PAGE = Path("books/morocco-tourist-scams/index.html")
text = PAGE.read_text()


# ---------- 1. Simple global token swaps ----------
SIMPLE = [
    # URL slug + ISO
    ("mexico-tourist-scams", "morocco-tourist-scams"),
    ("/country/mx/", "/country/ma/"),
    # Country/adjective
    ("Mexican", "Moroccan"),
    ("Mexico", "Morocco"),
    # Currency unit (do this carefully — only the numeric prefix forms)
    ("MX$", "MAD "),
    # Volume / numerical book stats
    ("Volume 16", "Volume 17"),
    ("VOLUME SIXTEEN", "VOLUME SEVENTEEN"),
    ("114 documented tourist scams", "61 documented tourist scams"),
    ("114 documented", "61 documented"),
    (">114 ", ">61 "),
    (">114<", ">61<"),
    ("114 scams", "61 scams"),
    (">114 ", ">61 "),
    ("19 Mexican cities", "10 Moroccan cities"),
    (">19 Mexican", ">10 Moroccan"),
    (">19 ", ">10 "),
    ("19 Moroccan cities", "10 Moroccan cities"),  # post-Mexico→Morocco swap
    ("19 CITIES", "10 CITIES"),
    ("nineteen most-visited", "ten most-visited"),
    ("412 pages", "234 pages"),
    ("412-page", "234-page"),
    ("\"numberOfPages\":412", "\"numberOfPages\":234"),
    ("412 pages in paperback", "234 pages in paperback"),
    ("approximately 320 pages on Kindle", "approximately 250 pages on Kindle"),
    ("about 78,000 words", "about 44,000 words"),
    ("1.03&#8221; spine", "0.585&#8221; spine"),
    # Amazon link — Morocco book live
    ("https://amzn.to/4mT6QGI", "https://amzn.to/4twGLj8"),
    # Schema / language: Mexican Spanish → Moroccan Arabic (Darija) + French
    ("Spanish exit-phrase card", "Darija exit-phrase card"),
    ("Spanish phrase card", "Darija exit-phrase card"),
    ("Spanish phrases that shut them down", "Darija and French phrases that shut them down"),
    ("Spanish phrases with pronunciation", "Darija and French phrases with pronunciation"),
    ("Mexican Spanish exit phrases", "Moroccan Darija and French exit phrases"),
    # Authority bodies
    ("PROFECO (800 468 8722)", "Allô Wlad Lablad (5050)"),
    ("PROFECO records", "Brigade Touristique records"),
    ("PROFECO and SECTUR records", "Brigade Touristique and Sûreté Nationale records"),
    ("PROFECO advisories", "Brigade Touristique advisories"),
    ("SECTUR (078)", "Sûreté Nationale (19)"),
    ("Polic&#237;a Tur&#237;stica", "Brigade Touristique"),
    ("Pol&#237;cia Tur&#237;stica", "Brigade Touristique"),
    ("Tourist Police records", "Brigade Touristique records"),
    ("CONDUSEF", "Bank Al-Maghrib"),
    # Press outlets list
    ("Reforma", "Le Matin"),
    ("El Universal", "Hespress"),
    ("Milenio", "Yabiladi"),
    ("La Jornada", "Morocco World News"),
    ("Riviera Maya News", "L&#8217;Économiste"),
    ("Mexico News Daily", "Le360"),
    ("Yucatan Times", "Maroc Hebdo"),
]

for old, new in SIMPLE:
    text = text.replace(old, new)


# ---------- 2. Series roadmap line ----------
# Replace the long "Volumes 1 (Japan)…and 15 (Greece) set the series structure" line.
text = text.replace(
    "Volumes 1 (Japan), 2 (Italy), 3 (France), 4 (Thailand), 5 (Spain), 6 (Vietnam), 7 (China), 8 (Indonesia), 9 (Turkey), 10 (Canada), 11 (Germany), 12 (United Kingdom), 13 (Brazil), 14 (Portugal), and 15 (Greece) set the series structure. Morocco (Volume 17) covers the nineteen most-visited Moroccan cities and beach destinations &#8212; Morocco City, the colonial bajio, the Yucat&#225;n, the Riviera Maya, and the Pacific coast &#8212; and is ordered so the flagship Morocco City and Riviera Maya chapters are first and the quieter Pacific anchors (Puerto Escondido, Mazatl&#225;n) last.",
    "Volumes 1 (Japan), 2 (Italy), 3 (France), 4 (Thailand), 5 (Greece), 6 (Vietnam), 7 (Spain), 8 (Indonesia), 9 (China), 10 (Canada), 11 (Mexico), 12 (Turkey), 13 (Germany), 14 (Brazil), 15 (Portugal), and 16 (United Kingdom) set the series structure. Morocco (Volume 17) covers the ten most-visited Moroccan cities &#8212; the imperial cities of Marrakech and Fez, the Atlantic-coast administrative spine (Casablanca, Rabat, Tangier), the blue mountain town of Chefchaouen, the Atlantic-coast resorts (Essaouira, Agadir), and the southern desert circuit (Merzouga, Ouarzazate) &#8212; and is ordered so the flagship Marrakech and Fez chapters are first and the quieter desert and Atlantic-coast anchors last.",
)


# ---------- 3. Hero H1 + hero-sub ----------
text = text.replace(
    "<h1>Don&#8217;t lose MAD 1,500 to an <em>&#8220;authorized taxi&#8221;</em> at Benito Ju&#225;rez airport.</h1>",
    "<h1>Don&#8217;t lose 5,000 dirhams to a Marrakech <em>&#8220;that way is closed&#8221;</em> faux guide.</h1>",
)
# Old hero-sub paragraph (after the Mexico→Morocco swaps it still talks about Mexican press, MEX-airport sitio-taxi etc.)
old_sub = (
    "<p class=\"hero-sub\">61 documented tourist scams across 10 Moroccan cities and beach destinations &#8212; "
    "drawn from Moroccan press (<em>Le Matin</em>, <em>Hespress</em>, <em>Yabiladi</em>, "
    "<em>Morocco World News</em>, <em>L&#8217;Économiste</em>, <em>Le360</em>) and Allô Wlad Lablad (5050), "
    "Sûreté Nationale (19), and Brigade Touristique records. You&#8217;ll learn the exact scripts MEX-airport "
    "sitio-taxi touts use at Terminal 1 arrivals, the moves that stop a Canc&#250;n Hotel-Zone time-share "
    "&#8220;ninety-minute&#8221; pitch from turning into a US$25,000 contract, and the Darija and French phrases "
    "that end an argument in seconds.</p>"
)
new_sub = (
    "<p class=\"hero-sub\">61 documented tourist scams across 10 Moroccan cities &#8212; "
    "drawn from Moroccan press (<em>Le Matin</em>, <em>Hespress</em>, <em>Yabiladi</em>, "
    "<em>Morocco World News</em>, <em>L&#8217;Économiste</em>, <em>Le360</em>) plus Sûreté Nationale (19), "
    "Gendarmerie Royale (177), Brigade Touristique advisories, and US/UK embassy traveler reports. You&#8217;ll "
    "learn the exact scripts faux guides use at Djemaa el-Fna and Bab Boujloud, the moves that stop a Chefchaouen "
    "hash-tout police shakedown from turning into a 5,000-MAD cash demand, and the Darija and French phrases that "
    "end an argument in seconds.</p>"
)
text = text.replace(old_sub, new_sub)


# Hero badges
text = text.replace(
    "<span>📖 234 pages paperback / ~250 Kindle</span>",
    "<span>📖 234 pages paperback / ~250 Kindle</span>",
)
text = text.replace(
    "<span>🌍 10 Moroccan cities</span>",
    "<span>🌍 10 Moroccan cities</span>",
)
text = text.replace(
    "<span>⚠️ 61 scams</span>",
    "<span>⚠️ 61 scams</span>",
)


# ---------- 4. Front-cover SVG title ----------
text = text.replace(
    "fill=\"#3a1010\" text-anchor=\"middle\" letter-spacing=\"-1\" style=\"paint-order: stroke; stroke: #fdf4e3; stroke-width: 4px;\">MOROCCO</text>",
    "fill=\"#3a1010\" text-anchor=\"middle\" letter-spacing=\"-1\" style=\"paint-order: stroke; stroke: #fdf4e3; stroke-width: 4px;\">MOROCCO</text>",
)
text = text.replace(
    "Don&#8217;t Lose MAD 1,500 in Morocco",
    "Don&#8217;t Lose 5,000 dirhams in Morocco",
)
text = text.replace(
    "Drawn from Moroccan press, Brigade Touristique, and Sûreté Nationale records.",
    "Drawn from Le Matin, Hespress &amp; Brigade Touristique advisories.",
)


# ---------- 5. Teaser cards (3 — replace inner content for Morocco) ----------

old_teaser_block_start = "<div class=\"teasers-grid\">"
old_teaser_block_end = "</div>\n  </div>\n</section>\n\n<section class=\"section-alt\">"
new_teasers = """<div class=\"teasers-grid\">
    <article class=\"teaser-card\">
      <span class=\"teaser-badge\">Excerpt &middot; <span class=\"teaser-city\">Marrakech</span></span>
      <h3>The &#8220;That Way&#8217;s Closed&#8221; Fake Guide</h3>
      <p class=\"teaser-excerpt\">A man on the edge of Djemaa el-Fna says the route to the Bahia Palace is closed today &#8212; <em>festival, construction, his cousin&#8217;s wedding</em> &#8212; and offers to walk you the right way. Fifteen turns later you&#8217;re in his uncle&#8217;s carpet shop and he wants 200 MAD ($20) when you try to leave. The original route was open the whole time. r/Morocco threads describe the experience the same way nearly every week: <em>&#8220;every day was relentless scamming of road closed or we are from your hotel.&#8221;</em> The Brigade Touristique still posts warning placards at Bab Doukkala and the entrances to Djemaa el-Fna every season&#8230;</p>
      <div class=\"teaser-flag\"><strong>Red flag:</strong> Anyone who proactively volunteers route information without you asking. Real route closures are visible &#8212; barricades, police, signage.</div>
      <div class=\"teaser-foot\">Full pattern, the offline-map move &amp; the Darija phrase that ends it &#8212; inside.</div>
    </article>

    <article class=\"teaser-card\">
      <span class=\"teaser-badge\">Excerpt &middot; <span class=\"teaser-city\">Chefchaouen</span></span>
      <h3>The Hash-Tout Police Shakedown</h3>
      <p class=\"teaser-excerpt\">A young man on a medina alley near Plaza Uta el-Hammam offers cannabis with a friendly <em>&#8220;you want hash, my friend?&#8221;</em> Within two to ten minutes a man in a short jacket steps out and identifies himself as a police officer. He may flash a real-looking ID. He says cannabis is illegal in Morocco (which it is) and that you&#8217;re going to the station unless you settle here. The opening number is 2,000 MAD ($200); the closing number depends on what&#8217;s in your wallet. r/Morocco documents this scam running in Chefchaouen continuously since at least 2018, and the US State Department warns about it directly&#8230;</p>
      <div class=\"teaser-flag\"><strong>Red flag:</strong> Any &#8220;police officer&#8221; demanding cash on the street rather than asking you to come to the station. Real officers take you to the Sûreté Nationale.</div>
      <div class=\"teaser-foot\">Full pattern, the &#8220;take me to the station&#8221; phrase &amp; the legal-exposure framing &#8212; inside.</div>
    </article>

    <article class=\"teaser-card\">
      <span class=\"teaser-badge\">Excerpt &middot; <span class=\"teaser-city\">Merzouga</span></span>
      <h3>The Marrakech-to-Merzouga Tour Bait-and-Switch</h3>
      <p class=\"teaser-excerpt\">An unverified operator (a clone Tripadvisor listing or a fresh Instagram profile) sells a 3-day Sahara tour for &euro;280&ndash;&euro;350 with photographs of luxury Berber tents, en-suite bathrooms, and a private 4&times;4. What arrives is a basic-tent group camp shared with twenty others, a 2017 minivan that breaks down on the Tizi n&#8217;Tichka pass, and a guide whose itinerary pivots toward four carpet-cooperative stops where the operator earns commission. By the time you can dispute, the operator&#8217;s number has gone dark&#8230;</p>
      <div class=\"teaser-flag\"><strong>Red flag:</strong> Any Sahara tour priced below &euro;500 for a 3-day private 4&times;4 experience. The real range is &euro;600&ndash;&euro;900.</div>
      <div class=\"teaser-foot\">Full list of verified Marrakech tour operators, the chargeback timeline &amp; the move that prevents it &#8212; inside.</div>
    </article>
  </div>
"""

# Replace just the teasers-grid block
import re as _re
text = _re.sub(
    r'<div class="teasers-grid">\s*<article.*?</article>\s*</div>',
    new_teasers.strip(),
    text,
    count=1,
    flags=_re.DOTALL,
)


# ---------- 6. Cities grid (19 → 10) ----------
new_cities_grid = """<div class="cities-grid">
    <div class="city-tile"><span class="city-flag">🕌</span> Marrakech</div>
    <div class="city-tile"><span class="city-flag">🏺</span> Fez</div>
    <div class="city-tile"><span class="city-flag">🏙️</span> Casablanca</div>
    <div class="city-tile"><span class="city-flag">🏛️</span> Rabat</div>
    <div class="city-tile"><span class="city-flag">⛴️</span> Tangier</div>
    <div class="city-tile"><span class="city-flag">🔵</span> Chefchaouen</div>
    <div class="city-tile"><span class="city-flag">🌊</span> Essaouira</div>
    <div class="city-tile"><span class="city-flag">🏖️</span> Agadir</div>
    <div class="city-tile"><span class="city-flag">🐪</span> Merzouga</div>
    <div class="city-tile"><span class="city-flag">🏜️</span> Ouarzazate</div>
  </div>"""
text = _re.sub(
    r'<div class="cities-grid">\s*<div class="city-tile">.*?</div>\s*</div>',
    new_cities_grid,
    text,
    count=1,
    flags=_re.DOTALL,
)


# ---------- 7. Section-alt city-grid header line ----------
text = text.replace(
    "From the Benito Ju&#225;rez airport sitio-taxi overcharge to the Canc&#250;n Hotel-Zone time-share pitch, from Tulum&#8217;s cenote-road shakedowns to Puerto Vallarta&#8217;s Malec&#243;n &#8220;silver&#8221; touts &#8212; full coverage of where foreign visitors actually get caught out across Morocco City, the colonial highlands, the Yucat&#225;n, the Caribbean coast, and the Pacific.",
    "From the Marrakech medina &#8220;that way is closed&#8221; faux guide to the Chefchaouen hash-tout police shakedown, from the Casablanca Marché Central no-menu seafood overcharge to the Merzouga desert-tour bait-and-switch &#8212; full coverage of where foreign visitors actually get caught out across the imperial cities, the Atlantic coast, the Rif, and the Sahara starting line.",
)


# ---------- 8. FAQ JSON-LD city list ----------
text = text.replace(
    "Morocco City, Puebla, Oaxaca, Guanajuato, San Miguel de Allende, Guadalajara, M&#233;rida, San Crist&#243;bal de las Casas, Canc&#250;n, Playa del Carmen, Tulum, Cozumel, Isla Mujeres, Holbox, Puerto Vallarta, Mazatl&#225;n, Acapulco, Cabo San Lucas, and Puerto Escondido.",
    "Marrakech, Fez, Casablanca, Rabat, Tangier, Chefchaouen, Essaouira, Agadir, Merzouga, and Ouarzazate.",
)


# ---------- 9. Updated-annually paragraph ----------
text = text.replace(
    "Sitio-taxi crews at MEX rotate through Terminal 1 every few seasons. Canc&#250;n time-share companies reopen under new names. Tulum cenote operators come and go. The peso drifts meaningfully year-to-year against the dollar.",
    "Marrakech faux-guide teams rotate through Djemaa el-Fna every few seasons. Tangier petit-taxi flat-rate ranges drift upward each year. Merzouga desert-tour operator names appear and disappear quarterly. The dirham is stable but seasonal price variation in tourist corridors is real.",
)


# ---------- 10. Schema.org Book keywords ----------
text = text.replace(
    "morocco, morocco city, cancun, tulum, playa del carmen, oaxaca, tourist scams, travel safety",
    "morocco, marrakech, fez, casablanca, rabat, chefchaouen, merzouga, tourist scams, travel safety",
)


# Save
PAGE.write_text(text)
print(f"transformed {PAGE} ({len(text)} bytes)")

# Quick residue check
residues = ["MX$", "PROFECO", "SECTUR", "Reforma", "El Universal", "Milenio",
            "La Jornada", "Yucat", "Canc", "Tulum", "Mazatl", "Cozumel",
            "Acapulco", "Cabo", "Puebla", "Mexico City", "Mexican",
            "Volume 16", "VOLUME SIXTEEN", "412 page", "78,000",
            "Spanish exit", "Mexican Spanish"]
for r in residues:
    n = text.count(r)
    if n > 0:
        print(f"  RESIDUE: '{r}' x{n}")
