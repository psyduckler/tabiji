const fulfillOrder = require('./fulfill-order');

const order = {
  id: "order_1772235457328_9rbq7a",
  email: "rodde13@gmail.com",
  destination: "België",
  start_date: "2026-06-01",
  end_date: "2026-07-12",
  group_size: "2",
  travel_style: "Cultural, Relaxation, Family-friendly",
  dining: "Mix of everything",
  budget: "$1,000-2,000",
  requests: "",
  amount: "0.00",
  timestamp: "2026-02-27T23:37:37.328Z",
  status: "pending"
};

const itineraryData = {
  destination: "Belgium",
  countryEmoji: "🇧🇪",
  title: "Belgium in 42 Days: The Complete Kingdom",
  subtitle: "Brussels → Bruges → Ghent → Antwerp → Wallonia → Ardennes → Coast",
  description: "A leisurely 6-week exploration of Belgium for two — covering every corner of this small but extraordinarily rich country. From medieval Flemish cities and world-class art to the forested Ardennes, French-speaking Wallonia, the North Sea coast, and Belgium's legendary food and beer culture. At this pace, you'll live like locals, not tourists.",
  duration: "42 days / 41 nights",
  dates: "Jun 1 – Jul 12, 2026",
  budget: "$1,000–2,000",
  pace: "Relaxed — deep immersion, no rushing",
  bestFor: "Couples seeking culture, food, relaxation & family-friendly experiences",
  highlights: [
    "Brussels' Grand-Place — Europe's most beautiful square, UNESCO World Heritage",
    "Bruges' medieval canals and Flemish Primitives at the Groeningemuseum",
    "Ghent's Altarpiece — Van Eyck's masterpiece, the most important painting in European art",
    "Antwerp — Rubens, diamonds, fashion, and the best food scene in Belgium",
    "Belgian beer pilgrimage — Trappist abbeys, lambic breweries, gueuze blenders",
    "The Ardennes — forested hills, castle ruins, kayaking the Semois and Lesse rivers",
    "Wallonia — Dinant's citadel, Namur's charm, Durbuy's medieval magic",
    "Belgian coast — Ostend's promenade, De Haan's Belle Époque villas",
    "Leuven — Europe's oldest Catholic university and the Stella Artois homeland",
    "Spa — the original wellness town that gave its name to all spas worldwide",
    "Chocolate, waffles, frites, and moules-frites at every turn",
    "Battlefields of Flanders Fields and the Somme — WWI history"
  ],
  essentials: [
    { title: "🚆 Getting Around", text: "Belgium is tiny (300km top to bottom) with excellent rail. Buy a 10-ride SNCB pass for €83 — any station to any station. Trains run every 15-30 min between major cities. Brussels to Bruges: 1hr. Brussels to Ghent: 30min. Brussels to Antwerp: 45min. No car needed in cities; consider renting for 4-5 days in the Ardennes." },
    { title: "💵 Budget Reality", text: "Belgium is mid-range Western Europe. Lunch: €12-20. Dinner: €25-50. Beer in a café: €3-6. Museum: €8-16. Budget €80-120/day for two beyond accommodation. The longer stay means you can cook some meals — Airbnbs with kitchens are ideal. Markets are excellent and cheap." },
    { title: "🌤️ Summer Weather", text: "June-July: 15-25°C, long days (sunrise 5:30, sunset 22:00). Rain is always possible — pack a light waterproof. July can occasionally hit 30°C. Perfect for outdoor dining, canal-side walks, and Ardennes hiking." },
    { title: "🗣️ Languages", text: "Belgium has three official languages: Dutch (Flanders/north), French (Wallonia/south), and German (tiny eastern region). Brussels is officially bilingual Dutch-French. English is widely spoken everywhere. Don't worry about language barriers." },
    { title: "🍺 Beer Guide", text: "Belgium has ~300 breweries and 1,500+ beers. Must-try styles: Trappist ales (Westvleteren, Chimay, Orval), lambics (spontaneous fermentation, Brussels region only), gueuze (blended lambics), witbier (Hoegaarden), and Belgian strong ales. Visit at least one Trappist abbey and one lambic brewer." },
    { title: "🏨 Accommodation Strategy", text: "For 42 days, mix it up: Airbnbs for week-long stays in base cities (cheaper, kitchens), B&Bs in Ardennes villages, and a couple of splurge hotels. Book Bruges and Ghent accommodations early — summer fills fast. Wallonia and the coast are easier to find last-minute." }
  ],
  days: [
    // === BRUSSELS (Days 1-7) ===
    {
      num: 1,
      title: "Arrival in Brussels — Grand-Place & First Beer",
      neighborhoods: "Grand-Place · Îlot Sacré · City Center",
      date: "Jun 1",
      mapPins: [
        { lat: 50.8467, lng: 4.3525, label: "Grand-Place", num: 1, cat: "activity", desc: "Europe's most beautiful square" },
        { lat: 50.8451, lng: 4.3498, label: "Manneken Pis", num: 2, cat: "activity", desc: "Brussels' famous little statue" },
        { lat: 50.8475, lng: 4.3540, label: "Delirium Café", num: 3, cat: "food", desc: "2,000+ beers on the menu" },
        { lat: 50.8460, lng: 4.3530, label: "Galeries Royales Saint-Hubert", num: 4, cat: "activity", desc: "Europe's oldest shopping arcade (1847)" }
      ],
      timeBlocks: [
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive & Settle In", description: "Check into your accommodation near the Grand-Place area. Brussels Midi/Zuid station is the main international hub (Eurostar, Thalys). Take the metro or walk to the center — everything is within 20 minutes.", details: ["💡 If arriving early, drop bags and head straight out. Brussels reveals itself on foot."] },
            { title: "Grand-Place", description: "Walk into the Grand-Place and let your jaw drop. Victor Hugo called it the most beautiful square in the world, and he wasn't exaggerating. Gothic Town Hall (1449), ornate Baroque guild houses with gold leaf facades, and the Maison du Roi museum. The square changes character with the light — come back at night when it's illuminated.", details: ["📍 Central Brussels · Free · Maison du Roi museum €8"] },
            { title: "Galeries Royales Saint-Hubert", description: "Europe's oldest covered shopping gallery (1847) — glass-roofed, elegant, lined with chocolate shops, cafés, and bookstores. Neuhaus invented the Belgian praline here in 1912. Window-shop or buy your first box.", details: ["📍 Off Grand-Place · Free to walk through"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Chez Léon", description: "Brussels' most famous moules-frites since 1893. A rite of passage — giant pots of mussels in white wine, herbs, and cream, with crispy double-fried frites. Touristy? Yes. Still good? Absolutely.", meta: "€20-30 · Rue des Bouchers · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Grand-Place is free and open 24/7. Visit at night — the illuminated guild houses are magical and crowds thin dramatically after 10pm." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Delirium Café", description: "Down a narrow alley off Grand-Place, this legendary bar holds the Guinness World Record for most beers available — over 2,000. Start with a Delirium Tremens (their house beer, a strong blonde) and ask the bartender for recommendations. Three floors of beer madness.", details: ["📍 Impasse de la Fidélité 4A · €4-8 per beer"] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "Delirium is touristy but genuinely fun. Go early (before 9pm) to actually get a seat and talk to the bartenders. They know their 2,000 beers.", cite: "r/belgium" }]
        }
      ]
    },
    {
      num: 2,
      title: "Brussels — Art, Chocolate & Marolles",
      neighborhoods: "Mont des Arts · Sablon · Marolles",
      date: "Jun 2",
      mapPins: [
        { lat: 50.8424, lng: 4.3596, label: "Royal Museums of Fine Arts", num: 1, cat: "activity", desc: "Bruegel, Rubens, Magritte" },
        { lat: 50.8425, lng: 4.3600, label: "Magritte Museum", num: 2, cat: "activity", desc: "World's largest Magritte collection" },
        { lat: 50.8413, lng: 4.3550, label: "Place du Grand Sablon", num: 3, cat: "food", desc: "Chocolate shops and antiques" },
        { lat: 50.8388, lng: 4.3472, label: "Jeu de Balle Flea Market", num: 4, cat: "activity", desc: "Daily flea market in the Marolles" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Royal Museums of Fine Arts", description: "Belgium's flagship art complex. The Old Masters museum has Bruegel's Census at Bethlehem, Rubens' grand canvases, and Flemish masterworks spanning 6 centuries. Next door, the Magritte Museum houses 200+ works by Belgium's most famous surrealist — bowler hats, floating rocks, and that famous pipe. Allow 3 hours for both.", details: ["📍 Rue de la Régence 3 · €15 combined · Opens 10am, closed Mondays"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Le Pain Quotidien", description: "Born in Brussels in 1990 — this is the original. Communal tables, organic bread, tartines with thick jam. Start the day properly Belgian.", meta: "€8-12 · Multiple locations" }
          ],
          tips: [{ type: "tip", text: "The Magritte Museum is chronological — start at the top floor and work down. His early work contextualizes the surrealism." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Sablon Chocolate Trail", description: "Place du Grand Sablon is Brussels' most elegant square, ringed with Belgium's finest chocolatiers. Pierre Marcolini (bean-to-bar perfectionist), Wittamer (royal warrant holder since 1910), and Patrick Roger (French interloper with wild chocolate sculptures). Taste at each — they're all generous with samples.", details: ["💡 Budget €30-40 for chocolate across the afternoon. Worth every centime."] },
            { title: "Marolles & Jeu de Balle", description: "Walk downhill from Sablon into the Marolles — Brussels' working-class neighborhood with daily flea market at Place du Jeu de Balle. Vintage furniture, old records, random treasures. The neighborhood has great local bars and a completely different vibe from touristy central Brussels.", details: ["📍 Place du Jeu de Balle · Daily 6am-2pm · Best on weekends"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Restobières", description: "Every dish cooked with Belgian beer. Carbonnade flamande (beef stewed in dark beer), rabbit in kriek, chocolate mousse with Chimay Blue. Cozy, unpretentious, and genuinely delicious.", meta: "€20-35 · Rue des Renards 32 · Marolles" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 3,
      title: "Brussels — Atomium, EU Quarter & Comic Strips",
      neighborhoods: "Heysel · EU Quarter · City Center",
      date: "Jun 3",
      mapPins: [
        { lat: 50.8950, lng: 4.3418, label: "Atomium", num: 1, cat: "activity", desc: "Iconic 1958 World's Fair structure" },
        { lat: 50.8413, lng: 4.3826, label: "European Parliament", num: 2, cat: "activity", desc: "Free visitor center — Parlamentarium" },
        { lat: 50.8474, lng: 4.3563, label: "Belgian Comic Strip Center", num: 3, cat: "activity", desc: "Tintin, Smurfs, Lucky Luke" },
        { lat: 50.8500, lng: 4.3480, label: "Comic Book Walls", num: 4, cat: "activity", desc: "50+ murals across the city" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Atomium", description: "Brussels' most iconic structure — a 102m iron crystal magnified 165 billion times, built for the 1958 World's Fair. Take the elevator to the top sphere for panoramic views, then explore the exhibitions inside. The escalator tube between spheres is like something from a sci-fi movie. Love it or find it weird, it's unmissably Brussels.", details: ["📍 Heysel · €16 · Metro line 6 to Heysel station"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Maison Dandoy", description: "Brussels' finest waffles since 1829. Try the Liège waffle (dense, sweet, caramelized pearl sugar) — it's the Belgian waffle most Belgians actually eat. The Brussels waffle (lighter, rectangular, crispy) is good too.", meta: "€6-10 · Rue au Beurre 31 · Near Grand-Place" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "European Quarter", description: "Brussels is the de facto capital of Europe. The Parlamentarium (European Parliament visitor center) is free, interactive, and surprisingly fascinating — covering EU history, decision-making, and current challenges. Even if politics isn't your thing, the multimedia experience is well done.", details: ["📍 Place du Luxembourg · Free · Closed Mondays"] },
            { title: "Belgian Comic Strip Center", description: "Belgium gave the world Tintin, the Smurfs, and Lucky Luke. This museum in a gorgeous Art Nouveau building (designed by Victor Horta) celebrates the comic strip as Belgium's 'ninth art.' Original Hergé drawings, life-size character statues, and a great bookshop. Walk the city afterward to spot 50+ comic book murals painted on building walls.", details: ["📍 Rue des Sables 20 · €12 · The Art Nouveau building alone is worth the visit"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Fin de Siècle", description: "No-frills, no-reservation Belgian institution. Hearty classics: vol-au-vent, stoemp (mashed potato with veg), waterzooi. Packed with locals, communal tables, great atmosphere. Cash only.", meta: "€15-25 · Rue des Chartreux 9 · Cash only · No reservations" }
          ],
          tips: [{ type: "reddit", text: "Fin de Siècle is the most recommended restaurant in Brussels for a reason. Go early (6pm) or wait 30+ min. The vol-au-vent is incredible.", cite: "r/brussels" }]
        }
      ]
    },
    {
      num: 4,
      title: "Brussels — Art Nouveau & Ixelles",
      neighborhoods: "Saint-Gilles · Ixelles · Louise",
      date: "Jun 4",
      mapPins: [
        { lat: 50.8223, lng: 4.3542, label: "Horta Museum", num: 1, cat: "activity", desc: "Victor Horta's Art Nouveau masterpiece home" },
        { lat: 50.8300, lng: 4.3650, label: "Place Flagey", num: 2, cat: "activity", desc: "Ixelles' vibrant square" },
        { lat: 50.8275, lng: 4.3700, label: "Ixelles Ponds", num: 3, cat: "activity", desc: "Peaceful urban ponds for strolling" },
        { lat: 50.8250, lng: 4.3550, label: "Châtelain Market", num: 4, cat: "food", desc: "Wednesday afternoon food market" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Horta Museum", description: "Victor Horta invented Art Nouveau architecture in Brussels in the 1890s. His own house-studio is now a museum — every detail, from the staircase's whiplash curves to the door handles and light fixtures, is pure flowing organic design. The stairwell alone justifies the visit: a spiral of iron, glass, and mosaic that feels alive. Small museum, enormous impact.", details: ["📍 Rue Américaine 25 · €12 · Timed tickets, book ahead · No photos inside"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Café Belga", description: "Art Deco café on Place Flagey — the heart of Ixelles' hipster scene. Great coffee, brunch options, and people-watching from the terrace.", meta: "€8-14 · Place Flagey · Ixelles" }
          ],
          tips: [{ type: "tip", text: "Brussels has more Art Nouveau buildings than any other city in the world. Beyond Horta Museum, walk Rue Defacqz, Avenue Louise area, and Rue Faider to spot stunning facades." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Ixelles Neighborhood Walk", description: "Ixelles is where young Brussels lives — diverse, creative, full of independent shops and excellent restaurants. Walk around the Ixelles ponds (Étangs d'Ixelles), browse vintage shops on Chaussée d'Ixelles, and soak up the multicultural atmosphere of Matongé (Brussels' Congolese quarter).", details: [] },
            { title: "Rest Day Activities", description: "After 3 intense days, take it easy. Cook a meal at your Airbnb using ingredients from the local market. Read in a park. Brussels rewards slow days just as much as busy ones.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "La Quincaillerie", description: "Stunning restaurant in a converted 19th-century hardware store. High ceilings, ornate woodwork, brass fittings. French-Belgian cuisine — duck confit, sole meunière, excellent wine list. A splurge evening.", meta: "€35-50 · Rue du Page 45 · Ixelles · Reserve" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 5,
      title: "Brussels — Laeken, Parks & Royal Greenhouses",
      neighborhoods: "Laeken · Cinquantenaire · Parc Royal",
      date: "Jun 5",
      mapPins: [
        { lat: 50.8764, lng: 4.3583, label: "Royal Greenhouses of Laeken", num: 1, cat: "activity", desc: "Stunning Art Nouveau glass houses (open only a few weeks/year)" },
        { lat: 50.8400, lng: 4.3930, label: "Cinquantenaire Park", num: 2, cat: "activity", desc: "Triumphal arch and museums" },
        { lat: 50.8440, lng: 4.3610, label: "Parc de Bruxelles", num: 3, cat: "activity", desc: "Royal park for a picnic" },
        { lat: 50.8420, lng: 4.3950, label: "Autoworld", num: 4, cat: "activity", desc: "Vintage car museum in Cinquantenaire" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Royal Greenhouses of Laeken", description: "If open (usually late April–early May, but check dates), these Art Nouveau glass palaces house exotic plant collections in breathtaking iron-and-glass structures. If closed, visit the Japanese Tower and Chinese Pavilion nearby — beautiful Asian-inspired royal follies.", details: ["📍 Domaine Royal de Laeken · Check dates · Tram 7"] },
            { title: "Cinquantenaire Park", description: "Brussels' grandest park — built for Belgium's 50th anniversary. The triumphal arch is impressive; the park itself is perfect for a morning stroll. The complex houses Autoworld (vintage cars) and the Art & History Museum (ancient Egyptian, Roman, Art Nouveau collections).", details: ["📍 Parc du Cinquantenaire · Free park · Museums €10-12 each"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "MOK Coffee", description: "Third-wave specialty coffee roastery in the city center. Excellent flat whites and pastries. Brussels' coffee scene has exploded in recent years.", meta: "€5-10 · Rue Antoine Dansaert 196" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Parc de Bruxelles & Picnic", description: "The formal royal park between the Royal Palace and Parliament. Grab supplies from a nearby deli — cheese, charcuterie, bread, beer — and have a proper Belgian park picnic. In summer, the park is alive with Bruxellois enjoying long evenings.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Nüetnigenansen", description: "Brussels institution — hearty Flemish food, massive portions, genuine local crowd. The name means 'good for nothing' in Brussels dialect. Try the stoofvlees or the shrimp croquettes.", meta: "€15-25 · Rue du Lombard 25" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 6,
      title: "Day Trip — Waterloo & Brabant Countryside",
      neighborhoods: "Waterloo · Braine-l'Alleud",
      date: "Jun 6",
      mapPins: [
        { lat: 50.6801, lng: 4.4097, label: "Lion's Mound (Butte du Lion)", num: 1, cat: "activity", desc: "Waterloo battlefield memorial — 226 steps to panoramic view" },
        { lat: 50.6810, lng: 4.4125, label: "Waterloo Memorial 1815", num: 2, cat: "activity", desc: "Immersive underground museum" },
        { lat: 50.6780, lng: 4.4050, label: "Hougoumont Farm", num: 3, cat: "activity", desc: "Key battlefield farm, restored" },
        { lat: 50.7140, lng: 4.3990, label: "Waterloo Town", num: 4, cat: "food", desc: "Wellington's headquarters museum" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Waterloo Battlefield", description: "Where Napoleon met his end on June 18, 1815. The new underground Memorial 1815 museum is genuinely excellent — immersive, cinematic, covering the battle from all sides. Climb the Lion's Mound (226 steps) for a 360° view of the battlefield. Stand where 200,000 soldiers fought and European history pivoted.", details: ["📍 Route du Lion 1815, Braine-l'Alleud · €20 combined ticket · Bus W from Brussels"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Quick breakfast in Brussels", description: "Eat before heading out — Waterloo dining options are limited.", meta: "" }
          ],
          tips: [{ type: "tip", text: "The combined ticket covers Lion's Mound + Memorial 1815 + Panorama + Hougoumont Farm. Allow 3-4 hours for everything." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Hougoumont Farm", description: "The farmstead where the battle's most desperate fighting occurred. Recently restored with a powerful exhibition inside. Walking the grounds where soldiers fought room-to-room is sobering and deeply moving.", details: [] },
            { title: "Return to Brussels", description: "Head back for a relaxed final Brussels evening. Pack up for tomorrow's move to Bruges.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Henri", description: "Classic Brussels brasserie with Art Deco interiors. Excellent steak tartare (a Belgian obsession), perfectly crispy frites, and good Belgian beers on tap. A proper farewell dinner for Brussels.", meta: "€25-40 · Rue de Flandre 113 · Center" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 7,
      title: "Brussels — Slow Morning & Move Day Buffer",
      neighborhoods: "City Center",
      date: "Jun 7",
      mapPins: [
        { lat: 50.8467, lng: 4.3525, label: "Grand-Place (farewell)", num: 1, cat: "activity", desc: "One last visit at morning light" },
        { lat: 50.8455, lng: 4.3535, label: "Neuhaus", num: 2, cat: "food", desc: "Buy chocolate for the road" },
        { lat: 50.8390, lng: 4.3360, label: "Brussels Midi Station", num: 3, cat: "activity", desc: "Train to Bruges" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Brussels Morning", description: "Revisit Grand-Place in morning light — the square has a completely different mood at 8am with no crowds. Pick up last chocolate gifts at Neuhaus in the Galeries. A slow coffee, a final waffle, then train to Bruges.", details: [] },
            { title: "Train to Bruges", description: "Direct train from Brussels Midi, 1 hour. Watch the landscape flatten into Flanders — fields, canals, church spires.", details: ["📍 Brussels Midi → Bruges · ~1h · Trains every 30 min · €15"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Grand-Place area café", description: "Leisurely final Brussels breakfast.", meta: "" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive in Bruges & Settle In", description: "Check into your Bruges accommodation — ideally inside the egg-shaped old city. The walk from the station is 15 minutes along Zuidzandstraat. Bruges is compact and entirely walkable. Drop bags and wander — let the canals, cobblestones, and medieval rooftops welcome you.", details: [] },
            { title: "Markt & Belfry First Impressions", description: "Walk to the Markt — Bruges' central square dominated by the 83m Belfry. Save climbing for tomorrow, but take in the guild houses and the scale of this UNESCO gem. Grab a first Brugse Zot (brewed two blocks away) on a terrace.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "De Stove", description: "Tiny, family-run, 20 seats. Classic Flemish waterzooi (creamy chicken stew) or stoofvlees (beef in dark beer). Book ahead. Zero pretension, 100% flavor.", meta: "€25-35 · Kleine Sint-Amandsstraat 4 · Reserve" }
          ],
          tips: [{ type: "reddit", text: "De Stove is one of the few restaurants in Bruges that locals actually eat at. Skip the Markt tourist traps.", cite: "r/belgium" }]
        }
      ]
    },
    // === BRUGES (Days 8-14) ===
    {
      num: 8,
      title: "Bruges — Belfry, Basilica & Canal Cruise",
      neighborhoods: "Markt · Burg · Dijver Canal",
      date: "Jun 8",
      mapPins: [
        { lat: 51.2093, lng: 3.2247, label: "Belfry of Bruges", num: 1, cat: "activity", desc: "366 steps, panoramic views" },
        { lat: 51.2087, lng: 3.2269, label: "Basilica of the Holy Blood", num: 2, cat: "activity", desc: "12th-century chapel with sacred relic" },
        { lat: 51.2062, lng: 3.2275, label: "Canal Boat Departure", num: 3, cat: "activity", desc: "30 min tour from water level" },
        { lat: 51.2065, lng: 3.2270, label: "Rozenhoedkaai", num: 4, cat: "activity", desc: "Most photographed spot in Bruges" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Belfry of Bruges", description: "Climb 366 narrow steps to the top of Bruges' iconic tower. At 83m, the views sweep over every red rooftop, the canal network, and on clear days to the coast. The 47-bell carillon rings every quarter hour — being up top during a chime is unforgettable.", details: ["📍 Markt · €14 · Go at opening (9:30) to avoid crowds"] },
            { title: "Burg Square & Basilica of the Holy Blood", description: "Through a narrow passage from the Markt to the more intimate Burg. The Basilica houses a relic believed to contain Christ's blood. The lower chapel is 12th-century Romanesque — dark, moody, barely changed in 900 years.", details: ["📍 Free entry · Treasury €2.50"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "That's Toast", description: "Specialty coffee and creative breakfasts near 't Zand. Strong flat whites and good avocado toast.", meta: "€8-14 · Walk-in" }
          ],
          tips: [{ type: "tip", text: "Buy the Musea Brugge card (€30, 72 hours, 16 museums). Essential for any cultural visit." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Canal Boat Tour", description: "30-minute ride from Dijver landing. See Bruges from water level — medieval facades, secret gardens, low stone bridges. Late afternoon light turns the brick golden.", details: ["📍 Dijver · €12 · No reservation needed"] },
            { title: "Rozenhoedkaai at Golden Hour", description: "The most photographed spot in Bruges — the canal bends under ancient trees with the Belfry reflected in the water. In June, golden hour lasts until nearly 10pm.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Den Dyver", description: "Every dish cooked with and paired to a specific Belgian beer. The biersommelier walks you through pairings with genuine passion. Canal-side setting.", meta: "€35-50 · Dijver 5 · Reserve" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 9,
      title: "Bruges — Flemish Masters & Memling",
      neighborhoods: "Museum Quarter · Begijnhof · Minnewater",
      date: "Jun 9",
      mapPins: [
        { lat: 51.2050, lng: 3.2265, label: "Groeningemuseum", num: 1, cat: "activity", desc: "Van Eyck, Memling, Bosch" },
        { lat: 51.2043, lng: 3.2256, label: "Sint-Janshospitaal", num: 2, cat: "activity", desc: "Memling's Shrine of St. Ursula" },
        { lat: 51.2037, lng: 3.2235, label: "Church of Our Lady", num: 3, cat: "activity", desc: "Michelangelo's Madonna and Child" },
        { lat: 51.2015, lng: 3.2245, label: "Begijnhof", num: 4, cat: "activity", desc: "13th-century walled beguinage" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Groeningemuseum", description: "World-class Flemish Primitives collection. Van Eyck's Madonna with Canon van der Paele — the birth of oil painting technique. Memling, Bosch, Provost. Small museum, immense art. Allow 90 minutes.", details: ["📍 Dijver 12 · €14 (Musea Brugge card) · Open 9:30"] },
            { title: "Sint-Janshospitaal & Memling Museum", description: "Medieval hospital housing Hans Memling's greatest works. The Shrine of St. Ursula is a tiny reliquary painted with impossibly intricate scenes. The hospital wards — massive oak-beamed halls — are atmospheric.", details: ["📍 Mariastraat 38 · €14"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "De Belegde Boterham", description: "No-frills sandwich shop. Massive open-faced sandwiches. Cheap, cheerful, beloved by locals.", meta: "€8-12 · Walk-in" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Church of Our Lady", description: "Belgium's tallest brick tower (115m). Inside: Michelangelo's Madonna and Child (1504) — the only Michelangelo to leave Italy in his lifetime. Smaller than expected but impossibly delicate.", details: ["📍 Mariastraat · €7 art section · Nave free"] },
            { title: "Begijnhof & Minnewater", description: "White-washed 1245 beguinage. Silence requested, deeply felt. Continue to Minnewater — the Lake of Love with swans and willows. Legend: cross the bridge with your beloved for eternal love.", details: ["📍 Free · House museum €2"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Christophe", description: "Contemporary Belgian-French cuisine. Seasonal tasting menu, clean flavors, canal view. Excellent value at €55 for 4 courses.", meta: "€55 tasting · Garenmarkt 34 · Reserve" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 10,
      title: "Bruges — Chocolate, Lace & Sint-Anna Quarter",
      neighborhoods: "Sint-Anna · Langestraat · Northeast Bruges",
      date: "Jun 10",
      mapPins: [
        { lat: 51.2130, lng: 3.2305, label: "The Chocolate Line", num: 1, cat: "food", desc: "Dominique Persoone's avant-garde shop" },
        { lat: 51.2140, lng: 3.2340, label: "Kantcentrum (Lace Centre)", num: 2, cat: "activity", desc: "Live bobbin lace demonstrations" },
        { lat: 51.2108, lng: 3.2370, label: "Café Vlissinghe", num: 3, cat: "food", desc: "Oldest pub since 1515" },
        { lat: 51.2155, lng: 3.2350, label: "Jerusalem Chapel", num: 4, cat: "activity", desc: "15th-century Holy Sepulchre replica" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "The Chocolate Line", description: "Dominique Persoone's avant-garde shop. Flavors: wasabi, cigar, cola, bacon. Behind the theatrics is genuine mastery.", details: ["📍 Simon Stevinplein 19 · €15-25/box"] },
            { title: "Choco-Story Museum", description: "4,000 years of chocolate history. Live praline-making demo with free tastings.", details: ["📍 Wijnzakstraat 2 · €11"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Le Pain Quotidien", description: "Communal tables, organic bread, Belgian start to the day.", meta: "€8-12" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Sint-Anna Quarter", description: "Bruges' quiet northeast — residential, zero tourists. Museum of Folklore recreates 17th-century rooms. Get lost in medieval streets.", details: [] },
            { title: "Café Vlissinghe", description: "Operating since 1515. Garden terrace, locals playing petanque, cheese croquettes. Five centuries of atmosphere.", details: ["📍 Blekersstraat 2 · €10-15 · Cash preferred"] },
            { title: "Lace Centre & Jerusalem Chapel", description: "Watch bobbin lace artisans work. Then visit the 1428 Adornes Chapel — a private replica of the Holy Sepulchre, dark and haunting.", details: ["📍 Combined ticket €10"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Sans Cravate", description: "Michelin-starred Bruges fine dining. Inventive Belgian-French cuisine in a historic townhouse. A special night out.", meta: "€65-85 tasting · Langestraat 159 · Reserve well ahead" }
          ],
          tips: [{ type: "reddit", text: "Café Vlissinghe garden in summer is the best-kept secret in Bruges. Also the cheese croquettes are insanely good.", cite: "r/belgium" }]
        }
      ]
    },
    {
      num: 11,
      title: "Day Trip — Ghent & the Altarpiece",
      neighborhoods: "Ghent",
      date: "Jun 11",
      mapPins: [
        { lat: 51.0543, lng: 3.7174, label: "St. Bavo's Cathedral", num: 1, cat: "activity", desc: "Van Eyck's Ghent Altarpiece" },
        { lat: 51.0575, lng: 3.7208, label: "Gravensteen", num: 2, cat: "activity", desc: "Castle of the Counts — hilarious audio guide" },
        { lat: 51.0536, lng: 3.7210, label: "Graslei & Korenlei", num: 3, cat: "activity", desc: "Medieval waterfront" },
        { lat: 51.0548, lng: 3.7215, label: "Graffiti Street", num: 4, cat: "activity", desc: "Ever-changing street art" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to Ghent & Ghent Altarpiece", description: "25 min from Bruges. Head straight to St. Bavo's Cathedral for Van Eyck's Adoration of the Mystic Lamb (1432) — the most important painting in European art. Recently restored to heart-stopping clarity. Stolen 13 times (Napoleon, Nazis). The audio guide is essential.", details: ["📍 Sint-Baafsplein · €16 · Allow 60-90 min"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Quick bite at station", description: "Save appetite for Ghent lunch.", meta: "" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Gravensteen", description: "12th-century castle with the most irreverent audio guide in any museum anywhere. Monty Python meets medieval history. Torture instrument exhibition. Great rooftop views.", details: ["📍 €12 · Audio guide essential"] },
            { title: "Graslei/Korenlei & Graffiti Street", description: "Medieval guild houses lining both canal banks — the postcard of Ghent. Then duck into Werregarenstraat for ever-changing street art murals.", details: [] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Pakhuis", description: "Converted warehouse brasserie. Excellent seafood platter and steak tartare.", meta: "€15-25 · Walk-in" },
            { type: "🍽️ Dinner", name: "Back in Bruges — 't Brugs Beertje", description: "300+ Belgian bottles, staff who love educating. Ask for a Trappist flight. Cash only.", meta: "€4-8/beer · Kemelstraat 5 · Cash" }
          ],
          tips: [{ type: "reddit", text: "Ghent > Bruges for food. Bruges > Ghent for medieval charm. The day trip combo is perfect.", cite: "r/travel" }]
        }
      ]
    },
    {
      num: 12,
      title: "Bruges — De Halve Maan & Relaxation Day",
      neighborhoods: "Walplein · Canals · City Center",
      date: "Jun 12",
      mapPins: [
        { lat: 51.2060, lng: 3.2300, label: "De Halve Maan Brewery", num: 1, cat: "food", desc: "Only active city-center brewery" },
        { lat: 51.2065, lng: 3.2270, label: "Rozenhoedkaai", num: 2, cat: "activity", desc: "Different light at different times" },
        { lat: 51.2045, lng: 3.2255, label: "Arentshuis", num: 3, cat: "activity", desc: "Frank Brangwyn art + lace gallery" },
        { lat: 51.2080, lng: 3.2230, label: "Le Trappiste", num: 4, cat: "food", desc: "Beer bar in a 13th-century basement" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "De Halve Maan Brewery Tour", description: "The only active brewery in Bruges' medieval center. 45 min tour → rooftop terrace → glass of Brugse Zot. Fun fact: in 2016 they built a 3.2km underground beer pipeline because trucks damaged the cobblestones.", details: ["📍 Walplein 26 · €16 with tasting · Book online"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Books & Brunch", description: "Cozy café with good pastries and a book exchange. Slow morning energy.", meta: "€8-12" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Relaxation Afternoon", description: "Bruges rewards slowness. Revisit favorite canals at different light. Browse the Arentshuis garden (free, peaceful). Read on a bench by the Dijver. Rent bikes and ride along the canal to Damme (7km, flat, beautiful).", details: [] },
            { title: "Le Trappiste", description: "Beer bar in a 13th-century vaulted basement. Excellent Trappist selection in an atmospheric setting.", details: ["📍 Kuipersstraat 33 · €4-8/beer"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "'t Zwart Huis", description: "Dining in a 1482 mansion. Candlelight, stained glass, carved wood. Refined Flemish cuisine. Try the vol-au-vent or North Sea sole.", meta: "€30-45 · Kuipersstraat 23 · Reserve" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 13,
      title: "Day Trip — Belgian Coast (Ostend & De Haan)",
      neighborhoods: "Ostend · De Haan",
      date: "Jun 13",
      mapPins: [
        { lat: 51.2272, lng: 2.9211, label: "Ostend Beach", num: 1, cat: "activity", desc: "Belgium's biggest beach resort" },
        { lat: 51.2288, lng: 2.9245, label: "Mu.ZEE", num: 2, cat: "activity", desc: "Modern art museum — Ensor, Spilliaert" },
        { lat: 51.2750, lng: 3.0320, label: "De Haan", num: 3, cat: "activity", desc: "Belle Époque seaside village" },
        { lat: 51.2285, lng: 2.9210, label: "Ostend Fish Market", num: 4, cat: "food", desc: "Fresh North Sea seafood" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to Ostend", description: "15 minutes from Bruges. Belgium's biggest coastal resort — a real working city, not a tourist trap. The promenade is long and windswept, the fish is ridiculously fresh, and Mu.ZEE houses an excellent collection of Belgian modern art (James Ensor and Léon Spilliaert were both from here).", details: ["📍 15 min train from Bruges · Regular service"] },
            { title: "Ostend Fish Market & Seafood Lunch", description: "The Vistrap (fish market) near the harbor sells the freshest North Sea catch. Nearby restaurants serve moules, sole, grey shrimp croquettes (garnaalcroquetten — a Belgian obsession), and raw oysters.", details: ["📍 Near the harbor · Morning is best for the market"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Fish Market restaurants", description: "Garnaalcroquetten (grey shrimp croquettes) — Belgium's most beloved seafood dish. Crispy outside, creamy bechamel-and-shrimp inside. Pair with a cold Vedett.", meta: "€15-25 · Harbor area" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Coastal Tram to De Haan", description: "The Kusttram runs the entire 67km Belgian coastline. Take it from Ostend to De Haan — a perfectly preserved Belle Époque seaside village. White villas with turrets and balconies, pine forests, quiet beach. Einstein stayed here in 1933. It's the antidote to Ostend's brashness.", details: ["📍 Kusttram from Ostend · ~20 min · €3"] },
            { title: "De Haan Beach Walk", description: "Peaceful, uncrowded beach backed by dunes and Belle Époque architecture. Walk, swim (if brave — North Sea is cold), or just sit with a book. The village center has tea rooms and a charming main street.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Back in Bruges — Breydel De Coninc", description: "Bruges' best moules-frites. The mussels are enormous and the frites are perfect. Simple, excellent, no-fuss.", meta: "€20-30 · Breidelstraat 24" }
          ],
          tips: [{ type: "tip", text: "The Kusttram is the world's longest tram line (67km). A ride from one end to the other takes 2.5 hours and shows every Belgian seaside personality." }]
        }
      ]
    },
    {
      num: 14,
      title: "Bruges — Final Day & Move to Ghent",
      neighborhoods: "Bruges → Ghent",
      date: "Jun 14",
      mapPins: [
        { lat: 51.2093, lng: 3.2247, label: "Markt farewell", num: 1, cat: "activity", desc: "Last morning walk" },
        { lat: 51.2050, lng: 3.2160, label: "Bruges Station", num: 2, cat: "activity", desc: "Train to Ghent" },
        { lat: 51.0536, lng: 3.7210, label: "Graslei (Ghent)", num: 3, cat: "activity", desc: "Evening waterfront" },
        { lat: 51.0539, lng: 3.7248, label: "Patershol", num: 4, cat: "food", desc: "Ghent's oldest neighborhood restaurants" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Bruges Wander", description: "One last morning stroll. Visit any streets you missed. The city always has one more hidden courtyard.", details: [] },
            { title: "Train to Ghent", description: "25 minutes. Switch from medieval fairy tale to vibrant university city.", details: ["📍 Bruges → Gent-Sint-Pieters · 25 min · €7"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Bruges bakery", description: "Pastry and coffee for the road.", meta: "" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Settle into Ghent", description: "Check in near the center. Ghent is bigger and edgier than Bruges — a real working university city where medieval architecture is just the backdrop to daily life.", details: [] },
            { title: "Graslei Evening", description: "Ghent's famous waterfront. Grab a beer, sit along the canal, watch the guild house reflections.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Mosquito Coast", description: "Traveler café with global flavors — a Ghent institution. Casual, affordable, great cocktails and world food.", meta: "€15-25 · Hoogpoort 28" }
          ],
          tips: []
        }
      ]
    },
    // === GHENT (Days 15-19) ===
    {
      num: 15,
      title: "Ghent — STAM, Design Museum & Beer",
      neighborhoods: "Bijloke · Patershol · City Center",
      date: "Jun 15",
      mapPins: [
        { lat: 51.0475, lng: 3.7140, label: "STAM Ghent City Museum", num: 1, cat: "activity", desc: "Interactive city history in a medieval abbey" },
        { lat: 51.0560, lng: 3.7195, label: "Design Museum Gent", num: 2, cat: "activity", desc: "Art Nouveau to contemporary design" },
        { lat: 51.0539, lng: 3.7248, label: "Patershol", num: 3, cat: "food", desc: "Cobblestoned restaurant quarter" },
        { lat: 51.0545, lng: 3.7220, label: "Gruut Brewery", num: 4, cat: "food", desc: "Unique gruit beer (no hops)" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "STAM — Ghent City Museum", description: "Ghent's history told through an immersive, modern museum in a medieval abbey complex. Walk across a massive aerial photo of the city on the floor while learning about 1,000 years of history. One of Belgium's best-designed museums.", details: ["📍 Godshuizenlaan 2 · €12"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Simon Says", description: "Ghent's best brunch spot. Creative dishes, specialty coffee, beautiful plating.", meta: "€10-16 · Sluizeken 8" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Design Museum Gent", description: "From Art Nouveau interiors to contemporary Belgian design. Beautiful rooms, thoughtful exhibitions. Belgium punches above its weight in design.", details: ["📍 Jan Breydelstraat 5 · €10"] },
            { title: "Patershol & Gruut Brewery", description: "Wander Ghent's oldest neighborhood — cobblestoned lanes crammed with restaurants. Visit Gruut Brewery — uniquely brews with gruit (herb mixture) instead of hops, like medieval brewers did.", details: ["📍 Grote Huidevettershoek 10 · Tour + tasting €11"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "De Vitrine", description: "Modern European in a gorgeous greenhouse-like space. Seasonal menu, wine-focused, genuinely excellent food.", meta: "€30-45 · Groentenmarkt" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 16,
      title: "Ghent — Markets, Street Art & Vegetarian Capital",
      neighborhoods: "Groentenmarkt · Sint-Jacobs · Blaarmeersen",
      date: "Jun 16",
      mapPins: [
        { lat: 51.0555, lng: 3.7175, label: "Groentenmarkt", num: 1, cat: "food", desc: "Daily market with local produce" },
        { lat: 51.0570, lng: 3.7150, label: "Sint-Jacobs Flea Market", num: 2, cat: "activity", desc: "Weekend flea market" },
        { lat: 51.0548, lng: 3.7215, label: "Street Art Walk", num: 3, cat: "activity", desc: "Guided or self-guided mural tour" },
        { lat: 51.0370, lng: 3.6870, label: "Blaarmeersen", num: 4, cat: "activity", desc: "Lake beach and recreation" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Markets Morning", description: "Groentenmarkt (daily) for local cheese, charcuterie, and fresh produce. If it's the weekend, Sint-Jacobs hosts a massive flea market with everything from antique maps to vintage clothes.", details: [] },
            { title: "Ghent Street Art Tour", description: "Self-guided or with Sorry Not Sorry tours. Ghent's street art scene rivals Bristol and Berlin. Beyond Graffiti Street, entire neighborhoods are open-air galleries.", details: ["💡 Download the Ghent Street Art map from the tourist office."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Julie's House", description: "Charming brunch spot in a canal-side house. Pancakes, eggs, fresh juices.", meta: "€10-15 · Kraanlei 13" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Veggie Day / Vegetarian Ghent", description: "Ghent is officially the 'veggie capital of Europe' — Thursday is Donderdag Veggiedag (Veggie Thursday). Even non-veggie days, the plant-based food scene is exceptional. Try Komkommertijd for creative vegetarian cuisine.", details: [] },
            { title: "Blaarmeersen (if warm)", description: "Ghent's urban lake beach — swimming, kayaking, lounging. Locals flock here on warm days. Pack a picnic.", details: ["📍 Tram from center · €5 entry in summer"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Komkommertijd", description: "Ghent's best vegetarian restaurant. Creative, seasonal, zero gimmicks. Even carnivores rave.", meta: "€20-30 · Reep 57" }
          ],
          tips: [{ type: "reddit", text: "Ghent's veggie scene is no joke. Komkommertijd even converts the most skeptical meat eaters.", cite: "r/ghent" }]
        }
      ]
    },
    {
      num: 17,
      title: "Ghent — Sint-Baafs & Hidden Gems",
      neighborhoods: "City Center · University Quarter",
      date: "Jun 17",
      mapPins: [
        { lat: 51.0543, lng: 3.7174, label: "St. Bavo's Cathedral (revisit)", num: 1, cat: "activity", desc: "Crypt and full cathedral tour" },
        { lat: 51.0510, lng: 3.7265, label: "Sint-Pietersabdij", num: 2, cat: "activity", desc: "Ancient Benedictine abbey" },
        { lat: 51.0580, lng: 3.7230, label: "Kraanlei Canal", num: 3, cat: "activity", desc: "Beautiful canal walk" },
        { lat: 51.0520, lng: 3.7190, label: "De Dulle Griet", num: 4, cat: "food", desc: "Famous for Max beer glass tradition" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "St. Bavo's Crypt & Full Cathedral", description: "Beyond the Altarpiece, the cathedral has a massive crypt with Romanesque foundations, Rubens paintings, and important tombstones. The full building deserves more time than most give it.", details: ["📍 Cathedral free · Altarpiece €16 · Crypt included"] },
            { title: "Sint-Pietersabdij", description: "Thousand-year-old Benedictine abbey with beautiful gardens and rotating exhibitions. The grounds are peaceful and often host summer events.", details: ["📍 Sint-Pietersplein 9 · Free gardens · Exhibition €8"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Café Parti", description: "Cozy neighborhood café in the university quarter. Good coffee, homemade cake.", meta: "€6-10" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Kraanlei Canal Walk", description: "One of Ghent's most beautiful canal stretches. Ornate house facades, each with a story. Look for the decorated almshouses (godshuyzen) — charitable housing from centuries past, now atmospheric courtyards.", details: [] },
            { title: "De Dulle Griet", description: "Famous beer pub with a tradition: order the house Max beer (served in a massive glass) and you must surrender one shoe as deposit. It hangs in a basket above the bar until you return the glass. 500+ beers, serious and silly simultaneously.", details: ["📍 Vrijdagmarkt 50 · €4-8 per beer"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Brasserie HA'", description: "Contemporary brasserie on Korenmarkt. Great people-watching, solid Belgian-French menu, canal views.", meta: "€25-40 · Korenmarkt" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 18,
      title: "Day Trip — Ypres & Flanders Fields",
      neighborhoods: "Ypres (Ieper)",
      date: "Jun 18",
      mapPins: [
        { lat: 50.8513, lng: 2.8875, label: "In Flanders Fields Museum", num: 1, cat: "activity", desc: "WWI museum in medieval Cloth Hall" },
        { lat: 50.8532, lng: 2.8910, label: "Menin Gate", num: 2, cat: "activity", desc: "Memorial to missing soldiers — Last Post ceremony every evening" },
        { lat: 50.8600, lng: 2.9500, label: "Tyne Cot Cemetery", num: 3, cat: "activity", desc: "Largest Commonwealth war cemetery" },
        { lat: 50.8500, lng: 2.8850, label: "Grote Markt Ypres", num: 4, cat: "food", desc: "Rebuilt Cloth Hall and market square" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Train to Ypres", description: "1h45 from Ghent (change at Kortrijk). Ypres was the epicenter of WWI's Western Front — completely destroyed and painstakingly rebuilt. The journey is sobering and essential.", details: ["📍 Ghent → Kortrijk → Ieper · ~1h45"] },
            { title: "In Flanders Fields Museum", description: "Housed in the reconstructed medieval Cloth Hall. One of the world's finest WWI museums — interactive, deeply personal, focusing on individual stories from all sides. You receive a bracelet linked to a real person's wartime experience. Emotionally devastating and brilliantly done.", details: ["📍 Grote Markt · €12 · Allow 2-3 hours"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Grote Markt café", description: "Simple lunch in the rebuilt square. The architecture looks medieval but is entirely 1920s reconstruction — a testament to Ypres' resilience.", meta: "€12-20" }
          ],
          tips: [{ type: "tip", text: "The In Flanders Fields Museum will move you deeply. Bring tissues. It's designed to honor individual humanity amid industrial slaughter." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Tyne Cot Cemetery", description: "The largest Commonwealth war cemetery in the world — 11,961 graves stretching across a hillside. The scale is staggering. The Wall of the Missing lists 34,957 additional names. Standing here, the human cost of war becomes viscerally real. Bus from Ypres or taxi (15 min).", details: ["📍 Free · Bus or taxi from Ypres · 15 min"] },
            { title: "Menin Gate — Last Post Ceremony (8pm)", description: "Every evening since 1928 — without a single break except during German occupation — buglers play the Last Post at the Menin Gate at 8pm. The gate lists 54,896 names of soldiers whose bodies were never found. The ceremony is simple, solemn, and unforgettable. Arrive by 7:45 for a good spot.", details: ["📍 Menin Gate · Free · 8pm daily · Arrive early"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "In 't Klein Stadhuis", description: "Traditional Flemish restaurant on Ypres' Grote Markt. Hearty stews, local beer, honest food after an emotional day.", meta: "€20-35 · Grote Markt" }
          ],
          tips: [{ type: "reddit", text: "The Last Post at Menin Gate is one of the most powerful things you'll experience in Belgium. Don't miss it.", cite: "r/travel" }]
        }
      ]
    },
    {
      num: 19,
      title: "Ghent — Rest Day & Move to Antwerp",
      neighborhoods: "Ghent → Antwerp",
      date: "Jun 19",
      mapPins: [
        { lat: 51.0530, lng: 3.7200, label: "Ghent center (morning)", num: 1, cat: "activity", desc: "Last stroll" },
        { lat: 51.0500, lng: 3.7100, label: "Gent-Sint-Pieters Station", num: 2, cat: "activity", desc: "Train to Antwerp" },
        { lat: 51.2172, lng: 4.4212, label: "Antwerp Central Station", num: 3, cat: "activity", desc: "Cathedral of railways" },
        { lat: 51.2209, lng: 4.4014, label: "Grote Markt Antwerp", num: 4, cat: "food", desc: "Brabo fountain and guild houses" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Slow Ghent Morning", description: "No agenda. Coffee by a canal, last visit to a favorite spot, pack up. Ghent's rhythm is perfect for doing nothing.", details: [] },
            { title: "Train to Antwerp", description: "1 hour direct. Antwerp is a completely different energy — port city, fashion capital, diamond district, Rubens' home.", details: ["📍 Gent-Sint-Pieters → Antwerp Central · 1h · €11"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Ghent canal-side café", description: "Final Ghent coffee.", meta: "" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Arrive at Antwerp Central Station", description: "Often called the world's most beautiful railway station — and the title is deserved. The cathedral-like main hall with marble, gilt, and a massive clock is breathtaking. Take a moment to just look up before heading out.", details: [] },
            { title: "Grote Markt & Cathedral", description: "Antwerp's guild-house-lined square with the Brabo fountain (a giant throwing a severed hand — it's the origin myth of Antwerp's name). The Cathedral of Our Lady looms behind with multiple Rubens masterpieces inside.", details: ["📍 Cathedral: €12 · Rubens' Descent from the Cross is the star"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Fiskebar", description: "Antwerp's best seafood — sleek, modern, Nordic-influenced. Raw bar, crudo, grilled whole fish. The food scene in Antwerp is Belgium's best.", meta: "€30-50 · Marnixplaats 12" }
          ],
          tips: [{ type: "reddit", text: "Antwerp has the best food scene in Belgium, hands down. It's where Belgian chefs come to push boundaries.", cite: "r/belgium" }]
        }
      ]
    },
    // === ANTWERP (Days 20-25) ===
    {
      num: 20,
      title: "Antwerp — Rubens, Cathedral & Diamond District",
      neighborhoods: "City Center · Diamond District · Meir",
      date: "Jun 20",
      mapPins: [
        { lat: 51.2203, lng: 4.4015, label: "Cathedral of Our Lady", num: 1, cat: "activity", desc: "Rubens' Descent from the Cross" },
        { lat: 51.2147, lng: 4.4080, label: "Rubenshuis", num: 2, cat: "activity", desc: "Peter Paul Rubens' house-studio" },
        { lat: 51.2178, lng: 4.4198, label: "Diamond District", num: 3, cat: "activity", desc: "World diamond capital" },
        { lat: 51.2160, lng: 4.4110, label: "Meir Shopping Street", num: 4, cat: "activity", desc: "Antwerp's main shopping avenue" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Cathedral of Our Lady", description: "Belgium's largest Gothic church, home to four Rubens paintings — the Descent from the Cross and the Raising of the Cross are monumental, theatrical, emotionally overwhelming. Rubens was Antwerp's most famous citizen, and these works justify a trip to the city alone.", details: ["📍 Groenplaats · €12 · Opens 10am"] },
            { title: "Rubenshuis", description: "Rubens' 17th-century mansion-studio, restored to its Baroque splendor. Rubens was an artist, diplomat, intellectual, and one of the richest men in Flanders. The house reflects all of it — art-filled rooms, an Italian-style garden, and the famous studio where assistants helped produce thousands of paintings.", details: ["📍 Wapper 9-11 · €12 · Timed tickets, book ahead"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Caffènation", description: "Antwerp's best coffee roasters. Third-wave specialty coffee in an industrial-chic space.", meta: "€5-10 · Hopland 46" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Diamond District", description: "Antwerp handles 84% of the world's rough diamonds. The quarter around the station is lined with diamond dealers and exchanges. Visit DIVA (diamond museum) for a dazzling journey through 500 years of Antwerp's diamond and silversmith heritage.", details: ["📍 DIVA Museum: Suikerrui 17-19 · €12"] },
            { title: "Meir & Shopping", description: "Antwerp's main shopping avenue in a string of ornate buildings. For Belgian fashion: the ModeNatie area around Nationalestraat — the Antwerp Six (Dries Van Noten, Ann Demeulemeester, etc.) put Belgian fashion on the world map.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "The Jane", description: "One of Belgium's most dramatic dining rooms — a converted chapel with stained glass. Chef Nick Bril's Asian-influenced cuisine in a Michelin-starred setting. The upper communion (bar area) is more casual and doesn't require reservation.", meta: "€40-60 (upper communion) · Paradeplein 1 · Reserve" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 21,
      title: "Antwerp — MAS, Port & Het Zuid",
      neighborhoods: "Eilandje · Het Zuid · Zurenborg",
      date: "Jun 21",
      mapPins: [
        { lat: 51.2292, lng: 4.4046, label: "MAS Museum", num: 1, cat: "activity", desc: "Museum aan de Stroom — rooftop panorama" },
        { lat: 51.2060, lng: 4.3900, label: "KMSKA", num: 2, cat: "activity", desc: "Royal Museum of Fine Arts — reopened after 11-year renovation" },
        { lat: 51.2050, lng: 4.3935, label: "Het Zuid neighborhood", num: 3, cat: "food", desc: "Antwerp's art gallery district" },
        { lat: 51.2020, lng: 4.4265, label: "Zurenborg", num: 4, cat: "activity", desc: "Art Nouveau architecture district" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "MAS — Museum aan de Stroom", description: "Striking red sandstone tower on the old port. Take the escalator to the free rooftop for the best panoramic view in Antwerp — the city, the Scheldt river, and the massive port. The museum inside covers Antwerp's history as a world trading hub.", details: ["📍 Hanzestedenplaats 1 · Rooftop free · Museum €10"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Normo", description: "Third-wave coffee and raw food café in the trendy Eilandje port district.", meta: "€8-12 · Minderbroedersrui 30" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "KMSKA — Royal Museum of Fine Arts", description: "Reopened in 2022 after an 11-year renovation. Blockbuster collection: Van Eyck, Rubens, Jordaens, Ensor, Magritte, plus Fouquet's extraordinary Madonna. The building itself is transformed — old masters in classical galleries, modern art in new white spaces. Allow 3 hours.", details: ["📍 Leopold de Waelplaats 2 · €20 · Timed tickets"] },
            { title: "Zurenborg Architecture Walk", description: "A neighborhood of Art Nouveau and eclectic architecture near Berchem station. Cogels-Osylei is the highlight — a street where every house tries to outdo its neighbor in ornamental exuberance. A gem that few tourists visit.", details: ["📍 Tram 11 to Berchem · Walk Cogels-Osylei"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Barnini", description: "Italian-Antwerp fusion in Het Zuid. Amazing pasta, buzzing atmosphere, wine bar next door. The neighborhood gallery-hopping crowd eats here.", meta: "€20-35 · Graaf van Egmontstraat 27" }
          ],
          tips: [{ type: "tip", text: "KMSKA is one of Europe's great art museums. The reopening made it world-class in presentation too. Book timed tickets online." }]
        }
      ]
    },
    {
      num: 22,
      title: "Antwerp — Fashion, Food & Local Life",
      neighborhoods: "Nationalestraat · Sint-Andries · Kloosterstraat",
      date: "Jun 22",
      mapPins: [
        { lat: 51.2135, lng: 4.3975, label: "MoMu Fashion Museum", num: 1, cat: "activity", desc: "The Antwerp Six and Belgian fashion" },
        { lat: 51.2110, lng: 4.3950, label: "Kloosterstraat", num: 2, cat: "activity", desc: "Antiques, vintage, galleries" },
        { lat: 51.2200, lng: 4.3990, label: "Plantin-Moretus Museum", num: 3, cat: "activity", desc: "UNESCO — world's oldest printing presses" },
        { lat: 51.2180, lng: 4.3960, label: "De Groote Witte Arend", num: 4, cat: "food", desc: "Hidden courtyard beer café" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "MoMu — Fashion Museum", description: "Antwerp is a world fashion capital thanks to the Antwerp Six — designers who stormed Paris in the 1980s. MoMu tells their story and showcases rotating exhibitions from Belgium's fashion avant-garde. Even non-fashion people find it fascinating.", details: ["📍 Nationalestraat 28 · €10"] },
            { title: "Kloosterstraat", description: "Antwerp's best street for antiques, vintage furniture, independent galleries, and quirky design shops. Every store is curated and interesting. Perfect browsing territory.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "De Groote Witte Arend", description: "Hidden courtyard café in a former abbey. Beautiful space, good pastries, peaceful morning start.", meta: "€8-12 · Reyndersstraat 18" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Plantin-Moretus Museum", description: "The only museum on the UNESCO World Heritage list. A 16th-century printing house with the world's oldest printing presses still in situ. Rubens did the company's typography. The library, the courtyard, the press room — everything is original. Utterly unique.", details: ["📍 Vrijdagmarkt 22 · €12"] },
            { title: "Rest & Wander", description: "Antwerp is a city for aimless walking. Explore streets you haven't seen. Duck into bars. Belgium's best vintage shops are here.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Balls & Glory", description: "Belgian comfort concept — massive meatballs (or veggie balls) with seasonal stoemp (mash). Simple, hearty, fun.", meta: "€15-20 · Nationalestraat 4" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 23,
      title: "Day Trip — Mechelen & Leuven",
      neighborhoods: "Mechelen · Leuven",
      date: "Jun 23",
      mapPins: [
        { lat: 51.0280, lng: 4.4796, label: "St. Rumbold's Cathedral", num: 1, cat: "activity", desc: "97m tower — 514 steps, incredible views" },
        { lat: 51.0270, lng: 4.4770, label: "Mechelen Grote Markt", num: 2, cat: "food", desc: "Beautiful Flemish square" },
        { lat: 50.8798, lng: 4.7005, label: "Oude Markt Leuven", num: 3, cat: "food", desc: "Longest bar in Europe" },
        { lat: 50.8790, lng: 4.7015, label: "Stella Artois Brewery", num: 4, cat: "food", desc: "Visit the homeland of Stella" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Mechelen", description: "A 20-min train from Antwerp. This charming Flemish city was once the capital of the Low Countries. Climb St. Rumbold's Tower (514 steps, 97m — higher than Bruges' Belfry) for panoramic views. The Grote Markt is beautiful without the crowds of Bruges. Kazerne Dossin is a powerful Holocaust museum — Mechelen was the transit camp for Belgian Jews.", details: ["📍 Antwerp → Mechelen · 20 min · Tower €10"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Mechelen Grote Markt", description: "Pick a terrace on the square. Mechelen's food scene is surprisingly good for its size.", meta: "€12-20" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Leuven", description: "15 min from Mechelen. Europe's oldest Catholic university (1425) — the city runs on student energy. The Oude Markt is called 'the longest bar in Europe' — an entire square ringed with bars. Visit the stunning Gothic town hall and the university library (rebuilt after both World Wars). Stella Artois has been brewed here since 1366.", details: ["📍 Mechelen → Leuven · 15 min"] },
            { title: "Stella Artois Experience", description: "Love it or mock it, Stella is Belgian heritage. The brewery experience covers 600+ years of brewing history in Leuven. Tour ends with tasting — Stella tastes genuinely different fresh from the source.", details: ["📍 De Hoorn · €15 · Book online"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Oude Markt terrace", description: "Grab a table on Europe's longest bar square. Watch the student life swirl around you. Order frites and a local beer.", meta: "€15-25 · Any terrace" }
          ],
          tips: [{ type: "reddit", text: "Leuven is underrated. Great vibe, great food, great beer, no tourists. The Oude Markt on a summer evening is magical.", cite: "r/belgium" }]
        }
      ]
    },
    {
      num: 24,
      title: "Antwerp — Middelheim & Relaxation",
      neighborhoods: "Middelheim · Linkeroever · City Center",
      date: "Jun 24",
      mapPins: [
        { lat: 51.1810, lng: 4.4230, label: "Middelheim Open-Air Museum", num: 1, cat: "activity", desc: "World-class sculpture park — free" },
        { lat: 51.2270, lng: 4.3870, label: "Linkeroever (Left Bank)", num: 2, cat: "activity", desc: "Scheldt tunnel pedestrian crossing — skyline views" },
        { lat: 51.2205, lng: 4.4020, label: "Sint-Carolus Borromeus", num: 3, cat: "activity", desc: "Baroque church — Rubens' ceiling" },
        { lat: 51.2150, lng: 4.4050, label: "Cocktail bars", num: 4, cat: "food", desc: "Antwerp's cocktail scene" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Middelheim Open-Air Sculpture Museum", description: "A park filled with world-class contemporary sculpture — Ai Weiwei, Rodin, Henry Moore — spread across lawns, woods, and meadows. Completely free. One of Europe's best sculpture parks. Perfect for a morning walk.", details: ["📍 Middelheimlaan 61 · Free · Tram 7"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Koffie", description: "Minimal, excellent coffee and pastries in the fashion district.", meta: "€5-10 · Kloosterstraat area" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Linkeroever & Sint-Anna Tunnel", description: "Walk through the 1930s Art Deco pedestrian tunnel under the Scheldt to the Left Bank. The city skyline view from across the river is spectacular. Locals picnic on the quays.", details: ["📍 Sint-Annatunnel entrance near Steenplein · Free"] },
            { title: "Evening Cocktails", description: "Antwerp has Belgium's best cocktail scene. Try Dogma (speakeasy vibes), Bar Entrepot (harbor views), or Cocktails at Nine (classic).", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "RAS", description: "Restaurant on the MAS promenade with waterfront views. Belgian-Mediterranean menu, sunset dining.", meta: "€25-40 · Ernest Van Dijckkaai" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 25,
      title: "Antwerp — Last Day & Move to Namur",
      neighborhoods: "Antwerp → Namur",
      date: "Jun 25",
      mapPins: [
        { lat: 51.2200, lng: 4.4050, label: "Antwerp morning", num: 1, cat: "activity", desc: "Final morning stroll" },
        { lat: 51.2172, lng: 4.4212, label: "Antwerp Central", num: 2, cat: "activity", desc: "Train south" },
        { lat: 50.4640, lng: 4.8670, label: "Namur Citadel", num: 3, cat: "activity", desc: "Hilltop fortress above two rivers" },
        { lat: 50.4650, lng: 4.8630, label: "Namur Old Town", num: 4, cat: "food", desc: "Wallonia's charming capital" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Antwerp Morning", description: "Last coffee at your favorite spot. A quick browse of any missed areas. Antwerp always rewards one more wander.", details: [] },
            { title: "Train to Namur", description: "Cross the linguistic border into French-speaking Wallonia. Namur is the capital of Wallonia — smaller, quieter, at the confluence of the Sambre and Meuse rivers. Completely different character from Flanders.", details: ["📍 Antwerp Central → Namur · ~2h (change Brussels) · €20"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Antwerp bakery", description: "Farewell pastry.", meta: "" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Namur Citadel", description: "Massive fortress complex above the city at the meeting of two rivers. Walk or take the cable car up. Panoramic views, underground tunnels, and centuries of military history. The ramparts offer a perfect introduction to Wallonia's dramatic landscape.", details: ["📍 Route Merveilleuse · €6-10 depending on tour"] },
            { title: "Namur Old Town Stroll", description: "Charming pedestrian streets, excellent chocolateries, and the start of your French-speaking Belgian chapter. The pace slows down here — Wallonia runs on a different clock.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "La Plage d'Amée", description: "Riverside restaurant with terrace overlooking the Meuse. French-Belgian cuisine — think duck confit, river fish, and excellent wine. A romantic dinner to start Wallonia.", meta: "€30-45 · Along the Meuse" }
          ],
          tips: [{ type: "tip", text: "Wallonia feels like a different country — French-speaking, more rural, closer to France in culture. Prices drop, pace slows, landscapes get more dramatic." }]
        }
      ]
    },
    // === WALLONIA & ARDENNES (Days 26-37) ===
    {
      num: 26,
      title: "Dinant — Saxophone City & River Cliffs",
      neighborhoods: "Dinant",
      date: "Jun 26",
      mapPins: [
        { lat: 50.2603, lng: 4.9125, label: "Dinant Citadel", num: 1, cat: "activity", desc: "Dramatic cliff-top fortress" },
        { lat: 50.2595, lng: 4.9138, label: "Collegiate Church", num: 2, cat: "activity", desc: "Gothic church with onion dome below cliffs" },
        { lat: 50.2585, lng: 4.9102, label: "Adolphe Sax House", num: 3, cat: "activity", desc: "Birthplace of the saxophone's inventor" },
        { lat: 50.2540, lng: 4.9100, label: "Meuse River Cruise", num: 4, cat: "activity", desc: "Boat trip through limestone gorges" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Dinant", description: "30 min by train from Namur. One of Belgium's most dramatically situated towns — a Gothic church with a bulbous dome wedged between towering limestone cliffs and the Meuse river, with a citadel perched above. The birthplace of Adolphe Sax (saxophone inventor) — colorful sax statues line the bridge.", details: ["📍 Namur → Dinant · 30 min · €5"] },
            { title: "Dinant Citadel", description: "Take the cable car (or climb 408 steps) to the cliff-top fortress. Views are extraordinary — the Meuse snaking through limestone gorges below. The history is turbulent: destroyed and rebuilt many times over a millennium.", details: ["📍 €10 combined citadel + cable car"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Riverside café", description: "Dinant's riverside has several terraces. Try a Flamiche — a local cheese tart that's a Dinant specialty.", meta: "€12-20" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Meuse River Cruise", description: "45-minute boat trip through the limestone Meuse gorges. Dramatic cliffs, castles on hills, peaceful villages. The landscape is nothing like Flanders — this is Belgium's wild, romantic side.", details: ["📍 Departure from Dinant quay · €10-15 · Check seasonal schedules"] },
            { title: "Couque de Dinant", description: "Dinant's signature — an extremely hard honey biscuit pressed into decorative wooden molds. It's been made here since the Middle Ages. Buy some at Jacobs or Collignon — they make unique edible souvenirs.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Back in Namur", description: "Return to Namur for dinner. Try L'Espièglerie — creative French-Belgian cuisine in the old town.", meta: "€25-40 · Rue de la Halle · Namur" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 27,
      title: "Durbuy — World's Smallest City",
      neighborhoods: "Durbuy · Ourthe Valley",
      date: "Jun 27",
      mapPins: [
        { lat: 50.3530, lng: 5.4567, label: "Durbuy Old Town", num: 1, cat: "activity", desc: "Officially the world's smallest city" },
        { lat: 50.3550, lng: 5.4590, label: "Durbuy Castle", num: 2, cat: "activity", desc: "11th-century castle overlooking the town" },
        { lat: 50.3520, lng: 5.4530, label: "Topiary Park", num: 3, cat: "activity", desc: "250+ sculpted boxwood shapes" },
        { lat: 50.3510, lng: 5.4555, label: "Ourthe River", num: 4, cat: "activity", desc: "Kayaking and riverside walks" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive/Bus to Durbuy", description: "Nestled in the Ourthe river valley, Durbuy holds the title of 'world's smallest city' — a medieval cluster of stone houses, cobblestoned lanes, and a castle, home to just 500 people. It's irresistibly charming. Best reached by car or bus from Barvaux (train from Namur, 1h15).", details: ["📍 Namur → Barvaux (train 1h15) → Durbuy (bus 15 min)"] },
            { title: "Old Town Walk", description: "The entire old town takes 20 minutes to walk end-to-end, but you'll spend hours. Stone houses dating to the 14th century, tiny artisan shops, the castle looming above. The Topiary Park has 250+ boxwood sculptures shaped into animals, geometric forms, and abstract art.", details: ["📍 Topiary Park: €10"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Le Sanglier des Ardennes", description: "Durbuy's most famous restaurant — Ardennes cuisine: game, wild boar, foraged mushrooms. The region's terroir is completely different from Flanders.", meta: "€25-40 · Grand Rue" }
          ],
          tips: [{ type: "tip", text: "Durbuy gets busy on weekends. Weekday visits are more pleasant and accommodations cheaper." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Ourthe River Activities", description: "Kayaking the Ourthe is one of the Ardennes' classic experiences. Several outfitters run trips from Barvaux to Durbuy — gentle rapids, forested banks, castle views. Or just walk the riverside path.", details: ["💡 Kayak rentals: ~€20-25 per person for a 2-3 hour descent"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Local Durbuy restaurant", description: "Stay the night in Durbuy if possible — the town empties after day-trippers leave and becomes magical.", meta: "" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 28,
      title: "Ardennes — La Roche & Forested Hills",
      neighborhoods: "La Roche-en-Ardenne · Ourthe Valley",
      date: "Jun 28",
      mapPins: [
        { lat: 50.1834, lng: 5.5757, label: "La Roche Castle", num: 1, cat: "activity", desc: "11th-century ruins above the town" },
        { lat: 50.1830, lng: 5.5750, label: "La Roche town center", num: 2, cat: "food", desc: "Charming Ardennes market town" },
        { lat: 50.1800, lng: 5.5730, label: "Battle of the Bulge Museum", num: 3, cat: "activity", desc: "WWII Ardennes Offensive history" },
        { lat: 50.1850, lng: 5.5780, label: "Forest hiking trails", num: 4, cat: "activity", desc: "Marked trails through deep forest" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "La Roche-en-Ardenne", description: "A quintessential Ardennes town — huddled in a deep valley, medieval castle ruins on the hill, forests pressing in from all sides. The Battle of the Bulge museum covers the area's devastating WWII history. The castle ruins are atmospheric and offer panoramic views.", details: ["📍 Castle: €5 · Battle museum: €7"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Local boulangerie", description: "Fresh croissants and coffee in a real Walloon village bakery.", meta: "€5-8" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Forest Hiking", description: "The Ardennes is Belgium's hiking heartland. Marked trails (GR routes) wind through deep beech and oak forests, across streams, past hidden chapels. The Promenade Natura (6km, easy) loops through forest and offers viewpoints. For more challenge, the GR 57 follows the Ourthe valley.", details: ["💡 Pick up trail maps at the La Roche tourist office."] },
            { title: "Ardennes Ham Tasting", description: "Jambon d'Ardenne — dry-cured, smoked ham, Belgium's PDO-protected specialty. Local butchers and farms sell it alongside artisanal pâtés and game terrines. Pick up provisions for a picnic dinner.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Forest picnic or local restaurant", description: "Either a charcuterie-and-cheese picnic in a meadow, or a hearty game stew at a village restaurant. The Ardennes' culinary identity is forest, game, and terroir.", meta: "" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 29,
      title: "Bastogne — Battle of the Bulge",
      neighborhoods: "Bastogne",
      date: "Jun 29",
      mapPins: [
        { lat: 50.0009, lng: 5.7164, label: "Bastogne War Museum", num: 1, cat: "activity", desc: "Immersive WWII experience" },
        { lat: 50.0080, lng: 5.7230, label: "Mardasson Memorial", num: 2, cat: "activity", desc: "Star-shaped memorial to American soldiers" },
        { lat: 49.9990, lng: 5.7150, label: "McAuliffe Square", num: 3, cat: "activity", desc: "Where General McAuliffe said 'Nuts!'" },
        { lat: 50.0050, lng: 5.7200, label: "Bastogne Barracks", num: 4, cat: "activity", desc: "Underground command post" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Bastogne War Museum", description: "One of Europe's best WWII museums. The Bastogne story is legendary: during the Battle of the Bulge (Dec 1944), German forces surrounded the town. When asked to surrender, General McAuliffe replied with one word: 'Nuts!' The museum tells the full story through immersive scenes, personal testimonies, and original artifacts.", details: ["📍 Colline du Mardasson · €16 · Allow 3 hours"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "McAuliffe Square", description: "Lunch in the town center where the famous reply was given. Local restaurants serve Ardennes fare.", meta: "€12-20" }
          ],
          tips: [{ type: "tip", text: "Bastogne is deeply emotional — especially the personal stories of civilians and soldiers on all sides. The museum is masterfully done." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Mardasson Memorial", description: "Star-shaped memorial honoring 76,890 American soldiers killed, wounded, or missing in the Battle of the Bulge. The views from the hilltop sweep across the Ardennes forests where the battle raged. A crypt below has mosaics designed by Fernand Léger.", details: ["📍 Adjacent to museum · Free"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Wagon-Léo", description: "Classic Bastogne restaurant. Hearty Ardennes game dishes, local beers, warm atmosphere after a heavy day.", meta: "€20-35 · Rue du Vivier" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 30,
      title: "Bouillon — Medieval Fortress & Semois Valley",
      neighborhoods: "Bouillon · Semois River",
      date: "Jun 30",
      mapPins: [
        { lat: 49.7937, lng: 5.0672, label: "Bouillon Castle", num: 1, cat: "activity", desc: "Belgium's most spectacular castle" },
        { lat: 49.7940, lng: 5.0690, label: "Bouillon Town", num: 2, cat: "food", desc: "Tiny riverside town below the castle" },
        { lat: 49.7920, lng: 5.0650, label: "Semois River", num: 3, cat: "activity", desc: "Kayaking and river walks" },
        { lat: 49.8100, lng: 5.0400, label: "Tombeau du Géant viewpoint", num: 4, cat: "activity", desc: "Iconic Ardennes panorama" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Bouillon Castle", description: "Belgium's most spectacular castle — a massive medieval fortress clinging to a rocky ridge above a tight bend in the Semois river. Once home to Godfrey of Bouillon, leader of the First Crusade (1096). The falconry display on the castle grounds features owls, hawks, and eagles in flight. The views of the river valley are breathtaking.", details: ["📍 €10 · Falconry shows at set times · Check schedule"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Riverside terrace", description: "Bouillon's Semois riverfront has charming cafés. Try local trout — the Semois is famous for it.", meta: "€12-25" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Semois Kayaking or Walk", description: "The Semois river winds through deep forest gorges — kayaking here is an Ardennes classic. Several outfitters run trips from Bouillon. Or walk the riverside path for forest and river views without the paddle.", details: ["💡 Kayak rental: ~€15-25 per person"] },
            { title: "Tombeau du Géant", description: "Belgium's most famous viewpoint. A river meander creates a hill that looks like a giant's tomb — the panorama is iconic Ardennes. Best at sunset.", details: ["📍 5 min drive from Bouillon · Signposted"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Auberge du Moulin Hideux", description: "Rustic-elegant restaurant in a converted mill. Ardennes game, local mushrooms, seasonal foraged ingredients. A gastronomic highlight of the region.", meta: "€35-55 · Book ahead · Route de Dohan" }
          ],
          tips: [{ type: "reddit", text: "Bouillon Castle is Belgium's most underrated attraction. The falconry show alone is worth the trip.", cite: "r/travel" }]
        }
      ]
    },
    {
      num: 31,
      title: "Spa — The Original Spa Town",
      neighborhoods: "Spa · Hautes Fagnes",
      date: "Jul 1",
      mapPins: [
        { lat: 50.4890, lng: 5.8658, label: "Thermes de Spa", num: 1, cat: "activity", desc: "Hilltop thermal baths" },
        { lat: 50.4880, lng: 5.8670, label: "Spa town center", num: 2, cat: "food", desc: "The original wellness town" },
        { lat: 50.5550, lng: 6.0700, label: "Hautes Fagnes", num: 3, cat: "activity", desc: "Belgium's highest plateau — moorland walks" },
        { lat: 50.4430, lng: 5.9726, label: "Spa-Francorchamps Circuit", num: 4, cat: "activity", desc: "Legendary F1 track (drive-by)" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Thermes de Spa", description: "The word 'spa' literally comes from this town — people have been coming here for thermal waters since Roman times. The modern Thermes de Spa sits on a hill with indoor/outdoor pools, saunas, steam rooms, and treatments all using the natural mineral-rich spring water. A genuine day of relaxation after weeks of sightseeing.", details: ["📍 Colline d'Annette et Lubin · €38 for 3 hours · Funicular from town"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Spa town bakery", description: "Quiet morning start before the thermal baths.", meta: "€5-10" }
          ],
          tips: [{ type: "tip", text: "The thermal baths are the real deal — the water has been analyzed since the 16th century. Bring swimwear and allow 3+ hours to fully relax." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Hautes Fagnes Nature Reserve", description: "Belgium's highest point and most unique landscape — a sub-Arctic moorland plateau at 694m. Boardwalk trails cross peat bogs, heathland, and dark spruce forest. It feels like Scotland, not Belgium. The Signal de Botrange marks Belgium's highest point (694m) — charmingly, they built a staircase to make it an even 700m.", details: ["📍 30 min drive from Spa · Free · Boardwalk trails 3-12km"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Source de Barisart", description: "Restaurant near one of Spa's historic springs. Traditional Walloon cuisine with a wellness town refinement.", meta: "€25-40" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 32,
      title: "Liège — Industrial City with a Heart",
      neighborhoods: "Liège city center",
      date: "Jul 2",
      mapPins: [
        { lat: 50.6292, lng: 5.5797, label: "Montagne de Bueren", num: 1, cat: "activity", desc: "374 steps up a cliff in the city center" },
        { lat: 50.6408, lng: 5.5666, label: "Liège-Guillemins Station", num: 2, cat: "activity", desc: "Santiago Calatrava's spectacular station" },
        { lat: 50.6308, lng: 5.5700, label: "La Batte Sunday Market", num: 3, cat: "food", desc: "Belgium's largest open-air market" },
        { lat: 50.6398, lng: 5.5726, label: "Le Carré", num: 4, cat: "food", desc: "Nightlife and restaurant district" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Liège-Guillemins Station", description: "Even if you arrive by car, detour to see Santiago Calatrava's railway station — a white, swooping, bone-like structure of steel and glass. Arguably the most beautiful modern railway station in Europe.", details: [] },
            { title: "Montagne de Bueren", description: "374 steps straight up a cliff face in the middle of the city. Built in 1881 to connect the garrison to the city center. The climb is steep but the view from the top is rewarding — Liège spreads out along the Meuse valley below.", details: ["📍 Free · Bring water and good shoes"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Liège waffle from a street vendor", description: "The Liège waffle (gaufre de Liège) is denser, sweeter, and more caramelized than the Brussels version. Buy one from a street cart — it's the definitive Belgian waffle experience.", meta: "€2-4 · Street carts throughout center" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Old Town & Le Carré", description: "Liège is gritty, real, and full of character — the anti-Bruges. The old town around Le Carré has excellent restaurants and bars. The Prince-Bishops' Palace courtyard is impressive. Liège is Wallonia's largest city and has a proud, independent spirit.", details: [] },
            { title: "Grand Curtius Museum", description: "Liège's main museum — archaeology, decorative arts, weapons, and religious art in a stunning Renaissance mansion. The glasswork and Mosan metalwork collections are world-class.", details: ["📍 Féronstrée 136 · €9"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Le Carré restaurant", description: "Le Carré is Liège's going-out district. For authentic Liégeois cuisine, try boulets à la liégeoise (meatballs in sweet-sour sauce with sirop de Liège) at any local bistro.", meta: "€15-30" }
          ],
          tips: [{ type: "reddit", text: "Liège is Belgium's most underrated city. Skip the tourist stuff and eat boulets — that's the real Liège experience.", cite: "r/belgium" }]
        }
      ]
    },
    {
      num: 33,
      title: "Ardennes — Trappist Abbey & Forest Day",
      neighborhoods: "Orval · Ardennes Forest",
      date: "Jul 3",
      mapPins: [
        { lat: 49.6336, lng: 5.3486, label: "Orval Abbey", num: 1, cat: "activity", desc: "Trappist abbey — beer, cheese, ruins" },
        { lat: 49.6340, lng: 5.3500, label: "Abbey Ruins", num: 2, cat: "activity", desc: "12th-century Cistercian ruins" },
        { lat: 49.8100, lng: 5.2500, label: "Gaume region", num: 3, cat: "activity", desc: "Belgium's sunniest region" },
        { lat: 49.7000, lng: 5.4000, label: "Forest trails", num: 4, cat: "activity", desc: "Deep Ardennes walking" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Orval Abbey", description: "One of the world's six Trappist breweries in Belgium. The abbey produces Orval — a distinctive, funky amber ale unlike any other. The medieval ruins (12th-century Cistercian) are atmospheric and beautiful. The shop sells Orval beer and the abbey's handmade cheese. A pilgrimage for beer lovers and history buffs alike.", details: ["📍 Southern Ardennes · Ruins €7 · Best by car", "💡 The abbey itself is closed to visitors (monks' privacy) but the ruins and grounds are open."] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "À l'Ange Gardien", description: "Restaurant near the abbey serving dishes made with Orval beer and cheese. The regional cuisine here is excellent and deeply connected to the abbey's products.", meta: "€15-30 · Near Orval" }
          ],
          tips: [{ type: "tip", text: "Orval is considered one of the world's greatest beers. Buy some at the abbey shop — it tastes different fresh from the source." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Gaume Region", description: "Belgium's southernmost corner — called the Belgian Provence for its (relatively) warm climate. Rolling farmland, stone villages, vineyards beginning to appear. It's the most French-feeling part of Belgium.", details: [] },
            { title: "Forest Walk", description: "The deep Ardennes forests are therapeutic. Pick any marked trail — GR routes are well-maintained. Beech, oak, and spruce forests, sometimes with wild boar sightings. The silence is restorative.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Gaume village restaurant", description: "Simple Walloon farmhouse cooking — grilled meats, seasonal vegetables, local beer and wine.", meta: "€20-35" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 34,
      title: "Rochefort & Han-sur-Lesse Caves",
      neighborhoods: "Rochefort · Han-sur-Lesse",
      date: "Jul 4",
      mapPins: [
        { lat: 50.1598, lng: 5.2219, label: "Rochefort town", num: 1, cat: "food", desc: "Another Trappist beer town" },
        { lat: 50.1268, lng: 5.1872, label: "Han-sur-Lesse Caves", num: 2, cat: "activity", desc: "Spectacular stalactite caves" },
        { lat: 50.1280, lng: 5.1890, label: "Wildlife Park", num: 3, cat: "activity", desc: "European wildlife in natural habitat" },
        { lat: 50.1600, lng: 5.2200, label: "Rochefort Abbey (nearby)", num: 4, cat: "activity", desc: "Trappist brewery (closed to public, beer available in town)" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Rochefort", description: "A small Ardennes town famous for Rochefort Trappist ales (6, 8, and 10 — the 10 is one of the world's greatest beers). The abbey isn't open to visitors, but every bar and restaurant in town serves Rochefort. It's a pilgrimage just to drink a Rochefort 10 in its hometown.", details: [] },
            { title: "Han-sur-Lesse Caves", description: "Belgium's most spectacular underground attraction. A guided tour through enormous caverns with stalactites, stalagmites, underground rivers, and a cathedral-like chamber. The exit is via a dramatic tram ride through the valley. A family-friendly highlight of the trip.", details: ["📍 Rue Joseph Lamotte · €24 combined caves + tram · 2h tour"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Han-sur-Lesse village", description: "Tourist-friendly village with several cafés. Simple lunch before or after the caves.", meta: "€12-20" }
          ],
          tips: [{ type: "tip", text: "The caves maintain 13°C year-round — bring a jacket even in summer." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Wildlife Park", description: "Adjacent to the caves — a large reserve with European wildlife (bison, bears, wolves, lynx, wild horses) in semi-natural habitats. A nice complement to the cave visit, especially family-friendly.", details: ["📍 €16 or combined ticket with caves"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Rochefort restaurant", description: "Drink a Rochefort 10 with dinner. Game stew, Ardennes ham, local cheese. The perfect end to an underground-and-wildlife day.", meta: "€20-35" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 35,
      title: "Chimay — Trappist Trilogy Complete",
      neighborhoods: "Chimay · Virelles Lake",
      date: "Jul 5",
      mapPins: [
        { lat: 50.0486, lng: 4.3167, label: "Chimay Castle", num: 1, cat: "activity", desc: "Home of the Princes of Chimay" },
        { lat: 50.0600, lng: 4.3200, label: "Espace Chimay", num: 2, cat: "food", desc: "Trappist beer and cheese tasting experience" },
        { lat: 50.0700, lng: 4.3350, label: "Virelles Lake", num: 3, cat: "activity", desc: "Nature reserve with birdwatching" },
        { lat: 50.0480, lng: 4.3150, label: "Chimay town center", num: 4, cat: "food", desc: "Charming town square" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Chimay", description: "Complete your Belgian Trappist trilogy. Chimay is the most commercially well-known Trappist brewery, and the Espace Chimay offers tastings of their beers (Blue, Red, White, Grand Reserve) paired with their exceptional Trappist cheeses. The town is charming — the castle of the Princes of Chimay overlooks the square.", details: ["📍 Espace Chimay: €10-15 for tasting experience"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Espace Chimay or town restaurant", description: "The Espace has a brasserie serving dishes made with Chimay products. The beer-cheese pairing is perfection.", meta: "€15-25" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Virelles Lake Nature Reserve", description: "One of Belgium's most important wetlands — a shallow lake surrounded by marshes, reed beds, and forests. Excellent birdwatching (herons, bitterns, kingfishers). Peaceful walking trails and an observation tower. A serene contrast to the abbey visits.", details: ["📍 €7 · Signed trails from 2-8 km"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Local Chimay bistro", description: "Ardennes country cooking with Chimay beer on tap. Simple, satisfying, authentic.", meta: "€20-30" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 36,
      title: "Tournai — Belgium's Oldest City",
      neighborhoods: "Tournai",
      date: "Jul 6",
      mapPins: [
        { lat: 50.6068, lng: 3.3875, label: "Tournai Cathedral", num: 1, cat: "activity", desc: "UNESCO — 5 towers, Romanesque/Gothic" },
        { lat: 50.6070, lng: 3.3860, label: "Grand-Place Tournai", num: 2, cat: "food", desc: "Charming square with belfry" },
        { lat: 50.6065, lng: 3.3890, label: "Museum of Fine Arts", num: 3, cat: "activity", desc: "Horta-designed museum" },
        { lat: 50.6080, lng: 3.3870, label: "Belfry of Tournai", num: 4, cat: "activity", desc: "Belgium's oldest belfry (UNESCO)" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Tournai", description: "Belgium's oldest city — Clovis, first king of the Franks, was born here. The cathedral has 5 towers visible from miles away and is a UNESCO masterpiece transitioning from Romanesque to Gothic. The belfry is Belgium's oldest (1187). Tournai feels like a hidden gem — significant history, virtually no tourists.", details: ["📍 By car or train from Chimay region · Cathedral: €5 · Belfry: €5"] }
          ],
          meals: [
            { type: "🥖 Lunch", name: "Grand-Place terrace", description: "Tournai's triangular Grand-Place has several welcoming terraces. Local Walloon cuisine.", meta: "€12-20" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Museum of Fine Arts", description: "Designed by Victor Horta himself — the building is art. Contains works by Rogier van der Weyden (born in Tournai), Manet, and Seurat. A small but curated collection.", details: ["📍 €5 · Enclos Saint-Martin"] },
            { title: "Return toward Brussels area", description: "Head back north. The final stretch of the trip will base around Brussels for easy departure logistics.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "En route or Brussels area", description: "Light dinner as you transition back north.", meta: "" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 37,
      title: "Ardennes Recovery & Travel Day",
      neighborhoods: "Transit · Brussels area",
      date: "Jul 7",
      mapPins: [
        { lat: 50.8467, lng: 4.3525, label: "Brussels accommodation", num: 1, cat: "activity", desc: "Base for final days" },
        { lat: 50.8413, lng: 4.3550, label: "Sablon area", num: 2, cat: "food", desc: "Familiar territory" },
        { lat: 50.8460, lng: 4.3530, label: "Galeries Royales", num: 3, cat: "activity", desc: "Last chocolate shopping" },
        { lat: 50.8440, lng: 4.3610, label: "Parc de Bruxelles", num: 4, cat: "activity", desc: "Relaxation" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Travel Day — Settle into Brussels", description: "Return to Brussels for your final stretch. Check into accommodation. After 12 days in the Ardennes and Wallonia, Brussels' urban energy hits different. You appreciate it more now.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Brussels café", description: "Back to city comforts.", meta: "" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Rest & Laundry Day", description: "After weeks of travel, a genuine rest day. Laundry, repacking, revisiting favorite Brussels spots. Walk the Sablon for more chocolate. Read in a park.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Fin de Siècle (revisit)", description: "Return to one of your first Brussels meals. The vol-au-vent hits differently after 5 weeks in Belgium.", meta: "€15-25 · Cash only" }
          ],
          tips: []
        }
      ]
    },
    // === FINAL STRETCH — Brussels & Surrounds (Days 38-42) ===
    {
      num: 38,
      title: "Tervuren & Africa Museum",
      neighborhoods: "Tervuren · Forêt de Soignes",
      date: "Jul 8",
      mapPins: [
        { lat: 50.8310, lng: 4.5150, label: "AfricaMuseum", num: 1, cat: "activity", desc: "Renovated colonial history museum" },
        { lat: 50.8100, lng: 4.4500, label: "Forêt de Soignes", num: 2, cat: "activity", desc: "Ancient beech forest" },
        { lat: 50.8300, lng: 4.5200, label: "Tervuren Park", num: 3, cat: "activity", desc: "Beautiful grounds around the museum" },
        { lat: 50.8320, lng: 4.5160, label: "Tervuren village", num: 4, cat: "food", desc: "Charming Brabant village" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "AfricaMuseum", description: "Completely renovated in 2018, this museum confronts Belgium's colonial history in the Congo head-on while celebrating African culture, art, and biodiversity. Originally built by Leopold II as propaganda, it now honestly examines that dark history. The building and grounds are magnificent. A complex, essential visit.", details: ["📍 Leuvensesteenweg 13, Tervuren · €12 · Tram 44 from Brussels"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Brussels café", description: "Morning coffee before heading to Tervuren.", meta: "" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Forêt de Soignes", description: "One of Europe's finest remaining beech forests — ancient, cathedral-like, right on Brussels' doorstep. Walk the marked trails through towering trees. UNESCO-recognized for its exceptional beech stands. Therapeutic after weeks of travel.", details: ["📍 Accessible from Tervuren · Free"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Brussels favorite", description: "Revisit any favorite from your first week.", meta: "" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 39,
      title: "Lambic Beer Pilgrimage — Pajottenland",
      neighborhoods: "Pajottenland · Lembeek · Brussels",
      date: "Jul 9",
      mapPins: [
        { lat: 50.7680, lng: 4.1910, label: "Cantillon Brewery", num: 1, cat: "food", desc: "World's most authentic lambic brewery" },
        { lat: 50.7280, lng: 4.2080, label: "3 Fonteinen", num: 2, cat: "food", desc: "Master gueuze blender in Beersel" },
        { lat: 50.7330, lng: 4.2050, label: "Beersel Castle", num: 3, cat: "activity", desc: "14th-century moated castle" },
        { lat: 50.7500, lng: 4.1500, label: "Pajottenland", num: 4, cat: "activity", desc: "Rolling countryside — lambic's terroir" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Cantillon Brewery", description: "The world's most authentic lambic brewery, operating in Brussels since 1900. Lambic is beer fermented by wild yeast — open to the air, no added cultures. This ancient technique exists nowhere else on Earth except the Brussels region. The self-guided tour shows century-old wooden barrels, cobwebbed rafters (the webs trap the wild yeast), and the coolship where wort is exposed overnight. Tasting of gueuze, kriek, and seasonal lambics included.", details: ["📍 Rue Gheude 56, Brussels · €10 with tastings · Book ahead"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Quick Brussels breakfast", description: "Eat light — you'll be tasting beer.", meta: "" }
          ],
          tips: [{ type: "reddit", text: "Cantillon is a religious experience for beer lovers. Even non-beer drinkers are fascinated — it's genuinely unique in the world.", cite: "r/beer" }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "3 Fonteinen — Beersel", description: "Master gueuze blender in the village of Beersel, 20 min south of Brussels. Their Oude Geuze is considered among the world's finest sour beers. The tasting room is simple and unpretentious. Pair with Beersel Castle — a beautiful 14th-century moated fortress.", details: ["📍 Hoogstraat 2A, Beersel · Tasting room hours vary, check website"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "In de Verzekering tegen de Grote Dorst", description: "Legendary lambic café in Eizeringen — a farmhouse bar open only on Sundays (check schedule). 100+ lambics in a living room setting. If it's closed, try Café de la Gare in Lembeek.", meta: "€4-8/beer · Check opening hours" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 40,
      title: "Belgian Chocolate Masterclass & Farewell Shopping",
      neighborhoods: "Brussels Center · Sablon",
      date: "Jul 10",
      mapPins: [
        { lat: 50.8413, lng: 4.3550, label: "Sablon chocolatiers", num: 1, cat: "food", desc: "Final chocolate purchases" },
        { lat: 50.8467, lng: 4.3525, label: "Grand-Place farewell", num: 2, cat: "activity", desc: "Last visit" },
        { lat: 50.8475, lng: 4.3540, label: "Galeries Royales", num: 3, cat: "activity", desc: "Last-minute gifts" },
        { lat: 50.8451, lng: 4.3498, label: "Manneken Pis (farewell)", num: 4, cat: "activity", desc: "One last look at the little guy" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Chocolate Workshop or Shopping", description: "Several Brussels chocolatiers offer hands-on workshops — make your own pralines under a master chocolatier's guidance. Laurent Gerbaud, Zaabär, or the Chocolate Museum all offer sessions. Alternatively, do a final curated chocolate shopping run through Sablon.", details: ["💡 Workshops: €35-65 per person, 1.5-2 hours, book ahead"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Wittamer", description: "Royal warrant-holding pâtisserie on the Sablon since 1910. Exquisite pastries and chocolate for a special final breakfast.", meta: "€10-15 · Place du Grand Sablon" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Farewell Brussels Walk", description: "Revisit your favorite spots with fresh eyes. The Grand-Place one more time — it hits different after 6 weeks in Belgium. You understand the guild houses, you know the beer, you've eaten the waffles. You're not a tourist anymore.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Comme Chez Soi", description: "If budget allows, Belgium's most famous restaurant — 2 Michelin stars in an Art Nouveau dining room. French-Belgian haute cuisine at its peak. A spectacular farewell dinner. If too pricey, return to Restobières for a beer-paired farewell.", meta: "€100-200 · Place Rouppe 23 · Reserve weeks ahead" }
          ],
          tips: []
        }
      ]
    },
    {
      num: 41,
      title: "Last Full Day — Loose Ends & Favorites",
      neighborhoods: "Brussels · Personal favorites",
      date: "Jul 11",
      mapPins: [
        { lat: 50.8467, lng: 4.3525, label: "Brussels center", num: 1, cat: "activity", desc: "Final explorations" },
        { lat: 50.8413, lng: 4.3550, label: "Sablon (last time)", num: 2, cat: "food", desc: "Final Marcolini chocolate" },
        { lat: 50.8475, lng: 4.3540, label: "Galeries Royales", num: 3, cat: "activity", desc: "Evening stroll" },
        { lat: 50.8460, lng: 4.3530, label: "Delirium (last visit)", num: 4, cat: "food", desc: "One final beer in 2,000-beer paradise" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Flexible Morning", description: "Revisit anything you missed or want to see again. Return to a museum, revisit a neighborhood, or simply enjoy a long breakfast reading at a café. After 6 weeks, Brussels feels like home.", details: [] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Your favorite Brussels spot", description: "You have a favorite by now. Go back.", meta: "" }
          ],
          tips: []
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Packing & Preparation", description: "Pack up souvenirs (chocolate, beer, lace, Trappist cheeses). Make sure delicate items are wrapped. Belgian chocolate travels well if kept cool.", details: ["💡 Most airlines allow beer in checked luggage — wrap bottles in clothes."] },
            { title: "Farewell Evening Walk", description: "One last circuit: Grand-Place (illuminated), Galeries Royales (buzzing), Delirium Café (for one final beer). Sit on the Grand-Place at night and reflect on 6 weeks across an extraordinary little country.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Chez Léon (full circle)", description: "Return to where it started — moules-frites at Brussels' most famous mussel house. Full circle. Same giant pot, same perfect frites, but now you understand Belgium.", meta: "€20-30 · Rue des Bouchers" }
          ],
          tips: [{ type: "tip", text: "The Grand-Place at night, one last time. You'll carry this image for years." }]
        }
      ]
    },
    {
      num: 42,
      title: "Departure — Tot Ziens, België!",
      neighborhoods: "Brussels · Airport/Station",
      date: "Jul 12",
      mapPins: [
        { lat: 50.8467, lng: 4.3525, label: "Grand-Place (early morning)", num: 1, cat: "activity", desc: "One last look at dawn" },
        { lat: 50.8390, lng: 4.3360, label: "Brussels Midi", num: 2, cat: "activity", desc: "Eurostar/Thalys departure" },
        { lat: 50.9014, lng: 4.4844, label: "Brussels Airport", num: 3, cat: "activity", desc: "BRU — international flights" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Early Grand-Place", description: "If time allows, one last walk through the Grand-Place at dawn — the square is empty, golden, and all yours. The perfect bookend to 42 unforgettable days.", details: [] },
            { title: "Depart", description: "Brussels Airport (BRU) is 30 min by train from Central station. Brussels Midi has Eurostar to London (2h) and Thalys to Paris (1h22), Amsterdam (2h50). Tot ziens, België — you'll carry the beer, chocolate, art, and memories for a lifetime.", details: ["📍 Airport train every 10 min from Central/Nord/Midi · €13"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Hotel or station", description: "Last Belgian coffee and croissant. You've earned it.", meta: "" }
          ],
          tips: [{ type: "tip", text: "Buy a last box of chocolate at the Brussels Airport duty-free — Neuhaus and Leonidas have airport shops with fresh stock. One final taste of Belgium for the journey home." }]
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
    console.log('Email sent:', result.emailSent);
} catch (err) {
    console.error('❌ Fulfillment failed:', err.stack);
    process.exit(1);
}