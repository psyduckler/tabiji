const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771686068692_81hnmo',
  email: 'psyduckler@gmail.com',
  destination: 'Tulum',
  startDate: '2026-02-21',
  endDate: '2026-02-24',
  groupSize: 1,
  travelStyle: 'Adventure & Culture',
  requests: ''
};

const itineraryData = {
  destination: 'Tulum, Mexico',
  countryEmoji: '🌊',
  title: 'Cenotes, Ruins & Jungle Vibes: Solo in Tulum',
  subtitle: '3 days of turquoise waters, ancient Maya mysteries, wild cenotes & the most magical stretch of Caribbean coast',
  description: "Tulum is where the ancient world meets the Caribbean sea — crumbling Maya temples perched on limestone cliffs above the turquoise Riviera Maya, crystalline cenote pools plunging into an underground river network that spans the entire Yucatán Peninsula, and a beachfront hotel zone that somehow stays bohemian despite global fame. February is peak season for good reason: zero chance of rain, 26°C ocean temps, and the cenotes at their clearest. For a solo traveler, Tulum is effortless — the town is walkable, the beach road is bikeable, and the cenotes are close enough to explore all three in a day. This itinerary covers the non-negotiables (Tulum Ruins, Gran Cenote, the beach) and the rewarding detours (Cobá's jungle pyramid, sea turtles at Akumal, a sunset Sian Ka'an boat tour). No fluff — just three dense, extraordinary days on one of the planet's most dramatically beautiful coastlines.",
  duration: '3 nights',
  dates: 'Feb 21 – Feb 24, 2026',
  budget: '$$',
  pace: 'Active',
  bestFor: 'Solo Travelers · Nature & Adventure · Culture & History',

  highlights: [
    'Swim in Gran Cenote — a cathedral of stalactites and turquoise water fed by an underground river',
    'Climb Cobá\'s Nohoch Mul pyramid for a 360° jungle canopy view — the last climbable Maya pyramid',
    'Watch sunrise over the Caribbean from the Tulum Archaeological Zone — ruins on a cliff edge',
    'Snorkel with sea turtles at Akumal Bay — they congregate here year-round in calm, shallow water',
    'Explore Dos Ojos — one of the world\'s longest underwater cave systems, now open for snorkeling',
    'Dine at Hartwood — no electricity, wood-fired everything, jungle-clearing magic under the stars'
  ],

  essentials: [
    { title: '☀️ February Weather', text: 'The best month to visit. Expect 28–30°C (82–86°F) days, low humidity, minimal rain, and 26°C ocean water. Evenings cool to a comfortable 20°C — bring a light layer for dinner. UV is intense; reef-safe SPF 50+ is essential (also required at cenotes).' },
    { title: '🚲 Getting Around', text: 'Tulum\'s hotel zone (Zona Hotelera) runs 10km along the beach road — renting a bicycle ($10–15/day) is the classic way to travel it. For Cobá, Akumal and the far cenotes, book a colectivo (shared van, very cheap) or rent a scooter ($25–40/day) from town. Avoid renting a car unless venturing to Sian Ka\'an.' },
    { title: '💧 Cenote Rules', text: 'All cenotes require reef-safe sunscreen only (regular sunscreen destroys the ecosystem — many cenotes sell eco-sunscreen at the entrance). No mosquito repellent in the water. Life jackets provided at most cenotes. Bring a waterproof bag for your phone and a quick-dry towel.' },
    { title: '📍 Two Tulums', text: 'Tulum has two distinct zones: El Pueblo (the town, 2km inland) where locals live, cheap food, and colectivos leave from, and the Zona Hotelera (beach road, 10km long) where hotels, beach clubs, and most restaurants are. Budget travelers stay in the pueblo; splurgers stay on the beach road. Both work.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-21',
      neighborhoods: 'Tulum Ruins → Zona Hotelera Beach → Tulum Pueblo',
      title: 'Arrival Day — Ruins on the Cliff & Your First Caribbean Dip',
      description: "Tulum's most iconic image — the El Castillo temple balanced on a limestone cliff above Caribbean turquoise — is your introduction to the destination. Get there early before the cruise crowds arrive, then spend the afternoon on the beach below the ruins and orient yourself in the pueblo by evening.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tulum Archaeological Zone — Ruins at Sunrise',
              description: 'Arrive at 8am when the gates open — you\'ll have the ruins nearly to yourself for the first 30–45 minutes before tour groups arrive from Cancún. The Tulum ruins are compact (walkable in 60–90 min) but dramatically situated: El Castillo temple stands on a cliff 12 meters above the Caribbean, and the views from the clifftop over the turquoise bay are among the most photogenic in the Maya world. The ruins date to 1200–1450 CE and were still an active trading port when the Spanish arrived.',
              details: [
                '⏰ Gates open 8am — arrive on the hour to beat the crowds',
                '💰 Admission: MX$95 (about $5 USD) + MX$45 parking if driving',
                '📸 Best shot: stand at the south end of the site — El Castillo framed against the turquoise sea',
                '🌊 You can descend steps to the beach below the ruins for a swim — bring your swimsuit',
                '⚠️ By 10am the site is packed with day-trippers from Cancún. Leave by 10am.',
                '📍 Zona Arqueológica de Tulum, Tulum, Quintana Roo'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Kitchen Table',
              description: 'Tulum\'s best-loved breakfast spot in El Pueblo — fresh smoothie bowls, excellent Mexican egg dishes, and the finest slow-drip coffee in town. Arrive by 7am to fuel up before the ruins.',
              meta: '💰 $ · 📍 Calle Osiris Sur, Tulum Pueblo · 7am–1pm'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Playa Paraíso & Tulum Beach Hotel Zone',
              description: 'After the ruins, head straight down to Playa Paraíso — the public beach directly beneath the ruins, named one of the most beautiful beaches in Mexico. The water is shallow and crystal-clear aquamarine, fringed by jungle and backed by white sand. This stretch of the Tulum hotel zone has the most dramatic setting: jungle-draped palapa restaurants perched above turquoise sea. Rent a beach chair ($5–10), order a fresh coconut, and simply float.',
              details: [
                '🏖️ Playa Paraíso: the public beach directly south of the ruins — accessible by walking down from the site',
                '🌴 Beach chairs: rent directly on the beach for $5–10 including a drink',
                '🐠 The water is shallow here — good for snorkeling with a mask (bring your own or rent for $5)',
                '🌊 Swim directly beneath the ruins walls — surreal to float and look up at the temple',
                '📍 Access via the road south of the ruins or directly from the archaeological zone exit'
              ]
            },
            {
              title: 'Bike the Beach Road South',
              description: 'Rent a bicycle in the hotel zone and explore the 10km beach road — the iconic strip where boutique hotels, beach clubs, and jungle restaurants line both sides. The road connects Playa Paraíso north to the beginning of Sian Ka\'an biosphere south. It\'s flat, scenic, and lined with some of the most photogenic architecture in the Riviera Maya — all palapa roofs, driftwood, and candlelit courtyards.',
              details: [
                '🚲 Bicycle rental: available at most hostels/hotels along the beach road (~$10–15/day)',
                '📸 Stop at Azulik for its treehouse architecture — visible from the road even without dining',
                '🌴 The road gets car-free farther south (good for evening cycling)',
                '💡 Download offline maps — the road has no addresses, everything is by GPS or landmark'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'February water temps are 26°C — warm enough to swim all day without discomfort. No jellyfish season either. You\'re visiting at the best possible time.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Hartwood',
              description: 'The restaurant that put Tulum on the culinary map — Eric Werner and Mya Henry opened this entirely off-grid, no-electricity, wood-fire kitchen in the jungle in 2010 and it became a global pilgrimage. Everything is sourced locally, cooked over an open mesquite and applewood fire, and served in an open-air garden under the stars. The menu changes daily. The whole grilled fish with charred salsa verde is the benchmark dish. Arrive before opening (5:30pm) to queue — no reservations.',
              meta: '💰 $$$ · 📍 Carretera Tulum-Boca Paila Km 7.6, Zona Hotelera · Open Tue–Sun from 5:30pm · No reservations — arrive by 5pm to queue'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.2141, lng: -87.4290, label: 'Tulum Ruins (El Castillo)', num: 1, cat: 'attraction', desc: 'Maya clifftop ruins overlooking the Caribbean — most photogenic spot in Tulum' },
        { lat: 20.2073, lng: -87.4337, label: 'Playa Paraíso', num: 2, cat: 'attraction', desc: 'Stunning white sand beach below the ruins — aquamarine shallow water' },
        { lat: 20.2109, lng: -87.4654, label: 'Kitchen Table', num: 3, cat: 'food', desc: 'Best breakfast in Tulum Pueblo — smoothie bowls, eggs, slow-drip coffee' },
        { lat: 20.2001, lng: -87.4360, label: 'Hartwood Restaurant', num: 4, cat: 'food', desc: 'World-famous off-grid wood-fire restaurant — no electricity, no reservations' },
        { lat: 20.1920, lng: -87.4362, label: 'Tulum Hotel Zone Beach Road', num: 5, cat: 'attraction', desc: 'Iconic 10km beach strip — jungle boutique hotels, beach clubs, palapa restaurants' }
      ]
    },
    {
      num: 2,
      date: '2026-02-22',
      neighborhoods: 'Gran Cenote → Dos Ojos → Cenote Calavera → Tulum Pueblo',
      title: 'Cenote Day — Underground Rivers & Stalactite Cathedrals',
      description: "The Yucatán Peninsula sits atop the world's largest underground river network — the Dos Ojos system alone stretches over 100km. Cenotes are the sinkholes where this subterranean world meets the surface: crystal-clear, cave-lit, stalactite-hung, and so geologically ancient that some harbor species found nowhere else. Today you explore the three best cenotes accessible from Tulum — each with a distinct character.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Gran Cenote — The Cathedral',
              description: 'The closest cenote to Tulum (3km from the ruins) and one of the most beautiful in the Yucatán. Gran Cenote is a semi-open sinkhole with one end enclosed in a limestone cave dripping with stalactites and stalagmites. Snorkel through the cave mouth into the open-air pool — visibility is 15–20 meters in the clear cenote water, and you\'ll spot freshwater turtles resting on the bottom. Arrive exactly at 8am opening to beat the crowds.',
              details: [
                '⏰ Open 8am–5pm — arrive at 8am sharp, it fills quickly by 10am',
                '💰 Entry: MX$400 (about $20 USD) — includes life jacket',
                '🤿 Snorkel rental: $5–7 on site, or bring your own',
                '🐢 Freshwater turtles are resident here — you\'ll almost certainly see them snorkeling',
                '📸 Best photos: the cave mouth where sunlight filters down through the stalactites — otherworldly',
                '📍 Carretera Tulum-Coba Km 3, 3km west of the ruins'
              ]
            },
            {
              title: 'Cenote Calavera — The Temple of Doom',
              description: 'A 5-minute drive west of Gran Cenote, Cenote Calavera is a deep, circular sinkhole with three natural openings in the limestone ceiling — the main entrance (via a metal ladder) and two smaller holes that give it a skull-like appearance from above (hence "Calavera" = skull). Leap off the edge into the deep pool for the classic photo, or take the ladder down sedately. Less visited than Gran, more dramatic.',
              details: [
                '💰 Entry: ~MX$200 (about $10 USD)',
                '🏊 The jump-in holes are 1m and 2m height — perfectly safe, well-checked',
                '📸 Look up from the water — the circular holes frame sun rays in the pool',
                '🤿 Snorkeling is good here too — less coral but beautiful geology',
                '📍 Near Gran Cenote on Carretera Tulum-Cobá'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'El Asadero (Pueblo)',
              description: 'Grab a quick breakfast taco from this beloved Tulum Pueblo institution before heading out early — cochinita pibil tacos from 7am, crowd of locals, three-peso coffee.',
              meta: '💰 $ · 📍 Calle Centauro Norte, Tulum Pueblo · Open from 7am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Dos Ojos Cenote System — The Deep Dive',
              description: 'Dos Ojos ("Two Eyes") is one of the most spectacular cenotes in the Riviera Maya — two interconnected sinkholes linked by an underwater passageway, part of the longest flooded cave system ever explored (the Sac Actun system, 376km of mapped passages). For non-divers, the snorkeling through the "Barbie Line" shallow passage into the main cenote is extraordinary: crystal water, bat cave gallery, and ancient stalactites illuminated by your headlamp. Book the guided cave snorkel tour (45 min, ~$35).',
              details: [
                '⏰ Open 8am–5pm · Book guided cave snorkel at entrance: ~$35 (includes guide, life jacket, lights)',
                '🦇 The "Barbie Line" — the cave passage is so named for its pink lighting effect',
                '🌊 Visibility: 30–40 meters — the clearest water you\'ll likely ever snorkel in',
                '🤿 No experience necessary for the snorkel tour — guide leads single file through the cave',
                '💡 Headlamp provided; go at ~1pm when sun angles into the cave openings most dramatically',
                '📍 Carretera Tulum-Boca Paila Km 12.5 · About 20 min south of Tulum by car/moto'
              ]
            }
          ],
          meals: [
            {
              type: '🥗 Lunch',
              name: 'Cenote Dos Ojos Restaurant (on site)',
              description: 'Simple but good Mexican food at the cenote itself — fresh tacos, grilled chicken, agua fresca. Eat here to save time between cenotes.',
              meta: '💰 $ · 📍 Dos Ojos complex, on-site'
            }
          ],
          tips: [
            { type: 'tip', text: 'Apply reef-safe sunscreen and let it fully absorb BEFORE entering the cenote — cenotes connect directly to the underwater river system that feeds local reefs. The fine at some cenotes for non-reef-safe sunscreen is $200 USD.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset at Tulum Beach — Ahau or La Zebra',
              description: 'Return to the hotel zone for a beach sunset. Ahau Tulum and La Zebra Beach Club both have excellent sunset programming — DJ, cocktails, toes in the sand. La Zebra\'s weekend live cumbia band is legendary; Ahau is moodier and more design-forward. Either works for a cenote-sore, sun-kissed solo traveler.',
              details: [
                '🌅 Sunset in Tulum in late February: around 6:15–6:20pm',
                '🍹 A michelada or margarita on the beach is non-negotiable at this point',
                '🎵 La Zebra has live music on Saturday nights — check the day',
                '📍 La Zebra: Carretera Tulum-Boca Paila Km 8.2 · Ahau: Km 7'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Posada Margherita',
              description: 'The best Italian food on the Caribbean coast — and possibly the most romantic setting. An Italian couple opened this beachfront trattoria and have been making fresh pasta with local seafood ingredients ever since. The tagliatelle with lobster is extraordinary. Set right on the sand — you can hear the waves.',
              meta: '💰 $$$ · 📍 Carretera Tulum-Boca Paila Km 4.5 · Reservations recommended for February'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.2203, lng: -87.4672, label: 'Gran Cenote', num: 1, cat: 'attraction', desc: 'Most beautiful cenote near Tulum — stalactite cave, turtles, crystal water' },
        { lat: 20.2252, lng: -87.4692, label: 'Cenote Calavera (Temple of Doom)', num: 2, cat: 'attraction', desc: 'Deep circular sinkhole — jump through skull-shaped ceiling holes into the pool' },
        { lat: 20.1737, lng: -87.5033, label: 'Dos Ojos Cenote System', num: 3, cat: 'attraction', desc: 'Cave snorkel through one of the world\'s longest underwater river systems' },
        { lat: 20.1900, lng: -87.4358, label: 'La Zebra Beach Club', num: 4, cat: 'attraction', desc: 'Sunset beach club — cocktails, live music, Caribbean views' },
        { lat: 20.1989, lng: -87.4367, label: 'Posada Margherita', num: 5, cat: 'food', desc: 'Beachfront Italian — fresh pasta, local seafood, waves at your table' }
      ]
    },
    {
      num: 3,
      date: '2026-02-23',
      neighborhoods: 'Cobá Ruins → Akumal → Tulum Pueblo (farewell)',
      title: 'Cobá Pyramid & Sea Turtles — The Yucatán Beyond the Beach',
      description: "Today ventures into the jungle and along the coast for two experiences that are genuinely unique in the region: climbing the tallest climbable pyramid in the Yucatán (Cobá's Nohoch Mul, 42 meters, still open when most are closed) and snorkeling with wild sea turtles at Akumal Bay — where loggerhead and green turtles feed on the seagrass year-round just 30 meters from shore.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Cobá Archaeological Site — The Climbable Pyramid',
              description: 'One hour northwest of Tulum, Cobá is everything Tulum Ruins is not: vast, jungle-covered, relatively uncrowded, and — uniquely in the Maya world — you can still climb the main pyramid. Nohoch Mul stands 42 meters above the jungle floor; at the summit, an unbroken 360° canopy extends to the horizon in every direction. The site covers 70 square kilometers and connected to other cities via an ancient Maya road network (sacbé). Bike or walk between the main groups (bikes available at the entrance). The ruins date to 250–900 CE, peak Classic Maya period.',
              details: [
                '⏰ Open 8am–5pm — arrive by 8am; Cobá is 1hr drive from Tulum via MEX-180',
                '💰 Entry: MX$95 ($5 USD) + bike rental inside the site $2–3',
                '🧗 Nohoch Mul pyramid: still open to climb (unlike Chichén Itzá) — rope provided, steep but doable',
                '🌳 The jungle surround means howler monkeys, tropical birds, and butterflies en route',
                '📸 Summit view: unbroken jungle canopy — dramatically different from Tulum\'s coastal setting',
                '⚠️ Closed-toe shoes strongly recommended — the steps are steep and uneven'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Early grab from Tulum Pueblo',
              description: 'Stock up before the 1hr drive — grab pastries and coffee from Antojitos La Chiapaneca in the pueblo (opens 7am). Eat at the wheel; you want maximum time at Cobá.',
              meta: '💰 $ · 📍 Tulum Pueblo · Takeaway'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Akumal Bay — Snorkeling with Sea Turtles',
              description: 'Akumal ("Place of the Turtles" in Maya) is a crescent bay 30km north of Tulum where a seagrass meadow in 2–3 meters of water draws loggerhead and green sea turtles to feed year-round. You can wade in from shore and find yourself surrounded by turtles within five minutes — some are genuinely enormous (80–100cm shell). No boat needed; the entire experience is a 3-minute walk from the car park. February is optimal — the water is calm, visibility excellent, and tourist density lower than July.',
              details: [
                '🐢 Turtles are almost guaranteed — the seagrass meadow supports a permanent population',
                '🤿 Snorkel gear rental at the beach: $10–15 including fins and mask',
                '⚠️ Do not touch or stand on turtles — rangers patrol and will ask you to leave',
                '💰 Free entry; small parking fee; gear rental on site',
                '📍 Akumal is on the 307 coastal highway, 30km north of Tulum — signed clearly',
                '⏰ Go by 1–2pm after Cobá — 30-min drive from the Cobá ruins back toward Tulum'
              ]
            },
            {
              title: 'Cenote Aktun-Ha (Carwash) — The Local Secret',
              description: 'On the way back from Akumal, stop at Cenote Aktun-Ha (locally called "Carwash" because taxi drivers used to wash their cars here). It\'s larger, quieter, and less touristy than Gran Cenote — a wide, lily-pad-dotted open cenote with a cave section at one end. Crocodiles have been spotted here (they\'re harmless and rare, but watch for the signs). The best afternoon light of any cenote in the region.',
              details: [
                '🌿 Wide, open cenote with lily pads and a cave mouth — photogenic at afternoon angles',
                '💰 Entry: ~MX$200 ($10 USD)',
                '🐊 Crocodile warning signs are posted — follow them (no incidents, but respect the wildlife)',
                '🤿 Great snorkeling in the cave section — bring a flashlight or rent one on site',
                '📍 Carretera Tulum-Cobá Km 2 — very close to Tulum town'
              ]
            }
          ],
          meals: [
            {
              type: '🥗 Lunch',
              name: 'La Cueva del Pescador, Akumal',
              description: 'Right at Akumal Bay — casual seafood palapa perfect for post-turtle-snorkel. The ceviche is fresh, the fresh-catch tacos are excellent, and the views of the calm turquoise bay complete the picture.',
              meta: '💰 $$ · 📍 Akumal Centro, beach road · Open noon–5pm'
            }
          ],
          tips: [
            { type: 'tip', text: 'Tulum\'s pet peeve for visitors: the road between Cobá, Akumal, and Tulum is easily done by colectivo for about $2–3 per leg (depart from ADO bus terminal or the colectivo hub on Avenida Tulum in el Pueblo). Cheaper than a scooter and totally reliable.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Explore El Pueblo — The Real Tulum',
              description: 'Your last evening in Tulum belongs to the pueblo — the working town that keeps the whole show running. Avenida Tulum is the main drag: taco stands, mezcal bars, local boutiques selling Maya-inspired jewelry, and a genuine neighborhood energy completely absent from the hotel zone. Walk south from the bus station; the Mercado Municipal has fresh produce, cheap food stalls, and the daily bustle of a Mexican town doing its thing. Stop at a mezcalería for a proper send-off.',
              details: [
                '🌮 Best tacos in Tulum: El Camello Jr (seafood tacos, open late) on Avenida Tulum',
                '🥃 Mezcal bar: La Mezcalería on Avenida Satélite — 150+ mezcals, knowledgeable staff',
                '🛒 Mercado Municipal: local produce market, cheap quesadillas, smoothie vendors',
                '🌙 The pueblo has the most authentic energy after 8pm when the beach crowd thins out'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Arca',
              description: 'The most exciting restaurant in Tulum — Chef José Luis Hinostroza\'s kitchen uses ancient Mesoamerican techniques (nixtamal, fermentation, wood fire) with contemporary Mexican intelligence. The duck mole enchiladas and the grilled octopus with black bean purée are worth a 45-minute wait (no reservations; put your name on the list at 6:30pm for a 7:30pm table). Finish with their mezcal-forward cocktail list. This is what Tulum tastes like at its very best.',
              meta: '💰 $$$  · 📍 Carretera Tulum-Boca Paila Km 4.5 · No reservations — arrive by 6:30pm to add to waitlist'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.4936, lng: -87.7182, label: 'Cobá Archaeological Site', num: 1, cat: 'attraction', desc: 'Climbable Nohoch Mul pyramid — 42m above the Yucatán jungle canopy' },
        { lat: 20.3946, lng: -87.3149, label: 'Akumal Bay', num: 2, cat: 'attraction', desc: 'Snorkel with wild loggerhead and green sea turtles in 2–3m of water' },
        { lat: 20.2274, lng: -87.4671, label: 'Cenote Aktun-Ha (Carwash)', num: 3, cat: 'attraction', desc: 'Wide lily-pad cenote with cave — the quieter local alternative' },
        { lat: 20.2109, lng: -87.4654, label: 'Tulum Pueblo / Avenida Tulum', num: 4, cat: 'attraction', desc: 'The real Tulum — taco stands, mezcal bars, Mercado Municipal' },
        { lat: 20.2075, lng: -87.4652, label: 'La Mezcalería', num: 5, cat: 'food', desc: '150+ mezcals — best mezcal selection in Tulum Pueblo' },
        { lat: 20.1960, lng: -87.4351, label: 'Arca Restaurant', num: 6, cat: 'food', desc: 'Contemporary Mesoamerican cuisine — Tulum\'s most exciting kitchen' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$30–60/night (hostel/guesthouse in pueblo)', midrange: '$80–150/night (hotel zone palapa)', luxury: '$300–700/night (beachfront boutique)' },
    { category: 'Meals (solo)', budget: '$20–35/day (tacos & local spots)', midrange: '$60–100/day', luxury: '$150–250/day' },
    { category: 'Transport', budget: '$15–25/day (colectivos + cenote bike)', midrange: '$35–55/day (scooter)', luxury: '$70–120/day (car rental)' },
    { category: 'Cenotes & Activities', budget: '$40–60/day', midrange: '$70–100/day', luxury: '$120–200/day (private guides)' },
    { category: '3-Day Total (solo)', budget: '$300–500', midrange: '$600–1,000', luxury: '$1,500–3,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Cancún International (CUN) — 2hr direct from most US cities', 'Cancún to Tulum: ADO bus ($10, 2hrs — most comfortable), colectivo ($5, faster but cramped), or taxi ($70–90)', 'ADO buses run on the hour from Cancún airport terminal; book tickets at the terminal window'] },
    { title: '🏨 Where to Stay', items: ['Tulum Pueblo: $30–80/night — best base for budget travelers, easy colectivo access to everything', 'Zona Hotelera north: $150–400/night — closest to the ruins, best beach access', 'Zona Hotelera south (near Hartwood): $250–700/night — most "Tulum vibe" bohemian energy', 'Best hostels: Mango Tulum (pueblo, social), Che Tulum (beach road, party)'] },
    { title: '💳 Money & Costs', items: ['Pesos preferred — dollar surcharge at tourist venues', 'ATMs in pueblo: Banamex and HSBC most reliable (fewer skimmer reports)', 'USD accepted everywhere but at poor exchange rates', 'Cenotes: bring exact cash — MX$200–500 per site'] },
    { title: '🦟 Health & Safety', items: ['Mosquitoes: heavy inland and near cenotes at dusk — DEET repellent on everything NOT going in the water', 'Reef-safe sunscreen is mandatory at cenotes and appreciated on the reef', 'Tap water not safe — buy a 5L jug ($1) from any convenience store and refill your bottle', 'Safety: Tulum Pueblo is generally safe for solo travelers; use common sense at night'] },
    { title: '📱 Practical Notes', items: ['SIM card: buy a Telcel SIM at the Cancún airport ($10–15 with 3GB data, best signal in Yucatán)', 'The beach road has no numbered addresses — everything is by kilometer marker (e.g. "Km 7.6")', 'Download offline maps before arriving (Google Maps works well for Tulum cenotes)', 'February weather: virtually zero rain chance — no raincoat needed', 'Solo travel rating: Tulum is extremely solo-friendly — cenotes, restaurants, and beach clubs all welcome single travelers'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
