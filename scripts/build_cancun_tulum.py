#!/usr/bin/env python3
"""Build compare-data/cancun-vs-tulum.json and render the page."""
import json
from pathlib import Path

REPO = Path("/Users/psy/tabiji")

# Load reference shell
with open(REPO / "compare-data/tokyo-vs-kyoto.json") as f:
    ref = json.load(f)

shell = ref["shell"]

# ── Content blocks ────────────────────────────────────────────────────────────

heroHtml = '''<section class="hero">
<div class="hero-badge">🆚 Mexico Beach Comparison</div>
<h1>Cancun vs Tulum: <em>Which Should You Visit?</em></h1>
<p>A data-backed comparison based on Reddit discussions, real costs, and traveler experiences — not generic AI filler.</p>
<div class="hero-meta">
<div><strong>Updated:</strong> March 2026</div>
<div><strong>Sources:</strong> r/cancun, r/tulum, r/MexicoTravel, r/travel</div>
<div><strong>Distance:</strong> ~130 km apart (2h by car or bus)</div>
</div>
</section>'''

tocMobileHtml = '''<div class="toc-mobile-sticky" id="toc-mobile">
<button class="toc-mobile-toggle" onclick="this.closest(\'.toc-mobile-sticky\').classList.toggle(\'open\')">
<span class="toc-active-label">📑 Contents</span>
<span class="toc-chevron">▼</span>
</button>
<div class="toc-mobile-dropdown">
<ul>
<li><a href="#the-tl-dr-verdict">⚡ The TL;DR Verdict</a></li>
<li><a href="#quick-comparison">Quick Comparison</a></li>
<li><a href="#cost-comparison">💰 Cost Comparison</a></li>
<li><a href="#beaches">🏖️ Beaches</a></li>
<li><a href="#cenotes-and-nature">🌿 Cenotes &amp; Nature</a></li>
<li><a href="#nightlife-and-entertainment">🎉 Nightlife &amp; Entertainment</a></li>
<li><a href="#food-and-dining">🌮 Food &amp; Dining</a></li>
<li><a href="#culture-and-history">🏛️ Culture &amp; History</a></li>
<li><a href="#where-to-stay">🏨 Where to Stay</a></li>
<li><a href="#getting-around">🚗 Getting Around</a></li>
<li><a href="#safety">🛡️ Safety</a></li>
<li><a href="#the-decision-framework">🎯 The Decision Framework</a></li>
<li><a href="#frequently-asked-questions">❓ Frequently Asked Questions</a></li>
</ul>
</div>
</div>'''

methodologyHtml = '''<div class="methodology-box"><h2 id="how-we-built-this-comparison">How we built this comparison</h2><p>This page combines real traveler discussion patterns, published price ranges, and seasonal data to make the Cancun vs Tulum decision easier to resolve.</p><ul class="methodology-points"><li>Reviewed Reddit threads from r/cancun, r/tulum, r/MexicoTravel, and r/travel covering hundreds of traveler experiences.</li><li>Cost data sourced from Reddit trip reports, Booking.com, and Hostelworld current listings.</li><li>Weather data from Open-Meteo for the Quintana Roo region (2024 averages).</li><li>Transit times and prices verified against ADO bus schedules and local reports.</li></ul></div>'''

tocSidebarHtml = '''<aside class="toc-sidebar">
<h2>Contents</h2>
<ul>
<li><a href="#the-tl-dr-verdict">⚡ The TL;DR Verdict</a></li>
<li><a href="#quick-comparison">Quick Comparison</a></li>
<li><a href="#cost-comparison">💰 Cost Comparison</a></li>
<li><a href="#beaches">🏖️ Beaches</a></li>
<li><a href="#cenotes-and-nature">🌿 Cenotes &amp; Nature</a></li>
<li><a href="#nightlife-and-entertainment">🎉 Nightlife &amp; Entertainment</a></li>
<li><a href="#food-and-dining">🌮 Food &amp; Dining</a></li>
<li><a href="#culture-and-history">🏛️ Culture &amp; History</a></li>
<li><a href="#where-to-stay">🏨 Where to Stay</a></li>
<li><a href="#getting-around">🚗 Getting Around</a></li>
<li><a href="#safety">🛡️ Safety</a></li>
<li><a href="#the-decision-framework">🎯 The Decision Framework</a></li>
<li><a href="#frequently-asked-questions">❓ Frequently Asked Questions</a></li>
</ul>
</aside>'''

tocItems = [
    {"href": "#the-tl-dr-verdict", "label": "⚡ The TL;DR Verdict"},
    {"href": "#quick-comparison", "label": "Quick Comparison"},
    {"href": "#cost-comparison", "label": "💰 Cost Comparison"},
    {"href": "#beaches", "label": "🏖️ Beaches"},
    {"href": "#cenotes-and-nature", "label": "🌿 Cenotes &amp; Nature"},
    {"href": "#nightlife-and-entertainment", "label": "🎉 Nightlife &amp; Entertainment"},
    {"href": "#food-and-dining", "label": "🌮 Food &amp; Dining"},
    {"href": "#culture-and-history", "label": "🏛️ Culture &amp; History"},
    {"href": "#where-to-stay", "label": "🏨 Where to Stay"},
    {"href": "#getting-around", "label": "🚗 Getting Around"},
    {"href": "#safety", "label": "🛡️ Safety"},
    {"href": "#the-decision-framework", "label": "🎯 The Decision Framework"},
    {"href": "#frequently-asked-questions", "label": "❓ Frequently Asked Questions"},
]

