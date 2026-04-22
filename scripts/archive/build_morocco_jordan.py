#!/usr/bin/env python3
"""Build compare-data/morocco-vs-jordan.json"""
import json
from pathlib import Path

SLUG = "morocco-vs-jordan"

# Read CSS/nav/footer from existing page
existing = json.loads(Path("compare-data/jordan-vs-egypt.json").read_text())
style_css = existing["shell"]["styleCss"]
nav_html = existing["shell"]["navHtml"]
footer_html = existing["shell"]["footerHtml"]
scripts = existing["shell"]["scripts"]

# Adjust CSS edge classes for morocco/jordan
style_css = style_css.replace(".edge-jordan {", ".edge-jordan {")
style_css = style_css.replace(".edge-egypt {", ".edge-morocco {")

# Add morocco edge class
style_css = style_css.replace(
    ".edge-jordan { color: var(--indigo); font-weight: 700; }",
    ".edge-jordan { color: var(--indigo); font-weight: 700; }\n        .edge-morocco { color: var(--terracotta); font-weight: 700; }"
)

data = {
    "slug": SLUG,
    "pageType": "compare-leaf",
    "status": "published",
    "destinations": {
        "destination1": "Morocco",
        "destination2": "Jordan"
    },
    "seo": {
        "title": "Morocco vs Jordan: Which Should You Visit? (2026 Comparison) | tabiji.ai",
        "metaDescription": "Morocco vs Jordan — a data-backed comparison based on Reddit discussions, real costs, and traveler preferences. Marrakech vs Petra, Sahara vs Wadi Rum, safety ratings, and honest verdicts.",
        "ogTitle": "Morocco vs Jordan: Which Should You Visit? — tabiji.ai",
        "ogDescription": "Reddit-backed comparison of Morocco and Jordan. Real costs, safety ratings, Sahara vs Wadi Rum, and honest verdicts from thousands of travelers.",
        "ogImage": "https://img.tabiji.ai/compare/morocco-vs-jordan/chefchaouen.jpg",
        "twitterTitle": "Morocco vs Jordan: Which Should You Visit?",
        "twitterDescription": "Data-backed comparison from Reddit discussions, real costs, and traveler preferences.",
        "twitterImage": "https://img.tabiji.ai/compare/morocco-vs-jordan/chefchaouen.jpg",
        "publishedTime": "2026-03-20T00:00:00Z",
        "modifiedTime": "2026-03-20T00:00:00Z",
        "canonical": "https://tabiji.ai/compare/morocco-vs-jordan/"
    },
    "schema": {
        "article": {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": "Morocco vs Jordan: Which Should You Visit?",
            "description": "A data-backed comparison of Morocco and Jordan based on Reddit discussions, real costs, safety data, and traveler preferences — Marrakech vs Petra, Sahara vs Wadi Rum, and which North Africa / Middle East destination wins.",
            "author": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
            "publisher": {"@type": "Organization", "name": "tabiji.ai", "url": "https://tabiji.ai"},
            "datePublished": "2026-03-20",
            "dateModified": "2026-03-20",
            "mainEntityOfPage": "https://tabiji.ai/compare/morocco-vs-jordan/",
            "image": "https://img.tabiji.ai/compare/morocco-vs-jordan/chefchaouen.jpg",
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
                {"@type": "ListItem", "position": 3, "name": "Morocco vs Jordan", "item": "https://tabiji.ai/compare/morocco-vs-jordan/"}
            ]
        },
        "faq": {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Is Morocco or Jordan better for first-time visitors to North Africa / Middle East?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Jordan is the easier and lower-hassle first-time experience. Its tourist infrastructure is excellent, the people are famously welcoming, and Petra alone justifies the trip. Morocco is more atmospheric and culturally overwhelming — in the best way — but the medina touts, scams, and general intensity can catch first-timers off guard. Reddit consensus: Jordan if you want a smoother trip; Morocco if you want immersion and are prepared to be assertive. Both are extraordinary."}
                },
                {
                    "@type": "Question",
                    "name": "Which is cheaper: Morocco or Jordan?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Morocco is generally cheaper. Budget travelers spend $30–50/day in Morocco vs $60–90/day in Jordan. Mid-range riads in Marrakech run $60–120/night while Amman hotels run $60–100/night. The gap narrows significantly if you use Jordan's Jordan Pass (~$108), which bundles your entry visa + 2 days at Petra + 40+ sites. Morocco's souk shopping and street food are world-class cheap; Jordan's is slightly more expensive but still excellent value vs. European prices."}
                },
                {
                    "@type": "Question",
                    "name": "Is Morocco or Jordan safer?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Jordan is generally considered safer and lower-hassle than Morocco. Solo female travelers consistently rate Jordan more comfortable, with men described as respectful and non-threatening. Morocco is safe overall — violent crime against tourists is rare — but the persistent hustling, fake guides, and pressure tactics in Marrakech and Fes are well-documented on Reddit and can feel overwhelming. Both countries have dramatically lower violent crime rates than Western cities; the difference is in day-to-day comfort and harassment levels."}
                },
                {
                    "@type": "Question",
                    "name": "Is Petra or the Sahara Desert better?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Incomparable — they're completely different experiences. Petra is the world's most extraordinary ancient city, carved into rose-red sandstone cliffs; the Siq entrance followed by the Treasury reveal is one of travel's great dramatic moments. Morocco's Sahara (Erg Chebbi near Merzouga) is the classic romantic desert — endless dunes, camel treks, and stargazing from Bedouin camps. Most travelers who've done both describe Petra as the more emotionally powerful site, but the Sahara sunrise from the dune top is equally bucket-list. If you can only choose one iconic experience, Petra edges it — but the Sahara overnight is unmissable."}
                },
                {
                    "@type": "Question",
                    "name": "How many days do you need in Morocco vs Jordan?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Morocco: minimum 7 days for the classic circuit (Marrakech → Fes → Sahara, or Marrakech → Chefchaouen), though 10–14 days lets you do it properly. 7 days feels rushed. Jordan: minimum 5 days — 1 day Jerash/Amman, 2 days Petra, 1 day Wadi Rum, 1 day Dead Sea. 7–9 days is ideal. Jordan's highlights are more geographically compact; Morocco requires more travel between cities."}
                },
                {
                    "@type": "Question",
                    "name": "What is the best time to visit Morocco vs Jordan?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Both countries share similar sweet spots: spring (March–May) and autumn (September–November). Morocco summer (June–August) hits 38–42°C in Marrakech and the inland Sahara gets brutal (50°C+ midday on the dunes). The coastal areas (Essaouira, Agadir) stay cooler. Jordan summer is similarly hot except at altitude — Petra and Amman are manageable at 30–35°C. Both countries are beautiful in April when wildflowers bloom. October is arguably the best month for both simultaneously."}
                },
                {
                    "@type": "Question",
                    "name": "Can you visit Morocco and Jordan on the same trip?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Yes, but they're not as naturally combined as Jordan + Egypt. The most common approach is to fly Morocco → Jordan (typically via Casablanca or Marrakech to Amman via Royal Air Maroc or Royal Jordanian, often with a connection; flights cost $100–200 one way). A 14–16 day trip doing Marrakech → Fes → Sahara → fly to Amman → Petra → Wadi Rum → Dead Sea → Jordan Pass sites is ambitious but rewarding. For most travelers, picking one per trip and returning for the other makes more sense."}
                },
                {
                    "@type": "Question",
                    "name": "Is Morocco good for solo female travelers?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Morocco is doable but requires preparation and assertiveness. Solo female travelers frequently report persistent street hassle in Marrakech and Fes — being followed, offered unsolicited 'guide' services, and general unwanted attention. Dressing conservatively helps significantly. The Reddit r/solotravel sub has long threads on this; the consensus is 'go, but don't be naive.' Jordan is significantly easier — solo women consistently report feeling comfortable and respected across the country. If solo travel comfort is a priority, Jordan is the better choice."}
                },
                {
                    "@type": "Question",
                    "name": "Which country has better food: Morocco or Jordan?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Morocco wins on food variety and depth. Moroccan cuisine — tagines, couscous, pastilla, harira, fresh seafood on the coast, Berber dishes in the mountains, and the world's best preserved lemons — is genuinely complex and varied. The spice culture at Marrakech's souks is an experience in itself. Jordan's food is excellent (mansaf, mezze, falafel, musakhan) but narrower in range. See our guide to Marrakech street food for the best bites. For food-first travelers, Morocco is the clear choice."}
                }
            ]
        }
    },
    "shell": {
        "styleCss": style_css,
        "navHtml": nav_html,
        "footerHtml": footer_html,
        "scripts": scripts
    },
    "content": {
        "heroHtml": """<section class="hero">
<div class="hero-badge">🆚 Country Comparison — North Africa &amp; Middle East</div>
<h1>Morocco vs Jordan: <em>Which Should You Visit?</em></h1>
<p class="subtitle">Marrakech vs Petra. Sahara vs Wadi Rum. Atlantic medinas vs desert canyons. A data-backed comparison of two of the world's most extraordinary travel destinations, built from Reddit discussions, real costs, and thousands of traveler experiences.</p>
<div class="hero-meta">
    <span>🗓️ Updated <strong>March 2026</strong></span>
    <span>📍 <strong>Morocco</strong> vs <strong>Jordan</strong></span>
    <span>💬 Based on <strong>30+ Reddit threads</strong></span>
</div>
</section>""",

        "tocMobileHtml": """<div class="toc-mobile-sticky" id="toc-mobile">
<button class="toc-mobile-toggle" onclick="this.closest('.toc-mobile-sticky').classList.toggle('open')">
<span class="toc-active-label">📑 Contents</span>
<span style="font-size:1.2rem;">▾</span>
</button>
<div class="toc-mobile-dropdown">
<ul>
<li><a href="#the-tl-dr-verdict">⚡ The TL;DR Verdict</a></li>
<li><a href="#quick-comparison">Quick Comparison</a></li>
<li><a href="#iconic-sites">🏺 Iconic Sites &amp; Landmarks</a></li>
<li><a href="#nature-and-landscape">🌄 Nature &amp; Landscape</a></li>
<li><a href="#cost-comparison">💰 Cost Comparison</a></li>
<li><a href="#food-and-dining">🍜 Food &amp; Dining</a></li>
<li><a href="#getting-around">🚗 Getting Around</a></li>
<li><a href="#weather-and-best-time">🌤️ Weather &amp; Best Time</a></li>
<li><a href="#safety">🛡️ Safety</a></li>
<li><a href="#where-to-stay">🏨 Where to Stay</a></li>
<li><a href="#day-trips">🗺️ Day Trips</a></li>
<li><a href="#why-not-both">🔀 Why Not Both?</a></li>
<li><a href="#the-decision-framework">🧭 Decision Framework</a></li>
<li><a href="#frequently-asked-questions">❓ FAQ</a></li>
</ul>
</div>
</div>""",

        "methodologyHtml": """<div class="methodology-box"><h2 id="how-we-built-this-comparison">How we built this comparison</h2><p>This page combines traveler discussion patterns from r/travel, r/solotravel, r/backpacking, r/Morocco, and r/jordan, published price data from Numbeo and recent traveler reports, and official tourism resources from both countries.</p><ul class="methodology-points"><li>30+ Reddit threads analyzed (2020–2026), including detailed solo female trip reports from both countries</li><li>Cost data from Numbeo, Budget Your Trip, and firsthand Reddit reports</li><li>Jordan Pass and Morocco visa pricing from official sources</li><li>Transit and logistics from ONCF/CTM bus schedules and JETT bus timetables</li></ul></div>""",

        "tocSidebarHtml": """<aside class="toc-sidebar">
<h2>Contents</h2>
<ul>
<li><a href="#the-tl-dr-verdict">⚡ The TL;DR Verdict</a></li>
<li><a href="#quick-comparison">Quick Comparison</a></li>
<li><a href="#iconic-sites">🏺 Iconic Sites &amp; Landmarks</a></li>
<li><a href="#nature-and-landscape">🌄 Nature &amp; Landscape</a></li>
<li><a href="#cost-comparison">💰 Cost Comparison</a></li>
<li><a href="#food-and-dining">🍜 Food &amp; Dining</a></li>
<li><a href="#getting-around">🚗 Getting Around</a></li>
<li><a href="#weather-and-best-time">🌤️ Weather &amp; Best Time</a></li>
<li><a href="#safety">🛡️ Safety</a></li>
<li><a href="#where-to-stay">🏨 Where to Stay</a></li>
<li><a href="#day-trips">🗺️ Day Trips</a></li>
<li><a href="#why-not-both">🔀 Why Not Both?</a></li>
<li><a href="#the-decision-framework">🧭 Decision Framework</a></li>
<li><a href="#frequently-asked-questions">❓ FAQ</a></li>
</ul>
</aside>""",

        "tocItems": [
            {"href": "#the-tl-dr-verdict", "label": "⚡ The TL;DR Verdict"},
            {"href": "#quick-comparison", "label": "Quick Comparison"},
            {"href": "#iconic-sites", "label": "🏺 Iconic Sites &amp; Landmarks"},
            {"href": "#nature-and-landscape", "label": "🌄 Nature &amp; Landscape"},
            {"href": "#cost-comparison", "label": "💰 Cost Comparison"},
            {"href": "#food-and-dining", "label": "🍜 Food &amp; Dining"},
            {"href": "#getting-around", "label": "🚗 Getting Around"},
            {"href": "#weather-and-best-time", "label": "🌤️ Weather &amp; Best Time"},
            {"href": "#safety", "label": "🛡️ Safety"},
            {"href": "#where-to-stay", "label": "🏨 Where to Stay"},
            {"href": "#day-trips", "label": "🗺️ Day Trips"},
            {"href": "#why-not-both", "label": "🔀 Why Not Both?"},
            {"href": "#the-decision-framework", "label": "🧭 Decision Framework"},
            {"href": "#frequently-asked-questions", "label": "❓ FAQ"}
        ],

        "photoGridHtml": """<div class="photo-grid">
<div>
<img alt="Chefchaouen, Morocco — the Blue City's narrow medina alleyways painted in shades of blue and white, nestled in the Rif Mountains" loading="lazy" src="https://img.tabiji.ai/compare/morocco-vs-jordan/chefchaouen.jpg"/>
<div class="photo-caption">Morocco — Chefchaouen, the Blue City</div>
</div>
<div>
<img alt="Wadi Rum, Jordan — vast red desert of towering sandstone cliffs and golden sand dunes under a wide open sky" loading="lazy" src="https://img.tabiji.ai/compare/morocco-vs-jordan/wadi-rum.jpg"/>
<div class="photo-caption">Jordan — Wadi Rum, the Valley of the Moon</div>
</div>
</div>""",

        "verdictHtml": """<div class="verdict-box"><h2 id="the-tl-dr-verdict">⚡ The TL;DR Verdict</h2><p class="verdict-summary"><strong>Jordan for ease and iconic sites. Morocco for atmosphere, food, and diversity.</strong> Jordan wins on tourist infrastructure, safety, and concentrated world-class experiences — Petra and Wadi Rum are two of the planet's most extraordinary destinations, packed into a compact, easy-to-navigate country. Morocco wins on sensory immersion, variety, and depth — the contrast between the Atlantic coast, the medinas of Marrakech and Fes, the Blue City of Chefchaouen, and the Sahara is unmatched anywhere on earth. Neither country disappoints. The choice is about what kind of traveler you are.</p>
<ul class="verdict-takeaways">
<li><strong>Jordan edge:</strong> Safety, ease, Petra, Wadi Rum, Dead Sea, tourist infrastructure, less hassle</li>
<li><strong>Morocco edge:</strong> Food, variety, atmospheric medinas, Sahara, Chefchaouen, value, cultural depth</li>
<li><strong>Best combo:</strong> Both reward a return trip — pick one first, come back for the other</li>
</ul>
<div class="verdict-cards">
<div class="verdict-card"><h3>Choose Morocco if…</h3><p>You want immersive cultural variety — souks, tagines, Sahara dunes, blue medinas, and coastline — and are happy being assertive with touts. One of the world's great travel countries.</p></div>
<div class="verdict-card"><h3>Choose Jordan if…</h3><p>You want a smooth, easy Middle East adventure anchored by world-class sites. Petra will be one of the best days of your life. Wadi Rum adds another. The Jordan Pass makes it efficient.</p></div>
<div class="verdict-card"><h3>Do both if…</h3><p>You have 14+ days and good logistics. Neither country is a quick trip — both reward slow travel. Most travelers pick one per trip and return for the other.</p></div>
</div></div>""",

        "comparisonHtml": """<div class="comparison-section">
<h2 id="quick-comparison">Quick Comparison</h2>
<table class="comparison-table">
<thead>
<tr>
<th>Category</th>
<th>🇲🇦 Morocco</th>
<th>🇯🇴 Jordan</th>
<th>Winner</th>
</tr>
</thead>
<tbody>
<tr>
<td>Daily budget (mid-range)</td>
<td>$40–70/day</td>
<td>$60–100/day</td>
<td><span class="edge-morocco">Morocco</span></td>
</tr>
<tr>
<td>Mid-range accommodation</td>
<td>$50–100 (riad)</td>
<td>$55–100/night</td>
<td><span class="edge-tie">Tie</span></td>
</tr>
<tr>
<td>Iconic site</td>
<td>Sahara Desert (Erg Chebbi)</td>
<td>Petra (Al-Khazneh Treasury)</td>
<td><span class="edge-tie">Tie</span></td>
</tr>
<tr>
<td>Cultural variety</td>
<td>Medinas, Sahara, Atlantic coast, Berber mountains</td>
<td>Petra, Wadi Rum, Dead Sea, Roman ruins</td>
<td><span class="edge-morocco">Morocco</span></td>
</tr>
<tr>
<td>Safety for tourists</td>
<td>Safe but higher hassle factor</td>
<td>Excellent — one of safest in region</td>
<td><span class="edge-jordan">Jordan</span></td>
</tr>
<tr>
<td>Solo female travel</td>
<td>Manageable with preparation</td>
<td>Very comfortable, less harassment</td>
<td><span class="edge-jordan">Jordan</span></td>
</tr>
<tr>
<td>Food quality</td>
<td>Exceptional — tagine, couscous, pastilla, seafood</td>
<td>Excellent — mansaf, mezze, falafel</td>
<td><span class="edge-morocco">Morocco</span></td>
</tr>
<tr>
<td>Getting around</td>
<td>ONCF trains + CTM buses (well-connected)</td>
<td>JETT buses + taxis (less frequent)</td>
<td><span class="edge-morocco">Morocco</span></td>
</tr>
<tr>
<td>Natural landscape</td>
<td>Sahara, Atlas Mountains, Atlantic coast</td>
<td>Wadi Rum, Dead Sea, Aqaba reef</td>
<td><span class="edge-tie">Tie</span></td>
</tr>
<tr>
<td>Best time to visit</td>
<td>Mar–May, Sep–Nov</td>
<td>Mar–May, Sep–Nov</td>
<td><span class="edge-tie">Tie</span></td>
</tr>
<tr>
<td>Days needed</td>
<td>7–14 days</td>
<td>5–9 days</td>
<td><span class="edge-jordan">Jordan</span></td>
</tr>
<tr>
<td>Instagram factor</td>
<td>Chefchaouen, medina colors, Sahara dunes</td>
<td>Petra, Wadi Rum, Dead Sea float</td>
<td><span class="edge-tie">Tie</span></td>
</tr>
</tbody>
</table>
</div>""",

        "deepDiveHtml": [

            # 1. Iconic Sites
            """<section class="deep-dive">
<h2 id="iconic-sites">🏺 Iconic Sites &amp; Landmarks</h2>
<p>Both countries have sites that belong on any traveler's bucket list — but the experiences couldn't be more different.</p>

<p><strong>Jordan: Petra.</strong> The Rose-Red City is arguably the single most extraordinary archaeological site in the world. You enter through the <strong>Siq</strong> — a 1.2km narrow sandstone canyon with walls 80 meters high — before the iconic <strong>Al-Khazneh Treasury</strong> is revealed in a moment of pure theatrical brilliance. But Petra is far more than the Treasury: 800+ monuments spread across 264 sq km, including the Street of Facades, the Roman Theatre, the Royal Tombs, the Colonnaded Street, the Qasr al-Bint temple, and the <strong>Monastery (Ad-Deir)</strong> — a 3-hour hike up 800 rock-carved steps to an even larger facade with a sweeping desert view. Plan two full days minimum. Beyond Petra: <strong>Jerash</strong> is one of the best-preserved Roman cities outside Italy — an afternoon well spent before or after. The <strong>Dead Sea</strong> float experience is uniquely bizarre and wonderfully photogenic.</p>

<p><strong>Morocco: Marrakech, Fes, and Chefchaouen.</strong> Morocco's landmarks are urban and atmospheric rather than archaeological. The <strong>Djemaa el-Fna</strong> square in Marrakech — a UNESCO-listed intangible cultural heritage site — transforms from market to carnival at dusk: snake charmers, Gnawa musicians, storytellers, and food stalls filling the air with smoke and sound. The <strong>Medina of Fes</strong> (Fes el-Bali) is the world's largest car-free urban area and the most disorienting city experience in the world — 9,000 streets, medieval tanneries, mosaics, and madrasas. <strong>Chefchaouen</strong>, the "Blue City" painted in every shade of indigo up in the Rif Mountains, is unlike anywhere else on earth. And none of this mentions the <strong>Sahara Desert</strong>, which is Morocco's grandest landmark of all (more on that below).</p>

<img alt="Petra Treasury (Al-Khazneh) in Jordan — the iconic rose-red rock-carved façade revealed at the end of the narrow Siq canyon" class="section-img" loading="lazy" src="https://img.tabiji.ai/compare/morocco-vs-jordan/petra.jpg"/>

<blockquote class="reddit-quote">
"Jordan had overall better people, nice scenery, Petra, Wadi Rum and if you find a good driver plenty of stories. Morocco has more things to see overall, but the tourist infrastructure in Jordan makes touring it a lot easier — less scams, less pressure."
<span class="source">— <a href="https://www.reddit.com/r/travel/comments/14vp5dv/jordan_vs_morocco_morocco_negative_reviews_jordan/" target="_blank" rel="noopener">r/travel — Jordan vs Morocco comparison thread</a></span>
</blockquote>

<blockquote class="reddit-quote">
"Jordan has more 'tourist attractions' — Petra, Wadi Rum, the Dead Sea, Jerash. Morocco is more atmospheric and non-western, with better food. The tourist infrastructure in Jordan makes touring it a lot easier."
<span class="source">— <a href="https://www.reddit.com/r/travel/comments/14vp5dv/jordan_vs_morocco_morocco_negative_reviews_jordan/" target="_blank" rel="noopener">r/travel</a></span>
</blockquote>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Jordan wins on concentrated iconic sites — Petra is one of the world's most extraordinary places, period. Morocco wins on cumulative landmark variety — Marrakech + Fes + Chefchaouen + Sahara = four world-class experiences that don't overlap with anything Jordan offers. If "seeing one truly unmissable thing" is the brief, Petra is it. If you want a journey through multiple extraordinary places, Morocco's variety is hard to match.</div>
</section>""",

            # 2. Nature & Landscape
            """<section class="deep-dive">
<h2 id="nature-and-landscape">🌄 Nature &amp; Landscape</h2>
<p>Both countries offer dramatic, otherworldly natural environments. This is one of the closest calls in the whole comparison.</p>

<p><strong>Jordan's landscapes:</strong></p>
<ul>
<li><strong>Wadi Rum</strong> — "The Valley of the Moon." Towering sandstone and granite cliffs in shades of red and ochre, vast sand plains, prehistoric petroglyphs, and a silence so complete it's its own experience. Bedouin jeep tours ($30–50/person, 4–8 hours) cover the highlights; overnight camps ($80–150/person, all-inclusive) put you under a sky absolutely blazing with stars. The filming location for Lawrence of Arabia, The Martian, and Rogue One — the landscape genuinely looks like another planet.</li>
<li><strong>Dead Sea</strong> — The lowest point on earth (430m below sea level), at 34% salinity. You float effortlessly. The mud is everywhere and feels extraordinary on your skin. Entry to the main public beaches costs around 20 JOD (~$28). The sea is shrinking rapidly due to water diversion — visit now rather than in 20 years.</li>
<li><strong>Aqaba and the Red Sea</strong> — Jordan's narrow access to the Red Sea offers world-class snorkeling and scuba in uncrowded conditions. Visibility 20–30m, pristine coral, and far fewer tourists than Egypt's Hurghada.</li>
<li><strong>Dana Biosphere Reserve</strong> — Four climate zones from the highlands to the Wadi Araba, with challenging hiking trails and dramatic views. Jordan's best-kept outdoor secret.</li>
</ul>

<p><strong>Morocco's landscapes:</strong></p>
<ul>
<li><strong>Sahara Desert (Erg Chebbi, Merzouga)</strong> — The classic desert experience: golden dunes up to 150 meters high at sunset, camel treks at dawn, and overnight Berber camps under the stars. The nearest main dune field is a 9–10 hour drive from Marrakech — most visitors do it on an organized 2–3 day tour ($80–200/person). Less remote than Wadi Rum but more dramatically "desert" looking.</li>
<li><strong>Atlas Mountains</strong> — North Africa's highest range, including <strong>Mount Toubkal</strong> (4,167m, highest peak in North Africa). Trekking villages, traditional Berber settlements, and views across both sides of the range. Toubkal summit is accessible without technical gear with a guide ($60–100/day).</li>
<li><strong>Atlantic and Mediterranean coastlines</strong> — <strong>Essaouira</strong>'s wind-battered ramparts and fishing port, <strong>Asilah</strong>'s whitewashed medina on the Atlantic, <strong>Taghazout</strong>'s surf breaks near Agadir. Morocco has a full coastline that Jordan simply lacks.</li>
<li><strong>Todra and Dades Gorges</strong> — Dramatic canyon walls rising 300m above the river, en route to the Sahara. Often overlooked but stunning.</li>
</ul>

<img alt="Sahara Desert sand dunes at Merzouga, Morocco — golden Erg Chebbi dunes at sunset with a clear sky above" class="section-img" loading="lazy" src="https://img.tabiji.ai/compare/morocco-vs-jordan/merzouga.jpg"/>

<blockquote class="reddit-quote">
"If the goal is a nature-focused trip with one amazing desert experience, Wadi Rum is more unique and atmospheric than the Sahara — it really does look like Mars. But Morocco gives you so much more variety — mountains, coast, desert, all in one trip."
<span class="source">— <a href="https://www.reddit.com/r/travel/comments/yb0g1n/morocco_vs_jordan_in_february/" target="_blank" rel="noopener">r/travel — Morocco vs Jordan in February thread</a></span>
</blockquote>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Genuine tie, but for different travelers. Wadi Rum is more alien and emotionally intense than Morocco's Sahara — there's nothing on earth quite like it. But Morocco's landscape variety (Sahara + Atlas Mountains + Atlantic coast all in one trip) is unmatched. If you want a single extraordinary desert experience: Wadi Rum. If you want a diverse natural landscape journey: Morocco wins decisively.</div>
</section>""",

            # 3. Cost
            """<section class="deep-dive">
<h2 id="cost-comparison">💰 Cost Comparison</h2>
<p>Morocco is the budget winner, but the gap is smaller than many expect — especially once you factor in Jordan's Jordan Pass smart bundling.</p>

<p><strong>Morocco costs:</strong> The country is genuinely affordable for Western travelers. Budget travelers (hostels, street food, buses) spend $30–45/day comfortably. Mid-range travelers staying in riads and eating at restaurants spend $50–80/day. The main costs are intercity transport (CTM buses $10–20/route, ONCF trains $15–30) and organized Sahara tours ($80–200/person for 2–3 days). Street food is excellent and cheap — harira soup for $1, fresh orange juice for $0.50, lamb kefta sandwich for $2. Riads in Marrakech's medina range from $50 (basic) to $200+ (boutique palace). Even mid-range riads offer stunning architecture for the price.</p>

<p><strong>Jordan costs:</strong> Jordan has a reputation for being expensive, and compared to Morocco it is — but it's still great value vs. Western Europe. The <strong>Jordan Pass</strong> (jordanpass.jo) is the key purchase: ~$108 for 2-day Petra access + entry visa (saves $40–65 for most nationalities) + Jerash + Wadi Rum reserve + 40+ other sites. If you're coming from a country that requires a visa and spending 2+ days at Petra, the math strongly favors the Pass. Mid-range hotel nights in Amman and Wadi Musa run $55–100. Food is affordable: $2–4 for street falafel, $10–20 for a proper restaurant dinner. Wadi Rum Bedouin camps: $100–150/person all-inclusive (jeep tour + dinner + breakfast).</p>

<table class="cost-table">
<thead><tr><th>Item</th><th>🇲🇦 Morocco</th><th>🇯🇴 Jordan</th></tr></thead>
<tbody>
<tr><td>Budget hostel/night</td><td>$10–20</td><td>$15–30</td></tr>
<tr><td>Mid-range riad/hotel</td><td>$50–100</td><td>$55–100</td></tr>
<tr><td>Street meal</td><td>$1–3</td><td>$2–5</td></tr>
<tr><td>Restaurant dinner</td><td>$8–18</td><td>$10–20</td></tr>
<tr><td>Main attraction access</td><td>$8–15/site (Sahara tour $80–200)</td><td>Jordan Pass ~$108 all-in</td></tr>
<tr><td>Inter-city transport</td><td>$8–20 (CTM bus/train)</td><td>$5–12 (JETT bus)</td></tr>
<tr><td>Daily budget (mid)</td><td>$45–75</td><td>$65–100</td></tr>
</tbody>
</table>

<blockquote class="reddit-quote">
"Morocco is truly beautiful and people are helpful and kind if you are respectful, but they can be a bit rough compared to Jordanians. Prices are comparable — maybe Morocco slightly cheaper, but not dramatically."
<span class="source">— <a href="https://www.reddit.com/r/travel/comments/at8n5f/morocco_or_jordan/" target="_blank" rel="noopener">r/travel — Morocco or Jordan? thread</a></span>
</blockquote>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Morocco wins on day-to-day cost — accommodation and food are cheaper, and transport is well-subsidized. Jordan's Jordan Pass closes the gap significantly on attraction access. Figure $45–75/day mid-range for Morocco, $65–100/day for Jordan. Neither country is expensive by Western European standards — you get extraordinary value from both. Budget travelers who need to stretch money: Morocco. Travelers who want all-inclusive simplicity: Jordan's Jordan Pass is a masterclass in bundling.</div>
</section>""",

            # 4. Food
            """<section class="deep-dive">
<h2 id="food-and-dining">🍜 Food &amp; Dining</h2>
<p>This is Morocco's clearest win. Moroccan cuisine is one of the world's great food traditions; Jordan's is excellent but narrower.</p>

<p><strong>Morocco's food scene</strong> is built on layers of flavor: preserved lemons, argan oil, ras el hanout spice blends, saffron, slow-cooked meats, fresh Atlantic seafood, and influences from Berber, Arab, Moorish, and French culinary traditions. The stars:</p>
<ul>
<li><strong>Tagine</strong> — Morocco's defining dish. Slow-cooked in a conical clay pot: lamb with prunes and almonds, chicken with preserved lemon and olives, vegetable varieties. Every riad and restaurant has its own version. $6–15 in a proper restaurant.</li>
<li><strong>Couscous</strong> (Fridays only in traditional households, but available everywhere) — hand-rolled semolina steamed over the stew, piled into a cone. One of the world's great comfort foods.</li>
<li><strong>Pastilla</strong> — Sweet-savory pigeon (or chicken) pie dusted with powdered sugar and cinnamon. One of the most surprising and wonderful things you'll eat.</li>
<li><strong>Harira</strong> — Rich tomato, lentil, and chickpea soup with herbs and lemon. $1 at any street cart. Essential.</li>
<li><strong>Seafood</strong> — Essaouira and Agadir have extraordinary fresh fish and grilled sardines for almost nothing at the port market.</li>
</ul>
<p>See our guides to <a href="/popular-picks/marrakech-street-food/">Marrakech street food</a>, <a href="/popular-picks/marrakech-cooking-classes/">Marrakech cooking classes</a>, and <a href="/popular-picks/marrakech-riads/">Marrakech riads</a> for the best experiences.</p>

<p><strong>Jordan's food scene</strong> revolves around generous mezze culture and slow-cooked Levantine traditions:</p>
<ul>
<li><strong>Mansaf</strong> — Jordan's national dish: lamb cooked in fermented dried yogurt (jameed) over saffron rice, served on a communal platter. Rich, unusual, and absolutely worth seeking out. $10–18 at a local restaurant.</li>
<li><strong>Falafel and mezze</strong> — Fresh-baked khubz flatbread with hummus, baba ganoush, labneh, tabbouleh, and stuffed vine leaves makes a perfect Jordanian breakfast. <strong>Hashem Restaurant</strong> in Amman (open since 1952, cash only) serves legendary falafel for under $3.</li>
<li><strong>Musakhan</strong> — Roasted chicken on flatbread with caramelized onions and sumac. Understated and delicious.</li>
<li><strong>Kanafeh</strong> — The great Levantine dessert: cheese pastry soaked in rosewater syrup. Nablus (near Jordan) is the alleged origin; excellent versions throughout Amman.</li>
</ul>

<blockquote class="reddit-quote">
"Morocco has some of the most interesting food in the world — the tagines, the pastilla, the couscous, the harira, the seafood in Essaouira. Jordan's food is good but more limited in range. Food-first traveler? Morocco wins."
<span class="source">— <a href="https://www.reddit.com/r/travel/comments/13o87hm/morocco_or_jordan_for_a_week/" target="_blank" rel="noopener">r/travel — Morocco or Jordan for a week?</a></span>
</blockquote>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Morocco wins clearly. Moroccan cuisine has more depth, variety, and centuries of layered influence than Jordan's. That said, Jordan's mezze culture is beautiful and mansaf is a genuinely unique dish. If you're a food-first traveler, Morocco is one of the world's top food destinations — it should be a primary reason to go, not an afterthought.</div>
</section>""",

            # 5. Getting Around
            """<section class="deep-dive">
<h2 id="getting-around">🚗 Getting Around</h2>
<p>Morocco has better public transport; Jordan has easier navigation between a smaller number of key sites.</p>

<p><strong>Morocco's transit options:</strong></p>
<ul>
<li><strong>ONCF (national rail)</strong> — Comfortable, affordable, and reliable trains connect Casablanca, Rabat, Fes, Meknes, and Tangier. The high-speed Al Boraq train between Casablanca and Tangier takes 2h15m (vs 5+ hours by road). Tickets $10–30 depending on distance and class. The rail network doesn't reach Marrakech (connection required) or the south (Sahara).</li>
<li><strong>CTM buses</strong> — Morocco's premium intercity bus company. Comfortable, air-conditioned, reliable. Reaches everywhere the trains don't: Marrakech, Agadir, Ouarzazate, Errachidia (Sahara). Tickets $8–20. The classic Marrakech → Fes overnight bus ($15–20) is a rite of passage.</li>
<li><strong>Supratours</strong> — Another reliable bus operator, often connecting to train stations. Good for coastal routes.</li>
<li><strong>Grands taxis</strong> — Shared taxis that run fixed routes between cities and towns. Cramped but cheap. Essential for reaching smaller destinations. Negotiate the price before boarding.</li>
<li><strong>Rental car</strong> — Great for reaching the Sahara and Atlas Mountains on your own schedule. Roads are good; drivers can be aggressive in cities.</li>
</ul>

<p><strong>Jordan's transit options:</strong></p>
<ul>
<li><strong>JETT bus</strong> — Jordan's main intercity bus service. Comfortable, air-conditioned, and affordable ($5–12/trip). Runs Amman → Aqaba and Amman → Petra (Wadi Musa). Timing is limited; check schedules carefully.</li>
<li><strong>Private taxis / transfers</strong> — The most flexible option. Amman → Petra by private taxi costs ~$70–80 vs $12 by JETT, but lets you stop at the Dead Sea and Madaba en route. Worth it for groups.</li>
<li><strong>Rental car</strong> — Increasingly popular. Roads are good; Jordan is compact and easy to drive. The King's Highway route between Amman and Petra is one of the most scenic drives in the Middle East — seriously consider renting.</li>
<li><strong>Uber/Careem</strong> — Works well in Amman. Highly recommended over negotiating with street taxis.</li>
</ul>

<blockquote class="reddit-quote">
"Jordan is logistically straightforward — hire a driver for a few days and cover Amman, Dead Sea, Petra, Wadi Rum. Morocco you need more time and planning to get between cities, but the journey is part of it."
<span class="source">— <a href="https://www.reddit.com/r/travel/comments/12wnqhk/morocco_vs_jordan_in_october/" target="_blank" rel="noopener">r/travel — Morocco vs Jordan in October</a></span>
</blockquote>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Morocco has better public transport infrastructure (especially the trains), but Jordan is easier to navigate as a first-time visitor because the key sites are fewer and more geographically concentrated. Morocco rewards independent travelers who plan their transport; Jordan makes it straightforward to hit all the highlights with minimal logistics. Neither requires a rental car, but both benefit from one.</div>
</section>""",

            # 6. Weather
            """<section class="deep-dive">
<h2 id="weather-and-best-time">🌤️ Weather &amp; Best Time to Visit</h2>
<p>Both Morocco and Jordan have broadly similar climates — hot dry summers, mild winters — with the same ideal travel window: <strong>spring (March–May) and autumn (September–November)</strong>.</p>

<p><strong>Morocco weather by season:</strong></p>
<ul>
<li><strong>March–May</strong> — Best overall window. Marrakech 20–28°C, pleasant for medina walking. Chefchaouen at altitude stays cooler. Atlas Mountain hiking excellent. Sahara manageable (30–35°C daytime vs 50°C in summer). Crowds building but not overwhelming.</li>
<li><strong>June–August</strong> — Brutal inland. Marrakech regularly hits 38–42°C; Sahara midday temperatures exceed 50°C. The coast (Essaouira, Agadir) stays moderate (22–28°C) thanks to Atlantic trade winds — very pleasant for a beach-focused trip. Avoid Fes and Marrakech in July–August.</li>
<li><strong>September–October</strong> — Second-best window. Temperatures dropping; summer tourists gone. Sahara back to comfortable range. October in Morocco is excellent.</li>
<li><strong>November–February</strong> — Mild on the coasts; cold in the mountains and at altitude (Chefchaouen can snow). Marrakech winters are pleasant at 15–20°C but can have rainy spells. Dead of winter is quieter and cheaper.</li>
</ul>

<p><strong>Jordan weather by season:</strong></p>
<ul>
<li><strong>March–May</strong> — Peak season and best weather for hiking. Petra 18–26°C. Wildflowers in Wadi Rum. Dana Reserve trails excellent. Spring brings occasional brief rains but mostly clear.</li>
<li><strong>June–August</strong> — Hot but manageable at Petra's altitude (25–35°C). The Jordan Valley and Dead Sea region hits 35–42°C. Wadi Rum is exhausting midday but magical at sunrise/sunset. Aqaba is swimmable year-round.</li>
<li><strong>September–November</strong> — Excellent. Temperatures dropping to ideal hiking range. Few crowds. Wadi Rum sunsets without summer heat.</li>
<li><strong>December–February</strong> — Cold, especially in Amman and Petra (can snow). Dead Sea and Aqaba stay warm (18–24°C) — a great winter escape. Petra in snow is hauntingly beautiful and uncrowded.</li>
</ul>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Both countries peak in the same window — October is arguably the single best month for either. Spring (March–April) is excellent for Jordan specifically (wildflower season, Petra hiking), and October–November is the sweet spot for the Sahara in Morocco. If you're planning a combined trip, target April or October when both countries are near their best simultaneously.</div>
</section>""",

            # 7. Safety
            """<section class="deep-dive">
<h2 id="safety">🛡️ Safety</h2>
<p>Both countries are safe for tourists — but the traveler experience is meaningfully different between them.</p>

<p><strong>Jordan</strong> is consistently ranked among the safest countries in the Middle East for tourists, and Reddit bears this out overwhelmingly. The Jordanian culture of hospitality (diyafa) is genuine and well-documented — locals offer tea, give directions without asking anything in return, and make travelers feel genuinely welcome. Violent crime against tourists is extremely rare. The main "dangers" are: minor overcharging at tourist sites (fixable by checking prices beforehand), being offered unnecessary guide services (a firm "la, shukran" works), and aggressive taxi haggling in tourist areas. Solo female travelers consistently describe Jordan as comfortable and respectful. The country has been politically stable for decades.</p>

<p><strong>Morocco</strong> is safe overall — violent crime against tourists is genuinely uncommon — but the persistent street harassment, fake guide culture, and scam density in Marrakech and Fes is well-documented and can be exhausting, particularly for first-time visitors and solo women. The famous Marrakech souk touts (men who "helpfully" guide you into a shop before demanding payment, or lead you in circles while the meter ticks up on a "free" tour) are a real phenomenon. The good news: Morocco's intense reputation has improved significantly in recent years, and with basic precautions (dress conservatively, be assertive, download offline maps) the experience is very manageable.</p>

<blockquote class="reddit-quote">
"They are both great destinations, but if you ask about safety and time I would recommend Jordan over Morocco. Morocco is an amazing destination but as a solo female traveler Jordan is a lot more comfortable — people leave you alone, touts are polite if persistent, and you never feel at risk."
<span class="source">— <a href="https://www.reddit.com/r/travel/comments/at8n5f/morocco_or_jordan/" target="_blank" rel="noopener">r/travel — Morocco or Jordan? thread</a></span>
</blockquote>

<blockquote class="reddit-quote">
"Morocco used to be a dream destination — and it still is! But prepare mentally for the hustle factor in Marrakech and Fes. Download Maps.me offline, know where you're going, and say no firmly and keep walking. The country is extraordinary once you get past the tourist entry gauntlet."
<span class="source">— <a href="https://www.reddit.com/r/travel/comments/15vdnok/morocco_used_to_be_a_dream_destination_is_it_that/" target="_blank" rel="noopener">r/travel</a></span>
</blockquote>

<blockquote class="reddit-quote">
"If you're a woman, go to Jordan. Morocco is worth it but Jordan is just easier and more comfortable, especially solo." 
<span class="source">— <a href="https://www.reddit.com/r/arabs/comments/xldyvc/study_abroad_in_jordan_or_morocco/" target="_blank" rel="noopener">r/arabs — Jordan or Morocco study abroad</a></span>
</blockquote>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Jordan wins clearly on comfort and ease — it's a significantly lower-hassle experience than Morocco's major tourist centers. That said, "Morocco is dangerous" is an overstatement; it's safe, just requires more psychological preparation and assertiveness. For first-time solo travelers, especially women, Jordan is the clear low-stress choice. For experienced travelers who understand the game: Morocco's intensity is part of what makes it so memorable.</div>
</section>""",

            # 8. Where to Stay
            """<section class="deep-dive">
<h2 id="where-to-stay">🏨 Where to Stay</h2>
<p>Morocco's riads are genuinely one of the world's great accommodation experiences. Jordan's Bedouin camps are in a different category entirely.</p>

<p><strong>Morocco's best bases:</strong></p>
<ul>
<li><strong>Marrakech (Medina)</strong> — Staying in a <strong>riad</strong> (traditional courtyard house, often with plunge pool, mosaic tilework, and a rooftop terrace) is the quintessential Morocco experience. Range from $50 (basic, budget riad) to $300+ (boutique palace). Even budget riads deliver extraordinary architecture for the price. The Medina is the place to be — Jemaa el-Fna at your doorstep. Gueliz (the modern French quarter) is quieter but less atmospheric. See our <a href="/popular-picks/marrakech-riads/">Marrakech riads guide</a> for picks.</li>
<li><strong>Fes (Fes el-Bali)</strong> — Staying inside the ancient medina walls puts you in the world's most intact medieval city. Riads in Fes's medina from $40–120/night. Bou Inania Madrasa, Chouara Tanneries, and Al-Qarawiyyin Mosque all within walking distance.</li>
<li><strong>Chefchaouen</strong> — Small mountain town, entirely walkable, with charming budget guesthouses ($20–60/night). The blue medina streets are genuinely as photogenic as Instagram suggests.</li>
<li><strong>Sahara camps (Merzouga)</strong> — Berber tent camps from $60 (basic) to $200+ (luxury glamping with private tent, shower, dinner + camel trek included). The experience of waking up in the dunes at sunrise — any price tier — is unforgettable.</li>
</ul>

<p><strong>Jordan's best bases:</strong></p>
<ul>
<li><strong>Amman (Jabal Amman)</strong> — Rainbow Street, 1st Circle, and the Weibdeh neighborhood have the best restaurants, cafes, and art galleries. Surprisingly cosmopolitan. Mid-range hotels $55–100/night. Great first and last night base before/after the desert.</li>
<li><strong>Wadi Musa (Petra gateway)</strong> — Where you sleep to visit Petra. Small, utilitarian town but convenient. Hotels from $35–80/night. Booking in advance is essential during March–May peak season.</li>
<li><strong>Wadi Rum (Bedouin camps)</strong> — The experience. Basic tents ($40–70/person) to luxury "bubble domes" with panoramic desert views and private bathrooms ($200+/night). Most include jeep tours, dinner cooked over open fire, and breakfast in the price. Sleeping under the Wadi Rum stars is one of those travel nights that stays with you forever.</li>
<li><strong>Aqaba (Red Sea)</strong> — Beach resort town, good for a rest day + diving. $55–100/night at decent hotels. Popular in winter when the rest of Jordan is cold.</li>
</ul>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Morocco's riads are a unique accommodation category that Jordan can't match for architecture and atmosphere — staying in a centuries-old courtyard house in a Marrakech medina is an experience in itself. Jordan's Wadi Rum Bedouin camps are equally special but in a completely different way — the stargazing from those camps is among the best on earth. Both countries deliver genuinely memorable accommodation; Morocco's is more widely distributed, Jordan's peaks harder.</div>
</section>""",

            # 9. Day Trips
            """<section class="deep-dive">
<h2 id="day-trips">🗺️ Day Trips</h2>
<p>Both countries are well-suited to day trip circuits from their main bases.</p>

<p><strong>From Marrakech:</strong></p>
<ul>
<li><strong>Atlas Mountains / Imlil</strong> (1.5h drive) — Berber villages, walnut orchards, and trailheads for the Toubkal summit (2-day hike). Day trip hiking from $40–70/person with guide.</li>
<li><strong>Ourika Valley</strong> (45 min) — Verdant river valley with Berber villages and waterfalls. Perfect half-day from Marrakech. Shared grands taxi from $3/person.</li>
<li><strong>Essaouira</strong> (2.5h bus) — Atlantic port town with whitewashed ramparts, fishing harbor, fresh grilled fish, and a famous wind (it's called "the windy city of Africa"). CTM bus $10 each way.</li>
<li><strong>Ait Benhaddou</strong> (3h) — UNESCO-listed ksar (fortified village) used in Gladiator, Game of Thrones, Lawrence of Arabia. Usually combined with an organized tour to the Sahara (2–3 day loop).</li>
</ul>

<p><strong>From Amman:</strong></p>
<ul>
<li><strong>Jerash</strong> (1h) — One of the best-preserved Roman cities on earth. Hadrian's Arch, the Oval Plaza, Temple of Artemis, colonnaded streets. Genuinely world-class; entry $12. Easy half-day.</li>
<li><strong>Dead Sea</strong> (1h) — The float. The mud. The lowest point on earth. Entry ~$28 at main beaches. Best combined with Madaba and Mt. Nebo into a full-day King's Highway drive.</li>
<li><strong>Madaba + Mt. Nebo</strong> (45 min) — The 6th-century Byzantine mosaic map of the Holy Land in St. George's Church is extraordinary for its age and detail. Mt. Nebo's view extends to Jerusalem on clear days. Free or minimal entry.</li>
<li><strong>Ajloun</strong> (1.5h) — 12th-century Arab castle built by Saladin's nephew, set dramatically atop a forested hill. Undervisited and excellent. Entry $3.</li>
</ul>

<blockquote class="reddit-quote">
"The day trip circuit from Amman is one of the best I've done anywhere — Jerash in the morning, Dead Sea float in the afternoon, sunset at Madaba. All within 3 hours of the city. Jordan is remarkably compact for what it offers."
<span class="source">— <a href="https://www.reddit.com/r/travel/comments/1rhu6ev/jordan_10_days_in_the_jewel_of_the_middle_east/" target="_blank" rel="noopener">r/travel — Jordan 10 days trip report</a></span>
</blockquote>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Jordan's day trip circuit from Amman is arguably more impressive for the concentration of world-class sites close together. Morocco's day trips from Marrakech are excellent but often require longer travel times or multi-day excursions (especially for the Sahara). Both countries reward slowing down and staying longer rather than packing too many day trips into too few days.</div>
</section>""",

            # 10. Why Not Both / Decision Framework
            """<section class="deep-dive">
<h2 id="why-not-both">🔀 Why Not Both?</h2>
<p>Morocco and Jordan aren't as naturally combined as, say, Jordan and Egypt — they're in different geographic regions with no obvious overland connection. But doing both on a longer trip is absolutely possible and extremely rewarding.</p>

<p><strong>Logistics:</strong> The most practical route is to fly between the two. Main connections: Casablanca (CMN) or Marrakech (RAK) to Amman (AMM) — typically with a layover in Casablanca, Istanbul, or Doha. Flights cost $100–200 one way. Travel time: 5–8 hours including connections. There's no ferry or overland option.</p>

<p><strong>A 16-day Morocco + Jordan itinerary:</strong></p>
<ul>
<li><strong>Days 1–3:</strong> Marrakech — Djemaa el-Fna, medina souks, day trip to Atlas Mountains</li>
<li><strong>Days 4–5:</strong> Fes — Medina exploration, Chouara Tanneries, Bou Inania Madrasa</li>
<li><strong>Day 6:</strong> Chefchaouen — Blue city afternoon and overnight</li>
<li><strong>Days 7–9:</strong> Sahara (Merzouga) — Ait Benhaddou, Dades Gorge, overnight Bedouin camp, sunrise dunes</li>
<li><strong>Day 10:</strong> Fly Marrakech → Amman (via connection)</li>
<li><strong>Days 11–12:</strong> Amman + Jerash + Dead Sea day circuit</li>
<li><strong>Days 13–14:</strong> Petra — 2 full days (Treasury, Monastery, trails)</li>
<li><strong>Day 15:</strong> Wadi Rum — Jeep tour + overnight Bedouin camp</li>
<li><strong>Day 16:</strong> Aqaba beach + fly home (Amman)</li>
</ul>

<p>Compare also: <a href="/compare/jordan-vs-egypt/">Jordan vs Egypt</a> if you're considering the Jordan + Egypt combo, or <a href="/compare/portugal-vs-morocco/">Portugal vs Morocco</a> if Morocco vs a European alternative is the question. For the Egypt side of this comparison, see <a href="/compare/morocco-vs-egypt/">Morocco vs Egypt</a>.</p>

<div class="tabiji-verdict"><strong>tabiji verdict:</strong> Both countries absolutely reward a dedicated trip each — Morocco ideally 10+ days, Jordan 7+ days. They're less naturally combined than Jordan+Egypt (which share a border and 90-minute flight), but for travelers with 3+ weeks and a love of MENA/North Africa, doing both delivers an incredible contrast: Morocco's chaotic, sensory, medina-and-desert immersion followed by Jordan's calm, ancient, world-class site experience. Or vice versa. Either way, extraordinary.</div>
</section>""",

            # Decision Framework
            """<section class="deep-dive">
<h2 id="the-decision-framework">🧭 The Decision Framework</h2>
<div class="decision-matrix">
<div>
<h3>Choose <strong>Morocco</strong> if…</h3>
<ul>
<li>Food and cultural immersion are primary motivations</li>
<li>You want maximum variety in one trip (medinas + mountains + desert + coast)</li>
<li>The Sahara Desert overnight is a bucket-list item</li>
<li>You want to explore a city as intensely atmospheric as Fes or Marrakech</li>
<li>You're combining with Portugal, Spain, or mainland Europe</li>
<li>Budget is a significant factor ($40–70/day vs $65–100)</li>
<li>You've already done Jordan and want something completely different</li>
<li>You're willing to be assertive with touts for the cultural payoff</li>
</ul>
</div>
<div>
<h3>Choose <strong>Jordan</strong> if…</h3>
<ul>
<li>Seeing Petra is a lifelong ambition — it will not disappoint</li>
<li>You want a smooth, easy Middle East introduction</li>
<li>You're traveling solo, especially as a woman</li>
<li>Wadi Rum's alien desert landscape appeals to you</li>
<li>You have only 5–7 days and want a tight, rewarding itinerary</li>
<li>You're combining with Israel, Egypt, or the Gulf</li>
<li>You want world-class sites without high hassle factor</li>
<li>The Jordan Pass value calculation works in your favor</li>
</ul>
</div>
</div>
</section>"""
        ],

        "faqHtml": """<section class="faq-section">
<h2 id="frequently-asked-questions">❓ Frequently Asked Questions</h2>
<div class="faq-item">
<h3>Is Morocco or Jordan better for first-time visitors?</h3>
<p>Jordan is the lower-hassle, easier first-time experience. Tourist infrastructure is excellent, the people are famously welcoming, and Petra alone justifies the trip. Morocco is more atmospheric and offers more variety — but the medina hustle in Marrakech and Fes can catch first-timers off guard. Reddit consensus: Jordan first if comfort is the priority; Morocco if you want cultural intensity and are prepared to be assertive.</p>
</div>
<div class="faq-item">
<h3>Which is cheaper: Morocco or Jordan?</h3>
<p>Morocco is generally cheaper — $40–70/day mid-range vs $65–100/day in Jordan. However, Jordan's Jordan Pass (~$108) bundles the entry visa + Petra + 40+ sites and provides excellent value if you're coming from a visa-required country. Morocco's day-to-day costs (street food, accommodation, transport) are all lower. Neither country is expensive by Western European standards.</p>
</div>
<div class="faq-item">
<h3>Is Morocco or Jordan safer?</h3>
<p>Jordan is significantly more comfortable in terms of day-to-day tourist experience. It has lower harassment levels, more respectful interactions with strangers, and solo travelers (especially women) consistently rate it safer and more comfortable than Morocco. Morocco is safe from a violent crime perspective, but the persistent tout culture in Marrakech and Fes requires mental preparation and assertiveness.</p>
</div>
<div class="faq-item">
<h3>Is Petra or Morocco's Sahara Desert better?</h3>
<p>Completely different experiences — both are extraordinary. Petra is the world's most dramatic ancient city, revealed through a 1.2km canyon; the emotional impact of first seeing the Treasury is something travelers describe as genuinely life-changing. Morocco's Sahara (Erg Chebbi near Merzouga) is the quintessential desert overnight — golden dunes at sunset, Berber camp, camel ride at dawn. Most travelers who've done both say Petra is the more powerful single experience, but the Sahara overnight is magical in a different way.</p>
</div>
<div class="faq-item">
<h3>How many days do you need in each country?</h3>
<p>Morocco: minimum 7 days for the classic Marrakech → Fes → Sahara circuit, ideally 10–14. Jordan: minimum 5 days for Amman + Jerash + Dead Sea + Petra + Wadi Rum, ideally 7–9. Jordan's highlights are more geographically compact; Morocco requires more travel time between its diverse regions. Both countries reward slow travel over rushing.</p>
</div>
<div class="faq-item">
<h3>What's the best time of year to visit Morocco vs Jordan?</h3>
<p>Both countries share the same ideal travel window: spring (March–May) and autumn (September–November). Summer (June–August) is brutally hot in both countries' inland areas — Marrakech hits 40°C+, Jordan's desert areas hit 40–45°C. October is arguably the single best month for either country; it works well for a combined trip. Morocco's Atlantic coast (Essaouira, Agadir) stays pleasant year-round.</p>
</div>
<div class="faq-item">
<h3>Is Morocco good for solo female travelers?</h3>
<p>Morocco is doable but requires more preparation and assertiveness than Jordan. Solo female travelers frequently report persistent unwanted attention in Marrakech and Fes. Dressing conservatively, having a confident manner, and knowing where you're going helps dramatically. Jordan is significantly more comfortable for solo women — the country consistently receives top marks for female solo travel comfort in the MENA region. If in doubt, start with Jordan.</p>
</div>
<div class="faq-item">
<h3>Which country has better food?</h3>
<p>Morocco wins clearly on food. Moroccan cuisine — tagines, couscous, pastilla, harira, preserved lemons, Atlantic seafood — is one of the world's great culinary traditions with extraordinary variety. Jordan's food is excellent (mansaf, mezze, falafel, kanafeh) but more limited in scope. For food-first travelers, Morocco is a primary reason to visit. See our <a href="/popular-picks/marrakech-street-food/">Marrakech street food guide</a> for the best bites.</p>
</div>
<div class="faq-item">
<h3>Can you visit Morocco and Jordan on the same trip?</h3>
<p>Yes, but they're not naturally combined — you'll need to fly (typically 5–8 hours with a connection, $100–200 one way). They're geographically in different regions with no overland route. Most travelers visit them on separate trips. A 14–16 day combined itinerary (Marrakech → Fes → Sahara → fly to Amman → Petra → Wadi Rum) is ambitious but very rewarding for travelers with the time and budget.</p>
</div>
</section>""",

        "faqItems": [
            {"question": "Is Morocco or Jordan better for first-time visitors?", "answer": "Jordan is the lower-hassle, easier first-time experience. Tourist infrastructure is excellent, the people are famously welcoming, and Petra alone justifies the trip. Morocco is more atmospheric and offers more variety — but the medina hustle in Marrakech and Fes can catch first-timers off guard. Reddit consensus: Jordan first if comfort is the priority; Morocco if you want cultural intensity and are prepared to be assertive."},
            {"question": "Which is cheaper: Morocco or Jordan?", "answer": "Morocco is generally cheaper — $40–70/day mid-range vs $65–100/day in Jordan. However, Jordan's Jordan Pass (~$108) bundles the entry visa + Petra + 40+ sites and provides excellent value if you're coming from a visa-required country. Morocco's day-to-day costs (street food, accommodation, transport) are all lower. Neither country is expensive by Western European standards."},
            {"question": "Is Morocco or Jordan safer?", "answer": "Jordan is significantly more comfortable in terms of day-to-day tourist experience. It has lower harassment levels, more respectful interactions with strangers, and solo travelers (especially women) consistently rate it safer and more comfortable than Morocco. Morocco is safe from a violent crime perspective, but the persistent tout culture in Marrakech and Fes requires mental preparation and assertiveness."},
            {"question": "Is Petra or Morocco's Sahara Desert better?", "answer": "Completely different experiences — both are extraordinary. Petra is the world's most dramatic ancient city, revealed through a 1.2km canyon; the emotional impact of first seeing the Treasury is something travelers describe as genuinely life-changing. Morocco's Sahara (Erg Chebbi near Merzouga) is the quintessential desert overnight — golden dunes at sunset, Berber camp, camel ride at dawn. Most travelers who've done both say Petra is the more powerful single experience, but the Sahara overnight is magical in a different way."},
            {"question": "How many days do you need in each country?", "answer": "Morocco: minimum 7 days for the classic Marrakech → Fes → Sahara circuit, ideally 10–14. Jordan: minimum 5 days for Amman + Jerash + Dead Sea + Petra + Wadi Rum, ideally 7–9. Jordan's highlights are more geographically compact; Morocco requires more travel time between its diverse regions. Both countries reward slow travel over rushing."},
            {"question": "What's the best time of year to visit Morocco vs Jordan?", "answer": "Both countries share the same ideal travel window: spring (March–May) and autumn (September–November). Summer (June–August) is brutally hot in both countries' inland areas — Marrakech hits 40°C+, Jordan's desert areas hit 40–45°C. October is arguably the single best month for either country; it works well for a combined trip. Morocco's Atlantic coast (Essaouira, Agadir) stays pleasant year-round."},
            {"question": "Is Morocco good for solo female travelers?", "answer": "Morocco is doable but requires more preparation and assertiveness than Jordan. Solo female travelers frequently report persistent unwanted attention in Marrakech and Fes. Dressing conservatively, having a confident manner, and knowing where you're going helps dramatically. Jordan is significantly more comfortable for solo women — the country consistently receives top marks for female solo travel comfort in the MENA region. If in doubt, start with Jordan."},
            {"question": "Which country has better food?", "answer": "Morocco wins clearly on food. Moroccan cuisine — tagines, couscous, pastilla, harira, preserved lemons, Atlantic seafood — is one of the world's great culinary traditions with extraordinary variety. Jordan's food is excellent (mansaf, mezze, falafel, kanafeh) but more limited in scope. For food-first travelers, Morocco is a primary reason to visit."},
            {"question": "Can you visit Morocco and Jordan on the same trip?", "answer": "Yes, but they're not naturally combined — you'll need to fly (typically 5–8 hours with a connection, $100–200 one way). They're geographically in different regions with no overland route. Most travelers visit them on separate trips. A 14–16 day combined itinerary (Marrakech → Fes → Sahara → fly to Amman → Petra → Wadi Rum) is ambitious but very rewarding for travelers with the time and budget."}
        ],

        "ctaHtml": """<div class="cta-section">
<h2>Ready to plan your Morocco or Jordan trip?</h2>
<p>Get a free custom itinerary for Morocco, Jordan, or both — built from real traveler insights, not generic templates. We'll match you with the right pace, cities, and experiences for your travel style.</p>
<a href="https://tabiji.ai/plan" class="cta-button">Plan My Trip →</a>
<p class="cta-sub">Also explore: <a href="/compare/jordan-vs-egypt/">Jordan vs Egypt</a> · <a href="/compare/morocco-vs-egypt/">Morocco vs Egypt</a> · <a href="/compare/portugal-vs-morocco/">Portugal vs Morocco</a></p>
</div>"""
    }
}

Path("compare-data/morocco-vs-jordan.json").write_text(
    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8"
)
print("Written compare-data/morocco-vs-jordan.json")
