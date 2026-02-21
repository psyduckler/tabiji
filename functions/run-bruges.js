const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1771633962141_3ntibd",
  email: "psyduckler@gmail.com",
  destination: "Bruges, Belgium",
  start_date: "2026-06-24",
  end_date: "2026-06-28",
  group_size: "1",
  travel_style: "Cultural",
  dining: "",
  budget: "",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-21T00:32:42.141Z",
  status: "pending"
};

const itineraryData = {
  destination: "Bruges, Belgium",
  countryEmoji: "🇧🇪",
  title: "Bruges in 4 Nights: Medieval Masterpieces & Belgian Bliss",
  subtitle: "Canals → Flemish Art → Chocolate → Beer → Belfry Bells",
  description: "A solo cultural pilgrimage through one of Europe's best-preserved medieval cities. Bruges is a UNESCO World Heritage site where every cobblestoned lane reveals Gothic architecture, world-class Flemish Primitives, legendary chocolatiers, and Trappist beer. Late June means long golden evenings, fewer crowds than July-August, and the canals at their most photogenic.",
  duration: "4 nights / 5 days",
  dates: "Jun 24 – 28, 2026",
  budget: "Flexible",
  pace: "Relaxed — wander, linger, savor",
  bestFor: "Solo culture lovers, art enthusiasts & food explorers",
  highlights: [
    "Markt & Belfry — climb 366 steps for panoramic views over medieval rooftops",
    "Groeningemuseum — Van Eyck's Madonna with Canon van der Paele & Memling masterpieces",
    "Basilica of the Holy Blood — 12th-century relic chapel, one of Europe's most sacred",
    "Canal boat tour — glide under medieval bridges at golden hour",
    "De Halve Maan brewery tour & 't Brugs Beertje's 300+ Belgian bottles",
    "Belgian chocolate trail — The Chocolate Line, Dumon, and Sukerbuyc",
    "Begijnhof — serene 13th-century beguinage with daffodil gardens",
    "Sint-Janshospitaal — Memling's shrine of St. Ursula in a medieval hospital",
    "Minnewater (Lake of Love) — sunset stroll with swans",
    "Day trip to Ghent — Van Eyck's Ghent Altarpiece, the most important painting in European art"
  ],
  essentials: [
    { title: "🚆 Getting There", text: "Direct trains from Brussels (1h, €15), Ghent (25min), or Brussels Airport (1h15). Bruges station is a 15-minute walk to the center. The city is tiny and entirely walkable — no transit needed once you arrive. Rent a bike from Fietspunt at the station for canal-side day trips." },
    { title: "💵 Budget Reality", text: "Bruges is mid-range for Western Europe. Lunch: €12-20. Dinner: €25-45. Museum entry: €8-14. Beer in a café: €4-6. Chocolate: free tastings everywhere, boxes €10-25. Budget €80-120/day beyond accommodation. The Musea Brugge card (€30) covers 16 museums for 72 hours — essential for cultural trips." },
    { title: "🌤️ Late June Weather", text: "Expect 15-22°C with long daylight (sunrise 5:30, sunset 22:00). Pack layers — mornings can be cool, afternoons warm. Rain is always possible in Belgium, so bring a light waterproof jacket. The extended evening light makes canal walks magical." },
    { title: "🏨 Where to Stay", text: "Stay inside the egg-shaped old city. Near the Markt: most central, lively. Near 't Zand: slightly quieter, close to the station. Sint-Anna quarter: peaceful, authentic neighborhood feel. Budget: Snuffel Hostel. Mid-range: Hotel Adornes (canal-side charm) or Hotel Jan Brito (historic center)." },
    { title: "🍫 Chocolate Protocol", text: "Skip the tourist shops on Markt. The Chocolate Line (Dominique Persoone) does wild flavors like wasabi and tobacco. Dumon is classic and traditional. Sukerbuyc near the Burg does beautiful pralines. Visit Choco-Story museum for the full bean-to-bar journey." },
    { title: "🍺 Beer Guide", text: "De Halve Maan is the only active city-center brewery — tour + tasting is €16. For serious exploration: 't Brugs Beertje (300+ bottles), Le Trappiste (13th-century basement bar), and Café Vlissinghe (oldest pub in Bruges, since 1515). Try Brugse Zot (local blonde) and Straffe Hendrik (local quad)." }
  ],
  days: [
    {
      num: 1,
      title: "Arrival & the Medieval Heart",
      neighborhoods: "Markt · Burg · City Center",
      date: "Jun 24",
      mapPins: [
        { lat: 51.2093, lng: 3.2247, label: "Markt (Market Square)", num: 1, cat: "activity", desc: "Iconic central square with the Belfry and guild houses" },
        { lat: 51.2082, lng: 3.2271, label: "Burg Square", num: 2, cat: "activity", desc: "City Hall, Basilica of the Holy Blood" },
        { lat: 51.2087, lng: 3.2269, label: "Basilica of the Holy Blood", num: 3, cat: "activity", desc: "12th-century chapel with venerated relic" },
        { lat: 51.2093, lng: 3.2247, label: "Belfry of Bruges", num: 4, cat: "activity", desc: "366 steps, 83m tower, panoramic views" },
        { lat: 51.2065, lng: 3.2270, label: "Rozenhoedkaai", num: 5, cat: "activity", desc: "Most photographed spot in Bruges" },
        { lat: 51.2096, lng: 3.2258, label: "Café Craenenburg", num: 6, cat: "food", desc: "Historic terrace on the Markt" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive & Settle In", description: "Drop bags, grab a city map, orient yourself. Bruges' old city is egg-shaped and compact — everything you'll visit is within a 15-minute walk. The streets are cobblestoned and slightly confusing by design (medieval cities weren't built on grids), but getting lost is half the charm.", details: ["💡 If arriving by train, walk north along Zuidzandstraat toward the Markt — it's the most direct route and you'll pass through the main shopping street."] },
            { title: "Belfry of Bruges", description: "Start at the absolute heart. The Belfry dominates the Markt — 83 meters of medieval engineering built between the 13th and 15th centuries. Climb the 366 narrow, spiraling stone steps (the staircase gets tighter as you go up). At the top: panoramic views over every red rooftop in the city, the canal network, and on clear days, the North Sea coast 15km away. The 47-bell carillon plays every quarter hour — if you're at the top during a chime, it's thunderous and thrilling.", details: ["📍 Markt Square · €14 entry · Last entry 45 min before closing", "💡 Go mid-afternoon to avoid morning tour groups. The narrow staircase means one-way flow — be ready for a workout."] },
            { title: "Burg Square & Basilica of the Holy Blood", description: "Duck through the narrow passage from the Markt to the Burg — Bruges' other main square, more intimate and arguably more beautiful. The Town Hall (1376) is one of the oldest in the Low Countries. The star is the Basilica of the Holy Blood: the lower chapel is pure 12th-century Romanesque — dark, moody, ancient stone, barely changed in 900 years. The upper chapel is ornate Neo-Gothic housing a relic believed to contain Christ's blood, brought back from the Crusades.", details: ["📍 Free entry to basilica, €2.50 for the treasury museum", "💡 The lower chapel is easily missed — look for the small door to the left. It's the most atmospheric space in Bruges."] }
          ],
          meals: [
            { type: "☕ Arrival Snack", name: "Café Craenenburg", description: "Historic terrace café right on the Markt — grab a first Belgian beer (try a Brugse Zot blonde, brewed two blocks away) and people-watch as the Belfry towers above you. This is your 'I'm in Bruges' moment.", meta: "€5-8 · Markt Square · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Buy the Musea Brugge card (€30, 72 hours) on your first museum visit — it covers 16 museums and pays for itself after just 3." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Rozenhoedkaai at Golden Hour", description: "Walk to Rozenhoedkaai — the most photographed spot in Bruges. The canal bends here under ancient trees with a perfect view of the Belfry reflected in the water. In late June, golden hour lasts until nearly 10pm. This is your first jaw-drop canal moment.", details: ["💡 Come back here at different times of day — the light is completely different each time."] },
            { title: "Flemish Dinner at De Stove", description: "Tiny, family-run restaurant beloved by locals. Only 20 seats, so book ahead. Try the waterzooi (Flanders' national dish — a creamy chicken or fish stew) or stoofvlees (Flemish beef stew braised in dark Belgian beer). Honest cooking, reasonable prices, zero pretension.", details: ["📍 Kleine Sint-Amandsstraat 4 · €25-35 mains · Reserve ahead"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "De Stove", description: "Classic Flemish home cooking in a room smaller than your apartment. The waterzooi is the move — creamy, comforting, and deeply Flemish. Pair with a local beer. This is the kind of place where the chef comes out to say hello.", meta: "€25-35 · Book ahead · Only 20 seats" }
          ],
          tips: [{ type: "reddit", text: "De Stove is one of the few restaurants in Bruges that locals actually eat at. Skip the Markt tourist traps — they're all mediocre and overpriced.", cite: "r/belgium" }]
        },
        {
          label: "Late Night",
          activities: [
            { title: "Markt at Night", description: "Come back to the Markt after dinner. The guild houses are lit up golden, the Belfry glows against the dark sky, and the tourist crowds have melted away. Grab a nightcap at a terrace and watch the square transform. Late June evenings stay light until 10pm, and the twilight is surreal.", details: [] }
          ],
          meals: [],
          tips: []
        }
      ]
    },
    {
      num: 2,
      title: "Flemish Masters & Canal Magic",
      neighborhoods: "Museum Quarter · Dijver Canal · Begijnhof",
      date: "Jun 25",
      mapPins: [
        { lat: 51.2050, lng: 3.2265, label: "Groeningemuseum", num: 1, cat: "activity", desc: "Flemish Primitives — Van Eyck, Memling, Bosch" },
        { lat: 51.2043, lng: 3.2256, label: "Sint-Janshospitaal", num: 2, cat: "activity", desc: "Medieval hospital with Memling works" },
        { lat: 51.2037, lng: 3.2235, label: "Onze-Lieve-Vrouwekerk", num: 3, cat: "activity", desc: "Michelangelo's Madonna and Child" },
        { lat: 51.2015, lng: 3.2245, label: "Begijnhof", num: 4, cat: "activity", desc: "13th-century walled beguinage" },
        { lat: 51.2005, lng: 3.2240, label: "Minnewater", num: 5, cat: "activity", desc: "Lake of Love — swans and willows" },
        { lat: 51.2062, lng: 3.2275, label: "Canal Boat Departure", num: 6, cat: "activity", desc: "30 min tour, €12" },
        { lat: 51.2060, lng: 3.2300, label: "De Halve Maan Brewery", num: 7, cat: "food", desc: "Only active Bruges city-center brewery" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Groeningemuseum", description: "The jewel of Bruges' cultural scene. Small but world-class — this is where you come face-to-face with the Flemish Primitives. Van Eyck's Madonna with Canon van der Paele (1436) is the centerpiece — the level of detail is insane. You can see individual hairs in the fur collar, the reflection of a window in an armor breastplate, and every wrinkle on the canon's aged face. This is the birth of oil painting technique. Also here: Memling's Moreel Triptych, a haunting Bosch Last Judgement panel, and Provost's misericordia scene. Allow 90 minutes minimum.", details: ["📍 Dijver 12 · €14 (included in Musea Brugge card) · Opens 9:30", "💡 Go when it opens at 9:30 — the small rooms get crowded. Ask at the desk about any temporary exhibitions."] },
            { title: "Sint-Janshospitaal & Memling Museum", description: "Right next door. A medieval hospital in use from the 12th to 19th century, now housing Hans Memling's greatest works. The Shrine of St. Ursula is a tiny wooden reliquary painted with impossibly intricate scenes — it's one of the most remarkable artworks you'll ever see. The hospital wards themselves are atmospheric — massive oak-beamed halls where the sick were treated for 700 years.", details: ["📍 Mariastraat 38 · €14 · Combined visits work well with Groeninge"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "That's Toast", description: "Specialty coffee and creative breakfast near 't Zand. Good avocado toast, pastries, and strong flat whites. Sets you up for a museum morning.", meta: "€8-14 · Near 't Zand · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Van Eyck essentially invented modern oil painting technique in the 1430s, right here in Bruges. The Groeningemuseum is where you understand why — the detail and luminosity of these 600-year-old paintings makes most modern art look rushed." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Church of Our Lady (Onze-Lieve-Vrouwekerk)", description: "The 115m brick tower is the tallest in Belgium and the second tallest brick tower in the world. Inside: Michelangelo's Madonna and Child (1504) — the only Michelangelo sculpture to leave Italy during his lifetime. It was bought by a Bruges merchant and shipped here. It's smaller than you'd expect but impossibly delicate — the way the Virgin's hand drapes over the Christ child is Michelangelo at his most tender. The Burgundian tombs of Charles the Bold and Mary of Burgundy are elaborately decorated and historically significant.", details: ["📍 Mariastraat · €7 for the art section · The nave is free"] },
            { title: "Begijnhof & Minnewater", description: "Walk through the white gates into another century. The Begijnhof (Beguinage) was founded in 1245 as a community for beguines — pious women who weren't nuns but lived communally. Today Benedictine nuns live here. White-washed houses surround a green courtyard with tall trees. Silence is requested and deeply felt. Continue south to Minnewater — the Lake of Love, where swans glide across still water and willow trees drape the banks. Legend says that if you cross the bridge with your beloved, you'll love forever. Solo? Cross it anyway.", details: ["📍 Free entry · The small Begijnhof house museum is €2", "💡 Best in late afternoon when the light hits the white facades."] },
            { title: "Canal Boat Tour", description: "Board at Dijver landing. The 30-minute boat ride shows you Bruges from water level — perspectives you can't get from the streets. Medieval brick facades, secret gardens hidden behind walls, low stone bridges you duck under, and the iconic view back at the Belfry. Late afternoon light turns the brick golden.", details: ["📍 Dijver canal · €12, no reservation needed · Boats every 10 min", "💡 Sit at the back of the boat for the best photo angles."] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "De Belegde Boterham", description: "No-frills sandwich shop beloved by locals. Massive open-faced sandwiches on thick bread with creative toppings — smoked salmon, brie and walnut, shrimp croquette. Cheap, cheerful, delicious. The kind of place where you sit at a communal table and eat something simple and perfect.", meta: "€8-12 · Kleine Sint-Amandsstraat · Walk-in" }
          ],
          tips: [{ type: "reddit", text: "The canal tour is absolutely worth it — you see a completely different city from the water. Rozenhoedkaai from the boat is the money shot.", cite: "r/travel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "De Halve Maan Brewery Tour", description: "The only active brewery still operating within Bruges' medieval center. The 45-minute tour covers brewing history and process, climbs through the building, and ends on the rooftop terrace with panoramic city views and a glass of Brugse Zot blonde. Fun fact: in 2016 they built a 3.2km underground beer pipeline to transport beer to their bottling plant outside the city — because trucks were damaging the cobblestones.", details: ["📍 Walplein 26 · €16 with tasting · Book online, tours fill up", "💡 The last tour of the day is usually less crowded."] },
            { title: "Beer-Paired Dinner at Den Dyver", description: "Unique concept — every single dish on the menu is cooked with Belgian beer and paired with a matching brew. The chef creates seasonal menus around different beer styles. Rabbit braised in kriek (cherry beer), beef cheek in Westmalle Dubbel, chocolate mousse with Chimay Blue. It's a cultural experience disguised as dinner.", details: ["📍 Dijver 5 · €35-50 for mains with pairing · Reserve ahead"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Den Dyver", description: "Beer cuisine at its finest. Every dish is cooked with and paired to a specific Belgian beer. The sommelier is actually a 'biersommelier' — they'll walk you through the pairings with genuine passion. The canal-side location on the Dijver doesn't hurt either.", meta: "€35-50 · Dijver 5 · Reservations recommended" }
          ],
          tips: [{ type: "reddit", text: "Den Dyver is where you go to understand why Belgium takes beer as seriously as France takes wine. The beer pairings aren't gimmicky — they genuinely elevate the food.", cite: "r/beer" }]
        }
      ]
    },
    {
      num: 3,
      title: "Chocolate, Lace & Hidden Bruges",
      neighborhoods: "Sint-Anna Quarter · Langestraat · Northeast Bruges",
      date: "Jun 26",
      mapPins: [
        { lat: 51.2130, lng: 3.2305, label: "The Chocolate Line", num: 1, cat: "food", desc: "Dominique Persoone's avant-garde chocolate shop" },
        { lat: 51.2140, lng: 3.2340, label: "Kantcentrum (Lace Centre)", num: 2, cat: "activity", desc: "Live bobbin lace demonstrations" },
        { lat: 51.2155, lng: 3.2350, label: "Jerusalem Chapel", num: 3, cat: "activity", desc: "15th-century replica of the Holy Sepulchre" },
        { lat: 51.2120, lng: 3.2330, label: "Sint-Annakerk", num: 4, cat: "activity", desc: "Hidden Baroque interior" },
        { lat: 51.2108, lng: 3.2370, label: "Café Vlissinghe", num: 5, cat: "food", desc: "Oldest pub in Bruges since 1515" },
        { lat: 51.2160, lng: 3.2290, label: "Choco-Story Museum", num: 6, cat: "activity", desc: "4,000 years of chocolate history" },
        { lat: 51.2100, lng: 3.2310, label: "Dumon Chocolatier", num: 7, cat: "food", desc: "Traditional Belgian pralines" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "The Chocolate Line", description: "Start your day at Dominique Persoone's shop on Simon Stevinplein. Belgium's most famous (and most iconoclastic) chocolatier — his flavors include wasabi, Havana cigar, cola, bacon, and Thai chili. He invented a chocolate-snorting device that debuted at a Rolling Stones party. Behind the theatrical branding is genuine mastery — the ganaches are silky, the flavor balance is precise, and the presentation is art. Buy a mixed box of his signature pralines.", details: ["📍 Simon Stevinplein 19 · €15-25 for a box", "💡 Ask for a tasting — they're generous and it helps you pick."] },
            { title: "Choco-Story Museum", description: "Three floors covering 4,000 years of chocolate history — from Aztec xocolatl drinking rituals to Belgian praline innovation. Includes original molds, historic equipment, and the full bean-to-bar process. Live praline-making demonstration at the end with free tastings. Good context before hitting more shops later.", details: ["📍 Wijnzakstraat 2 · €11 entry"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Le Pain Quotidien", description: "Belgian bakery chain that started in Brussels — communal tables, organic bread, thick tartines with jam. The perfect low-key start before a chocolate-heavy morning.", meta: "€8-12 · Multiple locations · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Bruges has over 50 chocolate shops. Most on the Markt are tourist-grade. The three worth your time: The Chocolate Line (avant-garde), Dumon (classic), and Sukerbuyc (artisan). Quality over quantity." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Sint-Anna Quarter", description: "Cross into Bruges' quiet northeast quarter — this is residential Bruges where tourist density drops to near zero. Wander Balstraat and Peperstraat, peek into tiny neighborhood squares, admire the simple brick facades that haven't changed in centuries. The Museum of Folklore (Volkskundemuseum) recreates 17th-century rooms and workshops — charming and genuinely informative.", details: ["💡 This quarter feels like what Bruges was before tourism. Let yourself get lost."] },
            { title: "Café Vlissinghe", description: "Bruges' oldest pub, operating continuously since 1515. Sit in the garden terrace under ancient trees, surrounded by locals playing petanque. Simple food — cheese croquettes, tartines, thick soup — but the atmosphere is priceless. Five centuries of conversations have soaked into these walls.", details: ["📍 Blekersstraat 2 · €10-15 · Cash preferred"] },
            { title: "Kantcentrum (Lace Centre)", description: "Bruges lace is UNESCO-recognized intangible cultural heritage. The Lace Centre occupies a restored lace school where artisans demonstrate traditional bobbin lace live. The speed and complexity of their hand movements is mesmerizing — dozens of bobbins dancing simultaneously to create intricate patterns. The small shop sells authentic handmade pieces (a table runner takes 100+ hours of work — the prices reflect real craftsmanship).", details: ["📍 Balstraat 16 · €6 entry"] },
            { title: "Jerusalem Chapel & Adornes Estate", description: "Built in 1428 by the wealthy Adornes merchant family as a private replica of the Church of the Holy Sepulchre in Jerusalem — based on their actual pilgrimage there. Dark, atmospheric, genuinely eerie. The Adornes family mausoleum with Anselm Adornes' effigy tomb is still here. One of the most unusual and haunting buildings in Belgium.", details: ["📍 Peperstraat 3 · Combined ticket with Lace Centre: €10"] },
            { title: "Sint-Annakerk", description: "Free and usually empty. Walk in and your jaw drops — the plain brick exterior hides an explosion of Baroque woodwork, marble screens, and oil paintings. It's one of Bruges' best-kept secrets. The contrast between the modest exterior and the theatrical interior is peak Flemish Baroque.", details: ["📍 Sint-Annaplein · Free · Usually open daytime"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Café Vlissinghe", description: "Doubles as your lunch stop. Cheese croquettes and a local beer in the oldest pub in town. The garden terrace with petanque players is the most authentic 'local Bruges' experience you'll find.", meta: "€10-15 · Blekersstraat 2 · Cash preferred" }
          ],
          tips: [{ type: "reddit", text: "Café Vlissinghe is where actual Bruges residents drink. The garden in summer is one of the best-kept secrets in town. Also the cheese croquettes are insanely good.", cite: "r/belgium" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Dumon Chocolatier & Sukerbuyc", description: "Two more essential chocolate stops before dinner. Dumon (Eiermarkt 6) is traditional and classic — rich, buttery pralines made by a family that's been doing this since 1992. Sukerbuyc (Katelijnestraat 5) near the Burg makes beautiful artisanal truffles and pralines. Pick up a box as gifts or late-night hotel room indulgence.", details: ["💡 Budget €10-15 per shop for a small box."] },
            { title: "Dinner at Christophe", description: "Contemporary Belgian-French cuisine in a refined canal-side setting. The tasting menu is excellent value — 4 courses around €55, showcasing seasonal ingredients with Belgian flair. Wine pairing available. An elegant way to cap a day spent exploring Bruges' quieter side.", details: ["📍 Garenmarkt 34 · €55 tasting menu · Reserve ahead"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Christophe", description: "Belgian-French fine dining without the stiffness. Seasonal tasting menu with clean, precise flavors. The canal view from the dining room adds atmosphere without feeling touristy. Good wine list with Belgian options you won't find elsewhere.", meta: "€55 tasting menu · Garenmarkt 34 · Reservations essential" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 4,
      title: "Day Trip to Ghent & Farewell Evening",
      neighborhoods: "Ghent (day) · Bruges evening",
      date: "Jun 27",
      mapPins: [
        { lat: 51.0543, lng: 3.7174, label: "St. Bavo's Cathedral", num: 1, cat: "activity", desc: "Home of Van Eyck's Ghent Altarpiece" },
        { lat: 51.0536, lng: 3.7210, label: "Graslei & Korenlei", num: 2, cat: "activity", desc: "Ghent's iconic medieval waterfront" },
        { lat: 51.0575, lng: 3.7208, label: "Gravensteen", num: 3, cat: "activity", desc: "12th-century castle with irreverent audio guide" },
        { lat: 51.0539, lng: 3.7248, label: "Patershol", num: 4, cat: "food", desc: "Ghent's oldest neighborhood, packed with restaurants" },
        { lat: 51.0548, lng: 3.7215, label: "Graffiti Street", num: 5, cat: "activity", desc: "Werregarenstraat — ever-changing street art" },
        { lat: 51.2088, lng: 3.2260, label: "'t Brugs Beertje", num: 6, cat: "food", desc: "Legendary Bruges beer bar, 300+ bottles" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to Ghent", description: "25 minutes, trains every 15 minutes, ~€7 each way. Ghent is Bruges' grittier, younger sibling — a university city with even more medieval architecture but more edge, energy, and street art. The two pair perfectly for a day trip. Ghent has a vibe Bruges doesn't: it's a living, working city where the medieval backdrop is just... normal life.", details: ["📍 Bruges station → Gent-Sint-Pieters · Trains every 15 min", "💡 Sit on the right side of the train for the best countryside views."] },
            { title: "St. Bavo's Cathedral & the Ghent Altarpiece", description: "The main event. Van Eyck's Adoration of the Mystic Lamb (1432) is widely considered the most important painting in European art history — the work that launched the entire Northern Renaissance. Recently restored to heart-stopping clarity after a decade of painstaking work — the colors are otherworldly, revealing details hidden under 600 years of varnish and overpainting. The altarpiece has been stolen 13 times (by Napoleon, the Nazis, and common thieves). You'll view it in a dedicated climate-controlled room with an audio guide that tells the whole wild story.", details: ["📍 Sint-Baafsplein · €16 entry for the altarpiece viewing room", "💡 Allow 60-90 minutes. The audio guide is excellent — don't skip it. You need context to appreciate the scale of what Van Eyck achieved."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Quick bite at Bruges station", description: "Grab a coffee and croissant before your train. Save your appetite for Ghent lunch.", meta: "€5-8 · Station area" }
          ],
          tips: [{ type: "tip", text: "If you saw Van Eyck's work at the Groeningemuseum yesterday, the Ghent Altarpiece will blow your mind — it's the masterpiece everything else was building toward. The recently restored panels are revelatory." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Gravensteen (Castle of the Counts)", description: "A 12th-century castle right in the city center — imposing, moat-surrounded, and surprisingly entertaining. The audio guide is famously funny and irreverent (in a 'Monty Python at a medieval castle' way). The torture instrument exhibition is darkly fascinating. Great views from the rooftop over Ghent's canal network.", details: ["📍 Sint-Veerleplein 11 · €12 entry · The audio guide is essential"] },
            { title: "Lunch in Patershol", description: "Ghent's oldest quarter — cobblestoned lanes crammed with restaurants from Michelin-starred to hole-in-the-wall. Try Pakhuis (gorgeous industrial-chic brasserie, great seafood) or Mosquito Coast (traveler café with global flavors). Ghent is officially the 'veggie capital of Europe' — more meat-free options per capita than anywhere on the continent.", details: ["💡 Ghent food is generally cheaper and more diverse than Bruges. Take advantage."] },
            { title: "Graslei & Korenlei Waterfront", description: "The postcard view of Ghent — medieval guild houses from the 1200s-1600s line both sides of the canal. Grab a Gentse Neuzen (Ghent's signature candy — cone-shaped violet-flavored jelly) from a sweet shop and sit along the water. The reflection of the guild houses in the canal on a clear afternoon is unforgettable.", details: [] },
            { title: "Graffiti Street & Street Art", description: "Ghent has one of Europe's best street art scenes. Werregarenstraat is a narrow alley that's an ever-changing open-air gallery — completely covered in murals, tags, and installations. The contrast between medieval architecture and contemporary street art is quintessentially Ghent. It's a living canvas that changes monthly.", details: ["📍 Werregarenstraat · Off Hoogpoort · Free and open"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Pakhuis", description: "Stunning converted warehouse with industrial-chic interior — high ceilings, iron columns, communal energy. The seafood platter is excellent, and the steak tartare is textbook. A lively, buzzing Ghent institution.", meta: "€15-25 · Schuurkenstraat 4 · Walk-in usually fine" }
          ],
          tips: [{ type: "reddit", text: "Ghent > Bruges for food and nightlife. Bruges wins on medieval charm. The day trip combo is perfect — you get both.", cite: "r/travel" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Train Back & Farewell Dinner", description: "Return to Bruges around 5:30pm. For your last proper dinner, try 't Zwart Huis — an atmospheric restaurant in a medieval mansion dating to 1482. Candlelit, dark wood, stained glass windows. Flemish cuisine with modern refinement. A setting worthy of your last Bruges evening.", details: ["📍 Kuipersstraat 23 · €30-45 mains · Reserve ahead"] },
            { title: "Beer Pilgrimage — 't Brugs Beertje", description: "Your cultural farewell to Bruges. This tiny, legendary pub has over 300 Belgian bottles and staff who genuinely love educating curious drinkers. Ask for a Trappist flight — Westvleteren 12 (often called the best beer in the world), Orval (funky and complex), Rochefort 10 (rich and dark). The bar is cash-only, small, and has zero pretension. This is Belgian beer culture at its purest.", details: ["📍 Kemelstraat 5 · Cash only · Gets busy after 9pm"] },
            { title: "Midnight Canal Walk", description: "Your farewell. Walk Rozenhoedkaai one last time — the canal reflections of lit-up medieval buildings with almost no one around. Cross Bonifaciusbrug — nicknamed the most romantic bridge in Bruges — in the quiet of the night. The city is even more beautiful when the tourists sleep. A fitting goodbye.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "'t Zwart Huis", description: "Dining inside a 1482 mansion. Candlelight, stained glass, carved wood — the atmosphere alone is worth the reservation. The food matches: refined Flemish cuisine with seasonal twists. Order the vol-au-vent (Belgium's comfort food classic) or the North Sea sole.", meta: "€30-45 · Kuipersstraat 23 · Reserve ahead" }
          ],
          tips: [{ type: "reddit", text: "'t Brugs Beertje is a pilgrimage site for beer lovers. The owner knows every single one of the 300+ beers. Just tell them what you like and trust the recommendation.", cite: "r/beer" }]
        }
      ]
    },
    {
      num: 5,
      title: "Morning Markets & Departure",
      neighborhoods: "City Center · Station",
      date: "Jun 28",
      mapPins: [
        { lat: 51.2093, lng: 3.2247, label: "Markt", num: 1, cat: "activity", desc: "One last look at the heart of Bruges" },
        { lat: 51.2070, lng: 3.2240, label: "Sint-Salvatorskathedraal", num: 2, cat: "activity", desc: "Bruges' oldest parish church — often overlooked" },
        { lat: 51.2050, lng: 3.2160, label: "Bruges Station", num: 3, cat: "activity", desc: "Onward connections" },
        { lat: 51.2085, lng: 3.2260, label: "Le Pain Quotidien", num: 4, cat: "food", desc: "Final breakfast" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Breakfast & Last Chocolate Run", description: "Leisurely coffee and pastry to start your departure day. If you need last-minute chocolate gifts, The Chocolate Line and Dumon open at 10:00. Mary Chocolatier on the Markt opens earlier for quick grabs.", details: [] },
            { title: "Sint-Salvatorskathedraal", description: "Bruges' oldest parish church, often completely overlooked by tourists fixated on the Belfry. Free entry, beautiful stained glass, and a treasury museum with Flemish art. A quiet, contemplative way to spend your last Bruges hour.", details: ["📍 Sint-Salvatorskoorstraat · Free · Treasury €4"] },
            { title: "One Last Wander", description: "Bruges always has one more hidden courtyard, one more canal angle, one more beautiful doorway you missed. Walk any streets you haven't explored. Let the city surprise you one final time.", details: [] },
            { title: "Depart", description: "Walk or taxi to the station. Trains run frequently to Brussels (1h, connections to Eurostar and the airport), Ghent (25min), or Antwerp (1h15). Tot ziens, Bruges — you'll carry the chocolate, beer, and Van Eyck memories for years.", details: ["📍 Trains every 30 min to Brussels · Buy tickets at the station or on the NMBS app"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Le Pain Quotidien", description: "A fitting Belgian bookend — organic bread, thick jam, strong coffee. The communal table is a nice way to end a solo trip, sharing space with strangers one last time.", meta: "€8-12 · Philipstockstraat · Walk-in" }
          ],
          tips: [{ type: "tip", text: "If departing Sunday, check train schedules — Belgian trains run reduced service on Sundays. The NMBS/SNCB app has real-time departures." }]
        }
      ]
    }
  ]
};

try {
    const result = fulfillOrder(order, itineraryData);
    console.log('✅ Fulfillment complete!');
    console.log('URL:', result.url);
    console.log('Slug:', result.slug);
    console.log('File:', result.filePath);
} catch (err) {
    console.error('❌ Fulfillment failed:', err.stack);
    process.exit(1);
}
