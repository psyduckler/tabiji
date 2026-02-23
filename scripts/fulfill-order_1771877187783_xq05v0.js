const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771877187783_xq05v0',
  email: 'dogmurras@gmail.com',
  destination: 'Alicante, Spain',
  startDate: '2026-03-01',
  endDate: '2026-03-08',
  groupSize: 1,
  style: 'Adventure, Relaxation',
  dining: 'Casual',
  budget: 'Under $1,000',
  requests: 'Place to hike for a day, check as many beaches as possible by foot'
};

const itineraryData = {
  destination: 'Alicante, Spain',
  countryEmoji: '🇪🇸',
  title: 'Alicante on Foot — Beaches, Castles & Hidden Coves',
  subtitle: '7 days of coastal hikes, sun-drenched beaches & tapas for the solo adventurer',
  description: "Alicante is made for exactly this kind of trip. A castle that rises straight out of the city, a chain of golden beaches you can walk between, secret coves reached only on foot, and a hilltop ridge with panoramic views of the Mediterranean. The city itself is compact and walkable — you'll spend your mornings exploring coastal trails and your evenings discovering why Spain's tapas culture is world famous. March brings mild sunshine, uncrowded beaches, and some of the cheapest accommodation you'll find all year.",
  duration: '7 nights',
  dates: 'Mar 1 – Mar 8, 2026',
  budget: '$',
  pace: 'Active',
  bestFor: 'Solo adventurers',
  highlights: [
    'Climb Castillo de Santa Bárbara towering over the sea',
    'Full-day Cabo de las Huertas coastal walk through hidden coves',
    'Serra Grossa ridge hike with panoramic Mediterranean views',
    'Playa de San Juan to Almadraba beach-hopping by foot and tram',
    'Tapas crawl through El Barrio — Alicante\'s lively old quarter'
  ],

  essentials: [
    { title: '☀️ March Weather', text: 'Alicante in March is warm and sunny — expect 17–20°C (63–68°F) with long daylight hours. The sea is around 14°C (cool but refreshing for a brave dip). Pack layers for evenings, SPF for daytime hiking.' },
    { title: '👟 Getting Around on Foot', text: 'Most beaches within the city are walkable. The TRAM (tram/metro) connects El Postiguet to Playa de San Juan for €1.50 each way. Otherwise, a good pair of walking shoes gets you everywhere.' },
    { title: '🥘 Eating on a Budget', text: 'Spain is incredibly affordable. A menú del día (3 courses + wine) costs €10–12. Tapas bars in El Barrio serve free tapas with every drink in many places. Mercado Central is perfect for cheap fresh snacks.' },
    { title: '🎒 Solo Traveller Tips', text: 'Alicante is very safe and welcoming. Hostels are social hubs — Pension La Milagrosa and Hostel Alifornia are popular. The tapas crawl scene is perfect for meeting fellow travellers. Spanish people are warm and enjoy chatting with solo visitors.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-01',
      neighborhoods: 'El Barrio · Explanada · El Postiguet',
      title: 'Arrival — Old Quarter, Promenade & First Beach',
      description: "Touch down in Alicante and let the city sink in. The famous Explanada de España palm promenade runs right along the port, El Barrio's tapas bars are waiting, and your first beach — El Postiguet — lies at the foot of a floodlit castle. A perfect, low-key arrival day.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Check In & Explore El Barrio',
              description: "Drop your bags and head straight into El Barrio — Alicante's 16th-century old quarter. The narrow lanes are packed with tapas bars, local shops, and hidden plazas. The neighbourhood climbs toward the base of the castle.",
              details: [
                '🏠 Stay near the Explanada or El Barrio for maximum walkability',
                '🍺 Bar Nou Manolín — legendary tapas, ask for whatever\'s on the bar',
                '📍 Plaza de Toros area has cheap, authentic local bars'
              ]
            },
            {
              title: 'Explanada de España & Port Walk',
              description: "Stroll the Explanada — a 500m palm-lined promenade paved with 6 million marble mosaic tiles. It runs along the port and is the city's social heart, especially at sunset.",
              details: [
                '🌴 One of Spain\'s most famous promenades — free to walk',
                '📸 The reflections in the mosaic tiles at golden hour are stunning',
                '🚢 Look out at the port — ferries to Ibiza and the Balearics depart from here'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Afternoon snack',
              name: 'Mercado Central de Abastos',
              description: "Pop into the covered market for a cheap, fresh bite — jamón croquetas, fresh fruit, local olives. A great introduction to Valencian food culture.",
              meta: '💰 $ · 📍 Av. Alfonso X El Sabio · Open Mon–Sat mornings'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'El Postiguet Beach at Sunset',
              description: "Walk to El Postiguet — the city's urban beach right at the foot of Castillo de Santa Bárbara. In March it's quiet and photogenic. Sit on the sand as the castle lights up at dusk.",
              details: [
                '🏖️ 5-minute walk from the Explanada',
                '🏰 The castle silhouette against the evening sky is spectacular',
                '🌊 March sea is cool but refreshing if you\'re brave'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'El Barrio tapas crawl',
              description: "Spend your first evening hopping through El Barrio. Start at La Tasca del Barrio for wines, move to Sento Barrio for modern tapas, finish with arroz a banda (Alicante's signature rice) wherever looks busy.",
              meta: '💰 $ · 📍 El Barrio streets around Plaza de Carmen'
            }
          ],
          tips: [
            { type: 'tip', text: "In El Barrio, follow the Spanish rule: eat where locals eat. If a bar has no tourists and everyone\'s standing — that\'s your spot." }
          ]
        }
      ],
      mapPins: [
        { lat: 38.3454, lng: -0.4836, label: 'El Barrio (Old Quarter)', num: 1, cat: 'attraction', desc: '16th-century quarter with tapas bars and narrow lanes' },
        { lat: 38.3436, lng: -0.4853, label: 'Explanada de España', num: 2, cat: 'attraction', desc: 'Famous mosaic palm promenade along the port' },
        { lat: 38.3440, lng: -0.4901, label: 'Mercado Central', num: 3, cat: 'food', desc: 'Covered market for fresh local snacks' },
        { lat: 38.3455, lng: -0.4779, label: 'Playa El Postiguet', num: 4, cat: 'attraction', desc: 'City beach at the foot of Santa Bárbara Castle' },
        { lat: 38.3454, lng: -0.4836, label: 'La Tasca del Barrio', num: 5, cat: 'food', desc: 'Lively wine and tapas bar in the old quarter' }
      ]
    },
    {
      num: 2,
      date: '2026-03-02',
      neighborhoods: 'Castillo de Santa Bárbara · El Postiguet · El Barrio',
      title: 'Castle Morning & Beach Afternoon',
      description: "Start with the castle — it's unmissable and the views explain everything about Alicante. Then descend to El Postiguet, follow the coastal path east toward the Albufereta, and end with a classic menú del día lunch in the old town.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Castillo de Santa Bárbara',
              description: "The castle sits 166m above the city on Mount Benacantil — you can hike up through the old town or take the free elevator built into the rock face. The views of the bay, the Explanada, and the coastline stretching to Cabo de las Huertas are extraordinary.",
              details: [
                '🏰 Free entry to the grounds — elevator access from Postiguet beach side',
                '⏰ Allow 2 hours to explore the three levels of fortification',
                '📸 The best panoramic views of Alicante you\'ll find anywhere',
                '🥾 Hike up via Calle San Rafael for the old-town approach — more atmospheric'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Coastal Walk: El Postiguet → Playa del Cocó → Albufereta',
              description: "After the castle, head down to El Postiguet then walk the coast northeast. Past the rocky Playa del Cocó and around the headland brings you to Playa de la Albufereta — a calm, sheltered bay about 2km from the castle. These are your first two walkable beaches of the trip.",
              details: [
                '🏖️ El Postiguet → Playa del Cocó → Albufereta: ~2.5km total on foot',
                '🪨 Playa del Cocó is rocky and wild — great for exploring',
                '🌊 Albufereta is sheltered and calm — popular with families and locals',
                '☕ Several beach bars (chiringuitos) at Albufereta are open year-round'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Menú del Día — any local bar near El Barrio',
              description: "Spain's greatest institution — a 3-course lunch with bread, wine or water for €10–12. Look for handwritten chalkboard menus outside busy local bars on Calle Mayor or around the Explanada.",
              meta: '💰 $ · 📍 Calle Mayor or Calle San Nicolás area'
            }
          ],
          tips: [
            { type: 'tip', text: "The menú del día is typically served 1pm–3:30pm. Order before 2:30pm for the freshest options and a real locals\' lunch experience." }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍺 Evening drinks',
              name: 'Chiringuito at Albufereta',
              description: "Sit at a beachside bar at Albufereta and watch the sun drop into the hills behind the city. Order a Valencian agua de Valencia (cava, OJ, vodka) and a plate of boquerones.",
              meta: '💰 $ · 📍 Paseo de la Albufereta'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 38.3482, lng: -0.4787, label: 'Castillo de Santa Bárbara', num: 1, cat: 'attraction', desc: 'Moorish fortress 166m above the city — free entry, spectacular views' },
        { lat: 38.3455, lng: -0.4779, label: 'Playa El Postiguet', num: 2, cat: 'attraction', desc: 'Urban city beach at the castle\'s foot' },
        { lat: 38.3490, lng: -0.4720, label: 'Playa del Cocó', num: 3, cat: 'attraction', desc: 'Wild, rocky cove between Postiguet and Albufereta' },
        { lat: 38.3535, lng: -0.4630, label: 'Playa de la Albufereta', num: 4, cat: 'attraction', desc: 'Calm sheltered bay with local chiringuitos, 2km east of castle' },
        { lat: 38.3436, lng: -0.4853, label: 'El Barrio lunch spot', num: 5, cat: 'food', desc: 'Classic menú del día for €10–12 in the old quarter' }
      ]
    },
    {
      num: 3,
      date: '2026-03-03',
      neighborhoods: 'Cabo de las Huertas · Cala Palmera · Cala Cantalar',
      title: 'The Coves Walk — Cabo de las Huertas Coastal Trail',
      description: "This is your big beach day. The Cabo de las Huertas coastal trail is one of Alicante's best-kept secrets — a 7km footpath that winds past a string of wild coves, rocky headlands, and hidden swimming spots. You'll hit four to six distinct beaches and coves, all only reachable by foot. Zero crowds, clear water, dramatic cliffs.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Walk to Cabo de las Huertas Trailhead',
              description: "Head northeast along the coast from Albufereta (or take a short bus to Cabo de las Huertas). The trail begins at the cape and winds along a dramatic rocky coastline with the Mediterranean to your right at every step.",
              details: [
                '🚌 Bus L21 from center takes ~25 min to Cabo de las Huertas',
                '🥾 Wear proper footwear — the path is rocky in places but well-marked',
                '💧 Bring 1.5L water and snacks — no shops on the trail',
                '🗺️ Full trail: Cala del Palmeral → Cala Palmera → Cala Cantalares → Cala Lagranja → Playa de la Almadraba (~7.6km)'
              ]
            }
          ]
        },
        {
          label: 'All Day',
          activities: [
            {
              title: 'Cala del Palmeral',
              description: "First cove on the trail — a sliver of sand between limestone cliffs, only accessible on foot. The water is crystal clear and the beach is rarely crowded even in peak season. In March you'll often have it entirely to yourself.",
              details: [
                '🏊 Water visibility here is exceptional for snorkelling',
                '🦎 Watch for lizards on the warm rocks',
                '📸 The approach through the pine-scented scrubland is beautiful'
              ]
            },
            {
              title: 'Cala Palmera → Cala Cantalares',
              description: "Continue along the coastal path past Cala Palmera (another secluded cove with fossil-rich rocks) to Cala Cantalares — a wider, sandy-bottomed cove perfect for a swim. The fossil beds along this stretch are a highlight — ancient mollusk shells embedded in the stone.",
              details: [
                '🔬 Palaeontological fossils visible at low tide — remarkable',
                '🌊 Cala Cantalares has calmer, swimmable water even in March',
                '🪨 The headlands between coves offer great views back toward the castle'
              ]
            },
            {
              title: 'Cala Lagranja → Playa de la Almadraba',
              description: "The trail ends at Playa de la Almadraba — a proper beach with a bar open year-round. This is your lunch stop after 7km of coastal walking. Well earned.",
              details: [
                '🏖️ Almadraba is a Blue Flag beach with services',
                '🍺 Beach bar (chiringuito) serves bocadillos, beer, and fresh seafood',
                '🚌 Bus back to center from here, or continue walking to San Juan (3km more)'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Chiringuito at Playa de la Almadraba',
              description: "Collapse at the beach bar after your coastal hike. Order a bocadillo de jamón, cold Estrella Damm, and the freshest grilled fish they have. You\'ve earned it.",
              meta: '💰 $ · 📍 Playa de la Almadraba, end of the coastal trail'
            }
          ],
          tips: [
            { type: 'tip', text: "Start early (9am) to have the coves to yourself and finish before the afternoon wind picks up. The trail goes west-to-east, so morning sun will be at your back." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Return to City & Recovery Dinner',
              description: "Bus or short walk back to the city center. Your legs will be tired — reward yourself with a proper sit-down dinner in El Barrio.",
              details: [
                '🦶 ~7.6km of coastal trail = well-earned dinner',
                '🚌 Bus from Almadraba back to center is about 20 min'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Nou Manolín',
              description: "Alicante's most famous restaurant — started as a bar in 1972 and still has the best tapas counter in town. Order the gambas a la plancha, local wine, and whatever rice dish they're serving.",
              meta: '💰 $$ · 📍 Calle Villegas 3, El Barrio'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 38.3542, lng: -0.4408, label: 'Cabo de las Huertas (start)', num: 1, cat: 'attraction', desc: 'Coastal trail trailhead — path runs northeast along wild coves' },
        { lat: 38.3553, lng: -0.4390, label: 'Cala del Palmeral', num: 2, cat: 'attraction', desc: 'First hidden cove — foot access only, crystal-clear water' },
        { lat: 38.3562, lng: -0.4368, label: 'Cala Palmera', num: 3, cat: 'attraction', desc: 'Fossil-rich rocky cove — rare palaeontological finds at low tide' },
        { lat: 38.3578, lng: -0.4340, label: 'Cala Cantalares', num: 4, cat: 'attraction', desc: 'Sandy-bottomed cove with calm, swimmable water' },
        { lat: 38.3605, lng: -0.4305, label: 'Cala Lagranja', num: 5, cat: 'attraction', desc: 'Dramatic clifftop views before descent to Almadraba' },
        { lat: 38.3628, lng: -0.4271, label: 'Playa de la Almadraba', num: 6, cat: 'attraction', desc: 'Blue Flag beach — end of the trail, beach bar for post-hike lunch' },
        { lat: 38.3454, lng: -0.4836, label: 'Nou Manolín', num: 7, cat: 'food', desc: 'Alicante\'s legendary tapas counter — gambas a la plancha' }
      ]
    },
    {
      num: 4,
      date: '2026-03-04',
      neighborhoods: 'Serra Grossa · Parque de la Ereta · City Views',
      title: 'The Big Hike — Serra Grossa Ridge',
      description: "Your dedicated hiking day. Serra Grossa is Alicante's natural ridge that rises north of the city — a full-day adventure with sweeping Mediterranean panoramas, quiet pine trails, and the satisfaction of earning your views on foot. This is the highest point accessible from the city without a car.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Serra Grossa Trail — City to Summit',
              description: "Begin at Parque de la Ereta (the hillside park between the old town and Serra Grossa) and follow the trail north-northeast up to the Serra Grossa ridge. The ridge walk rewards you with 360° views — Alicante's bay below, the salt flats inland, and on clear days the islands of Tabarca and Ibiza on the horizon.",
              details: [
                '🥾 Approx 10km round trip, moderate difficulty — rocky but well-marked',
                '⏰ Allow 4–5 hours for the full ridge walk with stops',
                '👟 Trail shoes or sturdy trainers required — loose rock on upper section',
                '💧 Bring 2L water — no water sources on the trail',
                '📍 Start from Parque de la Ereta entrance, Calle Juan de Herrera'
              ]
            }
          ],
          meals: [
            {
              type: '🍞 Pre-hike breakfast',
              name: 'Café near Explanada',
              description: "Fuel up before the climb — a tostada con tomate y jamón (toasted bread with tomato and ham) and a strong café con leche at any bar near the Explanada.",
              meta: '💰 $ · 📍 Any bar around Explanada de España'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Parque de la Ereta — Descent Through Terraced Gardens',
              description: "On your way back down, take the lower path through Parque de la Ereta — a beautiful tiered hillside garden with fountains, viewpoints, and a free outdoor café. The views of the old town and castle from here are the best in the city.",
              details: [
                '🌳 The park has multiple viewpoint terraces — each angle is different',
                '☕ The park café is a great spot to rest aching legs',
                '📸 The classic "Alicante postcard" shot: Ereta viewpoint with castle, old town, and bay'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "Serra Grossa is best in the morning when the light hits the coast from the east. Start by 8:30am to have the ridge to yourself and finish before midday heat." }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Recovery at El Postiguet & Sunset on the Explanada',
              description: "Cool tired legs at El Postiguet beach, then walk the Explanada for the evening paseo — the Spanish tradition of strolling before dinner. Watch families, dogs, and ice cream cones in the fading light.",
              details: [
                '🦶 The sea at El Postiguet is great for tired legs',
                '🍦 Helados Renomar on the Explanada — best ice cream in Alicante'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'La Taberna del Gourmet',
              description: "One of Alicante's best casual dining spots — extensive tapas selection with local products. Try the local rice dishes, Valencian cheeses, and Monastrell red wine from nearby Jumilla.",
              meta: '💰 $$ · 📍 Calle San Fernando 10'
            }
          ]
        }
      ],
      mapPins: [
        { lat: 38.3490, lng: -0.4800, label: 'Parque de la Ereta (start)', num: 1, cat: 'attraction', desc: 'Tiered hillside garden — trailhead for Serra Grossa' },
        { lat: 38.3628, lng: -0.4620, label: 'Serra Grossa Ridge', num: 2, cat: 'attraction', desc: 'City\'s highest accessible ridge — 360° Mediterranean views' },
        { lat: 38.3560, lng: -0.4720, label: 'Serra Grossa Viewpoint', num: 3, cat: 'attraction', desc: 'Mid-trail viewpoint looking back over the city and bay' },
        { lat: 38.3455, lng: -0.4779, label: 'Playa El Postiguet (recovery)', num: 4, cat: 'attraction', desc: 'Cool post-hike legs in the sea' },
        { lat: 38.3436, lng: -0.4853, label: 'Explanada de España (paseo)', num: 5, cat: 'attraction', desc: 'Evening stroll on the famous palm promenade' },
        { lat: 38.3441, lng: -0.4842, label: 'La Taberna del Gourmet', num: 6, cat: 'food', desc: 'Top-tier tapas and local Monastrell wine' }
      ]
    },
    {
      num: 5,
      date: '2026-03-05',
      neighborhoods: 'Playa de San Juan · Cabo de las Huertas · Albufereta',
      title: 'The Great Beach Crawl — San Juan to Almadraba on Foot',
      description: "Today is your pure beach day. Take the tram north to Playa de San Juan — Alicante's long, spacious Blue Flag beach — and walk south along the coast, hitting Playa del Agua Amarga, Playa de la Almadraba, and the coves of Cabo de las Huertas. One long, glorious beach-hopping walk back toward the city.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Tram to Playa de San Juan',
              description: "Grab the TRAM L1 from Luceros station to Playa de San Juan — a 15-minute ride for €1.50. San Juan is a 6km-long Blue Flag beach backed by palm-tree boulevards. In March it's blissfully uncrowded.",
              details: [
                '🚃 TRAM L1, Luceros → Playa San Juan — €1.50, 15 min',
                '🏖️ 6km of sand — the widest, cleanest beach in Alicante province',
                '☕ Several beach-facing cafés open year-round at the northern end'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Beach bar at San Juan',
              description: "Tostada con tomate, café con leche, and the sound of waves. Multiple bars line the beachfront at Playa de San Juan — open early and cheap.",
              meta: '💰 $ · 📍 Paseo de la Playa de San Juan (north end)'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Walking the Coast South: San Juan → Agua Amarga → Almadraba',
              description: "Walk south along the San Juan beach for 2km, then continue around the headland to the smaller, wilder Playa del Agua Amarga — a locals' favourite with no tourists. Keep walking south and you'll reach Playa de la Almadraba, already familiar from Day 3.",
              details: [
                '🚶 Total walk: ~5km from San Juan to Almadraba',
                '🏖️ Playa del Agua Amarga: narrow, wild, uncrowded — great for a dip',
                '📸 The limestone headlands between the beaches look best from the water\'s edge',
                '💧 Stock up on water at San Juan before walking the wilder section'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'La Olla Restaurante',
              description: "Beachside restaurant at Playa de San Juan famous for paella and fideuà (noodle paella). This is the best spot to try Alicante\'s signature dish — arroz a banda — the local rice cooked in fish stock.",
              meta: '💰 $$ · 📍 Paseo de la Playa de San Juan · Book ahead for weekends'
            }
          ]
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Cabo de las Huertas Loop & Return to City',
              description: "From Almadraba, walk the rocky headland of Cabo de las Huertas one more time — the light in the afternoon is completely different from morning. Then bus back to the city center.",
              details: [
                '🌅 Late afternoon light turns the limestone cliffs golden',
                '🚌 Bus L22 from Almadraba to center (~20 min)',
                '🍺 Stop at a bar on the Explanada for cold cerveza and jamón before dinner'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: "If your legs are tired, just relax on the San Juan sand with a book and a cerveza — you\'ve already covered serious ground this trip. The beach doesn't judge." }
          ]
        }
      ],
      mapPins: [
        { lat: 38.3740, lng: -0.4245, label: 'Playa de San Juan', num: 1, cat: 'attraction', desc: 'Blue Flag beach, 6km long — tram from city, uncrowded in March' },
        { lat: 38.3658, lng: -0.4272, label: 'Playa del Agua Amarga', num: 2, cat: 'attraction', desc: 'Wild locals\' beach, no tourists, narrow and beautiful' },
        { lat: 38.3628, lng: -0.4271, label: 'Playa de la Almadraba', num: 3, cat: 'attraction', desc: 'Blue Flag beach at end of Cabo de las Huertas trail' },
        { lat: 38.3542, lng: -0.4408, label: 'Cabo de las Huertas', num: 4, cat: 'attraction', desc: 'Rocky cape with afternoon golden-hour clifftops' },
        { lat: 38.3720, lng: -0.4248, label: 'La Olla Restaurante', num: 5, cat: 'food', desc: 'Best arroz a banda and paella on San Juan beach' }
      ]
    },
    {
      num: 6,
      date: '2026-03-06',
      neighborhoods: 'MARQ · Casco Antiguo · Barrio Santa Cruz',
      title: 'Culture Day — MARQ Museum, Santa Cruz & Catedral',
      description: "Rest your legs with a culture day. Alicante's MARQ is one of Spain's best archaeology museums, the Barrio de Santa Cruz is a whitewashed hillside neighbourhood with flower-draped balconies, and the Concatedral de San Nicolás anchors the old town. A slower, richer day — perfect mid-trip breathing room.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'MARQ — Museo Arqueológico Provincial',
              description: "One of Europe's best regional archaeology museums — five permanent exhibitions covering prehistoric to modern times, with excellent interactive displays and a Phoenician shipwreck reconstruction. Allow 2–3 hours.",
              details: [
                '🏛️ Entry: €3 (budget-friendly)',
                '⏰ Open Tue–Fri 10am–7pm, Sat 10am–8:30pm, Sun 10am–2pm',
                '🔍 The Phoenician and Iberian collections are world-class',
                '📍 Next to the bullring — very central'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Barrio de Santa Cruz',
              description: "Walk up into the Barrio de Santa Cruz — the ancient Moorish quarter on the slopes below the castle. Flower-bedecked balconies, steep white steps, and tiny neighbourhood bars where the wine is cheap and the conversation is easy.",
              details: [
                '🌸 The neighbourhood is at its most photogenic in spring — flowers everywhere',
                '🏘️ Calle Labradores: the most picturesque street in Alicante',
                '🍷 Bar El Portal: dark, ancient, great for local wine by the glass'
              ]
            },
            {
              title: 'Concatedral de San Nicolás de Bari',
              description: "Alicante's cathedral is a 17th-century Baroque masterpiece with a blue tiled dome and a stunning alabaster chapel. Free to enter, takes 20 minutes, and is genuinely beautiful.",
              details: [
                '⛪ Free entry · Just behind the Plaza del Ayuntamiento',
                '🔵 The blue dome is a city landmark — great viewed from a distance too'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Mercado de San Juan street food',
              description: "Grab lunch from one of the food stalls around the Mercado Central or nearby. Croquetas, empanadas, and fresh seafood tapas for €2–4 each — the best cheap eating in the city.",
              meta: '💰 $ · 📍 Around Av. Alfonso X El Sabio'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Sunset from Castillo de Santa Bárbara (again, at dusk)',
              description: "One last sunset from the castle — but this time in the evening light with the city all lit up below. The castle is open until 10pm in summer, 8pm in winter/spring.",
              details: [
                '🌅 March sunset is around 7:15pm — the castle closes at 8pm',
                '🏰 Free entry in the evenings to the main terraces',
                '📸 The city lights coming on as the sky turns purple is the shot'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'El Portal Taberna y Wines',
              description: "A much-loved natural wine bar with tapas in the heart of the old town. Rotating menu of creative pintxos and Valencian small plates — ideal for a solo diner at the bar.",
              meta: '💰 $$ · 📍 Calle Labradores, Barrio de Santa Cruz'
            }
          ],
          tips: [
            { type: 'tip', text: "Solo dining in Spain is totally normal and celebrated. Sit at the bar, chat with the staff, and ask what they recommend. You\'ll eat better than anyone with a table." }
          ]
        }
      ],
      mapPins: [
        { lat: 38.3449, lng: -0.4868, label: 'MARQ Museum', num: 1, cat: 'attraction', desc: 'Award-winning archaeology museum — €3, interactive exhibits' },
        { lat: 38.3464, lng: -0.4826, label: 'Barrio de Santa Cruz', num: 2, cat: 'attraction', desc: 'Ancient Moorish quarter with flower-bedecked white stairs' },
        { lat: 38.3453, lng: -0.4851, label: 'Concatedral de San Nicolás', num: 3, cat: 'attraction', desc: 'Baroque cathedral with blue dome — free entry' },
        { lat: 38.3440, lng: -0.4901, label: 'Mercado Central (lunch)', num: 4, cat: 'food', desc: 'Street food stalls — croquetas, tapas, cheap and fresh' },
        { lat: 38.3482, lng: -0.4787, label: 'Castillo at Dusk', num: 5, cat: 'attraction', desc: 'Evening sunset from the castle terraces — closes 8pm' },
        { lat: 38.3464, lng: -0.4826, label: 'El Portal Taberna y Wines', num: 6, cat: 'food', desc: 'Natural wine bar with creative pintxos — perfect for solo dining' }
      ]
    },
    {
      num: 7,
      date: '2026-03-07',
      neighborhoods: 'El Postiguet · Explanada · El Barrio',
      title: 'Final Beach Morning & Farewell Tapas',
      description: "Your last full day. A slow morning at El Postiguet with nowhere to be, a proper Alicante lunch, and an evening wandering the El Barrio one final time. This is the day to buy local rice, turron sweets, and Monastrell wine to take home — and to sit on the Explanada long enough to understand why people move here.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'El Postiguet — Final Beach Morning',
              description: "Go back to where it started. El Postiguet at 9am in March is quiet, golden, and beautiful. Swim if you're brave, or just sit on the sand with a café from the nearby bar and watch the fishing boats come in.",
              details: [
                '🏖️ El Postiguet faces southeast — the morning light is beautiful',
                '🏰 Look up at the castle one last time before you leave',
                '☕ Café Puntual nearby opens at 8am — great coffee, decent tostadas'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Mercado Central & Souvenir Shopping',
              description: "Head to the Mercado Central for a final wander. Pick up local turron (the nougat Alicante is famous for), bags of saffron, and bottles of local Monastrell wine. The market is also a great place for a cheap final lunch.",
              details: [
                '🍬 Turron de Alicante — the hard almond nougat is the real thing, buy here not at the airport',
                '🍷 Monastrell is the local grape — buy a bottle of Jumilla or Alicante DO',
                '🧅 Fresh local olives, preserved lemons, and Valencian sweets to take home'
              ]
            },
            {
              title: 'Final Explanada Paseo',
              description: "One last slow walk along the Explanada — the full length, end to end, then back. This is the quintessential Alicante experience. Watch the light change on the mosaic tiles, grab a horchata or granizado from a kiosk, and let the city say goodbye.",
              details: [
                '🍹 Horchata (tiger nut milk drink) or granizado de limón — both perfect',
                '🌴 The Explanada is busiest around 6–8pm — the Spanish paseo hour',
                '📸 The tiles shimmer differently every hour — one more photo opportunity'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Final Lunch',
              name: 'Restaurante El Buen Comer',
              description: "A classic Alicante lunch spot near the Explanada — simple, unfussy, incredible. Order the local arroz con costra (a baked rice dish with egg crust, unique to Alicante) and a glass of house wine.",
              meta: '💰 $ · 📍 Calle Mayor, near Plaza Gabriel Miró'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Final Tapas Crawl — El Barrio Farewell',
              description: "End where you started — in the El Barrio. One last tapas crawl through the neighbourhood you know by now. Order a final plate of gambas, toast to the trip, and head to bed knowing you've seen Alicante the right way.",
              details: [
                '🍤 Gambas a la plancha at Nou Manolín — non-negotiable final meal',
                '🍷 Try a glass of clarete — the local rosé that\'s impossible to find outside Spain',
                '🥂 Toast to the beaches, the hike, the coves — you earned all of it'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Nou Manolín (return visit)',
              description: "You came to the best tapas counter in the city on Day 3 — return for the finale. The gambas a la plancha and local white wine is a perfect last supper in Alicante.",
              meta: '💰 $$ · 📍 Calle Villegas 3, El Barrio'
            }
          ],
          tips: [
            { type: 'tip', text: "If you liked Alicante, consider an extra day trip to Isla de Tabarca — a tiny fortified island a 45-min ferry ride from the port. Best snorkelling in the region and a village frozen in time." }
          ]
        }
      ],
      mapPins: [
        { lat: 38.3455, lng: -0.4779, label: 'El Postiguet (final morning)', num: 1, cat: 'attraction', desc: 'Last slow morning at the city beach with castle views' },
        { lat: 38.3440, lng: -0.4901, label: 'Mercado Central (shopping)', num: 2, cat: 'attraction', desc: 'Buy turron, Monastrell wine, and saffron to take home' },
        { lat: 38.3436, lng: -0.4853, label: 'Explanada de España (paseo)', num: 3, cat: 'attraction', desc: 'Final walk on the mosaic promenade — golden hour is magic' },
        { lat: 38.3439, lng: -0.4870, label: 'El Buen Comer', num: 4, cat: 'food', desc: 'Classic arroz con costra — Alicante\'s unique baked rice' },
        { lat: 38.3454, lng: -0.4836, label: 'El Barrio (farewell crawl)', num: 5, cat: 'attraction', desc: 'Final tapas crawl through the old quarter' },
        { lat: 38.3454, lng: -0.4830, label: 'Nou Manolín (farewell dinner)', num: 6, cat: 'food', desc: 'The city\'s best tapas counter — gambas a la plancha for the final night' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation (hostel/guesthouse)', budget: '$25–40/night', midrange: '$50–80/night', luxury: '$100–180/night' },
    { category: 'Meals (casual tapas)', budget: '$15–25/day', midrange: '$30–50/day', luxury: '$60–100/day' },
    { category: 'Transport (tram + bus)', budget: '$5–10/day', midrange: '$10–20/day', luxury: '$20–40/day (taxi)' },
    { category: 'Activities (mostly free)', budget: '$5–15/day', midrange: '$15–30/day', luxury: '$30–60/day' },
    { category: 'MARQ Museum', budget: '€3 (once)', midrange: '€3', luxury: '€3' },
    { category: '7-Night Total (solo)', budget: '$450–700', midrange: '$700–1,000', luxury: '$1,200–1,800' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Alicante-Elche Miguel Hernández Airport (ALC) is 12km from the city center', 'TRAM C1 line connects the airport to the city in about 20 min (€3.85)', 'Taxi to center costs €15–20'] },
    { title: '🏨 Where to Stay', items: ['Hostel Alifornia — social hostel near the Explanada, great for solo travellers', 'Pensión La Milagrosa — budget guesthouse in the old town', 'Staying near the Explanada puts everything within 20 min walk', 'Airbnbs in El Barrio are great value and walkable to everything'] },
    { title: '🌡️ Weather in March', items: ['Average highs 17–20°C (63–68°F) — jacket for mornings and evenings', 'Sunny most days with occasional rain shower', 'Sea temperature ~14°C — refreshing for a brave dip', 'Daylight until around 7:15pm'] },
    { title: '💰 Budget Tips', items: ['Follow the menú del día for lunch — €10–12 for 3 courses', 'El Barrio tapas bars are cheap and walk-in friendly', 'Most beaches, parks, and the castle entrance are free', 'Buy Mercado Central snacks for hiking days instead of restaurant meals', 'TRAM is the only transport you really need — €1.50 per trip'] },
    { title: '📱 Practical Info', items: ['Buy an eSIM at the airport for cheap data (Lebara or Lycamobile work well)', 'Most bars and restaurants have free WiFi', 'Spain uses EU standard plugs (Type C/F, 220V)', 'Alicante is very safe — normal big-city caution in El Barrio at late night'] }
  ]
};

const result = fulfillOrder(order, itineraryData);
result.then ? result.then(r => console.log('✅ Fulfilled:', JSON.stringify(r, null, 2))).catch(err => { console.error('❌ Error:', err.message); process.exit(1); }) : console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
