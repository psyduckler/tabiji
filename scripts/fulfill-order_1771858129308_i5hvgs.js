const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771858129308_i5hvgs',
  email: 'bernard.j.huang@gmail.com',
  destination: 'Cozumel, Quintana Roo, Mexico',
  startDate: '2026-02-25',
  endDate: '2026-02-28',
  groupSize: 1,
  requests: 'solo traveler'
};

const itineraryData = {
  destination: 'Cozumel, Mexico',
  countryEmoji: '🇲🇽',
  title: 'A Solo Diver\'s Paradise in Cozumel',
  subtitle: '3 days of world-class reefs, Caribbean beaches & island culture — just for you',
  description: "Cozumel is one of the planet's great diving and snorkeling destinations, perched along the Mesoamerican Barrier Reef — the second-largest reef system in the world. For a solo traveler, the island is absolutely ideal: the dive community is welcoming, operators make it easy to join small groups, and the laid-back town of San Miguel offers everything from fresh ceviche to cold cervezas after a day underwater. This itinerary balances underwater adventure with island exploration, Mayan ruins, and sunset dinners on the waterfront.",
  duration: '3 nights',
  dates: 'Feb 25 – Feb 28, 2026',
  budget: '$$–$$$',
  pace: 'Active',
  bestFor: 'Solo Travelers',
  highlights: [
    'Drift dive along Palancar Reef — one of the world\'s top 10 dive sites',
    'Snorkel with sea turtles and stingrays at El Cielo starfish garden',
    'Explore Punta Sur Eco Park — lighthouse, crocodiles & Caribbean views',
    'Ancient Mayan temples at San Gervasio ruins',
    'Sunset ceviche and cocktails on the San Miguel Malecón'
  ],

  essentials: [
    {
      title: '🤿 Diving Conditions',
      text: 'February is peak season — warm water (~27°C/81°F), 30m+ visibility, and the best drift diving conditions of the year. Dive shops are everywhere; two-tank morning dives are the standard offering. Book the day before for best availability.'
    },
    {
      title: '🚗 Getting Around',
      text: 'Rent a moped or car (about $40/day) to explore the island independently. Taxis are plentiful in San Miguel. The east coast road is a stunning loop — circle the whole island in a half-day. Avoid driving on the east coast at night.'
    },
    {
      title: '🌊 February Weather',
      text: 'February is dry season — expect sunshine, low humidity, and light winds. Daytime highs of 28–30°C (82–86°F). Evenings are pleasant and breezy. Perfect conditions for diving, snorkeling, and beach days. Bring reef-safe sunscreen.'
    },
    {
      title: '💵 Money & Practicalities',
      text: 'USD is widely accepted alongside Mexican pesos. Credit cards work at most restaurants and shops. Tipping in dive shops (50–100 pesos per divemaster) is customary and appreciated. The ferry from Playa del Carmen takes 45 minutes and runs frequently.'
    }
  ],

  days: [
    {
      num: 1,
      date: '2026-02-25',
      neighborhoods: 'San Miguel de Cozumel · Malecón · Waterfront',
      title: 'Arrive & Get Your Island Bearings',
      description: "Touch down on this Caribbean island and fall under its spell immediately. February skies are brilliant blue, the air smells like salt and sunscreen, and the town of San Miguel has a genuine, unhurried charm. Spend your first afternoon exploring the waterfront Malecón, visit the island's museum, and book your dive trip for tomorrow over a cold Montejo at a waterfront bar.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Check In',
              description: 'Fly into Cozumel International Airport (CZM) or take the ferry from Playa del Carmen. Drop your bags, change into light clothes, and head out to explore.',
              details: [
                '✈️ Direct flights from many US hubs — American, United, Delta, Southwest all serve CZM',
                '🚢 Ferry alternative: fly into Cancún, take an ADO bus to Playa del Carmen, then the Ultramar/Winjet ferry (45 min, runs every 30–60 min)',
                '🏨 Stay in San Miguel for easy walkable access to waterfront, restaurants, and dive shops'
              ]
            },
            {
              title: 'Museo de la Isla de Cozumel',
              description: "Get oriented with Cozumel's natural and cultural history at this excellent little museum on the Malecón. Two floors cover the island's coral reef ecosystem, Mayan history, and colonial past. A perfect 45-minute introduction to where you are.",
              details: [
                '🏛️ Rafael Melgar Avenue between Calles 4 and 6 Norte',
                '💰 Entry: ~$3 USD · Open daily 9am–5pm',
                '🐠 The coral reef diorama is genuinely impressive — see what you\'ll be diving tomorrow'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Visit a dive shop this afternoon to book your two-tank morning dive for tomorrow. Blue XT Sea Diving, Deep Blue, and Aqua Safari all have excellent reputations. Confirm Palancar Reef is on the route.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Malecón Sunset Walk',
              description: "Stroll the waterfront promenade as the sun drops over the Caribbean. The Malecón stretches north from the ferry pier with benches, sculptures, and the whole island life on display. Locals jog, kids play, and cruise ship passengers snap photos. In February, the low-angle golden light is extraordinary.",
              details: [
                '🌅 Face west from the Malecón for the best sunset views over the water',
                '📸 The ferry pier and ocean backdrop make for a great photo',
                '🚶 Walk south of the pier for a quieter, more local stretch'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kinta Mexican Bistro',
              description: 'Contemporary Mexican cuisine in a beautiful garden courtyard. Chef Kris Wallenta transforms regional ingredients into something genuinely exciting — smoky moles, fresh ceviches, inventive cocktails. One of Cozumel\'s best restaurants and a perfect first-night meal.',
              meta: '💰 $$$ · 📍 Av 5 Norte between Calles 2 and 4 · Reserve ahead, especially in Feb high season'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.5092, lng: -86.9461, label: 'San Miguel Town Center', num: 1, cat: 'attraction', desc: 'Main hub of Cozumel — ferry pier, restaurants, dive shops, waterfront' },
        { lat: 20.5088, lng: -86.9489, label: 'Museo de la Isla de Cozumel', num: 2, cat: 'attraction', desc: 'Island museum — natural history, coral reef ecosystem, Mayan heritage' },
        { lat: 20.5100, lng: -86.9469, label: 'Malecón Waterfront', num: 3, cat: 'attraction', desc: 'Scenic promenade along the harbor — perfect sunset walk' },
        { lat: 20.5065, lng: -86.9433, label: 'Kinta Mexican Bistro', num: 4, cat: 'food', desc: 'Top restaurant in Cozumel — contemporary Mexican in a garden courtyard' },
        { lat: 20.5072, lng: -86.9455, label: 'Dive Shop Row', num: 5, cat: 'attraction', desc: 'Cluster of excellent dive operators — book your morning dive here' }
      ]
    },
    {
      num: 2,
      date: '2026-02-26',
      neighborhoods: 'Palancar Reef · El Cielo · South Island · Playa Palancar',
      title: 'Dive Day — Palancar Reef & Caribbean Magic',
      description: "Today is the heart of your Cozumel experience. An early two-tank dive boat heads out to Palancar Reef, one of the greatest coral reef systems on the planet. Then in the afternoon, snorkel the famous El Cielo starfish garden and finish the day at Playa Palancar beach club with your toes in the sand and a cold drink in hand. This is what you came here for.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Two-Tank Dive — Palancar Reef',
              description: "Meet your dive boat at the pier around 8am. Palancar Reef is a 45-minute ride south, and what awaits is breathtaking — towering coral pinnacles, swim-throughs, and the effortless drift diving that Cozumel is world-famous for. The current does the work; you just glide. Expect eagle rays, sea turtles, moray eels, and schools of tropical fish.",
              details: [
                '🤿 Two-tank dive: typically 8:00am departure, back by 1pm',
                '🐢 Palancar Horseshoe and Palancar Gardens are the two main Palancar sites — both stunning',
                '🦈 Nurse sharks rest on the sandy bottom at Palancar Caves — harmless but dramatic',
                '💰 Two-tank dive: $70–90 USD including gear rental',
                '⚡ Current can be strong — listen to your divemaster\'s briefing carefully'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Eat a light breakfast before the dive. Seasickness patches are available at pharmacies if needed — the crossing can have some chop in February.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Snorkel El Cielo — Starfish Garden',
              description: "El Cielo (\"The Sky\") is a magical, shallow snorkeling spot about 5km from Palancar. The sandy bottom is covered in hundreds of large starfish, and the turquoise water is so clear it looks like floating on glass. Many dive operators include a stop here after the morning dives.",
              details: [
                '⭐ El Cielo is 3–4m deep — perfect for snorkelers and non-divers',
                '🌊 Same current as Palancar, so the water is crystal-clear',
                '📍 Often included as a \"bonus\" stop on dive boat trips — confirm with your operator'
              ]
            },
            {
              title: 'Playa Palancar Beach Club',
              description: "After a morning underwater, there\'s no better place to recover than Playa Palancar. This is the prettiest beach on the island — a protected cove with impossibly blue water, fine white sand, and a palm-shaded beach club. Stake out a sun lounger, order a fresh coconut, and soak it all in.",
              details: [
                '🌴 Loungers are free with any food/drink purchase (reasonable prices)',
                '🚗 Accessible by taxi (~$15) or rental moped from San Miguel',
                '🐠 You can snorkel straight off the beach — the reef is close to shore',
                '🍹 The beach bar serves freshly made guacamole and cold cervezas'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'La Cocay',
              description: 'Cozumel\'s most sophisticated dining experience — Mediterranean-Caribbean fusion in a beautifully lit indoor setting. The menu changes seasonally but expect outstanding seafood, inventive pasta, and a wine list that\'s exceptional for a Caribbean island. A proper reward for a day of big underwater adventures.',
              meta: '💰 $$$ · 📍 Calle 8 Norte between Av 10 and Av 15 · Indoor A/C dining, open evenings only'
            }
          ],
          tips: [
            { type: 'tip', text: 'Log your dives tonight if you\'re keeping a logbook. The divemasters often sign off at the shop after the trip. Ask about tomorrow\'s conditions for the morning dive if you want to go again.' }
          ]
        }
      ],
      mapPins: [
        { lat: 20.3175, lng: -87.0833, label: 'Palancar Reef', num: 1, cat: 'attraction', desc: 'World-class drift dive site — coral pinnacles, turtles, eagle rays' },
        { lat: 20.3492, lng: -87.0527, label: 'El Cielo (Starfish Garden)', num: 2, cat: 'attraction', desc: 'Magical shallow snorkel spot carpeted in giant starfish' },
        { lat: 20.3182, lng: -87.0768, label: 'Playa Palancar Beach Club', num: 3, cat: 'attraction', desc: "Cozumel's prettiest beach — calm cove, crystal water, beach bar" },
        { lat: 20.5092, lng: -86.9461, label: 'Dive Boat Departure', num: 4, cat: 'attraction', desc: 'Pier near San Miguel — boats depart ~8am for Palancar' },
        { lat: 20.5081, lng: -86.9428, label: 'La Cocay', num: 5, cat: 'food', desc: 'Upscale Mediterranean-Caribbean fusion — best dinner in Cozumel' }
      ]
    },
    {
      num: 3,
      date: '2026-02-27',
      neighborhoods: 'Punta Sur · East Coast · San Gervasio · San Miguel',
      title: 'Island Loop — Ruins, Wildlife & Sunset Send-Off',
      description: "Your last full day is for exploring the rest of Cozumel that isn\'t underwater. Rent a moped or car and loop the island: ancient Mayan temples at San Gervasio, wild untouched beaches on the rugged east coast, crocodiles and flamingos at Punta Sur Eco Park, and a final sunset dinner on the Malecón to close out a perfect trip.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'San Gervasio Mayan Ruins',
              description: "Cozumel was a sacred Mayan pilgrimage site dedicated to Ixchel, the goddess of fertility and the moon. Women journeyed here from across Mesoamerica. The ruins at San Gervasio are smaller than Chichén Itzá but atmospheric — set among jungle foliage, with howler monkeys often heard nearby. The site is compact and easily walked in 1–1.5 hours.",
              details: [
                '🏛️ San Gervasio is in the middle of the island — 8km from San Miguel via a paved road',
                '🌿 7 main structures in a jungle clearing — a knowledgeable guide makes a huge difference ($10–15)',
                '🐒 Listen for howler monkeys in the surrounding forest',
                '💰 Entry: ~$11 USD · Open 7am–4pm'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'El Moro',
              description: 'A Cozumel institution beloved by locals and in-the-know travelers. Massive portions of huevos rancheros, chilaquiles, and fresh-squeezed OJ at rock-bottom prices. No-frills and perfect.',
              meta: '💰 $ · 📍 75 Bis Norte, San Miguel · Open from 7am · Cash preferred'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'East Coast Drive & Wild Beaches',
              description: "Cross to the island\'s wild east coast — a dramatic contrast to the calm western shores. No development, no beach clubs, just raw Caribbean sea crashing against deserted beaches and rocky coves. The road winds south along the coast; stop at any of the roadside palapa restaurants for freshly grilled fish.",
              details: [
                '🌊 The east coast faces open Caribbean — rougher water, not for swimming',
                '🐊 Watch for iguanas and exotic birds along the roadside',
                '🌴 Chen Rio Beach has a protected cove where swimming is safe — a hidden gem',
                '🐟 The roadside palapas serve fresh grilled fish with tortillas, rice, and beans for ~$10'
              ]
            },
            {
              title: 'Punta Sur Eco Park',
              description: "At the southern tip of the island, Punta Sur is a protected ecological reserve combining a lighthouse, a lagoon full of American crocodiles, flamingo habitats, and some of the best snorkeling on the island\'s exterior (Columbia Reef is just offshore). Climb the Celarain Lighthouse for panoramic views of the entire island.",
              details: [
                '🐊 Crocodile lagoon — Laguna Colombia — has dozens of resident crocs',
                '🦩 Flamingos and herons nest in the sanctuary area seasonally',
                '🌊 Excellent snorkeling on the Caribbean side — visibility is exceptional',
                '🏡 Lighthouse dates from 1902 — climb it for 360° views',
                '💰 Entry: ~$16 USD · Open 9am–4pm'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Malecón Final Sunset',
              description: "Return to San Miguel in time for golden hour. Walk the Malecón one last time, watch the fishing boats return, and let yourself feel grateful you found this island. February sunsets over the Caribbean turn the whole sky orange and pink.",
              details: [
                '🌅 The waterfront benches near the ferry pier are perfect for solo sunset watching',
                '🍺 El Muelle Bar on the Malecón is a great spot for a cold Montejo to watch the sunset',
                '📸 The last light hits the old colonial buildings in town beautifully'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Kondesa',
              description: 'Cozumel\'s beloved rooftop restaurant with views over San Miguel and the sea. The menu blends Mexican coastal flavors with Caribbean influences — standouts include the fresh fish tacos, seafood risotto, and excellent margaritas. The rooftop setting on a warm February evening is exactly the right way to end a trip like this.',
              meta: '💰 $$$ · 📍 Av Rafael Melgar near Calle 11 · Rooftop seating — arrive before 7pm for sunset views'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.5070, lng: -86.8481, label: 'San Gervasio Ruins', num: 1, cat: 'attraction', desc: 'Ancient Mayan pilgrimage site dedicated to Ixchel — jungle-shrouded temples' },
        { lat: 20.4850, lng: -86.7900, label: 'East Coast Wild Beaches', num: 2, cat: 'attraction', desc: 'Untouched Caribbean coastline with roadside fish palapas and dramatic waves' },
        { lat: 20.4420, lng: -86.7950, label: 'Chen Rio Beach', num: 3, cat: 'attraction', desc: 'Protected east coast cove — one of the few east coast spots safe for swimming' },
        { lat: 20.2701, lng: -87.0589, label: 'Punta Sur Eco Park', num: 4, cat: 'attraction', desc: 'Ecological reserve — lighthouse, crocodile lagoon, flamingos, snorkeling' },
        { lat: 20.5095, lng: -86.9467, label: 'Malecón Waterfront', num: 5, cat: 'attraction', desc: 'Farewell sunset walk on the harbor promenade' },
        { lat: 20.5073, lng: -86.9450, label: 'El Moro Breakfast', num: 6, cat: 'food', desc: 'Local institution — giant portions, rock-bottom prices, 7am open' },
        { lat: 20.5091, lng: -86.9461, label: 'Kondesa Rooftop', num: 7, cat: 'food', desc: 'Farewell dinner — rooftop views, seafood, excellent margaritas' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$60–100/night', midrange: '$100–200/night', luxury: '$200–450/night' },
    { category: 'Meals (solo)', budget: '$20–35/day', midrange: '$40–75/day', luxury: '$80–150/day' },
    { category: 'Diving (2-tank)', budget: '$70–90/trip', midrange: '$90–120/trip', luxury: '$150–250 (private)' },
    { category: 'Park Entry Fees', budget: '$25–35/day', midrange: '$25–35/day', luxury: '$25–35/day' },
    { category: 'Transport/Rental', budget: '$15–25/day (moped)', midrange: '$40–60/day (car)', luxury: '$60–100/day (private taxi)' },
    { category: '3-Day Total (solo)', budget: '$400–600', midrange: '$700–1,100', luxury: '$1,200–2,000' }
  ],

  practicalInfo: [
    {
      title: '✈️ Getting There',
      items: [
        'Cozumel International Airport (CZM) has direct flights from major US cities (Miami, Houston, Dallas, Chicago, Atlanta)',
        'Alternative: Fly to Cancún (CUN), take ADO bus to Playa del Carmen ($10), then Ultramar ferry to Cozumel (45 min, $15 each way)',
        'Ferries run every 30–60 minutes, 6am to midnight'
      ]
    },
    {
      title: '🏨 Where to Stay',
      items: [
        'Staying in San Miguel gives you walkable access to restaurants, dive shops, and the ferry',
        'Budget: Amigos Hostel or Hotel Flamingo — clean, social, and central',
        'Mid-range: Hotel B Cozumel or Casa del Mar — comfortable with pool',
        'Splurge: Presidente InterContinental — beachfront, best on-site snorkeling on the island'
      ]
    },
    {
      title: '🌡️ February Conditions',
      items: [
        'Peak dry season — sunny skies, low humidity, water temp 27°C (81°F)',
        'Water visibility: 30m+ at most sites — best conditions of the year',
        'Light northeast winds are normal — rough on the east coast, calm on the west',
        'Reef-safe sunscreen only (regular sunscreen is banned and damages coral)'
      ]
    },
    {
      title: '📱 Connectivity & Tips',
      items: [
        'Telcel and AT&T Mexico prepaid SIMs available at the airport and pharmacies',
        'Most restaurants and hotels have WiFi',
        'Dive shops are concentrated on Av Rafael Melgar (the waterfront road)',
        'Reef-safe sunscreen (zinc oxide only) is mandatory and available locally',
        'Solo divers — dive shops will pair you with a group or divemaster easily'
      ]
    }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
