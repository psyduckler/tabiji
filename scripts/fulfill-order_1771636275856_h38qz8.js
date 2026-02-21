const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1771636275856_h38qz8',
  email: 'psyduckler@gmail.com',
  destination: 'Trinidad',
  start_date: '2026-05-22',
  end_date: '2026-05-25',
  group_size: '1',
  travel_style: 'Cultural, Foodie, Family-friendly',
};

const itineraryData = {
  destination: 'Trinidad',
  countryEmoji: '🇹🇹',
  title: 'Trinidad: Rhythms, Rum & Real Caribbean Culture',
  subtitle: '4 days of steelpan, street food, scarlet ibis & lush rainforest',
  description: "Trinidad isn't the postcard Caribbean — it's better. The most culturally rich island in the region, birthplace of steelpan and soca, Trinidad pulses with music, street food, and biodiversity. This itinerary skips the tourist traps and goes deep: morning roti in Port of Spain, sunsets at Maracas Bay, a boat glide through the Caroni Swamp at dusk watching scarlet ibis flock home by the thousands, and a dawn birdwatching session in the rainforest canopy. Trinidadian food alone is worth the trip.",
  duration: '3 nights',
  dates: 'May 22 – May 25, 2026',
  budget: '$–$$',
  pace: 'Relaxed',
  bestFor: 'Solo, Cultural, Foodie',
  highlights: [
    'Scarlet ibis at sunset — Caroni Swamp boat tour',
    'Doubles breakfast at a roadside stall in Port of Spain',
    'Bake and shark at Maracas Bay (Richard\'s)',
    'The Magnificent Seven mansions & Queen\'s Park Savannah',
    'Steelpan yard visit — hear the original instrument being played',
    'Asa Wright Nature Centre — 400+ bird species in the rainforest',
  ],

  essentials: [
    { title: '☀️ May Weather', text: 'May is the start of rainy season, but showers tend to be short afternoon bursts. Mornings are typically clear and warm (28–32°C / 82–90°F). Bring a light rain jacket and embrace the lush green landscape.' },
    { title: '🚗 Getting Around', text: "Port of Spain is small enough to walk, but you'll need a car or maxi-taxi for day trips. Renting a car is highly recommended — it gives you freedom for Maracas Bay and the Northern Range. Maxi-taxis (shared minibuses) run fixed routes cheaply." },
    { title: '💵 Currency & Costs', text: "The TT dollar (TTD) is the local currency. 1 USD ≈ 6.75 TTD. Street food is incredibly cheap (doubles are $1–2 TTD each). You can eat brilliantly for under $10 USD/day at street level. ATMs are widely available in Port of Spain." },
    { title: '🎵 Lime & Liming', text: "'Liming' is the national pastime — hanging out, talking, eating, drinking, with nowhere to be. Embrace it. Trinidadians are famously warm and welcoming. Don't rush. The best moments happen when you slow down and lime." },
  ],

  days: [
    {
      num: 1,
      date: '2026-05-22',
      neighborhoods: 'Port of Spain · Woodbrook · Newtown',
      title: 'Arrival & Port of Spain Orientation',
      description: "Touch down in Port of Spain and dive straight into Trinidadian culture. The afternoon belongs to the grand Queen's Park Savannah and the legendary Magnificent Seven mansions. Evening on Ariapita Avenue — Port of Spain's most vibrant food and bar strip.",
      timeBlocks: [
        {
          label: 'Morning/Afternoon',
          activities: [
            {
              title: 'Check In & Breakfast Doubles',
              description: "Get your bearings and then fuel up the Trinidadian way — doubles. This is THE street food of Trinidad: two fried bara flatbreads loaded with curried channa (chickpeas), pepper sauce, and chutneys. It's cheap, delicious, and deeply cultural.",
              details: [
                '🍛 Doubles cost around $1–3 USD each — order two (or five)',
                '🌶️ Tell the vendor how much pepper you want: "slight," "moderate," or "full"',
                '📍 Grab doubles from any corner vendor near Port of Spain — it\'s everywhere in the morning',
              ]
            },
            {
              title: "Queen's Park Savannah Walk",
              description: "The Savannah is Port of Spain's giant green heart — 260 acres of open parkland ringed by grand old trees. In the afternoon it fills with joggers, food vendors, coconut water carts, and lime-rs. Walk the 3.5km perimeter loop and soak it all in.",
              details: [
                '🥥 Stop for a fresh coconut water from a roadside vendor — hugely refreshing',
                '🌳 The Savannah is one of the largest urban parks in the Caribbean',
                '⚽ You\'ll see cricket, football, and general liming happening simultaneously',
              ]
            },
          ],
          tips: [
            { type: 'tip', text: "Security note: Port of Spain is best explored during daylight hours. Stick to busy areas and leave valuables at your hotel. The Savannah, Woodbrook, and Ariapita Avenue are all safe and tourist-friendly." }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'The Magnificent Seven',
              description: "Along the western edge of the Savannah stand seven ornate historic mansions from the early 20th century, each built in a wildly different architectural style — French Baroque, Moorish, Scottish Baronial. It's a jaw-dropping streetscape. Stollmeyer's Castle and Queen's Royal College are the most photogenic.",
              details: [
                '🏛️ Stollmeyer\'s Castle — Scottish Baronial style, built 1904, looks like a fairy tale',
                '🏫 Queen\'s Royal College — German Renaissance style, now one of TT\'s top secondary schools',
                '📸 Best photo spot: stand on the Savannah side looking across at the full row of mansions',
              ]
            },
            {
              title: 'National Museum & Art Gallery',
              description: "A compact but excellent museum covering Trinidad's history — from indigenous Amerindian artifacts to colonial plantation life, Carnival culture, and independence. The Carnival section alone is worth an hour: costumes, history, and the story of how T&T gave the world steelpan.",
              details: [
                '🎨 Free admission · Open Tue–Sat 10am–6pm, Sun 2–6pm',
                '🥁 Steelpan exhibit covers the full origin story of this remarkable instrument',
                '📍 117 Frederick Street, Port of Spain — 5-min walk from the Savannah',
              ]
            },
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'All Stars Pan Yard — Steelpan Experience',
              description: "Before dinner, visit one of Port of Spain's historic steelpan yards. The All Stars Steel Orchestra on Duke Street is one of the oldest and most storied. If they're practicing (especially in carnival season build-up), you can hear the bands rehearsing — a truly unique, spine-tingling experience.",
              details: [
                '🥁 All Stars Pan Yard, Duke Street — one of the most legendary steelband yards',
                '📞 Call ahead or ask your hotel to confirm practice schedule',
                '💡 Even outside practice nights, the yard gives great context and photo ops',
              ]
            },
          ],
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Ariapita Avenue Food Crawl',
              description: "Ariapita Avenue in Woodbrook is Port of Spain's most famous food and nightlife strip. For a solo foodie night, do a crawl: hit the street food stalls for shark and bake or corn soup, then stop into a local bar for a Carib beer or rum punch. The avenue comes alive after 7pm.",
              meta: '💰 $ · 📍 Ariapita Avenue, Woodbrook · Best after 7pm',
            }
          ]
        }
      ],
      mapPins: [
        { lat: 10.6590, lng: -61.5190, label: "Queen's Park Savannah", num: 1, cat: 'attraction', desc: "Port of Spain's iconic 260-acre park — walking, vendors, cricket" },
        { lat: 10.6618, lng: -61.5199, label: 'The Magnificent Seven', num: 2, cat: 'attraction', desc: 'Row of ornate early-20th-century mansions along the Savannah' },
        { lat: 10.6502, lng: -61.5158, label: 'National Museum & Art Gallery', num: 3, cat: 'attraction', desc: 'TT history, Carnival culture, and steelpan origins — free entry' },
        { lat: 10.6480, lng: -61.5120, label: 'All Stars Pan Yard', num: 4, cat: 'attraction', desc: 'Historic steelpan yard on Duke Street — may catch rehearsals' },
        { lat: 10.6566, lng: -61.5299, label: 'Ariapita Avenue', num: 5, cat: 'food', desc: "Port of Spain's premier food and bar street — evening crawl" },
      ]
    },
    {
      num: 2,
      date: '2026-05-23',
      neighborhoods: 'Northern Range · Maracas Bay · Blanchisseuse Road',
      title: 'Maracas Bay — Beaches, Rainforest & Bake and Shark',
      description: "The drive to Maracas Bay over the Northern Range is one of the most spectacular in the Caribbean — winding rainforest roads with stunning valley views. At the end: Trinidad's most famous beach and the best bake and shark you'll ever eat.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Northern Range Scenic Drive',
              description: "The road from Port of Spain to Maracas Bay crosses the Northern Range through dense tropical rainforest. The viewpoints along the way are incredible — pull over at the first major lookout for a panoramic view over Port of Spain, the Gulf of Paria, and on clear days, Venezuela.",
              details: [
                '🚗 About 45 minutes from Port of Spain — rent a car or hire a driver',
                '🏔️ The summit viewpoint (Lookout) gives 360° views of ocean and rainforest',
                '🌿 Bamboo Cathedral on the way: a magical tunnel of towering bamboo lining the road',
              ]
            },
          ],
          tips: [
            { type: 'tip', text: "Leave by 8am to beat crowds at Maracas Bay. The beach fills up on weekends. Weekdays in May are much quieter — you may nearly have it to yourself." }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: "Maracas Bay Beach",
              description: "Trinidad's most famous beach — a long arc of golden sand backed by forested hills, with good waves for bodysurfing. The water is warm and inviting. Sling your towel under a palapa and spend a few hours doing absolutely nothing.",
              details: [
                '🏖️ The beach is about 1.5km long — quieter at the far ends',
                '🌊 Waves are gentle enough for swimming, enough for bodysurfing',
                '🎵 Soca music drifts from the beach bars — this is the quintessential TT beach vibe',
              ]
            },
          ],
          meals: [
            {
              type: '🐟 Lunch',
              name: "Richard's Bake and Shark",
              description: "THE pilgrimage of Trinidad food. Richard's is the most famous bake and shark stall in the country — fried shark fillet stuffed into a pillowy fried bake (bread), loaded with your choice of toppings: shadow beni (culantro), tamarind sauce, pepper sauce, coleslaw, pineapple, garlic. It's extraordinary.",
              meta: '💰 $ · 📍 Maracas Beach entrance · Get there before noon for shortest queue',
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Las Cuevas Bay (Optional Extension)',
              description: "If you have energy and a car, continue east along the coast to Las Cuevas Bay — a smaller, quieter beach that locals prefer. The drive hugs the dramatic coastline with gorgeous ocean views. Excellent snorkelling around the rocks.",
              details: [
                '🚗 About 20 min east of Maracas Bay',
                '🤿 The rocky headlands have good snorkelling and tidepools',
                '🥤 Grab a coconut water from a beach vendor before heading back',
              ]
            },
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Breakfast Shed / Rituals',
              description: "Back in Port of Spain, the Breakfast Shed near the waterfront is a local institution serving traditional Trinidadian food all day. Try pelau (one-pot rice with pigeon peas and chicken), callaloo soup, or fried bodi (long beans). Simple, cheap, and deeply authentic.",
              meta: '💰 $ · 📍 Wrightson Road waterfront, Port of Spain · Open from early morning',
            }
          ],
          tips: [
            { type: 'tip', text: "For a proper lime after dinner, head back to Ariapita Avenue for a rum punch. Angostura rum is made in Trinidad — try it with local bitters and fresh lime." }
          ]
        }
      ],
      mapPins: [
        { lat: 10.6972, lng: -61.4889, label: 'Bamboo Cathedral', num: 1, cat: 'attraction', desc: 'Stunning bamboo canopy tunnel on the Northern Range road' },
        { lat: 10.7100, lng: -61.4700, label: 'Northern Range Lookout', num: 2, cat: 'attraction', desc: 'Panoramic views of Port of Spain, Gulf of Paria, and Venezuela' },
        { lat: 10.7379, lng: -61.4059, label: 'Maracas Bay', num: 3, cat: 'attraction', desc: "Trinidad's most famous beach — golden sand, warm waves" },
        { lat: 10.7379, lng: -61.4062, label: "Richard's Bake and Shark", num: 4, cat: 'food', desc: "Legendary Trinidadian street food — fried shark in a bake" },
        { lat: 10.7450, lng: -61.3720, label: 'Las Cuevas Bay', num: 5, cat: 'attraction', desc: 'Quieter, local favourite beach with snorkelling' },
        { lat: 10.6480, lng: -61.5060, label: 'Breakfast Shed', num: 6, cat: 'food', desc: 'Local favourite for traditional Trinidadian home cooking' },
      ]
    },
    {
      num: 3,
      date: '2026-05-24',
      neighborhoods: 'Downtown Port of Spain · Caroni Swamp · Waterfront',
      title: 'Red House, Woodford Square & Scarlet Ibis at Sunset',
      description: "A morning of downtown culture — the parliamentary Red House, Woodford Square's 'University of Woodford Square,' and colonial-era architecture. Then the afternoon builds to one of the Caribbean's most spectacular wildlife moments: thousands of scarlet ibis returning to roost in the Caroni Swamp at sunset.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Downtown Port of Spain Walk',
              description: "Explore the historic downtown core. Woodford Square is the political and philosophical heart of Port of Spain — a lush public square where Eric Williams famously gave his \"University of Woodford Square\" political speeches that shaped independence. The Red House (parliament building) on the western side is one of the most striking colonial buildings in the Caribbean.",
              details: [
                '🏛️ Red House — Trinidadian Parliament, stunning Baroque Revival architecture built 1907',
                '🌳 Woodford Square — shaded, beautiful, with an obelisk and historic plaques',
                '📚 The square was the birthplace of Trinidad\'s independence movement — a deeply significant spot',
                '⛪ Holy Trinity Cathedral — imposing Gothic cathedral just south of the square',
              ]
            },
            {
              title: "Frederick Street & City Market",
              description: "Wander up Frederick Street — Port of Spain's main commercial artery. Dodge the traffic and absorb the city's energy. Duck into City Gate and the Central Market for spices, local produce, and street snacks.",
              details: [
                '🌶️ City Market on Charlotte Street — pick up shadow beni seeds, dried peppers, local spices',
                '🛍️ Frederick Street has everything from local fabric shops to modern retail',
                '🥤 Try a cold mauby (a bitter-sweet bark drink) from a street vendor',
              ]
            },
          ],
          meals: [
            {
              type: '🍛 Lunch',
              name: 'Roti from a Local Shop',
              description: "Roti is the other great Trinidadian staple — a large flatbread wrapper filled with curried vegetables, chicken, goat, or beef. Find a local roti shop for the real deal: Patraj Roti Shop or any 'roti shop' sign you see. Cheap, filling, and extraordinary.",
              meta: '💰 $ · 📍 Look for roti shops on Charlotte Street or Henry Street, downtown',
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Royal Botanic Gardens & Emperor Valley Zoo',
              description: "Next to the Savannah, the Royal Botanic Gardens are lush and lovely — some of the oldest in the western hemisphere, established in 1818. The adjacent Emperor Valley Zoo is small but well-regarded, with Trinidad's native wildlife including red howler monkeys, ocelots, and the beautiful red-and-blue macaw.",
              details: [
                '🌺 Botanic Gardens — free entry, great shade, rare tropical plants',
                '🐒 Emperor Valley Zoo — small admission fee, Trinidad native species',
                '🦜 The zoo has excellent examples of native parrots and macaws',
              ]
            },
          ],
        },
        {
          label: 'Late Afternoon/Sunset',
          activities: [
            {
              title: 'Caroni Swamp Boat Tour — Scarlet Ibis Sunset',
              description: "This is the unmissable Trinidad experience. The Caroni Bird Sanctuary is a 12,000-acre swamp where Trinidad's national bird — the brilliant scarlet ibis — roosts every evening. Board a flat-bottomed boat around 4pm and glide through mangrove channels as the light fades. Then: the sky fills with thousands of scarlet ibis, flocking in from their feeding grounds, landing en masse in the mangrove trees until the trees themselves appear to catch fire. Absolutely magnificent.",
              details: [
                '🚤 Tours depart around 4–4:30pm, return at dusk (~7pm)',
                '🦩 Scarlet ibis get their colour from the shrimp they eat — the red deepens with age',
                '📸 Bring a telephoto lens or zoom camera — the birds land far away on the mangroves',
                '🦟 Bring insect repellent — the swamp has mosquitoes at dusk',
                '📍 About 20 min south of Port of Spain — hire David Ramsahai (popular local guide) or book through your hotel',
              ]
            },
          ],
          tips: [
            { type: 'tip', text: "Book the Caroni tour in advance — it's the #1 attraction in Trinidad and good guides fill up quickly. Winston Nanan is the original and most famous guide; David Ramsahai is also excellent." }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🍽️ Dinner',
              name: 'Doubles Den or Chaud',
              description: "After the swamp tour, you've earned a great meal. For authentic street food, Doubles Den on Ariapita Avenue is beloved. For a sit-down experience, Chaud Restaurant on Ariapita Ave is one of Port of Spain's best — upscale Creole cuisine with excellent cocktails.",
              meta: '💰 $/$$$ · 📍 Ariapita Avenue, Woodbrook',
            }
          ]
        }
      ],
      mapPins: [
        { lat: 10.6469, lng: -61.5115, label: 'Red House (Parliament)', num: 1, cat: 'attraction', desc: "Trinidad's Baroque-Revival parliament building, built 1907" },
        { lat: 10.6471, lng: -61.5108, label: 'Woodford Square', num: 2, cat: 'attraction', desc: "The 'University of Woodford Square' — birthplace of independence" },
        { lat: 10.6622, lng: -61.5188, label: 'Royal Botanic Gardens', num: 3, cat: 'attraction', desc: 'Lush gardens established 1818 — one of the oldest in the Caribbean' },
        { lat: 10.6640, lng: -61.5196, label: 'Emperor Valley Zoo', num: 4, cat: 'attraction', desc: 'Native wildlife including howler monkeys, ocelots, and macaws' },
        { lat: 10.5833, lng: -61.3944, label: 'Caroni Bird Sanctuary', num: 5, cat: 'attraction', desc: 'Sunset boat tour to see thousands of scarlet ibis return to roost' },
        { lat: 10.6566, lng: -61.5299, label: 'Ariapita Avenue Dining', num: 6, cat: 'food', desc: 'Doubles Den & Chaud — the best of Port of Spain dining' },
      ]
    },
    {
      num: 4,
      date: '2026-05-25',
      neighborhoods: 'Arima · Northern Range · Port of Spain',
      title: 'Asa Wright Nature Centre & Farewell Lime',
      description: "Trinidad is one of the top birdwatching destinations on the planet — 471 species recorded. Your final morning at the legendary Asa Wright Nature Centre in the rainforest is a fitting farewell: sit on the veranda with coffee and watch toucans, hummingbirds, and 50+ other species come to the feeders. Then back to Port of Spain for one last doubles before you go.",
      timeBlocks: [
        {
          label: 'Early Morning',
          activities: [
            {
              title: 'Asa Wright Nature Centre',
              description: "High in the forested Northern Range, Asa Wright is a world-famous eco-lodge and nature reserve open for day visits. The centre's veranda is legendary: sit with coffee and watch an extraordinary parade of tropical birds at the feeders — channel-billed toucans, blue-crowned motmots, hummingbirds, tanagers, and if you're lucky, the bizarre oilbird. Guided trail walks into the forest reveal even more.",
              details: [
                '🦜 471 bird species recorded on Trinidad — more than all of North America combined',
                '☕ The veranda coffee-and-birdwatch experience is world-famous — truly magical',
                '🥾 Guided trail walks are available: the Oilbird cave trail is unforgettable',
                '💡 Day visitor fee is around $20–25 USD — worth every cent',
                '⏰ Open 7:30am–5pm — arrive early for best birding activity',
                '🚗 About 1.5 hours from Port of Spain via the Arima-Blanchisseuse Road',
              ]
            },
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Asa Wright Veranda Breakfast',
              description: "Asa Wright serves breakfast for day visitors (request in advance). Eat on the veranda with toucans landing metres away. It's one of those travel experiences you'll talk about for years.",
              meta: '💰 $ · 📍 Spring Hill Estate, Arima · Reserve breakfast when you book your day visit',
            }
          ],
          tips: [
            { type: 'tip', text: "Don't forget binoculars! Even a cheap pair transforms the Asa Wright experience. If you don't have any, check if your hotel can lend you a pair or ask the centre — they sometimes have loaners." }
          ]
        },
        {
          label: 'Midday',
          activities: [
            {
              title: 'Return via Arima & Final Port of Spain Lime',
              description: "Wind back down the mountain through the rainforest road to Arima — a charming market town where you can stop for one last taste of real Trinidad. Then back to Port of Spain for airport prep.",
              details: [
                '🛍️ Arima market has fresh local fruits, vegetables, and hot pepper sauce to bring home',
                '🌶️ Buy a bottle of Chief brand pepper sauce or homemade hot sauce — an essential souvenir',
                '🚗 Port of Spain airport (Piarco International) is about 30 min east of Port of Spain',
              ]
            },
          ],
          meals: [
            {
              type: '🍛 Final Meal',
              name: 'One Last Doubles',
              description: "Before you leave, grab one final doubles from a Port of Spain street vendor. It's the perfect final act — two bara, full pepper, a little shadow beni, and a smile. That's Trinidad.",
              meta: '💰 $ · 📍 Any street corner in Port of Spain, morning to noon',
            }
          ]
        }
      ],
      mapPins: [
        { lat: 10.7083, lng: -61.2706, label: 'Asa Wright Nature Centre', num: 1, cat: 'attraction', desc: 'World-famous birdwatching lodge — 471+ species, legendary veranda' },
        { lat: 10.6953, lng: -61.2844, label: 'Arima Market Town', num: 2, cat: 'attraction', desc: 'Charming market town with local produce, spices, and pepper sauce' },
        { lat: 10.5960, lng: -61.3370, label: 'Piarco International Airport', num: 3, cat: 'attraction', desc: 'Trinidad\'s main airport — 30 min east of Port of Spain' },
        { lat: 10.6590, lng: -61.5190, label: "Final Doubles — Queen's Park Area", num: 4, cat: 'food', desc: 'Last doubles before departure — the definitive Trinidadian farewell' },
      ]
    },
  ],

  budgetTable: [
    { category: 'Accommodation (Port of Spain)', budget: '$60–100/night', midrange: '$100–180/night', luxury: '$180–350/night' },
    { category: 'Meals', budget: '$10–20/day (street food)', midrange: '$30–60/day', luxury: '$80–150/day' },
    { category: 'Car Rental', budget: '$40–60/day', midrange: '$60–100/day', luxury: '$100–200/day' },
    { category: 'Caroni Swamp Tour', budget: '$25–40pp', midrange: '$25–40pp', luxury: '$25–40pp' },
    { category: 'Asa Wright Day Visit', budget: '$20–25pp', midrange: '$20–25pp', luxury: '$20–25pp' },
    { category: '4-Day Total (solo)', budget: '$300–500', midrange: '$500–900', luxury: '$900–1,500' },
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Piarco International Airport (POS) serves Trinidad', 'Major airlines from Miami, New York, Toronto, London, and Caribbean hubs', 'Airport is about 30km east of Port of Spain — 30–45 min by taxi', 'Taxi fare from airport to Port of Spain: ~$25–35 USD'] },
    { title: '🏨 Where to Stay', items: ['Hyatt Regency Port of Spain — waterfront luxury, great pool ($180–250/night)', 'Forty Winks Inn — boutique B&B in Woodbrook, near Ariapita Ave ($80–120/night)', 'Normandie Hotel — classic, colonial-style, Newtown ($100–150/night)', 'Stay in Woodbrook/Newtown for easy Ariapita Avenue access'] },
    { title: '🌡️ May Weather', items: ['Wet season begins in May — short afternoon rain showers', 'Mornings are typically clear and very hot (28–32°C / 82–90°F)', 'Humidity is high — breathable, light clothing is essential', 'Rain usually passes quickly; carry a packable rain jacket'] },
    { title: '🍽️ Must-Eat List', items: ['Doubles (breakfast staple — bara + curried channa)', 'Bake and Shark (beach lunch at Maracas)', 'Roti (curried filling wrapped in dhalpuri)', 'Pelau (one-pot rice and pigeon peas)', 'Corn soup (thick, sweet, street food classic)', 'Callaloo (dasheen leaf soup — national dish)', 'Rum punch with Angostura rum'] },
    { title: '📱 Connectivity', items: ['Buy a local SIM at the airport — Digicel or bmobile', 'Data plans are cheap and coverage is good across the island', 'Free WiFi at most hotels and many restaurants', 'Airtime (prepaid top-up) is sold at gas stations and convenience stores'] },
    { title: '🦟 Health & Safety', items: ['Bring mosquito repellent — especially for Caroni Swamp visit', 'Tap water is generally safe in Port of Spain', 'Standard Caribbean travel insurance recommended', 'Be street-smart in downtown Port of Spain at night — stay in busy areas'] },
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Order fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