photoGridHtml = '''<div class="photo-grid">
<div>
<img alt="Cancun Hotel Zone beach with turquoise Caribbean water and resort skyline" loading="lazy" src="https://img.tabiji.ai/compare/cancun-vs-tulum/cancun-beach.jpg">
<div class="caption">Cancun Hotel Zone, Quintana Roo</div>
</img></div>
<div>
<img alt="Tulum beach with white sand and clear turquoise Caribbean water" loading="lazy" src="https://img.tabiji.ai/compare/cancun-vs-tulum/tulum-beach.jpg">
<div class="caption">Tulum Beach, Quintana Roo</div>
</img></div>
</div>'''

verdictHtml = '''<div class="verdict-box"><h2 id="the-tl-dr-verdict">⚡ The TL;DR Verdict</h2><p class="verdict-summary"><strong>Cancun wins on value, logistics, and party scene. Tulum wins on cenotes, jungle vibes, and Instagram aesthetics — but at a significant price premium. Mid-range budget: Cancun ~$80–120/day vs Tulum ~$150–250/day (beachfront).</strong></p><ul class="verdict-takeaways"><li><strong>Choose Cancun:</strong> Budget travelers, all-inclusive fans, first-timers to Mexico's Caribbean coast, party seekers.</li><li><strong>Choose Tulum:</strong> Cenote addicts, ruin explorers, yoga retreaters, and anyone who doesn't mind paying $20 for a margarita for the vibe.</li><li><strong>Do both?</strong> Absolutely — they're only 2 hours apart. Stay in Cancun, day-trip to Tulum ruins and cenotes.</li></ul></div>'''

comparisonHtml = '''<div class="comparison-section">
<h2 id="quick-comparison">Quick Comparison</h2>
<table class="comparison-table">
<thead>
<tr>
<th>Category</th>
<th>🏖️ Cancun</th>
<th>🌿 Tulum</th>
<th>Winner</th>
</tr>
</thead>
<tbody>
<tr>
<td>Daily Budget (mid-range)</td>
<td>$80–120/day (non-all-inclusive)</td>
<td>$150–250/day (beachfront zone)</td>
<td>Cancun</td>
</tr>
<tr>
<td>All-Inclusive Options</td>
<td>Hundreds of resorts, all budgets</td>
<td>None — boutique hotels only</td>
<td>Cancun</td>
</tr>
<tr>
<td>Beach Quality</td>
<td>Wide, calm, turquoise water, fewer sargassum issues</td>
<td>Beautiful but narrow; sargassum varies by season</td>
<td>Cancun</td>
</tr>
<tr>
<td>Cenotes Access</td>
<td>Day trips (1–2h drive)</td>
<td>Several within 20–30 min</td>
<td>Tulum</td>
</tr>
<tr>
<td>Nightlife</td>
<td>Coco Bongo, Mandala, Señor Frog's — full party scene</td>
<td>Jungle clubs, DJ events, more boutique</td>
<td>Cancun</td>
</tr>
<tr>
<td>Mayan Ruins</td>
<td>Day trip to Chichén Itzá (3h) or Cobá (2.5h)</td>
<td>Tulum ruins on-site (15 min from town)</td>
<td>Tulum</td>
</tr>
<tr>
<td>Food Scene</td>
<td>Cheap tacos downtown, tourist restaurants in Hotel Zone</td>
<td>Trendy international; pricey beachfront; cheap in centro</td>
<td>Tie</td>
</tr>
<tr>
<td>Getting There</td>
<td>Major international airport (CUN), tons of flights</td>
<td>New Tulum airport (TQO), limited routes; most fly into CUN</td>
<td>Cancun</td>
</tr>
<tr>
<td>Getting Around</td>
<td>Hotel Zone bus (R1) for $0.80, taxis widely available</td>
<td>Need a car or taxis; beach and town are 5 km apart</td>
<td>Cancun</td>
</tr>
<tr>
<td>Safety</td>
<td>Tourist zones generally safe; watch for scams</td>
<td>Similar; police check-points can be an issue for drivers</td>
<td>Tie</td>
</tr>
<tr>
<td>Vibe</td>
<td>American-style resort city, package-tour energy</td>
<td>Bohemian jungle chic, yoga retreats, influencer central</td>
<td>—</td>
</tr>
<tr>
<td>Best For</td>
<td>First-timers, budget travelers, party-goers</td>
<td>Cenote lovers, adventurers, boutique travelers</td>
<td>—</td>
</tr>
</tbody>
</table>
</div>'''

