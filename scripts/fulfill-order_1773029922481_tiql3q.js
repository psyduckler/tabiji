const fulfillOrder = require('../functions/fulfill-order');

const order = {
  id: 'order_1773029922481_tiql3q',
  email: 'joshua.drueck@gmail.com',
  destination: 'Playa del Carmen, Quintana Roo, Mexico',
  startDate: '2026-03-18',
  endDate: '2026-03-20',
  groupSize: '3-4',
  requests: 'We have a 7 year old and a 4 year old. Hotel is already sorted: abbasuites.'
};

const itineraryData = {
  destination: 'Playa del Carmen, Mexico',
  countryEmoji: '🇲🇽',
  title: 'A Family Caribbean Escape in Playa del Carmen',
  subtitle: '3 days of beaches, cenotes & tacos with the kids',
  description: "Playa del Carmen is the perfect family destination — turquoise Caribbean waters, magical underground cenotes, and the friendliest taco joints you'll ever find. This itinerary is designed for families with young kids, balancing exciting adventures (swimming in cenotes! spotting sea turtles! exploring Mayan ruins!) with plenty of downtime for pool splashing and paleta breaks. The pace is relaxed, the vibe is casual, and every meal is kid-approved.",
  duration: '3 days',
  dates: 'Mar 18 – Mar 20, 2026',
  budget: '$$',
  pace: 'Relaxed',
  bestFor: 'Families with Kids',
  highlights: [
    'Swimming in crystal-clear cenotes with the kids',
    'Beach day on the Caribbean with soft white sand',
    'Xcaret eco-park — underground rivers, butterflies & Mayan culture',
    'Strolling 5th Avenue for ice cream, souvenirs & street performers',
    'Casual taco feasts at Playa\'s best local spots'
  ],

  essentials: [
    { title: '☀️ Sun Protection', text: 'The Riviera Maya sun is intense, especially for little ones. Bring reef-safe SPF 50+ sunscreen (regular sunscreen is banned at cenotes and eco-parks), rash guards for the kids, and wide-brim hats. Reapply every 2 hours — seriously.' },
    { title: '👟 Water Shoes', text: 'Bring water shoes for the whole family. Cenotes have rocky entries, some beaches have coral, and eco-parks involve lots of walking on wet surfaces. Keens or Natives work great for kids.' },
    { title: '🚕 Getting Around', text: 'Taxis are plentiful and affordable in Playa. From Abba Suites to most cenotes is 15-30 min by car. Colectivos (shared vans) run along Highway 307 for cheap transport to nearby attractions. For Xcaret, the park offers shuttle service from Playa.' },
    { title: '💧 Stay Hydrated', text: 'Carry water bottles everywhere — the heat and humidity sneak up on you. Buy big jugs of purified water at OXXO convenience stores. The kids will need frequent water and shade breaks, especially after swimming.' },
    { title: '🦟 Bug Spray', text: 'Mosquitoes come out at dusk, especially near cenotes and the jungle. Bring kid-safe insect repellent. Most restaurants have fans that keep bugs away, but evening beach walks benefit from a quick spray.' }
  ],

  days: [
    {
      num: 1,
      date: '2026-03-18',
      neighborhoods: 'Playa del Carmen Beach · 5th Avenue · Downtown',
      title: 'Beach Day & Exploring 5th Avenue',
      description: "Ease into vacation mode with a morning on Playa del Carmen's gorgeous Caribbean beach, just steps from your hotel. Let the kids splash in the calm, shallow turquoise water while you soak up the sun. Spend the afternoon exploring 5th Avenue — the pedestrian-only street packed with ice cream shops, street performers, and souvenir stores that kids love.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Beach Morning at Playa Mamitas',
              description: "Abba Suites is just 200 meters from the beach, so grab towels and head out for a relaxed morning on the sand. Playa Mamitas has calm, shallow water that's perfect for young kids to wade and splash. The sand is soft and white, and the water is that stunning Caribbean turquoise you came for.",
              details: [
                '🏖️ Arrive early (before 10am) to claim a good spot with shade',
                '🌊 The water is calm and shallow near shore — great for a 4-year-old',
                '🐚 Look for seashells along the waterline with the kids',
                '🧴 Apply reef-safe sunscreen before leaving the hotel — it\'s required on beaches here'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Chez Celine',
              description: 'A beloved French bakery and café on 5th Avenue. Amazing croissants, fresh fruit bowls, scrambled eggs, and freshly squeezed juices. Kids love the chocolate croissants and crêpes.',
              meta: '💰 $$ · 📍 5th Ave between Calle 34 & 36 · Opens 7am'
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Pool Time at Abba Suites',
              description: "Head back to the hotel for a midday break. Abba Suites has a rooftop infinity pool — perfect for the kids to cool off while you relax with a drink. This is important downtime for young kids who need a break from the sun and stimulation.",
              details: [
                '🏊 The pool is a great reset between morning beach and evening adventures',
                '😴 Let the 4-year-old nap if they need it — vacation pace, not race pace',
                '🧊 Grab paletas (Mexican popsicles) from a nearby shop on 5th Ave'
              ]
            },
            {
              title: '5th Avenue Exploration',
              description: "Once everyone's recharged, stroll down Quinta Avenida (5th Avenue) — the famous pedestrian street that runs parallel to the beach. It's a sensory wonderland for kids: street performers, Mayan dancers, bright murals, and shops selling everything from mini sombreros to Mexican candy.",
              details: [
                '🎭 Street performers and living statues pop up throughout the evening',
                '🍦 Stop at Ah Cacao for artisanal chocolate and ice cream — kids go wild',
                '🛍️ Let the kids pick out a small souvenir from the artisan stalls',
                '🎨 Look for the colorful 3D street art photo ops along 5th Ave'
              ]
            }
          ],
          tips: [
            { type: 'tip', text: '5th Avenue is car-free, so kids can walk freely without worrying about traffic. The best stretch for families is between Calle 28 and Calle 40 — less crowded and more local shops.' }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🌮 Dinner',
              name: 'El Fogón',
              description: "Playa's best taco spot — period. This casual open-air restaurant serves incredible al pastor (spit-roasted pork with pineapple) and every kind of taco imaginable. Kids love the cheese quesadillas and the simple but delicious bean soup (Frijoles Charros). Portions are huge and prices are local.",
              meta: '💰 $ · 📍 Av. Constituyentes, between 30th & 35th Ave · No reservations needed'
            }
          ],
          activities: [
            {
              title: 'Sunset Beach Walk',
              description: "After dinner, walk down to the beach for sunset. The Caribbean sunsets are spectacular, and the kids can run along the waterline as the sky turns orange and pink. Grab a coconut from a beach vendor and share it as a family.",
              details: [
                '🌅 Sunset is around 6:30pm in March — beautiful golden light from 5:45pm',
                '🥥 Beach coconut vendors charge about 50-80 pesos — worth it for the experience'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.6308, lng: -87.0769, label: 'Abba Suites', num: 1, cat: 'hotel', desc: 'Your home base — 200m from beach, 100m from 5th Ave' },
        { lat: 20.6320, lng: -87.0785, label: 'Playa Mamitas', num: 2, cat: 'attraction', desc: 'Beautiful Caribbean beach with calm, shallow water for kids' },
        { lat: 20.6315, lng: -87.0740, label: 'Chez Celine', num: 3, cat: 'food', desc: 'French bakery — chocolate croissants and crêpes the kids will love' },
        { lat: 20.6300, lng: -87.0750, label: '5th Avenue', num: 4, cat: 'attraction', desc: 'Pedestrian street with shops, ice cream, and street performers' },
        { lat: 20.6295, lng: -87.0745, label: 'Ah Cacao', num: 5, cat: 'food', desc: 'Artisanal chocolate shop and café — amazing ice cream' },
        { lat: 20.6270, lng: -87.0720, label: 'El Fogón', num: 6, cat: 'food', desc: 'Best tacos in Playa — al pastor, quesadillas, bean soup' }
      ]
    },
    {
      num: 2,
      date: '2026-03-19',
      neighborhoods: 'Xcaret Eco-Park',
      title: 'Xcaret — Jungle Rivers, Butterflies & Mayan Magic',
      description: "Today is your big adventure day: Xcaret, the world-famous eco-archaeological park. Kids will float down underground rivers, walk through a butterfly pavilion bursting with color, meet tropical birds and monkeys, and explore a recreated Mayan village. The park includes snorkeling gear, life jackets, and buffet meals — everything is taken care of so you can just enjoy.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Arrive at Xcaret & Underground River Float',
              description: "Get to Xcaret right when it opens at 8:30am to beat the crowds. Head straight to the underground rivers — the park's signature experience. You'll float through crystal-clear water inside ancient limestone caverns. Life jackets are provided and the current is gentle, making it safe for kids.",
              details: [
                '🏊 Life jackets included and required — safe for kids ages 4+',
                '🌊 Three river routes: Río Maya is the calmest and best for young children',
                '👟 Water shoes are essential here — the river entries are rocky',
                '🎒 Rent a locker near the river entrance for your dry stuff ($)',
                '⏰ Arrive at 8:30am — the rivers are magical without crowds'
              ]
            },
            {
              title: 'Children\'s World',
              description: "Xcaret's dedicated kids area has water slides, splash pads, and mini obstacles designed for children. Let the kids burn off energy here while you relax in a nearby hammock. It's shaded and has shallow water areas perfect for a 4-year-old.",
              details: [
                '🎢 Water slides sized for small children — safe and fun',
                '💦 Splash pads and shallow pools',
                '🏝️ Shaded seating for parents nearby'
              ]
            }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Butterfly Pavilion & Aviary',
              description: "Walk through the lush butterfly pavilion — a giant netted garden filled with hundreds of colorful butterflies that land on your arms and shoulders. Kids are mesmerized. Then visit the aviary, where tropical macaws, toucans, and flamingos strut around freely.",
              details: [
                '🦋 The butterfly pavilion is best visited around 11am-1pm when butterflies are most active',
                '🦜 Macaws and toucans in the aviary — kids can get surprisingly close',
                '🦩 The flamingo pond is a great photo spot'
              ]
            },
            {
              title: 'Mayan Village & Snorkeling Cove',
              description: "Explore the recreated Mayan village to learn about ancient culture — kids love the traditional houses and watching craftspeople work. Then head to the natural snorkeling inlet where colorful fish swim in crystal-clear water. Snorkel gear is included with admission.",
              details: [
                '🏛️ The Mayan village has interactive displays that engage kids',
                '🐠 Snorkeling inlet has calm water and lots of tropical fish',
                '🤿 Snorkel equipment is included — kid sizes available',
                '📸 The inlet is gorgeous for underwater photos'
              ]
            }
          ],
          meals: [
            {
              type: '🍽️ Lunch',
              name: 'Xcaret Buffet (included)',
              description: 'Your park admission includes a full buffet lunch with Mexican and international options. Tacos, grilled meats, pasta, fresh fruit, and a dessert spread that will make the kids\' eyes go wide. Multiple restaurant options throughout the park.',
              meta: '💰 Included with admission · Multiple locations throughout the park'
            }
          ],
          tips: [
            { type: 'tip', text: 'Pace yourselves — Xcaret is huge and you can\'t do everything in one day. Focus on the rivers, butterflies, aviary, and Children\'s World. Skip the more intense activities (cliff diving shows, etc.) and save energy for the evening show.' }
          ]
        },
        {
          label: 'Evening',
          activities: [
            {
              title: 'Xcaret México Espectacular Night Show',
              description: "Stay for the incredible evening show — a 90-minute spectacle of traditional Mexican music, dance, and culture with over 300 performers. It's colorful, loud, and exciting enough to keep even a 4-year-old riveted. The show covers Mexico's history from pre-Hispanic times to modern day with stunning costumes and choreography.",
              details: [
                '🎭 Show starts at 7pm — grab seats by 6:30pm for good spots',
                '🪑 Bring a light jacket — the outdoor theater can get cool after sunset',
                '🌟 The grand finale with the flying dancers (voladores) is jaw-dropping',
                '🚌 Xcaret shuttle runs back to Playa del Carmen after the show'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.5807, lng: -87.1179, label: 'Xcaret Park Entrance', num: 1, cat: 'attraction', desc: 'Main entrance to Xcaret eco-archaeological park' },
        { lat: 20.5785, lng: -87.1145, label: 'Underground Rivers', num: 2, cat: 'attraction', desc: 'Float through crystal-clear underground river caverns' },
        { lat: 20.5795, lng: -87.1160, label: 'Children\'s World', num: 3, cat: 'attraction', desc: 'Water slides, splash pads, and play areas for kids' },
        { lat: 20.5810, lng: -87.1170, label: 'Butterfly Pavilion', num: 4, cat: 'attraction', desc: 'Walk-through garden with hundreds of colorful butterflies' },
        { lat: 20.5800, lng: -87.1155, label: 'Aviary & Flamingos', num: 5, cat: 'attraction', desc: 'Tropical birds, macaws, toucans, and flamingo pond' },
        { lat: 20.5790, lng: -87.1135, label: 'Snorkeling Inlet', num: 6, cat: 'attraction', desc: 'Natural cove with tropical fish — gear included' },
        { lat: 20.5815, lng: -87.1175, label: 'Mayan Village', num: 7, cat: 'attraction', desc: 'Recreated ancient Mayan settlement with interactive displays' }
      ]
    },
    {
      num: 3,
      date: '2026-03-20',
      neighborhoods: 'Cenote Azul · Cenote Cristalino · Playacar',
      title: 'Cenote Swimming & Last Beach Afternoon',
      description: "Your final day features one of the most magical experiences the Riviera Maya offers: swimming in a cenote — a natural sinkhole filled with crystal-clear freshwater. Cenote Azul is the most kid-friendly cenote near Playa, with shallow areas perfect for little ones. Spend the afternoon back at the beach for one last Caribbean swim before heading home.",
      timeBlocks: [
        {
          label: 'Morning',
          activities: [
            {
              title: 'Cenote Azul',
              description: "Take a taxi 20 minutes south to Cenote Azul — the best family-friendly cenote in the Riviera Maya. It's an open-air cenote surrounded by jungle, with both shallow wading areas for the 4-year-old and deeper swimming sections for the 7-year-old. The water is impossibly clear and a stunning shade of blue. Life jackets are available to rent.",
              details: [
                '💧 Crystal-clear freshwater — you can see the bottom even in deep sections',
                '👶 Multiple shallow areas where toddlers and small kids can wade safely',
                '🏊 Deeper sections (up to 10m) for jumping and swimming — with life jackets',
                '🧴 Only biodegradable/reef-safe sunscreen allowed — rinse off regular sunscreen before entering',
                '💰 Entry is about 200 pesos/adult, kids discounted · Life jackets ~50 pesos',
                '🚕 20 min taxi south on Highway 307 — about 200-300 pesos each way'
              ]
            },
            {
              title: 'Cenote Cristalino',
              description: "Right next door to Cenote Azul (same road, 2-minute walk) is Cenote Cristalino — a gorgeous semi-open cenote with a small waterfall and lush jungle surroundings. It has shallow areas and a hidden second cenote through a path in the back. The kids will feel like they're exploring a secret jungle pool.",
              details: [
                '🌿 More jungle-enclosed than Cenote Azul — feels like a hidden world',
                '💦 Small waterfall the kids can stand under',
                '🗺️ Follow the path behind the main cenote to find a hidden second pool',
                '📸 The light filtering through the jungle canopy makes incredible photos'
              ]
            }
          ],
          meals: [
            {
              type: '☕ Breakfast',
              name: 'Don Sirloin',
              description: 'Quick and hearty breakfast before cenote adventures. This casual chain restaurant serves great tacos, eggs, and fresh juices at local prices. The kids can get simple quesadillas or scrambled eggs.',
              meta: '💰 $ · 📍 Multiple locations in Playa · Opens early'
            }
          ],
          tips: [
            { type: 'tip', text: 'Visit the cenotes in the morning (before 11am) when they\'re less crowded and the light is beautiful. Bring water shoes — the entry paths are rocky. Pack snacks and water; there are small vendors at the cenotes but options are limited.' }
          ]
        },
        {
          label: 'Afternoon',
          activities: [
            {
              title: 'Playacar Beach',
              description: "For your last afternoon, head to Playacar Beach — a quieter, less crowded stretch of sand south of the main Playa del Carmen beach. The water is calm and shallow, perfect for the kids to splash around one last time. There are fewer vendors here, making it more peaceful for families.",
              details: [
                '🏖️ Wider, quieter beach than the main strip — great for families',
                '🐢 Keep your eyes open — sea turtles are sometimes spotted near Playacar',
                '🌴 The beach is lined with palm trees for natural shade',
                '🦎 Playacar has resident iguanas — kids love spotting them on the paths'
              ]
            },
            {
              title: 'Parque Fundadores',
              description: "If the kids still have energy, walk up to Parque Fundadores — the main plaza where 5th Avenue meets the beach. Watch the Voladores de Papantla (Papantla Flyers) perform their ancient ritual of spinning down from a tall pole. It happens several times daily and it's free to watch (tips appreciated). Kids are absolutely mesmerized.",
              details: [
                '🎭 Voladores perform multiple times daily — check for the schedule at the plaza',
                '📸 The Portal Maya sculpture is a great family photo spot',
                '🍦 Grab one last ice cream or paleta from the vendors nearby'
              ]
            }
          ]
        },
        {
          label: 'Evening',
          meals: [
            {
              type: '🌮 Dinner',
              name: 'Carboncitos',
              description: "End your trip at Carboncitos — an authentic Mexican restaurant beloved by families. The chicken mole enchiladas are legendary, and the kids' menu has familiar favorites like chicken fingers alongside Mexican classics. They bring out complimentary tortillas with dips to start, plus crayons and coloring placemats for the kids.",
              meta: '💰 $$ · 📍 Calle 4 Norte, off 5th Avenue · Outdoor covered seating'
            }
          ],
          activities: [
            {
              title: 'Last Evening Stroll',
              description: "Take one final family walk down 5th Avenue as the street comes alive with evening energy. Let the kids pick out a last souvenir, grab churros from a street vendor, and soak in the warm Playa del Carmen night. The perfect ending to a perfect family trip.",
              details: [
                '🎵 Live music spills out of restaurants along 5th Ave in the evening',
                '🍩 Churros con chocolate from street vendors — the ultimate kid treat',
                '❤️ Playa has a way of making families promise to come back'
              ]
            }
          ]
        }
      ],
      mapPins: [
        { lat: 20.4917, lng: -87.2278, label: 'Cenote Azul', num: 1, cat: 'attraction', desc: 'Best family-friendly cenote — shallow wading areas for kids' },
        { lat: 20.4925, lng: -87.2265, label: 'Cenote Cristalino', num: 2, cat: 'attraction', desc: 'Semi-open jungle cenote with waterfall and hidden pool' },
        { lat: 20.6270, lng: -87.0720, label: 'Don Sirloin', num: 3, cat: 'food', desc: 'Casual tacos and breakfast at local prices' },
        { lat: 20.6215, lng: -87.0755, label: 'Playacar Beach', num: 4, cat: 'attraction', desc: 'Quiet, family-friendly beach with calm shallow water' },
        { lat: 20.6300, lng: -87.0793, label: 'Parque Fundadores', num: 5, cat: 'attraction', desc: 'Main plaza with Voladores performance and Portal Maya sculpture' },
        { lat: 20.6335, lng: -87.0735, label: 'Carboncitos', num: 6, cat: 'food', desc: 'Authentic Mexican — mole enchiladas, kids menu, crayons' }
      ]
    }
  ],

  budgetTable: [
    { category: 'Meals (family of 4)', budget: '$30–50/day', midrange: '$50–80/day', luxury: '$100–150/day' },
    { category: 'Transport (taxis)', budget: '$15–25/day', midrange: '$30–50/day', luxury: '$60–100/day (private)' },
    { category: 'Xcaret Park', budget: '—', midrange: '$120 adult / $60 kid', luxury: '$180+ (Plus package)' },
    { category: 'Cenotes', budget: '$10–15pp', midrange: '$15–20pp', luxury: '$25+ (private tour)' },
    { category: 'Beach Gear/Tips', budget: '$5–10/day', midrange: '$15–25/day', luxury: '$30+/day' },
    { category: '3-Day Total (family of 4)', budget: '$400–600', midrange: '$700–1,200', luxury: '$1,500–2,500' }
  ],

  practicalInfo: [
    { title: '✈️ Getting There', items: ['Fly into Cancún International Airport (CUN) — about 55 min drive south to Playa del Carmen', 'ADO bus from Cancún airport to Playa: ~$12 USD, runs frequently, kid-friendly', 'Private transfer services (USA Transfers, Canada Transfers) run $60-80 USD for families', 'Rental cars are available but not necessary for a Playa-focused trip'] },
    { title: '💰 Money', items: ['Mexican pesos preferred — better prices than paying in USD', 'ATMs on 5th Avenue dispense pesos (use bank ATMs inside buildings, not street ones)', 'Most restaurants and attractions accept credit cards', 'Tipping 10-15% at restaurants, 20+ pesos for good taxi service', 'Cenotes and small vendors are often cash-only'] },
    { title: '🌡️ Weather in March', items: ['Average highs of 29-31°C (84-88°F) with warm evenings', 'Low chance of rain in March — peak dry season', 'Humidity is moderate — carry water and take shade breaks with kids', 'Ocean water is around 26°C (79°F) — perfect for swimming'] },
    { title: '👨‍👩‍👧‍👦 Family Tips', items: ['Abba Suites location is ideal — walkable to beach and 5th Avenue', 'Pack biodegradable sunscreen — required at cenotes and eco-parks (regular sunscreen damages the ecosystem)', 'Bring water shoes for everyone — essential for cenotes and rocky beach entries', 'OXXO convenience stores are everywhere for snacks, water, and sunscreen', 'Pharmacias sell kid-safe bug spray and common medicines if you forget anything', 'March is spring break season — book Xcaret tickets online in advance for best prices'] }
  ]
};

try {
  const result = fulfillOrder(order, itineraryData);
  console.log('✅ Fulfilled:', JSON.stringify(result, null, 2));
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
