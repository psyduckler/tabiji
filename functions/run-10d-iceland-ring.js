const fs = require('fs');
const path = require('path');

// Monkey-patch generateSlug to return our descriptive slug
const slugPath = require.resolve('./generate-slug');
require.cache[slugPath] = { id: slugPath, filename: slugPath, loaded: true, exports: () => 'bold-ring' };

const fulfillOrder = require('./fulfill-order');

const order = {
  id: "sample-10d-iceland-ring",
  email: "internal@tabiji.ai",
  destination: "Iceland",
  start_date: "2026-04-01",
  end_date: "2026-04-10",
  group_size: "2",
  travel_style: "",
  dining: "",
  budget: "",
  requests: "The complete Ring Road at a comfortable pace — all regions, whale watching, Westfjords detour, and hidden hot springs.",
  amount: "0.00",
  timestamp: new Date().toISOString(),
  status: "pending",
  notes: "Internal sample itinerary — not a customer order"
};

const itineraryData = {
  destination: "Iceland",
  countryEmoji: "🇮🇸",
  title: "Iceland Ring Road: 10 Days of Fire, Ice & Hidden Hot Springs",
  subtitle: "Reykjavik → Golden Circle → South Coast → Eastfjords → Mývatn → Akureyri → Tröllaskagi → Snæfellsnes → Reykjavik",
  description: "The complete Ring Road at a comfortable pace — every region of Iceland in 10 unforgettable days. Glacier lagoons, whale watching, volcanic landscapes, hidden hot springs, and the dramatic Eastfjords. No rushing, no regrets.",
  duration: "10 days",
  dates: "April 1 – 10, 2026",
  budget: "Mid-range",
  pace: "Comfortable",
  bestFor: "Road trippers, nature lovers & adventure seekers",
  highlights: [
    "Drive the entire 1,322 km Ring Road (Route 1)",
    "Jökulsárlón glacier lagoon and Diamond Beach",
    "Whale watching in Húsavík — Europe's whale watching capital",
    "Mývatn's otherworldly volcanic landscape",
    "Hidden hot springs: Reykjadalur, Seljavallalaug, Mývatn Nature Baths",
    "Snæfellsnes Peninsula — 'Iceland in miniature'",
    "Eastfjords fishing villages and dramatic coastal scenery",
    "Tröllaskagi Peninsula and Siglufjörður's Herring Era Museum",
    "Skógafoss, Seljalandsfoss, Dettifoss, and Goðafoss waterfalls",
    "Blue Lagoon or Sky Lagoon on departure day"
  ],
  essentials: [
    { title: "🚗 4WD Rental", text: "Book a 4WD vehicle — essential for gravel roads and weather resilience. Pick up at Keflavík airport. Add gravel protection and sand/ash insurance. Check road.is daily for conditions." },
    { title: "⛽ Fuel Up Often", text: "Gas stations can be 200+ km apart in the east and north. Fill up every chance you get. Most stations take credit cards (PIN required). N1 and Orkan are the main chains." },
    { title: "🌦️ Layer Everything", text: "Iceland weather changes every 15 minutes. Pack waterproof outer layers, fleece mid-layers, and merino base layers. No cotton — it stays wet. Wind is the real enemy, not cold." },
    { title: "🌐 Connectivity", text: "Get a local SIM or eSIM (Síminn has the best coverage). Data is essential for road conditions (road.is), weather (vedur.is), and maps. Cell service is spotty in the Eastfjords." },
    { title: "🏪 Stock Up at Bónus", text: "Groceries in Iceland are expensive. Hit Bónus or Krónan in Reykjavik to stock up on snacks, bread, deli items, and water. Cooking in accommodations saves a fortune." },
    { title: "♨️ Bring a Swimsuit Everywhere", text: "Hot springs and pools pop up everywhere. Always have your swimsuit and a quick-dry towel in the car. Follow local etiquette — shower naked before entering pools." }
  ],
  days: [
    // DAY 1 — Arrival & Reykjavik
    {
      num: 1,
      title: "Arrival & Reykjavik Exploration",
      neighborhoods: "Keflavík · Reykjavik City Center",
      date: "April 1",
      mapPins: [
        { lat: 63.9850, lng: -22.6056, label: "Keflavík Airport (KEF)", num: 1, cat: "transport", desc: "Arrive and pick up rental car" },
        { lat: 64.1466, lng: -21.9426, label: "Hallgrímskirkja", num: 2, cat: "activity", desc: "Iconic church with panoramic tower views" },
        { lat: 64.1475, lng: -21.9352, label: "Laugavegur Street", num: 3, cat: "activity", desc: "Main shopping and café street" },
        { lat: 64.1506, lng: -21.9286, label: "Sundhöllin Pool", num: 4, cat: "activity", desc: "Historic geothermal pool in city center" },
        { lat: 64.1516, lng: -21.9511, label: "Old Harbour", num: 5, cat: "food", desc: "Waterfront area with restaurants and whale watching boats" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Arrive at Keflavík & Pick Up Rental Car", description: "Collect your 4WD from the airport. Drive the 45 minutes to Reykjavik and check into your accommodation.", details: ["💡 Blue Car Rental and Lotus are well-reviewed budget options. Book gravel + sand/ash insurance."] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "If your flight arrives early, drop bags and start exploring immediately — jet lag is easier to beat if you push through the first day." }]
        },
        {
          label: "Afternoon",
          activities: [
            { title: "Hallgrímskirkja Church", description: "Walk up to Iceland's most iconic church. Pay the small fee to take the elevator to the tower for 360° views over Reykjavik's colorful rooftops.", details: ["📍 Hallgrímstorg 1 · ~ISK 1,200 for tower"] },
            { title: "Laugavegur Street Stroll", description: "Wander Reykjavik's main street — boutique shops, cozy cafés, and Icelandic design stores. Pop into Handknitting Association of Iceland for a lopapeysa sweater.", details: [] },
            { title: "Sundhöllin Pool", description: "One of Reykjavik's oldest geothermal pools. Hot tubs, a cold plunge, and a steam room. The perfect intro to Icelandic bathing culture.", details: ["📍 Barónsstígur 45a · ~ISK 1,200"] }
          ],
          meals: [
            { type: "☕ Lunch", name: "Sandholt Bakery", description: "Best bakery in Reykjavik — sourdough, pastries, and excellent soup of the day. Beloved by locals.", meta: "ISK 2,500-4,000 · Laugavegur 36" }
          ],
          tips: [{ type: "reddit", text: "Sundhöllin is the local's pool — way more authentic than the touristy Blue Lagoon, and a fraction of the price.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Old Harbour Walk", description: "Stroll the harbor area, peek at the whale watching boats you won't need (we're saving that for Húsavík), and enjoy the mountain views across the bay.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Messinn", description: "Legendary fish pan restaurant — the catch of the day served sizzling in a cast iron skillet with buttery potatoes. The plokkfiskur (fish stew) is perfection.", meta: "ISK 3,500-5,500 · Lækjargata 6b" },
            { type: "🍺 Drinks", name: "Kaffi Loki", description: "Traditional Icelandic food and craft beer right across from Hallgrímskirkja. Try the rye bread ice cream — it's actually incredible.", meta: "ISK 2,000-3,000 · Lokastígur 28" }
          ],
          tips: [{ type: "tip", text: "Stock up at Bónus supermarket tonight — it closes early. Grab bread, cheese, deli meats, and snacks for the road. This will save you a fortune over the next 9 days." }]
        }
      ]
    },
    // DAY 2 — Golden Circle
    {
      num: 2,
      title: "Golden Circle & Secret Lagoon",
      neighborhoods: "Þingvellir · Geysir · Gullfoss · Flúðir",
      date: "April 2",
      mapPins: [
        { lat: 64.2559, lng: -21.1290, label: "Þingvellir National Park", num: 1, cat: "activity", desc: "UNESCO site — tectonic plates and Viking parliament" },
        { lat: 64.3104, lng: -20.3024, label: "Geysir Geothermal Area", num: 2, cat: "activity", desc: "Watch Strokkur erupt every 5-10 minutes" },
        { lat: 64.3271, lng: -20.1199, label: "Gullfoss Waterfall", num: 3, cat: "activity", desc: "Thundering two-tiered waterfall on the Hvítá river" },
        { lat: 64.1368, lng: -20.3094, label: "Secret Lagoon (Gamla Laugin)", num: 4, cat: "activity", desc: "Iceland's oldest natural hot spring pool" },
        { lat: 64.1167, lng: -20.3083, label: "Flúðir", num: 5, cat: "lodging", desc: "Small village near Secret Lagoon — overnight base" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Þingvellir National Park", description: "Walk between the North American and Eurasian tectonic plates at this UNESCO World Heritage Site. This is where the Icelandic parliament (Alþingi) was founded in 930 AD. Follow the main path through Almannagjá gorge to the waterfall viewpoint.", details: ["📍 Free entry, parking ISK 750", "💡 Optional: Silfra snorkeling between the tectonic plates — book in advance with DIVE.IS (~ISK 22,000). Crystal-clear glacial water, 2-3°C — visibility is insane."] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "Arrive at Þingvellir by 9am and you'll have the place nearly to yourself. By 11am, the tour buses roll in.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Midday",
          activities: [
            { title: "Geysir Geothermal Area", description: "Strokkur erupts every 5-10 minutes, shooting boiling water 20-30 meters into the air. The original Great Geysir is mostly dormant but still steams impressively. Walk around the colorful mud pools.", details: ["📍 Free entry · Gift shop and café on site"] },
            { title: "Gullfoss Waterfall", description: "Iceland's most famous waterfall — a massive two-tiered cascade plunging 32 meters into a rocky canyon. Walk down to the lower viewing platform to feel the spray.", details: ["📍 Free entry · Café with lamb soup at the top"] }
          ],
          meals: [
            { type: "🍅 Lunch", name: "Friðheimar Tomato Farm", description: "A working greenhouse restaurant where everything is made from their homegrown tomatoes — soup, bread, and even tomato beer and tomato ice cream. Reservations required.", meta: "ISK 3,500-5,000 · Book at fridheimar.is" }
          ],
          tips: [{ type: "reddit", text: "Friðheimar is touristy but genuinely worth it. The tomato soup is unlimited refills and the greenhouse setting is surreal.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Afternoon / Evening",
          activities: [
            { title: "Secret Lagoon (Gamla Laugin)", description: "Iceland's oldest natural hot spring pool — warm, uncrowded, and way more authentic than the Blue Lagoon. Sit in 38-40°C natural water while a small geyser erupts nearby. Magical at sunset.", details: ["📍 Hvammsvegur, Flúðir · ISK 3,000 · Open until 10pm"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Minilik (Flúðir)", description: "Surprisingly good Ethiopian-Icelandic fusion in tiny Flúðir. If closed, the N1 gas station hot dogs (pylsur) are an Icelandic institution — seriously.", meta: "ISK 2,500-4,000" }
          ],
          tips: [{ type: "tip", text: "Stay near Flúðir or Selfoss tonight to avoid backtracking to Reykjavik. You'll be heading south along the coast tomorrow." }]
        }
      ]
    },
    // DAY 3 — South Coast
    {
      num: 3,
      title: "South Coast Waterfalls & Black Sand",
      neighborhoods: "Seljalandsfoss · Skógafoss · Reynisfjara · Vík",
      date: "April 3",
      mapPins: [
        { lat: 63.6156, lng: -19.9885, label: "Seljalandsfoss", num: 1, cat: "activity", desc: "Walk behind this 60m waterfall" },
        { lat: 63.6210, lng: -19.9862, label: "Gljúfrabúi", num: 2, cat: "activity", desc: "Hidden waterfall inside a canyon — 5 min walk from Seljalandsfoss" },
        { lat: 63.5321, lng: -19.5114, label: "Skógafoss", num: 3, cat: "activity", desc: "Massive 60m waterfall — climb the stairs for views" },
        { lat: 63.5312, lng: -19.5073, label: "Skógar Museum", num: 4, cat: "activity", desc: "Folk museum with turf houses and transport collection" },
        { lat: 63.4044, lng: -19.0714, label: "Reynisfjara Black Sand Beach", num: 5, cat: "activity", desc: "Dramatic basalt columns and Atlantic waves" },
        { lat: 63.4186, lng: -19.0060, label: "Vík", num: 6, cat: "lodging", desc: "Charming village under Mýrdalsjökull glacier" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Seljalandsfoss", description: "One of Iceland's most photographed waterfalls — and you can walk behind it through a path carved into the cliff. Arrive early to beat the crowds and get the best light.", details: ["📍 Free · Parking ISK 800", "💡 Wear a waterproof jacket — you will get soaked walking behind the falls"] },
            { title: "Gljúfrabúi (Hidden Falls)", description: "Just a 5-minute walk from Seljalandsfoss, this secret waterfall hides inside a narrow canyon. Wade through a shallow stream to enter the cave and look up — stunning.", details: ["📍 Free · Bring waterproof boots or just accept wet feet"] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "Gljúfrabúi is the one most people miss. It's more magical than Seljalandsfoss — like finding a waterfall inside a cathedral.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Midday",
          activities: [
            { title: "Seljavallalaug Hidden Hot Spring", description: "A 15-minute easy hike up a valley to a semi-abandoned swimming pool built in 1923, fed by a natural hot spring. The water is lukewarm and algae-coated, but the mountain setting is breathtaking. Bring your own towel.", details: ["📍 Off Route 242, near Seljavellir · Free · No facilities"] },
            { title: "Skógafoss", description: "A thundering 60-meter wall of water. Walk up the 527 steps alongside the falls for dramatic views from the top. On sunny days, you'll see rainbows in the mist.", details: ["📍 Free · Parking ISK 800"] }
          ],
          meals: [
            { type: "🥪 Lunch", name: "Skógar Museum Café", description: "Simple café at the folk museum. Grab a lamb soup and rest before the afternoon drive. The museum itself has fascinating turf houses and a transport exhibit.", meta: "ISK 2,000-3,000" }
          ],
          tips: [{ type: "tip", text: "Seljavallalaug is an incredible free hot spring but bring realistic expectations — it's more 'wild swim' than 'spa.' The hike and valley views are the real reward." }]
        },
        {
          label: "Afternoon / Evening",
          activities: [
            { title: "Reynisfjara Black Sand Beach", description: "Jet-black volcanic sand, towering basalt columns, and massive Atlantic swells crashing in. Walk along the beach and admire the Reynisdrangar sea stacks offshore.", details: ["⚠️ DEADLY sneaker waves — never turn your back on the ocean. Stay well back from the waterline. People have been swept out and killed here. Not exaggerating."] },
            { title: "Vík í Mýrdal", description: "Iceland's southernmost village, nestled beneath the Mýrdalsjökull glacier. Walk up to the Vík Church for panoramic views of the coast and village.", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Suður-Vík", description: "Cozy restaurant in Vík with excellent fish and chips, lamb burgers, and craft beer. The fish of the day is always a solid choice.", meta: "ISK 3,000-5,000 · Suðurvíkurvegur 1" }
          ],
          tips: [{ type: "reddit", text: "I cannot stress this enough: respect the waves at Reynisfjara. Every year tourists get caught. Stay at LEAST 30 meters from the water's edge.", cite: "r/VisitingIceland" }]
        }
      ]
    },
    // DAY 4 — Vatnajökull & Glacier Lagoons
    {
      num: 4,
      title: "Canyons, Glaciers & Diamond Beach",
      neighborhoods: "Fjaðrárgljúfur · Skaftafell · Jökulsárlón",
      date: "April 4",
      mapPins: [
        { lat: 63.7712, lng: -18.1718, label: "Fjaðrárgljúfur Canyon", num: 1, cat: "activity", desc: "Stunning 100m deep mossy canyon" },
        { lat: 64.0751, lng: -16.9753, label: "Skaftafell / Svartifoss", num: 2, cat: "activity", desc: "Basalt column waterfall via 5.5km hike" },
        { lat: 64.0488, lng: -16.3792, label: "Fjallsárlón Glacier Lagoon", num: 3, cat: "activity", desc: "Smaller, quieter glacier lagoon — zodiac boats available" },
        { lat: 64.0784, lng: -16.1797, label: "Jökulsárlón Glacier Lagoon", num: 4, cat: "activity", desc: "Iceland's crown jewel — icebergs calving into the lagoon" },
        { lat: 64.0781, lng: -16.1750, label: "Diamond Beach", num: 5, cat: "activity", desc: "Crystal ice chunks on black sand" },
        { lat: 64.2559, lng: -15.2122, label: "Höfn", num: 6, cat: "lodging", desc: "Lobster capital of Iceland — overnight base" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Fjaðrárgljúfur Canyon", description: "A 2-km long, 100-meter deep serpentine canyon with vivid green moss walls. Walk along the rim on the maintained path for breathtaking views down into the gorge. Made famous by Justin Bieber's music video (and subsequently closed for restoration — check if open).", details: ["📍 Off Route 1, near Kirkjubæjarklaustur · Free · Parking ISK 800"] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "This canyon may be seasonally closed for vegetation restoration. Check signs at the parking area — respect closures, the moss takes decades to recover." }]
        },
        {
          label: "Midday",
          activities: [
            { title: "Skaftafell — Svartifoss Hike", description: "A 5.5 km round-trip hike (1.5-2 hours) through birch woodland to Svartifoss, a dramatic waterfall framed by hanging basalt columns. The columns inspired the design of Hallgrímskirkja in Reykjavik.", details: ["📍 Vatnajökull National Park · Free · Parking ISK 750"] },
            { title: "Optional: Glacier Hike", description: "Book a guided glacier hike on Skaftafellsjökull or Svínafellsjökull (~3 hours, ISK 12,000-15,000). Walk on ancient ice, into blue crevasses, and learn about Iceland's rapidly retreating glaciers.", details: ["💡 Book with Arctic Adventures or Glacier Guides. Crampons and equipment provided."] }
          ],
          meals: [
            { type: "🥪 Lunch", name: "Packed lunch from Bónus supplies", description: "Eat at the Skaftafell visitor center picnic area. Save your restaurant budget for Höfn's langoustine tonight.", meta: "Free if you packed from Reykjavik" }
          ],
          tips: []
        },
        {
          label: "Afternoon / Evening",
          activities: [
            { title: "Fjallsárlón Glacier Lagoon", description: "The smaller, less-visited sibling of Jökulsárlón. Take a zodiac boat tour right up to the glacier face — more intimate and often less crowded than the famous lagoon next door.", details: ["📍 Zodiac tour ~ISK 9,000 · 45 min · Book at fjallsarlon.is"] },
            { title: "Jökulsárlón Glacier Lagoon", description: "Iceland's most famous natural wonder. Massive icebergs calve from Breiðamerkurjökull glacier and drift serenely through the lagoon toward the sea. The blue and white ice against dark water is otherworldly.", details: ["📍 Free to view from shore · Amphibious boat tour ~ISK 6,500"] },
            { title: "Diamond Beach", description: "Directly across the road from Jökulsárlón — chunks of crystal-clear glacial ice wash up on black volcanic sand, glittering like diamonds. Best at golden hour.", details: ["📍 Free"] }
          ],
          meals: [
            { type: "🦞 Dinner", name: "Pakkhús Restaurant (Höfn)", description: "Höfn is the langoustine capital of Iceland. Pakkhús serves them pan-fried, grilled, and in soup. The tasting menu is the move. One of the best meals you'll have on the trip.", meta: "ISK 5,000-8,000 · Krosseyjarvegur 3 · Reservations recommended" }
          ],
          tips: [{ type: "reddit", text: "Do Fjallsárlón boat tour, not the Jökulsárlón one. You get way closer to the glacier, it's less crowded, and the zodiac is more fun than the amphibious truck.", cite: "r/VisitingIceland" }]
        }
      ]
    },
    // DAY 5 — Eastfjords
    {
      num: 5,
      title: "Eastfjords: Fishing Villages & Fjord Views",
      neighborhoods: "Höfn · Djúpivogur · Stöðvarfjörður · Egilsstaðir",
      date: "April 5",
      mapPins: [
        { lat: 64.2559, lng: -15.2122, label: "Höfn", num: 1, cat: "transport", desc: "Depart morning — the Eastfjords await" },
        { lat: 64.6458, lng: -14.2622, label: "Djúpivogur", num: 2, cat: "activity", desc: "Charming harbor village with Eggin í Gleðivík egg sculptures" },
        { lat: 64.8325, lng: -13.8694, label: "Stöðvarfjörður", num: 3, cat: "activity", desc: "Home to Petra's Stone Collection" },
        { lat: 65.0724, lng: -14.0172, label: "Seyðisfjörður", num: 4, cat: "activity", desc: "Rainbow street, blue church, and ferry port" },
        { lat: 65.2636, lng: -14.3948, label: "Egilsstaðir", num: 5, cat: "lodging", desc: "Largest town in East Iceland — services and fuel" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Scenic Drive: Höfn to Djúpivogur", description: "The Eastfjords coast road is one of Iceland's most dramatic drives — narrow roads winding between mountains and sea, through tunnels and along clifftops. Take it slow and stop for photos.", details: ["💡 ~2 hours. Fill up fuel in Höfn — the next station is in Djúpivogur"] },
            { title: "Djúpivogur Village", description: "A tiny fishing village with colorful houses. Walk along the harbor and find 'Eggin í Gleðivík' — 34 oversized granite eggs on the waterfront, each representing a different local bird species.", details: ["📍 Free to walk around"] }
          ],
          meals: [
            { type: "☕ Breakfast/Coffee", name: "Við Voginn (Djúpivogur)", description: "Cozy harbourside café — good coffee, homemade cakes, and the freshest fish soup you can imagine. Run by locals.", meta: "ISK 1,500-3,000" }
          ],
          tips: [{ type: "tip", text: "The Eastfjords are the least-visited region of Iceland. You might go hours without seeing another tourist — that's the whole point." }]
        },
        {
          label: "Midday",
          activities: [
            { title: "Petra's Stone Collection (Stöðvarfjörður)", description: "A lifelong personal collection of minerals, crystals, and semi-precious stones gathered by local woman Petra Sveinsdóttir over 75 years. Thousands of specimens fill her garden and house. Surprisingly captivating.", details: ["📍 ISK 2,000 · Open May-Oct (check seasonal hours)"] },
            { title: "Fjord-Hopping Drive", description: "Continue north through the dramatic fjords. Each one reveals a new view — waterfalls cascading off cliffsides, tiny farms, and vast empty valleys. The road twists in and out of fjords.", details: [] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "The Eastfjords drive is long but don't rush it — this is where Iceland feels truly remote and wild. Budget more time than Google Maps says.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Afternoon / Evening",
          activities: [
            { title: "Seyðisfjörður Detour", description: "A stunning 25-km mountain pass drive from Egilsstaðir down into this picturesque fjord town. Famous for its rainbow-painted street leading to the iconic blue church (Seyðisfjarðarkirkja), and the Skaftfell Center for Visual Art.", details: ["📍 25 km from Egilsstaðir · Free to explore", "⚠️ The mountain pass (Fjarðarheiði) can be closed in bad weather. Check road.is before driving."] },
            { title: "Egilsstaðir", description: "East Iceland's hub — stock up on fuel and groceries. Walk along the shores of Lagarfljót lake, said to harbor a serpent-like creature (the Lagarfljót Worm — Iceland's Loch Ness Monster).", details: [] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Salt Café & Bistro (Egilsstaðir)", description: "Modern bistro using local ingredients — reindeer, Arctic char, and lamb. The most refined dining option in east Iceland.", meta: "ISK 3,500-6,000 · Miðvangur 1-3" }
          ],
          tips: [{ type: "tip", text: "Egilsstaðir has one of the few Bónus stores outside of Reykjavik — restock snacks and supplies for the north." }]
        }
      ]
    },
    // DAY 6 — Mývatn & Volcanic North
    {
      num: 6,
      title: "Mývatn: Volcanoes, Craters & Geothermal Chaos",
      neighborhoods: "Dettifoss · Krafla · Hverir · Mývatn",
      date: "April 6",
      mapPins: [
        { lat: 65.8146, lng: -16.3845, label: "Dettifoss", num: 1, cat: "activity", desc: "Europe's most powerful waterfall" },
        { lat: 65.7150, lng: -16.7547, label: "Krafla Volcano / Víti Crater", num: 2, cat: "activity", desc: "Turquoise crater lake atop an active volcano" },
        { lat: 65.6413, lng: -16.8097, label: "Hverir (Námafjall)", num: 3, cat: "activity", desc: "Bubbling mud pots and steaming fumaroles" },
        { lat: 65.6267, lng: -16.8828, label: "Grjótagjá Cave", num: 4, cat: "activity", desc: "Lava cave with hot spring — Game of Thrones filming location" },
        { lat: 65.6308, lng: -16.8456, label: "Skútustaðagígar Pseudocraters", num: 5, cat: "activity", desc: "Crater-pocked landscape along Mývatn's south shore" },
        { lat: 65.6303, lng: -16.8472, label: "Mývatn Nature Baths", num: 6, cat: "activity", desc: "Northern Iceland's answer to the Blue Lagoon" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Dettifoss", description: "Europe's most powerful waterfall — 100 meters wide, plunging 44 meters into a massive canyon. The raw power is staggering. Access from Route 862 (east side, paved) for the best views. Hafragilsfoss, a short walk further, is equally impressive and usually deserted.", details: ["📍 Free · Parking available on east side (Route 862)", "💡 From Egilsstaðir, take Route 1 north then Route 862. ~150 km, ~2 hours."] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "Dettifoss is absolutely wild — photos don't capture the power. You feel it in your chest. Hafragilsfoss downstream is just as stunning and you'll have it to yourself.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Midday",
          activities: [
            { title: "Krafla Volcanic Area & Víti Crater", description: "Drive to the top of Krafla volcano and peer into the Víti explosion crater — a vivid turquoise lake sitting inside the caldera. Walk around the rim (30-min loop) for panoramic views of the surrounding lava fields.", details: ["📍 Free · Paved road to the top"] },
            { title: "Hverir (Námafjall) Geothermal Area", description: "A Martian landscape of bubbling grey mud pools, hissing steam vents, and sulfur-yellow deposits. Walk the boardwalk loop and watch the earth actively boiling beneath your feet. It stinks gloriously of sulfur.", details: ["📍 Free · Right on Route 1, east of Mývatn", "⚠️ Stay on the marked path — the ground is genuinely scalding hot in places"] }
          ],
          meals: [
            { type: "🥪 Lunch", name: "Vogafjós Cowshed Café", description: "A restaurant attached to a working cowshed — eat fresh bread and smoked trout while watching cows being milked through a glass partition. Only in Iceland.", meta: "ISK 3,000-5,000 · On Mývatn's east shore" }
          ],
          tips: [{ type: "tip", text: "The sulfur smell at Hverir is intense but you genuinely stop noticing after 10 minutes. Don't let it deter you — this place is surreal." }]
        },
        {
          label: "Afternoon / Evening",
          activities: [
            { title: "Grjótagjá Lava Cave", description: "A small lava cave with a geothermal hot spring inside — famously used as a Game of Thrones filming location (Jon Snow and Ygritte's cave scene). The water is too hot for bathing now (~50°C), but peering in is atmospheric.", details: ["📍 Free · Short walk from parking area near Mývatn"] },
            { title: "Skútustaðagígar Pseudocraters", description: "Walk the loop trail (1.3 km) around these unusual craters formed by steam explosions when lava flowed over wetland. Beautiful reflections in Mývatn at golden hour.", details: ["📍 Free · South shore of Mývatn"] },
            { title: "Mývatn Nature Baths", description: "Northern Iceland's Blue Lagoon — but quieter, cheaper, and arguably more beautiful. Milky-blue geothermal water overlooking the Mývatn landscape. Perfect way to end a day of volcanic exploration.", details: ["📍 ISK 5,500 · Open until 10pm in summer · jardbodin.is"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Daddi's Pizza (Mývatn)", description: "A beloved local institution — wood-fired pizza in a cozy cabin. After a day of lava and steam, this hits different. The Arctic char pizza is uniquely Icelandic.", meta: "ISK 2,500-4,000" }
          ],
          tips: [{ type: "reddit", text: "Mývatn Nature Baths at sunset > Blue Lagoon. A fraction of the price, way less crowded, and the views are incredible. Don't miss it.", cite: "r/VisitingIceland" }]
        }
      ]
    },
    // DAY 7 — Húsavík Whale Watching, Goðafoss, Akureyri
    {
      num: 7,
      title: "Whale Watching, Goðafoss & Akureyri",
      neighborhoods: "Húsavík · Goðafoss · Akureyri",
      date: "April 7",
      mapPins: [
        { lat: 66.0449, lng: -17.3380, label: "Húsavík", num: 1, cat: "activity", desc: "Europe's whale watching capital" },
        { lat: 66.0428, lng: -17.3362, label: "Húsavík Whale Museum", num: 2, cat: "activity", desc: "World-class museum with real whale skeletons" },
        { lat: 66.0456, lng: -17.3280, label: "GeoSea Geothermal Sea Baths", num: 3, cat: "activity", desc: "Infinity pool overlooking Skjálfandi Bay" },
        { lat: 65.6829, lng: -17.5504, label: "Goðafoss", num: 4, cat: "activity", desc: "Waterfall of the Gods — wide horseshoe cascade" },
        { lat: 65.6839, lng: -18.0878, label: "Akureyri", num: 5, cat: "lodging", desc: "Capital of the North — charming town on Eyjafjörður" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Húsavík Whale Watching", description: "Húsavík is Europe's whale watching capital with 98% sighting rates in summer. Take a 3-hour tour to spot humpback whales, minke whales, dolphins, and sometimes blue whales. Choose traditional oak boats (North Sailing) for the most authentic experience.", details: ["📍 Book with North Sailing or Gentle Giants · ISK 12,000-14,000 · 3 hours", "💡 Take Dramamine 30 min before departure if you get seasick. The sea can be rough.", "⚠️ April is early season — check if tours are running. Peak season is June-August."] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Heimabakarí Konditorí (Húsavík)", description: "Old-school Icelandic bakery — get a fresh kleinur (twisted doughnut) and strong coffee before the boat.", meta: "ISK 800-1,500" }
          ],
          tips: [{ type: "reddit", text: "Take sea sickness meds BEFORE the boat. Don't wait until you feel sick — it's too late by then. Also bring warm layers, it's freezing on the water.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Midday",
          activities: [
            { title: "Húsavík Whale Museum", description: "One of the best whale museums in the world — full whale skeletons suspended from the ceiling, interactive exhibits, and fascinating information about Icelandic whaling history. Worth at least an hour.", details: ["📍 ISK 2,000 · Hafnarstétt 1"] },
            { title: "GeoSea Geothermal Sea Baths", description: "Stunning infinity pools built into the clifftop overlooking Skjálfandi Bay. Natural geothermal seawater at 38-40°C. On a clear day, you can see the mountains across the bay. Try to time it for sunset.", details: ["📍 ISK 5,300 · Vitaslóð 1 · Book at geosea.is"] }
          ],
          meals: [
            { type: "🐟 Lunch", name: "Gamli Baukur", description: "Harbourside restaurant with the freshest seafood in town. Try the fish of the day or the seafood soup. Sit by the window and watch whales from your table.", meta: "ISK 3,000-5,000 · Hafnarstétt 9" }
          ],
          tips: [{ type: "reddit", text: "GeoSea at sunset is one of the best experiences in Iceland. The views over the bay while soaking in hot seawater — absolutely unbeatable.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Afternoon / Evening",
          activities: [
            { title: "Goðafoss — Waterfall of the Gods", description: "A wide, horseshoe-shaped waterfall where, in 1000 AD, the lawspeaker Þorgeir threw his Norse god statues to symbolize Iceland's conversion to Christianity. Walk to both sides for different perspectives.", details: ["📍 Free · Parking ISK 750 · Right on Route 1, between Húsavík and Akureyri"] },
            { title: "Akureyri Evening", description: "Iceland's 'Capital of the North' is a charming town of 19,000 on Eyjafjörður. Walk the pedestrian shopping street, spot the heart-shaped red traffic lights, and visit the Akureyri Botanical Garden (free, northernmost botanical garden in the world).", details: [] },
            { title: "Akureyri Swimming Pool", description: "One of Iceland's best public pools — multiple hot tubs, a water slide, a lap pool, and a steam room. The perfect way to unwind after a big day.", details: ["📍 ISK 1,050 · Þingvallastræti 21 · Open until 9pm"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Strikið", description: "Top-floor restaurant with panoramic fjord views. Creative Icelandic cuisine — grilled lamb, Arctic char, and reindeer. The cocktail bar is excellent too.", meta: "ISK 5,000-8,000 · Skipagata 14 · Reservations recommended" }
          ],
          tips: [{ type: "tip", text: "Akureyri is the best place to refuel, restock groceries, and do laundry before heading to the more remote Tröllaskagi Peninsula tomorrow." }]
        }
      ]
    },
    // DAY 8 — Tröllaskagi Peninsula
    {
      num: 8,
      title: "Tröllaskagi: Herring History & Mountain Passes",
      neighborhoods: "Dalvík · Siglufjörður · Hofsós · Skagafjörður · Blönduós",
      date: "April 8",
      mapPins: [
        { lat: 65.9713, lng: -18.5264, label: "Dalvík", num: 1, cat: "activity", desc: "Fishing village with whale watching alternative" },
        { lat: 66.1514, lng: -18.9108, label: "Siglufjörður", num: 2, cat: "activity", desc: "Herring Era Museum — Iceland's award-winning museum" },
        { lat: 65.8843, lng: -19.4064, label: "Hofsós", num: 3, cat: "activity", desc: "Infinity pool with fjord views" },
        { lat: 65.7389, lng: -19.6117, label: "Glaumbær Farm Museum", num: 4, cat: "activity", desc: "Perfectly preserved turf farmhouse from 1700s" },
        { lat: 65.6614, lng: -20.2864, label: "Blönduós", num: 5, cat: "lodging", desc: "Small town — overnight stop on the way west" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Dalvík", description: "A quiet fishing village with views across Eyjafjörður. If whale watching in Húsavík didn't happen (weather, season), Dalvík offers excellent alternative tours with Arctic Sea Tours.", details: ["📍 30 min north of Akureyri"] },
            { title: "Scenic Drive: Tröllaskagi Peninsula", description: "One of Iceland's most spectacular drives — mountain passes, avalanche tunnels, dramatic fjords, and almost zero tourists. The road from Dalvík to Siglufjörður passes through single-lane tunnels carved through the mountains.", details: ["💡 Take Route 76 along the coast — it's more scenic than the inland Route 1 shortcut"] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "Tröllaskagi is the most underrated region in Iceland. Most Ring Road drivers take the Route 1 shortcut and miss all of this. Don't make that mistake.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Midday",
          activities: [
            { title: "Siglufjörður — Herring Era Museum", description: "Iceland's most award-winning museum tells the story of the herring boom that made Siglufjörður the richest town in Iceland in the 1940s-60s. Three restored buildings with original equipment, boats, and recreated salting stations. Surprisingly fascinating and emotional.", details: ["📍 ISK 2,000 · Snorragata 10 · Allow 1-1.5 hours"] },
            { title: "Siglufjörður Town Walk", description: "Wander this picturesque fjord town — colorful houses, a small harbor, and mountain views in every direction. The Folk Music Centre is worth a peek if open.", details: [] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Hannes Boy (Siglufjörður)", description: "Named after a legendary herring captain — seafood soup, fried fish, and beautiful harbor views. One of the most charming lunch spots in Iceland.", meta: "ISK 2,500-4,500" }
          ],
          tips: [{ type: "reddit", text: "The Herring Era Museum sounds boring. It is NOT boring. It's genuinely one of the best museums in Iceland. Give it proper time.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Afternoon / Evening",
          activities: [
            { title: "Hofsós Infinity Pool", description: "One of Iceland's most photogenic swimming pools — an infinity-edge pool carved into the clifftop overlooking Skagafjörður fjord with views of Drangey island. Warm geothermal water, total serenity.", details: ["📍 ISK 1,000 · Open June-August typically (check seasonal hours)", "⚠️ April may be off-season — check if open before driving here specifically"] },
            { title: "Glaumbær Turf Farm Museum", description: "A beautifully preserved 18th-century turf farmhouse — the traditional Icelandic building style for centuries. Walk through the interconnected rooms and imagine rural Icelandic life. The adjacent café serves excellent waffles and coffee.", details: ["📍 ISK 2,000 · Off Route 75 near Sauðárkrókur"] }
          ],
          meals: [
            { type: "🧇 Afternoon", name: "Áskaffi (at Glaumbær)", description: "Tiny café next to the museum serving traditional Icelandic pancakes and waffles with cream and rhubarb jam. The coziest pit stop on the entire Ring Road.", meta: "ISK 1,000-2,000" },
            { type: "🍽️ Dinner", name: "Hotel & Pub Blönduós", description: "Simple but solid — burgers, fish, and Icelandic comfort food. Blönduós is a small town so options are limited, but the pub is reliable.", meta: "ISK 2,500-4,500" }
          ],
          tips: [{ type: "tip", text: "Between Siglufjörður and Hofsós, look for the Reykjafoss waterfall with a natural hot pot nearby. Locals soak here — it's free and usually empty." }]
        }
      ]
    },
    // DAY 9 — Snæfellsnes Peninsula
    {
      num: 9,
      title: "Snæfellsnes: Iceland in Miniature",
      neighborhoods: "Grundarfjörður · Kirkjufell · Snæfellsjökull · Arnarstapi",
      date: "April 9",
      mapPins: [
        { lat: 64.9426, lng: -23.2553, label: "Kirkjufell & Kirkjufellsfoss", num: 1, cat: "activity", desc: "Iceland's most photographed mountain" },
        { lat: 64.7539, lng: -23.9283, label: "Djúpalónssandur Beach", num: 2, cat: "activity", desc: "Black pebble beach with lifting stones and shipwreck remains" },
        { lat: 64.7667, lng: -23.7833, label: "Snæfellsjökull National Park", num: 3, cat: "activity", desc: "Glacier-capped volcano from Jules Verne's Journey to the Center of the Earth" },
        { lat: 64.7653, lng: -23.8097, label: "Vatnshellir Lava Cave", num: 4, cat: "activity", desc: "8,000-year-old lava tube with guided tours" },
        { lat: 64.7692, lng: -23.6247, label: "Arnarstapi", num: 5, cat: "activity", desc: "Coastal village with dramatic sea arches and basalt formations" },
        { lat: 64.7994, lng: -23.4742, label: "Ytri Tunga Beach", num: 6, cat: "activity", desc: "Seal colony — best chance to see seals in Iceland" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Drive to Snæfellsnes", description: "The drive from Blönduós to Grundarfjörður is about 3 hours. Stop for fuel and coffee in Borgarnes on the way. The landscape shifts from flat farmland to dramatic volcanic peninsula.", details: ["💡 If time allows, detour to Hvammsvik Hot Springs on Hvalfjörður — natural pools right on the fjord edge. ISK 6,500, book in advance."] },
            { title: "Kirkjufell & Kirkjufellsfoss", description: "Iceland's most photographed mountain — the distinctive cone shape was featured in Game of Thrones as 'the mountain like an arrowhead.' Walk down to the small waterfall in front for the iconic photo composition.", details: ["📍 Free · Parking in Grundarfjörður · 5 min walk to the viewpoint"] }
          ],
          meals: [],
          tips: [{ type: "reddit", text: "Kirkjufell is gorgeous but the parking situation is chaotic in summer. Go early morning or evening for better light AND fewer people.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Midday",
          activities: [
            { title: "Djúpalónssandur Black Pebble Beach", description: "A dramatic black-pebble beach with four 'lifting stones' (23-154 kg) that fishermen once used to test their strength. Scattered iron remains of a 1948 shipwreck rust poetically on the shore.", details: ["📍 Free · Short walk from parking to beach"] },
            { title: "Vatnshellir Lava Cave", description: "Descend into an 8,000-year-old lava tube beneath Snæfellsjökull. Guided 45-minute tours take you through two levels of the cave — the lower chamber is pitch-black and eerily silent. Magical.", details: ["📍 ISK 3,750 · Guided tours only · Book at summitguides.is", "💡 Bring warm layers — it's cool underground"] }
          ],
          meals: [
            { type: "🥪 Lunch", name: "Fjöruhúsið (Hellnar)", description: "A legendary tiny café perched on the coastline near Hellnar. Fresh fish soup, cakes, and coffee with crashing waves right outside. One of the most scenic lunch spots in Iceland.", meta: "ISK 2,000-3,500 · Open summer only — check if open in April" }
          ],
          tips: [{ type: "tip", text: "Snæfellsjökull glacier sits atop the volcano where Jules Verne's 'Journey to the Center of the Earth' begins. On a clear day, the glacier is visible from Reykjavik across the bay." }]
        },
        {
          label: "Afternoon / Evening",
          activities: [
            { title: "Arnarstapi Coastal Walk", description: "Walk the stunning 2.5 km coastal path between Arnarstapi and Hellnar. Dramatic basalt formations, natural sea arches, crashing waves, and nesting seabirds. The stone bridge at Gatklettur is the highlight.", details: ["📍 Free · Well-marked path, easy walking"] },
            { title: "Ytri Tunga Seal Beach", description: "Iceland's best spot to see harbor seals lounging on the rocks. Walk quietly to the beach and scan the shoreline — they're usually there year-round, especially in summer. Bring binoculars.", details: ["📍 Free · Short walk from parking"] }
          ],
          meals: [
            { type: "🍽️ Dinner", name: "Bjargarsteinn Mathús (Grundarfjörður)", description: "Excellent restaurant in a historic building — lamb, fish, and creative Icelandic plates with views of Kirkjufell. Worth the splurge on your second-to-last night.", meta: "ISK 4,500-7,000 · Sólvellir 15 · Reservations recommended" }
          ],
          tips: [{ type: "reddit", text: "Drive back to Reykjavik tonight if you can — it's about 2.5 hours from Grundarfjörður. That gives you a full Day 10 for the Blue Lagoon and any last-minute Reykjavik shopping.", cite: "r/VisitingIceland" }]
        }
      ]
    },
    // DAY 10 — Blue Lagoon & Departure
    {
      num: 10,
      title: "Blue Lagoon & Farewell Iceland",
      neighborhoods: "Reykjavik · Blue Lagoon · Keflavík",
      date: "April 10",
      mapPins: [
        { lat: 64.1466, lng: -21.9426, label: "Reykjavik — Last Morning", num: 1, cat: "activity", desc: "Final stroll and souvenir shopping" },
        { lat: 63.8803, lng: -22.4495, label: "Blue Lagoon", num: 2, cat: "activity", desc: "Iceland's famous geothermal spa" },
        { lat: 63.8947, lng: -22.4394, label: "Sky Lagoon (Alternative)", num: 3, cat: "activity", desc: "Newer infinity-edge spa closer to Reykjavik" },
        { lat: 63.9850, lng: -22.6056, label: "Keflavík Airport (KEF)", num: 4, cat: "transport", desc: "Return rental car and depart" }
      ],
      timeBlocks: [
        {
          label: "Morning",
          activities: [
            { title: "Final Reykjavik Morning", description: "Last chance to explore. Visit the Harpa Concert Hall's stunning glass facade, walk along the Sculpture and Shore Walk (Sæbraut) path, or browse the Kolaportið flea market (weekends only) for Icelandic wool, books, and fermented shark.", details: ["💡 Pick up any last souvenirs — lopapeysa sweaters, Icelandic chocolate, or volcanic salt from Saltverk"] },
            { title: "Reykjadalur Hot River (Optional Morning Hike)", description: "If you're up for one last adventure, this 3 km hike from Hveragerði leads to a natural hot river — steam rising from a river you can actually bathe in. Bring a swimsuit and towel. 45 min each way.", details: ["📍 Free · Parking at Hveragerði trailhead · 1.5-2 hours round trip + soak time", "💡 This is one of Iceland's best free hot spring experiences — a genuinely unique natural wonder"] }
          ],
          meals: [
            { type: "☕ Breakfast", name: "Brauð & Co", description: "Reykjavik's cult bakery — get there early for warm cinnamon rolls (snúður) and sourdough bread. The line is long but it moves fast.", meta: "ISK 800-2,000 · Frakkastígur 16" }
          ],
          tips: [{ type: "reddit", text: "Reykjadalur is incredible — you literally sit in a warm river surrounded by steam and mountains. Best free activity in Iceland, hands down. Start early to avoid crowds.", cite: "r/VisitingIceland" }]
        },
        {
          label: "Midday / Afternoon",
          activities: [
            { title: "Blue Lagoon", description: "Iceland's most famous attraction — milky-blue geothermal water in a lava field landscape. Book the Comfort package for entry, silica mud mask, and a drink. The water is 37-39°C and incredibly relaxing. Located near Keflavík airport — perfect timing before your flight.", details: ["📍 ISK 9,990+ · Book WAY in advance at bluelagoon.com — sells out weeks ahead", "💡 Time your visit to finish ~3 hours before your flight. The lagoon is 20 min from KEF."] },
            { title: "Alternative: Sky Lagoon", description: "If you prefer something newer and less touristy, Sky Lagoon near Reykjavik has a stunning infinity-edge pool overlooking the Atlantic, a 7-step spa ritual (cold plunge, sauna, scrub), and a more refined atmosphere.", details: ["📍 ISK 8,490+ · Vesturvör 44, Kópavogur · skylagoon.com"] }
          ],
          meals: [
            { type: "🍽️ Lunch", name: "Lava Restaurant (at Blue Lagoon)", description: "Fine dining with views over the lagoon and lava field. Excellent fish and lamb. If not doing the restaurant, the in-water bar serves drinks you can sip while soaking.", meta: "ISK 5,000-10,000 · Reservations essential" }
          ],
          tips: [{ type: "tip", text: "Blue Lagoon or Sky Lagoon — you can't go wrong. Blue Lagoon is the iconic experience; Sky Lagoon is the locals' favorite. Either way, it's the perfect bookend to your Ring Road adventure." }]
        },
        {
          label: "Evening",
          activities: [
            { title: "Return Rental Car & Depart", description: "Drive to Keflavík Airport (20 min from Blue Lagoon), return your rental car, and head to the terminal. Allow 2.5 hours before your flight for car return + check-in.", details: ["💡 Fill up the tank before returning — fuel at the airport station is the same price as anywhere else", "💡 Pick up tax-free shopping at the airport duty-free — Icelandic alcohol is much cheaper here than in stores"] }
          ],
          meals: [],
          tips: [{ type: "tip", text: "If you have an evening flight, the Keflavík airport has decent food options and a bookshop with Icelandic literature. Last chance for airport hot dogs — they're legitimately good." }]
        }
      ]
    }
  ]
};

// Day descriptions for the overview section
const dayDescs = [
  "Land in Keflavík, pick up your 4WD, and ease into Reykjavik with geothermal pools, church tower views, and the best fish pan in town.",
  "The classic Golden Circle — tectonic plates, erupting geysers, thundering Gullfoss, and a soak in the Secret Lagoon at sunset.",
  "Chase waterfalls down the South Coast — walk behind Seljalandsfoss, climb Skógafoss, and respect the raw power of Reynisfjara's black sand beach.",
  "Into the glacial realm — hike a canyon of green moss, touch ancient ice at Skaftafell, and watch icebergs drift at Jökulsárlón as diamonds wash ashore.",
  "The road less traveled — wind through dramatic Eastfjords, discover egg sculptures in fishing villages, and find the rainbow street of Seyðisfjörður.",
  "Enter the volcanic underworld — Europe's most powerful waterfall, bubbling mud pots, a Game of Thrones cave, and milky-blue Nature Baths at sunset.",
  "Whale watching in Húsavík, the Waterfall of the Gods, and a charming evening in Akureyri — Iceland's northern capital with heart-shaped traffic lights.",
  "The hidden Tröllaskagi Peninsula — Iceland's best museum about herring (trust us), an infinity pool over a fjord, and turf houses from another century.",
  "Snæfellsnes — 'Iceland in miniature' delivers a volcano from Jules Verne, lifting stones on black beaches, coastal arches, and sleepy seals.",
  "One last soak — Blue Lagoon's milky waters, Reykjavik's cult bakery, and a farewell to the land of fire and ice."
];
itineraryData.days.forEach((d, i) => { if (!d.description) d.description = dayDescs[i] || ''; });

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