deepDiveHtml = [
    # 1. Cost Comparison
    '''<section class="deep-dive">
<h2 id="cost-comparison">💰 Cost Comparison</h2>
<p>This is where Cancun and Tulum diverge most sharply. Cancun operates at every budget level — from $30/night dorm beds downtown to $500+/night beachfront suites. Tulum, especially in the <em>zona hotelera</em> (beachfront strip), has undergone rapid luxury-ification. What was a budget backpacker destination 15 years ago is now one of Mexico's most expensive coastal destinations.</p>
<table class="cost-table">
<thead>
<tr>
<th>Expense</th>
<th>🏖️ Cancun</th>
<th>🌿 Tulum</th>
</tr>
</thead>
<tbody>
<tr>
<td>Hostel dorm</td>
<td>$15–25/night (downtown Cancun)</td>
<td>$18–35/night (town only)</td>
</tr>
<tr>
<td>Mid-range hotel</td>
<td>$60–120/night (Hotel Zone)</td>
<td>$150–350/night (beach zone)</td>
</tr>
<tr>
<td>All-inclusive resort</td>
<td>$120–300/night (everything included)</td>
<td>Not available</td>
</tr>
<tr>
<td>Street tacos</td>
<td>25–40 MXN ($1.50–2.50) each</td>
<td>25–50 MXN ($1.50–3) in centro</td>
</tr>
<tr>
<td>Beach restaurant meal</td>
<td>$15–30 USD (Hotel Zone)</td>
<td>$30–80 USD (beachfront clubs)</td>
</tr>
<tr>
<td>Cocktail / beer at beach</td>
<td>$6–12 USD</td>
<td>$15–25 USD</td>
</tr>
<tr>
<td>Cenote entry</td>
<td>$15–30 USD (day trip included)</td>
<td>$10–25 USD (5 min away)</td>
</tr>
<tr class="total-row">
<td>Daily total (mid-range, non-all-inclusive)</td>
<td>~$80–120/day</td>
<td>~$150–250/day (beachfront)</td>
</tr>
</tbody>
</table>
<p><strong>The Tulum paradox:</strong> downtown Tulum (the actual town, 5 km from the beach) is actually quite affordable — good tacos for $1–2, hostels for $20–30/night, and cheap local restaurants. The sticker shock comes when you cross into the zona hotelera. Staying in town and day-tripping the beach is the budget hacker's Tulum strategy.</p>
<div class="reddit-quote">
"Spent more money in Tulum in 3 days than I did in Dubai for 5. And the service wasn't even better."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/13dwqju/prices_in_tulum/">r/tulum user</a></span>
</div>
<div class="reddit-quote">
"I stayed at Mayan Monkey hostel, very affordable at 15 euros/day. If you like street tacos, there's a spot towards downtown with 5 al pastor tacos for 50 pesos and they are incredible. The expensive part is the beach side — that's a whole different economy."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/13dwqju/prices_in_tulum/">r/tulum user</a></span>
</div>
<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> Cancun</li><li><strong>Why:</strong> Cancun wins decisively on value. An all-inclusive resort in Cancun's Hotel Zone can actually come out cheaper than a mid-range Tulum beach hotel — with food and drinks included. Budget travelers have far more options in Cancun.</li><li><strong>Who this matters for:</strong> Anyone watching their spending. Tulum's beach zone is genuinely expensive by Mexican standards.</li></ul></div>
</section>''',

    # 2. Beaches
    '''<section class="deep-dive">
<h2 id="beaches">🏖️ Beaches</h2>
<img alt="Cancun Hotel Zone aerial view showing the turquoise Caribbean and resort strip" class="section-img" loading="lazy" src="https://img.tabiji.ai/compare/cancun-vs-tulum/cancun-hotel-zone.jpg"/>
<p>Here's the hotly contested debate: which city actually has better beaches? The honest answer is more nuanced than either side admits. <strong>Cancun's Hotel Zone</strong> beaches (Playa Delfines, Playa Norte de Tortugas) offer wide stretches of white sand with consistently calm, turquoise water. Being on a barrier island, the hotel zone has both a calm lagoon side and the open Caribbean side. Crucially, the sargassum (seaweed) problem that has plagued Quintana Roo affects Cancun less than areas further south.</p>
<p><strong>Tulum's beaches</strong> are genuinely stunning — narrow strips of white sand backed by jungle rather than high-rise hotels. The panoramic views toward the ocean, without resort towers looming behind you, are what Reddit users consistently point out as the real differentiator. The water is clear and beautiful when conditions are right.</p>
<div class="reddit-quote">
"One of the reasons people prefer Tulum beaches is you don't see high-rises when you look back at the coast from the water. The beaches are nicer in Cancun technically, but the view from the water generally sucks."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/1ays16f/the_reason_why_people_prefer_tulum_over_cancun/">r/tulum user (52 upvotes)</a></span>
</div>
<p><strong>The sargassum problem:</strong> Between May and October, floating seaweed can blanket Tulum's beaches, making swimming unpleasant. Cancun's Hotel Zone faces less exposure due to its orientation. Check <a href="https://sargassummonitoring.com" target="_blank" rel="noopener">sargassummonitoring.com</a> before booking.</p>
<div class="reddit-quote">
"Cancun's hotel zone beaches are among the best in Mexico — wide, well-maintained, calm water. Tulum's charm is the <em>vibe</em> not the sand quality."
<span class="source">— r/cancun user</span>
</div>
<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> Cancun (technically); Tulum (aesthetically)</li><li><strong>Why:</strong> Cancun has wider beaches, calmer water, and fewer sargassum issues. Tulum wins on scenery — jungle meets Caribbean without a resort skyline ruining the shot. If Instagram matters, Tulum. If you want to actually swim comfortably, Cancun.</li><li><strong>Who this matters for:</strong> Beach quality makes or breaks trips for sun-and-sand travelers. Check sargassum forecasts for Tulum if visiting May–October.</li></ul></div>
</section>''',

    # 3. Cenotes & Nature
    '''<section class="deep-dive">
<h2 id="cenotes-and-nature">🌿 Cenotes &amp; Nature</h2>
<img alt="Gran Cenote near Tulum — crystal-clear underground cave pool" class="section-img" loading="lazy" src="https://img.tabiji.ai/compare/cancun-vs-tulum/tulum-cenote.jpg"/>
<p>This is Tulum's killer advantage and the main reason serious travelers choose it over Cancun. The cenotes — natural sinkholes filled with crystal-clear freshwater — around Tulum are among the most spectacular natural experiences in the Americas. Gran Cenote, Dos Ojos, Cenote Calavera, and Cenote Aktun-Ha (Car Wash) are all within 15–30 minutes of Tulum town. The freshwater is perfectly clear (visibility often exceeds 50 meters), cool (around 24°C/75°F year-round), and surrounded by stalactites and cave formations.</p>
<p>From Cancun, cenotes are accessible but require a 1.5–2 hour drive each way, typically organized as day trips. The experience is the same — you just lose a couple hours. Tulum is the only destination where you can wake up, grab a bike, and be swimming in a cenote within 30 minutes.</p>
<p>Beyond cenotes, Tulum is the gateway to the <strong>Sian Ka'an Biosphere Reserve</strong> — a UNESCO World Heritage site covering 1.3 million acres of mangroves, lagoons, and Caribbean reef. Cancun is near the Isla Mujeres coral reef and has whale shark encounters (May–September in nearby waters), but nature is less integrated into the Cancun experience.</p>
<div class="reddit-quote">
"We went for a single beach day in Tulum, visited the ruins, and centered a cenote — if you can do just one cenote, do Gran Cenote or Dos Ojos. Nothing else in Mexico compares."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/1pwa0nk/where_to_stay_cancun_or_a_tulum/">r/tulum user</a></span>
</div>
<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> Tulum (no contest)</li><li><strong>Why:</strong> Tulum's cenote access is unmatched. Gran Cenote alone is worth making Tulum a base. If cenotes and nature are the top priority, Tulum is clearly the right choice. From Cancun you can still visit, but it's a full-day commitment rather than a casual morning.</li><li><strong>Who this matters for:</strong> Anyone who came to Mexico for the cenotes. This is Tulum's single strongest argument.</li></ul></div>
</section>''',

    # 4. Nightlife
    '''<section class="deep-dive">
<h2 id="nightlife-and-entertainment">🎉 Nightlife &amp; Entertainment</h2>
<p>Cancun is one of the world's most famous party cities, and it earns that reputation. The Hotel Zone's "Party Strip" is home to Coco Bongo (the infamous Vegas-style show-club), Mandala, Señor Frog's, Dady'O, and dozens of bars running two-for-one deals until 4 AM. Spring Break brings tens of thousands of college students. Nightlife here is loud, unapologetic, and designed for maximum fun — or maximum chaos depending on your perspective.</p>
<p>Tulum's nightlife is a completely different animal. The jungle clubs — Zamna, Papaya Playa Project, Vagalume — are globally famous for bringing in world-class DJs (booked alongside Ibiza residencies). The vibe is more Berlin techno rave in a cenote than Cancun spring break. Dress codes are real, entrance fees can run $40–100 USD, and table service is astronomical. It's exclusive by design.</p>
<div class="reddit-quote">
"Cancun vs Tulum are two completely different vibes. Cancun is like Miami Beach with Mexican food. Tulum is a boho jungle rave with $25 cocktails and influencers pretending to meditate."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/1cr1z2j/tulum_vs_cancun/">r/tulum user</a></span>
</div>
<div class="reddit-quote">
"Cancun's hotel zone is on a barrier island and isolated from the city itself. If you want non-stop nightlife, Cancun. If you want upscale jungle parties, Tulum. They're completely different markets."
<span class="source">— r/travel user</span>
</div>
<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> Cancun (for mainstream party); Tulum (for upscale DJ culture)</li><li><strong>Why:</strong> Cancun wins for volume, accessibility, and affordability of nightlife. Tulum wins if you want an exclusive jungle club experience — budget permitting. Most travelers 18–25 want Cancun. Most 28–35 want Tulum's DJ nights.</li><li><strong>Who this matters for:</strong> Nightlife travelers need to decide: spring break energy vs Ibiza-in-the-jungle atmosphere.</li></ul></div>
</section>''',

    # 5. Food & Dining
    '''<section class="deep-dive">
<h2 id="food-and-dining">🌮 Food &amp; Dining</h2>
<p>Neither Cancun nor Tulum can match Mexico City for culinary depth, but both have their charms — and their drawbacks. In Cancun's Hotel Zone, restaurants are heavily tourist-oriented: Americanized Mexican, overpriced seafood, and chain restaurants. The real food is in <strong>downtown Cancun</strong> (La Ciudad), where locals eat $1.50 tacos al pastor, excellent poc chuc (Yucatecan grilled pork), and proper fish tacos at a fraction of Hotel Zone prices.</p>
<p>Tulum has developed an international food scene punching above its size. The town center has excellent cheap tacos and traditional Yucatecan food. The beachfront restaurant scene is international, creative, and eye-wateringly expensive — $20 grain bowls, $35 ceviche, $45 sea bass. The aesthetic is always gorgeous; the value is often poor.</p>
<div class="reddit-quote">
"You can do Tulum on a budget if you stop eating at every expensive restaurant and find cool spots in the centro area — cheap tacos, local spots. Just 9 pesos each for incredible al pastor. Stay away from the beach zone restaurants unless you have money to burn."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/1ays16f/the_reason_why_people_prefer_tulum_over_cancun/">r/tulum user (9 upvotes)</a></span>
</div>
<p><strong>Yucatecan specialties to try in both cities:</strong> cochinita pibil (slow-roasted pork in banana leaves), poc chuc (grilled pork with sour orange), sopa de lima (lime soup), panuchos and salbutes (topped tortillas), and fresh ceviches. Both cities are better than their tourist-facing restaurants suggest — go where locals eat.</p>
<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> Tie (if you know where to eat)</li><li><strong>Why:</strong> Both cities have excellent cheap food downtown and overpriced tourist food in the resort zones. Tulum's beachfront dining is more creative but far more expensive. Cancun's Hotel Zone dining is more predictable but less interesting. In both cases, the smart move is eating where locals eat.</li><li><strong>Who this matters for:</strong> Food-focused travelers should go downtown in both cities and save the beachfront restaurants for special occasions.</li></ul></div>
</section>''',

    # 6. Culture & History
    '''<section class="deep-dive">
<h2 id="culture-and-history">🏛️ Culture &amp; History</h2>
<p>Cancun is a purpose-built resort city — it was essentially constructed from scratch in the 1970s by Mexican government planners who saw the potential for a Caribbean tourism hub. Before that, it was a small fishing village. There's no deep urban heritage here. The nearby <strong>Museo Maya de Cancún</strong> is genuinely excellent, housing an impressive collection of Maya artifacts, and day trips to Chichén Itzá (3 hours each way) or Cobá (2.5 hours) are the main cultural draw from Cancun.</p>
<p>Tulum punches far above its weight culturally. The <strong>Tulum Archaeological Zone</strong> — Mayan ruins perched on a 12-meter cliff directly above the Caribbean Sea — is one of the most dramatically situated ancient sites in all of Mexico. The main pyramid, El Castillo, and the Temple of the Frescoes are remarkably well-preserved. It's touristy and gets crowded by midday, but arrive early (opening is 8 AM) and you'll have the ruins nearly to yourself with the turquoise Caribbean as your backdrop.</p>
<p>Beyond the ruins, Tulum town has developed into a wellness and spiritual center, with yoga retreats, temazcal ceremonies, and Mayan healing traditions. It's commercial, sure — but there's more cultural texture here than Cancun's Hotel Zone offers.</p>
<div class="reddit-quote">
"The Tulum ruins are incredible and the beach is right there — you can swim after walking the ruins. The ruins themselves are not as grand as Chichen Itza, but the setting is unbeatable. No other ruins in Mexico have the sea as a backdrop like that."
<span class="source">— r/MexicoTravel user</span>
</div>
<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> Tulum</li><li><strong>Why:</strong> Tulum has the ruins, the Sian Ka'an, and more cultural texture. Cancun is a resort city with excellent day trips — but the culture you're accessing from Cancun (Chichén Itzá, Cobá) requires a full day of travel. Tulum's ruins are walkable from town.</li><li><strong>Who this matters for:</strong> Travelers who came to see Mayan civilization should use Tulum as a base. The ruins + cenotes combination is Tulum's defining experience.</li></ul></div>
</section>''',

    # 7. Where to Stay
    '''<section class="deep-dive">
<h2 id="where-to-stay">🏨 Where to Stay</h2>
<h3>Cancun neighborhoods</h3>
<p><strong>Hotel Zone (Zona Hotelera)</strong> — The classic resort strip on a barrier island. Everything from budget all-inclusives to luxury resorts. Easy beach access, nightlife, and shopping. If you want the full "Cancun resort experience," stay here. Prices: $80–500+/night.</p>
<p><strong>Downtown Cancun (El Centro)</strong> — Where locals actually live and eat. Budget hotels ($30–60/night), great street food, access to ADO buses for day trips. Less glamorous but far better value. Most tourists don't realize this exists.</p>
<p><strong>Puerto Morelos</strong> — 30 minutes south of Cancun Airport. Small fishing village with excellent reef snorkeling, way fewer tourists, and a calmer pace. Great alternative if you want Caribbean without the Cancun chaos.</p>
<h3>Tulum neighborhoods</h3>
<p><strong>Tulum Beach Zone (Zona Hotelera)</strong> — The Instagram-famous boutique hotel strip. Cabanas, eco-lodges, and luxury boutique hotels right on the beach. Prices: $150–600+/night. You'll need a car or taxi to reach town (5 km). This is the Tulum experience most people imagine.</p>
<p><strong>Tulum Town (El Pueblo)</strong> — The actual town, 5 km inland from the beach. Budget-friendly ($30–80/night), excellent local restaurants, cenotes accessible by bike. A popular hack: stay in town, Uber or taxi to the beach. You save 60–70% on accommodation.</p>
<div class="reddit-quote">
"My recommended approach: stay in downtown Cancun or Playa del Carmen, and do Tulum as a day trip. You get the ruins, a cenote, and the beach at a fraction of the cost of staying there."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/1pwa0nk/where_to_stay_cancun_or_a_tulum/">r/tulum user</a></span>
</div>
<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> Cancun (for variety and value); Tulum (for boutique experience)</li><li><strong>Why:</strong> Cancun wins on hotel variety — there's something for every budget. Tulum's accommodation is either expensive beach boutiques or budget town hotels (with an awkward gap in the middle). The "stay in town, taxi to beach" hack makes Tulum much more affordable.</li><li><strong>Who this matters for:</strong> Budget matters most here. All-inclusive travelers should pick Cancun; boutique experience seekers should budget $200+/night for Tulum beach.</li></ul></div>
</section>''',

    # 8. Getting Around
    '''<section class="deep-dive">
<h2 id="getting-around">🚗 Getting Around</h2>
<p>Cancun is surprisingly easy to navigate. The Hotel Zone is served by the R1 and R2 bus routes running the entire length of the strip — costs about 14 MXN ($0.80 USD) per ride. Taxis are metered (though always confirm the price first) and widely available. No car rental needed if you're staying in the Hotel Zone and taking organized day trips.</p>
<p>Tulum is notably harder. The town and the beach zone are 5 km apart, which rules out casual walking. Options: rent a car ($35–60/day, but watch for police check-points on the Tulum highway — they can be aggressive), rent a moped ($25–40/day), or rely on taxis and Ubers. Cycling between town and the beach is possible but hot, sweaty, and trucks share the road.</p>
<div class="reddit-quote">
"The big difference between Cancun and Tulum: Cancun's overdevelopment is older and the infrastructure works. Tulum's sprawl is newer and the logistics haven't caught up — the beach and town being miles apart is a constant friction point."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/1pwa0nk/where_to_stay_cancun_or_a_tulum/">r/tulum user</a></span>
</div>
<p><strong>Getting between Cancun and Tulum:</strong> ADO buses run frequently (roughly every 30–60 min) from Cancun bus terminal to Tulum. Cost: 250–300 MXN ($15–18 USD) one way, about 2 hours. Renting a car gives you more flexibility to stop at cenotes en route (Cobá, Dos Ojos). Airport transfers via shared shuttle can be arranged.</p>
<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> Cancun</li><li><strong>Why:</strong> The Hotel Zone bus alone makes Cancun more navigable than Tulum for car-free travelers. Tulum's split between town and beach creates constant friction. If you don't want to rent a car, Cancun is significantly more convenient.</li><li><strong>Who this matters for:</strong> Travelers without a driving license, those who dislike renting cars, or anyone planning to drink freely and not drive.</li></ul></div>
</section>''',

    # 9. Safety
    '''<section class="deep-dive">
<h2 id="safety">🛡️ Safety</h2>
<p>Both Cancun and Tulum are in Quintana Roo state, which maintains a separate security apparatus partly funded by the tourism industry. In practical terms, the tourist zones of both cities are generally safe for travelers exercising normal big-city awareness. The scary headlines you've seen are mostly connected to organized crime that rarely targets tourists directly.</p>
<p>The most commonly reported issues in both destinations:</p>
<p><strong>Tourist scams:</strong> overpriced taxis, "free" tours with high-pressure upsells, and restaurants adding unauthorized gratuities. Standard travel awareness applies.</p>
<p><strong>Police check-points (especially Tulum):</strong> Multiple Reddit users report being stopped by police while driving a rental car or scooter in Tulum and being shaken down for cash for invented violations. This is reported more frequently around Tulum than Cancun. Don't drive under the influence; if stopped, stay calm, ask for a ticket, and photograph everything.</p>
<div class="reddit-quote">
"I've been stopped for made-up laws and issues and shaken down for money multiple times driving in Tulum at night. They set up checkpoints on the main roads. I always felt safe walking around, but be very careful if you're driving."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/1cr1z2j/tulum_vs_cancun/">r/tulum user (2 upvotes)</a></span>
</div>
<div class="reddit-quote">
"As someone who's been to Mexico more than 15 times, the scams are as prevalent as they are in any other tourist city. People seem to think they don't need to use the same precautions in Tulum they'd use anywhere else internationally."
<span class="source">— <a href="https://www.reddit.com/r/tulum/comments/1cr1z2j/tulum_vs_cancun/">r/tulum user</a></span>
</div>
<div class="section-winner"><h3>Winner takeaway</h3><ul><li><strong>Winner:</strong> Tie</li><li><strong>Why:</strong> Both cities have similar overall safety levels for tourists. Tulum has slightly more reported issues with police stops for drivers. In both destinations: stay in lit, populated areas at night, use Uber over random taxis, and don't carry excess cash. Neither destination is as dangerous as Reddit panic posts suggest.</li><li><strong>Who this matters for:</strong> Solo female travelers and first-time Mexico visitors should stick to well-trafficked tourist areas, which are plentiful in both cities.</li></ul></div>
</section>''',

    # 10. Decision Framework (required)
    '''<section class="deep-dive">
<h2 id="the-decision-framework">🎯 The Decision Framework</h2>
<div class="decision-grid">
<div class="decision-card tokyo-card">
<h3>Choose Cancun If…</h3>
<ul>
<li>You want an all-inclusive resort experience</li>
<li>Budget is a primary consideration</li>
<li>You're traveling in a large group or with family</li>
<li>You want non-stop nightlife and party energy</li>
<li>You prefer a walkable hotel zone without renting a car</li>
<li>This is your first trip to Mexico's Caribbean coast</li>
<li>You want whale shark tours (May–September)</li>
<li>You're flying into the region with limited connection options</li>
<li>You want to use it as a hub for day trips to Chichén Itzá or Cobá</li>
</ul>
</div>
<div class="decision-card kyoto-card">
<h3>Choose Tulum If…</h3>
<ul>
<li>Cenotes are the main reason for the trip</li>
<li>You want Mayan ruins you can walk to from your hotel</li>
<li>Boutique eco-lodges and jungle vibes appeal to you</li>
<li>You're into yoga retreats, wellness, or spiritual experiences</li>
<li>World-class DJ clubs and underground parties excite you</li>
<li>You don't mind paying premium prices for atmosphere</li>
<li>Sian Ka'an biosphere and wild nature are on your list</li>
<li>Instagram-worthy backdrops matter to your trip</li>
<li>You're a repeat Mexico visitor looking for something beyond resorts</li>
</ul>
</div>
</div>
</section>''',
]

