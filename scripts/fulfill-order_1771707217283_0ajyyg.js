const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771707217283_0ajyyg',
  email: 'psyduckler@gmail.com',
  destination: 'Antarctica',
  startDate: '2026-11-25',
  endDate: '2026-11-28',
  groupSize: 1,
  requests: ''
};

const itineraryData = {
  destination: 'Antarctica & Ushuaia, Argentina',
  countryEmoji: '🇦🇶',
  title: 'At the Edge of the World — Antarctica Gateway',
  subtitle: '3 days in Ushuaia: penguins, glaciers, and the last city before the ice',
  description: "Ushuaia is the last outpost of civilization before the frozen continent — the world's southernmost city, perched between the Beagle Channel and the snow-capped Martial Mountains. In November, the austral spring bursts to life: Magellanic penguins return to their colonies, glaciers gleam in 18-hour daylight, and the air smells of salt, peat, and pure adventure. This 3-day itinerary captures the raw, soul-stirring spirit of Antarctica without setting foot on the ice — hiking through sub-Antarctic wilderness, cruising past sea lion rookeries and cormorant colonies, and standing at the literal end of the road. It's expedition travel distilled to its essence.",
  duration: '3 nights',
  dates: 'Nov 25 – Nov 28, 2026',
  budget: '$$',
  pace: 'Active',
  bestFor: 'Solo Adventurers',
  highlights: [
    'Beagle Channel zodiac cruise to penguin colony at Martillo Island',
    'Train at the End of the World through Tierra del Fuego National Park',
    'Hiking to Laguna Esmeralda — turquoise glacial lake in Patagonian forest',
    'Standing at Lapataia Bay — the end of the Pan-American Highway (17,848 km from Alaska)',
    'Watching expedition ships depart for Antarctica from Ushuaia port at midnight'
  ],

  essentials: [
    { title: '🌤️ November in Ushuaia', text: 'Austral spring means long days (up to 17 hours of daylight), mild temperatures of 5–14°C, and active wildlife. Penguins arrive at Martillo Island from late October. Weather is unpredictable — pack waterproof layers, warm mid-layers, and sun protection.' },
    { title: '🚢 Getting There', text: 'Fly into Malvinas Argentinas International Airport (USH) from Buenos Aires (Aerolineas Argentinas, LATAM — about 3.5 hours). Most travelers connect through Ministro Pistarini (EZE) or Jorge Newbery (AEP). Book flights early — Ushuaia seats fill up in expedition season.' },
    { title: '🧭 Getting Around', text: 'Ushuaia city centre is walkable. Taxis and remises (private cars) are cheap and widely available. For Tierra del Fuego NP, either rent a car or take Bus Line 3 from downtown. Tour operators pick up from most hotels for excursions.' },
    { title: '🐧 Wildlife Notes', text: 'November is prime Magellanic penguin season at Martillo Island. Gentoo penguins are present year-round. Sea lions haul out at Isla de los Lobos. Bring binoculars and a telephoto lens if possible — wildlife is abundant but approaches must respect distance rules.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-11-25',
      neighborhoods: 'Ushuaia City Centre · Martial Glacier · Port',
      title: 'Arrival at the End of the World',
      description: "Touch down in Ushuaia and immediately feel the shift — the air is crisper, the mountains closer, the horizon wilder. Spend your first afternoon exploring the city at the end of the world: the historic prison-turned-museum, the colourful port where expedition ships cluster, and a chairlift ride toward the Martial Glacier with panoramic views over the Beagle Channel.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Museo del Presidio (Prison Museum)',
              description: "Ushuaia's old federal prison — once home to Argentina's most dangerous criminals — is now the most fascinating museum in town. The cells, the lighthouse, and the stories of the convicts who built this city from nothing are utterly gripping. Allow 2 hours.",
              details: [
                '🏛️ Open daily 10am–8pm · ~$10 USD entry',
                '🔦 The replica of the lighthouse inside is a highlight',
                '📜 Convicts literally built the railway that became the tourist train',
                '📍 Yaganes 256, Centro — 5-min walk from main street'
              ]
            },
            {
              title: 'Ushuaia Port Walk & Expedition Ship Spotting',
              description: "Stroll along the Muelle Turístico (tourist dock) and watch the expedition ships loading supplies for Antarctica. In November, vessels like the Scenic Eclipse, Hurtigruten ships, and Ponant yachts are all here. Reading the departure boards — 'Next stop: King George Island' — is genuinely thrilling.",
              details: [
                '⛵ Expedition ships dock right in the city centre — walk right up',
                '📸 Golden hour over the Beagle Channel and Chilean mountains is stunning',
                '🔭 Bring binoculars — you can spot cormorants and kelp geese from the dock'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Coffee',
              name: 'Café Bar Banana',
              description: 'Local institution on San Martín Street. Strong espresso, medialunas (Argentine croissants), and great people-watching.',
              meta: '💰 $ · 📍 San Martín 273, Centro'
            }
          ]
        },
        {
          label: 'Late Afternoon',
          activities: [
            {
              title: 'Aerosilla Glaciar Martial Chairlift',
              description: "Ride the chairlift up toward the Martial Glacier for bird's-eye views of the city, the Beagle Channel, and the Chilean Andes beyond. In November you may see patches of snow still clinging to the peaks. The hike up from the chairlift top to the glacier lip takes 30–40 min and rewards with raw Andean scenery.",
              details: [
                '🚡 Chairlift runs daily in good weather · ~$8 USD return',
                '🥾 Bring wind/waterproof jacket — it\'s significantly colder at altitude',
                '🌅 Best in late afternoon when the light hits the channel'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Midnight Sun Port Walk',
              description: "In late November, Ushuaia gets 17+ hours of daylight. Head down to the port around 10–11pm and watch the expedition ships prepare for departure under a sky that never truly darkens. The surreal Antarctic light gives everything a golden, dreamlike quality.",
              details: [
                '🌅 Sunset isn\'t until around 10:30pm in late November',
                '🚢 Ships often depart at night — you can watch them slip into the Beagle Channel',
                '🌊 The channel is calm and mirror-like at this hour'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Kalma Restó',
              description: 'The best king crab (centolla) in Ushuaia. Fresh local seafood in a warm, unpretentious setting right in the centre. The centolla empanadas and grilled merluza negra (Patagonian toothfish) are exceptional.',
              meta: '💰 $$ · 📍 San Martín 1253, Centro · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -54.8065, lng: -68.3029, label: 'Museo del Presidio', num: 1, cat: 'attraction', desc: 'Historic federal prison converted to fascinating museum' },
        { lat: -54.8085, lng: -68.3050, label: 'Muelle Turístico (Port)', num: 2, cat: 'attraction', desc: 'Main tourist dock — expedition ships depart for Antarctica here' },
        { lat: -54.8005, lng: -68.3295, label: 'Glaciar Martial Chairlift', num: 3, cat: 'attraction', desc: 'Chairlift to views of Beagle Channel and Andean peaks' },
        { lat: -54.8096, lng: -68.3041, label: 'Kalma Restó', num: 4, cat: 'food', desc: 'Best king crab in Ushuaia — fresh local seafood' },
        { lat: -54.8078, lng: -68.3050, label: 'Café Bar Banana', num: 5, cat: 'food', desc: 'Local institution for coffee and medialunas' }
      ]
    },
    {
      num: 2,
      date: '2026-11-26',
      neighborhoods: 'Beagle Channel · Isla de los Lobos · Martillo Island',
      title: 'The Beagle Channel — Penguins, Sea Lions & Antarctic Light',
      description: "Today is spent on the water — the same channel Charles Darwin sailed in 1832 aboard the HMS Beagle. A full-day expedition catamaran cruise takes you past sea lion rookeries, cormorant colonies, and historic lighthouses before arriving at Martillo Island, where hundreds of Magellanic and Gentoo penguins breed just metres from where you stand. This is why you came.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Beagle Channel Catamaran — Sea Lions & Cormorants',
              description: "Depart from Ushuaia port on a motorised catamaran for a full-day Beagle Channel cruise. First stop: Isla de los Lobos, home to hundreds of South American sea lions hauling out on the rocks. Then Isla de los Pájaros — literally 'Bird Island' — where imperial cormorants nest in dense colonies. The wildlife approaches within metres.",
              details: [
                '🚢 Depart ~9am from Muelle Turístico · Tour operators: Tres Marías, Canal Fun, Patagonia Adventure',
                '🦭 South American sea lions can reach 300kg — the males are enormous',
                '🐦 Imperial cormorants, kelp geese, and steamer ducks are all common',
                '💰 Full-day tour with Martillo Island landing: ~$80–120 USD'
              ]
            }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Les Eclaireurs Lighthouse',
              description: "Pass by the iconic red-and-white lighthouse at the mouth of the Beagle Channel — often called the 'Lighthouse at the End of the World' (though technically that's at Isla de los Estados). In the sparkling November light with snowy peaks behind, it looks like something from a dream.",
              details: [
                '🏮 Built 1919 by the Argentine Navy — still operational today',
                '📸 Best photo stop of the trip — bring a zoom lens',
                '🌊 The channel narrows here and the water gets intense'
              ]
            }
          ],
          meals: [
            {
              type: '🥪 Lunch',
              name: 'Onboard Picnic',
              description: 'Pack a lunch from the Mercado Central or grab provisions from La Rueda the night before. Many tours include mate and snacks. Eating centolla (king crab) empanadas while watching penguins is a peak travel experience.',
              meta: '💰 $ · 📍 Prepare the night before from Ushuaia markets'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Martillo Island Penguin Colony — Zodiac Landing',
              description: "The crown jewel of the Beagle Channel cruise: a zodiac landing on Martillo Island, home to one of the only accessible Magellanic penguin colonies in Patagonia. In November, adults are feeding chicks in burrows. Walk guided paths as penguins waddle past within arm's reach (you cannot touch them, but they have no fear of you).",
              details: [
                '🐧 ~3,000 Magellanic penguin pairs at peak season + resident Gentoo colony',
                '📸 Use telephoto if you have it — no touching, stay on marked paths',
                '⏰ About 1 hour on the island — guides explain breeding behaviour',
                '❄️ Wear waterproof boots — zodiac landings involve stepping into shallow water',
                '🎒 Tip: book the zodiac landing option, not just the sail-by tour'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍺 Drinks',
              name: 'Cervecería Beagle',
              description: 'Ushuaia\'s beloved craft brewery. Try the Beagle Stout (dark, roasty, perfect for cold evenings) or the Lager crafted with glacial water. Sit by the window and watch the channel fade to amber.',
              meta: '💰 $ · 📍 Av. Maipú 37, Centro — right on the waterfront'
            },
            {
              type: '🍽️ Dinner',
              name: 'El Almacén de Ramos Generales',
              description: 'Rustic Patagonian restaurant inside a heritage general store from the 1800s. Lamb a la parrilla (Tierra del Fuego lamb is extraordinary), locro stew, and a crackling fireplace. The most atmospheric dinner in Ushuaia.',
              meta: '💰 $$ · 📍 Av. Maipú 749, Centro'
            }
          ],
          tips: [
            { type: 'tip', text: 'Patagonian lamb raised on Tierra del Fuego is world-class. Do not skip it. The slow-roasted shoulder at El Almacén is a religious experience.' }
          ]
        }
      ],
      mapPins: [
        { lat: -54.8085, lng: -68.3050, label: 'Ushuaia Port Departure', num: 1, cat: 'attraction', desc: 'Catamaran departs from Muelle Turístico at ~9am' },
        { lat: -54.8347, lng: -68.1589, label: 'Isla de los Lobos', num: 2, cat: 'attraction', desc: 'Sea lion rookery — hundreds of massive males hauled out' },
        { lat: -54.8511, lng: -68.0972, label: 'Les Eclaireurs Lighthouse', num: 3, cat: 'attraction', desc: 'Iconic red-and-white lighthouse at the channel mouth' },
        { lat: -54.8631, lng: -68.2478, label: 'Martillo Island', num: 4, cat: 'attraction', desc: 'Magellanic & Gentoo penguin colony — zodiac landing' },
        { lat: -54.8078, lng: -68.3012, label: 'Cervecería Beagle', num: 5, cat: 'food', desc: 'Local craft brewery with glacial water lager and stouts' },
        { lat: -54.8091, lng: -68.3045, label: 'El Almacén de Ramos Generales', num: 6, cat: 'food', desc: 'Heritage general store turned Patagonian restaurant' }
      ]
    },
    {
      num: 3,
      date: '2026-11-27',
      neighborhoods: 'Tierra del Fuego National Park · Lapataia Bay · Laguna Esmeralda',
      title: 'The End of the Road — Tierra del Fuego & Emerald Lake',
      description: "Your final full day is the wildest: a morning hike to a hidden turquoise glacial lake hidden in lenga beech forest, then an afternoon in Tierra del Fuego National Park where you can stand at Lapataia Bay — the official end of the Pan-American Highway, 17,848km from Prudhoe Bay, Alaska. A ride on the Tren del Fin del Mundo (End of the World Train) through ancient peat bogs and cascading streams rounds out a day that feels genuinely remote.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Laguna Esmeralda Hike',
              description: "One of the finest hikes in Patagonia that almost nobody does. A 10km round-trip trail through lenga beech forest (glowing yellow-green in November), across peat bogs on wooden boardwalks, and up a glacial valley to an impossibly turquoise alpine lake. The colour comes from glacial silt — on a clear November day it's electric.",
              details: [
                '🥾 10km round-trip, ~3–4 hours, moderate difficulty (muddy sections)',
                '📍 Trailhead is 20km from Ushuaia — taxi or remise (~$15 USD one-way)',
                '🎒 Bring: packed lunch, waterproof boots (essential — bogs are muddy), layers, water',
                '📸 Best photography in afternoon light, but morning is quieter',
                '⚠️ Do NOT attempt without waterproof footwear — the bog sections are knee-deep in spots after rain'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Pre-Hike Breakfast',
              name: 'Café Tante Sara',
              description: 'The best bakery in Ushuaia. Fuel up on freshly baked croissants, scrambled eggs, and proper coffee before hitting the trail.',
              meta: '💰 $ · 📍 San Martín 175 — opens 7am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Tren del Fin del Mundo — End of the World Train',
              description: "Board the world's southernmost train — a narrow-gauge steam-and-diesel locomotive that recreates the route convict prisoners once walked to log the forests of Tierra del Fuego. The route winds through bog, stream, and Andean forest, with a guide narrating the area's colonial history. Ends inside the national park.",
              details: [
                '🚂 Departs from Estación del Fin del Mundo, 8km west of Ushuaia',
                '⏰ Multiple departures; the 3pm works well after a morning hike',
                '💰 ~$25 USD standard class; $40 USD first class (heated, panoramic windows)',
                '⏱️ Journey takes ~1.5 hours round-trip or drop-off inside the park'
              ]
            },
            {
              title: 'Lapataia Bay — End of the Pan-American Highway',
              description: "Stand at the most powerful spot in South America: the official end of the Pan-American Highway, marked by a simple wooden sign at Lapataia Bay. This is as far south as a road goes on earth. The bay beyond is ice-cold, glacier-blue, and utterly silent except for Andean condors overhead and the distant sound of waterfalls.",
              details: [
                '📍 Inside Tierra del Fuego National Park — entry ~$15 USD',
                '🦅 November is excellent for Andean condor sightings over the bay',
                '🌊 Lapataia Bay leads directly into the Beagle Channel',
                '🪧 The sign reads: "Ushuaia — Fin del Mundo / Inicio del Mundo" (End of the World / Beginning of the World)',
                '🚗 If you took the train to drop-off, you can walk Lapataia trails and hitch/taxi back (~$15)'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Walk Along the Waterfront',
              description: "Stroll the Av. Maipú coastal promenade as the Antarctic light turns golden. Stop at the replica of Ernest Shackleton's ship Endurance near the port, and browse Ushuaia's souvenir shops for a 'Fin del Mundo' stamp in your passport at the post office — a beloved traveller tradition.",
              details: [
                '📮 The Ushuaia post office stamps passports with a "Fin del Mundo" design — a travel rite of passage',
                '⛵ The waterfront has a replica of Shackleton\'s Endurance lifeboat',
                '🛍️ Mate gourds, Patagonian wool scarves, and penguin chocolates make great souvenirs'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Farewell Dinner',
              name: 'Kaupé Restaurant',
              description: "Ushuaia's most celebrated fine dining restaurant. Chef Ernesto Vivian is legendary for centolla (king crab) prepared five ways, and the wine list showcases Patagonian Pinot Noir and Malbec. Floor-to-ceiling windows overlook the city and channel below. Reserve ahead — it books weeks out.",
              meta: '💰 $$$ · 📍 Roca 470, Centro · Reserve in advance: +54 2901 422704'
            }
          ],
          tips: [
            { type: 'tip', text: 'Get to the post office before 5pm to get your "End of the World" passport stamp — it closes early and it\'s the best souvenir that costs nothing.' }
          ]
        }
      ],
      mapPins: [
        { lat: -54.7850, lng: -68.4082, label: 'Laguna Esmeralda Trailhead', num: 1, cat: 'attraction', desc: 'Starting point for the turquoise glacial lake hike — 10km RT' },
        { lat: -54.7752, lng: -68.4396, label: 'Laguna Esmeralda', num: 2, cat: 'attraction', desc: 'Glacial lake glowing turquoise from mineral silt — stunning' },
        { lat: -54.8187, lng: -68.5243, label: 'Estación del Fin del Mundo', num: 3, cat: 'attraction', desc: 'World\'s southernmost train station — departure point' },
        { lat: -54.8588, lng: -68.5492, label: 'Lapataia Bay', num: 4, cat: 'attraction', desc: 'End of the Pan-American Highway — 17,848km from Alaska' },
        { lat: -54.8078, lng: -68.3050, label: 'Ushuaia Post Office', num: 5, cat: 'attraction', desc: 'Get the "Fin del Mundo" passport stamp — a travel tradition' },
        { lat: -54.8069, lng: -68.3029, label: 'Kaupé Restaurant', num: 6, cat: 'food', desc: 'Best fine dining in Ushuaia — king crab and Patagonian Pinot' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$60–100/night', midrange: '$100–200/night', luxury: '$200–400/night' },
    { category: 'Meals (solo)', budget: '$20–35/day', midrange: '$40–70/day', luxury: '$80–150/day' },
    { category: 'Transport', budget: '$15–25/day', midrange: '$30–60/day', luxury: '$80–150/day (private driver)' },
    { category: 'Beagle Channel Cruise', budget: '$60 (basic)', midrange: '$90–120 (with penguin landing)', luxury: '$150–200 (private zodiac)' },
    { category: 'Tierra del Fuego Park', budget: '$15 entry + $25 train', midrange: '$60 (guided tour)', luxury: '$150 (private guide + 4WD)' },
    { category: '3-Day Total (solo)', budget: '$350–500', midrange: '$600–900', luxury: '$1,200–2,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Ushuaia (USH) from Buenos Aires — Aerolineas Argentinas and LATAM fly daily', 'About 3.5 hours from Jorge Newbery (AEP) domestic airport', 'Book early — November is expedition season and flights fill up', 'Airport is 4km from town — taxi costs ~$8 USD'] },
    { title: '🏨 Where to Stay', items: ['Hotel Tierra de Leyendas — boutique hotel with mountain views and homemade breakfast ($$)', 'Los Cauquenes Resort — 5km from town, on the Beagle Channel, spectacular views ($$$)', 'La Casa de Tere — small B&B, warm and local ($)', 'Stay on or near Av. Maipú for best waterfront access'] },
    { title: '🌡️ November Weather', items: ['Temperature: 5–14°C (41–57°F) — feels colder with wind chill', 'Expect wind, rain, sun, and snow within the same day (classic Patagonia)', 'Pack: waterproof jacket, fleece mid-layer, waterproof hiking boots, wool hat', 'Weather clears fast — if it\'s raining in the morning, wait it out'] },
    { title: '💳 Money & Logistics', items: ['Argentina uses ARS (pesos) but USD cash is king for tours and tips', 'Blue dollar rate: carry USD bills (especially $100) for 2–3x better exchange rate', 'ATMs are limited — bring enough USD cash', 'Tipping: 10–15% in restaurants, $5–10 USD for guides'] },
    { title: '📱 Connectivity', items: ['Buy a SIM at the airport or downtown — Personal and Claro have best coverage', 'WiFi is reliable at most accommodations', 'Note: cell signal disappears in Tierra del Fuego National Park — download offline maps'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
