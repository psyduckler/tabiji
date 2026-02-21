const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771705727239_49hl89',
  email: 'psyduckler@gmail.com',
  destination: 'Franschhoek, South Africa',
  startDate: '2026-06-27',
  endDate: '2026-06-29',
  groupSize: 2,
  requests: ''
};

const itineraryData = {
  destination: 'Franschhoek, South Africa',
  countryEmoji: '🇿🇦',
  title: 'A Winter Wine Escape in Franschhoek',
  subtitle: '3 days of world-class wine, fireside dining & mountain beauty for two',
  description: "Franschhoek — the French Corner of the Cape Winelands — is South Africa's culinary and wine capital. In winter, the valley transforms: misty mornings give way to crisp blue skies, vineyards glow amber and gold, and roaring fireplaces beckon from every estate. With fewer crowds, you'll have the tasting rooms, gourmet restaurants, and mountain trails practically to yourselves. This itinerary is a love letter to slow travel: world-class wines, long lunches, and evenings wrapped in warmth.",
  duration: '2 nights',
  dates: 'Jun 27 – Jun 29, 2026',
  budget: '$$–$$$',
  pace: 'Relaxed',
  bestFor: 'Couples',
  highlights: [
    'Franschhoek Wine Tram hop-on hop-off through the valley',
    'Long lunch at La Petite Colombe — one of Africa\'s best restaurants',
    'Wine & chocolate pairing at Haute Cabrière',
    'Historic Huguenot Memorial Museum & French heritage walk',
    'Fireside wine tastings at Boschendal and Grande Provence'
  ],

  essentials: [
    { title: '🍷 Winter Wine Season', text: 'June is winter in the Cape Winelands — expect 8–18°C, crisp mornings, and occasional rain. Pack warm layers, a rain jacket, and comfortable walking shoes. The upside: smaller crowds and cozy fireside tastings.' },
    { title: '🚗 Getting Around', text: 'Franschhoek is compact — the main village is walkable, but you\'ll need a car (or Uber) to reach estates along the valley. The Wine Tram is the best way to visit multiple wineries without driving. Book in advance.' },
    { title: '🍽️ Dining Capital', text: 'Franschhoek has more award-winning restaurants per square kilometre than almost anywhere in Africa. Book dinners in advance, especially at La Petite Colombe, Foliage, and The French Connection. Winter menus feature hearty, seasonal dishes.' },
    { title: '🏔️ The Valley', text: 'Surrounded by dramatic mountain peaks, Franschhoek sits in a sheltered valley. Winter sunsets paint the mountains orange and pink. The Franschhoek Pass offers stunning views — drive it at golden hour.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-06-27',
      neighborhoods: 'Franschhoek Village · Main Road · Huguenot Quarter',
      title: 'Arrival — Village Charm & Fireside Welcome',
      description: "Arrive in Franschhoek and soak in the charm of this tiny French-influenced village. Stroll the oak-lined main road, explore the Huguenot heritage, and settle into your first evening with wine by the fire.",
      timeBlocks: [
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Franschhoek Village Walk & Huguenot Museum',
              description: 'Wander down the oak-lined Huguenot Road — the village main street — past art galleries, boutiques, and chocolatiers. Visit the Huguenot Memorial Museum to learn how French Protestant refugees shaped this valley\'s wine culture over 300 years ago.',
              details: [
                '🏛️ Huguenot Memorial Museum — R25 entry, fascinating history',
                '🗿 The Huguenot Monument is a beautiful photo spot against the mountains',
                '🍫 Stop at Huguenot Fine Chocolates for artisan truffles'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Late Lunch',
              name: 'Bread & Wine at Morgenster',
              description: 'A relaxed vineyard bistro on the edge of the village. Excellent charcuterie boards, wood-fired pizzas, and estate wines — the perfect arrival meal.',
              meta: '💰 $$ · 📍 Happy Valley Road · Cozy indoor seating with fireplace'
            }
          ],
          tips: [
            { type: 'tip', text: 'Winter days are short — sunset is around 5:45pm. Plan your afternoon walk to catch the golden light on the Huguenot Monument.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Fireside Wine Tasting at Grande Provence',
              description: 'Grande Provence Heritage Wine Estate offers elegant tastings in a beautifully restored 18th-century manor house. In winter, they light the fireplaces in the tasting room — settle in with a flight of their award-winning reds.',
              details: [
                '🍷 Try the Shiraz and the Angels Tears Bordeaux blend',
                '🖼️ The estate also has a contemporary art gallery worth browsing',
                '🔥 Ask for the fireside seating — pure romance'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'Foliage Restaurant',
              description: 'An intimate fine-dining gem on the main road. Chef Chris Erasmus creates imaginative dishes from foraged and local ingredients — think truffle risotto, slow-braised lamb, and inventive desserts. One of Franschhoek\'s most romantic tables.',
              meta: '💰 $$$$ · 📍 11 Huguenot Road · Book ahead'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -33.9133, lng: 19.1172, label: 'Huguenot Memorial Museum', num: 1, cat: 'attraction', desc: 'French Huguenot history and the beautiful monument' },
        { lat: -33.9100, lng: 19.1150, label: 'Franschhoek Village Centre', num: 2, cat: 'attraction', desc: 'Oak-lined main road with galleries, boutiques & chocolatiers' },
        { lat: -33.8950, lng: 19.1050, label: 'Grande Provence Estate', num: 3, cat: 'attraction', desc: '18th-century manor with fireside wine tastings and art gallery' },
        { lat: -33.9110, lng: 19.1165, label: 'Foliage Restaurant', num: 4, cat: 'food', desc: 'Intimate fine dining with foraged seasonal cuisine' },
        { lat: -33.9060, lng: 19.0980, label: 'Bread & Wine', num: 5, cat: 'food', desc: 'Relaxed vineyard bistro with wood-fired pizza and charcuterie' }
      ]
    },
    {
      num: 2,
      date: '2026-06-28',
      neighborhoods: 'Franschhoek Wine Valley · Estate Circuit',
      title: 'Wine Tram Day — Valley Estates & Long Lunch',
      description: "Board the famous Franschhoek Wine Tram for a full day of hopping between world-class estates. Taste wines in historic cellars, enjoy a gourmet lunch among the vines, and discover why this valley produces some of the Southern Hemisphere's finest bottles.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Franschhoek Wine Tram — Morning Stops',
              description: 'The Wine Tram departs from the village centre and winds through the valley via open-sided tram car and tram bus. Choose the Blue or Purple line for the best winter estates. Start at Rickety Bridge for elegant Semillon and Pinotage, then hop to Vrede en Lust for their superb cheese and wine pairing.',
              details: [
                '🚃 Book the Wine Tram online in advance — winetram.co.za',
                '🍷 Rickety Bridge — beautiful riverside setting, outstanding Semillon',
                '🧀 Vrede en Lust — the cheese & wine pairing is legendary',
                '⏰ First tram departs ~10am — aim for 2-3 estates per half-day'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'Winter mornings can be chilly on the open tram. Bring a scarf and warm jacket — but the estates all have cozy indoor tasting rooms.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Haute Cabrière — Wine & Chocolate Pairing',
              description: 'Haute Cabrière is famous for its MCC (Méthode Cap Classique — South African sparkling wine) and their wine-and-chocolate pairing is a must-do. The underground cellar carved into the mountainside is atmospheric and unique.',
              details: [
                '🍫 The chocolate pairing matches 4 wines with artisan chocolates',
                '🥂 Their Pierre Jourdan MCC range is world-class sparkling',
                '⛰️ The cellar is built into the mountain — incredible setting'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Long Lunch',
              name: 'La Petite Colombe',
              description: 'Set on the Leeu Estates with sweeping valley views, La Petite Colombe is consistently ranked among Africa\'s best restaurants. The winter tasting menu is extraordinary — expect seasonal Cape ingredients elevated to art. This is the meal of the trip.',
              meta: '💰 $$$$ · 📍 Leeu Estates, Dassenberg Road · Book well in advance'
            }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Boschendal Estate — Sunset & Cellar Tour',
              description: 'End the tram day at historic Boschendal — one of South Africa\'s oldest wine estates (est. 1685). The Cape Dutch manor house is stunning, and winter afternoons see beautiful light across the vineyards. Do a cellar tour if available, then taste their flagship reds by the fire.',
              details: [
                '🏡 The Cape Dutch homestead dates to 1685 — breathtaking architecture',
                '🍷 Try the Boschendal Nicolas — their premium Bordeaux blend',
                '🌄 The mountain backdrop at sunset is spectacular'
              ]
            }
          ],
          meals: [
            {
              type: '🍷 Dinner',
              name: 'The French Connection',
              description: 'Classic French bistro cooking in the heart of Franschhoek village. Coq au vin, duck confit, and an excellent South African wine list. The perfect end to a day in the vineyards.',
              meta: '💰 $$$ · 📍 48 Huguenot Road · Warm, candlelit atmosphere'
            }
          ]
        }
      ],
      mapPins: [
        { lat: -33.9080, lng: 19.1130, label: 'Wine Tram Departure', num: 1, cat: 'attraction', desc: 'Franschhoek Wine Tram village departure point' },
        { lat: -33.9200, lng: 19.0900, label: 'Rickety Bridge Winery', num: 2, cat: 'attraction', desc: 'Riverside estate famous for Semillon and Pinotage' },
        { lat: -33.8850, lng: 19.0950, label: 'Vrede en Lust', num: 3, cat: 'attraction', desc: 'Legendary cheese and wine pairing experience' },
        { lat: -33.9050, lng: 19.0750, label: 'Haute Cabrière', num: 4, cat: 'attraction', desc: 'Mountain cellar with MCC sparkling and chocolate pairing' },
        { lat: -33.9020, lng: 19.1080, label: 'La Petite Colombe', num: 5, cat: 'food', desc: 'One of Africa\'s top restaurants — valley views and tasting menu' },
        { lat: -33.8700, lng: 19.0200, label: 'Boschendal Estate', num: 6, cat: 'attraction', desc: 'Historic 1685 estate with Cape Dutch architecture and premium reds' },
        { lat: -33.9105, lng: 19.1160, label: 'The French Connection', num: 7, cat: 'food', desc: 'Classic French bistro in the village centre' }
      ]
    },
    {
      num: 3,
      date: '2026-06-29',
      neighborhoods: 'Franschhoek Pass · Mont Rochelle · Village',
      title: 'Mountain Views, Farewell Bubbles & Departure',
      description: "Your final morning is for savouring. Drive the Franschhoek Pass for jaw-dropping mountain views, enjoy a late breakfast at Mont Rochelle — Sir Richard Branson's wine estate — and toast farewell with MCC sparkling before heading home.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Franschhoek Pass Scenic Drive',
              description: 'Drive (or be driven) over the Franschhoek Pass — a winding mountain road with dramatic switchbacks and panoramic views over the entire valley. On a clear winter morning, the views are extraordinary. Stop at the summit lookout for photos.',
              details: [
                '🏔️ The pass climbs to 524m — views stretch across the whole wine valley',
                '📸 Multiple pull-over viewpoints along the route',
                '🚗 About 20 minutes each way — take it slow and enjoy'
              ]
            }
          ]
        },
        {
          label: 'Late Morning',
          activities: [
            {
              title: 'Mont Rochelle — Branson\'s Wine Estate',
              description: 'Mont Rochelle, part of Sir Richard Branson\'s Virgin Limited Edition collection, sits high on the slopes with breathtaking views. Even if you\'re not staying here, the wine tasting and restaurant are open to visitors. Their Miko range is excellent.',
              details: [
                '🍷 Try the Miko Syrah and the MCC sparkling',
                '🏔️ The terrace views over the valley are the best in Franschhoek',
                '☀️ On a clear winter day, you can see all the way to Table Mountain'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Brunch',
              name: 'Mont Rochelle Country Kitchen',
              description: 'A relaxed, elegant brunch with panoramic mountain views. Fresh pastries, eggs Benedict with local ingredients, and excellent coffee — the perfect farewell meal before departure.',
              meta: '💰 $$$ · 📍 Dassenberg Road · Terrace seating with valley views'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Last Stroll & Farewell Bubbles',
              description: 'Take one last walk through the village — pick up a bottle or two from your favourite estate to take home. Pop into Le Franschhoek Hotel for a farewell glass of MCC on their terrace, or grab artisan souvenirs from the galleries on Huguenot Road.',
              details: [
                '🛍️ Wine direct from estates is often cheaper than retail',
                '🥂 MCC (Méthode Cap Classique) is the perfect farewell toast',
                '🎨 Browse the village galleries for South African art and ceramics'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: 'If driving back to Cape Town, the N1 via Paarl is fastest (~75 min). The scenic route via Stellenbosch adds 30 minutes but passes through more beautiful wine country.' }
          ]
        }
      ],
      mapPins: [
        { lat: -33.9300, lng: 19.1100, label: 'Franschhoek Pass Lookout', num: 1, cat: 'attraction', desc: 'Dramatic mountain pass with panoramic valley views' },
        { lat: -33.9050, lng: 19.1050, label: 'Mont Rochelle Estate', num: 2, cat: 'attraction', desc: 'Branson\'s luxury estate — wine tasting with stunning views' },
        { lat: -33.9050, lng: 19.1050, label: 'Mont Rochelle Country Kitchen', num: 3, cat: 'food', desc: 'Elegant brunch with panoramic mountain views' },
        { lat: -33.9100, lng: 19.1150, label: 'Franschhoek Village', num: 4, cat: 'attraction', desc: 'Final stroll — galleries, wine shops, and farewell bubbles' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Accommodation', budget: 'R1,500–2,500/night', midrange: 'R3,000–5,000/night', luxury: 'R6,000–15,000/night' },
    { category: 'Meals (per couple)', budget: 'R400–700/day', midrange: 'R800–1,500/day', luxury: 'R2,000–4,000/day' },
    { category: 'Wine Tram', budget: 'R290pp', midrange: 'R290pp', luxury: 'R290pp + premium tastings' },
    { category: 'Wine Tastings', budget: 'R50–100/tasting', midrange: 'R100–200/tasting', luxury: 'R200–500/pairing' },
    { category: 'Transport', budget: 'R0 (walkable)', midrange: 'R500–800/day (Uber)', luxury: 'R2,000+/day (private driver)' },
    { category: '3-Day Total (couple)', budget: 'R5,000–8,000', midrange: 'R10,000–18,000', luxury: 'R25,000–50,000' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Cape Town International (CPT) is the nearest airport — 75km, ~1 hour drive', 'Rent a car at the airport for flexibility in the Winelands', 'Private transfers available from Cape Town (R1,500–2,500 each way)', 'Uber works to/from Cape Town but is less reliable between estates'] },
    { title: '🏨 Where to Stay', items: ['Leeu Estates — luxury, walking distance to La Petite Colombe', 'Mont Rochelle — Branson\'s estate, spectacular views', 'La Cabrière Country House — intimate boutique charm', 'Akademie Street Boutique Hotel — village centre, walkable'] },
    { title: '🌡️ Winter Weather', items: ['June averages 8–18°C (46–64°F) — pack warm layers', 'Rain is possible — bring a waterproof jacket', 'Mornings can be misty, afternoons often clear and sunny', 'Sunset around 5:45pm — short but golden'] },
    { title: '💳 Money', items: ['South African Rand (ZAR) — roughly R18 = $1 USD', 'Cards accepted almost everywhere', 'Tipping: 10–15% at restaurants', 'Wine tastings range R50–R250 depending on the estate'] },
    { title: '📱 Connectivity', items: ['Buy a Vodacom or MTN SIM at CPT airport for data', 'WiFi available at most estates, hotels, and restaurants', 'Cell coverage is good throughout the valley'] }
  ]
};

fulfillOrder(order, itineraryData);