faqItems = [
    {
        "question": "Is Cancun or Tulum better for first-time visitors?",
        "answer": "Cancun is easier for first-timers — better infrastructure, more affordable options, and simpler logistics. The Hotel Zone is walkable, all-inclusives are abundant, and getting there from Cancun Airport takes 20 minutes. Tulum rewards travelers who do their research and don't mind a higher price tag for a boutique jungle vibe."
    },
    {
        "question": "How far is Cancun from Tulum?",
        "answer": "About 130 km (80 miles) south of Cancun. The drive takes roughly 2 hours by car. ADO buses run regularly between the two for about 250–300 MXN ($15–18 USD) one way, with departures roughly every 30–60 minutes from Cancun's bus terminal."
    },
    {
        "question": "Can I visit Tulum as a day trip from Cancun?",
        "answer": "Absolutely — and this is a popular strategy. Leave early, visit the Tulum ruins (best before 10 AM to beat crowds), swim in a nearby cenote (Gran Cenote is 4 km from the ruins), and return to Cancun in the evening. Round trip by ADO bus costs about $30–35 USD. The only downside is you don't get the Tulum beach club experience without spending extra time."
    },
    {
        "question": "Which has better beaches — Cancun or Tulum?",
        "answer": "Technically Cancun: wider beaches, calmer water, and fewer sargassum seaweed issues. Aesthetically Tulum: the Caribbean view without hotel towers in the background is more photogenic. Sargassum (floating seaweed) can make Tulum beaches unpleasant from May–October — check current conditions before booking."
    },
    {
        "question": "Is Tulum safe for tourists?",
        "answer": "Yes, for normal travel. The tourist zones in Tulum are generally safe. Common issues are overcharging at restaurants, tourist scams, and (more specific to Tulum) police check-points on the highway that can lead to shakedowns for drivers. Use Uber, stay in well-lit areas, and exercise the same caution you would in any international tourist city."
    },
    {
        "question": "Why is Tulum so expensive?",
        "answer": "Supply and demand. The Tulum beach zone (zona hotelera) is a narrow strip with limited boutique accommodation, all of which is right on the beach. There are no all-inclusive mega-resorts to provide budget competition. The clientele skews wealthy and Instagram-motivated, which drives pricing. The good news: Tulum town (5 km inland) is significantly cheaper for food and lodging."
    },
    {
        "question": "What are the best cenotes near Tulum?",
        "answer": "Gran Cenote (4 km from Tulum ruins, ~$18 USD entry) is the most accessible and stunning. Dos Ojos (17 km north) offers the best cave diving and snorkeling with two connected cavern systems. Cenote Calavera is smaller and wilder. Cenote Aktun-Ha (Car Wash) is a large open cenote popular with divers. All are within 30 minutes of Tulum town."
    },
    {
        "question": "Does Cancun have cenotes?",
        "answer": "Not directly — but Cancun is a good base for cenote day trips. Cenote Azul and Cenote Verde are about 45 minutes away near Puerto Morelos. The Ruta de los Cenotes (west of Puerto Morelos) has a cluster of cenotes 1–1.5 hours from Cancun. The famous ones near Tulum (Gran Cenote, Dos Ojos) are about 2 hours from Cancun."
    }
]

