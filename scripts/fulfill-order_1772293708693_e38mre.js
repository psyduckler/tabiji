const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1772293708693_e38mre',
  email: 'sobel.shawn@gmail.com',
  destination: 'San Pedro de Atacama, Chile',
  startDate: '2026-03-17',
  endDate: '2026-03-20',
  groupSize: 1,
  requests: 'No rental car is preferred'
};

const itineraryData = {
  destination: 'San Pedro de Atacama, Chile',
  countryEmoji: '🇨🇱',
  title: 'Desert Solitude in the Atacama',
  subtitle: '3 nights of otherworldly landscapes, stargazing & slow desert mornings for one',
  description: "San Pedro de Atacama is the kind of place that rewires your sense of scale. Salt flats stretch to the horizon, geysers erupt at dawn in freezing mist, and the night sky is so clear it feels like you could reach up and touch the Milky Way. This solo itinerary pairs big desert adventures — Moon Valley sunsets, geyser fields at sunrise, flamingo-dotted lagoons — with the slow, restorative rhythm of a small adobe town. No car needed: everything runs on guided tours and walkable streets.",
  duration: '3 nights',
  dates: 'Mar 17 – Mar 20, 2026',
  budget: '$',
  pace: 'Moderate',
  bestFor: 'Solo Travelers',
  highlights: [
    'Sunset over Valle de la Luna\'s salt formations',
    'Sunrise at El Tatio Geysers (4,320m altitude)',
    'Floating in the salt lagoons of Laguna Cejar',
    'Stargazing under some of the clearest skies on Earth',
    'Flamingo-spotting at Laguna Chaxa in the Salar de Atacama'
  ],

  essentials: [
    { title: '🏜️ Desert Climate', text: 'March is late summer — days reach 25°C but nights drop to 5°C. The sun is intense at altitude (2,400m). Pack sunscreen SPF 50+, sunglasses, a warm fleece for early mornings, and a hat. Hydrate constantly.' },
    { title: '🚐 Getting Around', text: 'San Pedro is tiny and walkable. All major excursions (geysers, salt flats, valleys) are done via guided tours booked on Calle Caracoles — the main street. No rental car needed. Tour agencies pick you up from your hostel.' },
    { title: '💰 Budget Tips', text: 'Book tours on Calle Caracoles and haggle — agencies compete on price. Set menus (almuerzo) at local restaurants are $5–8. Supermarket snacks save money. Most tours are $25–50 per person. Hostels with shared kitchens help cut costs.' },
    { title: '⛰️ Altitude', text: 'San Pedro sits at 2,400m and some excursions go above 4,000m. Drink coca tea, avoid alcohol on day 1, and take it easy. The geyser tour at 4,320m can cause mild altitude symptoms — acclimate first.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-17',
      neighborhoods: 'San Pedro Town · Valle de la Luna',
      title: 'Arrival & Moon Valley Sunset',
      description: "Arrive in San Pedro, settle into the adobe-walled town, and ease into desert time. Wander Calle Caracoles to book your tours for the next days, then head to Valle de la Luna for one of the most spectacular sunsets on Earth — the salt formations glow pink and orange as the Andes turn violet behind them.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Arrive & Explore San Pedro Town',
              description: 'Arrive from Calama airport (shuttle, ~1.5hrs) and check into your hostel. Stroll the dusty adobe streets, browse the artisan market on the plaza, and book your tours for the next two days along Calle Caracoles — the main drag lined with agencies, restaurants, and gear shops.',
              details: [
                '✈️ Fly into Calama (CJC), then shuttle bus to San Pedro (~$15, 1.5hrs)',
                '🏨 Budget stays: Casa Voyage Hostel, Hostal Mama Tierra',
                '🛍️ Browse Calle Caracoles for tour bookings — compare 3 agencies for best price'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Late Lunch',
              name: 'La Casona',
              description: 'Casual Chilean spot on the main street with affordable set lunches (almuerzo). Hearty soups, grilled chicken, and fresh juice — perfect fuel after travel.',
              meta: '💰 $ · 📍 Calle Caracoles · Set lunch ~$6'
            }
          ],
          tips: [
            { type: 'tip', text: 'Drink coca or muña tea to acclimate to the altitude. Skip alcohol today. Buy a 5L water jug from the mini-market — you\'ll need it.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Valle de la Luna Sunset Tour',
              description: 'Join a guided tour to the Moon Valley — a surreal landscape of wind-carved salt formations, sand dunes, and caverns. Hike through the Salt Cavern, climb the Great Dune, and watch the sunset paint the entire valley in impossible colors while the Licancabur volcano glows behind.',
              details: [
                '🌅 Tours depart ~4pm and return after sunset (~8pm)',
                '💰 ~$20–30 per person including transport and guide',
                '📸 The Great Dune viewpoint at sunset is the hero shot',
                '🧥 Bring a warm layer — it gets cold fast after sunset'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Adobe Restaurant',
              description: 'Popular casual restaurant with Chilean and international dishes. The courtyard has a cozy fire pit — perfect for post-sunset warmth. Try the pastel de choclo (corn pie) or a hearty cazuela soup.',
              meta: '💰 $$ · 📍 Calle Caracoles 211'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -22.9087, lng: -68.1997, label: 'San Pedro Town Center', num: 1, cat: 'attraction', desc: 'Adobe town center with tour agencies and artisan market' },
        { lat: -22.9100, lng: -68.2010, label: 'Calle Caracoles', num: 2, cat: 'attraction', desc: 'Main street for tours, dining, and shopping' },
        { lat: -22.9292, lng: -68.2872, label: 'Valle de la Luna', num: 3, cat: 'attraction', desc: 'Surreal salt formations and sand dunes with epic sunsets' },
        { lat: -22.9400, lng: -68.2750, label: 'Great Dune Viewpoint', num: 4, cat: 'attraction', desc: 'Best sunset viewpoint over Moon Valley' },
        { lat: -22.9095, lng: -68.1985, label: 'Adobe Restaurant', num: 5, cat: 'food', desc: 'Casual Chilean dining with courtyard fire pit' }
      ]
    },
    {
      num: 2,
      date: '2026-03-18',
      neighborhoods: 'El Tatio · Machuca · Salar de Atacama',
      title: 'Geysers at Dawn & Salt Flat Flamingos',
      description: "The biggest adventure day. Wake at 4am for the El Tatio Geysers — the world's highest geyser field erupting in the freezing pre-dawn light at 4,320m. Warm up in a natural thermal pool, visit the tiny village of Machuca, then spend the afternoon at the Salar de Atacama watching flamingos feed in the turquoise lagoons.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'El Tatio Geysers Sunrise',
              description: 'Depart San Pedro at 4am and drive 90 minutes up to 4,320m. Arrive in near-freezing darkness and watch dozens of geysers erupt as the first sunlight hits — columns of steam catch the golden light against the Andean peaks. Afterward, soak in a natural thermal pool surrounded by the geyser field.',
              details: [
                '⏰ Pick-up at 4:00am — pack warm layers, gloves, hat',
                '🌡️ Temperatures can be -10°C at dawn — it warms up fast after sunrise',
                '♨️ Thermal pool break included — bring swimwear under warm clothes',
                '💰 Tour ~$35–45 including breakfast and guide',
                '⚠️ Altitude: 4,320m — take it slow, breathe deeply'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Tour Breakfast at El Tatio',
              description: 'Most tours provide a hot breakfast at the geyser field — coffee, bread, eggs, and fruit. Some agencies even cook eggs in the geyser steam.',
              meta: '💰 Included with tour · 📍 El Tatio Geyser Field'
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Machuca Village Stop',
              description: 'On the drive back, stop at the tiny Atacameño village of Machuca — a cluster of adobe houses at 4,000m with a photogenic church. Try the famous llama empanadas sold by local families.',
              details: [
                '📸 The adobe church with Andean backdrop is iconic',
                '🫓 Llama empanadas — a unique Atacama experience (~$2)',
                '🦙 Herds of llamas and alpacas graze nearby'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Laguna Chaxa — Flamingos in the Salar de Atacama',
              description: 'After resting back in town, head to Laguna Chaxa in the Salar de Atacama — Chile\'s largest salt flat. Walk the boardwalks over the crusty white salt pan and watch Andean and Chilean flamingos feeding in the shallow turquoise water with the volcanic skyline behind.',
              details: [
                '🦩 Three flamingo species live here — Andean, Chilean, and James\'s',
                '📸 Late afternoon light reflects flamingos perfectly in the water',
                '💰 Tour ~$25 or self-guided (taxi ~$20 each way)',
                '🌅 The salt flat at golden hour is surreal — endless white with pink birds'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Rest between 11am–3pm after the geyser tour. The altitude and early wake-up will catch up with you. Nap, hydrate, eat — then head out for the afternoon excursion.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Baltinache',
              description: 'Cozy restaurant on Tocopilla street serving hearty Chilean comfort food — cazuelas, empanadas, and grilled meats. Good portions, honest prices, and a warm atmosphere after a long adventure day.',
              meta: '💰 $ · 📍 Calle Tocopilla'
            }
          ],
          activities: [
            {
              title: 'Stargazing Tour',
              description: 'The Atacama Desert has some of the clearest, darkest skies on Earth — it\'s where the world\'s most powerful telescopes are built. Join a small-group stargazing tour at a local observatory and see the Milky Way, nebulae, Saturn\'s rings, and Jupiter\'s moons through professional telescopes.',
              details: [
                '🌌 Tours run 9pm–11:30pm with guide + telescopes',
                '💰 ~$30–40 per person',
                '📍 SPACE Observatory or Atacama Desert Stargazing are top-rated',
                '🧥 Bring your warmest layer — desert nights are cold'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: -22.3340, lng: -68.0130, label: 'El Tatio Geysers', num: 1, cat: 'attraction', desc: 'World\'s highest geyser field — eruptions at sunrise' },
        { lat: -22.5660, lng: -68.0040, label: 'Machuca Village', num: 2, cat: 'attraction', desc: 'Tiny adobe village with llama empanadas' },
        { lat: -23.1700, lng: -68.1800, label: 'Laguna Chaxa', num: 3, cat: 'attraction', desc: 'Flamingo lagoon in the Salar de Atacama salt flat' },
        { lat: -22.9530, lng: -68.1780, label: 'SPACE Observatory', num: 4, cat: 'attraction', desc: 'Top-rated stargazing with professional telescopes' },
        { lat: -22.9095, lng: -68.1990, label: 'Baltinache Restaurant', num: 5, cat: 'food', desc: 'Hearty Chilean comfort food at honest prices' }
      ]
    },
    {
      num: 3,
      date: '2026-03-19',
      neighborhoods: 'Laguna Cejar · Ojos del Salar · San Pedro',
      title: 'Salt Lagoons, Floating & Desert Relaxation',
      description: "Today is about slowing down and soaking in — literally. Float effortlessly in the hyper-saline Laguna Cejar, peer into the impossibly blue sinkholes of Ojos del Salar, and spend the afternoon wandering San Pedro at your own pace. This is the relaxation day — hot springs, long lunches, and watching the desert light change over the volcanoes.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Laguna Cejar & Ojos del Salar',
              description: 'Join a morning tour to Laguna Cejar — a salt lagoon so saline you float like a cork, Dead Sea-style. Then visit Ojos del Salar — two perfectly circular freshwater sinkholes of impossibly deep blue. The contrast of turquoise water against white salt and brown desert is otherworldly.',
              details: [
                '🏊 You float effortlessly — bring swimwear and a towel',
                '💧 Shower facilities available at Laguna Cejar',
                '📸 Ojos del Salar — two perfect blue "eyes" in the salt flat',
                '💰 Tour ~$30–40 per person (morning departure)',
                '⚠️ Don\'t get the water in your eyes — it stings intensely'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Free Afternoon — Wander & Recharge',
              description: 'Take the afternoon to explore San Pedro at your own pace. Visit the Museo Arqueológico R.P. Gustavo Le Paige to learn about the Atacameño culture and see 3,000-year-old artifacts. Browse artisan stalls on the plaza. Or simply sit in a café courtyard with a book and a pisco sour — you\'ve earned it.',
              details: [
                '🏛️ Museo Arqueológico — small but excellent, ~$5 entry',
                '🧉 Try a terremoto (Chilean sweet wine cocktail) at a local bar',
                '🛍️ The plaza artisan market has beautiful alpaca wool goods'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Lunch',
              name: 'Franchutería',
              description: 'A beloved French-Chilean bakery café with fresh croissants, baguettes, empanadas, and excellent coffee. The garden courtyard is a perfect solo lunch spot — quiet, sunny, and unhurried.',
              meta: '💰 $ · 📍 Calle Tocopilla 442'
            }
          ],
          tips: [
            { type: 'tip', text: 'This is your rest day by design. Tomorrow is departure day. Use the afternoon to pack, wash off desert dust, and soak in the last of the Atacama atmosphere.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Farewell Sunset from Pukará de Quitor',
              description: 'Walk or bike 3km north of town to the pre-Inca fortress of Pukará de Quitor. Climb to the mirador (viewpoint) above the ruins for a sweeping 360° panorama of the valley, the San Pedro River oasis, and the volcanoes beyond. Watch your last Atacama sunset from here.',
              details: [
                '🏛️ 12th-century fortress ruins — entry ~$5',
                '🚶 30-min walk or 10-min bike ride from town center',
                '📸 The mirador above the ruins gives the best valley panorama',
                '🌅 Face west for sunset over the Cordillera de la Sal'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Ckunna Restaurant',
              description: 'A standout restaurant celebrating Indigenous Atacameño cuisine — dishes made with quinoa, chañar fruit, rica-rica herbs, and local chili. A meaningful final meal that connects you to the land and culture of the Atacama.',
              meta: '💰 $$ · 📍 Calle Tocopilla · Reservations recommended'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -23.0600, lng: -68.2100, label: 'Laguna Cejar', num: 1, cat: 'attraction', desc: 'Hyper-saline floating lagoon — Dead Sea of the Atacama' },
        { lat: -23.0500, lng: -68.2200, label: 'Ojos del Salar', num: 2, cat: 'attraction', desc: 'Two perfectly circular blue sinkholes in the salt flat' },
        { lat: -22.9087, lng: -68.1997, label: 'Museo Arqueológico', num: 3, cat: 'attraction', desc: 'Atacameño cultural artifacts spanning 3,000 years' },
        { lat: -22.8900, lng: -68.2050, label: 'Pukará de Quitor', num: 4, cat: 'attraction', desc: 'Pre-Inca hilltop fortress with 360° valley views' },
        { lat: -22.9100, lng: -68.2000, label: 'Franchutería', num: 5, cat: 'food', desc: 'French-Chilean bakery with garden courtyard' },
        { lat: -22.9090, lng: -68.1995, label: 'Ckunna Restaurant', num: 6, cat: 'food', desc: 'Indigenous Atacameño cuisine — a meaningful farewell meal' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: '$15–30/night', midrange: '$50–100/night', luxury: '$150–400/night' },
    { category: 'Meals', budget: '$10–20/day', midrange: '$25–50/day', luxury: '$60–120/day' },
    { category: 'Transport', budget: '$0–5/day', midrange: '$10–20/day', luxury: '$50–100/day (private)' },
    { category: 'Tours', budget: '$25–45/tour', midrange: '$50–80/tour', luxury: '$100–200/tour (private)' },
    { category: 'Stargazing', budget: '$30–40', midrange: '$50–70', luxury: '$100+ (private)' },
    { category: '3-Night Total (solo)', budget: '$250–450', midrange: '$500–900', luxury: '$1,200–2,500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Calama (CJC) — closest airport, served by LATAM and SKY from Santiago', 'Shuttle bus from Calama to San Pedro takes ~1.5 hours ($12–15 USD)', 'Transfer Licancabur and Buses Atacama run frequent shuttles', 'No direct flights to San Pedro — Calama is the gateway'] },
    { title: '🏨 Where to Stay', items: ['Casa Voyage Hostel — budget-friendly with communal kitchen ($15–25/night)', 'Hostal Mama Tierra — cozy adobe rooms near the center', 'Lodge Atacama Horse — mid-range with pool and volcano views', 'Our Habitas Atacama — luxury desert retreat for splurging'] },
    { title: '🌡️ Weather (March)', items: ['Daytime: 22–27°C (72–80°F) — warm and sunny', 'Nighttime: 3–8°C (37–46°F) — pack warm layers', 'UV index extreme at 2,400m altitude — SPF 50+ mandatory', 'Occasional afternoon clouds, very rare rain'] },
    { title: '💳 Money', items: ['Chilean Pesos (CLP) are preferred — ATMs available but charge fees', 'Many tour agencies accept USD but at poor rates', 'Cards accepted at restaurants and hotels, not always at small shops', 'Budget tip: withdraw larger amounts to minimize ATM fees'] },
    { title: '📱 Connectivity', items: ['WiFi at most hostels and cafés — can be slow', 'Chilean SIM from Entel or WOM works well in town', 'Cell signal drops on remote tours (geysers, salt flats)', 'Download offline maps before excursions'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