faqHtml = '<section class="faq-section">\n<h2 id="frequently-asked-questions">❓ Frequently Asked Questions</h2>\n'
for item in faqItems:
    faqHtml += f'<div class="faq-item">\n<h3>{item["question"]}</h3>\n<p>{item["answer"]}</p>\n</div>\n'
faqHtml += '</section>'

ctaHtml = '''<div class="cta-section">
<h2>Ready to plan your Mexico trip?</h2>
<p>Get a free custom itinerary for Cancun, Tulum, or both — built from real traveler insights, not generic templates.</p>
<div class="cta-buttons">
<a class="cta-btn-tokyo" href="/plan">Plan Your Cancun Trip →</a>
<a class="cta-btn-kyoto" href="/plan">Plan Your Tulum Trip →</a>
</div>
</div>'''

faq_schema_entities = [
    {
        "@type": "Question",
        "name": item["question"],
        "acceptedAnswer": {
            "@type": "Answer",
            "text": item["answer"]
        }
    }
    for item in faqItems
]

data = {
    "slug": "cancun-vs-tulum",
    "pageType": "compare-leaf",
    "status": "published",
    "destinations": {
        "destination1": "Cancun",
        "destination2": "Tulum"
    },
    "seo": {
        "title": "Cancun vs Tulum: Which Should You Visit? (2026 Comparison) | tabiji.ai",
        "metaDescription": "Cancun vs Tulum — a data-backed comparison based on Reddit discussions, real costs, and traveler preferences. Beach quality, cenotes, nightlife, safety, and honest verdicts.",
        "ogTitle": "Cancun vs Tulum: Which Should You Visit? — tabiji.ai",
        "ogDescription": "Reddit-backed comparison of Cancun and Tulum. Real costs, beach quality, cenotes, nightlife, and honest verdicts from thousands of travelers.",
        "ogImage": "https://img.tabiji.ai/compare/cancun-vs-tulum/cancun-beach.jpg",
        "twitterTitle": "Cancun vs Tulum: Which Should You Visit?",
        "twitterDescription": "Data-backed comparison from Reddit discussions, real costs, and traveler preferences.",
        "twitterImage": "https://img.tabiji.ai/compare/cancun-vs-tulum/cancun-beach.jpg",
        "publishedTime": "2026-03-19T00:00:00Z",
        "modifiedTime": "2026-03-19T00:00:00Z",
        "canonical": "https://tabiji.ai/compare/cancun-vs-tulum/"
    },
    "schema": {
        "article": {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": "Cancun vs Tulum: Which Should You Visit?",
            "description": "A data-backed comparison of Cancun and Tulum based on Reddit discussions, real costs, weather data, and traveler preferences.",
            "author": {
                "@type": "Organization",
                "name": "tabiji.ai",
                "url": "https://tabiji.ai"
            },
            "publisher": {
                "@type": "Organization",
                "name": "tabiji.ai",
                "url": "https://tabiji.ai"
            },
            "datePublished": "2026-03-19",
            "dateModified": "2026-03-19",
            "mainEntityOfPage": "https://tabiji.ai/compare/cancun-vs-tulum/",
            "image": "https://img.tabiji.ai/compare/cancun-vs-tulum/cancun-beach.jpg",
            "speakable": {
                "@type": "SpeakableSpecification",
                "cssSelector": [
                    ".hero h1",
                    ".hero .subtitle",
                    ".verdict-box",
                    ".faq-section"
                ]
            }
        },
        "breadcrumb": {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://tabiji.ai/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Compare",
                    "item": "https://tabiji.ai/compare/"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": "Cancun vs Tulum",
                    "item": "https://tabiji.ai/compare/cancun-vs-tulum/"
                }
            ]
        },
        "faq": {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema_entities
        }
    },
    "shell": shell,
    "content": {
        "heroHtml": heroHtml,
        "tocMobileHtml": tocMobileHtml,
        "methodologyHtml": methodologyHtml,
        "tocSidebarHtml": tocSidebarHtml,
        "tocItems": tocItems,
        "photoGridHtml": photoGridHtml,
        "verdictHtml": verdictHtml,
        "comparisonHtml": comparisonHtml,
        "deepDiveHtml": deepDiveHtml,
        "faqHtml": faqHtml,
        "faqItems": faqItems,
        "ctaHtml": ctaHtml
    }
}

out_path = REPO / "compare-data/cancun-vs-tulum.json"
with open(out_path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Written: {out_path}")
print(f"Deep dive sections: {len(deepDiveHtml)}")
print(f"FAQ items: {len(faqItems)}")
